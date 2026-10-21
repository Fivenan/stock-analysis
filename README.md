# Global Market Research Lab

English, EUR-based, offline research and internal paper simulation. **SIMULATION ONLY · SYNTHETIC SAMPLE**. Nine invented listings cover US, Germany, UK, Japan, Taiwan, Korea, Indonesia, mainland China and Hong Kong with 2024–2025 arithmetic prices. They are not actual securities or observed market history.

## Native Windows setup

Run in the repository root in PowerShell. Requires installed Python 3.12; no activation or execution-policy change is needed. The lock targets Windows CPython 3.12. Network access is needed for the first dependency installation, not normal offline use.

```powershell
# [modifying] Create project-local environment
py -3.12 -m venv .venv
# [modifying] [network] Install the approved exact wheel hashes
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-windows-py312.lock
# [modifying] Install this checkout without resolving additional dependencies
.\.venv\Scripts\python.exe -m pip install --no-deps --no-build-isolation -e .
# [read-only] Verify
.\.venv\Scripts\python.exe -m pytest
# [modifying] Launch local application; runtime metadata stays under .runtime
.\.venv\Scripts\python.exe -m streamlit run app/main.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
```

Open `http://127.0.0.1:8501`. Stop with Ctrl+C. The app works without API keys or a broker account. Bind to loopback only; this is a personal local app without multiuser authentication. To move the installation, stop the app, retain `.runtime` privately and preserve its initial paper capital. Never publish that directory. `GMRL_RUNTIME` can select a separate private runtime directory for tests or a separate research account.

## Static companion

```powershell
# [modifying] Generate allowlisted public files, no credentials or network
.\.venv\Scripts\python.exe scripts/build_static.py
```

Output: `build/site/index.html`, relative assets, `.nojekyll`, computed synthetic CSV/JSON downloads and a SHA-256 `manifest.json`. Open index locally or publish the reviewed directory to GitHub Pages in a separate publication step. It needs no Python server on Pages and works beneath `/stock-analysis/`. Pages cannot host the Streamlit app. Build never reads `.runtime`, imports, exports, `.env`, `.office` or private journals. It refuses unexpected artifacts in its output directory. This command does not push or change Pages settings. The repository is private; Pages plan eligibility remains unverified. See [deployment and future updates](docs/USER_GUIDE.md#deployment-and-future-updates) for the separate source and static publication procedure.

## What works and what remains

Twelve routed views; three strategies (buy-hold, moving-average trend, positive cross-sectional momentum); daily EUR engine with next-open fills, costs, FX, split/dividend handling; configurable allocations; saved experiments, benchmark, exports; durable internal paper account and append-only journal; simple concentration/shocks and isolated tax estimate. See [user guide](docs/USER_GUIDE.md), [trading course](docs/TRADING_GUIDE.md), [90-day plan](docs/LEARNING_PLAN_90_DAYS.md), [verification](docs/VERIFICATION.md), and [status](IMPLEMENTATION_STATUS.md).

Real market feeds, actual venue calendars, full global history, broker statement imports/reconciliation, contributions/TWR, external brokers, full German tax accounting, walk-forward, Monte Carlo and the remaining strategy research entries are deferred. The original `wiki/` remains preserved. Documentation research coverage is broader than executable sample coverage. No synthetic result validates a strategy or grants permission for live trading.
