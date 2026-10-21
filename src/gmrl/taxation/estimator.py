from decimal import Decimal

from gmrl.errors import DataValidationError


def estimate_tax(realized_gain_eur: Decimal, allowance_remaining_eur: Decimal,
                 effective_rate: Decimal) -> Decimal:
    """Single taxable-gain scenario; explicit rate/allowance, no legal defaults.

    Excludes fund partial exemptions, loss baskets, foreign withholding, church
    tax rules and advance lump sums. Never mutates cash or actual tax records.
    """
    if (any(not value.is_finite() for value in
            (realized_gain_eur, allowance_remaining_eur, effective_rate))
            or allowance_remaining_eur < 0 or not 0 <= effective_rate <= 1):
        raise DataValidationError("Finite amounts, nonnegative allowance and rate in [0,1] required")
    return max(Decimal(0), realized_gain_eur - allowance_remaining_eur) * effective_rate
