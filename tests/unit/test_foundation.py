from dataclasses import replace
from datetime import datetime, timezone, timedelta, date
from decimal import Decimal as D
from concurrent.futures import ThreadPoolExecutor
import socket
import pytest
from gmrl.domain import (
    AccountState,
    PaperState,
    JournalEntry,
    ProviderStatus,
    RatePolicy,
    DatasetRequest,
)
from gmrl.providers.sample import load_demo
from gmrl.providers.cache import CachedProvider, canonical_request_key
from gmrl.data.validation import validate_market_data, session_gaps
from gmrl.data.csv_import import import_bars_csv
from gmrl.storage.repository import Repository
from gmrl.storage.codec import dumps, loads
from gmrl.errors import (
    AccountingError,
    DataValidationError,
    AuthenticationError,
    TransientProviderError,
)


@pytest.fixture(scope="module")
def demo():
    return load_demo()


def test_offline_determinism(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Network forbidden")

    monkeypatch.setattr(socket, "socket", forbidden)
    a = load_demo()
    b = load_demo()
    assert a == b and len(a.instruments) == 9 and (len(a.bars) > 4500)
    assert all((i.isin is None and i.instrument_id.startswith("DEMO-") for i in a.instruments))
    assert not session_gaps(a)
    assert any((s.open_at.utcoffset() == timedelta(0) for s in a.sessions))


def test_validation(demo):
    b = demo.bars[0]
    for altered in (
        replace(b, high=D("0")),
        replace(b, volume=D("NaN")),
        replace(b, price_basis="adjusted"),
        replace(b, available_at=b.open_at),
        replace(b, open_at=b.open_at.replace(tzinfo=None)),
    ):
        with pytest.raises(DataValidationError):
            validate_market_data(replace(demo, bars=(altered,)))
    with pytest.raises(DataValidationError):
        validate_market_data(replace(demo, bars=(b, b)))
    assert session_gaps(replace(demo, bars=demo.bars[1:]))
    with pytest.raises(DataValidationError):
        validate_market_data(replace(demo, fx=(replace(demo.fx[0], eur_per_unit=D(0)),)))
    with pytest.raises(DataValidationError):
        validate_market_data(
            replace(
                demo,
                actions=(
                    replace(
                        demo.actions[0],
                        available_at=demo.actions[0].effective_at + timedelta(seconds=1),
                    ),
                ),
            )
        )


def test_codec_and_repository(tmp_path, demo):
    repo = Repository(tmp_path)
    key = repo.save_dataset(demo)
    assert repo.load_dataset(key) == demo
    value = AccountState(D("0.1234567890123456789012345678"), (("DEMO-US", D("1.000001")),))
    assert loads(dumps(value)) == value
    assert repo.save_dataset(demo) == key
    assert repo.save_experiment({"dataset_id": key}) == repo.experiments()[0][0]


def state(version=0):
    return PaperState(
        AccountState(D(1000), ()), D(1000), version, datetime(2025, 1, 1, tzinfo=timezone.utc), ()
    )


def test_rollback_and_versions(tmp_path):
    repo = Repository(tmp_path)
    with pytest.raises(RuntimeError):
        with repo.paper_transaction() as tx:
            tx.save_account(state(), expected_version=None)
            tx.append_journal(
                JournalEntry("j", None, "hypothesis", "lesson", state().simulation_time)
            )
            raise RuntimeError("Injected crash")
    with repo.paper_transaction() as tx:
        assert tx.load_account() is None and tx.journal() == ()
        tx.save_account(state(), expected_version=None)
    with pytest.raises(AccountingError):
        with repo.paper_transaction() as tx:
            tx.save_account(state(1), expected_version=None)

    def change(_):
        try:
            with repo.paper_transaction() as tx:
                tx.save_account(state(1), expected_version=0)
            return True
        except AccountingError:
            return False

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sum(pool.map(change, range(2))) == 1
    with Repository(tmp_path).paper_transaction() as tx:
        assert tx.load_account().version == 1


def test_csv(tmp_path, demo):
    import csv

    bar = demo.bars[0]
    keys = [
        "instrument_id",
        "session_date",
        "open_at",
        "close_at",
        "available_at",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "price_basis",
    ]
    path = tmp_path / "bars.csv"
    with path.open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerow({k: str(getattr(bar, k)) for k in keys})
    assert import_bars_csv(path, demo.instruments, demo.provenance[0]) == (bar,)
    path.write_text(path.read_text().replace("raw", "adjusted"))
    with pytest.raises(DataValidationError):
        import_bars_csv(path, demo.instruments, demo.provenance[0])


class Clock:
    def __init__(self):
        self.at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def now(self):
        return self.at

    def sleep(self, seconds):
        self.at += timedelta(seconds=seconds)


def test_cache_retry_quota(tmp_path, demo):
    clock = Clock()
    repo = Repository(tmp_path)

    class Provider:
        calls = 0

        def status(self):
            return ProviderStatus("fake", True, "test", 0, None)

        def fetch(self, request):
            self.calls += 1
            if self.calls < 3:
                raise TransientProviderError("retry", 0.1)
            return demo

    provider = Provider()
    cache = CachedProvider(
        provider,
        repo,
        60,
        clock=clock.now,
        sleep=clock.sleep,
        random=lambda: 0.5,
        rate_policy=RatePolicy(10, 1, 10),
    )
    req = DatasetRequest(("DEMO-US",), date(2024, 1, 1), date(2025, 12, 31))
    first = cache.fetch(req)
    assert provider.calls == 3 and first.cache_status == "miss"
    assert cache.fetch(req).cache_status == "hit" and provider.calls == 3
    assert repo.provider_status()[0].used_requests == 3
    assert canonical_request_key(
        "fake", replace(req, instrument_ids=("a", "b", "a"))
    ) == canonical_request_key("fake", replace(req, instrument_ids=("b", "a")))
    clock.sleep(61)

    def fail(request):
        raise TransientProviderError("outage")

    provider.fetch = fail
    assert cache.fetch(req).cache_status == "stale"


def test_auth_no_retry(tmp_path):
    clock = Clock()

    class Provider:
        calls = 0

        def status(self):
            return ProviderStatus("auth", True, "test", 0, None)

        def fetch(self, request):
            self.calls += 1
            raise AuthenticationError("No access")

    provider = Provider()
    cache = CachedProvider(
        provider,
        Repository(tmp_path),
        60,
        clock=clock.now,
        sleep=clock.sleep,
        random=lambda: 0,
        rate_policy=RatePolicy(1, 1, 10),
    )
    with pytest.raises(AuthenticationError):
        cache.fetch(DatasetRequest((), date(2025, 1, 1), date(2025, 1, 2)))
    assert provider.calls == 1


def test_synthetic_calendar_dst_is_explicit(demo):
    sessions = {s.session_date: s for s in demo.sessions if s.instrument_id == "DEMO-DE"}
    assert sessions[date(2025, 3, 28)].open_at.hour == 8
    assert sessions[date(2025, 3, 31)].open_at.hour == 7
    assert date(2025, 1, 1) not in sessions
    assert date(2025, 12, 25) not in sessions
