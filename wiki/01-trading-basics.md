# Trading basics

_Last checked: 2026-10-17 · Educational content, not investment advice._

Navigation: [Index](README.md) · [Markets overview](markets/README.md) · [Strategy](strategy.md) · [APIs](apis.md)

This page explains how trading works for a private investor living in Germany who uses the broker Trade Republic (TR). It covers instruments, how an order is executed, costs, risk, German tax, and TR specifics. It describes mechanisms and evidence only. It does not recommend any product.

Trade Republic changed its trading set-up in July 2026 after the EU ban on payment for order flow [19][43]. Many third-party guides still describe the older single-venue model. Where a fact comes only from press reports and not from a TR document, it is marked.

> Tip: check availability in the app. Fees, venues, interest rates and product lists change often. The binding price list (*Preis- und Leistungsverzeichnis*) is in the TR app under Documents [3].

---

## 1. Instruments

| Instrument | What it is | Main risk | Offered by TR? |
|---|---|---|---|
| Shares (*Aktien*) | Ownership stake in a company | Company-specific loss, up to total loss | Yes; Trade Republic's help pages give different counts (more than 6,500 international stocks; up to about 7,500 stocks in total); check the app [1] |
| ETFs (UCITS) | Exchange-traded fund that tracks an index; UCITS means it follows the EU fund rulebook | Market risk of the index | Yes; "more than 2,000 ETFs" [8] |
| ETCs / ETNs | Exchange-traded commodities / notes: debt securities that track a commodity or index. The issuer's credit risk applies. | Issuer default, commodity price risk | Not confirmed in the sources I found (unverified); check in the app |
| Bonds (*Anleihen*) | Loans to a government or company with fixed interest | Interest-rate risk, default risk | Yes; EUR bonds via LS Exchange, USD bonds via Walter Ludwig [1] |
| Funds (*Fonds*) | Pooled investments; actively managed funds are different from ETFs | Market risk plus higher fees | Classic funds not confirmed (unverified). TR holds cash above a threshold in money-market funds (see section 6) [41] |
| Derivatives | Products whose value depends on an underlying | Total loss, leverage | Yes: warrants, knock-out products, factor certificates; about 380,000 from HSBC, Societe Generale, UBS, Vontobel [6] |
| Crypto | Digital assets | Very high volatility, custody risk | Yes; "more than 50" coins [1][15] |

### Derivatives in short

- **Warrants** (*Optionsscheine*): the right, not the duty, to buy or sell an underlying at a set price. They lose value as expiry nears and can expire worthless [6].
- **Knock-out certificates** (*Knock-outs*): leveraged products with a barrier. If the underlying touches the barrier, the product is "knocked out" and removed from the depot [7]. Illustration with 10x leverage: a 10% adverse move in the underlying wipes out the stake (simple arithmetic, not a TR figure).
- **Factor certificates**: leveraged with a fixed daily factor. They compound daily, so they can lose value even when the underlying ends flat after a volatile path.
- **CFDs** (contracts for difference): leveraged contracts with a broker or provider. ESMA found that 74 to 89 percent of retail CFD accounts lost money [28] and capped leverage from 30:1 (major currency pairs) down to 2:1 (crypto) [27]. I found no CFD offer at TR (unverified).

TR's own help text calls knock-outs speculative and short-term [6][7]. Derivatives are traded over the counter (OTC) directly with the issuers, not on an exchange [1].

---

## 2. How an order works

### Bid, ask, spread

Every tradable instrument has a **bid** (the price buyers offer) and an **ask** (the price sellers want). The gap is the **spread** (*Spanne*). A market buyer pays the ask and a market seller receives the bid, so the spread is a cost even when the broker charges no commission. TR lists spreads as an extra cost next to the flat fee [3].

### Market maker vs exchange

- An **exchange** brings buyers and sellers together in an order book.
- A **market maker** quotes both prices itself and takes the other side of your trade. The venue LS Exchange (Lang & Schwarz) works this way.
- **Payment for order flow (PFOF)** means a market maker pays the broker for routing orders. The EU ban applies in Germany from 1 July 2026 (Germany had used an exemption until 30 June 2026) [19][43].

### Trading venues at Trade Republic (verified 2026-10-17, partly press-only)

| Product | Venue or counterparty | Source |
|---|---|---|
| Shares and ETFs, "Bestpreis" | An algorithm compares prices across relevant exchanges and routes the order | [1] |
| Shares and ETFs, "Direktpreis" | You pick one venue from TR's list of global venues | [1] |
| EUR bonds, fixed-term deposits | LS Exchange (LSX) | [1] |
| USD bonds | Walter Ludwig | [1] |
| Derivatives | OTC with HSBC, Societe Generale, UBS, Vontobel | [1] |
| Crypto | Tradias | [1] |
| Savings plans | XETRA hours, 09:00 to 17:30 CET [5] | [5] |

Since July 2026, shares and ETFs have two modes. **Bestpreis** (default, EUR 1 per order): Trade Republic is the counterparty and prices against up to about 30 venues. **Direktpreis**: you choose a venue (press reports name Xetra, Tradegate, LS Exchange, Nasdaq, NYSE and Euronext) for EUR 2 per order plus external costs (Stiftung Warentest, Finanztip; not shown on Trade Republic's help pages as of 2026-10-17) [19][47]. LS Exchange remains the venue for EUR bonds [1]. Xetra is the only additional German exchange; Finanztip also lists Tradegate and LS Exchange as Direktpreis venues [47]. TR's own help page does not list the venues [1]. TR received a BaFin permit for its own multilateral trading facility (MTF) in January 2026, reported by a secondary source [37]. Whether TR uses it is not confirmed (unverified). Standard Bestpreis trading hours are 07:30 to 23:00 CET on weekdays; Direktpreis hours follow the chosen venue [39].

### Order types

| Type | Meaning | TR detail |
|---|---|---|
| Market order | Buy or sell at the next available price; the displayed price is only an indication | Cannot be placed outside trading hours [2] |
| Limit order | Buy at your limit or lower, sell at your limit or higher | Valid for the day or 360 days [2] |
| Stop order (stop-loss) | Becomes active when the price reaches the stop level, then executes at market | TR warns it cannot guarantee that the market maker accepts it [2] |
| Stop-limit | A stop that triggers a limit order instead of a market order | Not listed in the TR help text I read [2] (unverified) |

A stop-loss is not a guarantee. In a gap or a fast market the fill can be far below the stop price.

### Settlement

After execution the securities and cash are exchanged at the central securities depository. In the EU, standard settlement is **T+2**, meaning two business days after the trade date. Regulation (EU) 2025/2075 moves the EU to **T+1 from 11 October 2027** [45], following ESMA's proposal [29]. The US has used T+1 since 28 May 2024 [30]. As a private investor you see the position immediately; settlement matters mainly for dividend record dates and for selling just after buying.

### Fractional shares and savings plans

- **Fractional shares** (*Bruchstuecke*): you can buy by amount, from 1 EUR, and by quantity up to 6 decimals. Market orders only. The help page says execution runs on LS Exchange with TR as counterparty and that a sale can take up to 2 days [4]. That page may predate the July 2026 change (check in the app).
- **Savings plan** (*Sparplan*): recurring automatic purchases. Intervals are weekly, biweekly, monthly or quarterly. Plans start on the 2nd or the 16th of a month and execute during XETRA hours [5]. A plan only executes when enough cash is on the account, so TR suggests a direct debit [5].

---

## 3. Costs

| Cost | Trade Republic (as of 2026-10-17) |
|---|---|
| Order commission | None, regardless of order size [3] |
| Flat external cost (*Fremdkostenpauschale*) per trade | 1 EUR per transaction, savings plans excluded [3][19] |
| "Direktpreis" (choose your venue) | 2 EUR per order plus external costs, per press reports; not shown on the TR pages I could open (unverified) [19] |
| Savings plan execution | 0 EUR [5][19] |
| Fractional trades | 1 EUR per buy and per sell; selling the leftover fraction with a market order after the whole shares costs nothing [4] |
| Custody | No custody fee (unverified) |
| Spread | Varies by instrument and moment; no fixed number [3] |
| Third-party costs | E.g. inducements and ETF management fees [3] |
| Foreign-currency conversion | Debits at the sell rate, credits at the buy rate; the USD margin is listed as 0.0014 [17] |
| Crypto | 1 EUR per transaction per an older help text (verify) [15] |

About FX: the help page does not state the unit of the margin. Compared with typical exchange rates it looks like roughly 0.1 percent (my inference, unverified) [17]. Whether this applies to a trade on a US venue under Bestpreis is not stated.

### Worked example: a 1 EUR flat fee

A fee is charged on the buy and on the sell, so a round trip costs 2 EUR with the standard fee (at least 4 EUR with Direktpreis, plus external costs, if the 2 EUR is confirmed).

| Order size | Fee per trade | Round trip, % of stake (1 EUR each way) | Round trip with 2 EUR each way |
|---|---|---|---|
| 25 EUR | 4.00% | 8.00% | 16.00% |
| 50 EUR | 2.00% | 4.00% | 8.00% |
| 500 EUR | 0.20% | 0.40% | 0.80% |
| 5,000 EUR | 0.02% | 0.04% | 0.08% |

Reading it: on a 50 EUR stake that earns 5% in a year (2.50 EUR), a 2 EUR round trip removes 80% of the gain before spread. The same logic is why free savings plans are cheap for small monthly amounts [5]. All figures here are my own arithmetic from the 1 EUR fee [3].

Fund costs: the **TER** (total expense ratio) is charged inside the fund and is not billed to you as a line item, so it is easy to overlook. Check each ETF's key information document (KID) for the TER.

---

## 4. Risk basics

- **Volatility**: how much prices move around their average. Higher volatility means a wider range of outcomes, including losses.
- **Drawdown** (*Kursrueckgang*): the fall from a peak to a later trough.
  - MSCI World: a maximum drawdown of 57.46% from 2007-10-31 to 2009-03-09, as listed in the MSCI factsheet (I could not open the PDF directly; the figure comes from the factsheet as quoted by a search result) [31].
  - S&P 500: a fall of 56.8% from 9 October 2007 to 9 March 2009 [32].
  - Recovery arithmetic: after a 57.46% loss you need roughly +135% to get back to the old level (own calculation: 1 divided by 0.4254).
- **Diversification**: spreading money across many holdings so one failure does not dominate. It lowers company-specific risk but not market risk.
- **Currency risk**: a US stock priced in USD changes in value for a EUR investor when EUR/USD moves, on top of the stock price.
- **Concentration**: a large share of wealth in one stock, sector or country.
- **Leverage**: borrowing or derivative gearing multiplies gains and losses. Knock-outs and CFDs are examples (section 1).
- **Compounding**: returns earn returns. Illustration only, not a forecast: 200 EUR per month for 30 years at a constant 5% a year grows to about 163,000 EUR on 72,000 EUR paid in (own calculation, monthly compounding). Real returns are uneven, and a bad early decade changes the outcome.
- **Sequence and behaviour**: selling in a crash locks in the loss. Costs and taxes also reduce compounding.

---

## 5. German tax

TR is a German bank, so it acts as the withholding agent (*Abzugsverpflichteter*). It withholds the tax on capital income automatically for German taxpayers and reports it in the annual tax report (*Jahressteuerbescheinigung*) in the app under Profile > Taxes [13]. Crypto is the exception (see below).

### Rates

| Component | Rate | Source |
|---|---|---|
| Flat withholding tax (*Abgeltungsteuer*) | 25% | [22] |
| Solidarity surcharge (*Solidaritaetszuschlag*) | 5.5% of the tax, no allowance on this tax | [25] |
| Church tax (*Kirchensteuer*), if you are a member | 8% of the tax in Baden-Württemberg and Bavaria, 9% in the other states | [46] |
| Combined without church tax | 26.375% (25% x 1.055, own calculation) | [22][25] |
| Combined with church tax 9% / 8% | about 27.99% / 27.82% (own calculation: the 25% is reduced by 25% of the church tax, see [22]) | [22] |

### Allowance and exemption order

The saver's allowance (*Sparer-Pauschbetrag*) is 1,000 EUR per person and 2,000 EUR for spouses assessed jointly [21]. An exemption order (*Freistellungsauftrag*) tells the bank to leave income up to that amount untaxed. You can split the total across banks, but not exceed it. TR manages it in the app. If you set it up during the year, taxes already paid in that year are refunded within 1 to 2 working days [42]. The exemption order does not cover foreign withholding tax [42].

### Loss pots (*Verlustverrechnungstoepfe*)

TR creates two pots per depot [12]:

- **Shares pot** (*Aktienverlusttopf*): losses from selling shares. Offsettable only against gains from selling shares [21].
- **General pot** (*sonstige Verluste*): all other losses. Offsettable against ETF/fund income, dividends, interest and similar [12].

Balances carry forward automatically. By 15 December you can request a loss certificate (*Verlustbescheinigung*) that zeroes the pots so you can offset the loss against gains at another bank via the tax return [12].

### Funds and ETFs

- **Partial exemption** (*Teilfreistellung*): equity funds 30%, mixed funds 15%, domestic real-estate funds 60%, foreign real-estate funds 80% of income is tax-free for private investors [23]. Example: 1,000 EUR gain on an equity ETF is taxed on 700 EUR; at 26.375% that is about 184.63 EUR, an effective 18.46% (own calculation).
- **Advance lump sum** (*Vorabpauschale*): an accumulating fund pays no distribution, so the law taxes a notional minimum yearly. The base income is the value at the start of the year times 70% of the base rate (*Basiszins*), capped at the year's price gain plus distributions, and reduced by 1/12 for each full month before purchase [24]. The base rate for 2026 is 3.20% (BMF letter of 13 January 2026, via a secondary summary) [26]. The tax is deemed received on the first working day of the following year [24]. Example (own calculation): 10,000 EUR value at the start of the year x 3.20% x 0.7 = 224 EUR; after 30% partial exemption 156.80 EUR is taxable; the tax is about 41.35 EUR at 26.375%, or 0 if your allowance still covers it. The bank has to collect it from your cash account; confirm how TR handles it in the app (unverified).

### Foreign withholding tax

Foreign countries withhold tax at source on dividends. The US standard rate is 30%. TR is a Qualified Intermediary with the US tax authority, so US dividends are reduced by 15% directly [14]. I found no W-8BEN step in TR's help pages (unverified). The paid foreign tax appears in the annual tax report and in a separate pot in the tax overview [13][14]. German law credits foreign tax against the German flat tax up to 25% per income item, in practice limited by the double-taxation treaty rate [35]. Rough result for a US dividend: 15% US + about 10.55% German (25% minus the 15% credit, plus Soli on the remainder), about 25.55% in total (own calculation, unverified in detail). Because the credit works against German tax actually due, a dividend covered fully by your allowance may not use up the foreign tax (secondary-level reasoning, unverified). Foreign tax above the treaty rate is not credited [35].

### When is the tax return (Anlage KAP) still needed?

Withholding is normally final (*Abgeltungswirkung*). You still use form Anlage KAP when, for example [38]:

1. You want a more favourable comparison against your personal rate (*Guenstigerpruefung*), useful if your total taxable income is low [22].
2. You need to offset losses across banks (loss certificate, section 5).
3. Church tax was not withheld although you owe it.
4. Income was not taxed at source, e.g. at a foreign broker.

Crypto and some ETC gains are declared manually: TR does not deduct tax on crypto, and gains within the one-year holding period are taxable at the personal rate, with gains up to a 1,000 EUR exemption limit (*Freigrenze*) tax-free [15]. Gains from ETCs with physical delivery and "other" income such as Saveback are also manual [13].

> Tip: tax rules change. Check the BMF and your tax adviser, and use the TR annual tax report as the primary source for your own numbers.

---

## 6. Trade Republic specifics

- **Licence**: Trade Republic Bank GmbH is a German bank. Secondary sources report that it obtained a full banking licence in December 2023 [36]. Supervision is by BaFin and the ECB.
- **Cash and deposit protection**: customer cash sits in pooled trust accounts at partner banks (the help page lists eight, including Citibank Europe, Deutsche Bank, J.P. Morgan SE). Cash is covered by the partner banks' deposit protection up to 100,000 EUR per customer [9]. The help text and the licence reports do not fully match (trust accounts at partner banks vs a bank licence); check the current set-up in the app (unverified).
- **Money-market funds**: a search excerpt of TR's help page says larger balances are spread into money-market funds, which are held as segregated assets and are not covered by deposit protection. The threshold amount was not found (unverified) [41].
- **Securities**: shares, ETFs and bonds remain your property, are not covered by deposit protection, and are held in central securities depositories via TR [9].
- **Interest on cash**: 2.5% a year on cash, advertised on TR's German page (undated; other country pages show other rates) [11]. Interest is calculated daily and paid out monthly; amounts reserved for limit orders still earn interest [10]. Interest is taxable capital income.
- **Crypto**: custody is with BitGo Europe GmbH in Germany [16]. TR announced MiCAR authorisation in November 2025 [40]. Crypto is not covered by deposit protection (an older customer agreement says no statutory compensation scheme applies; may be outdated) [44].
- **Why US-domiciled ETFs are not available**: since 2018 the EU PRIIPs regulation requires a key information document (KID) with a prescribed format, including performance scenarios. US-domiciled ETFs generally lack one, so EU retail investors cannot buy new units [33][34]. UCITS ETFs have a KID, which is why TR's list consists of EU-domiciled products (my inference from the ETF list [8]).
- **Saveback**: TR's help page for the card describes 1% of card spending invested in a savings plan, with a cap of 15 EUR per month and a minimum of 50 EUR in savings plans per month [18]. Another help page mentions a crypto variant (30 EUR cap), so terms differ by date and region (unverified). **Round up** (investing the change up to the next euro) is described on the card page, not verified here. Check availability in the app.
- **App-only**: access is through the mobile app. A web terminal for experienced investors with charts and data was announced in July 2026 at no extra charge [19].
- **What you cannot do**: I found no direct short selling at TR; the help centre points to bear/short derivative products instead (partly unverified) [6]. I found no exchange-traded options (e.g. calls and puts on Eurex) in TR's lists, only issuer warrants, knock-outs and factor certificates (inference, unverified) [6]. I found no CFDs at TR (unverified).

> Tip: check availability in the app. Venue list, Direktpreis fee, interest rate, Saveback terms and product universe are the items that change most.

---

## 7. Glossary

| Term | Meaning |
|---|---|
| Ask / bid | Lowest price a seller accepts / highest price a buyer offers |
| Spread | Difference between ask and bid; a hidden cost |
| Market maker | Firm that quotes buy and sell prices and trades against you |
| PFOF | Payment for order flow: market maker pays the broker for orders; banned in the EU, in Germany from 1 July 2026 |
| Limit order | Order with a price limit |
| Stop order | Order that triggers when a stop price is reached |
| T+2 / T+1 | Settlement two / one business days after the trade |
| UCITS | EU rulebook for retail-eligible funds and ETFs |
| KID / PRIIPs | Key information document required for packaged retail products |
| TER | Total expense ratio: yearly fund cost inside the fund |
| Accumulating / distributing | ETF that reinvests income / pays it out |
| Knock-out | Leveraged certificate that ends when a barrier is touched |
| CFD | Contract for difference: leveraged contract, high loss rate for retail |
| Drawdown | Fall from a peak to a later low |
| Diversification | Spreading risk over many holdings |
| *Abgeltungsteuer* | Flat 25% tax on capital income, withheld by the bank |
| *Sparer-Pauschbetrag* | Annual tax-free allowance for capital income (1,000 / 2,000 EUR) |
| *Freistellungsauftrag* | Instruction to the bank not to withhold tax up to the allowance |
| *Teilfreistellung* | Part of fund income that is tax-free (30% for equity funds) |
| *Vorabpauschale* | Notional yearly tax base for accumulating funds |
| *Verlustverrechnungstopf* | Bank-level pot that tracks realised losses for offsetting |
| Withholding tax (*Quellensteuer*) | Tax taken at source by the dividend's country |
| Savings plan (*Sparplan*) | Recurring automatic purchase |

---

## Sources

All accessed 2026-10-17. Items marked "(search excerpt)" were read as a snippet in a search result, not as a full page.

1. Orderausfuehrung (Order execution) - Trade Republic Support, https://support.traderepublic.com/de-de/39-Auf-welchem-Handelsplatz-werden-meine-Orders-ausgef
2. Welche Orderarten werden angeboten? - Trade Republic Support, https://support.traderepublic.com/de-lu/689-Welche-Orderarten-werden-angeboten
3. Are there commissions for order execution? - Trade Republic Support, https://support.traderepublic.com/en-de/784-Are-there-commissions-for-order-execution
4. Wie kann ich mit Bruchstuecken handeln? - Trade Republic Support, https://support.traderepublic.com/de-de/1420-Wie-kann-ich-mit-Bruchstuecken-handeln
5. Wann werden Sparplaene ausgefuehrt? - Trade Republic Support, https://support.traderepublic.com/de-de/849
6. Which derivatives can I trade with Trade Republic? - Trade Republic Support, https://support.traderepublic.com/en-lt/87-Which-derivatives-can-I-trade-with-Trade-Republic
7. What happens to derivatives that are stopped out or knocked out? - Trade Republic Support, https://support.traderepublic.com/en-sk/696-What-happens-to-derivatives-that-are-stopped-out-or-knocked-out
8. Welche ETFs kann ich bei Trade Republic handeln? - Trade Republic Support, https://support.traderepublic.com/de-de/42-Welche-ETFs-kann-ich-bei-Trade-Republic-handeln
9. Wie sind meine Gelder gesichert? - Trade Republic Support, https://support.traderepublic.com/de-de/3938
10. Was muss ich ueber die Zinsen wissen? - Trade Republic Support, https://support.traderepublic.com/de-de/2580-Was-muss-ich-ueber-die-Zinsen-wissen
11. 2.5 % p.a. Zinsen auf dein Cash - Trade Republic (marketing page, undated), https://traderepublic.com/de-de/zinsen
12. Was ist ein Verlustverrechnungstopf? - Trade Republic Support, https://support.traderepublic.com/de-de/158-Was-ist-ein-Verlustverrechnungstopf
13. Jahressteuerbescheinigung (Tax Report) - Trade Republic Support (search excerpt), https://support.traderepublic.com/de-de/1078-Was-ist-die-Jahressteuerbescheinigung
14. Dividenden Auszahlung von US Unternehmen - Vorab-Reduzierung - Trade Republic Support, https://support.traderepublic.com/de-de/1077-Dividenden-Auszahlung-von-US-Unternehmen-_-Vorab_Reduzierung
15. Wie werden Crypto versteuert? - Trade Republic Support, https://support.traderepublic.com/de-de/432-Wie-werden-Crypto-versteuert (crypto fee: Trade Republic Support 436, search excerpt, https://support.traderepublic.com/de-de/436-Welche-Geb%C3%BChren-fallen-beim-Handel-mit-Crypto-an)
16. Wo werden meine Crypto verwahrt? - Trade Republic Support, https://support.traderepublic.com/de-de/441-Wo-werden-meine-Crypto-verwahrt
17. Wie funktioniert die Devisenkonvertierung? - Trade Republic Support, https://support.traderepublic.com/de-de/88-Wie-funktioniert-die-Devisenkonvertierung
18. What is Saveback? - Trade Republic Support, https://support.traderepublic.com/en-de/1215-What-is-Saveback
19. Trade Republic fuehrt Aenderungen ein (dated 03.07.2026) - Stiftung Warentest (test.de), https://www.test.de/trade-republic-handelssystem-gebuehr-aenderung-6320863-0/
20. (removed 2026-10-17: advertising page)
21. Einkommensteuergesetz (EStG) section 20 - Bundesministerium der Justiz, https://www.gesetze-im-internet.de/estg/__20.html
22. Einkommensteuergesetz (EStG) section 32d - Bundesministerium der Justiz, https://www.gesetze-im-internet.de/estg/__32d.html
23. Investmentsteuergesetz (InvStG) section 20 - Bundesministerium der Justiz, https://www.gesetze-im-internet.de/invstg_2018/__20.html
24. Investmentsteuergesetz (InvStG) section 18 - Bundesministerium der Justiz, https://www.gesetze-im-internet.de/invstg_2018/__18.html
25. Solidaritaetszuschlaggesetz 1995 section 4 - Bundesministerium der Justiz, https://www.gesetze-im-internet.de/solzg_1995/__4.html
26. Basiszins zur Berechnung der Vorabpauschale zum 2.1.2026 (BMF letter, summary) - Otto Schmidt (secondary), https://www.otto-schmidt.de/news/steuerrecht/basiszins-zur-berechnung-der-vorabpauschale-gem-18-absatz-4-invstg-basiszins-zum-2-1-2026-2026-01-15.html
27. ESMA adopts final product intervention measures on CFDs and binary options (1 June 2018) - ESMA, https://www.esma.europa.eu/press-news/esma-news/esma-adopts-final-product-intervention-measures-cfds-and-binary-options
28. Technical advice to the EC on product intervention (final report; 74-89% loss range, search excerpt) - ESMA, https://www.esma.europa.eu/sites/default/files/library/esma35-43-2134_technical_advice_to_the_ec_on_product_intervention.pdf
29. ESMA proposes to move to T+1 by October 2027 - ESMA, https://www.esma.europa.eu/node/214007
30. New T+1 settlement cycle: what investors need to know (search excerpt) - U.S. SEC, https://www.sec.gov/oiea/investor-alerts-and-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor
31. MSCI World Index factsheet (2026; max drawdown figure via search excerpt) - MSCI, https://www.msci.com/documents/10199/178e6643-6ae6-47b9-82be-e1fc565ededb
32. Stock Prices in the Financial Crisis (Notes from the Vault, Sept 2009; search excerpt) - Federal Reserve Bank of Atlanta, https://www.atlantafed.org/cenfis/publications/notesfromthevault/0909
33. US-domiciled ETFs: why they are no longer available from many online brokers (March 2018) - justETF (secondary), https://www.justetf.com/en/news/etf/us-domiciled-etfs.html
34. Restricted access to US ETFs for ordinary EU retail investors (written question E-004745/2021) - European Parliament, https://www.europarl.europa.eu/doceo/document/E-9-2021-004745_EN.html
35. Kapitalertragsteuer; Ausstellung von Steuerbescheinigungen, Anhang 19 I (foreign tax credit cap; search excerpt) - Bundesministerium der Finanzen, Amtliches Einkommensteuer-Handbuch 2021, https://ao.bundesfinanzministerium.de/esth/2021/C-Anhaenge/Anhang-19/I/anhang-19-I.html
36. Trade Republic hat die Vollbanklizenz - Boersen-Zeitung (secondary, search excerpt), https://www.boersen-zeitung.de/banken-finanzen/trade-republic-hat-die-vollbanklizenz
37. Trade Republic erhaelt Lizenz fuer eigenen Handelsplatz - finanzwissen.de (secondary, search excerpt), https://finanzwissen.de/news/trade-republic-erhaelt-lizenz-fuer-eigenen-handelsplatz/
38. Anlage KAP: Wer muss und wer sollte sie machen? - Finanztip (secondary, search excerpt), https://www.finanztip.de/steuererklaerung-anlage-kap/
39. Wann sind die Handelszeiten? - Trade Republic Support (search excerpt), https://support.traderepublic.com/de-de/759-Wann-sind-die-Handelszeiten
40. Crypto press release, November 2025 (MiCAR; search excerpt) - Trade Republic, https://assets.traderepublic.com/assets/files/251114_TradeRepublic_Crypto_PressRelease_DE_DE.pdf
41. Wo wird mein Geld aufbewahrt? - Trade Republic Support (search excerpt), https://support.traderepublic.com/de-at/2201-Where-is-my-money-stored
42. Freistellungsauftrag (FSA) - Trade Republic Support (search excerpt; the URL redirected to the general support page when opened), https://support.traderepublic.com/de-de/3003-Freistellungsauftrag-(FSA)
43. PFOF-Verbot ab 1. Juli 2026 - finanzwissen.de (secondary, search excerpt), https://finanzwissen.de/news/pfof-verbot-ab-1-juli-2026-was-sich-fuer-anleger-aendert-und-welche-neobroker-noch-keine-ansage-gemacht-haben/
44. Kundenvereinbarung (2021 version; search excerpt, may be outdated) - Trade Republic Bank, https://assets.traderepublic.com/documents/DE/kundenvereinbarungen_de_20211115095540.pdf
45. Regulation (EU) 2025/2075 (amending CSDR; T+1 settlement from 11 October 2027) - EUR-Lex, https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R2075
46. Finanzamt NRW, "Abgeltungsteuer" (church tax rates by state), https://www.finanzamt.nrw.de/steuerinfos/privatpersonen/einkuenfte-aus-kapitalvermoegen/abgeltungsteuer
47. Trade Republic: von einem zu 30 Handelsplaetzen (10 Jul 2026) - Finanztip (secondary; fees and venue list to be checked in the app), https://www.finanztip.de/daily/trade-republic-von-einem-zu-30-handelsplaetzen/
