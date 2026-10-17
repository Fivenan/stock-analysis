# Strategy

_Last checked: 2026-10-17 · Educational content, not investment advice. Past performance does not predict future results._

This page compiles what peer-reviewed research, index providers and regulators say about which approaches have worked for private investors, which usually fail, and why. It describes frameworks and evidence; it does not tell you what to buy or how much to invest. Rules of thumb are labelled as such. Related pages: [Trading basics](01-trading-basics.md), [Markets overview](markets/README.md), [Germany](markets/germany.md), [Europe](markets/europe.md), [USA](markets/usa.md), [China](markets/china.md), [Indonesia](markets/indonesia.md), [APIs](apis.md), [Index](README.md).

Labels: "(unverified)" means the primary source could not be confirmed. Several publisher sites (S&P Dow Jones Indices, Morningstar, Trade Republic) blocked automated access, so some figures come from secondary summaries, stated where they apply. Trade Republic features (savings plans, per-order fee, fractional shares, instrument list) change over time; this page maps strategies to them only in general terms. The verified fee schedule belongs on [Trading basics](01-trading-basics.md).

---

## 1. What the evidence says first

### 1.1 Active versus passive: most professionals lose to the index

S&P Dow Jones Indices publishes the SPIVA ("S&P Indices Versus Active") scorecards, which compare actively managed funds with their benchmark and correct for funds that were closed or merged (survivorship).

- **US, 2025:** 79% of active US large-cap funds underperformed the S&P 500 in calendar 2025, up from 65% in 2024 [1][2]. Mid-cap funds: 55%; small-cap funds: 41%; international funds: 63%; global funds: 76% [2].
- **US, long horizons:** more than 90% of active large-cap funds underperformed over 15 years; the category table I could see put it at 89.93% over 15 years and 92.89% over 20 years [1] (secondary copy of the table; confirm against the S&P PDF). None of the 22 US equity categories had a majority of managers beating the benchmark over 15 years [1] (as reported by a secondary summary).
- **Europe (SPIVA Europe), 2025:** 81.8% of active equity funds lagged their benchmarks over one year and 97.0% over ten years; majority underperformance in 18 of 21 equity categories [3] (figures from S&P's own summary as quoted in search results; the PDF itself returned HTTP 403). For euro-denominated Global Equity funds, 71% underperformed the S&P World Index in 2025 [3]. The mid-year 2026 edition reports 94% of equity funds lagging over ten years [4] (secondary summary).

The scorecards measure professional managers after fees, not private stock pickers; private investors have no reason to expect better odds, and the retail studies below suggest worse. Active funds can still win in a given year: small caps in 2025 were a counter-example (41% underperformed) [2].

### 1.2 The behaviour gap: investors earn less than the funds they hold

Morningstar's "Mind the Gap" study compares a fund's reported total return (as if you held it for the whole period) with the dollar-weighted "investor return" that reflects when real money went in and out.

- For the 10 years to 31 December 2024, across more than 25,000 US open-end funds and ETFs, the average dollar earned about 7.0% a year versus 8.2% for the funds themselves, a 1.2 percentage-point gap, or about 15% of the funds' gains [5][6].
- Allocation funds (diversified, long-held) showed 6.3% investor return versus 6.5% fund return, a gap of about 0.2 points; funds held mainly by retail investors, funds with volatile cash flows and funds with larger tracking error showed larger gaps [5].
- Caveat: a 2026 paper in the *Financial Analysts Journal* using the same sample argues that poor timing by mutual-fund investors costs only about 0.10% a year, not 1.2%, and that the headline gap is mainly something else [7]. A newer 2026 edition of the Morningstar report is reported to show 8.7% versus 9.9% over the ten years to December 2025 (secondary source, not verified). Read the gap as "behaviour and cash-flow timing can cost something, with disagreement on how much", not as a precise number.

### 1.3 Retail trading studies

- **Barber and Odean, "Trading Is Hazardous to Your Wealth" (Journal of Finance, 2000).** 66,465 US households at a large discount broker, 1991 to 1996: the households that traded most earned 11.4% a year while the market returned 17.9%; the average household earned 16.4% and turned over 75% of its portfolio a year. The authors attribute the damage to overconfidence [8].
- **Barber, Lee, Liu and Odean, Taiwan (Review of Financial Studies, 2009).** All Taiwan Stock Exchange trades 1995 to 1999: individual investors' aggregate portfolios underperformed by 3.8 percentage points a year, with losses equal to 2.2% of Taiwan's GDP, while institutions gained about 1.5 points a year [9]. A university summary states that slightly less than two-thirds of the individual-investor losses came from transaction costs [10].
- **Barber, Lee, Liu and Odean, day traders in Taiwan (Journal of Financial Markets, 2014).** Over 1992 to 2006, less than 1% of the day-trader population could predictably and reliably earn positive abnormal returns net of fees [11].
- **Chague, De-Losso and Giovannetti, Brazil ("Day Trading for a Living?").** Among all individuals who began day trading Brazilian equity futures between 2013 and 2015 and persisted for more than 300 days, 97% lost money. Only 1.1% earned more than the Brazilian minimum wage, and only about 0.5% (depending on the version) earned more than a bank teller's starting salary; the authors find no evidence of learning by trading [12]. Caveat from a secondary summary: this is one country, one instrument class and possibly a hard period [12].

### 1.4 Leveraged derivatives for retail clients (CFDs)

ESMA's 2018 product-intervention announcement, based on analyses by national regulators, found that **74% to 89% of retail CFD accounts typically lose money**, with average losses per client in a range of about EUR 1,600 to EUR 29,000. ESMA capped retail leverage from 30:1 (major currency pairs) down to 5:1 for single stocks and 2:1 for crypto [13]. Providers must show their own loss percentage in a standard risk warning [13]. These are ESMA's 2018 figures; I did not find an official update in this session. They concern CFDs; knock-out certificates are a different instrument, and I did not verify an equivalent official loss share for them (see 2.7).

### 1.5 Costs and taxes

- Costs: in the Taiwan data, trading costs were the largest single piece of retail losses [9][10]. A one-euro order fee looks small, but a high-turnover portfolio pays it, plus spread, on every round trip.
- German tax on capital income (*Abgeltungsteuer*, the flat withholding tax): 25% of the income [14], plus *Solidaritätszuschlag* (solidarity surcharge) of 5.5% of that tax [15], i.e. 26.375% before any church tax (*Kirchensteuer*), which reduces the flat tax by a fraction as set out in the law [14]. Everyone has a tax-free allowance, the *Sparer-Pauschbetrag*, of EUR 1,000 (EUR 2,000 for jointly assessed spouses) [17]; brokers apply it via an exemption order (*Freistellungsauftrag*).
- For equity funds and ETFs, 30% of the income is exempt (*Teilfreistellung*) for private investors [16]. Arithmetic on the verified parameters: an equity-fund gain is taxed at about 26.375% x 70% = about 18.46% before church tax, versus 26.375% on a direct stock gain.
- Loss offsetting (*Verlustverrechnung*): losses from selling shares can only be offset against gains from selling shares (often called the *Aktienverlusttopf*); other capital-income losses are handled separately [17]. The EUR 20,000 cap on losses from derivatives (*Termingeschäfte*) and bad debts was abolished by the *Jahressteuergesetz 2024* for all open cases. Banks apply this in withholding from 1 January 2026; for earlier years, use a loss certificate and the tax return [17].
- Tax is a drag on frequent trading mainly through realisation: every sale with a gain triggers tax now, while buy-and-hold defers it. This is an inference from the rules, not a measured figure.

---

## 2. Strategy catalogue

Each entry gives: how it works, evidence, typical holding period, effort, main risks, Trade Republic mapping, German tax. "Trade Republic mapping" describes general features only (savings plans, fractional shares, a low flat order fee, stocks/ETFs/derivatives offered); verify current terms in [Trading basics](01-trading-basics.md).

### 2.1 Passive global index investing with a savings plan (*Sparplan*)

- **How it works.** Hold a broad, low-cost index fund or ETF covering many countries and sectors; invest a fixed amount at regular intervals (*Sparplan*, an automated savings plan); rebalance rarely.
- **Evidence.** It is the "do nothing clever" benchmark that most active funds fail to beat over long horizons (1.1) and that avoids most of the behaviour gap, because investment is automated (1.2; allocation and long-held funds had the smallest gaps [5]).
- **Lump sum versus cost averaging.** Vanguard (2023) found that investing a lump sum immediately beat spreading it over three months in 68% of historical one-year comparisons for a 100% equity portfolio across the US, UK, Australia, Canada and the EU; a simulation gave 65%. Cost averaging beat staying in cash 69% of the time. Vanguard's conclusion is that cost averaging mainly helps investors who are so loss-averse that they would otherwise hold the lump sum in cash [18]. Note the difference: a *Sparplan* funded from monthly income is not "cost averaging a lump sum"; you simply invest money when you receive it.
- **Rebalancing.** Periodic rebalancing to target weights controls risk drift. Common practitioner rules of thumb are an annual calendar rebalance or rebalancing when a weight drifts by about 5 percentage points; I did not retrieve a primary source for these thresholds this session (unverified). With a savings plan you can rebalance by redirecting new contributions, which avoids selling and so avoids realising tax.
- **Holding period.** 10+ years. **Effort:** low (annual review). **Risks:** full equity-market drawdowns (see 5), tracking a single market if the index is not global, currency effects, abandoning the plan in a crash (1.2).
- **Trade Republic.** Savings plans on ETFs and some stocks and fractional purchases fit this approach; confirm which ETFs are offered and any fee for each plan execution.
- **German tax.** Equity ETFs: 30% *Teilfreistellung* [16]. Accumulating funds: *Vorabpauschale*, an advance lump-sum tax. It is based on the fund's value at the start of the year times 70% of the base rate (*Basiszins*), capped at the fund's actual gain, and is deemed received on the first working day of the next year [19]; the broker collects the tax from the cash balance (how Trade Republic handles a shortfall is unverified, see [Trading basics](01-trading-basics.md#funds-and-etfs)). *Vorabpauschalen* already taxed are deducted from the gain when you sell, so they are not taxed twice. Distributing funds pay tax on distributions each year. Use the *Freistellungsauftrag* so that the first EUR 1,000 of income a year is untaxed [17].

### 2.2 Core-satellite

- **How it works.** A large "core" in a broad index fund (2.1) plus a small "satellite" for individual ideas, themes or tactical positions, capped at a fixed share so that mistakes cannot sink the plan.
- **Evidence.** I found no peer-reviewed test that core-satellite beats the core alone; it is a portfolio-construction convention whose value is behavioural: it gives the urge to pick stocks a boxed outlet. Given 1.1 and 1.3, a satellite should be expected to land at or below the index after costs (inference). A satellite cap of roughly 5% to 20% is a common practitioner rule of thumb, not a research finding (unverified).
- **Holding period:** core 10+ years; satellite varies. **Effort:** medium. **Risks:** satellite overconfidence (4), concentration, tax-inefficient turnover in the satellite.
- **Trade Republic mapping.** Savings plan for the core, manual orders for the satellite; track the two separately in your journal (3).
- **German tax.** Stock losses can only be offset against stock gains [17]; ETF gains and stock gains sit in different treatment (*Teilfreistellung* applies only to funds [16]).

### 2.3 Factor investing: value, size, momentum, quality, low volatility

- **How it works.** Tilt a portfolio toward characteristics that have historically earned higher average returns than the market: cheap stocks (value), small stocks (size), recent winners (momentum), profitable stocks (quality/profitability), low-risk stocks (low volatility).
- **Evidence.**
  - Fama and French (1992) found that size and book-to-market equity capture much of the variation in average stock returns, while market beta alone had a flat relationship in their sample [20]. Their five-factor model (2015) adds profitability and investment; in their sample the value factor became redundant once those were included [21].
  - Momentum: Jegadeesh and Titman (1993) found that buying past winners and selling past losers earns significant positive returns over 3 to 12 months, partly reversing in the following two years [22].
  - Value and momentum premia are reported across many asset classes by Asness, Moskowitz and Pedersen (2013) [23] (the abstract was not retrievable; the title and journal are verified).
  - Low volatility: Baker, Bradley and Wurgler (2011) show that from 1968 to 2008 low-volatility and low-beta portfolios earned higher returns with smaller drawdowns, and attribute this to investors' preference for lottery-like stocks plus benchmark-constrained managers [25]; Frazzini and Pedersen (2014) report positive risk-adjusted returns to betting against beta across several markets, with the strategy doing badly when funding conditions tighten [24].
  - **Decay after publication.** McLean and Pontiff (2016) studied 97 published return predictors: portfolio returns were 26% lower out-of-sample and 58% lower after publication, which they read as partly data mining and partly investors trading the discovered pattern away [26].
- **Holding period:** years to decades; premia can disappear for long stretches. **Effort:** low if done through factor ETFs, high if done with single stocks. **Risks:** long underperformance periods, crowding, decay [26], higher costs, tracking error versus a world index.
- **Trade Republic mapping.** Factor ETFs (if listed on the platform) can sit in a *Sparplan*; screening single stocks yourself is possible but demanding. Check the instrument list.
- **German tax.** Same as 2.1 for ETFs; high-turnover factor stock portfolios realise gains more often.

### 2.4 Dividend and dividend-growth investing

- **How it works.** Buy companies that pay (and raise) dividends and live off, or reinvest, the cash flow.
- **Evidence.** Hartzmark and Solomon ("The Dividend Disconnect", Journal of Finance, 2019) document that many individual investors, funds and analysts treat dividends and capital gains as separate things and fail to fully recognise that a dividend reduces the share price; investors rarely reinvest dividends; demand for dividends is higher when interest rates are low, and that demand is associated with lower subsequent returns for dividend stocks [27]. In plain terms: a dividend is a transfer of value from the company to you, not extra return.
- **German tax drag.** A dividend is taxed when paid (25% plus *Solidaritätszuschlag*, plus church tax if applicable, subject to the EUR 1,000 allowance) [14][15][17], while an unrealised gain is not taxed until sale. Foreign dividends can in addition carry foreign withholding tax; see [USA](markets/usa.md) and [Germany](markets/germany.md) for the market-specific handling (not verified on this page).
- **Holding period:** 10+ years. **Effort:** medium. **Risks:** concentration in a few sectors, dividend cuts, yield traps, tax drag versus accumulating funds, home bias.
- **Trade Republic mapping.** Fractional shares help build positions in dividend stocks; dividend ETFs exist for savings plans; check payout and tax-handling details in your account.

### 2.5 Trend following and momentum rules (for example the 200-day moving average)

- **How it works.** Hold an asset while its price is above a long-term average (for example 200 days or 10 months); move to cash or bonds when it is below.
- **Evidence.**
  - Brock, Lakonishok and LeBaron (1992) tested moving-average and trading-range breakout rules on Dow Jones data from 1897 to 1986 and found that buy signals were followed by higher, less volatile returns than sell signals [29].
  - Faber (2007), "A Quantitative Approach to Tactical Asset Allocation", proposes a 10-month moving-average timing rule across asset classes to cut volatility and drawdowns [28] (SSRN page was not retrievable; this is a description of the paper's idea, not a re-verified number).
  - Counter-evidence: Bajgrowicz and Scaillet (2012) re-tested technical rules on Dow data from 1897 to 2011 with a correction for data snooping: an investor could not have reliably picked the best rules in advance, and even low transaction costs eliminated the apparent profits [30].
- **Interpretation (inference).** Trend rules can reduce drawdown depth but tend to lag in rising markets and whipsaw (repeated in-and-out switching) in choppy ones; evidence of persistent excess return after costs and taxes is weak.
- **Holding period:** weeks to years. **Effort:** medium. **Risks:** whipsaws, tax cost of frequent realisation, missed rebounds, rule-mining [30].
- **Trade Republic / tax.** Manual orders on an index ETF; each switch pays order fee and spread and realises gains (no tax-free switching).

### 2.6 Swing trading and technical analysis

- **How it works.** Hold positions for days to weeks and decide from chart patterns, indicators and price action.
- **Evidence.** The classical results above [29] are for simple rules in older data; the data-snooping-corrected study finds that apparent profits mostly vanish out of sample and after costs [30]. Retail-trader studies (1.3) show that frequent traders as a group lose relative to the market. I did not find reliable peer-reviewed evidence that chart-pattern trading earns excess returns for private investors after costs (absence of evidence in this session, not proof of absence).
- **Holding period:** days to weeks. **Effort:** high. **Risks:** costs, overconfidence (4), tax realisation, overnight gaps (3). Low-friction ordering in the app also raises the risk of over-trading (4). Share losses can only absorb share gains [17].

### 2.7 Day trading and leveraged products (knock-outs, CFDs)

- **Evidence.** See 1.3 and 1.4: less than 1% of Taiwanese day traders predictably earn net-of-fee profits [11]; 97% of persistent Brazilian futures day traders lost money [12]; 74% to 89% of retail CFD accounts lose money [13].
- **Why leverage hurts.** Leverage multiplies both gains and losses; a move against you can wipe out the stake. Knock-out certificates (*Knock-out-Zertifikate*, leveraged securities that expire worthless if a barrier price is touched) have a built-in total-loss event. Daily-reset leveraged ETFs track a multiple of one day's return and can deviate from the multiple over longer periods; I did not retrieve a primary source on this in this session (unverified).
- **Holding period:** minutes to days. **Effort:** very high. **Risks:** total loss of the stake, costs, psychological pressure.
- **Trade Republic mapping.** Derivatives may be offered as listed securities; these are not CFDs, so the ESMA CFD loss percentages do not apply directly, and I did not verify an official loss share for them. Check the product's key information document.
- **German tax.** Derivative gains and losses fall under capital income [17]. The EUR 20,000 cap on losses from derivatives (*Termingeschäfte*) and bad debts was abolished by the *Jahressteuergesetz 2024* for all open cases. Banks apply this in withholding from 1 January 2026; for earlier years, use a loss certificate and the tax return [17].

### 2.8 Following public insider buying, politicians' trades and 13F "guru" portfolios

**The legal line.** Trading on non-public inside information is illegal (EU Market Abuse Regulation, Regulation (EU) No 596/2014, which prohibits insider dealing; the US has parallel rules) [36]. Acting on information that insiders are legally required to publish is legal; the research below uses only published filings. This is a general statement, not legal advice.

**Corporate insiders (US Form 4, German/EU *Directors' Dealings*, i.e. *Eigengeschäfte von Führungskräften*).**
- US officers, directors and 10% owners report trades on Form 4, generally within two business days [35] (the PDF could not be text-extracted here; the deadline is confirmed by secondary legal summaries). In the EU, managers must notify transactions under Article 19 MAR within three business days above a de-minimis threshold [36]; the threshold is set per calendar year. Under the EU Listing Act the EU default is EUR 20,000 and national regulators may set EUR 10,000–50,000. In Germany BaFin raised it to EUR 50,000 from 1 January 2026 (general ruling of 4 December 2025) [50]; see [Germany](markets/germany.md).
- Evidence: Lakonishok and Lee (2001, 1975 to 1995 data): little price movement when insiders trade or when they report to the SEC; the predictive content comes from purchases (sales carry no predictive ability), and the predictive power is concentrated in smaller firms [32]. Cohen, Malloy and Pomorski (2012) separate "routine" from "opportunistic" insider trades: a portfolio following opportunistic trades earns value-weighted abnormal returns of 82 basis points per month, routine traders' returns are about zero, and the most informed opportunistic traders are local, non-executive insiders at poorly governed, geographically concentrated firms [33].
- How fast it is priced in: Lakonishok and Lee find little market reaction around the report date [32]; my inference is that the usable edge, where it exists, sits in small, hard-to-trade stocks. Rozeff and Zaman (1988), as summarised in a survey, found that outsiders mimicking insider trades lose about half of their apparent profit once size and P/E effects are controlled for, and that with 2% transaction costs the profit is zero or negative [34]. Seyhun's early (1986) work is the usual reference for large insider profits [34]. These are older samples, and spreads in small caps are a real cost; the delay between trade and filing (two to three business days) is the entry lag.
- Practical reading: the evidence is stronger for insider purchases than sales, for small stocks and for opportunistic (non-routine) trades, and weaker after costs. It is a screening input at best.

**Politicians' disclosed trades (US).**
- Ziobrowski et al. (2004) found that a portfolio mimicking Senators' purchases in 1993 to 1998 beat the market by 85 basis points per month, while one mimicking their sales lagged by 12 basis points per month [37]; a later House study found smaller positive abnormal returns on purchases [38]. Eggers and Hainmueller ("Capitol Losses", Journal of Politics, 2013), using 2004 to 2008 disclosures, found no evidence of informed trading and estimated that the average member of Congress underperformed the market by 2 to 3% a year [39].
- Reporting lag: the STOCK Act requires reports within 30 days of notice of a transaction and no more than 45 days after it [40] (2012 CRS report; confirm current rules). A copy-trade therefore starts weeks late, in a rare data set with conflicting results.

**13F "guru" portfolios.** US institutional managers with at least USD 100 million in 13(f) securities file Form 13F within 45 days after quarter end; it lists long positions in mainly US-listed stocks, ETFs and some options, not short positions, not most non-US holdings, and not the trade dates [41]. The reporting lag is up to about 4.5 months from the start of a quarter's trading. I did not retrieve peer-reviewed evidence on copying 13F portfolios in this session; treat claims about "copying famous investors" as unverified (see Open questions).

- **Holding period:** weeks to a year or more. **Effort:** high. **Risks:** stale information, small-cap illiquidity and spreads, survivorship in anecdotes, concentration. **Trade Republic / tax.** Check that the stock is tradable on the platform; taxed as any stock trade.

### 2.9 Event and earnings strategies (post-earnings-announcement drift)

- **How it works.** After a company reports a positive earnings surprise, its stock tends to keep drifting up over following weeks; after a negative surprise, down.
- **Evidence.** Bernard and Thomas (1989) is the classic paper on this drift [42] (no abstract was available on the page used; this is the standard reference). Several later studies report that the effect has weakened as markets and arbitrageurs improved (unverified here). Capturing it needs fast, cheap execution, and gaps around earnings are large.
- **Holding period:** days to months. **Effort:** high. **Risks:** earnings-day gaps, costs, crowding, small-cap spreads. **Trade Republic / tax.** Manual orders; taxed as any stock trade.

---

## 3. Risk management

These are common practices and frameworks, not guarantees.

- **Emergency fund first.** A common rule of thumb is that money needed within a few years is not held in equities. Another common rule of thumb is a reserve of three to six months of expenses (*Notgroschen*), held in cash or a deposit account; I could not retrieve a German consumer-protection source for the exact number (unverified).
- **Position sizing.** A common practitioner rule: risk about 1% to 2% of your portfolio on any one trade (the amount you lose if the exit level is hit). Worked arithmetic: on EUR 10,000, 1% risk is EUR 100; if your exit level is 5% below entry, the position is EUR 100 / 0.05 = EUR 2,000. This is a rule of thumb whose origin I could not tie to a peer-reviewed source (unverified).
- **Stop-losses and their pitfalls.** A stop-loss reduces exposure after a loss threshold. Kaminski and Lo (2014) provide a framework to measure when a stop-loss adds or removes value; they find that at longer sampling frequencies some stop-loss policies can raise expected return while substantially reducing volatility [31]. Pitfalls (inference from how orders work): in a gap the order can execute well below the stop price; a tight stop in a volatile stock gets triggered by noise and locks in the loss and the tax event; a stop is not a guarantee.
- **Diversification.** Many holdings across regions and sectors reduce single-company risk; a world index fund is the simplest form.
- **Maximum-drawdown thinking.** Ask "how far can this fall from peak to trough, and could I hold on?" Arithmetic: after a 20% fall you need +25% to recover; after 33%, +50%; after 50%, +100%. Decide in advance what loss would force you to sell.
- **Leverage.** Borrowed or derivative exposure can lose more than the stake (2.7, 1.4). **Rebalancing:** see 2.1.
- **Trading journal.** Per trade: date, thesis, entry, exit rule, size, outcome, deviations from plan. It makes overconfidence and the disposition effect visible (4).
- **Benchmarking.** Compare your total result after costs and taxes with a global index fund over the same period; this is the test SPIVA applies to professionals (1.1).
- **Paper trading.** Practise without real money first. Caveat: it removes the emotional pressure behind many real losses (4), so a good paper result does not prove you can execute live.

---

## 4. Behavioural pitfalls

- **Overconfidence.** Barber and Odean (2001): men traded 45% more than women, which reduced men's annual net returns by 2.65 percentage points versus 1.72 for women; the authors tie excess trading to overconfidence [43]. The 2000 study found heavy traders earned 11.4% versus 17.9% for the market [8].
- **Loss aversion.** Losses feel larger than equal gains (Tversky and Kahneman, 1992, cumulative prospect theory, which names loss aversion as one of its principles) [46]. A commonly quoted ratio of about 2:1 is not stated on the abstract page I used (unverified). Result: selling in crashes and holding cash too long.
- **Disposition effect.** Investors tend to sell winners too early and hold losers too long (Shefrin and Statman, 1985 [45]; Odean, 1998 [44], on 10,000 discount-brokerage accounts; the abstract was not retrievable here). Hartzmark and Solomon connect it to attention on price changes rather than total returns [27].
- **Recency and trend-chasing.** Extrapolating the last year into the next; chasing last year's winner or sector.
- **FOMO and attention-driven buying.** Barber, Huang, Odean and Schwarz (2022): Robinhood investors engage in more attention-induced trading than other retail investors; the stocks bought most heavily each day had abnormal returns of about -4.7% over the next 20 days [47].
- **Gamification.** The same paper finds that the app's distinctive features contribute to this behaviour, beyond who the users are [47]. Confetti, push notifications, social feeds and zero-friction orders are design choices that raise trading frequency; the evidence in 1.3 says frequency is what hurts. The research suggests that ease of ordering can work as a risk factor rather than a benefit.

---

## 5. Realistic return expectations

- **Long-run equities.** The UBS Global Investment Returns Yearbook 2026 (Dimson, Marsh and Staunton, released 3 March 2026) reports a real (inflation-adjusted) equity return of 6.6% a year over 1900–2025 versus 1.6% for bonds [48]. The secondary report does not say whether this is the world or the US series; the 6.6% matches the US series (USD 1 grew to USD 3,296 in real terms per UBS) [51], and the world figure is likely lower (unverified). The gap between the two reported figures is about 5.0 points in real terms (my subtraction). Real returns were positive in all 21 countries with data back to 1900 (secondary report) [48].
- **What 6.6% real means.** At the US rate of 6.6%, money roughly doubles in real terms about every 11 years (rule of 72: 72 / 6.6), not in months. The path is uneven: long drawdowns occur, and the yearbook notes most large peacetime equity drawdowns were triggered by economic rather than geopolitical factors [48]. I did not obtain a verified percentage for the worst global drawdowns in this session; the MSCI World factsheet [49] contains calendar-year returns and risk figures but could not be text-extracted (unverified). Plan for equity falls of a third or more from peak to trough, as in 2008 to 2009 (my expectation from market history; unverified here; check the MSCI factsheet for exact figures).
- **Averages are not forecasts.** The 6.6% is an average over 126 years and many market regimes; any given 10 or 20 years can be far above or below it (inference from the average-versus-path distinction, not a cited statistic).
- **Why "double your money fast" is a red flag.** (i) Even the long-run annual equity return is single-digit in real terms [48]. (ii) 97% of persistent Brazilian day traders lost money [12]; 74 to 89% of retail CFD accounts lose [13]. (iii) High, steady or guaranteed returns are the pattern of fraud rather than markets; ask who bears the risk and who earns the fee. (iv) Course, signal and "copy" sellers show winners, not the many who lost (survivorship; inference).

---

## 6. A practical playbook template

Fill this in yourself; none of the entries is a recommendation.

1. **Goal.** What is the money for (retirement, a house, a buffer, learning)? Target amount and date: ______
2. **Horizon.** When will you need it? Money needed within roughly the next 3 to 5 years generally does not belong in equities (rule of thumb): ______
3. **Emergency fund.** Months of expenses held in cash, outside this plan: ______ (see 3)
4. **Risk budget.** The largest peak-to-trough fall of the whole portfolio you could sit through without selling: ____% ; worst-case euro loss you can tolerate: ______
5. **Core.** Instrument(s), regions, cost level, contribution amount and day (*Sparplan*): ______; rebalancing rule (calendar or band): ______
6. **Satellite (optional).** Cap as a share of the portfolio: ____% ; hard rule: when the cap is reached, no new money goes in. What am I allowed to do here (stocks, themes, no leverage)? ______
7. **Entry rules.** What has to be true before a satellite purchase (written thesis, maximum position size, maximum loss per idea)? ______
8. **Exit rules.** Planned exit conditions (thesis broken, target, time limit, rebalancing) and how they are executed: ______ ; pre-commit to "no panic sales in a fall of ____%".
9. **Prohibited list.** For example: no leverage, no CFDs, no knock-outs, no investing borrowed money, no trading on non-public information: ______
10. **Review cadence.** Monthly check that contributions ran; quarterly satellite review against the index; annual full review of goal, risk budget and rebalancing. Journal every satellite trade (3).
11. **Benchmark.** Which index will you compare the whole portfolio with, after costs and taxes: ______
12. **Tax checklist (Germany).** *Freistellungsauftrag* set up and split across brokers if you have several? [17] | Fund type and *Teilfreistellung* (30% for equity funds) understood? [16] | *Vorabpauschale* cash buffer for accumulating funds? [19] | Share losses only offset share gains [17]; keep the broker's annual tax report | Dividends and foreign withholding tax understood (see [Germany](markets/germany.md), [USA](markets/usa.md)) | Church tax status correct at the broker? [14] | Derivative loss treatment confirmed with a tax adviser [17].

---

## 7. Summary table

"Evidence strength" is my reading of the sources above: strong = repeated across independent peer-reviewed or index-provider studies; moderate = published evidence with decay, caveats or limited samples; weak = mixed or thin evidence; none/negative = evidence mainly of losses.

| Strategy | Evidence strength | Effort | Typical outcome vs index | Main risk |
|---|---|---|---|---|
| Passive global index + *Sparplan* [1][3][5] | Strong (as benchmark) | Low | Index return minus small cost; by definition the benchmark | Full market drawdowns; quitting in a crash |
| Core-satellite | Weak (no direct test found) | Medium | Core at index; satellite usually at or below index after costs | Satellite overconfidence |
| Factor tilts [20][21][22][26] | Moderate (decay after publication: 26% lower out of sample, 58% after publication [26]) | Low (ETF) to high (stocks) | May differ from index in either direction; long dry spells | Decay, crowding, tracking error |
| Dividend / dividend growth [27] | Weak to moderate | Medium | Roughly market-like; tax drag versus accumulating funds | Sector concentration, tax drag, "free money" illusion |
| Trend following / 200-day MA [28][29][30] | Mixed (positive in old data, weak after snooping and costs [30]) | Medium | Smaller drawdowns, often lower return in bull markets | Whipsaws, tax from frequent switching |
| Swing trading / technical analysis [29][30] | Weak to negative | High | Frequent traders as a group underperform [8][9] | Costs, overconfidence, gaps |
| Day trading and leverage [11][12][13] | Negative | Very high | Most lose; <1% of Taiwan day traders skilled net of fees [11] | Total loss, costs, stress |
| Insider-buying signals [32][33] | Moderate for purchases, small caps, opportunistic trades; weaker after costs [34] | High | Abnormal returns in samples (82 bp/month in [33]); not reliably capturable | Small-cap illiquidity, lag, costs |
| Politicians' trades [37][39] | Mixed / negative | Medium | Conflicting studies; one found 2 to 3% underperformance a year [39] | Reporting lag of up to 45 days [40] |
| 13F copying [41] | Not verified | Low to medium | Unknown (no evidence retrieved) | Lag up to 45 days after quarter end, partial view [41] |
| Earnings drift [42] | Moderate historically, reported weaker now (unverified) | High | Unknown net of costs | Gaps, crowding |

---

## Sources

All accessed 2026-10-17. Where a publisher blocked automated access (HTTP 403), the figure was taken from the search-result or secondary summary named in the text, and this is marked.

1. S&P Dow Jones Indices. "SPIVA U.S. Scorecard, Year-End 2025." 2026. https://www.spglobal.com/spdji/en/spiva/article/spiva-us-year-end-2025/ (PDF: https://www.spglobal.com/spdji/en/documents/spiva/spiva-us-year-end-2025.pdf). Page returned HTTP 403; figures from search summaries and a secondary copy of the report.
2. InvestmentNews. "Active managers stumble again in 2025 as large caps dominate." 2026. https://investmentnews.com/equities/active-managers-stumble-again-in-2025-as-large-caps-dominate/265541
3. S&P Dow Jones Indices. "SPIVA Europe Scorecard, Year-End 2025." 2026. https://www.spglobal.com/spdji/en/documents/spiva/spiva-europe-year-end-2025.pdf (HTTP 403; figures from S&P's Indexology summary as returned by search).
4. S&P Dow Jones Indices. "SPIVA Europe Scorecard, Mid-Year 2026." 2026. https://www.spglobal.com/spdji/en/documents/spiva/spiva-europe-mid-year-2026.pdf (not opened; figure from search summary).
5. Morningstar. "Mind the Gap US 2025." 2025. https://www.morningstar.com/business/insights/research/mind-the-gap-2025 (page text not retrievable; figures via source 6).
6. Wealth Management. "Morningstar Report: Investors Miss 15% of Fund Returns." 13 August 2025. https://www.wealthmanagement.com/investing-strategies/morningstar-investors-miss-out-on-15-of-fund-total-returns
7. Fulkerson, J. A., Jordan, B., Riley, T. B., Yan, Q. "Bad Timing Does Not Cost Investors 15% of Their Funds' Returns: An Examination of Morningstar's 'Mind the Gap' Study." Financial Analysts Journal 82(3), May 2026. https://rpc.cfainstitute.org/research/financial-analysts-journal/2026/bad-timing-does-not-cost-investors-funds-returns
8. Barber, B. M., Odean, T. "Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors." Journal of Finance 55(2), 2000, 773-806. https://ideas.repec.org/a/bla/jfinan/v55y2000i2p773-806.html
9. Barber, B. M., Lee, Y.-T., Liu, Y.-J., Odean, T. "Just How Much Do Individual Investors Lose by Trading?" Review of Financial Studies 22(2), 2009, 609-632. https://ideas.repec.org/a/oup/rfinst/v22y2009i2p609-632.html
10. Haas School of Business, UC Berkeley newsroom. Summary of source 9 (share of losses from transaction costs). https://newsroom.haas.berkeley.edu/?p=10491 (via search summary).
11. Barber, B. M., Lee, Y.-T., Liu, Y.-J., Odean, T. "The Cross-Section of Speculator Skill: Evidence from Day Trading." Journal of Financial Markets 18, 2014, 1-24. https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html
12. Chague, F., De-Losso, R., Giovannetti, B. "Day Trading for a Living?" SSRN working paper (2019). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101 ; summary: CXO Advisory, https://www.cxoadvisory.com/investing-expertise/day-trading-a-bust/
13. ESMA. "ESMA agrees to prohibit binary options and restrict CFDs to protect retail investors." Press release, 27 March 2018. https://www.esma.europa.eu/node/84933
14. Bundesrepublik Deutschland. Einkommensteuergesetz (EStG) section 32d (flat tax on capital income, church tax). https://www.gesetze-im-internet.de/estg/__32d.html
15. Bundesrepublik Deutschland. Solidaritätszuschlaggesetz 1995, section 4. https://www.gesetze-im-internet.de/solzg_1995/__4.html
16. Bundesrepublik Deutschland. Investmentsteuergesetz (InvStG 2018) section 20 (*Teilfreistellung*). https://www.gesetze-im-internet.de/invstg_2018/__20.html
17. Bundesrepublik Deutschland. Einkommensteuergesetz (EStG) section 20 (capital income, loss offsetting in para. 6, *Sparer-Pauschbetrag* in para. 9). https://www.gesetze-im-internet.de/estg/__20.html
18. Vanguard. "Cost averaging: Invest now or temporarily hold your cash?" February 2023. https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf (PDF not text-extractable here; figures from search summary of the paper).
19. Bundesrepublik Deutschland. Investmentsteuergesetz (InvStG 2018) section 18 (*Vorabpauschale*). https://www.gesetze-im-internet.de/invstg_2018/__18.html
20. Fama, E. F., French, K. R. "The Cross-Section of Expected Stock Returns." Journal of Finance 47(2), 1992, 427-465. https://ideas.repec.org/a/bla/jfinan/v47y1992i2p427-65.html
21. Fama, E. F., French, K. R. "A five-factor asset pricing model." Journal of Financial Economics 116(1), 2015, 1-22. https://ideas.repec.org/a/eee/jfinec/v116y2015i1p1-22.html
22. Jegadeesh, N., Titman, S. "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency." Journal of Finance 48(1), 1993, 65-91. https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html
23. Asness, C. S., Moskowitz, T. J., Pedersen, L. H. "Value and Momentum Everywhere." Journal of Finance 68(3), 2013, 929-985. https://ideas.repec.org/a/bla/jfinan/v68y2013i3p929-985.html (abstract not available on the page).
24. Frazzini, A., Pedersen, L. H. "Betting against beta." Journal of Financial Economics 111(1), 2014, 1-25. https://ideas.repec.org/a/eee/jfinec/v111y2014i1p1-25.html
25. Baker, M., Bradley, B., Wurgler, J. "Benchmarks as Limits to Arbitrage: Understanding the Low-Volatility Anomaly." Financial Analysts Journal 67(1), 2011, 40-54. https://ideas.repec.org/a/taf/ufajxx/v67y2011i1p40-54.html
26. McLean, R. D., Pontiff, J. "Does Academic Research Destroy Stock Return Predictability?" Journal of Finance 71(1), 2016, 5-32. https://ivey.uwo.ca/media/3775549/pontiff.pdf (figures 26% and 58% via search summary of the published version).
27. Hartzmark, S. M., Solomon, D. H. "The Dividend Disconnect." Journal of Finance 74(5), 2019, 2153-2199. https://ideas.repec.org/a/bla/jfinan/v74y2019i5p2153-2199.html
28. Faber, M. T. "A Quantitative Approach to Tactical Asset Allocation." SSRN / Journal of Wealth Management, 2007. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461 (HTTP 403; not re-verified).
29. Brock, W., Lakonishok, J., LeBaron, B. "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns." Journal of Finance 47(5), 1992, 1731-1764. https://ideas.repec.org/a/bla/jfinan/v47y1992i5p1731-64.html
30. Bajgrowicz, P., Scaillet, O. "Technical trading revisited: False discoveries, persistence tests, and transaction costs." Journal of Financial Economics 106(3), 2012, 473-491. https://ideas.repec.org/a/eee/jfinec/v106y2012i3p473-491.html
31. Kaminski, K. M., Lo, A. W. "When do stop-loss rules stop losses?" Journal of Financial Markets 18, 2014, 234-254. https://ideas.repec.org/a/eee/finmar/v18y2014icp234-254.html
32. Lakonishok, J., Lee, I. "Are Insider Trades Informative?" Review of Financial Studies 14(1), 2001, 79-111. https://ideas.repec.org/a/oup/rfinst/v14y2001i1p79-111.html
33. Cohen, L., Malloy, C., Pomorski, L. "Decoding Inside Information." Journal of Finance 67(3), 2012, 1009-1043. https://ideas.repec.org/a/bla/jfinan/v67y2012i3p1009-1043.html
34. Zeckhauser et al. survey of insider-trading research (summarising Seyhun 1986, J. Financial Economics 16(2), and Rozeff and Zaman 1988, Journal of Business 61). https://scholar.harvard.edu/sites/scholar.harvard.edu/files/rzeckhauser/files/insider_trading.pdf (via search summary; not opened in full).
35. U.S. SEC. "Forms 3, 4 and 5" (insider ownership reports). https://www.sec.gov/files/forms-3-4-5.pdf (PDF not text-extractable here; two-business-day deadline from secondary legal summaries).
36. European Union. Regulation (EU) No 596/2014 on market abuse (MAR), Articles 14 and 19. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32014R0596 (page text not retrievable by the tool; content stated from general knowledge, not re-verified).
37. Ziobrowski, A. J., Cheng, P., Boyd, J. W., Ziobrowski, B. J. "Abnormal Returns from the Common Stock Investments of the U.S. Senate." Journal of Financial and Quantitative Analysis 39(4), 2004, 661-676. https://ideas.repec.org/a/cup/jfinqa/v39y2004i04p661-676_00.html
38. Ziobrowski, A. J., Boyd, J. W., Cheng, P., Ziobrowski, B. J. "Abnormal Returns from the Common Stock Investments of Members of the U.S. House of Representatives." Business and Politics 13(1), 2011. https://ideas.repec.org/a/cup/buspol/v13y2011i01p1-22_00.html
39. Eggers, A. C., Hainmueller, J. "Capitol Losses: The Mediocre Performance of Congressional Stock Portfolios 2004-2008." Journal of Politics 75(2), 2013. https://www.mit.edu/~jhainm/Paper/Eggmueller_CapitolLosses.pdf
40. Congressional Research Service. "The STOCK Act, Insider Trading, and Public Service" (R42495), 2012. https://www.everycrsreport.com/files/20120419_R42495_3294279bf505ae0b66526fbfece0f4b5c867b024.html
41. U.S. SEC, Division of Investment Management. "Frequently Asked Questions About Form 13F." https://www.sec.gov/divisions/investment/13ffaq
42. Bernard, V. L., Thomas, J. K. "Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?" Journal of Accounting Research 27 (Supplement), 1989, 1-36. https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html
43. Barber, B. M., Odean, T. "Boys Will Be Boys: Gender, Overconfidence, and Common Stock Investment." Quarterly Journal of Economics 116(1), 2001, 261-292. https://ideas.repec.org/a/oup/qjecon/v116y2001i1p261-292..html
44. Odean, T. "Are Investors Reluctant to Realize Their Losses?" Journal of Finance 53(5), 1998, 1775-1798. https://doi.org/10.1111/0022-1082.00072 (page blocked, abstract not retrieved).
45. Shefrin, H., Statman, M. "The Disposition to Sell Winners Too Early and Ride Losers Too Long: Theory and Evidence." Journal of Finance 40(3), 1985, 777-790. https://ideas.repec.org/a/bla/jfinan/v40y1985i3p777-90.html
46. Tversky, A., Kahneman, D. "Advances in Prospect Theory: Cumulative Representation of Uncertainty." Journal of Risk and Uncertainty 5(4), 1992, 297-323. https://ideas.repec.org/a/kap/jrisku/v5y1992i4p297-323.html
47. Barber, B. M., Huang, X., Odean, T., Schwarz, C. "Attention-Induced Trading and Returns: Evidence from Robinhood Users." Journal of Finance 77(6), 2022, 3141-3190. https://ideas.repec.org/a/bla/jfinan/v77y2022i6p3141-3190.html
48. Family Wealth Report. "Equities Top-Performing Liquid Asset - UBS Yearbook" (report on UBS Global Investment Returns Yearbook 2026, by Dimson, Marsh, Staunton), 3 March 2026. https://www.familywealthreport.com/article.php/Equities-Top_dash_Performing-Liquid-Asset-%E2%80%93-UBS-Yearbook?id=207071 (secondary report; the UBS yearbook itself was not opened).
49. MSCI. "MSCI World Index factsheet." https://www.msci.com/documents/10199/178e6643-6ae6-47b9-82be-e1fc565ededb (PDF not text-extractable here; no figures taken).
50. BaFin. "Allgemeinverfügung zur Anhebung der Meldeschwelle für Eigengeschäfte von Führungskräften" (general ruling, 4 Dec 2025). https://www.bafin.de/SharedDocs/Veroeffentlichungen/DE/Aufsichtsrecht/Verfuegung/vf_20251204_meldeschwelle_kraft.html (accessed 2026-10-17).
51. UBS. Global Investment Returns Yearbook 2026, article. https://www.ubs.com/global/en/wealthmanagement/insights/marketnews/article.3435923.html (accessed 2026-10-17).
