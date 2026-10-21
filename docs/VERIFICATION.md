# Verification record

Target: native Windows CPython 3.12.6. Exact approved environment: Streamlit 1.50.0, Plotly 6.3.1, Pandas 2.3.3, NumPy 2.3.3, PyArrow 21.0.0, Pydantic 2.12.0, pytest 8.4.2, Ruff 0.13.3, mypy 1.18.2 and setuptools 80.9.0. The 52-wheel Windows lock was independently installed with `--require-hashes`; clean isolated wheel installation and offline sample smoke passed. No additional dependencies were installed for the UI/static work.

Foundation acceptance: 36 tests (32 author + 4 independent runtime) passed. Financial acceptance: 77 tests (37 author + 40 independent) passed; scoped core Ruff/mypy passed. Dataset: nine synthetic listings, 4,671 raw bars, split/dividend actions and FX, 2024–2025. These checks establish selected deterministic invariants, not general financial correctness or profitable trading.

Application/static verification is recorded below. Step 10 independent local acceptance passed; publication/secrets review remains required. No remote publication is claimed here. No actual external API or broker request was made by normal app use.

## Step 9 executed local checks

Run from the repository root with `.venv/Scripts/python.exe` (native Windows):

| Command / scope | Actual result |
|---|---|
| `-m pytest -q` | 121 passed in 18.35s: existing 113 foundation/financial tests plus 8 UI/static integration tests |
| `-m ruff check app scripts/build_static.py tests/integration/test_app.py tests/integration/test_static.py` | All checks passed |
| `-m mypy app/main.py scripts/build_static.py` | Success, 2 source files; third-party missing stubs follow project configuration |
| `scripts/build_static.py` and repeated build in static tests | `build/site` created; identical manifest bytes on repeated builds; all file hashes and local href/src targets checked under `/stock-analysis/`; custom output escape and lexical linked-site boundary rejected; unsafe Markdown link schemes remain text |
| Native `subprocess.Popen` Streamlit launch with address `127.0.0.1`, port 8501, headless and usage telemetry disabled | Loopback `/_stcore/health` returned HTTP 200 body `ok`; child terminated in `finally` |

UI checks use the actual `streamlit.testing.v1.AppTest` entry point. They navigate all twelve routes; select DEMO-US asset research; run momentum plus same-cost benchmark; save using returned repository IDs and compare saved results; verify three download controls; reject an empty universe and excessive allocation; freeze allocation report parameters despite subsequent control changes; initialize paper account; submit twice with one fill; append journal; restart; replay a persisted canonical order and reject an excessive new quantity. Risk page renders against persisted simulation time. Downloads call the existing JSON/CSV exporters; financial export correctness is covered by financial tests. No browser visual-pixel inspection or cross-platform runtime acceptance is claimed.

The static builder reads only named public guides and committed synthetic report fixtures, writes relative local CSS/JS without CDNs, escapes Markdown/HTML text with clickable HTTPS/allowlisted guide links, refuses unexpected output files/symlinks and output escapes, and emits a content fingerprint plus individual SHA-256 hashes. It copies no `.runtime`, `.env`, `.office`, imports, exports, actual journals or account records. No automatic push exists. Full deployment and independent acceptance remain separate gates.

Known limits: nine invented listings are not full global coverage; no actual current quotes/macroeconomic series, real exchange calendars, external connectivity adapter, broker account, contributions/TWR, complete German taxes, imported broker reconciliation, automated chronological holdouts, walk-forward or Monte Carlo. Synthetic low-price/volume constraints intentionally reject some orders. All displayed financial numbers remain simulated and are not evidence of strategy performance.

## Step 10 independent local release acceptance

Executed 2026-10-21 on native Windows CPython 3.12.6, using the existing approved environment. Result: **GO for the bounded offline local paper MVP**. Secrets review, source push and static publication are separate pending gates. No public binding, external broker, new dependency or external provider probe was used for this gate. The existing optional bounded World Bank GDP metadata helper is separate from the application's offline provider and is not an active market-data adapter.

| Command / actual scope | Result |
|---|---|
| `.venv/Scripts/python.exe -m pytest -q` | 125 passed in 24.18s after the junction repair; includes four new independent acceptance cases |
| `.venv/Scripts/python.exe -m ruff check src app scripts tests` | All checks passed |
| `.venv/Scripts/python.exe -m mypy src app scripts` | Success, 44 source files; project missing-third-party-stub configuration retained |
| `.venv/Scripts/python.exe -m pip wheel --no-deps --no-build-isolation --no-index . --wheel-dir .office/acceptance/wheels` | Current package wheel built successfully without dependency/network access |
| Existing isolated lock environment: `-m pip install --no-index --no-deps --force-reinstall` current wheel; `-m pip check` | Install passed; no broken requirements |
| Installed interpreter with `-I`, working directory outside checkout, network-forbidden `load_demo()` | Imported installed site-packages package; nine listings and 4,671 bars passed |
| Native hidden-window subprocess Streamlit on loopback port 8502, headless, telemetry disabled | Health HTTP 200 body `ok` and root HTTP 200; child terminated and waited in `finally` |
| Repeat independent acceptance plus static tests | 7 passed in 8.82s; subsequent full Ruff and 44-file mypy passed again |

Independent AppTest acceptance blocks socket connections while running an actual configured backtest, checking EUR/provenance/fills/warnings/drawdown exports, freezing report metadata when controls change, rerunning with changed capital and retaining the last valid result after reversed dates. A separate case captures the actual risk function's valuation timestamp after a fill, verifies it equals the persisted simulation cursor, changes the shock control without mutating the account and replays the canonical order with exactly one fill. Empty Risk/Journal pages demand initialization without creating an account. Widget bounds enforce positive capital and nonnegative costs/weights; existing tests exercise empty universes and allocation totals above one.

A real native Windows junction exposed an output-boundary defect: `build/site` could alias a sibling directory within `build` and receive writes. The builder owner repaired explicit junction checks for output roots/descendants, provided targets before resolution, and public input roots/items. The new acceptance regression creates a real junction in an isolated temporary project and verifies rejection before any target write. A private account sentinel fixture remains absent from every emitted file; unexpected output files and unsafe/nonallowlisted Markdown links reject or remain escaped text. Existing static tests verify repeat manifest bytes, each SHA-256 file hash, prefix-relative href/src targets and downloads. CSS/JS are local assets with no CDN dependency. No visual pixel review was performed.

| Master acceptance criterion | Executed evidence / bounded result |
|---|---|
| 1 Setup | Prior independent fresh 52-wheel `--require-hashes` install retained; current wheel rebuilt, installed and imported outside checkout; pip check clean |
| 2 Local launch | Real Streamlit child: loopback health and root HTTP 200 |
| 3 Offline/no keys | Network-forbidden actual AppTest run and installed sample load; no credentials required |
| 4 Search/select asset | Existing twelve-route test and DEMO-US Asset Research selection; explorer registry filters are sample-only |
| 5 Data/provenance | Actual report JSON contains provenance; dashboard/asset source and artificial 2024–2025 scope inspected |
| 6 Configure strategy | Actual momentum selection and default buy-hold run; capital/cost/limit controls inspected; three active strategies |
| 7 EUR run | Executed EUR 12,000/15,000 runs and exported EUR conventions/initial equity |
| 8 Same-cost benchmark | Actual comparison wrapper/results; shared configuration and financial benchmark regressions |
| 9 Transactions/costs/drawdown | Nonempty exported fills/warnings and nonpositive drawdown assertion; financial FIFO/cost/drawdown golden cases |
| 10 Changed-parameter rerun | Original export remains unchanged before rerun; new capital changes experiment ID and benchmark initial equity |
| 11 Paper trade | Actual submit/replay/restart, one fill; risk rerender preserves complete durable history |
| 12 Report/trade export | Actual three download controls plus report JSON/CSV exporter regressions; original run/allocation configuration retained |
| 13 Provider status/consumption | Actual API Management route and offline adapter test; persisted quota/cache fields; catalog is not active real feeds |
| 14 Guides | Actual Learning Center route plus allowlisted searchable static guide build; user guide/methodology/architecture read |
| 15 No live orders | Execution/provider/UI source inspected: only internal historical paper reducer is routed; no credential control or external broker submission adapter |

Fresh all-cash accounts have a pre-sample persisted cursor; the Risk page uses a sample-date fallback for this time-invariant EUR cash display without advancing saved state. Filled-account valuation uses the real persisted cursor, independently asserted. This local gate does not validate real feeds/global coverage, external broker access, contributions/TWR, full tax accounting, walk-forward/Monte Carlo, the remaining eleven strategy research entries, profitability or suitability.
