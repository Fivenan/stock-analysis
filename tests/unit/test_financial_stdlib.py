"""Financial golden cases; native Python stdlib, no package substitution."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import date, datetime, timezone
from decimal import Decimal as D
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from gmrl.data.subset import known_at
from gmrl.data.validation import validate_market_data
from gmrl.domain import (
    AccountState, BacktestConfig, Bar, CanonicalOrder, CorporateAction, CostModel, Fill,
    FXQuote, Instrument, JournalEntry, MarketData, OrderRequest, Provenance,
    RiskLimits, Session, TargetWeights,
)
from gmrl.errors import AccountingError, DataUnavailableError, DataValidationError, OrderRejectedError
from gmrl.execution.paper import InternalPaperBroker
from gmrl.execution.timeline import advance_actions, opening_event
from gmrl.portfolio.accounting import apply_action, apply_fill, fx_at, settle_dividends
from gmrl.portfolio.valuation import value_account
from gmrl.risk.validation import size_orders, validate_execution
from gmrl.storage.codec import dumps
from gmrl.storage.repository import PaperTransaction, Repository
from gmrl.strategies.factory import make_strategy, signal_series
from gmrl.taxation.estimator import estimate_tax

UTC = timezone.utc
ZERO_COST = CostModel(D(0), D(0), D(0), D(0), D(0))
LIMITS = RiskLimits(D(1), D(100000), D(1), D(100), 96, 96)


def stamp(day: int, hour: int = 0) -> datetime:
    return datetime(2025, 1, day, hour, tzinfo=UTC)


def fixture(prices: tuple[str, ...] = ("100", "110", "110", "110", "110"),
            currency: str = "EUR", ident: str = "SYNTHETIC-A", open_hour: int = 9) -> MarketData:
    instrument = Instrument(ident, ident, None, "TEST", currency, "UTC", "TEST",
                            "equity", "test", (), date(2025, 1, 1), None)
    sessions = tuple(Session(ident, date(2025, 1, n + 1), stamp(n + 1, open_hour),
                             stamp(n + 1, open_hour + 1)) for n in range(len(prices)))
    bars = tuple(Bar(ident, session.session_date, session.open_at, session.close_at,
                     session.close_at, D(price), D(price), D(price), D(price), D(10000),
                     "raw", "SYNTHETIC") for session, price in zip(sessions, prices))
    quotes = tuple(FXQuote(currency, stamp(n + 1), stamp(n + 1),
                           D(1) if currency == "EUR" else D("0.9"), "SYNTHETIC")
                   for n in range(len(prices)))
    provenance = Provenance("SYNTHETIC", "test", "explicit golden fixture", stamp(1),
                            "test only", True, "a" * 64)
    return MarketData((instrument,), sessions, bars, (), quotes, (provenance,))


def fill(side: str, quantity: str = "1", price: str = "100", day: int = 1,
         fee: str = "0", fx_cost: str = "0", fx: str = "1", ident: str = "SYNTHETIC-A") -> Fill:
    return Fill(f"PAPER-F-{side}-{day}", f"PAPER-O-{side}-{day}", ident, side,
                D(quantity), stamp(day, 9), D(price), D(fx), D(fee), D(fx_cost))


def canonical(data: MarketData, *, ident: str = "PAPER-ONE", day: int = 1,
              quantity: str = "1", side: str = "buy") -> CanonicalOrder:
    return CanonicalOrder(OrderRequest(ident, data.instruments[0].instrument_id, side,
                                       D(quantity), stamp(day, 23)),
                          sha256(dumps(data).encode()).hexdigest(), ZERO_COST, LIMITS)


class LedgerTests(unittest.TestCase):
    def test_exact_costs_and_fifo(self):
        state = apply_fill(AccountState(D(1000), ()), fill("buy", fee="1", fx_cost="0.5")).state
        self.assertEqual(state.cash_eur, D("898.5"))
        self.assertEqual(state.lots[0].total_basis_eur, D("101.5"))
        result = apply_fill(state, fill("sell", price="120", day=2, fee="2", fx_cost="0.5"))
        self.assertEqual(result.state.cash_eur, D(1016))
        self.assertEqual(result.realized_matches[0].pnl_eur, D(16))
        self.assertFalse(result.state.positions)

    def test_no_short_or_negative_cash(self):
        with self.assertRaises(AccountingError):
            apply_fill(AccountState(D(100), ()), fill("buy", fee="1"))
        with self.assertRaises(AccountingError):
            apply_fill(AccountState(D(100), ()), fill("sell"))
        with self.assertRaises(AccountingError):
            apply_fill(AccountState(D(100), ()), fill("buy", quantity="-1"))

    def test_fx_direction_and_gain(self):
        data = fixture(("100", "100"), "USD")
        state = apply_fill(AccountState(D(1000), ()), fill("buy", quantity="10", fx="0.9")).state
        self.assertEqual(state.cash_eur, D(100))
        self.assertEqual(value_account(state, data, stamp(1, 23), LIMITS).equity_eur, D(1000))
        updated = replace(data, fx=data.fx + (FXQuote("USD", stamp(2, 12), stamp(2, 12),
                                                     D(1), "SYNTHETIC"),))
        self.assertEqual(value_account(state, updated, stamp(2, 23), LIMITS).equity_eur, D(1100))

    def test_split_equity_and_partial_fifo(self):
        data = fixture(("100", "50", "50"))
        action = CorporateAction("SPLIT", "SYNTHETIC-A", "split", stamp(2, 8), stamp(1), D(2), None)
        data = replace(data, actions=(action,))
        state = apply_fill(AccountState(D(100), ()), fill("buy")).state
        state = apply_action(state, action, data.instruments[0])
        self.assertEqual(dict(state.positions)["SYNTHETIC-A"], D(2))
        self.assertEqual(value_account(state, data, stamp(2, 23), LIMITS).equity_eur, D(100))
        result = apply_fill(state, fill("sell", price="60", day=3))
        self.assertEqual(result.realized_matches[0].allocated_basis_eur, D(50))
        self.assertEqual(result.realized_matches[0].pnl_eur, D(10))
        self.assertEqual(result.realized_matches[0].acquired_at, stamp(1, 9))
        self.assertEqual(result.state.lots[0].total_basis_eur, D(50))

    def test_dividend_receivable_sell_and_pay_once(self):
        data = fixture(("100", "99", "99", "99"))
        action = CorporateAction("DIV", "SYNTHETIC-A", "dividend", stamp(2, 8), stamp(1),
                                 D(1), stamp(4, 8))
        data = replace(data, actions=(action,))
        state = apply_fill(AccountState(D(100), ()), fill("buy")).state
        state = apply_action(state, action, data.instruments[0])
        self.assertEqual(value_account(state, data, stamp(2, 23), LIMITS).equity_eur, D(100))
        state = apply_fill(state, fill("sell", price="99", day=3)).state
        self.assertEqual(state.cash_eur, D(99))
        state = settle_dividends(state, stamp(4, 8), data.fx, 96)
        self.assertEqual(state.cash_eur, D(100))
        self.assertEqual(settle_dividends(state, stamp(5), data.fx, 96), state)

    def test_payment_fx_uses_pay_cutoff_not_call_time(self):
        data = fixture(("100",) * 5, "USD")
        action = CorporateAction("DIV", "SYNTHETIC-A", "dividend", stamp(2, 8), stamp(1),
                                 D(10), stamp(3, 8))
        state = apply_fill(AccountState(D(1000), ()), fill("buy", fx="0.9")).state
        state = apply_action(state, action, data.instruments[0])
        quotes = data.fx + (FXQuote("USD", stamp(3, 9), stamp(3, 9), D(2), "SYNTHETIC"),)
        self.assertEqual(settle_dividends(state, stamp(4), quotes, 96).cash_eur, D(919))

    def test_late_and_ambiguous_actions_rejected(self):
        data = fixture()
        split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(2), stamp(3), D(2), None)
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, actions=(split,)))
        split = replace(split, available_at=stamp(1))
        dividend = CorporateAction("D", "SYNTHETIC-A", "dividend", stamp(2), stamp(1), D(1), stamp(3))
        with self.assertRaises(DataValidationError):
            validate_market_data(replace(data, actions=(split, dividend)))

    def test_post_split_entitlement_and_exact_once(self):
        data = fixture()
        split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(2), stamp(1), D(2), None)
        dividend = CorporateAction("D", "SYNTHETIC-A", "dividend", stamp(2), stamp(1), D(1),
                                   stamp(3), "post_split")
        data = replace(data, actions=(split, dividend))
        state = apply_fill(AccountState(D(100), ()), fill("buy")).state
        state, ids, _ = advance_actions(state, data, stamp(1, 10), stamp(2), (), 96)
        self.assertEqual(state.receivables[0].amount_local, D(2))
        self.assertEqual(state.receivables[0].quantity_entitled, D(2))
        again, _, actions = advance_actions(state, data, stamp(2), stamp(2), ids, 96)
        self.assertEqual(again, state)
        self.assertFalse(actions)

    def test_fractional_split_rejected_without_wealth_loss(self):
        data = fixture()
        state = apply_fill(AccountState(D(100), ()), fill("buy", quantity="0.000001")).state
        split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(2), stamp(1), D("0.5"), None)
        with self.assertRaises(AccountingError):
            apply_action(state, split, data.instruments[0])

    def test_stale_future_wrong_fx(self):
        quotes = (FXQuote("USD", stamp(2), stamp(2), D("0.9"), "SYNTHETIC"),)
        with self.assertRaises(DataUnavailableError):
            fx_at("USD", stamp(1), quotes, 96)
        with self.assertRaises(DataUnavailableError):
            fx_at("USD", stamp(5), quotes, 24)
        data = fixture(currency="USD")
        event = replace(opening_event(data, data.sessions[1], 96),
                        fx=FXQuote("GBP", stamp(2), stamp(2), D("0.9"), "SYNTHETIC"))
        verdict = validate_execution(canonical(data).order, AccountState(D(1000), ()), event,
                                     ZERO_COST, LIMITS, known=known_at(data, event.at))
        self.assertFalse(verdict.accepted)

    def test_frozen_sizing_reserves_cash_including_costs(self):
        data = fixture(("100", "200"))
        config = BacktestConfig(D(1000), date(2025, 1, 1), date(2025, 1, 2),
                                CostModel(D(1), D(0), D(0), D(0), D(0)), LIMITS, False)
        state = AccountState(D(1000), ())
        orders = size_orders(TargetWeights(stamp(1, 23), (("SYNTHETIC-A", D(1)),)),
                             state, known_at(data, stamp(1, 23)), config)
        self.assertEqual(orders[0].quantity, D("9.99"))
        event = opening_event(data, data.sessions[1], 96)
        self.assertFalse(validate_execution(orders[0], state, event, config.costs, LIMITS,
                                            known=known_at(data, event.at)).accepted)

    def test_neutral_split_and_dividend_signal_series(self):
        data = fixture(("100", "50", "49"))
        split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(2, 8), stamp(1), D(2), None)
        dividend = CorporateAction("D", "SYNTHETIC-A", "dividend", stamp(3, 8), stamp(1), D(1), stamp(4))
        data = replace(data, actions=(split, dividend))
        self.assertEqual(signal_series(data, "SYNTHETIC-A", stamp(2, 23)), [D(50), D(50)])
        self.assertEqual(signal_series(data, "SYNTHETIC-A", stamp(3, 23), total_return=True),
                         [D(1), D(1), D(1)])
        self.assertFalse(make_strategy("trend", {"lookback": 2}).weights(data, stamp(2, 23)).weights)
        self.assertFalse(make_strategy("momentum", {"lookback": 2}).weights(data, stamp(3, 23)).weights)

    def test_tax_estimate_explicit_inputs(self):
        self.assertEqual(estimate_tax(D(1200), D(1000), D("0.25")), D(50))
        self.assertEqual(estimate_tax(D(-50), D(0), D("0.25")), D(0))

    def test_each_pretrade_risk_limit_rejects(self):
        data = fixture()
        event = opening_event(data, data.sessions[1], 96)
        state = AccountState(D(1000), ())
        order = canonical(data).order
        for limits, costs in (
            (replace(LIMITS, max_weight=D("0.05")), ZERO_COST),
            (replace(LIMITS, max_order_eur=D(100)), ZERO_COST),
            (replace(LIMITS, max_volume_fraction=D("0.00001")), ZERO_COST),
            (replace(LIMITS, max_spread_bps=D(1)), replace(ZERO_COST, spread_bps=D(2))),
        ):
            with self.subTest(limits=limits):
                self.assertFalse(validate_execution(order, state, event, costs, limits,
                                                     known=known_at(data, event.at)).accepted)

    def test_whole_share_split_rejects_fractional_lot(self):
        data = fixture()
        state = apply_fill(AccountState(D(100), ()), fill("buy")).state
        split = CorporateAction("S", "SYNTHETIC-A", "split", stamp(2), stamp(1), D("0.5"), None)
        data = replace(data, actions=(split,))
        with self.assertRaises(AccountingError):
            advance_actions(state, data, stamp(1, 10), stamp(2), (), 96, whole_shares=True)

    def test_prior_volume_not_current_volume(self):
        data = fixture()
        data = replace(data, bars=(data.bars[0], replace(data.bars[1], volume=D(1))) + data.bars[2:])
        self.assertEqual(opening_event(data, data.sessions[1], 96).prior_volume, D(10000))


class PaperTests(unittest.TestCase):
    def test_action_receivable_persists_sale_then_explicit_advance_pays(self):
        data = fixture(("100", "100", "99", "99", "99"))
        action = CorporateAction("D", "SYNTHETIC-A", "dividend", stamp(3, 8), stamp(1),
                                 D(1), stamp(5, 8))
        data = replace(data, actions=(action,))
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            broker.submit(canonical(data), data)
            broker.submit(canonical(data, ident="PAPER-SELL", day=3, side="sell"), data)
            self.assertEqual(broker.state().cash_eur, D(999))
            self.assertEqual(len(broker.state().receivables), 1)
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            self.assertEqual(broker.advance(data, stamp(5, 9), LIMITS).cash_eur, D(1000))
            self.assertEqual(broker.advance(data, stamp(5, 9), LIMITS).cash_eur, D(1000))
            self.assertEqual(broker.history().actions, (action,))

    def test_replay_identity_includes_dataset_and_limits(self):
        data = fixture()
        order = canonical(data)
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            broker.submit(order, data)
            for changed in (replace(order, dataset_id="b" * 64),
                            replace(order, limits=replace(LIMITS, max_order_eur=D(90000)))):
                with self.assertRaises(OrderRejectedError):
                    broker.submit(changed, data)

    def test_next_open_replay_restart_and_conflict(self):
        data = fixture()
        order = canonical(data)
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            first = broker.submit(order, data)
            self.assertEqual(first.price_local, D(110))
            again = InternalPaperBroker(Repository(Path(root)), D(1000))
            self.assertEqual(again.submit(order, replace(data, bars=())), first)
            self.assertEqual(len(again.history().fills), 1)
            with self.assertRaises(OrderRejectedError):
                again.submit(replace(order, costs=replace(ZERO_COST, fixed_fee_eur=D(1))), data)
            with self.assertRaises(AccountingError):
                InternalPaperBroker(Repository(Path(root)), D(2000))
            with self.assertRaises(OrderRejectedError):
                again.submit(canonical(data, ident="PAPER-BACKWARD"), data)

    def test_concurrent_duplicate_and_crash_rollback(self):
        data = fixture()
        order = canonical(data)
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            with patch.object(PaperTransaction, "save_account", side_effect=RuntimeError("crash")):
                with self.assertRaises(RuntimeError):
                    broker.submit(order, data)
            self.assertEqual(broker.state().cash_eur, D(1000))
            self.assertFalse(broker.history().orders)
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _: broker.submit(order, data), range(2)))
            self.assertEqual(results[0], results[1])
            self.assertEqual(len(broker.history().fills), 1)

    def test_missing_open_not_deferred(self):
        data = fixture()
        data = replace(data, bars=(data.bars[0],) + data.bars[2:])
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            with self.assertRaises(OrderRejectedError):
                broker.submit(canonical(data), data)
            self.assertFalse(broker.history().fills)

    def test_journal_survives_restart(self):
        data = fixture()
        with TemporaryDirectory() as root:
            broker = InternalPaperBroker(Repository(Path(root)), D(1000))
            broker.submit(canonical(data), data)
            entry = JournalEntry("J1", "PAPER-ONE", "hypothesis", "lesson", stamp(3))
            broker.add_journal(entry)
            broker.add_journal(entry)
            self.assertEqual(InternalPaperBroker(Repository(Path(root)), D(1000)).history().journal,
                             (entry,))


if __name__ == "__main__":
    unittest.main()
