# Germany stock market

_Last checked: 2026-10-17 · Educational content, not investment advice._

Related pages: [Trading basics](../01-trading-basics.md) · [Markets overview](README.md) · [Europe](europe.md) · [USA](usa.md) · [China](china.md) · [Indonesia](indonesia.md) · [Strategy](../strategy.md) · [APIs](../apis.md)

## 1. Overview

- **Size.** At end-2025, listed domestic companies in Germany had a combined market capitalisation of about US$2.90 trillion, up from US$2.04 trillion at end-2024 [1]. That equals 57.4 % of German GDP [3]. The world total was about US$141.3 trillion, so Germany is roughly 2 % of global equity market value (own calculation from [1][4]); the USA is about US$68.9 trillion and China about US$15.5 trillion [4]. The World Bank series republishes World Federation of Exchanges (WFE) data; the definition counts domestic companies only and excludes funds and ETFs.
- **Listings.** 416 domestic companies at end-2025, down from 435 in 2024 and 470 in 2019 [2]. The market is shrinking in company count (more delistings than IPOs) while value is dominated by a few dozen large caps.
- **Role.** Germany is one of the larger European equity markets, with Frankfurt as the home of Deutsche Börse; a euro-area or Europe-wide ranking could not be verified from the sources used (the euro-area value was not available in [4]); see [Europe](europe.md). The large caps are global exporters (industry, insurance, software, chemicals, autos), so index returns depend heavily on world demand rather than German domestic demand (inference).
- **Retail culture.** The *Aktienkultur* (share culture) is often described as historically weak (common view, unverified) but is growing. In 2025, 14.1 million people in Germany held shares, equity funds or ETFs, a record [25]; this is about one in five people aged 14+ (19.9 %), and 12.1 million of them hold funds or ETFs [25b]. *Sparpläne* (automatic recurring savings plans, often monthly into an ETF) are a common entry route (popularity figures not verified); one secondary source reports that Trade Republic savings-plan executions are free of charge [21].

## 2. Exchanges and main indices

### Trading venues

| Venue | Operator / type | What it is | Typical hours (German time) |
|---|---|---|---|
| **Xetra** | Deutsche Börse, electronic order book (T7) | Reference market for German shares and ETFs; central limit order book with auctions | 09:00-17:30 [13] |
| **Börse Frankfurt** (Frankfurt floor and "Frankfurt" quotations) | Deutsche Börse | Regulated market with specialists/market makers; extended hours | generally 08:00-22:00 [13] |
| **Tradegate Exchange** (Berlin) | Tradegate Exchange GmbH; Deutsche Börse took 75 % plus one share in 2010 [24] | Regulated market built for retail order flow via online brokers | 08:00-22:00 at launch [24]; check current hours |
| **gettex** | Börse München (Bayerische Börse), Baader Bank as market maker | Market-maker model; since Jan 2025: 07:30-23:00 for ETPs, funds, bonds and the 1,000 most traded shares, 08:00-22:00 for the rest [23] | 07:30-23:00 / 08:00-22:00 |
| **LS Exchange** | Börse Hamburg trading system with Lang & Schwarz | Retail-focused market-maker venue; hours reported as 07:30-23:00 by secondary sites (unverified) | see left |
| **Börse Stuttgart** (incl. Euwax) | Boerse Stuttgart | Strong in structured products and bonds; described as Germany's second-largest exchange by turnover in a secondary source (unverified) | check venue |

How they differ (mechanism): Xetra is an open order book where buyers and sellers meet, with a tick-by-tick public price formation and the deepest liquidity. The others are mostly **market-maker venues**: a designated dealer quotes bid and ask and the order is executed against that quote, usually at the Xetra-referenced price, with extended hours and often no explicit commission to the broker. The reported share of Xetra in German share turnover is around 90 % (unverified, secondary). The trade-off for retail is the **spread** (difference between buy and sell price): outside 09:00-17:30 the reference price is stale and spreads widen (inference; see [Trading basics](../01-trading-basics.md)).

### Main indices (all operated with STOXX and Deutsche Börse)

| Index | Members | What it measures | Top sectors / notes |
|---|---|---|---|
| **DAX** | 40 (raised from 30 on 20 Sep 2021 [6]) | Largest firms by free-float market cap on the Frankfurt regulated market; about 80 % of German listed stock-corporation market value [5]; total-return ("performance") index, dividends reinvested [5] | Industrials 34.7 %, finance 22.6 %, technology 15.2 % (ETF classification, 31 Aug 2026) [8] |
| **MDAX** | 50 [7] | Mid caps ranked after the DAX [7] | Industrials 35.5 %, consumer cyclicals 13.1 %, finance 12.9 %, materials 11.9 % [9] |
| **SDAX** | 70 [5] | Small caps ranked after the MDAX [5] | sector split not retrieved |
| **TecDAX** | 30 (holdings of tracker [10]) | Largest technology and technology-related firms of the prime segment | Technology 46.3 %, healthcare 24.5 %, telecom 18.6 % [10] |
| **DAX All Cap** | 160 (40+50+70) [12] | Combination of DAX, MDAX and SDAX | n/a |

Rules: selection by free-float market cap with a minimum free float of 10 %, positive EBITDA in the last two years and minimum liquidity; regular reviews in March and September with fast entry or exit in June and December [5]. A single stock's weight is capped at 15 % (raised from 10 % in March 2024) [6]; the same 15 % cap is stated for the MDAX [7].

### Top constituents and concentration

Weights of the iShares Core DAX fund on 31 Aug 2026 (a proxy for index weights, not the index itself) [8]: Siemens 11.7 %, SAP 10.8 %, Allianz 9.6 %, Airbus 6.5 %, Siemens Energy 6.5 %, Deutsche Telekom 5.5 %, Infineon 4.1 %, Deutsche Bank 3.7 %, Munich Re 3.7 %, Deutsche Börse 3.0 %. The **top three alone are about 32 %, the top ten about 65 %** [8]. STOXX lists the same top ten order [6]. MDAX top ten (31 Aug 2026): about 38 % led by Lufthansa, Talanx, thyssenkrupp, Knorr-Bremse [9]. TecDAX top ten: about 80 %, with SAP near 20 % and Deutsche Telekom near 15 % [10]; the SAP figure is above the 15 % cap, which may be drift between rebalances (unverified).

### Segments for listing quality

On the Frankfurt regulated market there are two EU-regulated segments: the **General Standard** (legal minimum duties) and the **Prime Standard** (extra transparency: German and English reporting, quarterly statements, analysts' conference) [26]. The **Scale** segment is part of the unregulated *Open Market* with lighter rules [26]. Indices such as DAX draw only on the regulated market [5], so Prime Standard is where the index-grade companies sit (inference).

## 3. Trading hours

| Item | Detail |
|---|---|
| Local time | Central European time: CET (UTC+1) in winter, CEST (UTC+2) in summer. Deutsche Börse writes "CET" for the whole year. |
| Mismatch with German time | None (Germany is the reference time). Against the USA there are about 1 to 3 weeks twice a year when US and EU daylight saving differ; this year EU clocks go back on 25 Oct 2026, the USA on 1 Nov 2026 (inference from the standard DST rules; see [USA](usa.md)). |
| Xetra continuous trading | Mon-Fri 09:00-17:30 [13] |
| Auctions | Opening auction call from 08:50; closing auction call from 17:30, earliest price 17:35, trade-at-close until 17:45 [14]; an intraday auction around 13:00 is reported on special-day notices (regular schedule not confirmed, unverified) [14]. Auctions end at a random moment after the minimum duration [14]. |
| Extended retail | Xetra Retail Service 08:00-08:55 and 17:30-22:00 [13]; Frankfurt generally 08:00-22:00 [13] |
| Lunch break | None |
| Holiday calendar (source: [13]) | No trading 2026: 1 Jan, 3 Apr (Good Friday), 6 Apr (Easter Monday), 1 May, 24 Dec, 25 Dec, 31 Dec. 2027: 1 Jan, 26 Mar, 29 Mar, 24 Dec, 31 Dec. Trading takes place on Ascension (14 May 2026), Whit Monday (25 May) and Corpus Christi (4 Jun) [13]. |
| Price limits | No fixed daily limit. **Volatility interruptions** switch continuous trading to an auction when the next price would leave a dynamic or static corridor [15]; the corridors are per instrument and not published in the sources I read; a 2021 Xetra circular describes classes with dynamic ranges of ±0.5 % to ±5 % and static ranges of ±2 % to ±15 % (unverified, may be outdated) [16]. I did not find a market-wide circuit breaker. |
| Settlement | T+2 currently (standard EU cycle, unverified for this venue); T+1 from 11 Oct 2027 under Regulation (EU) 2025/2075 [35], following ESMA's proposal [17]. |
| Lot size | Shares trade per piece on Xetra; minimum order sizes depend on the instrument (not verified). |
| Trade Republic | Standard "Bestpreis" mode: Mon-Fri 07:30-23:00 CET; "Direktpreis" follows the chosen venue; market and stop orders only in hours, limit orders can be placed at any time [18]. |

## 4. Currency and FX risk for a euro investor

German shares are quoted in **EUR**, so there is no direct FX risk for a euro investor. Indirect FX exposure exists because many DAX companies earn large shares of revenue abroad (for example US dollars and Chinese yuan); a stronger euro can lower reported earnings (inference, no figure verified). DAX-tracking ETFs and Xetra lines are EUR-denominated.

## 5. Regulator and investor protection; filings

- **BaFin** (*Bundesanstalt für Finanzdienstleistungsaufsicht*, Federal Financial Supervisory Authority) supervises securities markets, issuers and market abuse. Each exchange also has its own state supervisory authority and a trading surveillance unit (*Handelsüberwachungsstelle*) (general knowledge, unverified here).
- **Market abuse rules.** The EU Market Abuse Regulation (MAR) covers ad-hoc disclosure and insider dealing; see *Directors' Dealings* in section 9.
- **Investor protection.** Securities in a custody account are segregated from the broker's own assets (*Sondervermögen*); statutory deposit and investor compensation schemes exist; I did not verify the current limits, so check the broker's documents.
- **Filings.** Company registers: *Unternehmensregister* (company register portal), *Bundesanzeiger* (federal gazette) and the issuers' own investor-relations pages; ad-hoc announcements are published by the issuer under MAR (general knowledge, unverified).

## 6. Market characteristics and specific risks

- **Concentration.** The top three DAX names are about 32 % and the top ten about 65 % of a DAX tracker; three sectors (industrials, finance, technology) make up about 72 % [8]. SAP alone is nearly 11 %, so a "German index" is partly a bet on a few global groups, not on the German domestic economy [8].
- **Cyclicality.** Heavy exposure to industrials, autos, chemicals and exports (inference): sensitive to global trade, energy costs and China/US demand.
- **Total-return design.** Because the DAX reinvests dividends, its level is not comparable with price indices such as the EURO STOXX 50; compare like with like [5].
- **Costs of the niche segments.** MDAX and TecDAX tracker ETFs charge higher annual fees (TER 0.51 %) than DAX trackers (0.09-0.16 %) [9][10][8][11].
- **Market structure.** Share count is falling [2]; retail participation is rising [25].
- **Retail vs institutional.** I did not find a verified split of turnover between retail and institutional investors.
- **Political and regulatory risk.** EU-wide rules (MAR, MiFID II, payment-for-order-flow ban) affect brokers: the EU banned payment for order flow from 1 July 2026, and Trade Republic then added venue choice [21].

## 7. Access from Germany via Trade Republic

- **Single shares.** Trade Republic's help pages give different counts (more than 6,500 international stocks; up to about 7,500 stocks in total); check the app. The help centre says nearly every security listed on the German market is included [20]. In Bestpreis mode the order is executed against Trade Republic at a price chosen by an algorithm comparing quotes on up to 30 exchanges; in "Direktpreis" mode you pick a venue [19][21]. The older help page states LS Exchange as the main venue with Tradegate as fallback [19b]; as of July 2026, the venue list includes Xetra, Tradegate and LS Exchange (gettex not mentioned) [21]. Fees reported by a secondary source: EUR 1 per order in Bestpreis, EUR 2 per order plus external costs for Direktpreis (press-sourced); plans free [21]. Check the current price list in the app.
- **Currency/venue.** German shares trade in EUR on these venues; availability and price details per security can only be confirmed in the app.
- **UCITS ETFs (category examples, not recommendations; availability must be checked in the app):**
  - Broad large-cap DAX trackers: iShares Core DAX UCITS ETF (DE), ISIN DE0005933931, TER 0.16 %, accumulating, German domicile [8]; Xtrackers DAX UCITS ETF 1C, ISIN LU0274211480, TER 0.09 %, accumulating, Luxembourg domicile [11].
  - Mid caps: iShares MDAX UCITS ETF (DE), ISIN DE0005933923, TER 0.51 %, accumulating [9]. TecDAX trackers also exist [10].
  - Broader exposure: Europe and developed-world index ETFs hold German weights; see [Europe](europe.md).
- **ADRs / secondary listings.** The natural way for a euro investor is the German line in EUR. Some German companies also have US ADRs or listings on other exchanges (unverified); this brings USD exposure and US/other withholding rules, see [USA](usa.md).

## 8. Taxes specific to this market

For a German tax resident holding **German-domiciled** shares:

- **Withholding on dividends.** *Kapitalertragsteuer* (capital gains tax at source, also called *Abgeltungsteuer*) of 25 % plus 5.5 % *Solidaritätszuschlag* (solidarity surcharge) on that tax, together 26.375 % [29]; church tax is added if applicable (9 % in most states, 8 % in Baden-Württemberg and Bavaria; the flat-tax component drops to 24.45 % at 9 % church tax (about 27.99 % in total with Soli and church tax)) [29]. The deduction is in principle final, so the annual return (*Anlage KAP*) is usually not needed [29].
- **Allowance.** *Sparer-Pauschbetrag* (saver's allowance) EUR 1,000 per person, EUR 2,000 for joint assessment, via a *Freistellungsauftrag* (exemption order) at the broker [29].
- **Treaty rate.** Not relevant for German companies paying a German resident (no double-tax treaty applies to a purely domestic payment).
- **Foreign-domiciled DAX members.** Some index members are registered abroad (for example Airbus SE and QIAGEN N.V., unverified). Their dividends may carry foreign withholding tax. For the Netherlands, a secondary table based on BZSt data shows 15 % withheld and 15 % creditable [32]. Foreign withholding is generally credited by the paying agent up to 25 % [30]; where the source country offers a refund, the paying agent does not credit that part and you must claim the excess abroad with BZSt forms [30][31]. Check the current BZSt table (as of 1 Jan 2026) for the exact rates [31].
- **Equity ETFs.** Equity funds receive a 30 % *Teilfreistellung* (partial exemption) of income for private investors [33].
- **Tax certificate.** Trade Republic issues an annual *Jahressteuerbescheinigung* (tax certificate) in Q1 of the following year [22].

## 9. Useful official data sources

- **Directors' Dealings (Art. 19 MAR).** Board members and other persons discharging managerial responsibilities (and closely associated persons) must report own-account transactions in the issuer's shares to the issuer and to BaFin promptly and within three business days; the issuer must publish within two working days [27]. The German threshold is **EUR 50,000 per calendar year from 1 January 2026** (BaFin general ruling of 4 Dec 2025) [34], raised from EUR 20,000 (in force since 1 Jan 2020; EU baseline under the Listing Act is EUR 20,000, national authorities may set 10,000-50,000) [28][27]. BaFin's database holds published transactions up to one year back, including voluntary reports below the threshold [27]. Use: a public, time-stamped signal for insider buying/selling; note the higher threshold means fewer small trades are reported. See [Strategy](../strategy.md) and [APIs](../apis.md) for how to use it; I did not verify any retrieval API.
- Exchange and trading calendar: Deutsche Börse cash market [13]; Börse Frankfurt data portal (live.deutsche-boerse.com) [15].
- Index data: STOXX (DAX family) [6][7][12] and Deutsche Börse explainer [5].
- Tax: BZSt foreign withholding tax pages and creditable-rates list [30][31]; Finanzamt NRW [29].
- Shareholder statistics: Deutsches Aktieninstitut [25].

## Sources

1. World Bank (WFE data), "Market capitalization of listed domestic companies (current US$)", Germany. https://api.worldbank.org/v2/country/DEU/indicator/CM.MKT.LCAP.CD?format=json. Accessed 2026-10-17.
2. World Bank (WFE data), "Listed domestic companies, total", Germany. https://api.worldbank.org/v2/country/DEU/indicator/CM.MKT.LDOM.NO?format=json. Accessed 2026-10-17.
3. World Bank (WFE data), "Market capitalization of listed domestic companies (% of GDP)", Germany. https://api.worldbank.org/v2/country/DEU/indicator/CM.MKT.LCAP.GD.ZS?format=json. Accessed 2026-10-17.
4. World Bank (WFE data), market capitalisation 2025 for World, USA, China. https://api.worldbank.org/v2/country/WLD;USA;CHN/indicator/CM.MKT.LCAP.CD?format=json&date=2025. Accessed 2026-10-17.
5. Deutsche Börse, "DAX - Benchmark and Barometer for the German Economy". https://deutsche-boerse.com/dbg-en/media/news-stories/explainers/financial-market-know-how/explainer-dax. Accessed 2026-10-17.
6. STOXX, DAX index page. https://stoxx.com/index/dax/. Accessed 2026-10-17.
7. STOXX, MDAX index page. https://stoxx.com/index/mdax/. Accessed 2026-10-17.
8. justETF, iShares Core DAX UCITS ETF (DE), holdings as of 31 Aug 2026. https://www.justetf.com/en/etf-profile.html?isin=DE0005933931. Accessed 2026-10-17.
9. justETF, iShares MDAX UCITS ETF (DE). https://www.justetf.com/en/etf-profile.html?isin=DE0005933923. Accessed 2026-10-17.
10. justETF, iShares TecDAX UCITS ETF (DE). https://www.justetf.com/en/etf-profile.html?isin=DE0005933972. Accessed 2026-10-17.
11. justETF, Xtrackers DAX UCITS ETF 1C. https://www.justetf.com/en/etf-profile.html?isin=LU0274211480. Accessed 2026-10-17.
12. STOXX, DAX All Cap index page. https://stoxx.com/index/daxacn/. Accessed 2026-10-17.
13. Deutsche Börse Cash Market, "Trading calendar and trading hours" (2026-2027). https://cashmarket.deutsche-boerse.com/cash-en/trading/trading-calendar-and-trading-hours. Accessed 2026-10-17.
14. Deutsche Börse / Xetra, "Final trading session 2024" notice (auction times; seen via search result, not opened in full). https://xetra.com/resource/blob/4064970/4beb98bd98c44f58e1fb68e3f3bb9746/data/Final%20trading%20session%202024.pdf. Accessed 2026-10-17.
15. Börse Frankfurt, "Protection in extreme situations" (volatility interruptions; seen via search result, page not retrievable on 2026-10-17). https://live.deutsche-boerse.com/en/know-how/handeln/protection-in-extreme-situations. Accessed 2026-10-17.
16. Xetra Circular 080/21, attachment (parameter classes; seen via search result). https://xetra.com/resource/blob/2842762/5946b6dd580acc5a09ab1062984a260f/data/Xetra_Circular_080_21_en_Attach.pdf. Accessed 2026-10-17.
17. ESMA, "ESMA proposes to move to T+1 by October 2027". https://www.esma.europa.eu/node/214007. Accessed 2026-10-17.
18. Trade Republic Support, "Wann sind die Handelszeiten?". https://support.traderepublic.com/de-de/2483-Wann-sind-die-Handelszeiten. Accessed 2026-10-17.
19. Trade Republic Support, "On which trading market will my orders be executed?" https://support.traderepublic.com/en-de/39-On-which-trading-market-will-my-orders-be-executed. Accessed 2026-10-17. 19b: older help page https://support.traderepublic.com/en-nl/705-On-which-trading-market-will-my-orders-be-executed (LS Exchange main, Tradegate fallback). Accessed 2026-10-17.
20. Trade Republic Support, "Which stocks can I trade at Trade Republic?" https://support.traderepublic.com/en-pt/758-Which-stocks-can-I-trade-at-Trade-Republic. Accessed 2026-10-17.
21. Finanztip, "Trade Republic: von einem zu 30 Handelsplätzen", 10 Jul 2026. https://www.finanztip.de/daily/trade-republic-von-einem-zu-30-handelsplaetzen/. Accessed 2026-10-17. (Secondary; fees and venue list to be checked in the app.)
22. Trade Republic Support, "Wie werden meine Dividenden besteuert?" https://support.traderepublic.com/fr-lu/460-Wie-werden-meine-Dividenden-besteuert. Accessed 2026-10-17.
23. gettex / Baader Bank, press release on extended trading hours, 21 Jan 2025 (seen via search result). https://gettex.de/fileadmin/user_upload/www.gettex.de/Downloads/Pressemeldungen/250121_gettex_Handelszeitverlaengerung.pdf. Accessed 2026-10-17.
24. Deutsche Börse, "Deutsche Börse Becomes Majority Shareholder in Tradegate Exchange", 30 Nov 2009. https://www.deutsche-boerse.com/dbg-en/investor-relations/announcements-and-services/press-releases/Deutsche-B-rse-Becomes-Majority-Shareholder-in-Tradegate-Exchange-to-be-Formed-in-Berlin-614848. Accessed 2026-10-17.
25. Deutsches Aktieninstitut, "Shareholder numbers 2025" (13 Jan 2026). https://www.dai.de/en/. Accessed 2026-10-17. 25b: split and 19.9 % share from press coverage of the DAI release (biallo.de, secondary): https://www.biallo.de/fonds/news/aktionaerszahlen-dai-2026/. Accessed 2026-10-17.
26. Deutsche Börse, Factsheet Prime Standard / Segment overview (seen via search result). https://www.cashmarket.deutsche-boerse.com/resource/blob/4508482/673c20fc3e0513c69ea9604583c3e3af/data/Segment%20overview%20EN.pdf. Accessed 2026-10-17.
27. BaFin, "Managers' transactions (Directors' Dealings)" (seen via search result; page not retrievable on 2026-10-17). https://www.bafin.de/EN/Aufsicht/BoersenMaerkte/Transparenz/InformationspflichtenEmittenten/DirectorsDealings/directorsdealings_artikel_en.html. Accessed 2026-10-17.
28. PwC Germany, "New reporting threshold for Directors' Dealings in Article 19 of the Market Abuse Regulation", 24 Jun 2026. https://blogs.pwc.de/en/german-tax-and-legal-news/article/255382/new-reporting-threshold-for-directors-dealings-in-article-19-of-the-market-abuse-regulation/. Accessed 2026-10-17.
29. Finanzamt NRW, "Abgeltungsteuer". https://www.finanzamt.nrw.de/steuerinfos/privatpersonen/einkuenfte-aus-kapitalvermoegen/abgeltungsteuer. Accessed 2026-10-17.
30. BZSt, "Ausländische Quellensteuer". https://www.bzst.de/DE/Service/SteuerlichesInfocenter/AuslaendischeQuellensteuer/auslaendischequellensteuer_node.html. Accessed 2026-10-17.
31. BZSt, "Anrechenbare ausländische Quellensteuer 2026" (as of 1 Jan 2026; PDF not machine-readable in this session). https://www.bzst.de/SharedDocs/Downloads/DE/EU_OECD/anrechenbare_ausl_quellensteuer_2026.pdf. Accessed 2026-10-17.
32. Finanztip, withholding tax table based on BZSt data (secondary; seen via search result). https://www.finanztip.de/indexfonds-etf/rendite-luecke/. Accessed 2026-10-17.
33. Investmentsteuergesetz (InvStG) § 20, Teilfreistellung. https://www.gesetze-im-internet.de/invstg_2018/__20.html. Accessed 2026-10-17.
34. BaFin, "Allgemeinverfügung zur Anhebung der Meldeschwelle für Eigengeschäfte von Führungskräften" (general ruling, 4 Dec 2025). https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Aufsichtsrecht/Verfuegung/vf_20251204_meldeschwelle_kraft.html. Accessed 2026-10-17.
35. Regulation (EU) 2025/2075 (amending CSDR; T+1 settlement from 11 October 2027), EUR-Lex. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R2075. Accessed 2026-10-17.
