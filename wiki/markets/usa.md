# USA stock market

_Last checked: 2026-10-17 · Educational content, not investment advice._

Related pages: [Markets overview](README.md) · [Germany](germany.md) · [Europe](europe.md) · [China](china.md) · [Indonesia](indonesia.md) · [Trading basics](../01-trading-basics.md) · [Strategy](../strategy.md) · [APIs](../apis.md)

Conventions: ET = US Eastern Time (EST/EDT); CET/CEST = German time. "(unverified)" marks a number or claim that could not be confirmed in a primary source during this research.

## 1. Overview

The USA hosts the two largest stock exchanges in the world by market capitalisation, the New York Stock Exchange (NYSE) and Nasdaq. The World Federation of Exchanges (WFE) reports global listed equity market capitalisation of USD 151.94 trillion at end-2025, up 18.5% in the year, across 49,054 listed companies on WFE-covered exchanges [1]. The WFE press release does not break out NYSE or Nasdaq separately. Secondary tables put each exchange in the range of roughly USD 30-45 trillion depending on date and definition (domestic vs. total); no single dated figure could be verified here (unverified). NYSE itself states "over 2,400 public companies", including over 530 international ones (undated) [2].

Role in the world: the US market is the main global reference for large-cap equity, technology and AI-related companies, and for equity derivatives. Many non-US companies list there as well (see ADRs in section 7).

## 2. Exchanges and main indices

**Exchanges.** US equity trading is fragmented across many venues under one rulebook, but three names matter most:

- **NYSE** (owned by Intercontinental Exchange): the NYSE family also includes NYSE American, NYSE Arca, NYSE National and NYSE Texas [9].
- **Nasdaq** (Nasdaq Stock Market): an all-electronic exchange, home of the Nasdaq-100 [6].
- **Cboe** (Cboe Global Markets): a derivatives and exchange operator, best known for US options and the VIX volatility index/futures/options [35]. It also runs US cash-equity exchanges (names such as BZX/EDGX, unverified; the fetched page does not list them).

**Main indices** (member counts and weights change; check the provider's factsheet for the current figure):

| Index | Members | What it measures | Top sectors |
|---|---|---|---|
| S&P 500 | 503 holdings in an ETF tracking it (as of 2026-08-31) [3] | Large-cap US equities; float-adjusted market-cap weighting, S&P Dow Jones Indices (unverified; provider page blocked) | Technology 45.2%, finance 13.6%, health care 9.1% (justETF sector classification [3]); under the GICS scheme, information technology is about 38% (unverified, fund-provider factsheet as of 2026-07-24 [37]) |
| Dow Jones Industrial Average (DJIA) | 30 (unverified) | 30 large US blue chips, price-weighted: a higher share price means a higher weight, regardless of company size (unverified) | Diversified; fewer technology names than S&P 500 (unverified) |
| Nasdaq-100 | 100 companies; Nasdaq's page lists 101 components, an ETF holds 103 lines because of multiple share classes [5][6] | The 100 largest non-financial companies on Nasdaq [6] | Technology 66.6% (justETF classification, 2026-08-31) [5] |
| Russell 2000 | 1,966 at 30 Dec 2023 per the FTSE Russell factsheet (unverified: current count not retrieved) [8] | The smallest 2,000 stocks of the Russell 3000; small-cap benchmark; free-float weighted | Broad; more financials, health care and industrials than large-cap indices (unverified) |

**Concentration.** Index weight is dominated by a handful of technology-related companies. The top 10 holdings made up 37.76% of the S&P 500 as tracked by one ETF on 2026-08-31 (NVIDIA 8.07%, Apple 7.03%, Microsoft 5.69%; Alphabet appears twice via two share classes) [3]. The top 10 in the Nasdaq-100 ETF are 46.15% [5]. Consequence: a "diversified" 500-stock fund behaves, to a large extent, like a bet on a few mega-caps. Russell 1000/3000 and equal-weight variants spread weight more evenly (unverified for current numbers).

**Russell reconstitution.** FTSE Russell is moving the Russell US indices from annual to semi-annual reconstitution in 2026; new listings are also added at quarterly reviews in March and September [7].

## 3. Trading hours

| Session | ET | German time (normal weeks) | German time (mismatch weeks) |
|---|---|---|---|
| Regular (core) session, NYSE/Nasdaq | 09:30-16:00 [9] | 15:30-22:00 | 14:30-21:00 |
| Pre-market / early session (e.g. NYSE Arca from 04:00; NYSE American, NYSE National from 07:00) [9] | 04:00-09:30 | 10:00-15:30 | 09:00-14:30 |
| After-hours / late session (NYSE Arca, NYSE American, NYSE National) [9] | 16:00-20:00 | 22:00-02:00 | 21:00-01:00 |

- **Lunch break:** none.
- **Daylight-saving mismatch.** US rule: DST starts on the second Sunday of March and ends on the first Sunday of November [13]. EU rule: summer time starts on the last Sunday of March and ends on the last Sunday of October [14]. For 2026 this gives (derived from those rules): US clocks forward 8 March, EU 29 March; EU clocks back 25 October, US 1 November. In the gaps (trading days 9-27 March and 26-30 October 2026) the US session runs 14:30-21:00 German time instead of 15:30-22:00. The next mismatch week starts on 26 October 2026. The 15:30 US open is a common rule of thumb; it is wrong in these weeks.
- **Holidays 2026 (NYSE):** 1 Jan, 19 Jan, 16 Feb, 3 Apr (Good Friday), 25 May, 19 Jun, 3 Jul (Independence Day observed), 7 Sep, 26 Nov (Thanksgiving), 25 Dec. Early close at 13:00 ET (19:00 German time) on 27 Nov and 24 Dec [9]. Official calendar: NYSE hours and calendars page [9]. Note that US and German holidays differ (e.g. Thanksgiving is US-only).
- **Extended and overnight trading.** Nasdaq has proposed near-24-hour trading (21:00 ET Sunday to 20:00 ET Friday with a daily one-hour pause), with a December 2026 "launch target" that depends on SEC approval; it was not approved as of the source's 2026-07-29 update [19]. Status as of today not verified.
- **Price limits.** Two mechanisms:
  - *Limit Up-Limit Down (LULD)* for single stocks during 09:30-16:00 ET. Bands are set around the average price of the last five minutes. For Tier 1 (S&P 500, Russell 1000, some ETPs) above USD 3.00 the band is 5%; for Tier 2 above USD 3.00 it is 10%. If the price stays at the band edge for 15 seconds, trading pauses for five minutes [12]. Bands double between 15:35 and 16:00 ET for Tier 1 [12].
  - *Market-wide circuit breakers*, based on the S&P 500's decline from the previous close: Level 1 at -7% and Level 2 at -13% halt trading for 15 minutes if hit before 15:25 ET; Level 3 at -20% halts trading for the rest of the day [11][12].
- **Settlement:** T+1 (one business day) for most US securities since the SEC's compliance date of 28 May 2024 [10]. Settlement for a German customer follows the custody chain of the broker; details to be checked in the broker's documents (unverified).
- **Lot sizes:** US exchanges have no mandatory minimum order for retail; the historical "round lot" is 100 shares but odd lots trade (unverified). Fractional shares depend on the broker (not verified for Trade Republic here).

## 4. Currency and FX risk for a euro investor

US shares are priced in USD. A euro-based investor carries EUR/USD risk on top of the stock risk: a falling dollar reduces the euro value of a position even if the share price is flat, and the reverse. On German venues the quote is shown in EUR, but it is derived from the US price and the current exchange rate (inference). Dividends are paid in USD and converted. Unhedged UCITS ETFs on US indices carry the same FX exposure; currency-hedged share classes exist as a category (check availability in the app). There is no capital control; the FX cost appears as spread in the EUR quote or as a conversion cost (check Trade Republic's price list).

## 5. Regulator and investor protection; filings

- **SEC** (Securities and Exchange Commission): federal regulator with a three-part mission: protect investors, keep markets fair, orderly and efficient, and facilitate capital formation. It oversees US securities markets, exchanges, broker-dealers and issuer disclosure [22].
- **FINRA**: a private, not-for-profit self-regulatory organisation under SEC supervision that supervises broker-dealers [23].
- **SIPC** protects customers when a US-member brokerage fails [36]. It is relevant to US brokers, not to a German bank. A Trade Republic customer's protections follow German/EU rules (see [Germany](germany.md)).
- **EDGAR** is the SEC's free filings database; full-text search covers filings since 2001 [24]. Key forms:
  - **10-K**: annual report with audited statements. Deadline 60/75/90 days after year-end for large accelerated, accelerated and non-accelerated filers [26].
  - **10-Q**: quarterly report, 40 days (large and accelerated filers) or 45 days after quarter-end [26]. The SEC proposed on 5 May 2026 to let companies file a semiannual **Form 10-S** instead of three 10-Qs; it is a proposal only, with the comment period ended on 6 July 2026 [20]. Check whether it has been finalised.
  - **8-K**: current report on material events, generally within four business days [26].
  - **Form 4**: insider transactions of directors, officers and holders of more than 10%, due within two business days of the trade [25]. Form 3 (initial) and Form 5 (annual) complement it.
  - **13F**: quarterly holdings of institutional managers with at least USD 100 million of 13(f) securities, due 45 days after quarter end (e.g. 15 May 2026 for Q1 2026). It shows long positions only, with a delay [21].
- **Earnings seasons.** Because 10-Q/10-K deadlines fall 40-60 days after period end, most S&P 500 companies report in the weeks after each quarter ends: roughly mid-January to mid-February, mid-April to mid-May, mid-July to mid-August, and mid-October to mid-November (calendar pattern, inferred from the deadlines). Many companies report outside US cash hours, which moves prices in pre-market and after-hours. Check each company's investor-relations calendar. See [APIs](../apis.md) for machine access.

## 6. Market characteristics and specific risks

- **Concentration:** see section 2. A few mega-cap technology stocks drive index returns in both directions [3][5].
- **Valuation and volatility:** the Cboe VIX is the standard measure of expected S&P 500 volatility [35]. I did not verify current levels.
- **Retail vs institutional:** institutional investors dominate volume; retail share data not verified.
- **Fragmented market, extended hours:** trading across many venues and, soon possibly, near-24-hour sessions [19]. Thin liquidity in pre- and after-market can mean wide spreads and large price jumps (general market structure; inferred).
- **Regulatory and political risk:** rule changes such as T+1 [10], possible optional semiannual reporting [20] and the Nasdaq extended-hours plan [19]. Trade policy, tax law and election cycles can move sectors (not quantified here).
- **Time-zone risk for EU investors:** US news during the German evening or night can only be traded at the next German-venue quote; limit orders can help (see [Trading basics](../01-trading-basics.md)).

## 7. Access from Germany via Trade Republic

- **Single shares:** US shares are available. As of July 2026 Trade Republic describes two modes: *Best Price* (the default, an algorithm compares tradable quotes across reference exchanges and executes against Trade Republic) and *Direct Price* (the user picks a venue from a list of global venues) [15][16]. Press coverage names Xetra, Euronext, Nasdaq and the NYSE among about 30 venues [18] (secondary; a sponsored article). Fees: EUR 1 per order for Best Price and EUR 2 per order plus external costs for Direct Price (press-sourced; confirm in the price list) [38]. The official venue-and-hours table could not be read here. The venue currency (EUR or USD) per venue is unverified.
- **Hours at Trade Republic:** Best Price for stocks and ETFs is Monday-Friday 07:30-23:00 CET; Direct Price hours depend on the venue; limit orders can be placed outside hours but market and stop orders cannot [15]. Take the app's venue table as authoritative.
- **Liquidity outside US hours:** between 07:30 and 15:30 German time the US market is closed or in pre-market, so a quote on a German venue is set by a market maker based on futures or last-close, with usually wider spreads (inference). Liquidity is best in the overlap of regular hours, 15:30-22:00 German time (14:30-21:00 in mismatch weeks). Late-evening quotes after 22:00 reflect US after-hours trading (inference).
- **ADRs and German secondary listings:** an *ADR* (American Depositary Receipt) is a US-traded certificate for a non-US company's shares. Many US shares also have a secondary quotation on German exchanges in EUR (unverified for each stock). Check the ISIN and the venue in the app.
- **ETFs:** US-domiciled ETFs and mutual funds (e.g. SPY, QQQ) are generally not sold to EU retail clients because under the PRIIPs Regulation the product manufacturer must prepare a key information document (KID) and the seller must hand it to retail investors before the transaction [34]. US issuers generally do not publish an EU-style KID (inference; EU brokers therefore block these products). Their EU-domiciled equivalents are *UCITS* ETFs (EU retail fund standard). Example categories, not recommendations; availability and costs must be checked in the app:
  - S&P 500: iShares Core S&P 500 UCITS ETF (IE00B5BMR087, accumulating, 0.07% TER, 503 holdings) [3]; Vanguard S&P 500 UCITS ETF (IE00B3XXRP09, distributing, 0.07%) [4].
  - Nasdaq-100: iShares Nasdaq 100 UCITS ETF (IE00B53SZB19, accumulating, 0.30%) [5].
  - Small caps (Russell 2000) and Dow Jones: UCITS ETFs exist in these categories (unverified; no ISIN checked).

## 8. Taxes specific to this market

- **US withholding tax (WHT):** US-source dividends paid to foreign persons are withheld at 30% by default or at a lower treaty rate [27][28][29]. Form W-8BEN is the certificate of foreign status the payer collects to apply a reduced treaty rate; it is generally valid until the end of the third calendar year after signing [27][28].
- **Treaty rate Germany-USA:** Article 10 caps WHT on dividends at 15% for portfolio investors (5% for companies holding at least 10% of votes; 0% for certain 80% parents) [30]. A private investor gets the 15% rate.
- **At Trade Republic:** Trade Republic Bank GmbH is a Qualified Intermediary with the US tax authorities, so US dividends are reduced at source to 15% instead of 30% [17]. The help article does not mention an individual W-8BEN step; check whether any form is needed (open question).
- **German side:** investment income is taxed at 25% flat (*Abgeltungsteuer*, plus solidarity surcharge and church tax where applicable) [31]. Foreign tax can be credited, capped at 25% of the individual income item and at the German tax due on it [31]; the treaty-limited 15% is the creditable amount [33]. Mechanism: US 15% credited against German 25% leaves roughly 10 percentage points (before surcharges and allowance) to pay in Germany. For details see [Germany](germany.md).
- **If more than 15% was withheld** (for example 30% because no valid certificate was on file): the excess 15 points is not creditable in Germany; it must be reclaimed from the US side. The BZSt forms page points to the IRS Form W-8BEN page for US refund applications and states it no longer provides forms itself [32]. The exact refund route (e.g. a US return for non-residents) was not verified (unverified).
- **UCITS ETFs:** US dividends are taxed at fund level; the investor-level German taxation of funds is covered in [Trading basics](../01-trading-basics.md#funds-and-etfs). The treaty rate achieved by Irish funds is a fund-level fact (unverified).
- **Not covered/unverified:** US capital-gains rules for non-residents, US estate tax on US-situated assets of non-residents, and Trade Republic's FX handling.

## 9. Useful official data sources

- SEC EDGAR: https://www.sec.gov/edgar/search/ [24]
- NYSE hours and calendar: https://www.nyse.com/markets/hours-calendars [9]
- Nasdaq-100 index page: https://indexes.nasdaqomx.com/Index/Overview/NDX [6]
- S&P Dow Jones Indices: https://www.spglobal.com/spdji/ (factsheets; blocked for automated fetch)
- FTSE Russell: https://www.lseg.com/en/ftse-russell/indices/russell-us [7]
- FINRA: https://www.finra.org [23]
- Cboe: https://www.cboe.com [35]
- BZSt (creditable foreign withholding tax list per year): https://www.bzst.de [33]
- Trade Republic help centre: https://support.traderepublic.com [15]

## Sources

1. WFE, "New WFE data: public markets post strong growth in 2025 despite geopolitical instability", World Federation of Exchanges, https://www.world-exchanges.org/news/articles/new-wfe-data-public-markets-post-strong-growth-2025-despite-geopolitical-instability, accessed 2026-10-17.
2. NYSE Listings, Intercontinental Exchange, https://www.nyse.com/listings, accessed 2026-10-17.
3. iShares Core S&P 500 UCITS ETF USD (Acc), IE00B5BMR087, justETF, https://www.justetf.com/en/etf-profile.html?isin=IE00B5BMR087, accessed 2026-10-17.
4. Vanguard S&P 500 UCITS ETF (USD) Distributing, IE00B3XXRP09, justETF, https://www.justetf.com/en/etf-profile.html?isin=IE00B3XXRP09, accessed 2026-10-17.
5. iShares Nasdaq 100 UCITS ETF (Acc), IE00B53SZB19, justETF, https://www.justetf.com/en/etf-profile.html?isin=IE00B53SZB19, accessed 2026-10-17.
6. NASDAQ-100 Index (NDX) overview, Nasdaq Global Indexes, https://indexes.nasdaqomx.com/Index/Overview/NDX, accessed 2026-10-17.
7. Russell US Indexes, FTSE Russell (LSEG), https://www.lseg.com/en/ftse-russell/indices/russell-us, accessed 2026-10-17.
8. Russell 2000 Reg 871 Factsheet (v1.4, constituent count taken from a search-result extract, PDF not machine-readable), FTSE Russell, https://www.lseg.com/content/dam/ftse-russell/en_us/documents/policy-documents/russell-2000-reg-871-factsheet.pdf, accessed 2026-10-17.
9. NYSE Hours and Calendars, Intercontinental Exchange, https://www.nyse.com/markets/hours-calendars, accessed 2026-10-17.
10. "SEC Adopts Rules to Shorten Securities Transaction Settlement Cycle" (2023-29), U.S. SEC, https://www.sec.gov/newsroom/press-releases/2023-29, accessed 2026-10-17.
11. "Investor Bulletin: Measures to Address Market Volatility (circuit breakers)", U.S. SEC, https://www.sec.gov/investor/alerts/circuitbreakersbulletin.htm, accessed 2026-10-17.
12. "Guardrails for market volatility (LULD and circuit breakers)", FINRA, https://www.finra.org/investors/insights/guardrails-market-volatility, accessed 2026-10-17.
13. 15 U.S.C. § 260a (daylight saving time), Cornell Legal Information Institute, https://www.law.cornell.edu/uscode/text/15/260a, accessed 2026-10-17.
14. Directive 2000/84/EC on summer-time arrangements, EUR-Lex (rule text taken from a search extract; page body not retrieved), https://eur-lex.europa.eu/eli/dir/2000/84/oj/eng, accessed 2026-10-17.
15. "When are the trading hours?", Trade Republic help centre, https://support.traderepublic.com/en-sk/759, accessed 2026-10-17.
16. "On which trading market will my orders be executed?", Trade Republic help centre, https://support.traderepublic.com/en-de/39-On-which-trading-market-will-my-orders-be-executed, accessed 2026-10-17.
17. "Dividend payout from US companies - advance reduction", Trade Republic help centre, https://support.traderepublic.com/en-pt/1077-Dividenden-Auszahlung-von-US-Unternehmen-_-Vorab_Reduzierung, accessed 2026-10-17.
18. M. Raffard, "Trade Republic lance Best Price et Direct Price" (20 July 2026, sponsored article), Café de la Bourse, https://www.cafedelabourse.com/evenements-partenariats/trade-republic-best-price-direct-price; also Teleborsa, 2 July 2026, https://www.teleborsa.it/AMP/News/2026/07/02/trade-republic-lancia-il-best-price-sugli-ordini-dopo-ban-a-pfof-e-un-web-terminal-avanzato-15.html; accessed 2026-10-17.
19. "24-Hour Trading: Nasdaq's FAQs and SEC's Roundtable" (updated 2026-07-29), Cooley, https://governancebeat.cooley.com/24-hour-trading-nasdaqs-faqs-and-secs-roundtable/, accessed 2026-10-17.
20. "SEC Proposes Optional Semiannual Reporting" (2026-05-08), Deloitte DART, https://dart.deloitte.com/USDART/home/publications/deloitte/heads-up/2026/sec-proposes-semi-annual-reporting, accessed 2026-10-17.
21. "Frequently Asked Questions About Form 13F", U.S. SEC, https://www.sec.gov/divisions/investment/13ffaq, accessed 2026-10-17.
22. "What We Do", U.S. SEC, https://www.sec.gov/about/what-we-do, accessed 2026-10-17.
23. "About FINRA", FINRA, https://www.finra.org/about, accessed 2026-10-17.
24. EDGAR full-text search, U.S. SEC, https://www.sec.gov/edgar/search/, accessed 2026-10-17.
25. "Officers, Directors and 10% Shareholders" (Section 16, Forms 3/4/5; two-business-day rule taken from a search extract), U.S. SEC, https://www.sec.gov/resources-small-businesses/going-public/officers-directors-10-shareholders, accessed 2026-10-17.
26. Form 10-Q fast answer and "Revisions to Accelerated Filer Definition" (filing deadlines; taken from search extracts), U.S. SEC, https://www.sec.gov/fast-answers/answersform10qhtm.html and https://www.sec.gov/files/rules/final/33-8644.pdf, accessed 2026-10-17.
27. "About Form W-8 BEN", IRS, https://www.irs.gov/forms-pubs/about-form-w-8-ben, accessed 2026-10-17.
28. Instructions for Form W-8BEN, IRS, https://www.irs.gov/instructions/iw8ben, accessed 2026-10-17.
29. "Federal Income Tax Withholding and Reporting on Other Kinds of U.S. Source Income Paid to Nonresident Aliens", IRS, https://www.irs.gov/individuals/international-taxpayers/federal-income-tax-withholding-and-reporting-on-other-kinds-of-us-source-income-paid-to-nonresident-aliens, accessed 2026-10-17.
30. Senate Executive Report 110-5 (Protocol amending the Germany-US tax convention, Article 10), U.S. Senate via govinfo, https://www.govinfo.gov/content/pkg/CRPT-110erpt5/html/CRPT-110erpt5.htm, accessed 2026-10-17.
31. § 32d EStG, Bundesministerium der Justiz, https://www.gesetze-im-internet.de/estg/__32d.html, accessed 2026-10-17.
32. "Ausländische Formulare", Bundeszentralamt für Steuern, https://www.bzst.de/DE/Service/SteuerlichesInfocenter/Ausl_Formulare/auslaendische_formulare.html, accessed 2026-10-17.
33. "Ausländische Quellensteuer" and yearly list "Anrechenbare ausländische Quellensteuer" (USA row not read: PDF unreadable), Bundeszentralamt für Steuern, https://www.bzst.de/DE/Service/SteuerlichesInfocenter/AuslaendischeQuellensteuer/auslaendischequellensteuer_node.html, accessed 2026-10-17.
34. Regulation (EU) No 1286/2014 (PRIIPs), Articles 5 and 13, EUR-Lex, https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R1286, accessed 2026-10-17.
35. About Cboe Global Markets, Cboe, https://www.cboe.com/about/, accessed 2026-10-17.
36. About SIPC, Securities Investor Protection Corporation, https://www.sipc.org/about-sipc, accessed 2026-10-17.
37. Schwab ETF/factsheet page quoting S&P 500 sector weights as of 2026-07-24 (search extract, secondary), Schwab, https://international.schwab.com/node/14346, accessed 2026-10-17.
38. Trade Republic fuehrt Aenderungen ein (dated 03.07.2026), Stiftung Warentest (test.de), https://www.test.de/trade-republic-handelssystem-gebuehr-aenderung-6320863-0/, accessed 2026-10-17.
