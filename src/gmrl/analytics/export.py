"""Portable reports. Decimal amounts are strings in human-readable JSON."""
from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal
import csv
import io
import json
from typing import Any

from gmrl.domain import BacktestConfig, BacktestResult, MarketData

CONVENTIONS = {
    "currency": "EUR", "prices": "raw execution; point-in-time action-safe signals",
    "returns": "daily simple, initial fees included, external contributions unsupported",
    "cagr": "actual calendar time / 365.25", "volatility": "sample ddof=1, sqrt(252)",
    "sharpe": "mean daily excess / sample excess std * sqrt(252)",
    "sortino": "mean excess / sqrt(mean(min(excess,0)^2)) * sqrt(252)",
    "turnover": "absolute EUR consideration / (2 * mean equity)",
    "realized": "closed FIFO matches including allocated trade costs",
    "dividend_fx_fees": "zero", "tax": "not deducted",
}


def _json_default(value: Any) -> str:
    if isinstance(value, (Decimal, datetime, date)):
        return str(value) if isinstance(value, Decimal) else value.isoformat()
    raise TypeError(f"Unsupported report value {type(value).__name__}")


def result_manifest(result: BacktestResult, data: MarketData, config: BacktestConfig,
                    parameters: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "experiment_id": result.experiment_id, "parameters": parameters or {},
        "config": asdict(config), "provenance": [asdict(p) for p in data.provenance],
        "warnings": list(result.warnings), "metrics": result.metrics,
        "conventions": CONVENTIONS, "fills": [asdict(f) for f in result.fills],
        "realized_matches": [asdict(m) for m in result.realized_matches],
        "equity": [{**row, "timestamp": row["timestamp"].isoformat()}
                   for row in result.equity.to_dict(orient="records")],
    }


def result_json(result: BacktestResult, data: MarketData, config: BacktestConfig,
                parameters: dict[str, object] | None = None) -> str:
    return json.dumps(result_manifest(result, data, config, parameters), default=_json_default,
                      indent=2, allow_nan=False)


def equity_csv(result: BacktestResult) -> str:
    return result.equity.to_csv(index=False)


def fills_csv(result: BacktestResult) -> str:
    fields = ["fill_id", "order_id", "instrument_id", "side", "quantity", "filled_at",
              "price_local", "fx_eur_per_unit", "fee_eur", "fx_cost_eur"]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fields)
    writer.writeheader()
    writer.writerows(asdict(fill) for fill in result.fills)
    return output.getvalue()
