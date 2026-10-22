# Implementation status

Progress merged from completed worker handbacks. This file distinguishes implemented source, executed checks and unverified runtime behaviour.

| Component | Status | Verification / limitation |
|---|---|---|
| Architecture and worker contracts | Step 4 final GO after amendments | UTC event/frozen sizing, action/FX timing, atomic paper state, RealizedMatch and cache contracts tightened |
| Dependency installation | Installed and independently reproducible on Windows CPython 3.12.6 | All 52 exact hash-locked wheels installed in a fresh environment; pip check, isolated project wheel install and offline demo smoke PASS |
| Provider/broker/tax/global access research | Six documents merged; Step 2 PASS for offline-paper scope | 73-source register; authenticated entitlements, individual broker instruments and redistribution rights remain unresolved |
| Repository integration | Existing history preserved; main tracks origin/main | Baseline 84aac2fd945e05dc2a0df32697bfefdfbbe2bbbe; original wiki preserved; current remote commits are the publication authority |
| Package/data/fixtures/cache | Step 6 independent runtime GO | Nine listings/4,671 bars; timezone/DST, Parquet integrity, persisted cache/quota metadata and experiment storage verified with network forbidden |
| Strategies/backtest/metrics/tax estimator | Step 8 independent financial GO | 77 tests PASS (37 author + 40 independent); scoped financial Ruff/mypy PASS |
| Twelve-page application/guide | Step 10 independent local acceptance GO | Actual Streamlit AppTest workflows, frozen report configuration, changed-parameter rerun and persisted risk cursor verified; no pixel review claimed |
| Internal paper broker/journal | Implemented; independent financial GO | Atomic execution, replay, restart, risk, FIFO and append-only journal verified; internal historical sample only |
| Live execution | Excluded | No live adapter or key-based enabling path is permitted |
| Local app + static companion + GitHub integration/push | APPROVED scope; repository integrated locally | Local acceptance complete; main holds source/docs/wiki, gh-pages only reviewed build/site contents; remote commits and Pages deployment history establish publication; check GitHub for current repository visibility and Pages configuration; private repositories require an eligible Pages plan |
| Executed foundation checks | 36 foundation unit/integration tests PASS; scoped Ruff and mypy PASS | Independent runtime gate covers 16 typed foundation files; these are not financial or whole-app acceptance |
| Full combined local tests/lint/types/build | Step 10 independent local acceptance GO | 125 tests PASS; full Ruff PASS; mypy 44 source files PASS; current wheel installed/imported outside checkout offline; loopback health/root HTTP 200; no measured coverage claim |
| Secrets review and remote publication | Separate release gate | Local acceptance establishes no source push or Pages publication; consult remote commits and Pages deployment history |

Release gates: secrets audit and verified source/static publication; current remote commits and Pages deployment history establish their publication outcome. Step 10 local acceptance is complete; review ARCHITECTURE and ROADMAP for exact acceptance and unsupported features. Synthetic examples are educational, not observed market history or guaranteed performance.

No orders have been submitted to any external broker. Financial and independent local whole-app acceptance passed. Timezone and cache/Parquet foundation checks passed; project-local dependencies are installed. No publication or live-market validation follows from these checks.

UI/static implementation: app/main.py, scripts/build_static.py, README.md, docs/TRADING_GUIDE.md, USER_GUIDE.md, LEARNING_PLAN_90_DAYS.md and VERIFICATION.md. See VERIFICATION for actual final commands/counts. Static companion has no Python runtime, no private journal/account records and no automatic publishing. Contributions/TWR, external feeds/brokers, full tax, remaining research strategies and advanced validation remain deferred.
