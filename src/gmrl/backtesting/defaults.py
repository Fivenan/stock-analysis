from datetime import date
from decimal import Decimal

from gmrl.domain import BacktestConfig, CostModel, RiskLimits


def default_costs() -> CostModel:
    """Illustrative assumptions; not any broker's fee schedule."""
    return CostModel(Decimal("1"), Decimal("1"), Decimal("10"), Decimal("2"), Decimal("5"))


def default_limits() -> RiskLimits:
    return RiskLimits(Decimal("0.30"), Decimal("10000"), Decimal("0.01"),
                      Decimal("50"), 96, 96)


def default_config(start: date, end: date, initial_cash_eur: Decimal = Decimal("10000"),
                   *, whole_shares: bool = False) -> BacktestConfig:
    return BacktestConfig(initial_cash_eur, start, end, default_costs(), default_limits(),
                          whole_shares)
