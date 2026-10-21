"""Durable historical/sample next-open simulation. No live routing capability."""
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256

from gmrl.data.subset import known_at
from gmrl.data.validation import validate_market_data
from gmrl.domain import (
    AccountState, CanonicalOrder, CorporateAction, Fill, JournalEntry, MarketData,
    PaperState, RiskLimits, ValidationResult,
)
from gmrl.errors import AccountingError, GMRLError, OrderRejectedError
from gmrl.execution.costs import make_fill
from gmrl.execution.timeline import advance_actions, next_session, opening_event
from gmrl.risk.validation import validate_execution
from gmrl.storage.codec import dumps
from gmrl.storage.repository import Repository


@dataclass(frozen=True, slots=True)
class PaperHistory:
    snapshot: PaperState
    orders: tuple[CanonicalOrder, ...]
    fills: tuple[Fill, ...]
    actions: tuple[CorporateAction, ...]
    journal: tuple[JournalEntry, ...]


class InternalPaperBroker:
    def __init__(self, repository: Repository, initial_cash_eur: Decimal) -> None:
        self.repository = repository
        if not initial_cash_eur.is_finite() or initial_cash_eur <= 0:
            raise AccountingError("Positive finite initial capital required")
        with repository.paper_transaction() as tx:
            prior = tx.load_account()
            if prior is None:
                tx.save_account(PaperState(AccountState(initial_cash_eur, ()), initial_cash_eur,
                                          0, datetime.min.replace(tzinfo=timezone.utc), ()),
                                expected_version=None)
            elif prior.initial_cash_eur != initial_cash_eur:
                raise AccountingError("This repository already has a different initial capital")

    def history(self) -> PaperHistory:
        with self.repository.paper_transaction() as tx:
            state = tx.load_account()
            if state is None:
                raise AccountingError("Paper account missing")
            return PaperHistory(state, tx.orders(), tx.fills(), tx.actions(), tx.journal())

    def state(self) -> AccountState:
        return self.history().snapshot.account

    def validate(self, order: CanonicalOrder, known: MarketData) -> ValidationResult:
        """Preview against the complete selected historical dataset, without writes."""
        try:
            with self.repository.paper_transaction() as tx:
                existing = tx.lookup_order(order.order.client_order_id)
                if existing is not None:
                    if existing != order:
                        raise OrderRejectedError("Client ID conflicts with persisted canonical order")
                    return ValidationResult(True, ())
                state = tx.load_account()
                if state is None:
                    raise AccountingError("Paper account missing")
                self._prepare(order, known, state)
            return ValidationResult(True, ())
        except (GMRLError, ValueError, ArithmeticError) as exc:
            return ValidationResult(False, (str(exc),))

    def _prepare(self, canonical: CanonicalOrder, data: MarketData, state: PaperState
                 ) -> tuple[PaperState, Fill, tuple[CorporateAction, ...]]:
        order = canonical.order
        if not order.client_order_id.startswith("PAPER-"):
            raise OrderRejectedError("Internal orders require a PAPER- client identifier")
        if order.submitted_at < state.simulation_time:
            raise OrderRejectedError("New order decision precedes the account simulation cursor")
        if sha256(dumps(data).encode()).hexdigest() != canonical.dataset_id:
            raise OrderRejectedError("Canonical dataset identity does not match supplied data")
        validate_market_data(data)
        if not set(state.processed_action_ids).issubset({a.action_id for a in data.actions}):
            raise OrderRejectedError("Dataset omits an action already applied to this account")
        session = next_session(data, order.instrument_id, order.submitted_at)
        if any(a.kind == "split" and a.instrument_id == order.instrument_id
               and order.submitted_at < a.effective_at <= session.open_at for a in data.actions):
            raise OrderRejectedError("Split between decision and open cancels frozen order")
        account, ids, actions = advance_actions(
            state.account, data, state.simulation_time, session.open_at,
            state.processed_action_ids, canonical.limits.max_fx_age_hours)
        event = opening_event(data, session, canonical.limits.max_fx_age_hours)
        validation = validate_execution(order, account, event, canonical.costs, canonical.limits,
                                        known=known_at(data, event.at))
        if not validation.accepted:
            raise OrderRejectedError("; ".join(validation.reasons))
        listing = next(i for i in data.instruments if i.instrument_id == order.instrument_id)
        fill = make_fill(order, event, canonical.costs, listing.currency)
        from gmrl.portfolio.accounting import apply_fill
        account = apply_fill(account, fill).state
        return PaperState(account, state.initial_cash_eur, state.version + 1,
                          event.at, ids), fill, actions

    def submit(self, order: CanonicalOrder, data: MarketData) -> Fill:
        with self.repository.paper_transaction() as tx:
            existing = tx.lookup_order(order.order.client_order_id)
            if existing is not None:
                if existing != order:
                    raise OrderRejectedError("Client ID conflicts with persisted canonical order")
                fill = tx.lookup_fill(order.order.client_order_id)
                if fill is None:
                    raise AccountingError("Persisted order has no atomic fill")
                return fill
            state = tx.load_account()
            if state is None:
                raise AccountingError("Paper account missing")
            for action in data.actions:
                previous = tx.lookup_action(action.action_id)
                if previous is not None and previous != action:
                    raise OrderRejectedError("Previously applied action identity has changed")
            try:
                updated, fill, actions = self._prepare(order, data, state)
            except GMRLError as exc:
                raise OrderRejectedError(str(exc)) from exc
            tx.append_order(order)
            tx.append_fill(order.order.client_order_id, fill)
            for action in actions:
                tx.append_action(action)
            tx.save_account(updated, expected_version=state.version)
            return fill

    def advance(self, data: MarketData, at: datetime, limits: RiskLimits) -> AccountState:
        """Advance historical actions/payments without a trade; never use wall-clock now."""
        validate_market_data(data)
        if not data.sessions or at > max(s.close_at for s in data.sessions):
            raise OrderRejectedError("Advance cutoff must lie within the selected historical dataset")
        with self.repository.paper_transaction() as tx:
            state = tx.load_account()
            if state is None:
                raise AccountingError("Paper account missing")
            if not set(state.processed_action_ids).issubset({a.action_id for a in data.actions}):
                raise OrderRejectedError("Dataset omits previously processed actions")
            for action in data.actions:
                prior = tx.lookup_action(action.action_id)
                if prior is not None and prior != action:
                    raise OrderRejectedError("Previously applied action identity has changed")
            account, ids, actions = advance_actions(
                state.account, data, state.simulation_time, at, state.processed_action_ids,
                limits.max_fx_age_hours)
            for action in actions:
                tx.append_action(action)
            if at != state.simulation_time or account != state.account or ids != state.processed_action_ids:
                tx.save_account(PaperState(account, state.initial_cash_eur, state.version + 1, at, ids),
                                expected_version=state.version)
            return account

    def add_journal(self, entry: JournalEntry) -> None:
        """Append-only revisions: use a new entry ID when revising a lesson."""
        if not entry.entry_id or entry.recorded_at.tzinfo is None:
            raise AccountingError("Journal identity and aware recorded time required")
        with self.repository.paper_transaction() as tx:
            previous = tx.lookup_journal(entry.entry_id)
            if previous is not None:
                if previous != entry:
                    raise AccountingError("Journal ID conflicts; append a revision with a new ID")
                return
            tx.append_journal(entry)
