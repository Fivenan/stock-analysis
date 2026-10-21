"""Independent acceptance at UI persistence, export and public-build boundaries."""
from datetime import date
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import socket
import subprocess

import pytest
from streamlit.testing.v1 import AppTest

from gmrl.analytics.export import result_json
from gmrl.execution.paper import InternalPaperBroker
from gmrl.storage.repository import Repository


def start(tmp_path, monkeypatch):
    monkeypatch.setenv("GMRL_RUNTIME", str(tmp_path / "runtime"))
    return AppTest.from_file(str(Path("app/main.py").resolve()), default_timeout=90).run()


def click(at, label):
    next(item for item in at.button if item.label == label).click().run()
    assert not at.exception


def number(at, label):
    return next(item for item in at.number_input if item.label == label)


def test_offline_run_export_frozen_config_and_changed_parameter_rerun(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Offline acceptance attempted network access")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    at = start(tmp_path, monkeypatch)
    at.sidebar.radio[0].set_value("Backtesting Lab").run()
    number(at, "Initial capital EUR").set_value(12000.0).run()
    click(at, "Run backtest and benchmark")
    result, benchmark, data, config, parameters = at.session_state.run
    exported = result_json(result, data, config, parameters)
    document = json.loads(exported)
    assert document["conventions"]["currency"] == "EUR"
    assert document["provenance"] and document["fills"] and document["warnings"]
    assert document["config"]["initial_cash_eur"] == "12000.0"
    assert result.equity.iloc[0].equity_eur == benchmark.equity.iloc[0].equity_eur == 12000
    assert document["metrics"]["max_drawdown"] <= 0
    number(at, "Initial capital EUR").set_value(15000.0).run()
    assert result_json(at.session_state.run[0], at.session_state.run[2],
                       at.session_state.run[3], at.session_state.run[4]) == exported
    click(at, "Run backtest and benchmark")
    updated = at.session_state.run
    assert updated[3].initial_cash_eur == Decimal("15000")
    assert updated[0].experiment_id != result.experiment_id
    assert updated[1].equity.iloc[0].equity_eur == 15000
    # Invalid controls must not replace the last completed report.
    next(item for item in at.date_input if item.label == "Start date").set_value(date(2025, 12, 31)).run()
    next(item for item in at.date_input if item.label == "End date").set_value(date(2024, 1, 2)).run()
    click(at, "Run backtest and benchmark")
    assert at.error and at.session_state.run[0].experiment_id == updated[0].experiment_id


def test_empty_account_guidance_and_risk_uses_saved_fill_cursor(tmp_path, monkeypatch):
    import gmrl.risk.scenarios as scenarios

    observed = []
    original = scenarios.risk_snapshot

    def capture(state, data, at, limits, **kwargs):
        observed.append(at)
        return original(state, data, at, limits, **kwargs)

    monkeypatch.setattr(scenarios, "risk_snapshot", capture)
    at = start(tmp_path, monkeypatch)
    repository = Repository(tmp_path / "runtime")
    for page in ("Risk Dashboard", "Trade Journal"):
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception
        assert any("Initialize" in item.value for item in at.error)
        with repository.paper_transaction() as tx:
            assert tx.load_account() is None
    at.sidebar.radio[0].set_value("Paper Trading").run()
    click(at, "Initialize paper account")
    click(at, "Submit simulated order")
    broker = InternalPaperBroker(repository, Decimal("10000"))
    before = broker.history()
    at.sidebar.radio[0].set_value("Risk Dashboard").run()
    at.slider[0].set_value(-50).run()
    assert not at.exception
    assert observed and all(cursor == before.snapshot.simulation_time for cursor in observed)
    assert broker.history() == before
    at.sidebar.radio[0].set_value("Paper Trading").run()
    click(at, "Replay persisted canonical order")
    assert broker.history() == before and len(before.fills) == 1


def test_static_private_sentinel_unexpected_file_and_unsafe_links(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("acceptance_builder", "scripts/build_static.py")
    assert spec and spec.loader
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    # An isolated public source tree permits private and malformed-output probes safely.
    root = tmp_path / "project"
    (root / "docs").mkdir(parents=True)
    fixture = root / "tests/fixtures/financial_reports"
    fixture.mkdir(parents=True)
    (fixture / "summary.json").write_text("{}", encoding="utf-8")
    for name in builder.DOCS:
        (root / "docs" / (name + ".md")).write_text("Public synthetic guide", encoding="utf-8")
    (root / ".runtime").mkdir()
    sentinel = "PRIVATE-ACCEPTANCE-SENTINEL-DO-NOT-PUBLISH"
    (root / ".runtime/account.json").write_text(sentinel, encoding="utf-8")
    monkeypatch.setattr(builder, "ROOT", root)
    output = builder.build()
    assert all(sentinel.encode() not in file.read_bytes() for file in output.rglob("*") if file.is_file())
    unwanted = output / "private.json"
    unwanted.write_text(sentinel, encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected output"):
        builder.build()
    for link in ("//example.test/a", "http://example.test/a", "file:///private", "../USER_GUIDE.md",
                 "https://name:secret@example.test/a", "javascript:alert"):
        assert "<a " not in builder.document_text(f"[unsafe]({link})")


def test_static_refuses_real_windows_junction_before_writing(tmp_path, monkeypatch):
    import sys

    if sys.platform != "win32":
        pytest.skip("Native Windows junction acceptance")
    spec = importlib.util.spec_from_file_location("junction_builder", "scripts/build_static.py")
    assert spec and spec.loader
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    root = tmp_path / "project"
    private = root / "build/private"
    private.mkdir(parents=True)
    site = root / "build/site"
    # Temporary fixture paths are supplied as environment values, not executable shell text.
    import os

    env = {**os.environ, "ACCEPTANCE_JUNCTION": str(site), "ACCEPTANCE_TARGET": str(private)}
    subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                    "New-Item -ItemType Junction -Path $env:ACCEPTANCE_JUNCTION "
                    "-Target $env:ACCEPTANCE_TARGET | Out-Null"],
                   env=env, check=True, capture_output=True)
    assert site.is_junction() and not site.is_symlink()
    monkeypatch.setattr(builder, "ROOT", root)
    with pytest.raises(ValueError, match="build/site"):
        builder.build()
    assert not list(private.iterdir())
