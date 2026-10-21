"""Independent native-runtime foundation checks with all network access forbidden."""
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from zoneinfo import ZoneInfo
import socket

import pyarrow.parquet as pq
import pytest

from gmrl.domain import DatasetRequest, ProviderStatus, RatePolicy
from gmrl.errors import DataUnavailableError
from gmrl.providers.cache import CachedProvider
from gmrl.providers.sample import load_demo
from gmrl.storage.repository import Repository


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Foundation integration attempted network access")
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)


@pytest.fixture(scope="module")
def demo():
    # Module fixtures precede function fixtures, so guard generation explicitly too.
    from unittest.mock import patch
    with patch("socket.socket", side_effect=AssertionError("Demo attempted network")):
        return load_demo()


def test_every_venue_session_matches_iana_local_clock_and_dst(demo):
    assert len(demo.instruments) == 9
    assert len(demo.sessions) == len(demo.bars) == 4671
    zones = {listing.instrument_id: ZoneInfo(listing.timezone) for listing in demo.instruments}
    for session in demo.sessions:
        local_open = session.open_at.astimezone(zones[session.instrument_id])
        local_close = session.close_at.astimezone(zones[session.instrument_id])
        assert local_open.date() == local_close.date() == session.session_date
        assert (local_open.hour, local_open.minute) == (9, 0)
        assert (local_close.hour, local_close.minute) == (16, 0)
        assert session.session_date.weekday() < 5
        assert (session.session_date.month, session.session_date.day) not in ((1, 1), (12, 25))
    sessions = {(s.instrument_id, s.session_date): s for s in demo.sessions}
    # US and European DST change on different dates; test both and autumn reversal.
    for ident, day, utc_hour in (
        ("DEMO-US", date(2025, 3, 7), 14), ("DEMO-US", date(2025, 3, 10), 13),
        ("DEMO-DE", date(2025, 3, 28), 8), ("DEMO-DE", date(2025, 3, 31), 7),
        ("DEMO-DE", date(2025, 10, 24), 7), ("DEMO-DE", date(2025, 10, 27), 8),
        ("DEMO-US", date(2025, 10, 31), 13), ("DEMO-US", date(2025, 11, 3), 14),
        ("DEMO-JP", date(2025, 3, 31), 0),
    ):
        assert sessions[ident, day].open_at.hour == utc_hour


def test_real_parquet_roundtrip_restart_and_hash_tamper_rejection(tmp_path, demo):
    repository = Repository(tmp_path)
    key = repository.save_dataset(demo)
    assert key == "fb6ca5c5cc54aae1181c1c0242afdc6aa1b3c42b670a22b6ad3a2d7ac0f69fcf"
    assert Repository(tmp_path).load_dataset(key) == demo
    # Store a different, valid dataset at this identity: integrity must reject it.
    changed_bar = replace(demo.bars[0], volume=demo.bars[0].volume + Decimal(1))
    changed = replace(demo, bars=(changed_bar,) + demo.bars[1:])
    changed_key = repository.save_dataset(changed)
    source = tmp_path / "datasets" / (changed_key + ".parquet")
    target = tmp_path / "datasets" / (key + ".parquet")
    pq.write_table(pq.read_table(source), target)
    with pytest.raises(DataUnavailableError, match="hash mismatch"):
        Repository(tmp_path).load_dataset(key)


def test_actual_cache_survives_restart_and_retains_research_freshness(tmp_path, demo):
    now = datetime(2026, 10, 20, tzinfo=timezone.utc)

    class Provider:
        quota = None
        calls = 0

        def status(self):
            return ProviderStatus("offline-integration", True, "synthetic", self.calls, self.quota)

        def fetch(self, request):
            self.calls += 1
            return demo

    provider = Provider()
    def cache(repository):
        return CachedProvider(provider, repository, 60, clock=lambda: now,
                              sleep=lambda seconds: None, random=lambda: .5,
                              rate_policy=RatePolicy(3, 1, 10))
    repository = Repository(tmp_path)
    request = DatasetRequest(tuple(i.instrument_id for i in demo.instruments),
                             date(2024, 1, 1), date(2025, 12, 31))
    original = cache(repository).fetch(request)
    assert original.cache_status == "miss"
    assert repository.load_dataset(original.dataset_id) == demo
    restarted = cache(Repository(tmp_path))
    hit = restarted.fetch(request)
    assert hit.cache_status == "hit" and hit.data == demo
    assert max(b.available_at for b in hit.data.bars) < hit.retrieved_at
    assert hit.retrieved_at == original.retrieved_at
    now += timedelta(seconds=61)
    provider.quota = 0
    stale = restarted.fetch(request)
    assert stale.cache_status == "stale" and stale.data == demo
    assert stale.retrieved_at == original.retrieved_at
    assert stale.expires_at == original.expires_at
    assert any("cannot authorize fills" in warning for warning in stale.warnings)
    assert provider.calls == 1
    persisted = Repository(tmp_path)
    assert persisted.provider_status()[0].used_requests == 1
    assert persisted.provider_status()[0].quota_remaining is None
    assert set(persisted.usage_stats()) == {
        ("offline-integration", "success", 1, 1),
        ("offline-integration", "cache_hit", 1, 0),
        ("offline-integration", "refresh_blocked", 1, 0),
    }


def test_experiment_read_apis_are_lossless_and_isolated_after_restart(tmp_path):
    repository = Repository(tmp_path)
    manifest = {"capital": Decimal("1.123456789012345678901234567"),
                "parameters": {"universe": ("DEMO-X",)}, "warnings": ("synthetic",)}
    key = repository.save_experiment(manifest)
    restarted = Repository(tmp_path)
    assert restarted.load_experiment(key) == manifest
    assert restarted.list_experiments() == (manifest,)
    loaded = restarted.load_experiment(key)
    loaded["parameters"]["universe"] = ("changed",)
    assert restarted.load_experiment(key) == manifest
    with pytest.raises(DataUnavailableError, match="not found"):
        restarted.load_experiment("absent")
