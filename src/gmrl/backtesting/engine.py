"""UTC event union; strategy views never contain future HLCV or future actions."""
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal
from hashlib import sha256

from gmrl.analytics.metrics import calculate_metrics, metric_warnings
from gmrl.data.subset import known_at
from gmrl.data.validation import validate_market_data
from gmrl.domain import (
    AccountState, BacktestConfig, BacktestResult, Fill, MarketData, OrderRequest,
    RealizedMatch, TargetWeights,
)
from gmrl.errors import DataUnavailableError, DataValidationError, GMRLError
from gmrl.execution.costs import make_fill, validate_costs
from gmrl.execution.planning import plan_orders
from gmrl.execution.timeline import advance_actions, next_session, opening_event
from gmrl.portfolio.accounting import apply_fill
from gmrl.portfolio.valuation import value_account
from gmrl.risk.validation import validate_execution, validate_limits
from gmrl.storage.codec import dumps
from gmrl.strategies.base import Strategy


def run_backtest(data: MarketData, strategy: Strategy, config: BacktestConfig) -> BacktestResult:
    import pandas as pd
    validate_market_data(data)
    validate_costs(config.costs)
    validate_limits(config.limits)
    if (config.start > config.end or not config.initial_cash_eur.is_finite()
            or config.initial_cash_eur <= 0):
        raise DataValidationError("Valid date range and positive finite initial EUR cash required")
    sessions = [s for s in data.sessions if config.start <= s.session_date <= config.end]
    if not sessions:
        raise DataUnavailableError("No supported sessions in requested date range")
    days = sorted({s.session_date for s in sessions})
    start = datetime.combine(config.start, time.min, timezone.utc)
    end = datetime.combine(config.end, time.max, timezone.utc)
    if any(s.open_at < start or s.close_at > end for s in sessions):
        raise DataValidationError("UTC run boundaries exclude a requested venue session")
    state = AccountState(config.initial_cash_eur, ())
    fills: list[Fill] = []
    matches: list[RealizedMatch] = []
    warnings: list[str] = []
    observed = {(b.instrument_id, b.session_date) for b in data.bars}
    warnings.extend(f"Expected bar missing: {s.instrument_id} {s.session_date}; no executable open"
                    for s in sessions if (s.instrument_id, s.session_date) not in observed)
    rows = [{"timestamp": start - timedelta(microseconds=1),
             "equity_eur": float(config.initial_cash_eur), "cash_eur": float(config.initial_cash_eur),
             "exposure": 0.0, "external_flow_eur": 0.0, "stale": False}]
    cursor = start
    processed = tuple(a.action_id for a in data.actions if a.effective_at < start)
    pending: dict[datetime, list[OrderRequest]] = {}
    decisions: list[TargetWeights] = []
    cutoffs = {datetime.combine(day, time.max, timezone.utc) for day in days}
    events = sorted({s.open_at for s in sessions} | cutoffs
                    | {a.effective_at for a in data.actions if start <= a.effective_at <= end}
                    | {a.pay_at for a in data.actions if a.pay_at is not None and start <= a.pay_at <= end})
    rebalance = getattr(strategy, "rebalance", "daily")
    scheduled_months: set[tuple[int, int]] = set()
    once_done = False
    spread_cost = Decimal(0)
    slippage_cost = Decimal(0)
    rejected_orders = 0
    for at in events:
        state, processed, _ = advance_actions(state, data, cursor, at, processed,
                                              config.limits.max_fx_age_hours,
                                              whole_shares=config.whole_shares)
        cursor = at
        for order in sorted(pending.pop(at, []),
                            key=lambda o: (o.side != "sell", o.instrument_id, o.client_order_id)):
            try:
                if any(a.kind == "split" and a.instrument_id == order.instrument_id
                       and order.submitted_at < a.effective_at <= at for a in data.actions):
                    raise DataUnavailableError("Split between decision and open cancels frozen order")
                session = next_session(data, order.instrument_id, order.submitted_at)
                event = opening_event(data, session, config.limits.max_fx_age_hours)
                verdict = validate_execution(order, state, event, config.costs, config.limits,
                                             known=known_at(data, at))
                if not verdict.accepted:
                    raise DataUnavailableError("; ".join(verdict.reasons))
                listing = next(i for i in data.instruments if i.instrument_id == order.instrument_id)
                fill = make_fill(order, event, config.costs, listing.currency)
                reduced = apply_fill(state, fill)
                state = reduced.state
                fills.append(fill)
                matches.extend(reduced.realized_matches)
                raw_eur = fill.quantity * event.price_local * event.fx.eur_per_unit
                spread_cost += raw_eur * config.costs.spread_bps / 20000
                slippage_cost += raw_eur * config.costs.slippage_bps / 10000
            except GMRLError as exc:
                rejected_orders += 1
                warnings.append(f"{order.client_order_id} cancelled at {at.isoformat()}: {exc}")
        if at not in cutoffs:
            continue
        history = known_at(data, at)
        valuation = value_account(state, history, at, config.limits)
        rows.append({"timestamp": at, "equity_eur": float(valuation.equity_eur),
                     "cash_eur": float(state.cash_eur),
                     "exposure": float(valuation.invested_eur / valuation.equity_eur),
                     "external_flow_eur": 0.0, "stale": valuation.stale})
        month = (at.year, at.month)
        should_decide = not (rebalance == "once" and once_done
                             or rebalance == "monthly" and month in scheduled_months)
        if should_decide and at < end:
            targets = strategy.weights(history, at)
            if targets.decided_at != at:
                raise DataValidationError("Strategy returned a different decision timestamp")
            decisions.append(targets)
            orders = plan_orders(targets, state, history, config)
            for order in orders:
                try:
                    session = next_session(data, order.instrument_id, at)
                    if session.session_date > config.end or session.open_at > end:
                        warnings.append(f"{order.client_order_id}: next open beyond run end")
                    else:
                        pending.setdefault(session.open_at, []).append(order)
                except DataUnavailableError as exc:
                    warnings.append(f"{order.client_order_id}: {exc}")
            scheduled_months.add(month)
            if targets.weights:
                once_done = True
    equity = pd.DataFrame(rows)
    metrics = calculate_metrics(equity, tuple(fills), tuple(matches))
    metrics["spread_costs_eur"] = float(spread_cost)
    metrics["slippage_costs_eur"] = float(slippage_cost)
    metrics["rejected_order_count"] = float(rejected_orders)
    metrics["total_costs_eur"] = (
        float(spread_cost + slippage_cost)
        + float(metrics["fees_eur"] or 0) + float(metrics["fx_costs_eur"] or 0))
    warnings.extend(metric_warnings(metrics))
    if not fills:
        warnings.append("No fills: inspect warm-up, risk limits, dates and cancellation reasons")
    if any(row["stale"] for row in rows):
        warnings.append("Some valuations use age-limited prior closes; these are never executable")
    warnings.append("252-observation annualization; calendar CAGR; synthetic data is not market evidence")
    identity = sha256(dumps((data, config, type(strategy).__name__, tuple(decisions),
                            tuple(fills), tuple(matches))).encode()).hexdigest()
    return BacktestResult(equity, tuple(fills), tuple(matches), metrics,
                          tuple(dict.fromkeys(warnings)), identity)


def compare_with_benchmark(data: MarketData, strategy: Strategy, config: BacktestConfig
                           ) -> tuple[BacktestResult, BacktestResult]:
    from gmrl.strategies.factory import make_strategy
    return run_backtest(data, strategy, config), run_backtest(
        data, make_strategy("buy_hold", {}), config)
