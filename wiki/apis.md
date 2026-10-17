# Public APIs for market data and insider filings

_Last checked: 2026-10-17 · Free tiers and terms change often; verify before building on them._

This page lists public, documented data sources you can use for research next to a Trade Republic account: price and fundamentals APIs, official disclosure registers, and what is (not) possible with Trade Republic itself. It is a reference, not investment advice and not legal advice. For the concepts behind the data see [Trading basics](01-trading-basics.md); for the exchanges themselves see [Markets overview](markets/README.md); for how to use signals see [Strategy](strategy.md). Back to the [Index](README.md).

How to read the evidence: figures marked with a citation number come from the provider's or regulator's own page as fetched on 2026-10-17. "(unverified)" means I could not load the official page, only found a secondary source, or the page did not state the number. Several vendor pages blocked automated fetching (HTTP 403), so their free-tier numbers are the least certain part of this page.

**Rules for all sections**

- Never put a Trade Republic PIN, a password, or a broker login into any script, API client or third-party tool.
- Store API keys in environment variables (never in code, never in a Git repository, never in a notebook you share).
- Respect rate limits and terms; a free key is usually "personal, non-commercial use" only.
- Published filings are legal to use. Trading on non-public information is insider trading (see the legal line in the last section).

---

## 1. Market-data APIs (prices, fundamentals, FX)

### 1.1 Quick summary

| Verdict | Providers |
|---|---|
| Good free starting points | Alpha Vantage (25 calls/day), Finnhub (60 calls/min, personal use), Twelve Data (800 credits/day), FMP Basic (250 calls/day), Tiingo (1,000 calls/day), Massive/Polygon (5 calls/min, US EOD), ECB, FRED, Eurostat, OpenFIGI |
| Cheap paid, wide coverage | EODHD (about 20 to 100 EUR/month), Twelve Data Grow/Pro, Marketstack |
| Unofficial, terms risk | yfinance, Stooq CSV, AKShare |
| Dead or changed | IEX Cloud (shut down 2024), Polygon.io (renamed Massive), Nasdaq Data Link WIKI prices (frozen) |
| No free option verified | Indonesia (IDX), Deutsche Börse real-time and tick data |

### 1.2 Comparison table (a): market-data APIs

"Official" means the data owner or a registered data vendor offers it under a licence. Markets: DE = Germany (Xetra/Frankfurt), EU, US, CN = mainland China, HK, ID = Indonesia.

| Provider | Official? | Markets (free tier unless noted) | Data types | Free tier and limits | Auth | Licence / terms note |
|---|---|---|---|---|---|---|
| Alpha Vantage [1][2] | Vendor API | US free; global tickers via suffix (.DEX Xetra, .LON, .SHH, .SHZ seen in docs; HK/ID not confirmed) | EOD, intraday, fundamentals, news, FX, insider and congressional trades | 25 requests/day; paid 75 to 1,200 requests/min, 49.99 to 249.99 USD/month [1] | `apikey` query parameter | Free key is personal use; check Terms of Service for redistribution (unverified, PDF not readable) |
| Finnhub [3][4] | Vendor API | US stocks, FX, crypto free; international mostly paid (unverified) | Quotes, candles, fundamentals, news, insider transactions and sentiment | 60 calls/min, personal use licence [3] | Token (key) | Free plan is "personal use" [3]; which endpoints are free is (unverified) |
| Twelve Data [5][6] | Vendor API | Free: US equities/ETFs, FX, crypto (3 markets). Xetra and Frankfurt EOD from Grow, HK, Shanghai, Shenzhen, Indonesia EOD from Pro [6] | EOD, intraday, real-time (plan dependent), fundamentals | 8 credits/min, 800/day [5] | API key | Commercial use needs business plans [6] |
| Financial Modeling Prep [7] | Vendor API | US on free; UK/CA on Premium; global on Ultimate (unverified) | EOD, fundamentals, ratios, insider and congress trades | Basic: 250 calls/day (unverified; page blocked) | API key | Older pages: free plan personal use only (unverified) |
| Massive (formerly Polygon.io) [9][10] | Vendor API | US only | EOD, minute/second bars, trades, quotes, financials | Free: 5 calls/min, 2 years history, EOD only [9] | API key | Individual and business plans differ (unverified) |
| EODHD [11] | Vendor API | Worldwide EOD (150,000+ tickers); DE, EU, US, CN, HK, ID presumably included (unverified per exchange) | EOD, intraday, fundamentals, live (delayed) | Free: 20 calls/day, 1 year EOD [11]; paid 19.99 to 99.99 EUR/month, 100,000 calls/day | API token | Personal vs commercial licences differ (unverified) |
| Tiingo [12] | Vendor API | US and Chinese stocks, ETFs, funds | EOD, fundamentals (add-on), news | 50 requests/hour, 1,000/day, 500 symbols/month [12] | API token | Free and Power tiers are "internal use only", no sharing [12] |
| Marketstack [13] | Vendor API | 70 exchanges, 30,000+ tickers (per exchange list unverified) | EOD (free), intraday from Basic | 100 requests/month, 1 year, non-commercial [13] | `access_key` parameter | Free is non-commercial only [13] |
| Nasdaq Data Link [14] | Official (Nasdaq) | Mostly US, macro and alternative datasets | Time series, tables | Authenticated: 300 calls/10 s, 50,000/day; free datasets limited (which are free: unverified) [14] | API key | Per-dataset licences. WIKI EOD prices stopped updating in 2018 (third-party report, unverified) |
| Alpaca Market Data [15] | Broker API | US stocks, options, crypto | Historical and real-time bars/quotes/trades | Basic: IEX feed only, 200 historical calls/min, latest 15 minutes only for SIP [15] | Key ID and secret in headers; needs an Alpaca account [15] | Account terms apply; account creation is your decision |
| Stooq [16] | Unofficial-style free site | Poland, global indices, many exchanges (DE, US, HK) | EOD CSV, bulk downloads | Free, but CSV endpoint reportedly now needs a key obtained via captcha (third-party, unverified) [16] | Key from web form (unverified) | No published API terms found; treat as personal use |
| yfinance [17] | Unofficial scraper of Yahoo | Global incl. DE (.DE), HK (.HK), CN (.SS/.SZ), ID (.JK) | EOD, intraday, fundamentals, news, options | No official limits; can be blocked at any time | None | Project says "research and educational purposes", Yahoo API "personal use only" [17] |
| IEX Cloud [18] | Dead | n/a | n/a | Shut down 2024-08-31 (third-party analysis) [18] | n/a | Do not use |
| OpenFIGI [19] | Official (Bloomberg-operated) | All instruments (identifier mapping) | ISIN/ticker to FIGI mapping | Mapping: 25 requests/min and 10 jobs without key; 250 requests/min and 100 jobs with key [19] | `X-OPENFIGI-APIKEY` header, optional | Free and open to the public [19] |
| ECB Data Portal [20][21] | Official (ECB) | Euro FX reference rates (about 30 currencies, daily) and euro-area statistics | FX, rates, macro | No key; no limit stated (unverified) | None | Rates are indicative, not for transactions [21] |
| FRED [22] | Official (St. Louis Fed) | US and international macro series | Economic time series | Rate-limited; number not stated on the fetched page [22] | Free API key | Separate API terms of use [22] |
| Eurostat [23] | Official (EU) | EU statistics | Macro, trade, prices | Free, no key mentioned; datasets update 11:00 and 23:00 CET [23] | None | Reuse notice not read (unverified) |
| Deutsche Börse [24] | Official (exchange) | Xetra, Eurex, EEX | Order-level and historical data | Commercial only; no free API verified [24] | Contract | Paid Market Data + Services licence |
| Tushare Pro [25] | Vendor (China) | CN, partly HK | Daily bars, fundamentals, indices | Points-gated: `daily` from 120 points; `daily_basic`, financial statements from 2,000 points [25] | Token after registration | Points tier controls frequency [25] |
| AKShare [26] | Unofficial open-source library | CN, HK, US and more | Prices, fundamentals, macro | No key; depends on the scraped sources | None | "Academic research" disclaimer; other use is your commercial risk [26] |
| BaoStock [27] | Free community platform | CN A-shares | Daily and minute K-lines, fundamentals | Free, no key per PyPI quick start; limits (unverified) [27] | `bs.login()` session | Terms not read (unverified) |
| Indonesia [28] | IDX sells data via its own service and distributors | ID | Streaming, EOD, history from 2005 via ICE | No free official data service verified [28] | Contract | See section 1.4 |

### 1.3 Docs URLs and points the table cannot show

- **Alpha Vantage** [1][2]: 25 requests/day suits a small EOD watchlist, not screening. Docs: https://www.alphavantage.co/documentation/
- **Finnhub** [3][4]: `/stock/insider-transactions` (Form 3/4/5 plus some non-US filings, 100 records per call) and `/stock/insider-sentiment` (monthly MSPR score, US only) are documented [4]; whether the free key includes them is (unverified). Docs: https://finnhub.io/docs/api
- **Twelve Data** [5][6]: European real-time data needs Pro [5]. Docs: https://twelvedata.com/docs
- **Financial Modeling Prep** [7][8]: paid Starter about 19 USD/month and Premium about 49 USD/month with annual billing; sources disagree on Ultimate (unverified). Stable insider endpoints: `insider-trading/latest`, `search`, `statistics` [8]. Docs: https://site.financialmodelingprep.com/developer/docs
- **Massive (formerly Polygon.io)**: the rename took effect 2025-10-30 (polygon.io to massive.com), existing APIs unaffected [10]. Stocks Starter 29 USD/month adds 15-minute delayed data and WebSockets; real-time needs Advanced at 199 USD/month [9]. Docs: https://massive.com/docs (certificate error on my fetch; check yourself).
- **EODHD** [11]: cheapest route to worldwide EOD in one API. Paid (monthly): EOD 19.99 EUR, EOD+intraday 29.99 EUR, fundamentals 59.99 EUR, all-in-one 99.99 EUR [11]. Docs: https://eodhd.com/financial-apis/
- **Tiingo** [12]: clean US/China EOD; licensed for internal personal use only. Docs: https://www.tiingo.com/documentation/general/overview
- **Marketstack** [13]: Basic 9.99 USD/month adds intraday for US via IEX. Docs: https://marketstack.com/documentation
- **Nasdaq Data Link** [14]: the former Quandl; most useful datasets are paid. Docs: https://docs.data.nasdaq.com/v1.0/docs/getting-started
- **Alpaca** [15]: a US broker's data API, not a way to trade through Trade Republic; Algo Trader Plus is 99 USD/month for all US exchanges. Docs: https://docs.alpaca.markets/docs/about-market-data-api
- **Stooq**: bulk historical files at https://stooq.com/db/h/ plus a CSV endpoint. 2026 reports say the CSV endpoint now needs a key obtained through a captcha, with quotas [16]; I could not load Stooq's own pages. Do not automate captcha solving.
- **yfinance** [17]: wraps Yahoo's unofficial endpoints. Risks: blocking, silent schema changes, no SLA, Yahoo terms. Fine for private experiments; never redistribute data from it. Docs: https://github.com/ranaroussi/yfinance
- **IEX Cloud**: retired on 2024-08-31 after the 2024-05-31 announcement [18]; a successor by former staff may exist (unverified). Drop it. **Polygon.io** is not dead, only renamed.
- **OpenFIGI** [19]: maps ISIN/ticker/CUSIP to FIGI, handy to join Trade Republic ISINs to vendor tickers. Docs: https://www.openfigi.com/api/documentation
- **ECB Data Portal** [20][21]: SDMX REST at `data-api.ecb.europa.eu`. Euro reference rates come around 16:00 CET on TARGET working days. Docs: https://data.ecb.europa.eu/help/api/data
- **FRED** [22]: JSON/XML, good for US rates and inflation. Docs: https://fred.stlouisfed.org/docs/api/fred/
- **Eurostat** [23]: REST APIs (STATISTICS, SDMX 2.1, SDMX 3.0). Docs: https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction
- **Deutsche Börse** [24]: Market Data + Services sells real-time Xetra data; a Data Shop and the A7 platform sell historical and order-level data. No free official API found. Docs: https://mds.deutsche-boerse.com/
- **Tushare Pro** [25]: points are a threshold, not consumed per call; more points allow higher call frequency; earned by activity or bought. Docs: https://tushare.pro/document/1
- **AKShare** [26]: Python library over public web data; the source sites' own terms still apply. Docs: https://akshare.akfamily.xyz/
- **BaoStock** [27]: A-share history via a Python package. Docs: https://pypi.org/project/baostock/
### 1.4 Indonesia and Hong Kong: what is actually free

- **Indonesia:** the IDX website publishes company announcements, but I could not load it (HTTP 403). IDX market data (streaming, EOD, history back to 2005) is sold through IDX data services and distributors such as ICE [28]. I found no free, official, key-based IDX price API. The practical free options are unofficial (yfinance `.JK` tickers) or paid vendors: Twelve Data lists IDX EOD from its Pro plan [6]. Treat any "free IDX API" claim as unverified.
- **Hong Kong:** HKEX real-time data is licensed. Vendor routes: Twelve Data HK EOD from Pro [6], EODHD (unverified per exchange), Tushare HK daily (points-gated, table inconsistent) [25], yfinance `.HK` (unofficial).
- **Germany and EU:** Xetra EOD via Twelve Data Grow [6], Alpha Vantage `.DEX` suffix [2], EODHD, or yfinance `.DE`. Exact Trade Republic venue (Bestpreis quote from Trade Republic, or the chosen Direktpreis venue) prices will differ from Xetra closing prices; see [Markets overview](markets/README.md).

---

## 2. Insider and disclosure sources

### 2.1 United States

**SEC EDGAR** is the primary source and the best free one.

- **data.sec.gov REST APIs** [29]: no key, no authentication. `submissions/CIK##########.json` (filing history, tickers, at least one year or 1,000 most recent filings), `api/xbrl/companyconcept`, `companyfacts` (all XBRL facts for one company), `frames` (one fact across companies for a period), plus nightly bulk files `companyfacts.zip` and `submissions.zip` (about 03:00 ET) [29]. The submissions API updates in typically under a second, XBRL APIs in under a minute [29]. CORS is not supported, so call from a script, not from browser JavaScript [29].
- **Fair access** [30]: declare a User-Agent that identifies you (company or name plus an admin contact email); current maximum is 10 requests per second; the SEC does not allow botnets or crawling tools and offers no technical support for scripts [30]. Stay well under the limit (for example 2 to 5 per second) and use bulk files for large jobs.
- **Form 4** [35]: insiders (officers, directors, more than 10 percent holders) report changes in ownership, due within two business days of the transaction. Plan-driven trades can fall under a later "notice" clock; check the bulletin. Form 3 (initial) and Form 5 (annual) have other deadlines (Form 3: 10 days, Form 5: 45 days after fiscal year end; from general knowledge, unverified here).
- **Insider Transactions Data Sets** [31]: quarterly ZIP files with the flattened XML portion of Forms 3, 4 and 5, January 2006 to September 2026, as filed, no licence text on the page and an accuracy disclaimer. Good for back-testing; not for same-week signals.
- **Form 13F data sets** [32]: quarterly ZIPs (July 2013 on) of the XML part of institutional holdings reports. 13F shows large institutions' positions after quarter end, so it is stale by design. The page does not state the 13F deadline.
- **Full-text search** [34]: filings since 2001 searchable by words, name, ticker, CIK, form and dates. It is a web search page; it is not among the documented data.sec.gov APIs [29], so do not scrape it heavily.
- **Fails-to-deliver** [33]: pipe-delimited files, twice per month (first half posted at month end, second half around the 15th of the next month), February 2004 on. Figures are cumulative balances, not daily new fails, and are not proof of abusive shorting [33].

**FINRA short interest** [50][51]: downloadable pipe-delimited files by settlement date, one rolling year online and archives; the page does not state frequency, delay or costs, so those are (unverified). FINRA also runs an API platform with a fees page [51]; the free tier is (unverified).

**US Congress (STOCK Act)**

- **House** [36][37]: Periodic Transaction Reports for transactions over 1,000 USD are due at the earlier of 30 days after the member is notified or 45 days after the transaction; filed with the Clerk of the House, searchable at https://disclosures-clerk.house.gov/FinancialDisclosure [36][37]. Bulk files on the Clerk's site cover member data; a bulk filings index (unverified).
- **Senate** [38]: electronic filing search at https://efdsearch.senate.gov. The page returned HTTP 403 for automated access; the site requires accepting a use statement before search. By federal law, reports may not be used for commercial purposes or fundraising (unverified here; read the statement on the site).
- **Third-party APIs**: Quiver Quantitative sells API access to congress trading data [39]; a competitor's July 2026 comparison reports about 30 USD/month for the entry tier, no free tier, and no commercial rights on the lower tiers [40] (all unverified; Quiver's pricing page did not show prices). Alpha Vantage and FMP also list congressional endpoints [2][8].
- **Quality note:** disclosures lag by up to 45 days, amounts are ranges, and spouse/dependent trades appear. It is a weak, late signal.

**Commercial insider endpoints:** Finnhub insider transactions and sentiment [4], FMP insider trading latest/search/statistics [8], Alpha Vantage `INSIDER_TRANSACTIONS` (`function=INSIDER_TRANSACTIONS&symbol=...`) [2]. All repackage SEC Form 4 data; check which plan includes them before paying.

**OpenInsider** (http://openinsider.com) [57]: free website that screens SEC Form 4 purchases and sales. It has no official API; I could not load the site, so its terms are (unverified). Scraping may break its terms; prefer the SEC bulk data or the SEC APIs above, which are the same underlying source.

### 2.2 Germany, EU and UK

- **BaFin managers' transactions ("Directors' Dealings", Art. 19 MAR)** [41][42]: reports are due without delay and at most three business days after the transaction; the reporting threshold was 20,000 EUR per calendar year until 31 Dec 2025 and has been 50,000 EUR since 2026-01-01 (BaFin general ruling of 4 Dec 2025; BaFin may revoke it at any time) [41][42]. The BaFin database lists notifications, updated daily, kept for 12 months after first publication, and only for issuers for which BaFin is competent authority; entries can appear days or weeks late because BaFin adds them after its administrative process. The primary source is the Unternehmensregister [41]. The page describes no export or API; BaFin gives no guarantee of completeness [41]. Search: https://portal.mvp.bafin.de/database/DealingsInfo/sucheForm.do
- **Unternehmensregister** [43]: central platform for company data. Registration and searching for individual companies and viewing publications are free; retrieving stored annual financial statements costs 1.00 EUR per document plus VAT; no bulk API described [43]. Capital-market notices such as voting-rights notifications are searchable there. https://www.unternehmensregister.de
- **Bundesanzeiger short-selling register** [44]: published net short positions (entries show holder, issuer, ISIN, position in percent, date), with history, searchable and filterable on the web page; no full-register export documented [44]. EU thresholds: positions are notified to the regulator from 0.1 percent and published from 0.5 percent, with further steps of 0.1 percent [45]. https://www.bundesanzeiger.de/pub/de/to_nlp_start
- **ESMA** [45]: does not host a central net-short register; it links to national central websites [45]. ESMA's European Single Access Point (ESAP) starts collecting information in July 2026 and opens to the public by July 2027 (ESMA) [58].
- **UK FCA National Storage Mechanism** [46]: free archive of regulated announcements (including MAR Art. 17 to 19 notifications, so UK directors' dealings), searchable by company, LEI, date and keyword, with CSV and JSON download of documents and CSV export of search results; no public API for readers (the API is for submitters), information is generally available within an hour of submission [46]. https://data.fca.org.uk/#/nsm/nationalstoragemechanism

### 2.3 Hong Kong, mainland China, Indonesia

- **Hong Kong, HKEXnews** [47][56]: HKEXnews offers listed-company announcements, CCASS shareholding and a Disclosure of Interests (DI) search [47]. Under Part XV of the Securities and Futures Ordinance, holders of 5 percent or more of voting shares must notify, and the notification period is three business days (secondary law-firm summaries; the directors' regime and the current rules are (unverified)) [56]. Access: web search; cost and bulk or API options are not stated on the fetched page [47]. https://www.hkexnews.hk
- **Mainland China, CNINFO** [48]: disclosure website of Shenzhen Stock Exchange's information subsidiary, with announcements for Shenzhen, Shanghai, ChiNext, STAR and Beijing boards; it also links a data platform and data API (webapi.cninfo.com.cn) whose pricing is not stated [48]. Insider trade reporting deadlines for Chinese directors and executives: (unverified). Web search only for most users; mostly Chinese language.
- **Indonesia, IDX and KSEI** [49]: under POJK 4/2024 and SEOJK 10/2025 (as cited by OJK), directors, commissioners and 5 percent holders of public companies report ownership and changes electronically through KSEI's AKSes system, which forwards the information to IDX for publication; full implementation reported from 2025-12-05 [49]. The filing deadline is (unverified). Access is the IDX website; I found no documented public API (unverified).

### 2.4 Comparison table (b): insider and disclosure sources

| Source | Jurisdiction | What is disclosed | Deadline | Access method | Cost | Docs |
|---|---|---|---|---|---|---|
| SEC EDGAR data.sec.gov [29][30] | US | Filing index, XBRL facts | Real time after filing | REST JSON, bulk ZIP | Free, 10 req/s, User-Agent needed | https://www.sec.gov/search-filings/edgar-application-programming-interfaces |
| SEC Form 4 [35] | US | Insider trades | 2 business days | EDGAR search, API, ZIP data sets [31] | Free | https://www.sec.gov/files/forms-3-4-5.pdf |
| SEC 13F data sets [32] | US | Institutional holdings | Not stated on page | Quarterly ZIP | Free | https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets |
| SEC full-text search [34] | US | Words in filings since 2001 | n/a | Web page | Free | https://www.sec.gov/edgar/search/ |
| SEC fails-to-deliver [33] | US | Cumulative FTD balances | Twice monthly, lagged | Pipe-delimited files | Free | https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data |
| FINRA short interest [50][51] | US | Short positions by settlement date | Not stated (unverified) | Files, API platform | Not stated (unverified) | https://www.finra.org/finra-data/browse-catalog/equity-short-interest/data |
| House PTR [36][37] | US | Members' trades | 30 days after notice / 45 days after trade | Clerk web search | Free | https://disclosures-clerk.house.gov/FinancialDisclosure |
| Senate eFD [38] | US | Senators' trades | 45 days (STOCK Act, unverified for Senate) | Web search, use statement | Free | https://efdsearch.senate.gov |
| Quiver Quantitative [39][40] | US | Congress trades via API | Follows filings | REST API | Paid (about 30 USD/month, unverified) | https://www.quiverquant.com |
| Finnhub / FMP / Alpha Vantage insider [2][4][8] | US plus some EU/other (Finnhub) | Form 3/4/5 data, sentiment scores | Follows filings | REST API | Free tier unverified | see section 1.3 |
| OpenInsider [57] | US | Form 4 screens | Follows filings | Website only | Free; terms unverified | http://openinsider.com |
| BaFin managers' transactions [41][42] | DE | PDMR trades at BaFin-supervised issuers | 3 business days; threshold 50,000 EUR from 2026 | Web database | Free | https://portal.mvp.bafin.de/database/DealingsInfo/sucheForm.do |
| Unternehmensregister [43] | DE | Company data, notices | Varies | Web search | Search free; financial statements 1 EUR each | https://www.unternehmensregister.de |
| Bundesanzeiger short register [44] | DE | Net short positions at or above 0.5% | Per EU SSR | Web search | Free | https://www.bundesanzeiger.de/pub/de/to_nlp_start |
| ESMA registers [45] | EU | Links to national registers | n/a | Links | Free | https://www.esma.europa.eu/esmas-activities/markets-and-infrastructure/short-selling |
| FCA National Storage Mechanism [46] | UK | Regulated announcements incl. MAR | Within about 1 hour of submission | Web, CSV/JSON download | Free | https://data.fca.org.uk/#/nsm/nationalstoragemechanism |
| HKEXnews DI [47][56] | HK | Substantial holders, directors | 3 business days (secondary, unverified) | Web search | Not stated | https://www.hkexnews.hk |
| CNINFO [48] | CN | Announcements, equity changes | Unverified | Web; data API (pricing unverified) | Not stated | http://www.cninfo.com.cn |
| IDX / KSEI AKSes [49] | ID | Ownership and changes (5%+, directors) | Unverified | IDX website | Not stated | https://www.idx.co.id |

---

## 3. Trade Republic: is there an API?

- **Official public trading API:** I found none. The only official API I found is a PSD2 open-banking API for registered third-party providers (payment initiation and account information on the cash account), documented in a TPP integration guide. Access needs a bearer token obtained with an eIDAS QSeal certificate and customer strong authentication [52]. That is for licensed providers, not for retail users who want to read their depot or place orders. I did not find order or portfolio endpoints in it (unverified, the PDF was not readable).
- **Unofficial clients exist.** The best known is "pytr", an MIT-licensed command-line library for Trade Republic's private API; the project states it is not affiliated with Trade Republic Bank GmbH, can stop working whenever Trade Republic changes its systems, and may require repeated logins [55].
- **Terms of service.** Trade Republic's customer agreement, clause 2.3 in the 2022 versions I found, forbids using Trade Republic's functions through access paths, programs or interfaces outside the app that Trade Republic did not provide, and reserves the right to terminate the relationship extraordinarily (clause 10.2) [53]. Check the current version of the agreement before relying on this wording.
- **Security.** The agreement and Trade Republic's help pages say the PIN must stay secret, must not be passed on, and that Trade Republic never asks for the PIN or SMS code [53][54]. Typing credentials into third-party code gives that code full account access.
- **Account risk.** Possible consequences: broken access, account restrictions or termination, and liability for losses if credentials leak.

Recommendation for this wiki: do not put Trade Republic credentials into any third-party tool or script. Do research with the public sources on this page and place orders yourself in the official app. This page gives no setup steps for unofficial clients.

---

## 4. Minimal, safe Python examples (not executed)

These are illustrations. They were not run when this page was written. They use `requests` only, no keys, and stay under the SEC's request limit. Replace the placeholders yourself.

### 4.1 Recent Form 4 filings from data.sec.gov

```python
import os
import time

import requests

# Fair-access rule: identify yourself. Use a real name and contact address of your own.
USER_AGENT = os.environ.get("SEC_USER_AGENT", "YOUR_NAME your-email@example.com")
HEADERS = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}

CIK = "0000320193"  # example issuer CIK, 10 digits, zero-padded

def get_json(url: str) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    time.sleep(0.3)  # stay far below the 10 requests/second maximum
    return response.json()

submissions = get_json(f"https://data.sec.gov/submissions/CIK{CIK}.json")
recent = submissions["filings"]["recent"]  # parallel lists

form4 = [
    (recent["filingDate"][i], recent["accessionNumber"][i], recent["primaryDocument"][i])
    for i, form in enumerate(recent["form"])
    if form == "4"
][:10]

for filing_date, accession, document in form4:
    folder = accession.replace("-", "")
    # primaryDocument is often an XSL-rendered path such as "xslF345X05/<name>.xml";
    # the raw XML is the same file name without that prefix folder.
    url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{folder}/{document}"
    print(filing_date, accession, url)
```

Notes: a Form 4 appears in the submissions list of both the issuer and the reporting person. To parse the XML later, use `defusedxml` rather than the standard parser for untrusted input, and keep the same User-Agent and pacing. Buys have transaction code `P` (open-market purchase), sales `S`.

### 4.2 ECB euro reference rate (EUR/USD)

```python
import csv
import io

import requests

# No key needed. Key = frequency.currency.denominator.type.suffix (daily USD per 1 EUR).
URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"
response = requests.get(
    URL,
    params={"lastNObservations": 5, "format": "csvdata"},
    timeout=30,
)
response.raise_for_status()

for row in csv.DictReader(io.StringIO(response.text)):
    print(row["TIME_PERIOD"], row["OBS_VALUE"])  # indicative rate, USD per EUR
```

### 4.3 Pattern for a keyed API

```python
import os

import requests

API_KEY = os.environ["API_KEY"]  # set in your shell or a secrets manager, never in code
response = requests.get(
    "https://www.alphavantage.co/query",
    params={"function": "INSIDER_TRANSACTIONS", "symbol": "IBM", "apikey": API_KEY},
    timeout=30,
)
response.raise_for_status()
data = response.json()
```

The Alpha Vantage free tier allows 25 requests per day [1], so cache results to disk instead of re-calling.

---

## 5. Ideas for a personal data pipeline

All of this is research tooling for your own use. Nothing here needs Trade Republic access.

- **Watchlist with EOD prices.** Map your Trade Republic ISINs to tickers with OpenFIGI [19], then pull daily closes once per day from one vendor: EODHD (cheap, global), Twelve Data (free for US), or Tiingo (US/China, personal use) [11][5][12]. Store in SQLite or CSV and convert to EUR with the ECB daily rate [21]. Keep the raw responses so you can re-run calculations.
- **Insider-buy screener (US).** Download the quarterly Insider Transactions Data Sets [31] for history and poll `data.sec.gov` submissions for your watchlist's recent Form 4s [29]. Filter on open-market purchases by officers and directors, and look at cluster buys. For German issuers, check the BaFin database manually (no API) [41] and for UK issuers the FCA NSM CSV export [46]. Remember Form 4 can be two business days late and BaFin entries may appear days later.
- **Short-interest and FTD overlay.** Add FINRA short interest and SEC fails-to-deliver files [50][33] for US names, and the Bundesanzeiger register for German names [44]. These are lagging, noisy context, not trading signals by themselves.
- **Dividend and earnings calendar.** Fundamentals vendors (FMP, EODHD, Finnhub, Alpha Vantage) expose dividend and earnings calendars on their paid or limited free tiers (endpoint availability per plan unverified). Cross-check against the company's own investor-relations page.
- **Macro dashboard.** ECB for FX and euro-area rates, FRED for US rates and inflation, Eurostat for EU indicators [20][22][23].
- **Quality gates.** Compare two sources for the same close, log failures, respect each provider's daily quota, and store the "as of" time of every figure.

**The legal line.** Using published filings and public registers (Form 4, BaFin managers' transactions, public registers) is legal and is what these pages are for. Trading on material non-public information is insider trading and is a criminal offence in the EU, Germany, the UK and the US; so is passing such information on. Disclosure data is also delayed, incomplete and sometimes wrong, and does not tell you why someone traded. This page is not investment or legal advice; see [Strategy](strategy.md) for how to weigh signals and risk.

---

## Sources

1. Alpha Vantage, "Premium API Key" plans, Alpha Vantage Inc., https://www.alphavantage.co/premium/, accessed 2026-10-17.
2. Alpha Vantage, "API Documentation", Alpha Vantage Inc., https://www.alphavantage.co/documentation/, accessed 2026-10-17.
3. Finnhub, "Pricing" (free tier 60 calls/minute, personal use; figure read through a search result of the page, my direct fetch returned only marketing text), Finnhub, https://api.finnhub.io/pricing, accessed 2026-10-17.
4. Finnhub, "API Documentation" (insider transactions and insider sentiment endpoint descriptions from a docs snapshot), Finnhub, https://finnhub.io/docs/api, accessed 2026-10-17.
5. Twelve Data, "Pricing", Twelve Data, https://twelvedata.com/pricing, accessed 2026-10-17.
6. Twelve Data, "Exchanges" (minimum plan per exchange), Twelve Data, https://twelvedata.com/exchanges, accessed 2026-10-17.
7. Financial Modeling Prep, "Pricing Plans" (direct fetch blocked with HTTP 403; figures from search snippets of the page), FMP, https://site.financialmodelingprep.com/pricing-plans, accessed 2026-10-17.
8. Financial Modeling Prep, "Insider Trade Statistics API", FMP, https://site.financialmodelingprep.com/developer/docs/stable/insider-trade-statistics, accessed 2026-10-17.
9. Massive, "Pricing", Massive (formerly Polygon.io), https://massive.com/pricing, accessed 2026-10-17.
10. FISD, "Polygon.io is Now Massive" (rename effective 2025-10-30), Financial Information Services Division of SIIA, https://fisd.net/polygon-io-is-now-massive, accessed 2026-10-17.
11. EODHD, "Pricing", EOD Historical Data, https://eodhd.com/pricing, accessed 2026-10-17.
12. Tiingo, "Pricing", Tiingo Inc., https://www.tiingo.com/about/pricing, accessed 2026-10-17.
13. Marketstack, "Pricing", apilayer, https://marketstack.com/pricing, accessed 2026-10-17.
14. Nasdaq Data Link, "Getting started" and rate limits, Nasdaq, https://docs.data.nasdaq.com/v1.0/docs/getting-started, accessed 2026-10-17 (read through search result text).
15. Alpaca, "About Market Data API", Alpaca Markets, https://docs.alpaca.markets/docs/about-market-data-api, accessed 2026-10-17.
16. pandas-datareader issue #1012, "Stooq now requires API key" (third-party report, Stooq's own pages not loaded), https://github.com/pydata/pandas-datareader/issues/1012, accessed 2026-10-17.
17. yfinance, README (legal disclaimer), Ran Aroussi and contributors, https://github.com/ranaroussi/yfinance, accessed 2026-10-17.
18. Alpha Vantage, "IEX Cloud Has Shut Down: Analysis & Migration Guide" (competitor; third-party account of the 2024-08-31 shutdown), https://www.alphavantage.co/iexcloud_shutdown_analysis_and_migration/, accessed 2026-10-17.
19. OpenFIGI, "API Documentation", Bloomberg L.P., https://www.openfigi.com/api/documentation, accessed 2026-10-17.
20. ECB Data Portal, "Data API" help, European Central Bank, https://data.ecb.europa.eu/help/api/data, accessed 2026-10-17 (page returned 503 on direct fetch; URL pattern confirmed through a search result of the page).
21. European Central Bank, "Euro foreign exchange reference rates", https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html, accessed 2026-10-17.
22. St. Louis Fed, "FRED API overview", https://fred.stlouisfed.org/docs/api/fred/overview.html, accessed 2026-10-17.
23. Eurostat, "API - Introduction", European Commission, https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction, accessed 2026-10-17.
24. Deutsche Börse Market Data + Services, "A7 Analytics Platform", https://mds.deutsche-boerse.com/mds-en/analytics/A7-analytics-platform, accessed 2026-10-17 (via search result).
25. Tushare, "Points (积分) system", Tushare Pro, https://tushare.pro/document/1?doc_id=108, accessed 2026-10-17.
26. AKShare, "Introduction", AKFamily, https://akshare.akfamily.xyz/introduction.html, accessed 2026-10-17.
27. BaoStock, package page, Python Package Index, https://pypi.org/project/baostock/, accessed 2026-10-17 (via search result).
28. ICE, "Indonesia Stock Exchange (IDX)" data catalogue, Intercontinental Exchange, https://developer.ice.com/fixed-income-data-services/catalog/indonesia-stock-exchange-idx, accessed 2026-10-17 (via search result).
29. SEC, "EDGAR Application Programming Interfaces", U.S. Securities and Exchange Commission, https://www.sec.gov/search-filings/edgar-application-programming-interfaces, accessed 2026-10-17.
30. SEC, "Accessing EDGAR Data" (fair access), U.S. Securities and Exchange Commission, https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data, accessed 2026-10-17.
31. SEC, "Insider Transactions Data Sets", https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets, accessed 2026-10-17.
32. SEC, "Form 13F Data Sets", https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets, accessed 2026-10-17.
33. SEC, "Fails-to-Deliver Data", https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data, accessed 2026-10-17.
34. SEC, "EDGAR Full-Text Search", https://www.sec.gov/edgar/search/, accessed 2026-10-17.
35. SEC and Investor.gov, "Updated Investor Bulletin: Insider Transactions and Forms 3, 4, and 5" (two-business-day Form 4 deadline; direct fetch blocked, confirmed through search result), https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-69, accessed 2026-10-17.
36. Committee on Ethics, U.S. House of Representatives, "Financial Disclosure", https://ethics.house.gov/financial-disclosure/, accessed 2026-10-17.
37. Clerk of the U.S. House of Representatives, "Financial Disclosure Reports", https://disclosures-clerk.house.gov/FinancialDisclosure, accessed 2026-10-17.
38. U.S. Senate, "Electronic Financial Disclosure (eFD) search", https://efdsearch.senate.gov/search/home/, accessed 2026-10-17 (HTTP 403 on automated fetch; not read).
39. Quiver Quantitative, website and pricing link, https://www.quiverquant.com/pricing/, accessed 2026-10-17 (no prices shown on the fetched page).
40. Disclosed Capitol, "vs QuiverQuant" (competitor comparison, July 2026; third-party), https://www.disclosedcapitol.com/vs/quiverquant, accessed 2026-10-17 (via search result).
41. BaFin, "Eigengeschäfte von Führungskräften" (database page), Bundesanstalt für Finanzdienstleistungsaufsicht, https://www.bafin.de/DE/die-bafin/publikationen-daten/datenbanken-uebersichten/eigengeschaefte-fuehrungskraefte/eigengeschaefte-fuehrungskraefte_node.html, accessed 2026-10-17.
42. BaFin, "Bekanntmachung einer Allgemeinverfügung zur Anhebung des Schwellenwertes auf 50.000,00 EUR" (2025-12-04), https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Aufsichtsrecht/Verfuegung/vf_20251204_meldeschwelle_kraft.html, accessed 2026-10-17.
43. Unternehmensregister, "Kosten", https://www.unternehmensregister.de/de/so-gehts/kosten, accessed 2026-10-17.
44. Bundesanzeiger, "Netto-Leerverkaufspositionen" register, Bundesanzeiger Verlag, https://www.bundesanzeiger.de/pub/de/to_nlp_start, accessed 2026-10-17.
45. ESMA, "Short selling", European Securities and Markets Authority, https://www.esma.europa.eu/esmas-activities/markets-and-infrastructure/short-selling, accessed 2026-10-17.
46. FCA, "National Storage Mechanism", Financial Conduct Authority, https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism, accessed 2026-10-17.
47. HKEXnews, home page (listed company information, CCASS shareholding, Disclosure of Interests), Hong Kong Exchanges and Clearing, https://www.hkexnews.hk/, accessed 2026-10-17.
48. CNINFO (巨潮资讯网), Shenzhen Securities Information Co., http://www.cninfo.com.cn/new/index, accessed 2026-10-17.
49. OJK, press release on AKSes KSEI electronic reporting, Otoritas Jasa Keuangan, https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Documents/Pages/AKSes-KSEI-dan-Fitur-Publikasi-Melalui-Website-BEI/SP%208%20OJK%20Dorong%20Keterbukaan%20Informasi%20Dan%20Penguatan%20Pengawasan%20%20Bidang%20Pasar%20Modal%20melalui%20AKSes%20KSEI.pdf, accessed 2026-10-17 (via search result summary).
50. FINRA, "Equity Short Interest" data, https://www.finra.org/finra-data/browse-catalog/equity-short-interest/data, accessed 2026-10-17.
51. FINRA, "FINRA API Platform", https://developer.finra.org/, accessed 2026-10-17.
52. Trade Republic, "PSD2 Open Banking TPP Integration Guide v2", Trade Republic Bank GmbH, https://assets.traderepublic.com/assets/files/TPP_API_Guide_v2.pdf, accessed 2026-10-17 (PDF text not readable by my tool; summary from search result).
53. Trade Republic, "Kundenvereinbarung" (customer agreement, clause 2.3 and 10.2 as in 2022 versions), https://assets.traderepublic.com/documents/DE/CONTRACT_CUSTOMER_AGREEMENT_20221230100013.pdf, accessed 2026-10-17 (via search result; check the current version).
54. Trade Republic Support, "Wie kann ich mein Konto sicher halten?", https://support.traderepublic.com/de-de/1686-Wie-kann-ich-mein-Konto-sicher-halten, accessed 2026-10-17 (via search result).
55. pytr, README (unofficial Trade Republic client; MIT licence), https://github.com/pytr-org/pytr, accessed 2026-10-17.
56. Charltons, "Disclosure of Interests under the Securities and Futures Ordinance Overview" (secondary law-firm summary), https://www.charltonslaw.com/disclosure-of-interests-under-the-securities-and-futures-ordinance/, accessed 2026-10-17 (via search result).
57. OpenInsider, home page, http://openinsider.com/, accessed 2026-10-17 (fetch failed; not read).
58. ESMA, "European Single Access Point (ESAP)", European Securities and Markets Authority, https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/european-single-access-point-esap, accessed 2026-10-17.
