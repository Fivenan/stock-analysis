"""Executed with the approved Pandas/NumPy environment."""
from dataclasses import replace
from datetime import date
from decimal import Decimal as D
import json

import numpy as np
import pandas as pd
import pytest

from gmrl.analytics.export import equity_csv, fills_csv, result_json
from gmrl.analytics.metrics import calculate_metrics, periodic_returns
from gmrl.backtesting.engine import run_backtest
from gmrl.domain import BacktestConfig, CorporateAction, MarketData, RealizedMatch, TargetWeights
from gmrl.errors import DataUnavailableError, DataValidationError
from gmrl.strategies.factory import make_strategy
from test_financial_stdlib import LIMITS, ZERO_COST, fixture, stamp


def config(end: int = 5, cash: str = "1000") -> BacktestConfig:
    return BacktestConfig(D(cash), date(2025, 1, 1), date(2025, 1, end),
                          ZERO_COST, LIMITS, False)


class Half:
    rebalance = "once"

    def weights(self, history, decided_at):
        assert all(b.close_at <= decided_at and b.available_at <= decided_at for b in history.bars)
        assert all(q.available_at <= decided_at for q in history.fx)
        return TargetWeights(decided_at, ((history.instruments[0].instrument_id, D("0.5")),))


def test_next_open_frozen_quantity_and_initial_equity():
    result = run_backtest(fixture(), Half(), config())
    assert len(result.fills) == 1
    assert result.fills[0].price_local == 110
    assert result.fills[0].quantity == 5
    assert result.fills[0].filled_at == stamp(2, 9)
    assert result.equity.iloc[0].equity_eur == 1000
    assert len(result.equity) == 6
    assert result.equity.timestamp.is_monotonic_increasing
    assert run_backtest(fixture(), Half(), config()).experiment_id == result.experiment_id


def test_future_hlcv_and_fx_do_not_change_earlier_decisions_or_fills():
    data = fixture()
    baseline = run_backtest(data, Half(), config())
    bars = tuple(replace(b, high=b.high * 20, low=b.low / 10, volume=D(1),
                         close=D(150) if b.session_date.day >= 3 else b.close)
                 if b.session_date.day >= 2 else b for b in data.bars)
    mutated = run_backtest(replace(data, bars=bars), Half(), config())
    assert mutated.fills[0] == baseline.fills[0]


def test_execution_gap_rejects_not_resizes():
    data = fixture(("100", "200", "200", "200", "200"))
    result = run_backtest(data, make_strategy("buy_hold", {}), config())
    assert not result.fills
    assert any("Insufficient cash" in warning for warning in result.warnings)


def test_expected_missing_open_cancelled():
    data = fixture()
    data = replace(data, bars=(data.bars[0],) + data.bars[2:])
    result = run_backtest(data, Half(), config())
    assert not result.fills
    assert any("never deferred" in warning for warning in result.warnings)


def test_dates_strictly_bound_fills_and_daily_rows():
    data = fixture()
    result = run_backtest(data, Half(), replace(config(3), start=date(2025, 1, 2)))
    assert len(result.equity) == 3
    assert all(date(2025, 1, 2) <= f.filled_at.date() <= date(2025, 1, 3) for f in result.fills)


def test_split_and_dividend_neutral_equity_and_no_double_counting():
    data = fixture(("100", "100", "50", "49", "49"))
    split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(3, 8), stamp(1), D(2), None)
    dividend = CorporateAction("D", "SYNTHETIC-A", "dividend", stamp(4, 8), stamp(1), D(1), stamp(5, 8))
    result = run_backtest(replace(data, actions=(split, dividend)), Half(), config())
    assert result.equity.equity_eur.tolist() == [1000.0] * 6
    assert result.equity.iloc[-1].cash_eur == 510


def test_late_actions_fail_run():
    data = fixture()
    action = CorporateAction("S", "SYNTHETIC-A", "split", stamp(3), stamp(4), D(2), None)
    with pytest.raises(DataValidationError):
        run_backtest(replace(data, actions=(action,)), Half(), config())


def test_stale_holding_blocks_valuation_instead_of_fabricating():
    data = fixture()
    data = replace(data, bars=data.bars[:2])
    with pytest.raises(DataUnavailableError):
        run_backtest(data, Half(), replace(config(), limits=replace(LIMITS, max_price_age_hours=24)))


def test_holiday_is_mark_only_and_has_no_execution():
    a = fixture(("100",) * 5)
    b = fixture(("100",) * 5, ident="SYNTHETIC-B", open_hour=12)
    # A has an explicit holiday on day 3; B supplies the union valuation date.
    a = replace(a, sessions=tuple(s for s in a.sessions if s.session_date.day != 3),
                bars=tuple(bar for bar in a.bars if bar.session_date.day != 3))
    data = MarketData(a.instruments + b.instruments, a.sessions + b.sessions,
                      a.bars + b.bars, (), a.fx, a.provenance)
    result = run_backtest(data, Half(), config())
    assert bool(result.equity.iloc[3].stale)
    assert not any(f.filled_at.day == 3 for f in result.fills)


def test_costs_reduce_initial_return_once_and_exports():
    data = fixture(("100",) * 5)
    cfg = replace(config(), costs=replace(ZERO_COST, fixed_fee_eur=D(1)))
    result = run_backtest(data, Half(), cfg)
    assert result.equity.iloc[0].equity_eur == 1000
    assert result.equity.iloc[-1].equity_eur == 999
    assert result.metrics["total_return"] == pytest.approx(-0.001)
    report = json.loads(result_json(result, data, cfg, {"name": "half"}))
    assert D(report["fills"][0]["fee_eur"]) == D(1)
    assert "timestamp" in equity_csv(result)
    assert "fill_id" in fills_csv(result)


def metric_frame(values, dates=None):
    return pd.DataFrame({"timestamp": pd.to_datetime(dates or [
        f"2025-01-{n + 1:02d}T23:59:59Z" for n in range(len(values))]),
        "equity_eur": values, "cash_eur": values, "exposure": [0.] * len(values),
        "external_flow_eur": [0.] * len(values), "stale": [False] * len(values)})


def test_flat_metrics_are_undefined_not_infinite():
    metrics = calculate_metrics(metric_frame([100, 100, 100]), (), ())
    assert metrics["sharpe"] is None
    assert metrics["sortino"] is None
    assert metrics["calmar"] is None
    assert metrics["max_drawdown"] == 0
    assert metrics["drawdown_duration_days"] == 0


def test_metric_formula_sample_std_sortino_and_calendar_cagr():
    frame = metric_frame([100, 110, 88, 100])
    metrics = calculate_metrics(frame, (), ())
    returns = np.array([.1, -.2, 100 / 88 - 1])
    assert metrics["annualized_volatility"] == pytest.approx(returns.std(ddof=1) * np.sqrt(252))
    assert metrics["sortino"] == pytest.approx(
        returns.mean() / np.sqrt(np.mean(np.minimum(returns, 0) ** 2)) * np.sqrt(252))
    assert metrics["max_drawdown"] == pytest.approx(-.2)
    assert metrics["drawdown_duration_days"] == 2
    assert metrics["unrecovered_drawdown"] == 1
    assert metrics["cagr"] == 0


def test_monthly_compounding_and_flow_rejection():
    frame = metric_frame([100, 110, 121, 108.9], [
        "2025-01-01Z".replace("Z", "T00:00:00Z"),
        "2025-01-30T23:59:59Z", "2025-01-31T23:59:59Z", "2025-02-01T23:59:59Z"])
    periods = periodic_returns(frame)
    assert periods.iloc[0] == pytest.approx(.21)
    assert periods.iloc[1] == pytest.approx(-.1)
    frame.loc[2, "external_flow_eur"] = 10
    with pytest.raises(DataValidationError):
        calculate_metrics(frame, (), ())


def test_fifo_metric_denominators_use_ledger_matches():
    matches = (
        RealizedMatch("A", stamp(1), stamp(3), D(2), D(100), D(120), D(20)),
        RealizedMatch("A", stamp(1), stamp(5), D(1), D(50), D(40), D(-10)),
    )
    metrics = calculate_metrics(metric_frame([100, 110, 105]), (), matches)
    assert metrics["win_rate"] == .5
    assert metrics["profit_factor"] == 2
    assert metrics["closed_fifo_match_count"] == 2
    assert metrics["trade_count"] == 0
    assert metrics["average_holding_days"] == 3


def test_later_venue_sales_cannot_fund_early_buys():
    a = fixture(("100",) * 5, ident="ASIA", open_hour=1)
    b = fixture(("100",) * 5, ident="EUROPE", open_hour=9)
    data = MarketData(a.instruments + b.instruments, a.sessions + b.sessions,
                      a.bars + b.bars, (), a.fx, a.provenance)

    class Switch:
        def weights(self, history, decided_at):
            ident = "EUROPE" if decided_at.day == 1 else "ASIA"
            return TargetWeights(decided_at, ((ident, D(1)),))

    result = run_backtest(data, Switch(), config())
    assert [(f.instrument_id, f.side, f.filled_at.day) for f in result.fills[:3]] == [
        ("EUROPE", "buy", 2), ("EUROPE", "sell", 3), ("ASIA", "buy", 4)]
    assert result.equity.cash_eur.min() >= 0
