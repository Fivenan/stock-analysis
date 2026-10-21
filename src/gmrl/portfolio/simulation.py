from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from gmrl.backtesting.engine import run_backtest
from gmrl.domain import BacktestConfig, BacktestResult, MarketData, TargetWeights
from gmrl.errors import DataValidationError


@dataclass(frozen=True, slots=True)
class AllocationStrategy:
    allocations: tuple[tuple[str, Decimal], ...]
    rebalance: str = "monthly"

    def weights(self, history: MarketData, decided_at: datetime) -> TargetWeights:
        observed = {bar.instrument_id for bar in history.bars}
        return TargetWeights(decided_at, tuple((ident, weight) for ident, weight in self.allocations
                                               if ident in observed))


def simulate_allocation(data: MarketData, allocations: dict[str, Decimal],
                        config: BacktestConfig, *, rebalance: str = "monthly") -> BacktestResult:
    registered = {instrument.instrument_id for instrument in data.instruments}
    if not set(allocations).issubset(registered):
        raise DataValidationError("Allocation contains an unregistered listing")
    if any(not isinstance(weight, Decimal) or not weight.is_finite() or not 0 <= weight <= 1
           for weight in allocations.values()):
        raise DataValidationError("Allocation weights must be finite Decimals in [0, 1]")
    if sum(allocations.values(), Decimal(0)) > 1:
        raise DataValidationError("Allocation weights must sum to at most one")
    if rebalance not in ("once", "monthly"):
        raise DataValidationError("Allocation rebalance must be once or monthly")
    return run_backtest(data, AllocationStrategy(tuple(sorted(allocations.items())), rebalance), config)
