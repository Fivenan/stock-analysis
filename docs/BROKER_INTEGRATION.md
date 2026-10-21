# Broker compatibility and simulation boundary

Research/access date **2026-10-18**. The initial product requires no broker account and has **internal paper execution only**. Data adapters, instrument identity, accounting and execution must be separate components. A future API key must never activate live routing automatically.

## Trade Republic evidence

| Question | Finding | Status / primary evidence, accessed 2026-10-18 |
|---|---|---|
| Public supported trading/developer API? | No first-party public API specification, supported SDK, API contract or paper endpoint was located in official support searches. Absence of located documentation is not proof no API exists. Banking/PSD2 access, if available, would not by itself establish securities execution support. | **UNVERIFIED** capability; [official support](https://support.traderepublic.com/de-de/705) is product evidence, not API authorization. Requires explicit broker-supported documentation before any connector. |
| Unofficial community interfaces? | They must not be treated as supported APIs. No private-interface login, reverse-engineered authentication, browser automation, anti-bot workaround or credential collection is approved. | **Design decision**; no unofficial code was downloaded, installed or run. |
| Venue | German support states stocks, ETFs and bonds use LS Exchange; stocks/ETFs may fall back to Tradegate on LS Exchange failure. Derivatives use stated issuers OTC where available. | **VERIFIED**, [German venue page](https://support.traderepublic.com/de-de/705). This is not direct NYSE, Xetra or Asian home-market routing. |
| Fees | Support describes EUR1 external settlement cost for an individual securities trade, product costs and possible currency conversion costs for foreign dividends. Exact instrument/order disclosure and current schedule prevail. | **VERIFIED** general description, [ex-post costs](https://support.traderepublic.com/en-de/809-What-is-the-ex_post-cost-information). Do not apply one fee universally to savings plans, corporate actions or every product. |
| Tax records | Official German annual-tax-certificate page located, but no substantive details extracted. Exact delivery date, downloadable formats and complete field schema not verified. | **PARTIALLY VERIFIED**, [certificate page](https://support.traderepublic.com/de-de/1078-Was-ist-die-Jahressteuerbescheinigung). No assumption of CSV portfolio/API export. |
| Tax withholding | Domestic withholding framework exists; this research does not verify every TR operational withholding/reclaim process or account circumstance. | **PARTIALLY VERIFIED**, [EStG section 43](https://www.gesetze-im-internet.de/estg/__43.html); reconcile actual official statements. |
| Individual global security availability | No account/instrument search or current catalog inspection performed. | **UNVERIFIED for every instrument**, including ADRs, UCITS funds and commodity products. No fabricated TR mappings. |

Paper transaction costs may use an **illustrative configurable** EUR1 contribution plus separate spread, slippage and FX assumptions. Label that preset as a simplified assumption; it does not reproduce all current broker costs. Reference-market daily closes cannot establish LS Exchange bid/ask or a real fill. No claim of simulated broker fidelity should be made.

## Officially documented paper alternatives

| Option | What is established | Unresolved German-resident/account/cost conditions | MVP decision |
|---|---|---|---|
| Internal paper broker | Local simulated cash/positions/orders; deterministic fixture prices; no network execution | Fill model, calendars, costs and latency are assumptions requiring tests. No real-time entitlement is needed for offline demo | Required default; non-live IDs, visible simulation state, no remote order adapter. |
| Alpaca | Official [paper documentation](https://docs.alpaca.markets/us/docs/paper-trading) describes separate paper environment and limitations | **VERIFIED docs**, accessed 2026-10-18; no signup/runtime test. German residency eligibility for a particular paper-only/live account, available feeds/instruments and current costs must be confirmed. Simulated fills omit real execution effects; no assumption of worldwide live brokerage eligibility | Future optional paper connector only after current terms review; no new account required for MVP. |
| Interactive Brokers | Official [paper-account instructions](https://www.interactivebrokers.com/campus/trading-lessons/request-paper-trading-account/?retakeFinal=1) distinguish paper accounts and trial/API access; [supported Web API docs](https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-doc/) exist | **VERIFIED docs / PARTIALLY VERIFIED account requirements**, accessed 2026-10-18. Official pages differ by interface/account context about approval/funding. Trial UI access does not prove API permission. Check TWS vs Web API, entity/residency, approved account, funding, permissions, market-data subscriptions and fees separately | Future optional paper integration; not a keyless substitute and not required for demo. |

No live eligibility, fees, supported country onboarding or authenticated paper execution was tested for Alpaca or IBKR. Neither alternative is a recommendation to open/fund an account. No credentials were requested.

## Import and reconciliation design

An optional manual import can accept user-owned, sanitized statement data after schema mapping. Retain original document hash, import date, transaction ID, booking/trade/value date, ISIN, quantity, cash currency, gross amount, fees, FX conversion, withholding and corrections. Unknown fields remain unknown. Do not assume a broker provides this exact machine-readable schema.

Compare broker statements to an independent cash-and-position ledger; classify transfers, dividends, tax debits/refunds, splits and sales distinctly. Match booking corrections and avoid duplicate imports. Simulated taxes stay separate from actual withholding. Account holdings must not be sent to market-data search endpoints; only the public symbol required for the approved request is sent.

## Future integration gate

A new, explicitly implemented paper adapter would need documented support, endpoint allowlist, separate paper account configuration, response contract tests, account-type verification, stale-data/limits checks and paper-only order IDs. Live execution would require a separate implementation and explicit authorization/review; no configuration switch or credential entry should bypass this boundary.
