"""Pure Decimal reducers. Persistence owns event identity deduplication."""
from dataclasses import replace
from datetime import datetime
from decimal import Decimal

from gmrl.domain import (
    AccountState, CorporateAction, DividendReceivable, Fill, FXQuote,
    Instrument, LedgerResult, Lot, RealizedMatch,
)
from gmrl.errors import AccountingError, DataUnavailableError

ZERO = Decimal(0)
UNIT = Decimal("0.000001")


def check_quantity(quantity: Decimal, *, whole_shares: bool = False) -> None:
    step = Decimal(1) if whole_shares else UNIT
    if not quantity.is_finite() or quantity < 0 or quantity % step:
        raise AccountingError("Quantity must be nonnegative and exactly representable")


def check_state(state: AccountState) -> None:
    if not state.cash_eur.is_finite() or state.cash_eur < 0:
        raise AccountingError("Cash must be finite and nonnegative")
    positions = dict(state.positions)
    if len(positions) != len(state.positions):
        raise AccountingError("Duplicate position")
    totals: dict[str, Decimal] = {}
    if len({lot.lot_id for lot in state.lots}) != len(state.lots):
        raise AccountingError("Duplicate lot identity")
    for lot in state.lots:
        check_quantity(lot.quantity)
        if lot.quantity <= 0 or not lot.total_basis_eur.is_finite() or lot.total_basis_eur < 0:
            raise AccountingError("Invalid lot")
        totals[lot.instrument_id] = totals.get(lot.instrument_id, ZERO) + lot.quantity
    for ident, quantity in positions.items():
        check_quantity(quantity)
        if quantity != totals.get(ident, ZERO):
            raise AccountingError("Position quantity does not reconcile with FIFO lots")
    if any(ident not in positions for ident in totals):
        raise AccountingError("Lot without position")
    if len({r.action_id for r in state.receivables}) != len(state.receivables):
        raise AccountingError("Duplicate receivable")
    for receivable in state.receivables:
        if (not receivable.amount_local.is_finite() or receivable.amount_local <= 0
                or not receivable.quantity_entitled.is_finite()
                or receivable.quantity_entitled <= 0 or receivable.pay_at.tzinfo is None):
            raise AccountingError("Invalid dividend receivable")


def fx_at(currency: str, at: datetime, quotes: tuple[FXQuote, ...],
          max_age_hours: int) -> FXQuote:
    if at.tzinfo is None or at.utcoffset() is None or max_age_hours < 0:
        raise DataUnavailableError("Aware FX cutoff and nonnegative age required")
    if currency == "EUR":
        return FXQuote("EUR", at, at, Decimal(1), "EUR-IDENTITY")
    candidates = [q for q in quotes if q.currency == currency
                  and q.available_at <= at and q.observed_at <= at]
    if not candidates:
        raise DataUnavailableError(f"No FX known at cutoff for {currency}")
    quote = max(candidates, key=lambda q: (q.observed_at, q.available_at))
    if (not quote.eur_per_unit.is_finite() or quote.eur_per_unit <= 0
            or (at - quote.observed_at).total_seconds() > max_age_hours * 3600):
        raise DataUnavailableError(f"Invalid or stale FX for {currency}")
    return quote


def apply_fill(state: AccountState, fill: Fill) -> LedgerResult:
    check_state(state)
    check_quantity(fill.quantity)
    if fill.side not in ("buy", "sell") or fill.quantity <= 0:
        raise AccountingError("Positive buy/sell quantity required")
    if fill.filled_at.tzinfo is None or fill.filled_at.utcoffset() is None:
        raise AccountingError("Aware fill time required")
    if any(not value.is_finite() or value < 0 for value in
           (fill.price_local, fill.fx_eur_per_unit, fill.fee_eur, fill.fx_cost_eur)):
        raise AccountingError("Invalid fill values")
    if fill.price_local <= 0 or fill.fx_eur_per_unit <= 0:
        raise AccountingError("Positive price and EUR-per-local-unit FX required")
    positions = dict(state.positions)
    quantity = positions.get(fill.instrument_id, ZERO)
    consideration = fill.quantity * fill.price_local * fill.fx_eur_per_unit
    costs = fill.fee_eur + fill.fx_cost_eur
    matches: list[RealizedMatch] = []
    lots = list(state.lots)
    if fill.side == "buy":
        cash = state.cash_eur - consideration - costs
        if cash < 0 or any(lot.lot_id == fill.fill_id for lot in lots):
            raise AccountingError("Insufficient cash including costs, or duplicate lot")
        lots.append(Lot(fill.fill_id, fill.instrument_id, fill.filled_at,
                        fill.quantity, consideration + costs))
        positions[fill.instrument_id] = quantity + fill.quantity
    else:
        if quantity < fill.quantity:
            raise AccountingError("Short selling is unsupported")
        cash = state.cash_eur + consideration - costs
        if cash < 0:
            raise AccountingError("Sale cannot pay its costs")
        remaining = fill.quantity
        new_lots: list[Lot] = []
        for lot in sorted(lots, key=lambda value: (value.acquired_at, value.lot_id)):
            if lot.instrument_id != fill.instrument_id or remaining == 0:
                new_lots.append(lot)
                continue
            if lot.acquired_at > fill.filled_at:
                raise AccountingError("Disposal precedes acquisition")
            matched = min(lot.quantity, remaining)
            basis = lot.total_basis_eur * matched / lot.quantity
            proceeds = (consideration - costs) * matched / fill.quantity
            matches.append(RealizedMatch(fill.instrument_id, lot.acquired_at, fill.filled_at,
                                         matched, basis, proceeds, proceeds - basis))
            remaining -= matched
            if matched < lot.quantity:
                new_lots.append(replace(lot, quantity=lot.quantity - matched,
                                        total_basis_eur=lot.total_basis_eur - basis))
        lots = new_lots
        positions[fill.instrument_id] = quantity - fill.quantity
    result = AccountState(cash, tuple(sorted((i, q) for i, q in positions.items() if q)),
                          tuple(lots), state.receivables)
    check_state(result)
    return LedgerResult(result, tuple(matches))


def apply_action(state: AccountState, action: CorporateAction,
                 instrument: Instrument) -> AccountState:
    check_state(state)
    if (action.instrument_id != instrument.instrument_id
            or action.available_at > action.effective_at
            or not action.amount.is_finite() or action.amount <= 0):
        raise AccountingError("Invalid or late-known corporate action")
    quantity = dict(state.positions).get(instrument.instrument_id, ZERO)
    if action.kind == "split":
        lots = tuple(replace(lot, quantity=lot.quantity * action.amount)
                     if lot.instrument_id == instrument.instrument_id else lot for lot in state.lots)
        for lot in lots:
            check_quantity(lot.quantity)
        positions = dict(state.positions)
        if quantity:
            positions[instrument.instrument_id] = quantity * action.amount
        result = replace(state, positions=tuple(sorted(positions.items())), lots=lots)
        check_state(result)
        return result
    if action.kind != "dividend" or action.pay_at is None or action.pay_at < action.effective_at:
        raise AccountingError("Dividend requires a valid payment time")
    if any(r.action_id == action.action_id for r in state.receivables):
        raise AccountingError("Duplicate dividend entitlement")
    if not quantity:
        return state
    receivable = DividendReceivable(action.action_id, instrument.instrument_id, quantity,
                                    quantity * action.amount, instrument.currency, action.pay_at)
    return replace(state, receivables=state.receivables + (receivable,))


def settle_dividends(state: AccountState, at: datetime, fx: tuple[FXQuote, ...],
                      max_fx_age_hours: int) -> AccountState:
    cash = state.cash_eur
    remaining: list[DividendReceivable] = []
    for receivable in state.receivables:
        if receivable.pay_at > at:
            remaining.append(receivable)
        else:
            quote = fx_at(receivable.currency, receivable.pay_at, fx, max_fx_age_hours)
            cash += receivable.amount_local * quote.eur_per_unit
    return replace(state, cash_eur=cash, receivables=tuple(remaining))
