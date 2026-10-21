"""As-of marks only; adjusted stale marks never become executable prices."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from gmrl.domain import AccountState, MarketData, RiskLimits
from gmrl.errors import DataUnavailableError
from gmrl.portfolio.accounting import fx_at


@dataclass(frozen=True, slots=True)
class Valuation:
    equity_eur: Decimal
    invested_eur: Decimal
    values: tuple[tuple[str, Decimal], ...]
    stale: bool


def mark_at(data: MarketData, ident: str, at: datetime, max_age_hours: int) -> tuple[Decimal, bool]:
    listing = next((i for i in data.instruments if i.instrument_id == ident), None)
    if listing is None or (listing.available_until is not None and at.date() > listing.available_until):
        raise DataUnavailableError("Unknown listing or unresolved delisting proceeds")
    bars = [b for b in data.bars if b.instrument_id == ident
            and b.close_at <= at and b.available_at <= at]
    if not bars:
        raise DataUnavailableError(f"No completed mark for {ident}")
    bar = max(bars, key=lambda b: b.close_at)
    age = (at - bar.close_at).total_seconds() / 3600
    if age > max_age_hours:
        raise DataUnavailableError(f"Mark exceeds age limit for {ident}")
    price = bar.close
    # Preserve valuation across an action before publication of the next raw close.
    actions = sorted((a for a in data.actions if a.instrument_id == ident
                      and bar.close_at < a.effective_at <= at and a.available_at <= at),
                     key=lambda a: (a.effective_at, a.kind == "split", a.action_id))
    for action in actions:
        if action.kind == "split":
            price /= action.amount
        else:
            amount = action.amount
            if action.dividend_basis == "post_split":
                for split in actions:
                    if split.kind == "split" and split.effective_at == action.effective_at:
                        amount *= split.amount
            price -= amount
    if not price.is_finite() or price <= 0:
        raise DataUnavailableError("Action-adjusted stale mark is not positive")
    return price, bar.close_at.date() < at.date()


def value_account(state: AccountState, data: MarketData, at: datetime, limits: RiskLimits,
                  overrides: dict[str, Decimal] | None = None) -> Valuation:
    instruments = {i.instrument_id: i for i in data.instruments}
    values: list[tuple[str, Decimal]] = []
    stale = False
    overrides = overrides or {}
    for ident, quantity in state.positions:
        if ident in overrides:
            price = overrides[ident]
        else:
            price, old = mark_at(data, ident, at, limits.max_price_age_hours)
            stale |= old
        quote = fx_at(instruments[ident].currency, at, data.fx, limits.max_fx_age_hours)
        values.append((ident, quantity * price * quote.eur_per_unit))
    receivables = sum((r.amount_local * fx_at(r.currency, at, data.fx,
                       limits.max_fx_age_hours).eur_per_unit for r in state.receivables), Decimal(0))
    invested = sum((value for _, value in values), Decimal(0))
    equity = state.cash_eur + invested + receivables
    if not equity.is_finite() or equity <= 0:
        raise DataUnavailableError("Account equity must be finite and positive")
    return Valuation(equity, invested, tuple(values), stale)
