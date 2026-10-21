from pathlib import Path

from streamlit.testing.v1 import AppTest


def app(tmp_path, monkeypatch):
    monkeypatch.setenv("GMRL_RUNTIME", str(tmp_path / "runtime"))
    return AppTest.from_file(str(Path("app/main.py").resolve()), default_timeout=90).run()


def button(at, label):
    return next(b for b in at.button if b.label == label)


def test_all_pages_and_offline_test(tmp_path, monkeypatch):
    at = app(tmp_path, monkeypatch)
    pages = list(at.sidebar.radio[0].options)
    assert len(pages) == 12
    for page in pages:
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page, at.exception)
    at.sidebar.radio[0].set_value("API Management").run()
    button(at, "Run offline adapter test").click().run()
    assert at.success


def test_backtest_save_compare_asset_and_invalid(tmp_path, monkeypatch):
    at = app(tmp_path, monkeypatch)
    at.sidebar.radio[0].set_value("Asset Research").run()
    at.selectbox[0].set_value("DEMO-US").run()
    assert not at.exception
    at.sidebar.radio[0].set_value("Backtesting Lab").run()
    at.selectbox[0].set_value("momentum").run()
    button(at, "Run backtest and benchmark").click().run()
    assert not at.exception
    assert "run" in at.session_state
    assert len(at.session_state.run[0].equity) > 500
    button(at, "Save experiment").click().run()
    compare = next(x for x in at.multiselect if x.label == "Compare saved experiments")
    assert compare.options
    compare.set_value(compare.options).run()
    assert not at.exception
    assert len(at.get("download_button")) == 3
    next(x for x in at.multiselect if x.label == "Universe").set_value([]).run()
    button(at, "Run backtest and benchmark").click().run()
    assert at.error


def test_paper_replay_journal_restart(tmp_path, monkeypatch):
    at = app(tmp_path, monkeypatch)
    at.sidebar.radio[0].set_value("Paper Trading").run()
    button(at, "Initialize paper account").click().run()
    button(at, "Submit simulated order").click().run()
    assert at.success and not at.exception
    button(at, "Submit simulated order").click().run()
    assert at.success and not at.exception
    from gmrl.execution.paper import InternalPaperBroker
    from gmrl.storage.repository import Repository
    from decimal import Decimal
    account = InternalPaperBroker(Repository(tmp_path / "runtime"), Decimal("10000"))
    assert len(account.history().fills) == 1
    at.sidebar.radio[0].set_value("Trade Journal").run()
    at.text_area[0].set_value("Test hypothesis and entry/exit plan").run()
    button(at, "Append journal entry").click().run()
    assert len(account.history().journal) == 1
    restarted = app(tmp_path, monkeypatch)
    restarted.sidebar.radio[0].set_value("Paper Trading").run()
    assert not restarted.exception
    assert len(account.history().fills) == 1
    restarted.sidebar.radio[0].set_value("Risk Dashboard").run()
    assert not restarted.exception
    restarted.sidebar.radio[0].set_value("Paper Trading").run()
    button(restarted, "Replay persisted canonical order").click().run()
    assert restarted.success and len(account.history().fills) == 1
    next(x for x in restarted.number_input if x.label == "Quantity").set_value(1000000.0).run()
    button(restarted, "Submit simulated order").click().run()
    assert restarted.error and len(account.history().fills) == 1


def test_invalid_allocation_and_empty_asset_dates(tmp_path, monkeypatch):
    at = app(tmp_path, monkeypatch)
    at.sidebar.radio[0].set_value("Portfolio Simulator").run()
    at.number_input[0].set_value(1.0).run()
    button(at, "Simulate allocation").click().run()
    assert at.error and not at.exception


def test_allocation_report_retains_original_parameters(tmp_path, monkeypatch):
    at = app(tmp_path, monkeypatch)
    at.sidebar.radio[0].set_value("Portfolio Simulator").run()
    button(at, "Simulate allocation").click().run()
    assert not at.exception
    original = at.session_state.allocation[2]
    at.selectbox[0].set_value("once").run()
    at.number_input[0].set_value(0.2).run()
    assert at.session_state.allocation[2] == original
    assert original["rebalance"] == "monthly"
    assert str(original["allocations"]["DEMO-US"]) == "0.1"
