"""Offline Streamlit interface. Start from repository root with streamlit run app/main.py."""
from dataclasses import asdict, replace
from datetime import date, datetime, time, timezone
from decimal import Decimal
from hashlib import sha256
import os
from pathlib import Path
from uuid import uuid4

import pandas as pd
import streamlit as st

from gmrl.analytics.export import equity_csv, fills_csv, result_json, result_manifest
from gmrl.analytics.metrics import periodic_returns, worst_periods
from gmrl.backtesting.defaults import default_config, default_costs, default_limits
from gmrl.backtesting.engine import compare_with_benchmark
from gmrl.domain import CanonicalOrder, DatasetRequest, JournalEntry, OrderRequest
from gmrl.data.subset import subset
from gmrl.errors import AccountingError, GMRLError
from gmrl.execution.paper import InternalPaperBroker
from gmrl.portfolio.simulation import simulate_allocation
from gmrl.providers.sample import SampleProvider, load_demo
from gmrl.risk.scenarios import risk_snapshot
from gmrl.storage.codec import dumps
from gmrl.storage.repository import Repository
from gmrl.strategies.factory import make_strategy, signal_series
from gmrl.taxation.estimator import estimate_tax

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("Global Dashboard", "Market Explorer", "Asset Research", "Global Macro Dashboard",
         "Strategy Builder", "Backtesting Lab", "Portfolio Simulator", "Paper Trading",
         "Risk Dashboard", "API Management", "Trade Journal", "Learning Center")


@st.cache_resource
def demo():
    return load_demo()


def table(records):
    st.dataframe(pd.DataFrame([asdict(r) for r in records]), hide_index=True)


def broker(repository):
    with repository.paper_transaction() as tx:
        prior = tx.load_account()
    if prior is None:
        raise AccountingError("Initialize your account on Paper Trading first; choose its initial capital explicitly.")
    return InternalPaperBroker(repository, prior.initial_cash_eur)


def configure(data):
    st.caption("Illustrative settings, not personal objectives. Costs are assumptions, not broker fees.")
    name = st.selectbox("Strategy", ["buy_hold", "trend", "momentum"])
    ids = st.multiselect("Universe", [i.instrument_id for i in data.instruments],
                        default=[i.instrument_id for i in data.instruments])
    start = st.date_input("Start date", date(2024, 1, 2))
    end = st.date_input("End date", date(2025, 12, 31))
    capital = st.number_input("Initial capital EUR", min_value=1.0, value=10000.0)
    lookback = st.number_input("Lookback sessions", 2, 250, 60)
    top_n = st.number_input("Top N", 1, 9, 3)
    with st.expander("Costs and risk limits"):
        values = {}
        for field, default in asdict(default_costs()).items():
            values[field] = Decimal(str(st.number_input(field, min_value=0.0, value=float(default))))
        limits = default_limits()
        weight = st.number_input("Maximum position weight", 0.01, 1.0, float(limits.max_weight))
        order = st.number_input("Maximum order EUR", min_value=1.0, value=float(limits.max_order_eur))
        volume = st.number_input("Maximum prior-volume fraction", 0.000001, 1.0,
                                 float(limits.max_volume_fraction), format="%.6f")
    config = replace(default_config(start, end, Decimal(str(capital))),
                     costs=replace(default_costs(), **values),
                     limits=replace(limits, max_weight=Decimal(str(weight)),
                                    max_order_eur=Decimal(str(order)),
                                    max_volume_fraction=Decimal(str(volume))))
    return name, ids, {"lookback": int(lookback), "top_n": int(top_n)}, config


def report(result, data, config, parameters):
    st.line_chart(result.equity.set_index("timestamp")[["equity_eur", "cash_eur"]])
    st.json(result.metrics)
    with st.expander("Monthly, yearly and worst-period returns"):
        st.write("Compounded monthly returns", periodic_returns(result.equity, "ME"))
        st.write("Compounded yearly returns", periodic_returns(result.equity, "YE"))
        st.write("Five worst months", worst_periods(result.equity))
    st.write("Warnings and rejected/cancelled order reasons")
    for warning in result.warnings:
        st.warning(warning)
    st.write("Filled trades")
    table(result.fills)
    st.download_button("Download JSON report", result_json(result, data, config, parameters),
                       "synthetic-report.json", "application/json")
    st.download_button("Download equity CSV", equity_csv(result), "synthetic-equity.csv", "text/csv")
    st.download_button("Download fills CSV", fills_csv(result), "synthetic-fills.csv", "text/csv")


def render(page, data, repository):
    registry = pd.DataFrame([asdict(i) for i in data.instruments])
    if page == "Global Dashboard":
        watch = st.multiselect("Watchlist", registry.instrument_id, default=list(registry.instrument_id))
        st.dataframe(registry[registry.instrument_id.isin(watch)], hide_index=True)
        st.write(f"Coverage: {len(data.instruments)} synthetic listings; {len(data.bars)} raw daily bars.")
        st.write("Observation range: 2024–2025. Historical sample; unsuitable as current quotes.")
        table(data.provenance)
    elif page == "Market Explorer":
        for field in ("country", "sector", "currency", "asset_class", "mic"):
            chosen = st.multiselect(field, sorted(registry[field].unique()))
            if chosen:
                registry = registry[registry[field].isin(chosen)]
        st.dataframe(registry, hide_index=True)
        st.info("Sample registry coverage does not establish broker availability. See MARKET_ACCESS.")
    elif page == "Asset Research":
        ident = st.selectbox("Asset", registry.instrument_id)
        bounds = st.date_input("Research dates", (date(2024, 1, 2), date(2025, 12, 31)))
        if len(bounds) != 2:
            st.info("Choose both dates.")
            return
        selected = subset(data, DatasetRequest((ident,), *bounds))
        if not selected.bars:
            st.warning("No observations in this range. Choose dates in 2024–2025.")
            return
        frame = pd.DataFrame([asdict(b) for b in selected.bars]).set_index("session_date")
        st.write("Raw execution prices in listing currency; a split can cause a mechanical price drop.")
        st.line_chart(frame[["close"]].astype(float))
        table(selected.bars)
        at = max(b.available_at for b in selected.bars)
        values = signal_series(selected, ident, at, total_return=True)
        st.write("Split-safe local gross total-return index; dividend reinvestment convention, before costs/FX.")
        st.line_chart(pd.DataFrame({"index": [float(v) for v in values]}, index=frame.index))
        returns = pd.Series([float(v) for v in values]).pct_change().dropna()
        st.write("Local gross daily volatility (sample std × √252):",
                 None if len(returns) < 2 else float(returns.std() * (252 ** 0.5)))
        st.bar_chart(frame[["volume"]].astype(float))
        table(selected.actions)
    elif page == "Global Macro Dashboard":
        currency = st.selectbox("Synthetic FX currency", sorted({q.currency for q in data.fx}))
        bounds = st.date_input("FX comparison dates", (date(2024, 1, 2), date(2025, 12, 31)))
        if len(bounds) != 2:
            st.info("Choose both dates.")
            return
        frame = pd.DataFrame([asdict(q) for q in data.fx if q.currency == currency
                              and bounds[0] <= q.observed_at.date() <= bounds[1]])
        if frame.empty:
            st.warning("No FX observations in this range; choose dates in 2024–2025.")
            return
        st.line_chart(frame.set_index("observed_at")[["eur_per_unit"]].astype(float))
        st.info("Synthetic EUR per local-currency unit only. Inflation, yield curves, commodities and macro vintages are research documentation, not implemented series.")
    elif page in ("Strategy Builder", "Backtesting Lab"):
        name, ids, parameters, config = configure(data)
        st.info("Three active strategies. Other research entries, optimization and walk-forward are deferred.")
        if st.button("Run backtest and benchmark", type="primary"):
            if not ids or config.start > config.end:
                st.error("Choose at least one listing and start date no later than end date.")
            else:
                selected = subset(data, DatasetRequest(tuple(ids), date(2024, 1, 1), config.end))
                result, benchmark = compare_with_benchmark(selected, make_strategy(name, parameters), config)
                st.session_state.run = (result, benchmark, selected, config, {"strategy": name, **parameters})
        if "run" in st.session_state:
            result, benchmark, selected, config, parameters = st.session_state.run
            report(result, selected, config, parameters)
            st.write("Equal-weight buy-and-hold benchmark: identical costs, dates and execution rules")
            st.json(benchmark.metrics)
            if st.button("Save experiment"):
                saved = repository.save_experiment(result_manifest(result, selected, config, parameters))
                st.success("Saved repository ID: " + saved)
        experiments = repository.experiments()
        chosen = st.multiselect("Compare saved experiments", [ident for ident, _ in experiments])
        for ident in chosen:
            saved = repository.load_experiment(ident)
            st.write(ident)
            st.json(saved.get("parameters"))
            st.json(saved.get("metrics"))
            st.line_chart(pd.DataFrame(saved["equity"]).set_index("timestamp")[["equity_eur"]])
    elif page == "Portfolio Simulator":
        st.info("Contributions and time-weighted flow returns are deferred. Residual allocation remains EUR cash.")
        allocations = {}
        for ident in registry.instrument_id:
            allocations[ident] = Decimal(str(st.number_input(ident + " weight", 0.0, 1.0, 0.1)))
        rebalance = st.selectbox("Rebalance", ["monthly", "once"])
        capital = st.number_input("Allocation capital EUR", min_value=1.0, value=10000.0)
        fee = st.number_input("Allocation fixed fee EUR", min_value=0.0, value=1.0)
        if st.button("Simulate allocation"):
            config = replace(default_config(date(2024, 1, 2), date(2025, 12, 31),
                                           Decimal(str(capital))),
                             costs=replace(default_costs(), fixed_fee_eur=Decimal(str(fee))))
            result = simulate_allocation(data, allocations, config, rebalance=rebalance)
            st.session_state.allocation = (result, config,
                                           {"rebalance": rebalance, "allocations": dict(allocations)})
        if "allocation" in st.session_state:
            result, config, original_parameters = st.session_state.allocation
            report(result, data, config, original_parameters)
    elif page == "Paper Trading":
        with repository.paper_transaction() as tx:
            prior = tx.load_account()
        if prior is None:
            capital = st.number_input("New paper account initial EUR", min_value=1.0, value=10000.0)
            if st.button("Initialize paper account"):
                InternalPaperBroker(repository, Decimal(str(capital)))
                st.success("Paper account initialized with the supplied capital.")
            else:
                st.info("Initialize explicitly to persist your chosen capital before submitting orders.")
                return
        else:
            st.write("Persisted initial capital EUR:", str(prior.initial_cash_eur))
        account = broker(repository)
        st.caption("Initial capital is persisted. Existing capital is retained on restart.")
        ident = st.selectbox("Paper asset", registry.instrument_id, index=1)
        side = st.selectbox("Side", ["buy", "sell"])
        quantity = st.number_input("Quantity", min_value=0.000001, value=1.0, format="%.6f")
        day = st.date_input("Historical decision date (UTC end of day)", date(2024, 1, 2))
        st.session_state.setdefault("paper_id", "PAPER-" + uuid4().hex)
        if st.button("New order ID"):
            st.session_state.paper_id = "PAPER-" + uuid4().hex
        st.code(st.session_state.paper_id)
        history = account.history()
        if history.orders:
            replay = st.selectbox("Persisted order to replay exactly", history.orders,
                                  format_func=lambda item: item.order.client_order_id)
            if st.button("Replay persisted canonical order"):
                st.success("Identical replay: " + account.submit(replay, data).fill_id)
        if st.button("Submit simulated order"):
            canonical = CanonicalOrder(OrderRequest(st.session_state.paper_id, ident, side,
                Decimal(str(quantity)), datetime.combine(day, time.max, timezone.utc)),
                sha256(dumps(data).encode()).hexdigest(), default_costs(), default_limits())
            fill = account.submit(canonical, data)
            st.success("Filled or identical replay: " + fill.fill_id)
        if st.button("Advance actions to selected historical date"):
            account.advance(data, datetime.combine(day, time(22), timezone.utc), default_limits())
        history = account.history()
        st.json(asdict(history.snapshot))
        table(history.orders)
        table(history.fills)
        table(history.actions)
        st.caption("Keep ID/payload unchanged for replay. New intent needs New order ID; historical time cannot move backward.")
    elif page == "Risk Dashboard":
        account = broker(repository)
        history = account.history()
        shock = st.slider("Price shock %", -100, 100, -20)
        fx = st.slider("Foreign FX shock %", -100, 100, -10)
        at = history.snapshot.simulation_time
        if at.year < 2024:
            at = datetime(2024, 1, 3, 23, tzinfo=timezone.utc)
        st.json(risk_snapshot(account.state(), data, at, default_limits(),
                             price_shock=Decimal(shock) / 100, foreign_fx_shock=Decimal(fx) / 100))
        if "run" in st.session_state:
            st.write("Latest experiment drawdown and risk metrics")
            st.json(st.session_state.run[0].metrics)
        saved = repository.experiments()
        if saved:
            choice = st.selectbox("Saved experiment risk metrics", [ident for ident, _ in saved])
            st.json(repository.load_experiment(choice).get("metrics"))
        st.info("Holdings are from the durable paper account. Instantaneous shocks are not forecasts or VaR.")
        st.write("Isolated estimated tax scenario; never deducted from paper cash or broker records")
        gain = st.number_input("Estimated realized gain EUR", value=0.0)
        allowance = st.number_input("User-supplied remaining allowance EUR", min_value=0.0, value=0.0)
        rate = st.number_input("User-supplied effective tax rate", 0.0, 1.0, 0.0)
        st.write("Estimated tax EUR:", str(estimate_tax(Decimal(str(gain)), Decimal(str(allowance)), Decimal(str(rate)))))
        st.caption("Excludes fund exemptions, loss pots, foreign withholding, church tax and advance lump sums. See tax guide.")
    elif page == "API Management":
        st.json(asdict(SampleProvider().status()))
        table(repository.provider_status())
        st.write("Persisted usage: provider / outcome / attempts / quota debit")
        st.write(repository.usage_stats())
        with repository.connect() as connection:
            st.write("Persisted cache records:", connection.execute("SELECT COUNT(*) FROM cache").fetchone()[0])
        st.info("External catalog entries are not active adapters. Quota unknown means unknown. Offline sample uses zero requests; observation age is independent of cache TTL.")
        if st.button("Run offline adapter test"):
            checked = SampleProvider().fetch(DatasetRequest(("DEMO-DE",), date(2024, 1, 2), date(2024, 1, 3)))
            st.success(f"Offline adapter passed: {len(checked.bars)} bars; zero network requests.")
    elif page == "Trade Journal":
        account = broker(repository)
        order = st.selectbox("Linked PAPER order", [""] + [o.order.client_order_id for o in account.history().orders])
        hypothesis = st.text_area("Hypothesis / entry and exit plan")
        lesson = st.text_area("Lesson / revision (include prior entry ID when revising)")
        if st.button("Append journal entry"):
            if not hypothesis.strip() and not lesson.strip():
                st.error("Enter a hypothesis or lesson before appending.")
            else:
                account.add_journal(JournalEntry(uuid4().hex, order or None, hypothesis, lesson,
                                                datetime.now(timezone.utc)))
                st.success("Journal entry appended; previous entries retained.")
        entries = account.history().journal
        table(entries)
        st.download_button("Export journal JSON", dumps(entries), "journal.json", "application/json")
    elif page == "Learning Center":
        search = st.text_input("Search guides")
        paths = [p for p in sorted((ROOT / "docs").glob("*.md"))
                 if search.lower() in p.read_text(encoding="utf-8").lower()]
        if not paths:
            st.info("No matching guide. Try a broader term.")
        else:
            chosen = st.selectbox("Guide", paths, format_func=lambda p: p.stem.replace("_", " "))
            st.markdown(chosen.read_text(encoding="utf-8"), unsafe_allow_html=False)


def main():
    st.set_page_config(page_title="Global Market Research Lab", layout="wide")
    st.title("Global Market Research Lab")
    st.warning("SIMULATION ONLY · SYNTHETIC SAMPLE · 2024–2025 · No current market prices or live orders")
    st.caption("Source: deterministic arithmetic generator v1, CC0; retrieved 2026-01-01 UTC. Sample calendars are simplified.")
    page = st.sidebar.radio("Research workspace", PAGES)
    st.header(page)
    repository = Repository(Path(os.environ.get("GMRL_RUNTIME", str(ROOT / ".runtime"))))
    try:
        render(page, demo(), repository)
    except (GMRLError, ValueError, ArithmeticError) as exc:
        st.error("Unable to complete this simulation: " + str(exc))


main()
