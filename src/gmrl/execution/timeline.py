"""Shared action/payment chronology for paper and research execution."""
from dataclasses import replace
from datetime import datetime
from decimal import Decimal

from gmrl.domain import AccountState, CorporateAction, MarketData, OpeningEvent, Session
from gmrl.errors import AccountingError, DataUnavailableError
from gmrl.portfolio.accounting import apply_action, check_quantity, fx_at, settle_dividends


def next_session(data: MarketData, ident: str, after: datetime) -> Session:
    sessions = [s for s in data.sessions if s.instrument_id == ident and s.open_at > after]
    if not sessions:
        raise DataUnavailableError("No next scheduled open in this dataset")
    return min(sessions, key=lambda s: s.open_at)


def opening_event(data: MarketData, session: Session, max_fx_age_hours: int) -> OpeningEvent:
    bar = next((b for b in data.bars if b.instrument_id == session.instrument_id
                and b.session_date == session.session_date), None)
    if bar is None:
        raise DataUnavailableError("Expected opening bar missing; order cancelled, never deferred")
    listing = next(i for i in data.instruments if i.instrument_id == session.instrument_id)
    prior = [b for b in data.bars if b.instrument_id == session.instrument_id
             and b.available_at < session.open_at and b.close_at < session.open_at]
    if not prior:
        raise DataUnavailableError("Prior completed session volume is required")
    previous = max(prior, key=lambda b: b.close_at)
    # Prior volume measured in today's split-adjusted units, never today's HLCV.
    volume = previous.volume
    for action in data.actions:
        if (action.instrument_id == session.instrument_id and action.kind == "split"
                and previous.close_at < action.effective_at <= session.open_at):
            volume *= action.amount
    return OpeningEvent(session.instrument_id, session.open_at, bar.open,
                        fx_at(listing.currency, session.open_at, data.fx, max_fx_age_hours), volume)


def apply_action_group(state: AccountState, actions: tuple[CorporateAction, ...],
                       data: MarketData, *, whole_shares: bool = False) -> AccountState:
    """Entitle pre/post-split dividends first, then apply splits once."""
    instruments = {i.instrument_id: i for i in data.instruments}
    for action in sorted(actions, key=lambda a: (a.kind == "split", a.instrument_id, a.action_id)):
        normalized = action
        if action.kind == "dividend" and action.dividend_basis == "post_split":
            ratio = Decimal(1)
            for split in actions:
                if split.kind == "split" and split.instrument_id == action.instrument_id:
                    ratio *= split.amount
            normalized = replace(action, amount=action.amount * ratio)
        before = len(state.receivables)
        state = apply_action(state, normalized, instruments[action.instrument_id])
        if normalized != action and len(state.receivables) > before:
            # Store the actual post-split unit entitlement, while total cash is unchanged.
            last = state.receivables[-1]
            state = replace(state, receivables=state.receivables[:-1] + (
                replace(last, quantity_entitled=last.amount_local / action.amount),))
        for lot in state.lots:
            check_quantity(lot.quantity, whole_shares=whole_shares)
    return state


def advance_actions(state: AccountState, data: MarketData, after: datetime, through: datetime,
                    processed: tuple[str, ...], max_fx_age_hours: int,
                    *, whole_shares: bool = False
                    ) -> tuple[AccountState, tuple[str, ...], tuple[CorporateAction, ...]]:
    if through < after:
        raise AccountingError("Simulation time cannot move backward")
    seen = set(processed)
    pending = [a for a in data.actions if a.action_id not in seen and a.effective_at <= through]
    if any(a.effective_at < after for a in pending):
        raise AccountingError("Unprocessed action predates the account cursor")
    times = {a.effective_at for a in pending}
    times.update(r.pay_at for r in state.receivables if r.pay_at <= through)
    times.update(a.pay_at for a in pending if a.pay_at is not None and a.pay_at <= through)
    applied: list[CorporateAction] = []
    for at in sorted(times):
        group = tuple(a for a in pending if a.effective_at == at)
        state = apply_action_group(state, group, data, whole_shares=whole_shares)
        state = settle_dividends(state, at, data.fx, max_fx_age_hours)
        for action in group:
            seen.add(action.action_id)
            applied.append(action)
    return state, tuple(sorted(seen)), tuple(applied)
