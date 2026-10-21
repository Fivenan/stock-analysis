from __future__ import annotations

from typing import TYPE_CHECKING
import math

from gmrl.domain import Fill, RealizedMatch
from gmrl.errors import DataValidationError

if TYPE_CHECKING:
    import pandas as pd


def periodic_returns(equity: pd.DataFrame, frequency: str = "ME") -> pd.Series:
    import pandas as pd
    values = pd.Series(equity["equity_eur"].astype(float).to_numpy(),
                       index=pd.DatetimeIndex(equity["timestamp"]))
    returns = values.pct_change(fill_method=None).dropna()
    return (1 + returns).resample(frequency).prod(min_count=1).dropna() - 1


def calculate_metrics(equity: pd.DataFrame, fills: tuple[Fill, ...],
                      realized_matches: tuple[RealizedMatch, ...],
                      annual_risk_free_rate: float = 0.0) -> dict[str, float | None]:
    import numpy as np
    import pandas as pd
    if not math.isfinite(annual_risk_free_rate) or annual_risk_free_rate <= -1:
        raise DataValidationError("Risk-free rate must be finite and greater than -1")
    required = {"timestamp", "equity_eur", "cash_eur", "exposure", "external_flow_eur", "stale"}
    if not required.issubset(equity.columns) or len(equity) < 2:
        raise DataValidationError("Initial equity and at least one daily valuation required")
    times = pd.DatetimeIndex(equity["timestamp"])
    values = equity["equity_eur"].astype(float)
    if (times.tz is None or not times.is_monotonic_increasing or times.has_duplicates
            or not np.isfinite(values).all() or (values <= 0).any()
            or (equity["external_flow_eur"].astype(float) != 0).any()):
        raise DataValidationError("Invalid equity chronology/values; external-flow metrics unsupported")
    returns = values.pct_change(fill_method=None).dropna()
    excess = returns - ((1 + annual_risk_free_rate) ** (1 / 252) - 1)
    sample_std = float(excess.std(ddof=1)) if len(excess) > 1 else None
    downside = float(np.sqrt(np.mean(np.minimum(excess.to_numpy(), 0) ** 2)))
    total = float(values.iloc[-1] / values.iloc[0] - 1)
    years = (times[-1] - times[0]).total_seconds() / (365.25 * 86400)
    try:
        cagr = math.expm1(math.log1p(total) / years) if years > 0 else None
    except OverflowError:
        cagr = None
    drawdown = values / values.cummax() - 1
    max_dd = float(drawdown.min())
    peak_at = times[0]
    peak = float(values.iloc[0])
    duration = 0.0
    underwater = False
    for at, value in zip(times, values):
        if value >= peak:
            if underwater:
                duration = max(duration, (at - peak_at).total_seconds() / 86400)
            peak, peak_at = float(value), at
            underwater = False
        else:
            underwater = True
            duration = max(duration, (at - peak_at).total_seconds() / 86400)
    # Flat paths have no underwater duration.
    if max_dd == 0:
        duration = 0.0
    pnls = [float(match.pnl_eur) for match in realized_matches]
    positive = sum(max(pnl, 0) for pnl in pnls)
    negative = -sum(min(pnl, 0) for pnl in pnls)
    turnover = sum(float(f.quantity * f.price_local * f.fx_eur_per_unit) for f in fills)
    metrics: dict[str, float | None] = {
        "total_return": total, "cagr": cagr, "annualized_return": cagr,
        "arithmetic_annual_return": float(returns.mean()) * 252,
        "annualized_volatility": float(returns.std(ddof=1)) * math.sqrt(252)
        if len(returns) > 1 else None,
        "sharpe": float(excess.mean()) / sample_std * math.sqrt(252)
        if sample_std is not None and sample_std > 0 else None,
        "sortino": float(excess.mean()) / downside * math.sqrt(252) if downside > 0 else None,
        "calmar": cagr / abs(max_dd) if cagr is not None and max_dd < 0 else None,
        "max_drawdown": max_dd, "drawdown_duration_days": duration,
        "unrecovered_drawdown": float(drawdown.iloc[-1] < 0),
        "exposure": float(equity["exposure"].iloc[1:].astype(float).mean()),
        "turnover": turnover / (2 * float(values.mean())),
        "trade_count": float(len(fills)), "closed_fifo_match_count": float(len(pnls)),
        "win_rate": sum(pnl > 0 for pnl in pnls) / len(pnls) if pnls else None,
        "profit_factor": positive / negative if negative > 0 else None,
        "average_holding_days": sum((m.disposed_at - m.acquired_at).total_seconds() / 86400
                                    for m in realized_matches) / len(pnls) if pnls else None,
        "fees_eur": sum(float(f.fee_eur) for f in fills),
        "fx_costs_eur": sum(float(f.fx_cost_eur) for f in fills),
    }
    for frequency, prefix in (("ME", "month"), ("YE", "year")):
        periods = periodic_returns(equity, frequency)
        metrics[f"worst_{prefix}"] = float(periods.min()) if len(periods) else None
        for at, value in periods.items():
            label = at.strftime("%Y-%m" if prefix == "month" else "%Y")
            metrics[f"{prefix}_{label}"] = float(value)
    return metrics


def metric_warnings(metrics: dict[str, float | None]) -> tuple[str, ...]:
    return tuple(f"{key} undefined: insufficient observations or zero denominator"
                 for key, value in metrics.items() if value is None)


def worst_periods(equity: pd.DataFrame, count: int = 5) -> pd.Series:
    if count < 1:
        raise DataValidationError("Positive worst-period count required")
    return periodic_returns(equity, "ME").sort_values(kind="stable").head(count)
