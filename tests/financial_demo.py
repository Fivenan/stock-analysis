"""Generate actual synthetic reports with the approved environment; zero network.

Run: .venv/Scripts/python.exe tests/financial_demo.py
Reports are outputs under tests/fixtures/financial_reports, not market evidence.
"""
from datetime import date
from pathlib import Path
import json

from gmrl.analytics.export import equity_csv, fills_csv, result_json
from gmrl.backtesting.defaults import default_config
from gmrl.backtesting.engine import run_backtest
from gmrl.providers.sample import load_demo
from gmrl.strategies.factory import make_strategy


def main() -> None:
    data = load_demo()
    config = default_config(date(2024, 1, 1), date(2025, 12, 31))
    output = Path(__file__).parent / "fixtures" / "financial_reports"
    output.mkdir(parents=True, exist_ok=True)
    summary = []
    for name in ("buy_hold", "trend", "momentum"):
        parameters = {"lookback": 60, "top_n": 3}
        result = run_backtest(data, make_strategy(name, parameters), config)
        (output / f"{name}.json").write_text(result_json(
            result, data, config, {"strategy": name, **parameters}), encoding="utf-8")
        (output / f"{name}_equity.csv").write_text(equity_csv(result), encoding="utf-8")
        (output / f"{name}_fills.csv").write_text(fills_csv(result), encoding="utf-8")
        summary.append({"strategy": name, "rows": len(result.equity), "fills": len(result.fills),
                        "fifo_matches": len(result.realized_matches),
                        "total_return": result.metrics["total_return"],
                        "cagr": result.metrics["cagr"], "warnings": len(result.warnings),
                        "rejected_orders": result.metrics["rejected_order_count"],
                        "experiment_id": result.experiment_id})
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
