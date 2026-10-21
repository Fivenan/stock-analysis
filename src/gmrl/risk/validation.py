"""Risk checks use explicit known portfolio marks and instrument currencies."""
from dataclasses import replace
from decimal import Decimal, ROUND_DOWN
from hashlib import sha256
from typing import Literal

from gmrl.data.subset import known_at
from gmrl.domain import (
    AccountState, BacktestConfig, CostModel, MarketData, OpeningEvent,
    OrderRequest, RiskLimits, TargetWeights, ValidationResult,
)
from gmrl.errors import GMRLError, OrderRejectedError
from gmrl.execution.costs import make_fill, validate_costs
from gmrl.portfolio.accounting import apply_fill, check_quantity, fx_at
from gmrl.portfolio.valuation import mark_at, value_account


def validate_limits(limits: RiskLimits) -> None:
    for value in (limits.max_weight, limits.max_order_eur, limits.max_volume_fraction,
                  limits.max_spread_bps):
        if not value.is_finite() or value < 0:
            raise OrderRejectedError("Risk limits must be finite and nonnegative")
    if (not 0 < limits.max_weight <= 1 or not 0 < limits.max_volume_fraction <= 1
            or limits.max_order_eur <= 0 or limits.max_price_age_hours < 0
            or limits.max_fx_age_hours < 0):
        raise OrderRejectedError("Invalid concentration, liquidity, order or age limit")


def validate_execution(order: OrderRequest, state: AccountState, opening: OpeningEvent,
                       costs: CostModel, limits: RiskLimits, *,
                       known: MarketData) -> ValidationResult:
    """`known` is physically filtered at opening.at, not a full future dataset."""
    try:
        validate_costs(costs)
        validate_limits(limits)
        check_quantity(order.quantity)
        if order.quantity <= 0 or order.side not in ("buy", "sell"):
            raise OrderRejectedError("Positive buy/sell quantity required")
        if (opening.at.tzinfo is None or opening.at.utcoffset() is None
                or order.submitted_at.tzinfo is None or order.submitted_at.utcoffset() is None
                or opening.at <= order.submitted_at or opening.instrument_id != order.instrument_id):
            raise OrderRejectedError("Execution must follow the decision at the listing's next open")
        listing = next((i for i in known.instruments if i.instrument_id == order.instrument_id), None)
        if listing is None or opening.fx.currency != listing.currency:
            raise OrderRejectedError("Unknown listing or incorrect FX currency")
        # At equal timestamps opening events precede completed-bar publication.
        known = known_at(known, opening.at)
        known = replace(known, bars=tuple(b for b in known.bars
                                        if b.close_at < opening.at and b.available_at < opening.at))
        if (not opening.price_local.is_finite() or opening.price_local <= 0
                or not opening.prior_volume.is_finite() or opening.prior_volume <= 0):
            raise OrderRejectedError("Positive raw open and prior volume required")
        if not listing.available_from <= opening.at.date() or (
                listing.available_until and opening.at.date() > listing.available_until):
            raise OrderRejectedError("Listing unavailable")
        expected_fx = fx_at(listing.currency, opening.at, known.fx, limits.max_fx_age_hours)
        if (opening.fx.eur_per_unit != expected_fx.eur_per_unit
                or opening.fx.observed_at != expected_fx.observed_at
                or opening.fx.available_at != expected_fx.available_at
                or opening.fx.observed_at > opening.at or opening.fx.available_at > opening.at):
            raise OrderRejectedError("Opening FX differs from the as-of quote")
        mark_at(known, order.instrument_id, opening.at, limits.max_price_age_hours)
        if costs.spread_bps > limits.max_spread_bps:
            raise OrderRejectedError("Spread exceeds configured limit")
        if order.quantity > opening.prior_volume * limits.max_volume_fraction:
            raise OrderRejectedError("Quantity exceeds prior-volume participation")
        fill = make_fill(order, opening, costs, listing.currency)
        value = fill.quantity * fill.price_local * fill.fx_eur_per_unit
        if value > limits.max_order_eur:
            raise OrderRejectedError("Order EUR consideration exceeds configured cap")
        post = apply_fill(state, fill).state
        valuation = value_account(post, known, opening.at, limits,
                                  {order.instrument_id: opening.price_local})
        position_value = dict(valuation.values).get(order.instrument_id, Decimal(0))
        # Reducing a pre-existing concentration is allowed even if still above the cap.
        if order.side == "buy" and position_value > limits.max_weight * valuation.equity_eur:
            raise OrderRejectedError("Post-trade concentration exceeds configured limit")
        return ValidationResult(True, ())
    except (GMRLError, ValueError, ArithmeticError, TypeError) as exc:
        return ValidationResult(False, (str(exc),))


def size_orders(targets: TargetWeights, state: AccountState, known: MarketData,
                config: BacktestConfig) -> tuple[OrderRequest, ...]:
    """Freeze sizes at decision marks; reserve only existing EUR cash.

    Pending sales are deliberately not spendable here. Actual same-time manual
    sells can fund subsequent buys, but later venue proceeds never fund earlier opens.
    """
    validate_costs(config.costs)
    validate_limits(config.limits)
    weights = dict(targets.weights)
    if (len(weights) != len(targets.weights)
            or any(not w.is_finite() or w < 0 or w > 1 for w in weights.values())
            or sum(weights.values(), Decimal(0)) > 1):
        raise OrderRejectedError("Weights must be unique, nonnegative and sum to at most one")
    if not set(weights).issubset({i.instrument_id for i in known.instruments}):
        raise OrderRejectedError("Unknown target listing")
    known = known_at(known, targets.decided_at)
    valuation = value_account(state, known, targets.decided_at, config.limits)
    holdings = dict(state.positions)
    instruments = {i.instrument_id: i for i in known.instruments}
    cash = state.cash_eur
    orders: list[OrderRequest] = []
    step = Decimal(1) if config.whole_shares else Decimal("0.000001")
    for ident in sorted(set(holdings) | set(weights)):
        price, _ = mark_at(known, ident, targets.decided_at, config.limits.max_price_age_hours)
        quote = fx_at(instruments[ident].currency, targets.decided_at,
                      known.fx, config.limits.max_fx_age_hours)
        unit = price * quote.eur_per_unit
        weight = min(weights.get(ident, Decimal(0)), config.limits.max_weight)
        # Leave costs within the concentration cap, rather than fill a nominal cap then reject.
        target = (valuation.equity_eur * weight / unit).quantize(step, rounding=ROUND_DOWN)
        delta = target - holdings.get(ident, Decimal(0))
        side: Literal["buy", "sell"] = "buy" if delta > 0 else "sell"
        quantity = abs(delta)
        shift = config.costs.spread_bps / 20000 + config.costs.slippage_bps / 10000
        executable_unit = unit * (1 + shift if side == "buy" else 1 - shift)
        quantity = min(quantity, (config.limits.max_order_eur / executable_unit).quantize(
            step, rounding=ROUND_DOWN))
        if side == "buy":
            rates = config.costs.commission_bps / 10000
            if instruments[ident].currency != "EUR":
                rates += config.costs.fx_fee_bps / 10000
            all_in_unit = executable_unit * (1 + rates)
            budget = max(Decimal(0), cash - config.costs.fixed_fee_eur)
            # Solve post-fee concentration inequality at the decision price.
            cap_budget = (config.limits.max_weight
                          * (valuation.equity_eur - config.costs.fixed_fee_eur)
                          - holdings.get(ident, Decimal(0)) * unit)
            cap_quantity = max(Decimal(0), cap_budget / (
                unit + config.limits.max_weight * (all_in_unit - unit)))
            quantity = min(quantity, (budget / all_in_unit).quantize(step, rounding=ROUND_DOWN),
                           cap_quantity.quantize(step, rounding=ROUND_DOWN))
            if quantity:
                cash -= quantity * all_in_unit + config.costs.fixed_fee_eur
        if quantity <= 0:
            continue
        identity = f"{targets.decided_at.isoformat()}:{ident}:{side}:{quantity}"
        orders.append(OrderRequest("PAPER-BT-" + sha256(identity.encode()).hexdigest()[:24],
                                   ident, side, quantity, targets.decided_at))
    return tuple(sorted(orders, key=lambda order: (order.side != "sell", order.instrument_id)))
