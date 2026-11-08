# Setup zones - 08 Nov 2026 (setuplab v0.8)

Freeze FROZEN_SETUPS.json (sha256 483f1539324f3ae5); tags TAGS_20261108_001; whole market: every stock-day in C:\QuantData\cache_daily\panel_oc\panel.parquet from 2020-01-01 (held 5 sessions).

**The rule (declared before any zone result):** zones v1, declared 8 Nov 2026 before any zone result. Every dimension is read at the close before the entry (the close the setup's own conditions are read at). A candidate is one range of one dimension, or two ranges of two dimensions. It must keep 40 trades a year in each population. It QUALIFIES when, in every population (picks: D and ENS; the whole market: one), inside minus outside (net % per trade) has a 95% interval above 0 and the check (picks: the lift over the model's D1 entry on the same picks; the whole market: the excess over buying every stock at the same open) has a 95% interval above 0. The winner is the qualifying zone whose net per trade has the highest strict lower bound (mean - 3.29 bootstrap standard deviations, 99.9%) in its weakest population - the strict level only RANKS the qualifiers, so a narrow lucky slice does not beat a broad real one. None qualifies = no zone. Plain 95% per candidate (Karan's choice, 8 Nov): about 1 in 20 candidates passes by luck, so the same search is replayed year by year (choose with exits before 1 Jan, judge on that year): HOLDS only if inside beats outside out of sample.

**ATR check** (S1's 1-ATR dip; the whole market and the chart compute the ATR themselves): 32057 of 32076 picks: pick_meta's s_atr14 = the simple ATR14 / close from the bars (within 1e-6)

Money: Rs a year at Rs 1 L a trade = net %% per trade x trades a year x Rs 1,000 (one position of Rs 1 L per trade, no compounding, skipped trades in cash).

## Verdicts

| setup | picks: zone | picks: out of sample (D / ENS) | whole market: zone | whole market: out of sample |
|---|---|---|---|---|
| S1 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & TREND close vs EMA50 and EMA200: below both to between | NOT SHOWN / NOT SHOWN | TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30 | NOT SHOWN |
| S2 | ATRP ATR14 % of the close: 2 and above & DD52 % from the highest close of the last 252 sessions: below -5 | NOT SHOWN / HOLDS | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | HOLDS |
| S3 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | NOT SHOWN / HOLDS | TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30 | NOT SHOWN |
| C1 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | NOT SHOWN / NOT SHOWN | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | NOT SHOWN |
| C2 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | NOT SHOWN / HOLDS | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | HOLDS |
| C3 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & TREND close vs EMA50 and EMA200: between | NOT SHOWN / HOLDS | TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30 | WORSE |
| N1 | ATRP ATR14 % of the close: 4.5 and above & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | NOT SHOWN / NOT SHOWN | TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30 | NOT SHOWN |

HOLDS = inside beat outside out of sample (95%). NOT SHOWN = it did not. A zone is a hypothesis until the forward record (ON TIME scans) confirms it; the nightly scan marks every setup IN ZONE or OUTSIDE and the forward record keeps both.

## S1 - Bad week + WQ-16 rising + 1-ATR dip

### Picks (D and ENS, primary exit original_d5) - the zone: ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & TREND close vs EMA50 and EMA200: below both to between

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 110 | +1.47 [+0.72, +2.21] | 161,505 | +8.13 [+7.28, +8.85] | 121 | +1.52 [+0.87, +2.18] | 184,388 | +7.80 [+6.91, +8.63] |
| inside the zone | 43 | +3.20 [+1.89, +4.39] | 137,694 | +10.25 [+9.37, +11.19] | 43 | +2.94 [+1.70, +4.04] | 126,866 | +10.29 [+9.41, +11.11] |
| outside the zone | 67 | +0.35 | 23,810 |  | 78 | +0.74 | 57,522 | |

Inside minus outside (net % per trade): D +2.85 [+1.52, +3.99]; ENS +2.20 [+0.86, +3.33].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 40.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +1.80 vs outside +1.28, inside minus outside +0.52 [-1.19, +2.01], 5 years with a zone; ENS NOT SHOWN - inside +1.85 vs outside +1.54, inside minus outside +0.31 [-1.48, +1.76], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | DD52 % from the highest close of the last 252 sessions: below -15 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 114 | 17 | +1.91 | +0.59 | 127 | 10 | +2.46 | +0.94 |
| 2023 | TREND close vs EMA50 and EMA200: below both to between & VIX5 India VIX 5-session change %: below 10 | 83 | 31 | +0.83 | +0.66 | 110 | 37 | +0.15 | +0.85 |
| 2024 | ATRP ATR14 % of the close: 2 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 99 | 38 | +1.45 | +2.41 | 110 | 33 | +0.84 | +2.22 |
| 2025 | ATRP ATR14 % of the close: 3 and above & TREND close vs EMA50 and EMA200: below both to between | 139 | 110 | +2.28 | +1.89 | 145 | 112 | +2.53 | +2.09 |
| 2026 | DD52 % from the highest close of the last 252 sessions: below -15 & VIX5 India VIX 5-session change %: -10 to 10 | 79 | 41 | +1.52 | +1.98 | 100 | 45 | +2.17 | +2.28 |

### Whole market (every stock, held 5 sessions) - the zone: TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 4743 | +0.60 [-0.09, +1.28] | 2,853,695 | +0.20 [+0.11, +0.29] |
| inside the zone | 58 | +2.56 [+1.03, +3.74] | 147,359 | +1.40 [+0.90, +1.98] |
| outside the zone | 4685 | +0.58 | 2,706,337 | |

Inside minus outside (net % per trade): MKT +1.98 [+0.81, +2.92].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 13.

**Out of sample (the search replayed year by year):** MKT NOT SHOWN - inside +2.14 vs outside +0.50, inside minus outside +1.64 [-0.44, +2.97], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: -3 and above | 4663 | 331 | +4.73 | +0.24 |
| 2023 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 3546 | 337 | +1.36 | +0.46 |
| 2024 | RS20 20-session return minus Smallcap 250's (pts): 5 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 5568 | 221 | -0.19 | +1.09 |
| 2025 | ATRP ATR14 % of the close: 4.5 and above & VIX5 India VIX 5-session change %: -10 to 10 | 6492 | 1686 | +3.22 | +1.67 |
| 2026 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 4912 | 406 | -2.53 | -0.45 |


## S2 - Bad week + minus-DI 5-day change rising + gap down

### Picks (D and ENS, primary exit original_d5) - the zone: ATRP ATR14 % of the close: 2 and above & DD52 % from the highest close of the last 252 sessions: below -5

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 209 | +1.59 [+0.93, +2.29] | 333,920 | +3.58 [+3.01, +4.14] | 238 | +1.50 [+0.91, +2.12] | 356,626 | +3.25 [+2.71, +3.76] |
| inside the zone | 175 | +1.83 [+1.08, +2.58] | 320,080 | +4.15 [+3.61, +4.65] | 193 | +1.76 [+1.08, +2.46] | 339,570 | +3.83 [+3.33, +4.30] |
| outside the zone | 34 | +0.40 | 13,840 |  | 45 | +0.38 | 17,057 | |

Inside minus outside (net % per trade): D +1.43 [+0.54, +2.32]; ENS +1.39 [+0.36, +2.42].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 10.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +0.15 vs outside -0.13, inside minus outside +0.29 [-0.34, +1.09], 1 years with a zone; ENS HOLDS - inside +1.10 vs outside -0.29, inside minus outside +1.39 [+0.70, +2.33], 1 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | none (no zone (the setup alone)) | 240 |  |  | +1.72 | 250 |  |  | +1.39 |
| 2023 | none (no zone (the setup alone)) | 145 |  |  | +0.63 | 173 |  |  | +0.35 |
| 2024 | none (no zone (the setup alone)) | 231 |  |  | +1.21 | 266 |  |  | +1.10 |
| 2025 | none (no zone (the setup alone)) | 210 |  |  | +2.55 | 245 |  |  | +2.04 |
| 2026 | ATRP ATR14 % of the close: 3 and above | 155 | 140 | +0.15 | +0.13 | 190 | 154 | +1.10 | +0.83 |

### Whole market (every stock, held 5 sessions) - the zone: RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 3134 | +0.49 [-0.09, +1.07] | 1,549,378 | +0.44 [+0.34, +0.55] |
| inside the zone | 202 | +3.37 [+1.63, +4.64] | 682,337 | +1.62 [+1.00, +2.58] |
| outside the zone | 2931 | +0.30 | 867,041 | |

Inside minus outside (net % per trade): MKT +3.08 [+1.43, +4.31].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 4.

**Out of sample (the search replayed year by year):** MKT HOLDS - inside +3.11 vs outside +0.39, inside minus outside +2.72 [+2.04, +4.84], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 0 to 1 & VIXP India VIX percentile in its last 250 sessions: below 33.3333 | 2999 | 57 | +3.11 | +0.01 |
| 2023 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 2202 | 0 |  | +0.64 |
| 2024 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 3817 | 0 |  | +0.84 |
| 2025 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 4079 | 0 |  | +0.95 |
| 2026 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 3756 | 0 |  | -0.47 |


## S3 - Bad week + WQ-40 rising + 3% dip

### Picks (D and ENS, primary exit original_d5) - the zone: RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 159 | +1.49 [+0.88, +2.07] | 238,114 | +7.03 [+6.56, +7.45] | 171 | +1.39 [+0.82, +1.94] | 237,768 | +6.87 [+6.35, +7.35] |
| inside the zone | 44 | +3.69 [+2.53, +4.87] | 162,483 | +8.20 [+7.56, +8.77] | 45 | +4.08 [+2.73, +5.27] | 184,533 | +8.15 [+7.52, +8.63] |
| outside the zone | 115 | +0.66 | 75,630 |  | 125 | +0.42 | 53,235 | |

Inside minus outside (net % per trade): D +3.03 [+1.55, +4.58]; ENS +3.65 [+1.93, +5.31].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 39.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +2.61 vs outside +1.06, inside minus outside +1.55 [-0.11, +3.24], 5 years with a zone; ENS HOLDS - inside +2.63 vs outside +0.90, inside minus outside +1.73 [+0.23, +3.19], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 183 | 16 | +0.95 | +0.44 | 186 | 14 | +1.03 | +0.22 |
| 2023 | DD52 % from the highest close of the last 252 sessions: below -30 & VIX5 India VIX 5-session change %: below 10 | 80 | 15 | +6.95 | +1.99 | 103 | 22 | +3.78 | +0.68 |
| 2024 | RET20 20-session return %: below -10 & VIX5 India VIX 5-session change %: below 10 | 173 | 46 | +1.39 | +2.18 | 186 | 53 | +1.77 | +1.72 |
| 2025 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & VIX5 India VIX 5-session change %: -10 to 10 | 214 | 118 | +2.47 | +1.71 | 222 | 111 | +2.46 | +1.86 |
| 2026 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 117 | 35 | +3.59 | +1.61 | 128 | 35 | +4.38 | +2.38 |

### Whole market (every stock, held 5 sessions) - the zone: TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 5256 | +0.42 [-0.23, +1.00] | 2,208,314 | +0.17 [+0.08, +0.26] |
| inside the zone | 54 | +2.65 [+1.38, +3.67] | 143,631 | +1.72 [+1.06, +2.52] |
| outside the zone | 5201 | +0.40 | 2,064,683 | |

Inside minus outside (net % per trade): MKT +2.26 [+1.22, +3.12].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 9.

**Out of sample (the search replayed year by year):** MKT NOT SHOWN - inside +1.23 vs outside +0.51, inside minus outside +0.73 [-1.30, +2.48], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 to 2 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 4941 | 254 | +5.29 | +0.02 |
| 2023 | VIXP India VIX percentile in its last 250 sessions: 33.3333 to 66.6667 & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | 3793 | 424 | +0.19 | +0.46 |
| 2024 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 6546 | 452 | +0.52 | +0.51 |
| 2025 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: -3 and above | 6665 | 447 | +3.14 | +1.52 |
| 2026 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 5225 | 321 | -2.25 | -0.03 |


## C1 - Bad week + minus-DI rising + 2% dip

### Picks (D and ENS, primary exit original_d5) - the zone: RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 308 | +1.19 [+0.62, +1.71] | 365,366 | +6.27 [+5.81, +6.70] | 321 | +1.14 [+0.61, +1.63] | 364,638 | +6.05 [+5.51, +6.54] |
| inside the zone | 83 | +2.93 [+1.79, +4.13] | 243,815 | +7.24 [+6.57, +7.80] | 78 | +2.90 [+1.69, +4.05] | 227,442 | +7.30 [+6.48, +7.96] |
| outside the zone | 225 | +0.54 | 121,551 |  | 243 | +0.57 | 137,196 | |

Inside minus outside (net % per trade): D +2.39 [+1.02, +3.84]; ENS +2.34 [+0.82, +3.77].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 40.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +2.14 vs outside +0.58, inside minus outside +1.56 [-0.15, +3.14], 5 years with a zone; ENS NOT SHOWN - inside +2.19 vs outside +0.66, inside minus outside +1.53 [-0.13, +3.09], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 355 | 80 | +3.57 | +0.46 | 369 | 96 | +2.49 | +0.50 |
| 2023 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 174 | 66 | +2.94 | +0.90 | 205 | 75 | +2.87 | +1.27 |
| 2024 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 337 | 52 | +0.84 | +1.25 | 360 | 57 | +0.93 | +0.86 |
| 2025 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 346 | 199 | +2.19 | +1.53 | 350 | 179 | +2.73 | +1.46 |
| 2026 | RSI14 RSI 14: below 30 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 251 | 45 | -0.28 | +1.06 | 288 | 54 | +0.23 | +1.65 |

### Whole market (every stock, held 5 sessions) - the zone: IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 8407 | +0.27 [-0.22, +0.76] | 2,237,922 | +0.10 [+0.04, +0.17] |
| inside the zone | 157 | +5.90 [+2.56, +6.72] | 924,543 | +1.00 [+0.47, +1.40] |
| outside the zone | 8251 | +0.16 | 1,313,378 | |

Inside minus outside (net % per trade): MKT +5.74 [+2.23, +6.84].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 21.

**Out of sample (the search replayed year by year):** MKT NOT SHOWN - inside -0.10 vs outside +0.22, inside minus outside -0.32 [-5.10, +6.56], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 8155 | 493 | +4.96 | -0.39 |
| 2023 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 6204 | 0 |  | +0.31 |
| 2024 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 to 2 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 10438 | 552 | -4.63 | +0.36 |
| 2025 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 9991 | 0 |  | +0.86 |
| 2026 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 8756 | 0 |  | -0.21 |


## C2 - B + 3% dip (bad week + EMA20 angle falling + 3% dip)

### Picks (D and ENS, primary exit original_d5) - the zone: RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 282 | +1.17 [+0.52, +1.79] | 329,540 | +7.05 [+6.57, +7.48] | 281 | +1.17 [+0.54, +1.72] | 328,280 | +6.97 [+6.44, +7.43] |
| inside the zone | 69 | +3.27 [+2.15, +4.36] | 225,890 | +8.09 [+7.48, +8.58] | 67 | +3.43 [+2.36, +4.40] | 230,651 | +8.13 [+7.42, +8.71] |
| outside the zone | 213 | +0.49 | 103,650 |  | 213 | +0.46 | 97,629 | |

Inside minus outside (net % per trade): D +2.78 [+1.38, +4.23]; ENS +2.97 [+1.61, +4.36].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 39.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +2.22 vs outside +0.90, inside minus outside +1.32 [-0.49, +3.07], 5 years with a zone; ENS HOLDS - inside +2.50 vs outside +0.85, inside minus outside +1.66 [+0.07, +3.15], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | RSI14 RSI 14: below 30 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 322 | 14 | +4.40 | +0.51 | 318 | 8 | +2.87 | +0.69 |
| 2023 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 138 | 57 | +2.90 | +1.13 | 153 | 68 | +2.36 | +1.13 |
| 2024 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 315 | 38 | +2.26 | +1.64 | 317 | 44 | +1.40 | +0.99 |
| 2025 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 320 | 167 | +2.33 | +1.52 | 313 | 147 | +3.27 | +1.60 |
| 2026 | RSI14 RSI 14: below 30 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 215 | 38 | -0.16 | +1.23 | 232 | 44 | +1.22 | +1.89 |

### Whole market (every stock, held 5 sessions) - the zone: IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 7975 | +0.23 [-0.47, +0.84] | 1,798,197 | +0.14 [+0.07, +0.21] |
| inside the zone | 152 | +6.05 [+2.75, +6.79] | 920,618 | +1.12 [+0.66, +1.58] |
| outside the zone | 7823 | +0.11 | 877,580 | |

Inside minus outside (net % per trade): MKT +5.94 [+2.34, +7.13].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 10.

**Out of sample (the search replayed year by year):** MKT HOLDS - inside +4.60 vs outside +0.32, inside minus outside +4.28 [+1.41, +6.51], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: -3 and above | 7607 | 535 | +4.60 | -0.28 |
| 2023 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 5646 | 0 |  | +0.47 |
| 2024 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 10187 | 0 |  | +0.35 |
| 2025 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 9165 | 0 |  | +1.00 |
| 2026 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: 3 and above | 7569 | 0 |  | +0.27 |


## C3 - A+C, no dip (bad week + EMA20 angle falling + WQ-44 rising + Bollinger width rising)

### Picks (D and ENS, primary exit original_d5) - the zone: ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & TREND close vs EMA50 and EMA200: between

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 240 | +1.29 [+0.45, +2.06] | 309,475 | +2.89 [+2.40, +3.32] | 262 | +1.28 [+0.55, +1.91] | 337,163 | +3.00 [+2.53, +3.43] |
| inside the zone | 41 | +3.03 [+1.66, +4.14] | 123,419 | +3.36 [+2.59, +4.00] | 50 | +3.30 [+2.11, +4.36] | 163,722 | +3.57 [+2.77, +4.24] |
| outside the zone | 199 | +0.94 | 186,056 |  | 213 | +0.82 | 173,441 | |

Inside minus outside (net % per trade): D +2.09 [+0.63, +3.43]; ENS +2.48 [+1.10, +3.80].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 21.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +2.12 vs outside +0.98, inside minus outside +1.14 [-0.54, +2.92], 5 years with a zone; ENS HOLDS - inside +2.53 vs outside +0.89, inside minus outside +1.64 [+0.20, +3.03], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | RSI14 RSI 14: below 30 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 284 | 17 | +1.13 | +1.25 | 282 | 20 | -0.86 | +1.33 |
| 2023 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 165 | 37 | +3.38 | +0.82 | 229 | 55 | +3.65 | +1.01 |
| 2024 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 214 | 48 | +2.46 | +1.46 | 238 | 53 | +2.14 | +1.66 |
| 2025 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: below 10 | 298 | 176 | +2.60 | +2.21 | 312 | 160 | +3.26 | +1.95 |
| 2026 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 168 | 54 | -0.27 | +0.15 | 207 | 55 | +0.87 | +0.38 |

### Whole market (every stock, held 5 sessions) - the zone: TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 3783 | +0.36 [-0.30, +0.97] | 1,375,456 | +0.15 [+0.05, +0.24] |
| inside the zone | 50 | +2.62 [+0.99, +3.91] | 131,528 | +1.46 [+0.85, +2.10] |
| outside the zone | 3733 | +0.33 | 1,243,928 | |

Inside minus outside (net % per trade): MKT +2.28 [+0.97, +3.30].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 11.

**Out of sample (the search replayed year by year):** MKT WORSE - inside -0.52 vs outside +0.47, inside minus outside -0.99 [-1.93, -0.09], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 0 to 1 & VIXP India VIX percentile in its last 250 sessions: below 33.3333 | 3680 | 111 | +1.46 | -0.22 |
| 2023 | VIXP India VIX percentile in its last 250 sessions: 33.3333 to 66.6667 & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | 2864 | 194 | +0.21 | +0.21 |
| 2024 | VIXP India VIX percentile in its last 250 sessions: 33.3333 to 66.6667 & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | 4346 | 744 | -0.46 | +0.58 |
| 2025 | TREND close vs EMA50 and EMA200: between & RS20 20-session return minus Smallcap 250's (pts): below -5 | 5071 | 359 | +0.45 | +1.42 |
| 2026 | RSI14 RSI 14: below 30 & VIX5 India VIX 5-session change %: -10 to 10 | 3963 | 305 | -2.97 | -0.44 |


## N1 - Below the lower Bollinger band + 2% dip (any weekday)

### Picks (D and ENS, primary exit fresh) - the zone: ATRP ATR14 % of the close: 4.5 and above & NIFTY20 NIFTY 50 20-session return %: -3 to 3

| | D trades/yr | D net % per trade [95%] | D Rs a year at Rs 1 L a trade | D lift over D1 [95%] | ENS trades/yr | ENS net % per trade [95%] | ENS Rs a year at Rs 1 L a trade | ENS lift over D1 [95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| the setup alone | 243 | +1.41 [+0.08, +2.60] | 343,892 | +6.49 [+5.79, +7.15] | 290 | +1.51 [+0.53, +2.47] | 438,088 | +6.32 [+5.80, +6.85] |
| inside the zone | 88 | +2.70 [+1.35, +4.01] | 238,669 | +7.00 [+6.10, +7.85] | 93 | +2.63 [+1.39, +3.96] | 243,850 | +6.63 [+5.89, +7.45] |
| outside the zone | 155 | +0.68 | 105,223 |  | 197 | +0.99 | 194,238 | |

Inside minus outside (net % per trade): D +2.02 [+0.01, +3.98]; ENS +1.64 [+0.01, +3.38].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 7.

**Out of sample (the search replayed year by year):** D NOT SHOWN - inside +1.06 vs outside +2.50, inside minus outside -1.44 [-3.46, +0.78], 5 years with a zone; ENS NOT SHOWN - inside +0.94 vs outside +2.00, inside minus outside -1.06 [-2.94, +1.09], 5 years with a zone

| year | zone chosen with exits before 1 Jan | D trades | D in zone | D net in zone | D net all | ENS trades | ENS in zone | ENS net in zone | ENS net all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | DD52 % from the highest close of the last 252 sessions: below -15 & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 to 2 | 275 | 27 | -3.28 | +1.55 | 322 | 32 | -0.73 | +1.54 |
| 2023 | RSI14 RSI 14: below 30 & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 219 | 77 | +3.24 | +2.38 | 266 | 90 | +1.92 | +1.63 |
| 2024 | ATRX ATR14 % / its mean of the last 50 sessions: 1.15 and above & VIXP India VIX percentile in its last 250 sessions: below 66.6667 | 181 | 10 | -0.70 | +4.37 | 250 | 14 | -1.85 | +2.67 |
| 2025 | ATRP ATR14 % of the close: 4.5 and above & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | 288 | 135 | +2.31 | +1.72 | 359 | 163 | +2.30 | +1.77 |
| 2026 | RET20 20-session return %: below -10 & NIFTY20 NIFTY 50 20-session return %: -3 to 3 | 201 | 113 | -0.71 | +0.79 | 258 | 107 | -1.08 | +0.95 |

### Whole market (every stock, held 5 sessions) - the zone: TREND close vs EMA50 and EMA200: between & RSI14 RSI 14: below 30

| | MKT trades/yr | MKT net % per trade [95%] | MKT Rs a year at Rs 1 L a trade | MKT excess [95%] |
|---|---:|---:|---:|---:|
| the setup alone | 7936 | +0.13 [-0.74, +0.90] | 1,053,816 | +0.14 [+0.04, +0.25] |
| inside the zone | 203 | +1.80 [+0.89, +2.62] | 365,478 | +1.34 [+0.92, +1.72] |
| outside the zone | 7734 | +0.09 | 688,338 | |

Inside minus outside (net % per trade): MKT +1.72 [+1.04, +2.28].

Candidates tested: 2990; finalists bootstrapped: 40; qualifying: 21.

**Out of sample (the search replayed year by year):** MKT NOT SHOWN - inside +0.77 vs outside +0.47, inside minus outside +0.30 [-1.20, +1.70], 5 years with a zone

| year | zone chosen with exits before 1 Jan | MKT trades | MKT in zone | MKT net in zone | MKT net all |
|---|---|---:|---:|---:|---:|
| 2022 | ATRP ATR14 % of the close: 4.5 and above & VIXP India VIX percentile in its last 250 sessions: 33.3333 to 66.6667 | 8544 | 209 | -0.05 | +0.43 |
| 2023 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 0 & VIXP India VIX percentile in its last 250 sessions: below 33.3333 | 5867 | 2799 | +0.76 | +0.55 |
| 2024 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 & NIFTY20 NIFTY 50 20-session return %: -3 and above | 9869 | 1688 | +0.73 | +1.07 |
| 2025 | TREND close vs EMA50 and EMA200: between to above both & RSI14 RSI 14: below 30 | 10475 | 139 | +1.75 | +0.48 |
| 2026 | TREND close vs EMA50 and EMA200: between to above both & RSI14 RSI 14: below 30 | 8475 | 65 | +2.62 | -0.09 |

