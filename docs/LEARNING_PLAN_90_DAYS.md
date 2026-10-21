# 90-day learning and paper research plan

Days 1–30 build understanding; days 31–60 practice reproducible backtests; days 61–90 practice internal paper operations only. Ninety days passing never authorizes live trading. Adapt time spent and policy inputs to your situation. All exercises use synthetic data unless a later separately reviewed lawful dataset is supplied.

| Week / days | Measurable objective | Exercise and review evidence |
|---|---|---|
| 1 / 1–7 | Explain shares, funds, bonds, currencies and derivatives in your own words | Read beginner guide; write five instrument cards with ownership claim, currency, loss mechanism and access question; solve exercises 1–2 |
| 2 / 8–14 | Reconcile three EUR trade examples to the cent | Calculate spread, commission and FX costs; explain order types and next-open timing; solve exercise 3 without looking, then check solution |
| 3 / 15–21 | Distinguish local return, EUR return and cash flows | Reproduce split/dividend examples; inspect DEMO-US raw prices versus action-safe index; show why the split is not a 50% wealth loss |
| 4 / 22–28 | Write a user-supplied policy and market-access checklist | Complete IPS blanks; compare direct listing, ETF, ADR and commodity equity; find dated official evidence in source register; leave unknown eligibility explicit |
| 5 / 29–35 | Finish foundation review by day 30; define one frozen hypothesis on day 31 | Score beginner exercises; preregister universe, strategy, benchmark, dates, costs, lag and rejection criteria; do not optimize |
| 6 / 36–42 | Reproduce one saved experiment from parameters | Run buy-hold and same-cost benchmark, save and export JSON/equity/fills; reconcile initial equity and two fills; record repository ID and provenance hash |
| 7 / 43–49 | Explain all three implemented strategy rules and warm-up | Run trend and momentum with fixed lookback; compare warnings and rejected orders; change one parameter as a labeled in-sample sensitivity exercise, retain failures |
| 8 / 50–56 | Detect five forms of invalid backtest evidence | Audit leakage, survival, publication dates, split/dividend handling and FX; manually outline chronological holdout/walk-forward protocol; acknowledge these app features are deferred |
| 9 / 57–63 | Close backtest review by day 60; start paper-only operations on day 61 | Complete experiment card; reject unsupported profitability conclusions; place one small DEMO-DE paper buy; press identical submit twice and prove only one fill |
| 10 / 64–70 | Demonstrate durable accounting and journal revisions | Restart, compare holdings/cash/fill ID; add hypothesis and lesson, append revision referencing prior ID; use a new PAPER ID for a later sell; export private journal |
| 11 / 71–77 | Document three risk scenarios including foreign FX | Compare price −20%, FX −10% and combined shocks with cash/receivables; reconcile exposure denominator; review risk plan without assuming VaR or forecast probabilities |
| 12 / 78–84 | Complete failure and recovery rehearsal | Attempt excessive quantity/conflicting replay/backward time; verify actionable rejection and unchanged account; stop app and copy runtime privately; document restore procedure |
| 13 / 85–90 | Produce a reproducible final research dossier | Include policy, hypothesis, frozen configuration, failed experiments, cost/FX/action audit, exports, journal and limitations; self-review against the rubric below; continue paper only |

## Weekly review template

Week/date ___; objective ___; evidence file/experiment ID ___; expected result ___; actual result ___; discrepancy ___; data/cost assumptions ___; mistakes and corrections ___; unanswered question ___; next week's bounded experiment ___. Score each objective 0 (not attempted), 1 (can repeat with help), 2 (can explain and reproduce unaided). Revisit any zero before increasing complexity. Keep a log of all tried parameters so failed rules do not disappear.

## Experiment card

Hypothesis and economic mechanism ___; precise falsification condition ___; universe and historical eligibility ___; raw/action basis ___; available-at timestamps ___; currency convention ___; train/validation/test intention ___; parameters frozen before inspection ___; benchmark ___; capital/cost/limits ___; rejection count/reasons ___; result/provenance IDs ___; statistical versus economic uncertainty ___; what this evidence cannot establish ___. With sample data the final field must include: no real-market strategy validation.

## Policy and risk review template

Purpose/horizon ___; available risk capital and cash needs ___; tolerable EUR/% loss ___; allowed instruments/venues ___; position/country/currency limits ___; minimum liquidity ___; maximum order/participation ___; stale-data response ___; operational backup ___; conditions to stop research ___; review person/date ___; outstanding suitability/legal/tax/access questions ___. Values remain blank until you supply them; default app settings are illustrations.

## End-of-plan acceptance rubric

Can you reproduce one experiment from exports, reconcile EUR cash and FIFO costs, distinguish local/FX returns, explain split/dividend neutrality, identify data leakage, retain failed trials, replay one order safely, recover private state and state every deferred capability? If any answer is no, repeat the relevant week. Even all yes means improved research practice only. Real datasets, source licenses, instrument access, operational/legal/tax questions and independent strategy validation remain separate gates; no schedule or app result grants live-trading approval.
