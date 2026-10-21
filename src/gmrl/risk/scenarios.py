from datetime import datetime
from decimal import Decimal

from gmrl.domain import AccountState, MarketData, RiskLimits
from gmrl.errors import DataValidationError
from gmrl.portfolio.accounting import fx_at
from gmrl.portfolio.valuation import value_account


def risk_snapshot(state: AccountState, data: MarketData, at: datetime, limits: RiskLimits,
                  *, price_shock: Decimal = Decimal(0), foreign_fx_shock: Decimal = Decimal(0)
                  ) -> dict[str, object]:
    if any(not value.is_finite() or value < -1 for value in (price_shock, foreign_fx_shock)):
        raise DataValidationError("Shock factors must be finite and at least -100%")
    valuation = value_account(state, data, at, limits)
    listings = {i.instrument_id: i for i in data.instruments}
    groups: dict[str, dict[str, Decimal]] = {name: {} for name in ("currency", "country", "sector")}
    groups["currency"]["EUR"] = state.cash_eur
    shocked = state.cash_eur
    for ident, value in valuation.values:
        listing = listings[ident]
        for dimension, buckets in groups.items():
            key = str(getattr(listing, dimension))
            buckets[key] = buckets.get(key, Decimal(0)) + value
        factor = 1 + foreign_fx_shock if listing.currency != "EUR" else Decimal(1)
        shocked += value * (1 + price_shock) * factor
    for receivable in state.receivables:
        value = receivable.amount_local * fx_at(receivable.currency, at, data.fx,
                                                limits.max_fx_age_hours).eur_per_unit
        groups["currency"][receivable.currency] = (
            groups["currency"].get(receivable.currency, Decimal(0)) + value)
        receivable_listing = listings.get(receivable.instrument_id)
        for dimension in ("country", "sector"):
            key = (str(getattr(receivable_listing, dimension))
                   if receivable_listing is not None else "UNATTRIBUTED")
            groups[dimension][key] = groups[dimension].get(key, Decimal(0)) + value
        shocked += value * (1 + foreign_fx_shock if receivable.currency != "EUR" else 1)
    return {
        "equity_eur": valuation.equity_eur,
        "exposure": valuation.invested_eur / valuation.equity_eur,
        "position_weights": {ident: value / valuation.equity_eur for ident, value in valuation.values},
        "groups_eur": groups, "shocked_equity_eur": shocked,
        "group_weight_denominator_eur": valuation.equity_eur,
        "cash_eur": state.cash_eur,
        "group_scope": (
            "Currency includes EUR cash, positions and receivables; country/sector include "
            "positions and attributable receivables, with cash shown separately. "
            "Divide all group EUR values by total account equity for weights."
        ),
        "shock_pnl_eur": shocked - valuation.equity_eur,
        "stale": valuation.stale,
        "limitation": "Instantaneous configurable price/FX shock; not probability, VaR or forecast",
    }
