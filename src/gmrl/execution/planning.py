"""Architecture public planning API, shared by research and UI callers."""
from gmrl.domain import AccountState, BacktestConfig, MarketData, OrderRequest, TargetWeights
from gmrl.risk.validation import size_orders, validate_execution

__all__ = ["plan_orders", "validate_execution"]


def plan_orders(targets: TargetWeights, state: AccountState, known: MarketData,
                config: BacktestConfig) -> tuple[OrderRequest, ...]:
    return size_orders(targets, state, known, config)
