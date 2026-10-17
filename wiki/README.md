# Trading wiki

_Last checked: 2026-10-17 · For a private investor in Germany who uses Trade Republic._

> **Disclaimer.** This wiki is a compilation of publicly available, sourced information for learning. It is **not investment, tax or legal advice**, and nobody who wrote it is a licensed financial adviser. Markets can fall a long way and stay down for years; you can lose money. Figures marked "(unverified)" could not be confirmed from a primary source on the date above. Check fees, rules and product availability in the Trade Republic app and with the official source before you act.

## Reading order

| # | Page | What you get |
|---|---|---|
| 1 | [Trading basics](01-trading-basics.md) | Instruments, how an order works, costs, risk, German tax, Trade Republic specifics, glossary |
| 2 | [Markets overview](markets/README.md) | One table comparing the five markets: hours in German time, currency, tax, access |
| 2a | [Germany](markets/germany.md) | Xetra and the German venues, DAX / MDAX / SDAX / TecDAX, BaFin, Directors' Dealings |
| 2b | [Europe](markets/europe.md) | Euronext, LSE, SIX, Nasdaq Nordic, BME; EURO STOXX 50 / STOXX 600; withholding-tax table |
| 2c | [USA](markets/usa.md) | NYSE / Nasdaq, S&P 500, SEC and EDGAR, T+1, 15 % US withholding at source (Trade Republic is a Qualified Intermediary), why US ETFs are not available |
| 2d | [China](markets/china.md) | Shanghai, Shenzhen, Hong Kong; A / H shares, Stock Connect, VIE and delisting risks |
| 2e | [Indonesia](markets/indonesia.md) | IDX, IHSG / LQ45, OJK, trading sessions, IDR risk, limited access from Germany |
| 3 | [Strategy](strategy.md) | What the evidence says, nine strategies compared, risk management, a playbook template |
| 4 | [APIs](apis.md) | Public market-data APIs and insider / disclosure sources, with code examples |

## The short version

These points are drawn from the pages above. Each is sourced there.

1. **Costs scale against small trades.** Trade Republic charges €1 per order in the default Bestpreis mode (€2 plus external costs if you pick the venue); savings plans are free. On a €50 trade that is 4 % for buying and selling; on €5,000 it is 0.04 %. See [Trading basics → Costs](01-trading-basics.md#3-costs).
2. **Most active approaches lose to the index.** In S&P's SPIVA reports, most professional funds trail their benchmark over ten years. Studies of private traders (Barber & Odean; Taiwan and Brazil day-trader studies) find that frequent trading loses money for the large majority, and ESMA reports that 74–89 % of retail CFD accounts lose. See [Strategy §1](strategy.md#1-what-the-evidence-says-first).
3. **Known "edges" fade.** Published factor returns fell by about 58 % after publication (McLean & Pontiff). Following public insider buying has some evidence behind it, mainly in small, hard-to-trade stocks; copying 13F filings or politicians' trades comes with reporting delays of up to 45 days. See [Strategy §2.8](strategy.md#2-strategy-catalogue).
4. **Realistic expectations.** US equities returned about 6.6 % a year after inflation from 1900 to 2025 (the world average is lower), which doubles real money roughly every 11 years, with drawdowns of more than 50 % along the way. Anyone promising much more, faster, is a red flag. See [Strategy §5](strategy.md#5-realistic-return-expectations).
5. **Tax matters.** German capital gains and dividends are taxed at 26.375 % plus church tax above the €1,000 saver's allowance (€2,000 for couples). Equity ETFs get a 30 % partial exemption. Trade Republic withholds the tax automatically; a *Freistellungsauftrag* (exemption order) tells it how much of your allowance to apply before withholding. See [Trading basics → German tax](01-trading-basics.md#5-german-tax).
6. **Insider data is public and legal to use.** Form 4 on SEC EDGAR and BaFin's managers' transactions database are free. Trading on *non-public* information is a crime; reading published filings is not. Trade Republic has no public API, and unofficial clients conflict with its customer agreement, so never give them your login. See [APIs](apis.md).

## Ideas for how people try to profit, ordered by evidence

This is a map of approaches, not a recommendation. The [Strategy](strategy.md) page has the evidence, risks and a [playbook template](strategy.md#6-a-practical-playbook-template) to fill in yourself.

| Approach | Evidence (per the Strategy page) | Fits Trade Republic because… |
|---|---|---|
| Broad index ETF savings plan (*Sparplan*), held long term | Strongest | Free savings plans, fractional amounts |
| Core-satellite (index core plus a small, capped "ideas" part) | Good for the core; satellite usually at or below the index | Satellite trades cost €1 each (Bestpreis), which is a larger share of small orders |
| Factor tilts (value, momentum, quality, small caps) | Real but smaller after publication; long dry spells | Factor UCITS ETFs available as savings plans (check the app) |
| Dividend focus | Weak as a return source; tax drag in Germany | Dividend ETFs and single shares available |
| Trend following (e.g. 200-day average) | Mixed; reduces drawdowns at the cost of whipsaws | Needs discipline; €1 per switch |
| Insider-buying signals | Some evidence, concentrated in small caps; fades quickly | Data from [APIs](apis.md); small caps may be illiquid on German venues |
| Swing and day trading, knock-outs, CFDs | Weak to negative; most participants lose | Knock-outs and derivatives offered, which makes it easy to lose quickly |

## Glossary

The full glossary is in [Trading basics → Glossary](01-trading-basics.md#7-glossary).

## Maintenance

- Every page has a "Last checked" date and a numbered Sources list. Re-check fees, tax allowances and API free tiers at least once a year; they change often.
- Items marked "(unverified)" are the first candidates for a re-check.
