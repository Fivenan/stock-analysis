# Global Market Research Lab: implementation contract

Design dated 2026-10-18; conditional-review amendments 2026-10-20. This document remains the implementation contract. The local foundation, financial engine and application are implemented; executed evidence and remaining gates are recorded in VERIFICATION.md and IMPLEMENTATION_STATUS.md. Native Windows, Python 3.12, local Streamlit, offline by default, EUR account, internal simulation only. No API key or brokerage account is required. Published dependency specifications are in `pyproject.toml` and `requirements-windows-py312.lock`; executed installation evidence is in `docs/VERIFICATION.md`.

## Scope and boundaries

One installable `src/gmrl` package; setuptools build backend; `requires-python = ">=3.12,<3.13"` initially. Streamlit entry point `app/main.py`. No service tier, Docker, Node build, scheduler daemon, remote execution, live broker SDK, credential form or live-routing configuration. GitHub Pages cannot host the Python runtime; the local application plus static companion and GitHub integration/push are APPROVED scope. The static companion cannot execute Streamlit or submit orders; the local app and static builder are implemented; remote deployment remains a separate gate.

Use Pandas/NumPy for arrays, rolling statistics and reporting, Plotly for charts, PyArrow Parquet for normalized datasets, and stdlib SQLite for durable metadata, quota ledger, experiment manifest, orders, fills and journal. Pydantic validates configuration and imported boundaries. Decimal handles ledger amounts and quantities (28 digit precision, quantities rounded down to six decimals; final reported money rounds to cents, internal values retained). Conversion from floats uses decimal strings. No double rounding of each intermediate operation.

Provider, strategy, simulator, ledger and UI depend on immutable domain records, never each other's concrete adapters. A provider cannot submit an order. InternalPaperBroker accepts only a validated market snapshot and writes simulated fills through the same accounting reducer used by backtests. No external broker adapter exists in v1. A paper identifier always starts `PAPER-`; setting an environment key cannot add execution capability. Do not implement an actual broker connection in these steps.

## Existing engine decision

Evidence accessed 2026-10-18; runtime compatibility remains untested until approved installation. [Backtrader documentation](https://www.backtrader.com/docu/) provides event execution and multiple feeds; [repository license](https://github.com/mementum/backtrader/blob/master/LICENSE) is GPL-3. It requires a separate compatibility spike on Python 3.12 and does not eliminate the need to prove FX and action semantics. [vectorbt portfolio API](https://vectorbt.dev/api/portfolio/base/) offers fast array simulation; its [terms](https://vectorbt.dev/terms/) apply Apache 2.0 with Commons Clause, so it is not an unrestricted Apache dependency. Its compilation stack adds complexity to this small Windows slice. [backtesting.py API](https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html) offers fees, spread and next-open execution on an OHLC frame; [upstream](https://github.com/kernc/backtesting.py) uses AGPL-3.0. Multiple independent single-asset runs do not establish shared multi-currency portfolio cash correctness.

Decision: none is a required MVP dependency. Implement a small, inspectable daily event ledger and use established Pandas/NumPy operations for statistics rather than reinventing numerical primitives. This is a deliberate accounting exception, not a claim that a new general-purpose engine is superior. Restrict assets to cash equities/ETF-like sample units, long only, unleveraged, six-decimal fractional units or explicit whole-share mode. No derivatives, carry, margin, intraday stops or automated tax withholding. Future engine adapters must pass identical golden ledger cases before replacing this implementation. License and package compatibility findings are partial, not executed compatibility tests.

## Public contracts and ownership

Step 5 owns `pyproject.toml`, environment examples, package foundation, `src/gmrl/domain.py`, `config.py`, `errors.py`, `data/`, `storage/`, `providers/`, `scripts/`, bundled fixtures and data tests. Step 5 also owns every shared domain record below and the Repository/cache protocols. Step 7 owns the reducers and `strategies/`, `backtesting/`, `portfolio/`, `execution/`, `risk/`, `analytics/`, `taxation/` and financial tests. Step 9 owns `app/`, README, user/learning documentation, UI tests and final status updates. Changes to shared domain contracts require a manager handoff before dependent workers start. Step 5 starts only after Step 2 source verification and Step 4 design review. Domain definitions below are exact public names and field types; all domain dataclasses use `@dataclass(frozen=True, slots=True)`.

```python
# gmrl.domain; datetime is always aware; date is venue session date.
Instrument(instrument_id: str, name: str, isin: str | None, mic: str,
           currency: str, timezone: str, country: str, asset_class: str,
           sector: str, provider_symbols: tuple[tuple[str, str], ...],
           available_from: date, available_until: date | None)
Session(instrument_id: str, session_date: date, open_at: datetime,
        close_at: datetime)
Bar(instrument_id: str, session_date: date, open_at: datetime,
    close_at: datetime, available_at: datetime, open: Decimal,
    high: Decimal, low: Decimal, close: Decimal, volume: Decimal,
    price_basis: Literal["raw"], provenance_id: str)
CorporateAction(action_id: str, instrument_id: str,
                kind: Literal["dividend", "split"], effective_at: datetime,
                available_at: datetime, amount: Decimal, pay_at: datetime | None,
                dividend_basis: Literal["pre_split", "post_split"] | None = None)
FXQuote(currency: str, observed_at: datetime, available_at: datetime,
        eur_per_unit: Decimal, provenance_id: str)
Provenance(provenance_id: str, provider: str, source: str,
           retrieved_at: datetime, license_note: str, synthetic: bool,
           content_sha256: str)
MarketData(instruments: tuple[Instrument, ...], sessions: tuple[Session, ...],
           bars: tuple[Bar, ...], actions: tuple[CorporateAction, ...],
           fx: tuple[FXQuote, ...], provenance: tuple[Provenance, ...])
DatasetRequest(instrument_ids: tuple[str, ...], start: date, end: date)
CacheResult(data: MarketData, dataset_id: str, retrieved_at: datetime,
            expires_at: datetime, cache_status: Literal["hit", "miss", "stale"],
            warnings: tuple[str, ...])
RatePolicy(capacity: int, refill_per_second: float, max_delay_seconds: float)
OpeningEvent(instrument_id: str, at: datetime, price_local: Decimal,
             fx: FXQuote, prior_volume: Decimal)
ProviderStatus(provider: str, enabled: bool, message: str,
               used_requests: int, quota_remaining: int | None)
TargetWeights(decided_at: datetime, weights: tuple[tuple[str, Decimal], ...])
CostModel(fixed_fee_eur: Decimal, commission_bps: Decimal,
          spread_bps: Decimal, slippage_bps: Decimal, fx_fee_bps: Decimal)
RiskLimits(max_weight: Decimal, max_order_eur: Decimal,
           max_volume_fraction: Decimal, max_spread_bps: Decimal,
           max_price_age_hours: int, max_fx_age_hours: int)
BacktestConfig(initial_cash_eur: Decimal, start: date, end: date,
               costs: CostModel, limits: RiskLimits, whole_shares: bool)
OrderRequest(client_order_id: str, instrument_id: str,
             side: Literal["buy", "sell"], quantity: Decimal,
             submitted_at: datetime)
Fill(fill_id: str, order_id: str, instrument_id: str, side: str,
     quantity: Decimal, filled_at: datetime, price_local: Decimal,
     fx_eur_per_unit: Decimal, fee_eur: Decimal, fx_cost_eur: Decimal)
Lot(lot_id: str, instrument_id: str, acquired_at: datetime,
    quantity: Decimal, total_basis_eur: Decimal)
DividendReceivable(action_id: str, instrument_id: str,
                   quantity_entitled: Decimal, amount_local: Decimal,
                   currency: str, pay_at: datetime)
AccountState(cash_eur: Decimal, positions: tuple[tuple[str, Decimal], ...],
             lots: tuple[Lot, ...] = (),
             receivables: tuple[DividendReceivable, ...] = ())
RealizedMatch(instrument_id: str, acquired_at: datetime, disposed_at: datetime,
              quantity: Decimal, allocated_basis_eur: Decimal,
              net_proceeds_eur: Decimal, pnl_eur: Decimal)
LedgerResult(state: AccountState, realized_matches: tuple[RealizedMatch, ...])
PaperState(account: AccountState, initial_cash_eur: Decimal, version: int,
           simulation_time: datetime, processed_action_ids: tuple[str, ...])
CanonicalOrder(order: OrderRequest, dataset_id: str, costs: CostModel,
               limits: RiskLimits)
JournalEntry(entry_id: str, order_id: str | None, hypothesis: str,
             lesson: str, recorded_at: datetime)
ValidationResult(accepted: bool, reasons: tuple[str, ...])
BacktestResult(equity: pd.DataFrame, fills: tuple[Fill, ...],
               realized_matches: tuple[RealizedMatch, ...],
               metrics: dict[str, float | None], warnings: tuple[str, ...],
               experiment_id: str)
```

Public functions and synchronous protocols (implementations may add private helpers):

```python
# gmrl.providers.base
class DataProvider(Protocol):
    def instruments(self) -> tuple[Instrument, ...]: ...
    def fetch(self, request: DatasetRequest) -> MarketData: ...
    def status(self) -> ProviderStatus: ...
# gmrl.data.validation / gmrl.data.csv_import
def validate_market_data(data: MarketData) -> None: ...
def import_bars_csv(path: Path, instruments: tuple[Instrument, ...],
                    provenance: Provenance) -> tuple[Bar, ...]: ...
# gmrl.providers.sample
def load_demo() -> MarketData: ...
# gmrl.storage.repository
class Repository:
    def __init__(self, root: Path) -> None: ...
    def save_dataset(self, data: MarketData) -> str: ...
    def load_dataset(self, dataset_id: str) -> MarketData: ...
    def save_experiment(self, manifest: dict[str, object]) -> str: ...
    def provider_status(self) -> tuple[ProviderStatus, ...]: ...
    @contextmanager
    def paper_transaction(self) -> Iterator[PaperTransaction]: ...

class PaperTransaction(Protocol):
    def load_account(self) -> PaperState | None: ...
    def save_account(self, state: PaperState, *, expected_version: int | None) -> None: ...
    def lookup_order(self, client_order_id: str) -> CanonicalOrder | None: ...
    def lookup_fill(self, client_order_id: str) -> Fill | None: ...
    def lookup_action(self, action_id: str) -> CorporateAction | None: ...
    def lookup_journal(self, entry_id: str) -> JournalEntry | None: ...
    def append_order(self, order: CanonicalOrder) -> None: ...
    def append_fill(self, client_order_id: str, fill: Fill) -> None: ...
    def append_action(self, action: CorporateAction) -> None: ...
    def append_journal(self, entry: JournalEntry) -> None: ...
    def journal(self) -> tuple[JournalEntry, ...]: ...
# gmrl.providers.cache
class CachedProvider:
    def __init__(self, provider: DataProvider, repository: Repository,
                 ttl_seconds: int, *, clock: Callable[[], datetime],
                 sleep: Callable[[float], None], random: Callable[[], float],
                 rate_policy: RatePolicy, max_attempts: int = 3) -> None: ...
    def fetch(self, request: DatasetRequest) -> CacheResult: ...
# gmrl.strategies.base
class Strategy(Protocol):
    def weights(self, history: MarketData, decided_at: datetime) -> TargetWeights: ...
# gmrl.strategies.factory
def make_strategy(name: str, parameters: dict[str, int | float]) -> Strategy: ...
# gmrl.backtesting.engine
def run_backtest(data: MarketData, strategy: Strategy,
                 config: BacktestConfig) -> BacktestResult: ...
# gmrl.execution.planning: known contains completed, available records only
def plan_orders(targets: TargetWeights, state: AccountState,
                known: MarketData, config: BacktestConfig) -> tuple[OrderRequest, ...]: ...
def validate_execution(order: OrderRequest, state: AccountState,
                       opening: OpeningEvent, costs: CostModel,
                       limits: RiskLimits) -> ValidationResult: ...
# gmrl.portfolio.accounting
def apply_fill(state: AccountState, fill: Fill) -> LedgerResult: ...
def apply_action(state: AccountState, action: CorporateAction,
                 instrument: Instrument) -> AccountState: ...
def settle_dividends(state: AccountState, at: datetime,
                      fx: tuple[FXQuote, ...], max_fx_age_hours: int) -> AccountState: ...
# gmrl.execution.paper
class InternalPaperBroker:
    def __init__(self, repository: Repository, initial_cash_eur: Decimal) -> None: ...
    def state(self) -> AccountState: ...
    def validate(self, order: CanonicalOrder, known: MarketData) -> ValidationResult: ...
    def submit(self, order: CanonicalOrder, data: MarketData) -> Fill: ...
# gmrl.analytics.metrics
def calculate_metrics(equity: pd.DataFrame, fills: tuple[Fill, ...],
                      realized_matches: tuple[RealizedMatch, ...],
                      annual_risk_free_rate: float = 0.0) -> dict[str, float | None]: ...
# gmrl.taxation.estimator
def estimate_tax(realized_gain_eur: Decimal, allowance_remaining_eur: Decimal,
                 effective_rate: Decimal) -> Decimal: ...
```

`GMRLError` subclasses `DataValidationError`, `DataUnavailableError`, `QuotaExceededError`, `OrderRejectedError`, `AccountingError` give actionable English messages. `submit` raises OrderRejectedError rather than filling a rejected request. Stable IDs use internal synthetic IDs in demo, never an invented ISIN. An instrument ID identifies a tradable listing; ISIN alone does not merge currencies/venues. Provider symbols are an immutable tuple.

## Data truth and event chronology

Raw OHLC plus separate corporate actions is the only execution input. Adjusted series may be derived for research and must have a distinct name and metadata. CSV `price_basis` must equal `raw`; reject absent/adjusted/mixed basis, missing required data, duplicate instrument/session, naive timestamps, nonfinite values, negative volume, bad OHLC and unknown instruments. Required UTF-8 CSV columns: instrument_id, session_date (ISO date), open_at, close_at, available_at (ISO8601 offsets), open, high, low, close, volume, price_basis. Currency/MIC come from registered instrument. Imported data is not automatically trusted or broker-reconciled; file hash and import time are recorded. CSV action/FX import is deferred unless separately validated; a non-EUR import without valid FX cannot run.

Bars are available only after their close and declared availability. A strategy sees a physically filtered immutable history containing no future values; availability must be <= decision time. Select one global decision cutoff after relevant daily closes; quantity is frozen using only decision-time known marks/FX and costs; orders target the first scheduled session open strictly after decision time. Only the simulator reads bar.open at that UTC opening event and emits OpeningEvent; strategy/sizing never receives future HLCV, even though the simulator owns the complete dataset. Revalidate frozen quantity at execution against cash, FX, limits and price; reject rather than resize using future opening prices. A missing expected open rejects/cancels that order, never defers it to another session. Never execute at the signal close. Pre-open fills may use only FX known by that open, never a later same-day fixing. EUR quotes are identity 1. A quote is EUR per one local currency unit: local price times quote gives EUR. Reject future/zero/negative FX. No inverse-direction guessing.

Preserve each listing's explicit venue session calendar and operate on a union of events. A closed market has no tradable bar. Do not forward-fill OHLC or volume into a holiday. Missing an expected session is an outage: do not trade, warn, and invalidate a result if holdings cannot be valued under the configured age limit. Last known close may be used for valuation only with an age/stale flag, never execution. Default conservative thresholds are configurable (price 96h, FX 96h), measured in elapsed hours; fixture calendars document weekends/holidays. Unknown real calendars block a claim of production historical correctness. No zero-fill returns or look-ahead bfill.

All events process in UTC order. Equal-time priority is dividend entitlement, split, dividend payment, opens, completed-bar publication, then decisions/valuation. Deterministic instrument/action IDs break ties within a priority. Actions require available_at <= effective_at; late-known actions reject the affected run. Same-time split/dividend is rejected unless dividend_basis explicitly names pre_split or post_split; post_split entitlement quantity is derived from the declared split ratio even though entitlement is recorded first. Corporate actions are ID-deduplicated. Split amount is new units / old unit; apply before effective session open, multiply quantity, divide per-unit basis, preserve total basis/equity. Splits must preserve representable lot quantities exactly under selected precision/whole-share mode; unsupported precision, fractional entitlement or cash-in-lieu rejects rather than rounding away wealth. Dividend amount is local cash per entitled pre-ex-date unit: create a receivable at ex time. DividendReceivable.amount_local is the TOTAL local entitlement, not per-unit cash. Settle at pay_at using FX whose observed_at and available_at are both <= pay_at and whose age is within max_fx_age_hours measured at pay_at; later same-day FX cannot settle an earlier payment. Modeled dividend FX conversion fees are explicitly zero in MVP. Never credit adjusted total-return prices a second time. Receivable valuation is included in equity until settlement; share sales after ex date do not erase entitlement. Missing pay dates block action-inclusive runs rather than invent payment timing. For demo, all events and availability times are documented synthetic facts. Unknown delisting proceeds cannot be inferred; halt affected valuation and explain.

Fixtures use a published deterministic arithmetic generator or committed values, fixed seed where randomness is needed, fixed dates, deliberate gaps/actions/FX moves, SHA-256 provenance and a conspicuous SYNTHETIC SAMPLE label. Do not assign generated prices to real tickers or call them historical market observations. Macro sample series are educational only; revised macro vintages and official global coverage are later phases.

## Accounting and execution

Cash is EUR only; a trade converts its full local consideration immediately, with explicit FX charge. Foreign cash accounts are unsupported. Buy effective price = raw open * (1 + spread_bps/20000 + slippage_bps/10000); sell uses minus. Reject nonpositive price and impossible cost rates. Fee = fixed EUR + absolute EUR consideration * commission_bps/10000. FX cost = absolute EUR consideration * fx_fee_bps/10000 for non-EUR only. Buys subtract consideration + fee + FX cost; sells add consideration - fee - FX cost. Realized P&L uses FIFO lots including allocated buy/sell costs. The ledger emits immutable RealizedMatch records with split-adjusted matched quantity and acquisition/disposal times; metrics never reconstruct lots from fills. Freeze affordable target quantities at decision time, reserving cash conservatively. Process cross-venue opens in actual UTC order: later sale proceeds cannot fund earlier buys. Sell-before-buy applies ONLY to opens sharing exactly the same timestamp, with stable instrument ID ordering. Revalidate at execution; a gap making a frozen buy unaffordable rejects it, not a retroactive rescale. No negative cash, holdings or aggregate weights >1; residual EUR cash earns zero.

Equity = cash EUR + sum(quantity * raw mark local * as-of FX) + dividend receivables EUR. Fees reduce equity exactly once; deposits increase cash and are external flows, not gains. Backtests initially use no contributions; Portfolio Simulator may present separately labeled cash-flow scenarios and time-weighted returns or explicitly omit CAGR for flow cases. Exposure = invested gross EUR / equity. Initial row is initial equity before the first transaction. Do not hide initial fees by starting the return series after the first fill.

Paper orders use a selected historical/sample decision snapshot and its next scheduled open, never pretend to access current quotes. Validate positive quantity, available instrument/session, freshness, FX, available cash including costs, sell quantity, max order EUR, post-trade position concentration, spread cap and participation against prior completed session volume (not future full-day volume). Reject rather than partly fill manual orders. SQLite transaction atomically stores order/fill/state with a unique client_order_id; canonical identity includes the order payload, dataset_id, costs and limits; identical replay returns the prior fill BEFORE validating current state/time/cash. Same ID with conflicting canonical identity rejects. Streamlit reruns must not duplicate submissions. Repository.paper_transaction uses SQLite BEGIN IMMEDIATE, commit-on-success and rollback-on-any-exception; unique client IDs, foreign keys and expected-version checks enforce concurrent replay safety. One root contains exactly one paper account. Account initial capital is persisted and conflicting constructor capital rejects; simulation time cannot move backward for new operations. Version, simulation time, processed action IDs, canonical orders, fills, action records and journal persist atomically with account/lots/receivables. Decimal values serialize losslessly as text, never SQLite REAL. Crash rollback must leave no partial fill/account update. Persistent journal and account survive app restart. Backtest target-weight orders and manual orders share ledger/cost semantics.

## Strategy and metrics conventions

MVP names: `buy_hold` (equal weight selected universe; initial allocation only), `trend` (close > trailing SMA, otherwise cash, monthly rebalance), `momentum` (positive trailing local total-return momentum, top configurable N with stable ID tie-break, monthly equal weight). Parameters include lookback and top N; require complete warm-up and explicit action-safe return series, or reject action-containing trend AND momentum input until that derivation passes tests. Signals computed only from known closes; both trend and momentum require point-in-time split-normalized signals or reject unsupported action inputs; adjustment may use only actions already effective and available at that decision. Raw split jumps must never become trend or momentum signals. Remaining fourteen-strategy library requirements are research entries, not active dropdown choices. No optimized profitability claims.

Equity table uses UTC aware `timestamp`, `equity_eur`, `cash_eur`, `exposure`, `external_flow_eur`, `stale`. Use one daily UTC cutoff (23:59:59.999999 UTC) on each date in the union of venue session dates, plus the initial-capital row immediately before the first event; no per-fill or per-venue extra return rows. Decisions use that cutoff after all available daily closes. Daily simple returns include initial transaction costs. Total return E_end/E_start-1; CAGR uses actual elapsed days /365.25. Annualized geometric return is CAGR, separately labeled from arithmetic mean return*252. Volatility uses sample std(ddof=1)*sqrt(252) and a disclosed 252 convention; nontrading valuation rows do not multiply observation counts. Sharpe uses mean daily excess/std daily excess*sqrt(252), daily risk-free=(1+annual rate)^(1/252)-1. Sortino = mean(excess) / sqrt(mean(min(excess,0)^2)) * sqrt(252), using all return observations in downside mean. Undefined/insufficient denominators yield None with explanation in BacktestResult.warnings, not infinity/zero. Max drawdown is min(E/cummax(E)-1); duration is calendar days from peak until recovery or endpoint (unrecovered flagged). Calmar=CAGR/abs(max drawdown). Monthly/yearly returns compound within period. Turnover=sum(abs traded EUR)/(2*mean equity), disclosed two-sided convention; costs are EUR totals by component. Exposure is mean daily exposure. Trade count counts fills, while win rate/profit factor/holding period use completed FIFO matched lots and explicitly exclude open lots; profit factor is gross positive net realized P&L / abs(negative net realized P&L). Undefined if no losses. Benchmark uses same calendar, initial capital, cost assumptions and execution lag. Export parameters, provenance hashes, warnings, fills, equity and metric conventions as CSV/JSON. Worst periods are sorted monthly returns in MVP. Rolling windows, train/test/walk-forward, Monte Carlo and multiple-testing corrections are later; a fixed sensitivity grid can be added only with clearly labeled in-sample results.

## Provider resilience contract

Demo and CSV adapters are functional v1 providers. Live catalog entries do not imply implemented adapters. TTL cache key includes provider, sorted unique instrument IDs, interval, date bounds, raw/action mode and schema version. SQLite records request timestamps, outcome and quota debit, even failed attempts where provider rules debit them. Unknown quota stays unknown, never unlimited. CachedProvider checks expiry, coalesces same-process duplicate requests, uses a configurable token bucket, at most three TOTAL attempts (initial request plus at most two retries) with bounded exponential jitter, honors Retry-After and never retries authentication/validation failures. Clock/sleep/random/rate_policy are required keyword-injected dependencies. CacheResult carries data, dataset ID, retrieval/expiry timestamps, cache status and warnings; observation age is independent of retrieval TTL. A fresh cache hit may contain historically old observations and does not make them executable current prices. Fallback is an explicit ordered configuration of compatible providers, preserves changed provenance, never silently combines adjusted/raw series. Persisted cache remains usable offline with stale labeling; stale data cannot authorize fills. Incremental tail updates retain revision history; disputed revisions require revalidation. Conditional requests and batching are capability flags, not assumed universal features. Initial sample path has zero network calls; actual external adapters wait for verified licensing, tested responses and separate scope.

## Twelve pages and meaningful MVP controls

| Page | Required MVP behavior | Explicit limitation |
|---|---|---|
| Global Dashboard | Select demo universe/watchlist, show coverage/freshness and source | Synthetic market overview |
| Market Explorer | Filter registered country, sector, currency, class; select asset | Sample registry only, no TR availability claim |
| Asset Research | Asset/date selection, OHLC/volume/returns and action table | No unverified fundamentals |
| Global Macro Dashboard | Select labeled synthetic FX/macro series and compare dates | No current yield curve/inflation claim |
| Strategy Builder | Select three strategies, universe, lookback, capital, costs, dates | Research strategies disabled with reason |
| Backtesting Lab | Run, compare saved experiments, inspect fills and download report | Synthetic backtests, no profitability evidence |
| Portfolio Simulator | Change allocation/costs/scenario and run the same engine | Contributions explicitly deferred unless flow handling verified |
| Paper Trading | Submit sample market buy/sell, view durable cash/holdings/order status | Internal paper only; no current execution |
| Risk Dashboard | Select experiment, concentration/FX/exposure/drawdown; scenario shock slider | Simple instantaneous shocks, no VaR validation |
| API Management | Inspect provider/cache/quota, run offline adapter validation | External connectivity unavailable until adapter exists |
| Trade Journal | Add/edit hypothesis and lesson linked to PAPER ID, export | No broker imports/reconciliation claim |
| Learning Center | Search/select documentation chapter and exercises | Research coverage status shown |

All pages show simulation banner and per-series provenance; no decorative fake KPIs. Unsupported controls must be disabled and explained. A sample API test is explicitly an offline adapter test.

## Deterministic release tests

1. Future bar/FX mutation cannot change earlier weights/fills; decision close at 100 followed by open 110 must fill at 110 plus costs, never 100.
2. EUR1000 buys 10 units at USD100 with EUR/USD-unit=0.90: cash EUR100, holding EUR900; same local mark and FX1.00 gives equity EUR1100. An inverse quote is not accepted under the contract.
3. Raw 100 to 99 with EUR1 dividend per unit retains equity EUR100 for one unit through receivable/payment; adjusted input rejects. Sell after ex before pay still receives dividend. Duplicate action ID rejects/deduplicates deterministically.
4. Two-for-one split changes 1x100 to 2x50 without P&L or momentum signal; cost basis total remains100.
5. Buy EUR100 with fee1 and FX cost0.5 subtracts101.5 exactly; corresponding sell applies its own cost once. Insufficient cash with fees rejects. Weight sizing respects affordability.
6. Exchange holiday retains the holding valuation with stale metadata but no executable bar; missing expected open blocks fills. Future FX and over-age FX reject. No artificial filled holiday bar.
7. Buy then sell ledger reconciles cash, quantity, FIFO realized P&L, receivables and equity. Short sale, leverage, negative quantity and duplicate mismatched client IDs reject. Identical replay/restart returns one fill.
8. Flat equity metrics produce undefined Sharpe/Sortino/Calmar, drawdown zero; known peak100/trough80 gives -20%; monthly compounding and initial fee return verified.
9. Cache TTL/quota/retry/fallback tests use fake clock/transport; offline demo test fails on any attempted network call. CSV rejects ambiguous basis/naive time/duplicate/bad OHLC.
10. Streamlit AppTest exercises asset selection, configuration, run, comparison, export and paper submit twice; separate localhost launch smoke confirms entry point. Test installs and actual commands/results must be recorded; no tests have run at this design stage.

11. Cross-venue cash chronology: an Asian opening buy cannot spend later European sale proceeds; same-time sells may fund same-time buys only. Future HLCV mutation cannot change frozen quantity or prior decisions; missing expected open cancels.
12. Reject late-known actions and ambiguous equal-time split/dividend; test declared pre/post basis, total entitlement and unsupported cash-in-lieu. Payment FX uses the pay-time cutoff and age, with zero modeled dividend conversion fees.
13. Split-aware partial FIFO matches retain acquisition date, total allocated basis and net P&L; metrics consume RealizedMatch rather than reconstruct fills.
14. Concurrent duplicate canonical submissions yield one fill; different dataset/cost/limits under same ID rejects. Crash injection rolls back order/fill/actions/journal/state; restart rejects initial-capital conflict and backward new-order time while identical replay succeeds.
15. On native Windows, zoneinfo resolves fixture venue zones and UTC/DST transitions; if no timezone database is available, stop and propose a separately pinned tzdata dependency for approval, never silently use local machine time.

Final quality gate: pytest unit/integration and deterministic end-to-end tests, Ruff, mypy on typed core (narrow documented missing-stub exceptions), package wheel build and clean install smoke. No unsupported cross-platform claim: Windows is the verified target; POSIX instructions may be documented later as untested. No guaranteed returns or personal suitability claim.
