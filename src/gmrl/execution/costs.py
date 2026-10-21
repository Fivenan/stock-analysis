from decimal import Decimal

from gmrl.domain import CostModel, Fill, OpeningEvent, OrderRequest
from gmrl.errors import OrderRejectedError


def validate_costs(costs: CostModel) -> None:
    if any(not value.is_finite() or value < 0 for value in
           (costs.fixed_fee_eur, costs.commission_bps, costs.spread_bps,
            costs.slippage_bps, costs.fx_fee_bps)):
        raise OrderRejectedError("Costs must be finite and nonnegative")
    if costs.spread_bps / 20000 + costs.slippage_bps / 10000 >= 1:
        raise OrderRejectedError("Spread/slippage would produce a nonpositive sale price")
    if costs.commission_bps + costs.fx_fee_bps >= 10000:
        raise OrderRejectedError("Variable charges must be below consideration")


def make_fill(order: OrderRequest, opening: OpeningEvent, costs: CostModel,
              currency: str) -> Fill:
    validate_costs(costs)
    shift = costs.spread_bps / 20000 + costs.slippage_bps / 10000
    price = opening.price_local * (1 + shift if order.side == "buy" else 1 - shift)
    consideration = order.quantity * price * opening.fx.eur_per_unit
    fee = costs.fixed_fee_eur + consideration * costs.commission_bps / 10000
    fx_cost = consideration * costs.fx_fee_bps / 10000 if currency != "EUR" else Decimal(0)
    return Fill("PAPER-FILL-" + order.client_order_id, order.client_order_id,
                order.instrument_id, order.side, order.quantity, opening.at, price,
                opening.fx.eur_per_unit, fee, fx_cost)
