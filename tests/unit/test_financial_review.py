"""Independent Step 8 golden cases; all prices and identities are synthetic."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal as D
from hashlib import sha256
from math import sqrt
from unittest.mock import patch

import pandas as pd
import pytest

from gmrl.analytics.metrics import calculate_metrics, periodic_returns
from gmrl.backtesting.engine import run_backtest
from gmrl.domain import (
    AccountState, BacktestConfig, Bar, CanonicalOrder, CorporateAction, CostModel,
    Fill, FXQuote, Instrument, JournalEntry, MarketData, OrderRequest, Provenance,
    RiskLimits, Session, TargetWeights,
)
from gmrl.errors import AccountingError, DataValidationError, GMRLError, OrderRejectedError
from gmrl.execution.paper import InternalPaperBroker
from gmrl.execution.timeline import advance_actions, opening_event
from gmrl.portfolio.accounting import apply_fill, check_state, settle_dividends
from gmrl.portfolio.simulation import simulate_allocation
from gmrl.portfolio.valuation import value_account
from gmrl.risk.scenarios import risk_snapshot
from gmrl.risk.validation import validate_execution
from gmrl.storage.codec import dumps
from gmrl.storage.repository import PaperTransaction, Repository
from gmrl.strategies.factory import make_strategy, signal_series
from gmrl.taxation.estimator import estimate_tax

UTC = timezone.utc
COST = CostModel(*(D(0) for _ in range(5)))
LIMIT = RiskLimits(D(1), D(100000), D(1), D(100), 120, 120)


def t(day, hour=0):
    return datetime(2025, 6, day, hour, tzinfo=UTC)


def market(prices=(100, 100, 100, 100, 100, 100), *, currency="EUR",
           ident="REVIEW", opening=8):
    listing = Instrument(ident, "Synthetic review", None, "TEST", currency, "UTC",
                         "TEST", "equity", "TEST", (), date(2025, 6, 1), None)
    sessions = tuple(Session(ident, t(n).date(), t(n, opening), t(n, opening + 2))
                     for n in range(1, len(prices) + 1))
    bars = tuple(Bar(ident, s.session_date, s.open_at, s.close_at, s.close_at,
                     D(p), D(p), D(p), D(p), D(1000), "raw", "REVIEW")
                 for s, p in zip(sessions, prices))
    fx = tuple(FXQuote(currency, t(n), t(n), D(1) if currency == "EUR" else D(".8"),
                       "REVIEW") for n in range(1, len(prices) + 1))
    provenance = Provenance("REVIEW", "test", "independent synthetic golden cases",
                            t(1), "test only", True, "c" * 64)
    return MarketData((listing,), sessions, bars, (), fx, (provenance,))


def cfg(data, cash=1000):
    return BacktestConfig(D(cash), data.sessions[0].session_date,
                          data.sessions[-1].session_date, COST, LIMIT, False)


def trade(key, side, quantity, price, day, fee=0, fx=1, fx_cost=0):
    return Fill(key, "PAPER-" + key, "REVIEW", side, D(quantity), t(day, 9),
                D(price), D(fx), D(fee), D(fx_cost))


def canonical(data, key="PAPER-REVIEW", day=1, quantity=1, side="buy"):
    return CanonicalOrder(OrderRequest(key, "REVIEW", side, D(quantity), t(day, 23)),
                          sha256(dumps(data).encode()).hexdigest(), COST, LIMIT)


def test_two_lot_split_partial_fifo_conservation():
    state = apply_fill(AccountState(D(1000), ()), trade("B1", "buy", 2, 100, 1, 2)).state
    state = apply_fill(state, trade("B2", "buy", 1, 120, 2, 3)).state
    action = CorporateAction("S", "REVIEW", "split", t(3), t(1), D(2), None)
    data = replace(market(), actions=(action,))
    state, ids, _ = advance_actions(state, data, t(2, 10), t(3), (), 120)
    sold = apply_fill(state, trade("S1", "sell", 5, 70, 4, 5))
    assert sold.state.cash_eur == 1020  # 1000 - 202 - 123 + 350 - 5
    assert sold.state.positions == (("REVIEW", D(1)),)
    assert sold.state.lots[0].total_basis_eur == D("61.5")
    assert [m.allocated_basis_eur for m in sold.realized_matches] == [D(202), D("61.5")]
    assert [m.net_proceeds_eur for m in sold.realized_matches] == [D(276), D(69)]
    assert [m.pnl_eur for m in sold.realized_matches] == [D(74), D("7.5")]
    assert [m.acquired_at for m in sold.realized_matches] == [t(1, 9), t(2, 9)]
    end = apply_fill(sold.state, trade("S2", "sell", 1, 70, 5, 1))
    assert end.state.cash_eur == D(1089)
    assert sum(m.pnl_eur for m in sold.realized_matches + end.realized_matches) == 89
    assert not end.state.positions and not end.state.lots and ids == ("S",)


@pytest.mark.parametrize("basis,amount,close,entitled", [
    ("pre_split", "6", "47", "3"), ("post_split", "3", "47", "6"),
])
def test_simultaneous_actions_stale_bridge_total_return_and_sale(basis, amount, close, entitled):
    data = market((100, 100, int(close), int(close), int(close), int(close)))
    split = CorporateAction("S", "REVIEW", "split", t(3, 7), t(1), D(2), None)
    dividend = CorporateAction("D", "REVIEW", "dividend", t(3, 7), t(1),
                               D(amount), t(5, 7), basis)
    data = replace(data, actions=(split, dividend))
    state = apply_fill(AccountState(D(1000), ()), trade("B", "buy", 3, 100, 2)).state
    state, ids, _ = advance_actions(state, data, t(2, 10), t(3, 7), (), 120)
    assert state.receivables[0].amount_local == 18
    assert state.receivables[0].quantity_entitled == D(entitled)
    assert state.positions == (("REVIEW", D(6)),)
    assert value_account(state, data, t(3, 7), LIMIT).equity_eur == 1000
    assert value_account(state, data, t(3, 23), LIMIT).equity_eur == 1000
    assert signal_series(data, "REVIEW", t(3, 23), total_return=True) == [D(1)] * 3
    state = apply_fill(state, trade("SELL", "sell", 6, close, 4)).state
    assert state.cash_eur == 982 and len(state.receivables) == 1
    state, ids, _ = advance_actions(state, data, t(4, 9), t(6), ids, 120)
    assert state.cash_eur == 1000 and not state.receivables
    assert advance_actions(state, data, t(6), t(6), ids, 120)[0] == state


def test_foreign_receivable_kept_after_sale_and_exact_payment_fx():
    data = market(currency="USD")
    dividend = CorporateAction("D", "REVIEW", "dividend", t(3), t(1), D(5), t(5, 7))
    quotes = data.fx + (
        FXQuote("USD", t(5, 6), t(5, 6), D(".9"), "REVIEW"),
        FXQuote("USD", t(5, 7), t(5, 8), D("1.1"), "REVIEW"),
        FXQuote("USD", t(6, 1), t(6, 1), D(2), "REVIEW"),
    )
    data = replace(data, actions=(dividend,), fx=quotes)
    state = apply_fill(AccountState(D(1000), ()),
                       trade("B", "buy", 2, 100, 2, fx=".8")).state
    state, _, _ = advance_actions(state, data, t(2, 10), t(3), (), 120)
    state = apply_fill(state, trade("S", "sell", 2, 95, 4, fx=".8")).state
    assert state.cash_eur == 992
    assert value_account(state, data, t(4, 23), LIMIT).equity_eur == 1000
    settled = settle_dividends(state, t(6, 2), quotes, 120)
    assert settled.cash_eur == 1001  # 992 + USD 10 * pay-time 0.9
    assert settle_dividends(settled, t(6, 2), quotes, 120) == settled


class Capture:
    def __init__(self):
        self.decisions = []

    def weights(self, history, decided_at):
        assert all(b.available_at <= decided_at and b.close_at <= decided_at
                   for b in history.bars)
        assert all(q.available_at <= decided_at and q.observed_at <= decided_at
                   for q in history.fx)
        assert all(a.effective_at <= decided_at for a in history.actions)
        weights = make_strategy("buy_hold", {}).weights(history, decided_at)
        self.decisions.append(weights)
        return replace(weights, weights=(("REVIEW", D(".25")),))


def test_future_mutation_cannot_rewrite_weights_or_prior_fills():
    data = market(currency="USD")
    original_strategy, changed_strategy = Capture(), Capture()
    original = run_backtest(data, original_strategy, cfg(data))
    mutated = replace(data, bars=tuple(
        replace(b, high=D(9000), low=D(1), close=D(200), volume=D(1))
        if b.session_date.day >= 4 else b for b in data.bars),
        fx=tuple(replace(q, eur_per_unit=D(2)) if q.observed_at.day >= 4 else q
                 for q in data.fx))
    changed = run_backtest(mutated, changed_strategy, cfg(data))
    assert original_strategy.decisions[:3] == changed_strategy.decisions[:3]
    assert [f for f in original.fills if f.filled_at < t(4)] == [
        f for f in changed.fills if f.filled_at < t(4)]
    pd.testing.assert_frame_equal(original.equity.iloc[:4], changed.equity.iloc[:4])


def test_executing_bar_hlcv_does_not_change_frozen_quantity():
    data = market(currency="USD")
    changed = replace(data, bars=(data.bars[0], replace(
        data.bars[1], high=D(10000), low=D(1), close=D(9000), volume=D(0))) + data.bars[2:])
    a = run_backtest(data, Capture(), cfg(data))
    b = run_backtest(changed, Capture(), cfg(data))
    assert a.fills[0] == b.fills[0]
    assert a.fills[0].quantity == D("3.125")
    assert a.fills[0].fx_eur_per_unit == D(".8")


def test_next_open_gap_rejects_whole_frozen_order():
    data = market((100, 500, 500, 500, 500, 500))
    result = run_backtest(data, make_strategy("buy_hold", {}), cfg(data))
    assert not result.fills and result.metrics["rejected_order_count"] == 1
    assert result.equity.equity_eur.eq(1000).all()


def test_actual_utc_order_with_offsets_and_existing_cash_only():
    early = market(ident="EARLY", opening=1)
    late = market(ident="LATE", opening=14)
    # Same instant, different displayed offsets: processing must compare absolute instants.
    offset = timezone(timedelta(hours=-4))
    late = replace(late, sessions=tuple(replace(
        s, open_at=s.open_at.astimezone(offset), close_at=s.close_at.astimezone(offset))
        for s in late.sessions), bars=tuple(replace(
            b, open_at=b.open_at.astimezone(offset), close_at=b.close_at.astimezone(offset),
            available_at=b.available_at.astimezone(offset)) for b in late.bars))
    data = replace(early, instruments=early.instruments + late.instruments,
                   sessions=early.sessions + late.sessions, bars=early.bars + late.bars)

    class Rotate:
        def weights(self, history, decided_at):
            return TargetWeights(decided_at, (
                ("LATE" if decided_at.day == 1 else "EARLY", D(1)),))

    result = run_backtest(data, Rotate(), cfg(early))
    assert [(f.side, f.instrument_id, f.filled_at.astimezone(UTC)) for f in result.fills] == [
        ("buy", "LATE", t(2, 14)), ("sell", "LATE", t(3, 14)),
        ("buy", "EARLY", t(4, 1))]
    assert len(result.equity) == 7 and result.equity.cash_eur.ge(0).all()


@pytest.mark.parametrize("field,value", [
    ("max_weight", D(".05")), ("max_order_eur", D(50)),
    ("max_volume_fraction", D(".0001")), ("max_price_age_hours", 1),
    ("max_fx_age_hours", 1),
])
def test_each_risk_failure_returns_reason(field, value):
    data = market(currency="USD")
    event = opening_event(data, data.sessions[1], 120)
    verdict = validate_execution(canonical(data).order, AccountState(D(1000), ()), event,
                                 COST, replace(LIMIT, **{field: value}), known=data)
    assert not verdict.accepted and verdict.reasons


def test_split_adjusts_prior_volume_units():
    data = market()
    split = CorporateAction("S", "REVIEW", "split", t(2, 7), t(1), D(3), None)
    data = replace(data, actions=(split,))
    assert opening_event(data, data.sessions[1], 120).prior_volume == 3000


@pytest.mark.parametrize("quantity", ["NaN", "-1", "0", "0.0000001", "Infinity"])
def test_bad_fill_quantity_is_domain_rejection(quantity):
    with pytest.raises(AccountingError):
        apply_fill(AccountState(D(1000), ()), trade("BAD", "buy", quantity, 100, 2))


def test_state_reconciliation_rejects_missing_lot():
    with pytest.raises(AccountingError):
        check_state(AccountState(D(100), (("REVIEW", D(1)),)))


def test_statistics_hand_calculated_nonzero_cagr_and_recovery():
    times = pd.to_datetime(["2024-12-31T00:00:00Z", "2025-01-01T00:00:00Z",
                            "2025-01-02T00:00:00Z", "2025-02-01T00:00:00Z"])
    frame = pd.DataFrame({"timestamp": times, "equity_eur": [100, 120, 90, 135],
                          "cash_eur": [100, 120, 90, 135], "exposure": [0, 1, 1, 1],
                          "external_flow_eur": [0] * 4, "stale": [False] * 4})
    metrics = calculate_metrics(frame, (), ())
    # Daily returns .2, -.25, .5; mean .15; sum of squared deviations .285.
    cagr = 1.35 ** (365.25 / 32) - 1
    assert metrics["cagr"] == pytest.approx(cagr)
    assert metrics["annualized_volatility"] == pytest.approx(sqrt(.1425 * 252))
    assert metrics["sharpe"] == pytest.approx(.15 / sqrt(.1425) * sqrt(252))
    assert metrics["sortino"] == pytest.approx(.15 / sqrt(.0625 / 3) * sqrt(252))
    assert metrics["max_drawdown"] == -.25
    assert metrics["calmar"] == pytest.approx(cagr / .25)
    assert metrics["drawdown_duration_days"] == 31
    assert metrics["unrecovered_drawdown"] == 0
    assert periodic_returns(frame).tolist() == pytest.approx([-.1, .5])


@pytest.mark.parametrize("rate,allowance", [("NaN", "0"), ("1.01", "0"), (".25", "-1")])
def test_tax_boundary_has_no_silent_defaults(rate, allowance):
    with pytest.raises(DataValidationError):
        estimate_tax(D(100), D(allowance), D(rate))


def test_paper_concurrent_restart_replay_after_sale_and_canonical_conflict(tmp_path):
    data = market()
    order = canonical(data)
    brokers = [InternalPaperBroker(Repository(tmp_path), D(1000)) for _ in range(4)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        fills = list(pool.map(lambda broker: broker.submit(order, data), brokers))
    assert all(f == fills[0] for f in fills)
    brokers[0].submit(canonical(data, "PAPER-SELL", 3, side="sell"), data)
    restarted = InternalPaperBroker(Repository(tmp_path), D(1000))
    assert restarted.submit(order, replace(data, bars=(), actions=(), fx=())) == fills[0]
    assert restarted.state().cash_eur == 1000
    assert not restarted.state().positions and len(restarted.history().fills) == 2
    for change in (replace(order, dataset_id="0" * 64),
                   replace(order, costs=replace(COST, fixed_fee_eur=D(1))),
                   replace(order, limits=replace(LIMIT, max_order_eur=D(99999))),
                   replace(order, order=replace(order.order, quantity=D(2)))):
        with pytest.raises(OrderRejectedError):
            restarted.submit(change, data)


def test_atomic_failure_after_action_and_journal_write_then_retry(tmp_path):
    data = market((100, 100, 99, 99, 99, 99))
    action = CorporateAction("D", "REVIEW", "dividend", t(3, 7), t(1), D(1), t(5, 7))
    data = replace(data, actions=(action,))
    broker = InternalPaperBroker(Repository(tmp_path), D(1000))
    broker.submit(canonical(data), data)
    before = broker.history()
    sell = canonical(data, "PAPER-SELL", day=2, side="sell")
    original = PaperTransaction.save_account

    def fail_after_write(tx, state, *, expected_version):
        original(tx, state, expected_version=expected_version)
        tx.append_journal(JournalEntry("CRASH", "PAPER-SELL", "test", "test", t(3)))
        raise RuntimeError("injected post-state crash")

    with patch.object(PaperTransaction, "save_account", fail_after_write):
        with pytest.raises(RuntimeError, match="injected"):
            broker.submit(sell, data)
    assert InternalPaperBroker(Repository(tmp_path), D(1000)).history() == before
    broker.submit(sell, data)
    assert broker.state().cash_eur == 999 and broker.state().receivables[0].amount_local == 1
    broker.advance(data, t(5, 8), LIMIT)
    assert broker.state().cash_eur == 1000
    assert len(broker.history().actions) == 1 and not broker.history().journal


@pytest.mark.parametrize("allocations", [
    {"UNKNOWN": D(1)}, {"UNKNOWN": D("NaN")}, {"REVIEW": D(".8"), "UNKNOWN": D(".8")},
])
def test_allocation_boundary_rejects_unknown_or_invalid_input(allocations):
    data = market()
    with pytest.raises(GMRLError):
        simulate_allocation(data, allocations, cfg(data))


def test_currency_risk_includes_unsold_foreign_receivable_after_position_sale():
    data = market(currency="USD")
    dividend = CorporateAction("D", "REVIEW", "dividend", t(3), t(1), D(5), t(5))
    data = replace(data, actions=(dividend,))
    state = apply_fill(AccountState(D(1000), ()),
                       trade("B", "buy", 2, 100, 2, fx=".8")).state
    state, _, _ = advance_actions(state, data, t(2, 10), t(3), (), 120)
    state = apply_fill(state, trade("S", "sell", 2, 95, 4, fx=".8")).state
    snapshot = risk_snapshot(state, data, t(4, 23), LIMIT, foreign_fx_shock=D("-.5"))
    assert snapshot["shock_pnl_eur"] == -4
    assert snapshot["groups_eur"]["currency"].get("USD", D(0)) == 8


@pytest.mark.parametrize("strategy_name", ["trend", "momentum"])
def test_price_dependent_weights_ignore_future_closes_and_actions(strategy_name):
    data = market((100, 101, 102, 103, 104, 105))
    strategy = make_strategy(strategy_name, {"lookback": 2})
    before = strategy.weights(data, t(3, 23))
    assert before.weights == (("REVIEW", D(1)),)
    split = CorporateAction("FUTURE", "REVIEW", "split", t(5, 7), t(1), D(10), None)
    mutated = replace(data, actions=(split,), bars=tuple(
        replace(b, open=D(1), high=D(1), low=D(1), close=D(1), volume=D(1))
        if b.session_date.day > 3 else b for b in data.bars))
    assert strategy.weights(mutated, t(3, 23)) == before


def test_wrong_decision_timestamp_rejected_before_any_execution():
    class WrongTime:
        def weights(self, history, decided_at):
            return TargetWeights(decided_at + timedelta(days=1), (("REVIEW", D(1)),))

    data = market()
    with pytest.raises(DataValidationError, match="timestamp"):
        run_backtest(data, WrongTime(), cfg(data))


def test_missing_expected_open_and_intervening_split_cancel():
    data = market()
    missing = replace(data, bars=data.bars[:1] + data.bars[2:])
    strategy = make_strategy("buy_hold", {})
    result = run_backtest(missing, strategy, cfg(data))
    assert not result.fills and any("never deferred" in s for s in result.warnings)
    split = CorporateAction("S", "REVIEW", "split", t(2, 7), t(1), D(2), None)
    result = run_backtest(replace(data, actions=(split,)), strategy, cfg(data))
    assert not result.fills and any("cancels frozen order" in s for s in result.warnings)


@pytest.mark.parametrize("variant", ["late", "ambiguous", "duplicate"])
def test_invalid_action_information_blocks_engine(variant):
    data = market()
    split = CorporateAction("S", "REVIEW", "split", t(3, 7), t(1), D(2), None)
    if variant == "late":
        actions = (replace(split, available_at=t(4)),)
    elif variant == "ambiguous":
        actions = (split, CorporateAction("D", "REVIEW", "dividend",
                                         t(3, 7), t(1), D(1), t(5)))
    else:
        actions = (split, split)
    with pytest.raises(DataValidationError):
        run_backtest(replace(data, actions=actions), make_strategy("buy_hold", {}), cfg(data))


def test_exact_foreign_costs_and_initial_return_no_double_subtraction():
    data = market(currency="USD")
    costs = CostModel(D(2), D(100), D(100), D(50), D(100))
    # 1 unit: raw EUR80, execution EUR80.8, commission2.808, FX0.808.
    configuration = replace(cfg(data), costs=costs)

    class OneUnit:
        rebalance = "once"

        def weights(self, history, decided_at):
            return TargetWeights(decided_at, (("REVIEW", D(".08")),))

    result = run_backtest(data, OneUnit(), configuration)
    fill = result.fills[0]
    assert fill.quantity == 1 and fill.price_local == 101
    assert fill.fee_eur == D("2.808") and fill.fx_cost_eur == D(".808")
    assert result.equity.iloc[0].equity_eur == 1000
    assert result.equity.iloc[-1].cash_eur == pytest.approx(915.584)
    assert result.equity.iloc[-1].equity_eur == pytest.approx(995.584)
    assert result.metrics["total_costs_eur"] == pytest.approx(4.416)
    assert result.metrics["total_return"] == pytest.approx(-.004416)


def test_currency_mismatch_and_spread_are_explicit_execution_rejections():
    data = market(currency="USD")
    event = opening_event(data, data.sessions[1], 120)
    state = AccountState(D(1000), ())
    wrong = replace(event, fx=replace(event.fx, currency="JPY"))
    verdict = validate_execution(canonical(data).order, state, wrong, COST, LIMIT, known=data)
    assert not verdict.accepted and "currency" in verdict.reasons[0]
    verdict = validate_execution(canonical(data).order, state, event,
                                 replace(COST, spread_bps=D(101)), LIMIT, known=data)
    assert not verdict.accepted and "Spread" in verdict.reasons[0]


def test_paper_restart_capital_backward_time_and_short_reject(tmp_path):
    data = market()
    broker = InternalPaperBroker(Repository(tmp_path), D(1000))
    broker.submit(canonical(data), data)
    before = broker.history()
    with pytest.raises(AccountingError):
        InternalPaperBroker(Repository(tmp_path), D(1001))
    with pytest.raises(OrderRejectedError):
        broker.submit(canonical(data, key="PAPER-BACK", day=1), data)
    with pytest.raises(OrderRejectedError):
        broker.submit(canonical(data, key="PAPER-SHORT", day=3, quantity=2, side="sell"), data)
    assert broker.history() == before
