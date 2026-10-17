# Indonesia stock market

_Last checked: 2026-10-17 · Educational content, not investment advice._

Navigation: [Markets overview](README.md) · [Trading basics](../01-trading-basics.md) · [Germany](germany.md) · [Europe](europe.md) · [USA](usa.md) · [China](china.md) · [Strategy](../strategy.md) · [APIs](../apis.md)

> **Situation as of 2026-10-17.** Indonesia is in an unusual stress phase. MSCI froze Indonesian index changes in January 2026 and on 15 October 2026 opened a consultation on moving Indonesia from "Emerging Market" to "Standalone Market" status [7][8]. One secondary report (not cross-checked) says the Jakarta index fell about 11% in one day on 16 October [9]. Treat every price level and weight in this page as a snapshot that may be out of date within days.

## 1. Overview

- **One exchange.** The *Bursa Efek Indonesia* (BEI, Indonesia Stock Exchange, IDX) was formed in December 2007 by merging the Jakarta and Surabaya exchanges [21]. It is the only stock exchange in Indonesia [23].
- **Size.** Total market capitalisation was about Rp10,695 trillion in September 2026 [3] (roughly USD 0.6 trillion; inferred, using a mid-2026 exchange rate near 17,850 IDR/USD that I did not verify against a primary source). It stood at Rp15,849 trillion at the end of 2025 and Rp9,897 trillion on 30 June 2026 [4]; the fall reflects both price declines and the rupiah (see section 4). Figures from different outlets differ in date and exchange rate.
- **Listings.** 957 listed companies at end-April 2026 [5]; a secondary report says 963 by July 2026 (unverified, not opened) [6]. IDX targets 1,100 by 2030 (unverified) [6].
- **Role.** A mid-sized emerging market: domestic-bank-heavy, commodity-linked, with a large retail investor base. It is not a core holding of most world indices (see MSCI weighting in section 7).

## 2. Exchanges and main indices

| Index | Members | What it measures | Top sectors / notes |
|---|---|---|---|
| IDX Composite (*Indeks Harga Saham Gabungan*, IHSG, JCI) | all stocks on Main and Development Boards (count not stated by IDX) [2] | Capped, free-float-adjusted market-cap-weighted price index, 9% weight cap, base 100 on 1 April 1983 [2] | Banks, coal/energy, telecom (inferred from top-10 market cap [3]) |
| LQ45 | 45 [2] | Large, liquid, fundamentally sound stocks; 15% weight cap [2] | Banks dominate (inferred) |
| IDX30 | 30 [2] | Same criteria, narrower; 15% cap [2] | Banks, telecom (inferred) |
| IDX80 | 80 [2] | Same criteria, broader; 9% cap [2] | Mixed |
| MSCI Indonesia (Standard) | 9 securities as of 30.09.2026 per justETF [16]; the Xtrackers ETF lists 10 holdings [17] | Large and mid caps, free-float adjusted, USD index | Financials about 69%, telecom 11%, materials 10% (28.08.2026) [17] |

Index membership rules were tightened in 2026: from 4 May 2026 IDX added a minimum free float, trading-day thresholds and exclusion of stocks flagged for *High Shareholding Concentration* (HSC) (unverified, from a trade-press summary of the IDX notice) [30]. IDX reviews LQ45, IDX30 and IDX80 twice a year, with interim reviews (unverified) [30].

**Largest companies by market cap, September 2026 (Rp trillion)** [3]: Bank Central Asia (BBCA) 741; DCI Indonesia (DCII, data centres) 472; Bank Rakyat Indonesia (BBRI) 471; Bayan Resources (BYAN, coal) 393; Barito Renewables Energy (BREN) 388; Bank Mandiri (BMRI) 371; Amman Mineral (AMMN, copper/gold) 327; Telkom Indonesia (TLKM) 227; Mora Telematika (MORA) 220; Dian Swastatika Sentosa (DSSA) 206. BBCA alone was about 6.9% of total market cap [3]. Note that several of the big names are tycoon-controlled groups with limited free float; that is exactly the issue MSCI is examining (section 6).

## 3. Trading hours, limits and settlement

All times are *WIB* (*Waktu Indonesia Barat*, UTC+7). Source for the schedule: IDX trading-hours page [1]. Indonesia has no daylight saving (general knowledge, not separately cited). Germany is UTC+1 (CET, winter) or UTC+2 (CEST, summer), so the gap is **6 hours in winter and 5 hours in summer**. The EU clock change on 25 October 2026 (last Sunday of October) moves the gap from 5 to 6 hours; the next change is 28 March 2027. Because Indonesia does not shift, there are no "mismatch weeks" like those with the US; there is only a one-hour shift of German-time equivalents twice a year.

| Phase | WIB Mon-Thu | WIB Friday | German time CEST (summer) Mon-Thu | German time CET (winter) Mon-Thu |
|---|---|---|---|---|
| Pre-opening (order input) | 08:45-08:57:59 | same | 03:45-03:58 | 02:45-02:58 |
| Pre-opening matching | 08:58-08:59:59 | same | 03:58-04:00 | 02:58-03:00 |
| Session I | 09:00-12:00 | 09:00-11:30 | 04:00-07:00 (Fri to 06:30) | 03:00-06:00 (Fri to 05:30) |
| Lunch break | 12:00-13:30 | 11:30-14:00 | 07:00-08:30 (Fri to 09:00) | 06:00-07:30 (Fri to 08:00) |
| Session II | 13:30-15:49:59 | 14:00-15:49:59 | 08:30-10:50 (Fri from 09:00) | 07:30-09:50 (Fri from 08:00) |
| Pre-closing input | 15:50-15:59:59 | same | 10:50-10:59 | 09:50-09:59 |
| Pre-closing matching | 16:00-16:01:59 | same | 11:00-11:02 | 10:00-10:02 |
| Post-closing | 16:02-16:15 | same | 11:02-11:15 | 10:02-10:15 |

The Friday break is longer (11:30-14:00 vs 12:00-13:30) [1]. The whole session lies in the German early morning to late morning, so most German brokers will route Indonesian trades only via a foreign or OTC-style venue, not during a typical German workday afternoon.

- **Lot size.** 1 lot = 100 shares in the regular and cash markets; the negotiated market has no round lots [1].
- **Tick size.** Rp1 below Rp200 up to Rp25 at Rp5,000 and above [1].
- **Auto rejection (*Auto Rejection*, price limits).** Valid from 28 September 2026 on the Main, New Economy and Development Boards: Rp1-Rp10 moves by Rp1; Rp11-Rp200 up 35% / down 15%; above Rp200 to Rp5,000 up 25% / down 15%; above Rp5,000 up 20% / down 15%. On the Acceleration and Watchlist Boards: 10% up and down above Rp10 [1].
- **Index circuit breaker.** A 30-minute halt if the IHSG falls more than 8%, another at 15%, and suspension at 20% (duration disputed between sources; check IDX text) [24]. Halts were triggered in late January 2026 [26].
- **Watchlist Board and full call auction.** Stocks with unusual market activity or weak fundamentals can be moved to the *Papan Pemantauan Khusus* / Watchlist Board, where trading runs as a Full Call Auction in hourly sessions (09:00-09:55, 10:00-10:55 ... with a break 12:00-14:00 Mon-Thu) [1][29]. The call-auction mechanism was introduced from 25 March 2024 (unverified, secondary) [29].
- **Settlement.** T+2 in the regular market, T+0 in the cash market [1].
- **Short selling.** Allowed only for listed securities and via licensed members; intraday short sales need no borrowing [1].
- **Holidays.** IDX publishes an annual trading-holiday calendar on idx.id; Indonesia also has *cuti bersama* (collective leave days) that close the exchange (calendar not fetched here).

## 4. Currency and FX risk

Shares trade and settle in Indonesian rupiah (IDR) [21]. A euro investor holds IDR exposure and, via USD-based funds, also USD/EUR exposure. The rupiah weakened roughly 8% in 2026 according to a secondary report [9]; Bank Indonesia says it is committed to stability [9]. Market-cap data above fell much more than the currency alone (from Rp15,849 trillion to Rp9,897 trillion, H1 2026) [4], so the currency is a secondary but additive driver. Dividend payments are converted from IDR; the ETFs discussed below are denominated in USD and currency-unhedged [17].

## 5. Regulator and investor protection

- **OJK** (*Otoritas Jasa Keuangan*, Financial Services Authority) supervises the capital market; it took over from Bapepam-LK on 1 January 2013 [21].
- **IDX** is the exchange and a self-regulatory organisation; **KSEI** (*Kustodian Sentral Efek Indonesia*) is the central securities depository (C-BEST system, Single Investor Identification SID) [22]; **KPEI** (*Kliring Penjaminan Efek Indonesia*) is the clearing and guarantee institution [21].
- **2026 reform package** (OJK/IDX/KSEI, 2 April 2026): public disclosure of holders above 1%; HSC announcements on the IDX site; KSEI data split into 39 investor classifications; minimum free float raised to 15% via IDX Regulation I-A, effective 31 March 2026, with a transition period [10]. Beneficial-ownership data for holders of 10% or more is non-public [10].
- **Disclosure.** Company announcements, financial statements and the stock list are on idx.id; KSEI publishes securities ownership statistics on ksei.co.id [22].
- **Investor protection.** I did not verify whether Indonesia has a deposit-insurance-like investor compensation scheme (open question). An investor who holds shares through a German broker is not a direct Indonesian account holder (see section 7).

## 6. Market characteristics and specific risks

- **Concentration.** Banks plus a handful of conglomerate-linked commodity stocks dominate. The MSCI Indonesia index had about 69% financials and the top holding near 31% (28.08.2026) [17].
- **Free float and ownership opacity.** MSCI cited opaque shareholding and suspected coordinated trading [8]. IDX data suggest hundreds of issuers did not yet meet the 15% free-float requirement (unverified, trade press) [34].
- **MSCI freeze and reclassification risk.** Since January 2026 MSCI has frozen foreign inclusion factors, additions and size-segment migration, and deletes HSC-flagged stocks [7][8]. On 15 October 2026 it proposed reclassifying Indonesia to Standalone status; feedback is accepted until 30 April 2027 and the decision is due by 30 June 2027 [8]. Funds tracking MSCI Emerging Markets could be forced sellers if it goes ahead [9]. A single-day fall of about 11% was reported on 16 October 2026 (single secondary source, unverified) [9].
- **Drawdown.** The IHSG fell from 8,646 (end 2025) to 5,643 (30 June 2026), -34.7% [27]; a secondary report says it was about 39% down by 16 October (single secondary source, unverified) [9].
- **Foreign flows.** Foreign institutions held about 36% of market cap in mid-June 2026 per KSEI data [25]. Offshore funds net-sold about Rp67 trillion (USD 3.7 billion) by mid-June [25]; one report says USD 4.9 billion net outflow in 2026 by mid-October [9].
- **Retail vs institutional.** Retail participation is large (the investor count surpassed 21 million, per trade press, unverified) [25]. Local speculative behaviour in small caps is a recognised issue (inferred).
- **Political/regulatory risk.** Reform enforcement is "unproven" in MSCI's view [8]. Foreign-ownership limits depend on sector; I did not verify specific caps (open question).

## 7. Access from Germany via Trade Republic

**Direct access to the IDX (rupiah, Jakarta hours) from Trade Republic is not documented anywhere I could find, and Trade Republic's help page does not name Indonesia [18]; treat it as unavailable unless the app shows otherwise (unverified, could not open the in-app list).** What I could verify:

- Trade Republic's help pages give different counts (more than 6,500 international stocks; up to about 7,500 stocks in total); check the app. The help page [18] refers to stocks from Europe, North America and Asia and to the app's stock browser and partner L&S Exchange for the list (help-centre text that may predate the July 2026 change); Indonesia is not named. **Whether any given Indonesian share is offered must be checked in the app; I could not verify it.**
- **German secondary quotations exist.** Telkom Indonesia (ISIN ID1000129000, WKN A1W4LG) quotes in EUR at L&S Exchange (about EUR 0.11, 16 October) [19] and at Stuttgart, Frankfurt and gettex [20]. Such quotations are typically traded OTC-style off a market maker and may have wide bid/ask spreads (the L&S quote showed a ~21% spread on a EUR 0.11 price [19]; inference: illiquid, check before trading).
- **ADRs.** Telecommunications Indonesia (TLK) has a NYSE-listed ADR via BNY Mellon; the ratio was 200 shares per ADS from September 2013 [31] and a broker page now says 100 (unverified) [32]. I could not confirm other large Indonesian ADRs.
- **UCITS ETFs.** Category: single-country *MSCI Indonesia* ETFs. Examples (not recommendations; availability and savings-plan eligibility must be checked in the app): HSBC MSCI Indonesia UCITS ETF (IE00B46G8275, full replication, TER 0.50%); Amundi MSCI Indonesia UCITS ETF Acc (LU1900065811, swap, TER 0.45%); Xtrackers MSCI Indonesia Swap UCITS ETF 1C (LU0476289623, swap, TER 0.65%) [16]. Fund sizes were EUR 202 m, 160 m and 49 m (30.09.2026) [16]. The 1-year index return was -34% and the 3-year -51% [16]. ETF with swap replication carries counterparty risk; all three are USD-denominated. No UCITS ETF tracking ASEAN was found; an Italian guide says none exists (secondary) [33]. If MSCI reclassifies Indonesia to Standalone, the MSCI Indonesia index may continue to exist but its use in EM funds would drop (inference).

## 8. Taxes specific to this market

- **Indonesian withholding tax on dividends to non-residents.** The domestic rate is **20%** (Article 26, "PPh 26") [13]. Without a certified certificate of domicile (CoD), 20% applies even if a treaty exists [13].
- **Germany-Indonesia treaty** (signed 30 October 1990, in effect 1991 per the official text): **15%** of the gross amount for the beneficial owner generally, **10%** if the recipient is a company directly holding at least 25% [11][12]. A private investor gets 15%.
- **Sale proceeds.** Indonesian exchange sales are subject to a 0.1% final income tax on proceeds, under certain treaties not due (unverified applicability for German residents) [14].
- **Documentation.** Treaty relief needs a DGT form and a CoD certified by the home tax office, and under Regulation PMK 112/2025 (effective 30 December 2025) the withholding agent must verify entitlement; failure means 20% (secondary advisory sources, official text not read) [13][15].
- **Credit in Germany.** For private investors, the German *Abgeltungsteuer* (flat 25% plus solidarity surcharge) credit covers only foreign tax that was assessed, paid and cannot be reduced under the treaty or domestic law of the source state (§ 32d Abs. 5, § 43a Abs. 3 EStG) [28]. So **only 15% is creditable**; the extra 5 percentage points (20% minus 15%) must be reclaimed from the Indonesian tax office (DGT). The reclaim procedure, forms and deadlines were **not verified** (open question). Whether Trade Republic withholds at 15% or 20% for Indonesian dividends is also **not verified**.

## 9. Useful official data sources

- IDX: idx.id (listings, announcements, indices, trading-hours page [1], index guides [2]).
- OJK: ojk.go.id and the Investor Relations Unit iru.ojk.go.id [10].
- KSEI: ksei.co.id (ownership statistics, registered securities) [22].
- Tax: pajak.go.id (treaty text [11], treaty rate table [12]).
- Index provider: MSCI index consultations and announcements (msci.com) [7][8].
- German side: BZSt overview of creditable foreign withholding tax (not fetched; see [28]).

## Sources

1. Trading Hours and Mechanism, Indonesia Stock Exchange (IDX). https://www.idx.id/en/products-services/trading-hours-and-mechanism/ , accessed 2026-10-17.
2. Index, IDX. https://www.idx.id/en/products/index/ , accessed 2026-10-17.
3. "BBCA the largest stock by market capitalization on the IDX, September 2026", Databoks Katadata (citing IDX). https://databoks.katadata.co.id/en/market/statistics/6ac6f65732605/bbca-the-largest-stock-by-market-capitalization-on-the-idx-september-2026 , accessed 2026-10-17 (secondary).
4. "Indonesia's stock market capitalization declined in H1 2026", Databoks Katadata. https://databoks.katadata.co.id/en/market/statistics/6a584da19d1dc/indonesias-stock-market-capitalization-declined-in-the-h1-2026 , accessed 2026-10-17 (secondary).
5. "Listed companies on the IDX remained relatively stagnant through April 2026", Databoks Katadata. https://databoks.katadata.co.id/en/market/statistics/6a24e09f528c8/listed-companies-on-the-idx-remained-relatively-stagnant-through-april-2026 , accessed 2026-10-17 (secondary).
6. "Indonesia Stock Exchange saw seven listing while four IPO await as of July 2026", Business Today Malaysia. https://www.businesstoday.com.my/2026/07/12/indonesia-stock-exchange-saw-seven-listing-while-four-ipo-await-as-of-july-2026/ , from search snippet only, accessed 2026-10-17 (secondary, unverified).
7. "Update on free float assessment of Indonesian securities" (20 April 2026), MSCI. https://app2.msci.com/webapp/index_ann/DocGet?pub_key=L%2FzT8OMvlCI%3D&lang=en&format=html , accessed 2026-10-17.
8. "MSCI launches a consultation on a proposal to reclassify Indonesia from Emerging Market to Standalone Market status" (15 October 2026), MSCI, as reproduced by MarketScreener (the MSCI PDF itself at https://www.msci.com/downloads/documents/press-releases/media-room/Indonesia_PR_Oct_26.pdf could not be read as text). https://www.marketscreener.com/news/msci-launches-a-consultation-on-a-proposal-to-reclassify-indonesia-from-emerging-market-to-standalon-ce785dd3d180fe2c , accessed 2026-10-17.
9. "Indonesian stocks plunge 11% as MSCI reviews emerging market status", IndexBox (16 October 2026). https://www.indexbox.io/blog/indonesian-stocks-plunge-11-as-msci-reviews-emerging-market-status/ , accessed 2026-10-17 (secondary, single source; not cross-checked against Reuters/Bloomberg).
10. "OJK, IDX, and KSEI complete four agenda items for Indonesia capital market transparency reform" (2 April 2026), OJK Investor Relations Unit. https://iru.ojk.go.id/iru/WebSite/ArticleList/View/978_OJK,_IDX,_and__KSEI_Complete_Four_Agenda_Items_for_Indonesia_Capital_Market_Transparency_Reform , accessed 2026-10-17.
11. Agreement between the Federal Republic of Germany and the Republic of Indonesia for the avoidance of double taxation (signed 30.10.1990), Directorate General of Taxes (DGT). https://www.pajak.go.id/en/node/115866 , accessed 2026-10-17.
12. Tax treaty rates (Germany row), DGT. https://www.pajak.go.id/en/tax-treaty-rates , accessed 2026-10-17.
13. Indonesia: Corporate - Withholding taxes, PwC Worldwide Tax Summaries. https://taxsummaries.pwc.com/indonesia/corporate/withholding-taxes , accessed 2026-10-17.
14. Indonesia: Individual - Other taxes, PwC Worldwide Tax Summaries. https://taxsummaries.pwc.com/indonesia/individual/other-taxes , accessed 2026-10-17.
15. "Indonesia's PMK No. 112 of 2025: procedures for implementing double taxation avoidance agreements", Alvarez & Marsal. https://www.alvarezandmarsal.com/thought-leadership/indonesia-s-pmk-no-112-of-2025-procedures-for-implementing-double-taxation-avoidance-agreements , accessed via search snippet only 2026-10-17 (secondary; page returned 403).
16. "Investieren in Indonesien mit ETFs", justETF (data as of 30.09.2026). https://www.justetf.com/de/how-to/invest-in-indonesia.html , accessed 2026-10-17.
17. Xtrackers MSCI Indonesia Swap UCITS ETF 1C (LU0476289623) profile, justETF. https://www.justetf.com/en/etf-profile.html?isin=LU0476289623 , accessed 2026-10-17.
18. Which stocks can I trade at Trade Republic?, Trade Republic Help Centre. https://support.traderepublic.com/en-de/1347-Which-stocks-can-I-trade-at-Trade-Republic , accessed 2026-10-17.
19. PT Telekom Indonesia, L&S Exchange tradecenter page. https://www.ls-tc.de/de/aktie/351621 , accessed 2026-10-17.
20. Telkom Indonesia, ISIN ID1000129000, comdirect. https://www.comdirect.de/inf/aktien/ID1000129000 , search snippet only, accessed 2026-10-17 (secondary).
21. Market infrastructure Indonesia, Clearstream. https://clearstream.com/clearstream-en/res-library/market-coverage/market-infrastructure-indonesia-1281038 , accessed 2026-10-17.
22. About KSEI, overview, PT Kustodian Sentral Efek Indonesia. https://www.ksei.co.id/en/about-ksei/overview , accessed 2026-10-17.
23. Cross-border listings guide, Indonesia Stock Exchange overview, Baker McKenzie. https://resourcehub.bakermckenzie.com/en/resources/cross-border-listings-guide/asia-pacific/indonesia-stock-exchange/topics/overview-of-exchange , search snippet only, accessed 2026-10-17 (states IDX is the only stock exchange in Indonesia).
24. "IDX adjusted rules on lower limit of auto rejection and rules on temporary halt on securities trading", ASEAN Exchanges. https://www.aseanexchanges.org/content/idx-adjusted-rules-on-lower-limit-of-auto-rejection-and-rules-on-temporary-halt-on-securities-trading/ , search snippet only, accessed 2026-10-17 (secondary).
25. "Indonesia masih jadi tujuan investasi asing" and related reports citing KSEI/JPMorgan, Investortrust.id; "Investors surpassed 21 million", IDNFinancials. https://investortrust.id/business/106386/indonesia-masih-jadi-tujuan-investasi-asing , https://www.idnfinancials.com/videos/watch/2329/investors-surpassed-21-million-idx-market-cap-fallen-5-1 , search snippets only, accessed 2026-10-17 (secondary).
26. "Indonesian stocks plunge 7% after MSCI warning on investability" (28 January 2026), Bloomberg. https://www.bloomberg.com/news/articles/2026-01-28/msci-halts-indonesia-index-changes-flags-transparency-risks , search snippet only, accessed 2026-10-17.
27. "Indonesia stocks suffer world's worst first-half slump as OJK addresses MSCI concerns", Investortrust.id. https://investortrust.id/market/108025/indonesia-stocks-suffer-worlds-worst-first-half-slump-as-ojk-addresses-msci-concerns , search snippet only, accessed 2026-10-17 (secondary).
28. "Auslandserträge - Anrechnung der Quellensteuer mit DBA-Staaten auf die Abgeltungsteuer", IWW (summarising §§ 32d, 43a EStG and BZSt notes). https://www.iww.de/astw/archiv/-auslandsertraege--anrechnung-der-quellensteuer-mit-dba-staaten-auf-die-abgeltungsteuer-f61914 , search snippet only, accessed 2026-10-17 (secondary).
29. "IDX Full Call Auction", CLSA (March 2024). https://clsa.com/wp-content/uploads/2024/03/IDX-Full-Call-Auction.pdf , PDF not readable as text; and Rajah & Tann Asia, "IDX tightens supervision ... Watchlist Board" (24 July 2023), https://www.rajahtannasia.com/viewpoints/idx-tightens-supervision-on-listed-companies-with-the-introduction-of-the-watchlist-board/ , accessed 2026-10-17.
30. "Reflecting market dynamics, IDX adjusts evaluation criteria for IDX30, LQ45 and IDX80 indices", ASEAN Exchanges. https://www.aseanexchanges.org/content/reflecting-market-dynamics-idx-adjusts-evaluation-criteria-for-idx30-lq45-and-idx80-indices/ , search snippet only, accessed 2026-10-17 (secondary).
31. Form 424B3, Telecommunications Indonesia /ADR/ (BNY Mellon, ADS ratio change 2013), SEC EDGAR. https://www.sec.gov/Archives/edgar/data/0001002486/000120193513000050/memo424b3pttelkom.txt , search snippet only, accessed 2026-10-17.
32. TLK quote page ("ADR Rep 100 Series B"), Fidelity. https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol=TLK , search snippet only, accessed 2026-10-17 (secondary).
33. "Migliori ETF Sud-Est Asiatico (ASEAN)", FiscoInvestimenti (June 2026). https://fiscoinvestimenti.it/?p=13858 , search snippet only, accessed 2026-10-17 (secondary).
34. "Hundreds of issuers yet to meet required free float, IDX eyes roadshow", IDNFinancials. https://www.idnfinancials.com/news/65890/ratusan-emiten-belum-penuhi-free-float-bei-siapkan-roadshow , search snippet only, accessed 2026-10-17 (secondary).
