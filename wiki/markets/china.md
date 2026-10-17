# China stock market

_Last checked: 2026-10-17 · Educational content, not investment advice._

Scope: mainland China (Shanghai, Shenzhen, Beijing) and Hong Kong. Both are covered on one page because most foreign investors reach Chinese companies through Hong Kong. See also: [Trading basics](../01-trading-basics.md), [Markets overview](README.md), [Germany](germany.md), [Europe](europe.md), [USA](usa.md), [Indonesia](indonesia.md), [Strategy](../strategy.md), [APIs](../apis.md).

## 1. Overview

- **Hong Kong (HKEX):** 2,772 listed companies and a market capitalisation of HK$45,480.4 billion at 30 Sep 2026 (about US$5.8 trillion at the HK$7.8 peg, own calculation) [1]. Mainland enterprises make up 77.3% of HKEX market cap and 88.8% of equity turnover, and 536 companies are H-shares [1]. So "Hong Kong" is largely a mainland-China market.
- **Shanghai (SSE):** 2,310 listed A-share companies and RMB 67.21 trillion market cap at 31 Jul 2026; of these the STAR Market has 612 companies and RMB 15.77 trillion [2].
- **Shenzhen (SZSE):** roughly 2,880 listings and about RMB 50 trillion (both unverified, third-party encyclopaedia figures from Feb and May 2026) [3]. ChiNext reported about 1,400 companies in May 2026 (unverified) [3]. The SZSE page I could open gave only 2020 figures [4].
- **Beijing (BSE):** 339 companies and about RMB 840 billion at its fifth anniversary (2 Sep 2026); trading started 15 Nov 2021 [5]. It focuses on small and mid-sized firms.
- **Role:** Shanghai, Shenzhen and Hong Kong are among the world's largest exchanges. I could not retrieve the World Federation of Exchanges ranking, so no rank is claimed here; the WFE statistics portal is the place to check [6].

Share classes and terms:

| Term | Meaning |
|---|---|
| *A-shares* | Yuan (CNY) shares of mainland companies on SSE, SZSE or BSE. The SSE quotes them in RMB with a 0.01 tick [7]. Reserved mainly for domestic investors and approved foreign channels. |
| *B-shares* | Foreign-currency shares on SSE (USD, tick USD 0.001) [7] and SZSE (HKD). A small legacy segment. |
| *H-shares* | Mainland-incorporated companies listed in Hong Kong, priced in HKD. |
| *Red chips* | Hong Kong-listed companies incorporated outside the mainland (for example Hong Kong, Cayman) and controlled by mainland state entities. Definition from general market usage (unverified in the sources fetched). |
| *P chips* | Same idea, but controlled by private mainland owners (general usage, unverified). |
| *ADRs* | US-listed depositary receipts of Chinese companies. Exposure is to the same company but under US rules (see risks). |
| *D-shares* | Chinese shares listed in Frankfurt (CEINEX); the German finance ministry letter mentions them for tax purposes [8]. |

## 2. Exchanges and main indices

| Index | Members | What it measures | Top sectors / notes |
|---|---|---|---|
| SSE Composite (000001) | All eligible Shanghai-listed shares (count not verified) | Cap-weighted broad Shanghai benchmark; base 100 on 19 Dec 1990 [9]. Closed 3,832.26 on 31 Jul 2026, -3.44% YTD [2] | Banks and heavy industry historically (unverified) |
| CSI 300 | 300 [10] | Large, liquid A-shares from Shanghai and Shenzhen (description from general knowledge; unverified) | As of 27 Aug 2026: technology 30.1%, finance 19.6%, industrials 18.0%, materials 10.1%; top holding CATL 4.0% [10] |
| Hang Seng Index (HSI) | 90 after Mar 2026 review [11]; 93 after the Jun 2026 review per a secondary report (unverified) [12]; 95 after Sep 2026 (unverified) | Large Hong Kong-listed companies | Technology, finance, consumer (unverified) |
| Hang Seng China Enterprises (HSCEI) | 80 (Aug 2026 review notice) [13] | Mainland enterprises listed in Hong Kong; originally H-shares, methodology since broadened (check factsheet) | Finance, technology, consumer (unverified) |
| Hang Seng TECH | 30 [14] | 30 largest Hong Kong-listed tech companies, reviewed quarterly; single-name cap 8% [14] | Internet, platform, hardware |
| MSCI China | 577 (31 Aug 2026) [15] | Large and mid caps across China share classes, including US-listed ADRs | Top 10 = 41.4%; Tencent 13.9%, Alibaba 9.6% [15] |

Hang Seng and MSCI weights differ by date and share class; always read the current factsheet.

## 3. Trading hours, limits and settlement

All Chinese markets use UTC+8 and have **no daylight saving time**. Germany is UTC+1 (CET) in winter and UTC+2 (CEST) in summer, so the gap is 7 hours in winter and 6 hours in summer. In 2026 CEST ends on Sun 25 Oct, and in 2027 it starts on Sun 28 Mar (own calculation). There are therefore no "mismatch weeks" against China, but the clock shift moves every session by one hour in German time. For US-listed ADRs, the US and EU change clocks on different dates, which creates short mismatch periods; check the exchange's calendar [see US page](usa.md).

| Session | Local time (CST/HKT) | German time, winter (CET) | German time, summer (CEST) |
|---|---|---|---|
| SSE/SZSE opening call auction | 09:15-09:25 | 02:15-02:25 | 03:15-03:25 |
| SSE continuous, morning | 09:30-11:30 | 02:30-04:30 | 03:30-05:30 |
| Lunch break (mainland) | 11:30-13:00 | 04:30-06:00 | 05:30-07:00 |
| SSE continuous, afternoon + closing auction | 13:00-14:57 and 14:57-15:00 | 06:00-08:00 | 07:00-09:00 |
| HKEX pre-opening auction | 09:00-09:30 | 02:00-02:30 | 03:00-03:30 |
| HKEX continuous trading | 09:30-12:00 and 13:00-16:00 | 02:30-05:00 and 06:00-09:00 | 03:30-06:00 and 07:00-10:00 |
| HKEX lunch break | 12:00-13:00 | 05:00-06:00 | 06:00-07:00 |
| HKEX closing auction (random end 16:08-16:10) | 16:00-16:10 | 09:00-09:10 | 10:00-10:10 |

- Mainland hours: SSE main board and STAR share the same sessions; STAR also has an after-hours fixed-price session at 15:05-15:30 [16]. SZSE hours are not verified here; they are generally the same as SSE (unverified).
- **Lunch break:** both the mainland (11:30-13:00) and Hong Kong (12:00-13:00) pause trading at lunch. HKEX's "Extended Morning Session" applies only to a few designated securities [41]. HKEX was studying ending the lunch break in July 2026, but no date was set [40].
- **Holidays:** SSE publishes yearly closures (for example Spring Festival and 1-8 Oct National Day weeks) [16]. HKEX publishes its own calendar; Hong Kong is closed on 19 Oct 2026 and reopens on 20 Oct [17]. Mainland and Hong Kong calendars differ, and Stock Connect trades only when both sides are open.
- **Price limits, mainland:** main board +/-10%; "risk-warning" (ST) stocks +/-5%; STAR +/-20%, with no limit for the first five trading days after IPO [7]. ChiNext +/-20% and BSE +/-30% are widely reported but I could not verify them in official pages (unverified).
- **Hong Kong:** no daily limit. A *volatility control mechanism* (VCM) triggers a 5-minute cooling-off period when the price moves 5% to 50% (threshold depends on the stock) from the price five minutes earlier; the closing auction applies a +/-5% band [18].
- **A-share T+1:** shares bought today can only be sold the next trading day (secondary source [19]; not stated on the SSE pages I fetched; unverified). Stock Connect Northbound also prohibits day trading [20].
- **Settlement:** not verified for mainland A-shares beyond T+1 for securities (unverified) [19]. HKEX's menu lists a "T+1 Settlement for the Hong Kong Cash Market" section [18]; the cycle used today (T+2 historically) must be confirmed on HKEX.
- **Lot sizes:** main board A-shares trade in multiples of 100; STAR orders are 200 to 100,000 shares (limit orders) [7]. Hong Kong board lots differ per stock.
- Trade Republic customers do not trade on these venues directly; see section 7.

## 4. Currency and FX risk for a euro investor

- **CNY vs CNH:** *CNY* is the onshore yuan and *CNH* the offshore yuan traded mainly in Hong Kong; they can diverge and capital controls separate the two (general knowledge, unverified). Mainland A-shares are priced in CNY; B-shares in USD or HKD.
- **HKD peg:** the Linked Exchange Rate System keeps HKD within HK$7.75-7.85 per US dollar and has done so since 17 Oct 1983 [21]. A euro investor in Hong Kong shares therefore carries EUR/USD risk, not a separate HKD risk.
- On Trade Republic, quotes are in EUR, so currency conversion is built into the price and spread (see section 7). Moves in the dollar (and, for A-shares, the yuan) against the euro act as an extra return driver or drag on top of the share price.

## 5. Regulator, investor protection and disclosure

- **Mainland:** the *China Securities Regulatory Commission* (CSRC) supervises securities markets; QFII and RQFII were merged by CSRC, PBOC and SAFE rules effective 1 Nov 2020 [22]. I could not open the CSRC English site, so its mandate here is general knowledge (unverified).
- **Hong Kong:** the *Securities and Futures Commission* (SFC) is an independent statutory body set up in 1989 under the Securities and Futures Ordinance. It licenses intermediaries, authorises retail products and oversees the exchange's listing regulation [23].
- **Disclosure:** mainland companies file via the exchanges and *CNINFO* (Juchao), operated by an SZSE subsidiary; the site is almost entirely in Chinese [24]. Hong Kong filings are on *HKEXnews* (listed company information, CCASS shareholding, disclosure of interests) [25].
- **Investor protection for you:** you are protected as a client of your German broker, not as a Chinese-market investor. Mainland and Hong Kong investor compensation schemes were not researched and should not be assumed to apply.

## 6. Market characteristics and risks

- **Retail-driven mainland market:** A-shares have a large retail base and tight price limits (section 3). A limit-hit stock can stay stuck for days; at +/-10% a stock can lose 10% per day.
- **Concentration:** MSCI China has 41.4% in 10 stocks and 13.9% in Tencent alone [15]. CSI 300 is tilted to technology and finance [10]. Sector mix shifts quickly, as the 2026 CSI 300 top names (CATL, optical-component makers) differ from earlier years.
- **Foreign access limits:** foreigners reach A-shares only through Stock Connect (Northbound) or licensed institutions (QFII/RQFII). Northbound STAR and ChiNext shares are open to institutional professional investors only; mainland retail investors can access Hong Kong only with at least RMB 500,000 in assets (Southbound) [20]. Northbound average daily turnover was RMB 256.4 billion in Sep 2026 [1]. Stock Connect also has daily quotas, a short-selling ban on naked shorts and ownership caps (10% single, 30% aggregate foreign holding is general knowledge, unverified).
- **VIE structures:** many Chinese internet firms are listed through offshore holding companies with contractual control (*variable interest entities*) because foreign ownership is restricted in some sectors. You own the offshore shell, not the operating company, so legality and enforceability are a risk (general knowledge; no primary source retrieved, see Open questions).
- **US delisting risk (HFCAA):** the Holding Foreign Companies Accountable Act can force trading bans on US-listed issuers if the US audit oversight board cannot inspect their auditors for consecutive years. On 15 Dec 2022 the PCAOB said it had complete access in mainland China and Hong Kong and vacated its earlier findings; it reassesses each year [26]. I did not verify determinations after 2023.
- **Regulatory crackdowns:** the 2021 measures against internet platforms and private education caused sharp declines (general knowledge; not sourced in this pass). Treat policy shifts as a recurring factor.
- **State influence and capital controls:** the state shapes sector policy and owns large listed groups (red chips, banks). Cash movements out of the mainland are controlled (general knowledge, unverified).
- **Information and governance:** English-language disclosure is limited on the mainland [24].

## 7. Access from Germany via Trade Republic

- **Single shares:** Trade Republic's help pages give different counts (more than 6,500 international stocks; up to about 7,500 stocks in total); check the app. The help page lists stocks from Europe, North America and Asia and states that the assets are on its partner Lang & Schwarz Exchange (LSX) (help-centre text that may predate the July 2026 change) [27]. The page does not name Hong Kong, China or ADRs. Third-party reviews claim Hong Kong shares are available, and one price feed shows a Hong Kong stock quoted in EUR on LSX on 16 Oct 2026, but I could not confirm which Chinese or Hong Kong names Trade Republic offers (unverified). Mainland A-shares: no evidence of availability, and Stock Connect is not offered to retail clients through the app (unverified).
- **Venues:** a Trade Republic notice of January 2026 lists Lang & Schwarz Exchange, Lang & Schwarz Tradecenter, Trade Republic Bank and Tradegate Exchange as venues (help-centre text that may predate the July 2026 change) [28]. One secondary report says ETF execution moved away from LSX in July 2026; the answer depends on current Trade Republic documents.
- **UCITS ETF categories (examples, not recommendations; check availability in the app, since Trade Republic says not every LSX-listed ETF is tradable with it [29]):**
  - *Broad China, MSCI China:* iShares MSCI China UCITS ETF (IE00BJ5JPG56), TER 0.28%, 577 holdings (31 Aug 2026) [15].
  - *Mainland A-shares, CSI 300:* Xtrackers CSI 300 Swap UCITS ETF 1C (LU0779800910), TER 0.50%, synthetic swap-based, EUR 1,727 m [10].
  - *Hong Kong tech, Hang Seng TECH:* HSBC Hang Seng TECH UCITS ETF (IE00BMWXKN31), TER 0.50%, 30 holdings, EUR 946 m [14].
  - An ETF on the Hang Seng Index itself is not widely offered as a UCITS product (secondary claim, unverified).
- **ADRs:** US-listed ADRs of Chinese firms (for example Alibaba or PDD) trade in the US and can also be quoted in Europe. ADR availability and which share class you hold (ADR, H-share or A-share) differ by name. Check the ISIN in the app.
- **Secondary listings:** a few Chinese firms have German listings (D-shares, for example Haier Smart Home, discussed in section 8). Liquidity can be thin.

## 8. Taxes specific to this market

Not tax advice; confirm with a tax adviser or the BZSt.

| Item | Rate / rule |
|---|---|
| China dividend WHT, H-shares and non-resident enterprises | 10% (Circular 897 for companies; Notice 348 for individuals) [30] |
| China dividend WHT, A-shares through Stock Connect | 10%, withheld by the listed company [31]; treaty-rate refunds possible if lower |
| China WHT, A-shares held directly (German finance ministry summary) | 20%, halved to an effective 10% if held 1 month to 1 year, nil after 1 year; B-shares nil [8] |
| Hong Kong dividend WHT | None under domestic law; Germany is not in Hong Kong's list of comprehensive tax treaties (only a 2003 shipping-income agreement) [32][33] |
| Germany-China treaty (signed 28 Mar 2014) | 10% general; 5% for a company holding at least 25% directly; 15% for real-estate-linked dividends [34][35]; the treaty does not cover Hong Kong [36] |

- **Application date:** the treaty entered into force on 6 April 2016 (BGBl. 2016 II p. 1005) and applies from 1 January 2017 [42].
- **Credit in Germany:** private investors pay 25% flat tax plus the solidarity surcharge (church tax extra) [37]. Chinese tax is creditable up to the treaty cap of 10% under Art. 10(2)(c) [8][38]. By BMF letter of 31 Mar 2022 (BStBl I 2022 p. 328), the bank may credit up to 10% in the withholding procedure for private H-share holders [8]. For mainland A-shares, crediting happens in the assessment procedure, not at the bank [8].
- **Illustration (own calculation, per EUR 100 dividend, ignoring allowance and church tax):** China withholds 10.00; Germany charges 25% = 25.00 less 10.00 credit = 15.00, plus 5.5% soli on 15.00 = 0.83. Total about 25.83 versus 26.38 for a dividend with no foreign tax.
- **Excess over the treaty rate:** anything withheld above 10% (for example 20% on A-shares) is not creditable in Germany; the relief decision lies with China, so you must apply there for a refund [38]. No uniform form or deadline is known to me; first ask the broker for the paying agent and legal basis.
- **ADRs:** the rate depends on the issuer's country of tax residence, not on the US listing (unverified); the broker's tax statement is the working document.
- **Capital gains:** gains are German capital income (25% flat). Northbound gains were temporarily exempt from Chinese tax; current status not confirmed [39].

## 9. Useful official data sources

- HKEX monthly highlights and statistics [1]; HKEXnews filings [25]; HKEX Stock Connect pages and Investor Book [20].
- SSE: english.sse.com.cn (market statistics, trading rules, calendar) [2][3][16]; SZSE: szse.cn [4]; CNINFO [24].
- SFC: sfc.hk [23]; CSRC: csrc.gov.cn (not opened in this pass).
- Index providers: Hang Seng Indexes (hsi.com.hk), China Securities Index Co. (csindex.com.cn), MSCI (msci.com): JavaScript pages that I could not read; use their factsheets.
- Tax: BZSt foreign withholding tax tables (2026 edition) [38]; BMF letter of 31 Mar 2022 [8].

## Sources

1. HKEX Monthly Market Highlights (Sep 2026), HKEX, https://www.hkex.com.hk/market-data/statistics/consolidated-reports/hkex-monthly-market-highlights?sc_lang=en, accessed 2026-10-17.
2. Shanghai Stock Exchange Newsletter, July 2026, SSE, https://english.sse.com.cn/news/publications/newsletter/c/10827993/files/a3a75e0b15654ce7a030a6ea803fb916.html, accessed 2026-10-17.
3. Shenzhen Stock Exchange (listing count and market cap as of Feb and May 2026; ChiNext count as of 14 May 2026), Wikipedia and a ChiNext commentary (both third-party, unverified), https://en.wikipedia.org/wiki/Shenzhen_Stock_Exchange, accessed 2026-10-17.
4. SZSE ChiNext product page, Shenzhen Stock Exchange, https://www.szse.cn/www/English/products/equity/ChiNext/, accessed 2026-10-17.
5. Five years on, Beijing Stock Exchange fuels China's hard-tech push, CGTN, 2 Sep 2026, https://news.cgtn.com/news/2026-09-02/Five-years-on-Beijing-Stock-Exchange-fuels-China-s-hard-tech-push-1Q726jmmdSE/p.html, accessed 2026-10-17.
6. WFE statistics page, World Federation of Exchanges, https://www.world-exchanges.org/our-work/statistics, accessed 2026-10-17.
7. Stock Trading Mechanism, Shanghai Stock Exchange, https://english.sse.com.cn/start/trading/mechanism/, accessed 2026-10-17.
8. BMF letter 31 Mar 2022 on crediting Chinese withholding tax (§ 43a Abs. 3 EStG), summary by Verlag Dr. Otto Schmidt, https://www.otto-schmidt.de/news/steuerrecht/anrechnung-von-quellensteuer-die-auf-ausschuttungen-von-chinesischen-aktien-erhoben-wird-auf-die-deutsche-kapitalertragsteuer-nach-43a-absatz-3-estg-2022-04-07.html, accessed 2026-10-17.
9. Methodology of SSE Composite Index, SSE, http://english.sse.com.cn/indices/indices/list/indexmethods/c/000001_000001hbooken_EN.pdf, accessed 2026-10-17 (from a search extract).
10. Xtrackers CSI 300 Swap UCITS ETF 1C profile, justETF, https://www.justetf.com/en/etf-profile.html?isin=LU0779800910, accessed 2026-10-17.
11. Hang Seng Index quarterly review, Feb 2026, HKEX, https://www.hkex.com.hk/-/media/HKEX_Common/Market/Indices/SCCEA/Documents/20260213_EN_review_result.pdf, accessed 2026-10-17 (from a search extract).
12. Hang Seng Indexes review of May 2026, Caproasia, https://www.caproasia.com/2026/05/26/hang-seng-indexes-company-index-review-1-hang-seng-index-hsi-to-add-3-constituents-to-total-93-from-90-add-10-billion-jt-global-express-27-billion-aluminum-corp-of-china-38-billion-beone/, accessed 2026-10-17.
13. Index review result, Aug 2026, HKEX, https://www.hkex.com.hk/-/media/HKEX_Common/Market/Indices/SCCEA/Documents/20260821_EN_review_result.pdf, accessed 2026-10-17 (PDF not readable; count from a search extract).
14. HSBC Hang Seng TECH UCITS ETF profile, justETF, https://www.justetf.com/en/etf-profile.html?isin=IE00BMWXKN31, accessed 2026-10-17; and HKEX HSTECH info sheet, https://www.HKEX.com.hk/-/media/HKEX-Market/Products/Listed-Derivatives/Equity-Index/HSTECH/HKEX_infosheet_HSTECH_202211_EN_1125.pdf, accessed 2026-10-17 (search extract).
15. iShares MSCI China UCITS ETF profile, justETF, https://www.justetf.com/en/etf-profile.html?isin=IE00BJ5JPG56, accessed 2026-10-17.
16. Trading hours and calendar, Shanghai Stock Exchange, https://english.sse.com.cn/start/trading/schedule/, accessed 2026-10-17.
17. Securities Market trading hours (English and Traditional Chinese versions), HKEX, https://www.hkex.com.hk/Services/Trading-hours-and-Severe-Weather-Arrangements/Trading-Hours/Securities-Market?sc_lang=en, accessed 2026-10-17.
18. Securities trading mechanism, HKEX, https://www.hkex.com.hk/Services/Trading/Securities/Overview/Trading-Mechanism?sc_lang=en, accessed 2026-10-17.
19. A-share trading rules (T+1), Tiger Brokers help centre (broker secondary source), https://www-web.itiger.com/hk/en/help/detail/37048941, accessed 2026-10-17 (search extract).
20. Stock Connect Information Book for Investors and FAQ (6 Jul 2026), HKEX, https://www.hkex.com.hk/-/media/HKEX-Market/Mutual-Market/Stock-Connect/Getting-Started/Information-Booklet-and-FAQ/Information-Book-for-Investors/Investor_Book_En.pdf, accessed 2026-10-17 (PDF not readable; rules read from a search extract).
21. Linked Exchange Rate System, Hong Kong Monetary Authority, https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/, accessed 2026-10-17.
22. China releases new QFII and RQFII rules, Haynes Boone, https://www.haynesboone.com/news/alerts/china-releases-new-qfii-and-rqfii-rules, accessed 2026-10-17 (search extract).
23. Our role, Securities and Futures Commission, https://www.sfc.hk/en/About-the-SFC/Our-role, accessed 2026-10-17.
24. CNINFO home page, Shenzhen Securities Information Co., http://www.cninfo.com.cn/new/index, accessed 2026-10-17.
25. HKEXnews home page, HKEX, https://www.hkexnews.hk/index.htm, accessed 2026-10-17.
26. PCAOB Secures Complete Inspection Access to Audits of Chinese Companies, Orrick, Dec 2022, https://www.orrick.com/en/Insights/2022/12/PCAOB-Secures-Complete-Inspection-Access-to-Audits-of-Chinese-Companies-Removing-Delisting-Risks, accessed 2026-10-17.
27. Which stocks can I trade at Trade Republic?, Trade Republic help centre, https://support.traderepublic.com/en-de/758-Which-stocks-can-I-trade-at-Trade-Republic, accessed 2026-10-17.
28. Information for trading via the Trade Republic App on the exchanges (Jan 2026), Trade Republic, https://assets.traderepublic.com/documents/NL/EXCHANGES_INFO_20260127163726.pdf, accessed 2026-10-17 (only title and venue names read via search extract).
29. Which ETFs can I trade at Trade Republic?, Trade Republic help centre, https://support.traderepublic.com/en-sk/1429-Which-ETFs-can-I-trade-at-Trade-Republic, accessed 2026-10-17.
30. HK-listed company filings describing SAT Circular 897 and Notice 348, HKEXnews, https://www1.hkexnews.hk/app/sehk/2026/108526/a132765/sehk26051000262.pdf, accessed 2026-10-17 (search extract; primary SAT texts not retrieved).
31. HKEXnews filing on Stock Connect tax treatment (Caishui [2014] 81, [2016] 127), https://www1.hkexnews.hk/app/sehk/2026/108513/a133925/sehk26061101582.pdf, accessed 2026-10-17 (search extract).
32. Comprehensive double taxation agreements, Hong Kong Inland Revenue Department, https://www.ird.gov.hk/eng/tax/dta_inc.htm, accessed 2026-10-17.
33. Germany shipping-income agreement, Hong Kong Inland Revenue Department, https://www.ird.gov.hk/eng/pdf/dt_germany_sh.pdf, accessed 2026-10-17 (search extract).
34. Comparison between old and new Sino-German Tax Treaties, Ecovis, https://www.ecovis.com/focus-china/?p=3793, accessed 2026-10-17.
35. New tax treaty between China and Germany, Forvis Mazars, https://www.forvismazars.com/hk/en/insights/our-publications/tax-publications/china-tax-newsletters/new-tax-treaty-between-china-and-germany, accessed 2026-10-17.
36. Equities - Double Taxation Treaties concluded by Germany, Clearstream, https://clearstream.com/clearstream-en/res-library/market-coverage/equities-double-taxation-treaties-concluded-by-germany-and-currently-in-force-cbf--1312904, accessed 2026-10-17 (search extract).
37. Ausländische Quellensteuer, Bundeszentralamt für Steuern, https://www.bzst.de/DE/Service/SteuerlichesInfocenter/AuslaendischeQuellensteuer/auslaendischequellensteuer_node.html, accessed 2026-10-17 (search extract).
38. Anrechenbare ausländische Quellensteuer, Stand 1 Jan 2026, BZSt, https://www.bzst.de/SharedDocs/Downloads/DE/EU_OECD/anrechenbare_ausl_quellensteuer_2026.pdf?__blob=publicationFile&v=1, accessed 2026-10-17 (PDF not readable; China 10% row read from a search extract).
39. Shanghai-Hong Kong Stock Connect Programme, Forvis Mazars, Nov 2014, https://www.forvismazars.com/hk/en/insights/our-publications/tax-publications/hong-kong-tax-newsletters/shanghai-hong-kong-stock-connect-programme, accessed 2026-10-17 (search extract).
40. The Standard (Hong Kong), 20 Jul 2026 (HKEX study on ending the lunch break), https://www.thestandard.com.hk/finance/article/337681, accessed 2026-10-17.
41. HKEX receives approval to extend its trading hours from 7 March 2011 (HKEX notice), Mondovisione, https://www.mondovisione.com/news/hkex-receives-approval-to-extend-its-trading-hours-from-7-march-2011125/, accessed 2026-10-17.
42. DBA China-Deutschland: Abkommen unterzeichnet, Deloitte Tax News, https://www.deloitte-tax-news.de/steuern/internationales-steuerrecht/dba-china-deutschland-abkommen-unterzeichnet.html, accessed 2026-10-17.
