# setuplab leaderboard - the declared rule over every setup (setuplab v0.6)

Engines D, ENS; D 15819 picks, ENS 16257 picks. 8282 setups x 2 exits tested in every engine; eligible: both exits 688, original_d5 732, fresh 1302.

## The rule

- Declared 7 Nov 2026 (13:00 IST) before the final run, applied by the code - nobody picks by eye.
- Universe: every setup of the run - controls and price-only rules, the A/B/C labels (with and without confirmations and dips), every single feature and pair, the dip exploration, every setup x confluence and every confluence alone - each counted once by its conditions, and only if it was tested in every engine of the run.
- ELIGIBLE (for one exit) when in EVERY engine: (1) at least 300 trades; (2) the lift over the model's D1 entry on its own trades has a 95% interval above 0 (Karan's comparison); (3) when it has an indicator-free twin (the same dip / confluence without the indicator conditions), the indicators add with a 95% interval above 0; (4) trades in at least 6 signal years and net per trade above 0 in all but at most one; (5) net per trade above 0 in both halves of the period.
- (6) A context filter (a condition on the pick's snapshot at the signal: state, market, NIFTY, VIX, breadth, the volatility flag, the rank) only chooses WHICH trades to take: it must keep better trades than it drops - the same setup's trades with the filter minus those without it - and pass after counting EVERY filter test of the run (thousands: each setup meets every context filter, alone and with each price confluence): a false discovery rate of at most 5% (Benjamini-Hochberg), in every engine. Otherwise a filter that kept a lucky subset would float a setup to the top: a filtered setup gets no more chances to pass by luck than a plain one.
- SCORE = the lower end of the 95% interval of net per trade (after 0.35 pp) in the worst engine: money per trade, marked down for small samples and for disagreement between the engines.
- Lists: BOTH EXITS (eligible under original_d5 AND fresh; score = the lower of the two) is the main list; each exit on its own follows.
- Top 3 = the best scores, skipping VERSIONS of a setup already chosen: a setup whose rule (leaving out the context filters) contains the other's rule or is contained in it, or whose trades overlap 70% or more with it (of the smaller set, first engine). Different setups, not versions of one.

## BOTH EXITS - the top 3

### 1. w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1  (confluence)

**Rule:** d_wq_16 rose on the previous session; yesterday's close more than 1 ATR below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 733 | 110 | 4.6 | +1.4659 | +0.7399 .. +2.2107 | -6.6636 | +8.1295 [+7.5665, +8.6755] | +1.1305 [+0.8529, +1.4088] | 6/7 | +1.23 / +1.70 | 0.9 / 22 (22) |
| D | fresh | 733 | 110 | 4.6 | +2.1034 | +0.7876 .. +3.4141 | -6.6636 | +8.7670 [+7.7211, +9.8457] | +1.1547 [+0.6672, +1.6237] | 6/7 | +1.02 / +3.18 | 2.2 / 22 (22) |
| ENS | original_d5 | 806 | 121 | 5.0 | +1.5220 | +0.7954 .. +2.2892 | -6.2803 | +7.8023 [+7.1631, +8.3856] | +1.1427 [+0.7864, +1.5512] | 7/7 | +0.96 / +2.04 | 1.0 / 24 (24) |
| ENS | fresh | 806 | 121 | 5.0 | +2.3973 | +1.1368 .. +3.6643 | -6.2803 | +8.6776 [+7.6620, +9.7031] | +1.2139 [+0.7206, +1.7520] | 6/7 | +1.32 / +3.38 | 2.4 / 24 (24) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_wq_16_change>0 || DIP3 (place 6, score +0.6500); B+C&DIP_3 (place 7, score +0.5398); X2|w_ret_13w_change<0&d_mdi14_change>0 (place 8, score +0.5226); w_ret_13w_change<0&d_mdi14_change>0 || DIP3 (place 9, score +0.5178); w_ret_13w_change<0&d_mdi14_change>0 || DIPATR1 (place 10, score +0.5125).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/both_exits_1__D.csv`, `FINALISTS/both_exits_1__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.79 (202) | +1.34 (531) | +2.81 (249) | +0.77 (484) | 2020 -0.09 (119), 2021 +2.94 (102), 2022 +0.65 (112), 2023 +0.62 (84), 2024 +2.54 (100), 2025 +1.74 (139), 2026 +2.12 (77) |
| D | fresh | +2.36 (202) | +2.00 (531) | +4.04 (249) | +1.11 (484) | 2020 -1.79 (119), 2021 +4.09 (102), 2022 +0.44 (112), 2023 +1.93 (84), 2024 +3.56 (100), 2025 +4.47 (139), 2026 +1.94 (77) |
| ENS | original_d5 | +1.21 (234) | +1.65 (572) | +2.84 (252) | +0.92 (554) | 2020 +0.11 (101), 2021 +1.99 (114), 2022 +0.96 (126), 2023 +0.83 (111), 2024 +2.32 (110), 2025 +1.92 (147), 2026 +2.45 (97) |
| ENS | fresh | +2.46 (234) | +2.37 (572) | +3.98 (252) | +1.68 (554) | 2020 -0.96 (101), 2021 +3.30 (114), 2022 +1.37 (126), 2023 +1.83 (111), 2024 +3.27 (110), 2025 +4.46 (147), 2026 +2.69 (97) |

### 2. w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN  (confluence)

**Rule:** d_mdi14_diff5 rose on the previous session; opens below yesterday's close (gap down); w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 1393 | 209 | 8.8 | +1.5948 | +0.7375 .. +2.4815 | -1.9864 | +3.5812 [+3.1245, +4.0343] | +2.0560 [+1.6902, +2.4405] | 7/7 | +1.99 / +1.21 | 2.8 / 37 (37) |
| D | fresh | 1393 | 209 | 8.8 | +2.0907 | +0.9890 .. +3.2570 | -1.9864 | +4.0771 [+3.4621, +4.6889] | +2.2710 [+1.8585, +2.6442] | 7/7 | +2.45 / +1.73 | 4.2 / 43 (37) |
| ENS | original_d5 | 1583 | 237 | 9.7 | +1.4988 | +0.7245 .. +2.3720 | -1.7511 | +3.2499 [+2.8146, +3.6558] | +1.9205 [+1.5930, +2.2707] | 7/7 | +1.88 / +1.15 | 3.1 / 38 (38) |
| ENS | fresh | 1583 | 237 | 9.7 | +1.9207 | +0.8509 .. +3.1805 | -1.7511 | +3.6717 [+3.0603, +4.3440] | +2.1497 [+1.7403, +2.5742] | 7/7 | +2.46 / +1.42 | 4.8 / 46 (38) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_mdi14_change>0 || GAPDOWN (place 34, score +0.3278); w_ret_13w_change<0&d_ll_run_change>0 || GAPDOWN (place 40, score +0.2907); w_ret_13w_change<0&d_lh_run_change>0 || GAPDOWN (place 124, score +0.1466).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/both_exits_2__D.csv`, `FINALISTS/both_exits_2__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.92 (423) | +1.45 (970) | +2.50 (504) | +1.08 (889) | 2020 +1.73 (222), 2021 +2.65 (192), 2022 +1.69 (238), 2023 +0.62 (146), 2024 +1.26 (231), 2025 +2.51 (209), 2026 +0.13 (155) |
| D | fresh | +2.59 (423) | +1.87 (970) | +3.36 (504) | +1.37 (889) | 2020 +2.07 (222), 2021 +3.57 (192), 2022 +1.94 (238), 2023 +1.08 (146), 2024 +1.74 (231), 2025 +3.39 (209), 2026 +0.24 (155) |
| ENS | original_d5 | +2.07 (504) | +1.23 (1079) | +2.94 (517) | +0.80 (1066) | 2020 +2.21 (254), 2021 +2.20 (205), 2022 +1.39 (250), 2023 +0.29 (180), 2024 +1.20 (260), 2025 +2.01 (244), 2026 +0.83 (190) |
| ENS | fresh | +2.64 (504) | +1.59 (1079) | +3.88 (517) | +0.97 (1066) | 2020 +3.54 (254), 2021 +2.56 (205), 2022 +1.70 (250), 2023 +0.26 (180), 2024 +1.31 (260), 2025 +2.32 (244), 2026 +1.24 (190) |

### 3. w_ret_13w_change<0&d_wq_40_change>0 || DIP3  (confluence)

**Rule:** d_wq_40 rose on the previous session; yesterday's close more than 3% below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 1061 | 159 | 6.7 | +1.4931 | +0.8452 .. +2.1482 | -5.5366 | +7.0297 [+6.6076, +7.4114] | +1.4840 [+1.1727, +1.7974] | 7/7 | +1.28 / +1.69 | 1.5 / 27 (27) |
| D | fresh | 1061 | 159 | 6.7 | +1.9453 | +0.7017 .. +3.1540 | -5.5366 | +7.4819 [+6.5953, +8.3869] | +1.6591 [+1.1596, +2.1775] | 6/7 | +1.46 / +2.41 | 3.2 / 27 (27) |
| ENS | original_d5 | 1135 | 170 | 7.0 | +1.3937 | +0.7074 .. +2.0685 | -5.4804 | +6.8741 [+6.4499, +7.2963] | +1.3133 [+0.9291, +1.6903] | 7/7 | +1.00 / +1.76 | 1.6 / 29 (29) |
| ENS | fresh | 1135 | 170 | 7.0 | +2.0719 | +0.8516 .. +3.3968 | -5.4804 | +7.5523 [+6.6880, +8.4755] | +1.5199 [+0.9883, +2.0933] | 7/7 | +1.73 / +2.40 | 3.4 / 29 (29) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1 (place 5, score +0.6517); w_ret_13w_change<0&d_wq_40_change>0 || DIP2 (place 12, score +0.5011); S2|w_ret_13w_change<0&d_wq_40_change>0 (place 15, score +0.4300); w_ret_13w_change<0&d_wq_40_change>0 || DIP1 (place 20, score +0.4033).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/both_exits_3__D.csv`, `FINALISTS/both_exits_3__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.34 (331) | +1.56 (730) | +2.50 (437) | +0.79 (624) | 2020 +0.40 (154), 2021 +2.47 (144), 2022 +0.43 (179), 2023 +1.99 (80), 2024 +2.22 (174), 2025 +1.61 (215), 2026 +1.71 (115) |
| D | fresh | +1.95 (331) | +1.94 (730) | +3.66 (437) | +0.74 (624) | 2020 -0.40 (154), 2021 +3.86 (144), 2022 +0.71 (179), 2023 +2.05 (80), 2024 +2.86 (174), 2025 +3.01 (215), 2026 +1.16 (115) |
| ENS | original_d5 | +1.84 (348) | +1.20 (787) | +2.76 (439) | +0.53 (696) | 2020 +1.19 (139), 2021 +1.54 (172), 2022 +0.23 (185), 2023 +0.66 (104), 2024 +1.77 (187), 2025 +1.78 (222), 2026 +2.49 (126) |
| ENS | fresh | +2.56 (348) | +1.86 (787) | +3.98 (439) | +0.87 (696) | 2020 +2.08 (139), 2021 +3.14 (172), 2022 +0.27 (185), 2023 +0.64 (104), 2024 +2.32 (187), 2025 +3.19 (222), 2026 +2.10 (126) |

#### The 20 best eligible scores, both exits (before the overlap rule)

| # | setup | family | score | D net (orig / fresh) | ENS net (orig / fresh) |
|---:|---|---|---:|---:|---:|
| 1 | w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1 * | confluence | +0.7399 | +1.47 / +2.10 | +1.52 / +2.40 |
| 2 | w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN * | confluence | +0.7245 | +1.59 / +2.09 | +1.50 / +1.92 |
| 3 | w_ret_13w_change<0&d_wq_40_change>0 || DIP3 * | confluence | +0.7017 | +1.49 / +1.95 | +1.39 / +2.07 |
| 4 | w_ret_13w_change<0&d_wq_40_change>0 || GAPDOWN | confluence | +0.6830 | +1.61 / +1.96 | +1.59 / +1.79 |
| 5 | w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1 | confluence | +0.6517 | +1.53 / +2.44 | +1.35 / +2.17 |
| 6 | w_ret_13w_change<0&d_wq_16_change>0 || DIP3 | confluence | +0.6500 | +1.45 / +1.80 | +1.39 / +2.03 |
| 7 | B+C&DIP_3 | label+dip | +0.5398 | +1.53 / +1.82 | +1.50 / +1.93 |
| 8 | X2|w_ret_13w_change<0&d_mdi14_change>0 | pair+dip | +0.5226 | +1.19 / +1.68 | +1.14 / +1.51 |
| 9 | w_ret_13w_change<0&d_mdi14_change>0 || DIP3 | confluence | +0.5178 | +1.37 / +1.88 | +1.20 / +1.67 |
| 10 | w_ret_13w_change<0&d_mdi14_change>0 || DIPATR1 | confluence | +0.5125 | +1.27 / +2.06 | +1.19 / +1.98 |
| 11 | w_ret_13w_change<0&d_wq_16_change>0 || GAPDOWN | confluence | +0.5033 | +1.54 / +1.66 | +1.56 / +1.70 |
| 12 | w_ret_13w_change<0&d_wq_40_change>0 || DIP2 | confluence | +0.5011 | +1.30 / +1.64 | +1.45 / +1.92 |
| 13 | S2|w_ret_13w_change<0&d_mdi14_diff5_change>0 | pair | +0.4665 | +1.08 / +1.49 | +0.94 / +1.25 |
| 14 | A+C&DIP_2 | label+dip | +0.4353 | +1.51 / +1.98 | +1.41 / +1.80 |
| 15 | S2|w_ret_13w_change<0&d_wq_40_change>0 | pair | +0.4300 | +0.97 / +1.28 | +0.88 / +1.13 |
| 16 | w_ret_13w_change<0&d_mdi14_change>0 || DIP1 | confluence | +0.4225 | +1.09 / +1.58 | +0.94 / +1.30 |
| 17 | A+C&DIP_1 | label+dip | +0.4130 | +1.33 / +1.78 | +1.33 / +1.66 |
| 18 | S2|w_ret_13w_change<0&x_z_d_downside_dev_60_change>0 | pair | +0.4113 | +0.86 / +1.20 | +0.88 / +1.23 |
| 19 | w_ret_13w_change<0&x_z_d_downside_dev_60_change>0 || DIPATR1 | confluence | +0.4095 | +1.19 / +1.81 | +1.40 / +2.19 |
| 20 | w_ret_13w_change<0&d_wq_40_change>0 || DIP1 | confluence | +0.4033 | +1.09 / +1.39 | +1.13 / +1.52 |

## original_d5 exit - the top 3

### 1. w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1  (confluence)

**Rule:** d_wq_16 rose on the previous session; yesterday's close more than 1 ATR below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 733 | 110 | 4.6 | +1.4659 | +0.7399 .. +2.2107 | -6.6636 | +8.1295 [+7.5665, +8.6755] | +1.1305 [+0.8529, +1.4088] | 6/7 | +1.23 / +1.70 | 0.9 / 22 (22) |
| D | fresh | 733 | 110 | 4.6 | +2.1034 | +0.7876 .. +3.4141 | -6.6636 | +8.7670 [+7.7211, +9.8457] | +1.1547 [+0.6672, +1.6237] | 6/7 | +1.02 / +3.18 | 2.2 / 22 (22) |
| ENS | original_d5 | 806 | 121 | 5.0 | +1.5220 | +0.7954 .. +2.2892 | -6.2803 | +7.8023 [+7.1631, +8.3856] | +1.1427 [+0.7864, +1.5512] | 7/7 | +0.96 / +2.04 | 1.0 / 24 (24) |
| ENS | fresh | 806 | 121 | 5.0 | +2.3973 | +1.1368 .. +3.6643 | -6.2803 | +8.6776 [+7.6620, +9.7031] | +1.2139 [+0.7206, +1.7520] | 6/7 | +1.32 / +3.38 | 2.4 / 24 (24) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): B+C&DIP_3 (place 2, score +0.7313); w_ret_13w_change<0&d_wq_16_change>0 || DIP3 (place 5, score +0.7074); B+C&DIPATR_1 (place 9, score +0.6753); w_ret_13w_change<0&d_wq_16_change>0 || DIP2 (place 11, score +0.6422); B+C&DIP_2 (place 13, score +0.5771).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/original_d5_1__D.csv`, `FINALISTS/original_d5_1__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.79 (202) | +1.34 (531) | +2.81 (249) | +0.77 (484) | 2020 -0.09 (119), 2021 +2.94 (102), 2022 +0.65 (112), 2023 +0.62 (84), 2024 +2.54 (100), 2025 +1.74 (139), 2026 +2.12 (77) |
| D | fresh | +2.36 (202) | +2.00 (531) | +4.04 (249) | +1.11 (484) | 2020 -1.79 (119), 2021 +4.09 (102), 2022 +0.44 (112), 2023 +1.93 (84), 2024 +3.56 (100), 2025 +4.47 (139), 2026 +1.94 (77) |
| ENS | original_d5 | +1.21 (234) | +1.65 (572) | +2.84 (252) | +0.92 (554) | 2020 +0.11 (101), 2021 +1.99 (114), 2022 +0.96 (126), 2023 +0.83 (111), 2024 +2.32 (110), 2025 +1.92 (147), 2026 +2.45 (97) |
| ENS | fresh | +2.46 (234) | +2.37 (572) | +3.98 (252) | +1.68 (554) | 2020 -0.96 (101), 2021 +3.30 (114), 2022 +1.37 (126), 2023 +1.83 (111), 2024 +3.27 (110), 2025 +4.46 (147), 2026 +2.69 (97) |

### 2. w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN  (confluence)

**Rule:** d_mdi14_diff5 rose on the previous session; opens below yesterday's close (gap down); w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 1393 | 209 | 8.8 | +1.5948 | +0.7375 .. +2.4815 | -1.9864 | +3.5812 [+3.1245, +4.0343] | +2.0560 [+1.6902, +2.4405] | 7/7 | +1.99 / +1.21 | 2.8 / 37 (37) |
| D | fresh | 1393 | 209 | 8.8 | +2.0907 | +0.9890 .. +3.2570 | -1.9864 | +4.0771 [+3.4621, +4.6889] | +2.2710 [+1.8585, +2.6442] | 7/7 | +2.45 / +1.73 | 4.2 / 43 (37) |
| ENS | original_d5 | 1583 | 237 | 9.7 | +1.4988 | +0.7245 .. +2.3720 | -1.7511 | +3.2499 [+2.8146, +3.6558] | +1.9205 [+1.5930, +2.2707] | 7/7 | +1.88 / +1.15 | 3.1 / 38 (38) |
| ENS | fresh | 1583 | 237 | 9.7 | +1.9207 | +0.8509 .. +3.1805 | -1.7511 | +3.6717 [+3.0603, +4.3440] | +2.1497 [+1.7403, +2.5742] | 7/7 | +2.46 / +1.42 | 4.8 / 46 (38) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_mdi14_change>0 || GAPDOWN (place 15, score +0.5614); w_ret_13w_change<0&d_ll_run_change>0 || GAPDOWN (place 16, score +0.5584); w_ret_13w_change<0&d_lh_run_change>0 || GAPDOWN (place 32, score +0.4365).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/original_d5_2__D.csv`, `FINALISTS/original_d5_2__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.92 (423) | +1.45 (970) | +2.50 (504) | +1.08 (889) | 2020 +1.73 (222), 2021 +2.65 (192), 2022 +1.69 (238), 2023 +0.62 (146), 2024 +1.26 (231), 2025 +2.51 (209), 2026 +0.13 (155) |
| D | fresh | +2.59 (423) | +1.87 (970) | +3.36 (504) | +1.37 (889) | 2020 +2.07 (222), 2021 +3.57 (192), 2022 +1.94 (238), 2023 +1.08 (146), 2024 +1.74 (231), 2025 +3.39 (209), 2026 +0.24 (155) |
| ENS | original_d5 | +2.07 (504) | +1.23 (1079) | +2.94 (517) | +0.80 (1066) | 2020 +2.21 (254), 2021 +2.20 (205), 2022 +1.39 (250), 2023 +0.29 (180), 2024 +1.20 (260), 2025 +2.01 (244), 2026 +0.83 (190) |
| ENS | fresh | +2.64 (504) | +1.59 (1079) | +3.88 (517) | +0.97 (1066) | 2020 +3.54 (254), 2021 +2.56 (205), 2022 +1.70 (250), 2023 +0.26 (180), 2024 +1.31 (260), 2025 +2.32 (244), 2026 +1.24 (190) |

### 3. w_ret_13w_change<0&d_wq_40_change>0 || DIP3  (confluence)

**Rule:** d_wq_40 rose on the previous session; yesterday's close more than 3% below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 1061 | 159 | 6.7 | +1.4931 | +0.8452 .. +2.1482 | -5.5366 | +7.0297 [+6.6076, +7.4114] | +1.4840 [+1.1727, +1.7974] | 7/7 | +1.28 / +1.69 | 1.5 / 27 (27) |
| D | fresh | 1061 | 159 | 6.7 | +1.9453 | +0.7017 .. +3.1540 | -5.5366 | +7.4819 [+6.5953, +8.3869] | +1.6591 [+1.1596, +2.1775] | 6/7 | +1.46 / +2.41 | 3.2 / 27 (27) |
| ENS | original_d5 | 1135 | 170 | 7.0 | +1.3937 | +0.7074 .. +2.0685 | -5.4804 | +6.8741 [+6.4499, +7.2963] | +1.3133 [+0.9291, +1.6903] | 7/7 | +1.00 / +1.76 | 1.6 / 29 (29) |
| ENS | fresh | 1135 | 170 | 7.0 | +2.0719 | +0.8516 .. +3.3968 | -5.4804 | +7.5523 [+6.6880, +8.4755] | +1.5199 [+0.9883, +2.0933] | 7/7 | +1.73 / +2.40 | 3.4 / 29 (29) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_wq_40_change>0 || DIP2 (place 8, score +0.6807); w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1 (place 10, score +0.6517); w_ret_13w_change<0&d_wq_40_change>0 || DIP1 (place 17, score +0.5365); S2|w_ret_13w_change<0&d_wq_40_change>0 (place 35, score +0.4300).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/original_d5_3__D.csv`, `FINALISTS/original_d5_3__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.34 (331) | +1.56 (730) | +2.50 (437) | +0.79 (624) | 2020 +0.40 (154), 2021 +2.47 (144), 2022 +0.43 (179), 2023 +1.99 (80), 2024 +2.22 (174), 2025 +1.61 (215), 2026 +1.71 (115) |
| D | fresh | +1.95 (331) | +1.94 (730) | +3.66 (437) | +0.74 (624) | 2020 -0.40 (154), 2021 +3.86 (144), 2022 +0.71 (179), 2023 +2.05 (80), 2024 +2.86 (174), 2025 +3.01 (215), 2026 +1.16 (115) |
| ENS | original_d5 | +1.84 (348) | +1.20 (787) | +2.76 (439) | +0.53 (696) | 2020 +1.19 (139), 2021 +1.54 (172), 2022 +0.23 (185), 2023 +0.66 (104), 2024 +1.77 (187), 2025 +1.78 (222), 2026 +2.49 (126) |
| ENS | fresh | +2.56 (348) | +1.86 (787) | +3.98 (439) | +0.87 (696) | 2020 +2.08 (139), 2021 +3.14 (172), 2022 +0.27 (185), 2023 +0.64 (104), 2024 +2.32 (187), 2025 +3.19 (222), 2026 +2.10 (126) |

#### The 20 best eligible scores, original_d5 (before the overlap rule)

| # | setup | family | score | D net (original_d5) | ENS net (original_d5) |
|---:|---|---|---:|---:|---:|
| 1 | w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1 * | confluence | +0.7399 | +1.47 | +1.52 |
| 2 | B+C&DIP_3 | label+dip | +0.7313 | +1.53 | +1.50 |
| 3 | w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN * | confluence | +0.7245 | +1.59 | +1.50 |
| 4 | w_ret_13w_change<0&d_wq_40_change>0 || DIP3 * | confluence | +0.7074 | +1.49 | +1.39 |
| 5 | w_ret_13w_change<0&d_wq_16_change>0 || DIP3 | confluence | +0.7074 | +1.45 | +1.39 |
| 6 | w_ret_13w_change<0&d_wq_40_change>0 || GAPDOWN | confluence | +0.6914 | +1.61 | +1.59 |
| 7 | w_ret_13w_change<0&d_wq_16_change>0 || GAPDOWN | confluence | +0.6879 | +1.54 | +1.56 |
| 8 | w_ret_13w_change<0&d_wq_40_change>0 || DIP2 | confluence | +0.6807 | +1.30 | +1.45 |
| 9 | B+C&DIPATR_1 | label+dip | +0.6753 | +1.48 | +1.56 |
| 10 | w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1 | confluence | +0.6517 | +1.53 | +1.35 |
| 11 | w_ret_13w_change<0&d_wq_16_change>0 || DIP2 | confluence | +0.6422 | +1.28 | +1.35 |
| 12 | A+C&DIP_3 | label+dip | +0.5940 | +1.71 | +1.50 |
| 13 | B+C&DIP_2 | label+dip | +0.5771 | +1.29 | +1.39 |
| 14 | A+C&DIP_2 | label+dip | +0.5765 | +1.51 | +1.41 |
| 15 | w_ret_13w_change<0&d_mdi14_change>0 || GAPDOWN | confluence | +0.5614 | +1.50 | +1.30 |
| 16 | w_ret_13w_change<0&d_ll_run_change>0 || GAPDOWN | confluence | +0.5584 | +1.30 | +1.34 |
| 17 | w_ret_13w_change<0&d_wq_40_change>0 || DIP1 | confluence | +0.5365 | +1.09 | +1.13 |
| 18 | X2|w_ret_13w_change<0&d_mdi14_change>0 | pair+dip | +0.5226 | +1.19 | +1.14 |
| 19 | w_ret_13w_change<0&d_mdi14_change>0 || DIP3 | confluence | +0.5178 | +1.37 | +1.20 |
| 20 | w_ret_13w_change<0&d_mdi14_change>0 || DIPATR1 | confluence | +0.5125 | +1.27 | +1.19 |

## fresh exit - the top 3

### 1. w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1  (confluence)

**Rule:** d_wq_40 rose on the previous session; yesterday's close more than 1 ATR below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 655 | 98 | 4.1 | +1.5346 | +0.7882 .. +2.2800 | -6.7652 | +8.2998 [+7.7242, +8.8345] | +1.2289 [+0.9195, +1.5236] | 6/7 | +1.25 / +1.81 | 0.9 / 23 (23) |
| D | fresh | 655 | 98 | 4.1 | +2.4367 | +1.0804 .. +3.8659 | -6.7652 | +9.2019 [+8.0232, +10.3638] | +1.5089 [+1.0208, +2.0234] | 6/7 | +1.61 / +3.24 | 2.0 / 23 (23) |
| ENS | original_d5 | 756 | 113 | 4.7 | +1.3525 | +0.6517 .. +2.1018 | -6.4608 | +7.8132 [+7.2069, +8.3991] | +1.1761 [+0.8379, +1.5964] | 7/7 | +0.63 / +1.99 | 1.0 / 27 (27) |
| ENS | fresh | 756 | 113 | 4.7 | +2.1697 | +0.9567 .. +3.4974 | -6.4608 | +8.6305 [+7.6215, +9.7149] | +1.3270 [+0.8374, +1.8749] | 6/7 | +1.23 / +3.01 | 2.3 / 27 (27) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_mdi14_change>0 || DIPATR1 (place 2, score +0.8628); w_ret_13w_change<0&d_wq_40_change>0 || DIP3 (place 5, score +0.7017); w_ret_13w_change<0&d_mdi14_change>0 || DIP3 (place 8, score +0.6036); X2|w_ret_13w_change<0&d_mdi14_change>0 (place 9, score +0.5929); S2|w_ret_13w_change<0&d_mdi14_diff5_change>0 (place 10, score +0.5889).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/fresh_1__D.csv`, `FINALISTS/fresh_1__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.64 (185) | +1.49 (470) | +2.60 (216) | +1.01 (439) | 2020 -0.34 (93), 2021 +2.85 (92), 2022 +0.65 (105), 2023 +1.04 (79), 2024 +3.03 (87), 2025 +1.65 (133), 2026 +2.14 (66) |
| D | fresh | +3.32 (185) | +2.09 (470) | +4.72 (216) | +1.31 (439) | 2020 -1.91 (93), 2021 +5.06 (92), 2022 +1.28 (105), 2023 +1.57 (79), 2024 +4.18 (87), 2025 +4.30 (133), 2026 +1.73 (66) |
| ENS | original_d5 | +1.21 (201) | +1.40 (555) | +2.64 (246) | +0.73 (510) | 2020 +0.26 (85), 2021 +1.20 (112), 2022 +0.52 (114), 2023 +0.98 (99), 2024 +2.23 (94), 2025 +1.67 (160), 2026 +2.53 (92) |
| ENS | fresh | +2.51 (201) | +2.05 (555) | +4.10 (246) | +1.24 (510) | 2020 -0.29 (85), 2021 +3.01 (112), 2022 +0.78 (114), 2023 +1.51 (99), 2024 +2.91 (94), 2025 +3.76 (160), 2026 +2.34 (92) |

### 2. w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN  (confluence)

**Rule:** d_mdi14_diff5 rose on the previous session; opens below yesterday's close (gap down); w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 1393 | 209 | 8.8 | +1.5948 | +0.7375 .. +2.4815 | -1.9864 | +3.5812 [+3.1245, +4.0343] | +2.0560 [+1.6902, +2.4405] | 7/7 | +1.99 / +1.21 | 2.8 / 37 (37) |
| D | fresh | 1393 | 209 | 8.8 | +2.0907 | +0.9890 .. +3.2570 | -1.9864 | +4.0771 [+3.4621, +4.6889] | +2.2710 [+1.8585, +2.6442] | 7/7 | +2.45 / +1.73 | 4.2 / 43 (37) |
| ENS | original_d5 | 1583 | 237 | 9.7 | +1.4988 | +0.7245 .. +2.3720 | -1.7511 | +3.2499 [+2.8146, +3.6558] | +1.9205 [+1.5930, +2.2707] | 7/7 | +1.88 / +1.15 | 3.1 / 38 (38) |
| ENS | fresh | 1583 | 237 | 9.7 | +1.9207 | +0.8509 .. +3.1805 | -1.7511 | +3.6717 [+3.0603, +4.3440] | +2.1497 [+1.7403, +2.5742] | 7/7 | +2.46 / +1.42 | 4.8 / 46 (38) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_wq_29_change>0 || GAPDOWN (place 27, score +0.3984); w_ret_13w_change<0&d_mdi14_change>0 || GAPDOWN (place 55, score +0.3278); w_ret_13w_change<0&d_ll_run_change>0 || GAPDOWN (place 99, score +0.2907).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/fresh_2__D.csv`, `FINALISTS/fresh_2__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.92 (423) | +1.45 (970) | +2.50 (504) | +1.08 (889) | 2020 +1.73 (222), 2021 +2.65 (192), 2022 +1.69 (238), 2023 +0.62 (146), 2024 +1.26 (231), 2025 +2.51 (209), 2026 +0.13 (155) |
| D | fresh | +2.59 (423) | +1.87 (970) | +3.36 (504) | +1.37 (889) | 2020 +2.07 (222), 2021 +3.57 (192), 2022 +1.94 (238), 2023 +1.08 (146), 2024 +1.74 (231), 2025 +3.39 (209), 2026 +0.24 (155) |
| ENS | original_d5 | +2.07 (504) | +1.23 (1079) | +2.94 (517) | +0.80 (1066) | 2020 +2.21 (254), 2021 +2.20 (205), 2022 +1.39 (250), 2023 +0.29 (180), 2024 +1.20 (260), 2025 +2.01 (244), 2026 +0.83 (190) |
| ENS | fresh | +2.64 (504) | +1.59 (1079) | +3.88 (517) | +0.97 (1066) | 2020 +3.54 (254), 2021 +2.56 (205), 2022 +1.70 (250), 2023 +0.26 (180), 2024 +1.31 (260), 2025 +2.32 (244), 2026 +1.24 (190) |

### 3. w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1  (confluence)

**Rule:** d_wq_16 rose on the previous session; yesterday's close more than 1 ATR below the D1 open; w_ret_13w fell on the previous session. Watch D1-D5 after the pick, buy at the first open where all hold; exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs.

| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] | indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |
|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|
| D | original_d5 | 733 | 110 | 4.6 | +1.4659 | +0.7399 .. +2.2107 | -6.6636 | +8.1295 [+7.5665, +8.6755] | +1.1305 [+0.8529, +1.4088] | 6/7 | +1.23 / +1.70 | 0.9 / 22 (22) |
| D | fresh | 733 | 110 | 4.6 | +2.1034 | +0.7876 .. +3.4141 | -6.6636 | +8.7670 [+7.7211, +9.8457] | +1.1547 [+0.6672, +1.6237] | 6/7 | +1.02 / +3.18 | 2.2 / 22 (22) |
| ENS | original_d5 | 806 | 121 | 5.0 | +1.5220 | +0.7954 .. +2.2892 | -6.2803 | +7.8023 [+7.1631, +8.3856] | +1.1427 [+0.7864, +1.5512] | 7/7 | +0.96 / +2.04 | 1.0 / 24 (24) |
| ENS | fresh | 806 | 121 | 5.0 | +2.3973 | +1.1368 .. +3.6643 | -6.2803 | +8.6776 [+7.6620, +9.7031] | +1.2139 [+0.7206, +1.7520] | 6/7 | +1.32 / +3.38 | 2.4 / 24 (24) |

**Versions skipped** (eligible, but the same rule with conditions or context filters added or removed, or 70%+ the same trades): w_ret_13w_change<0&d_wq_16_change>0 || DIP3 (place 7, score +0.6500); B+C&DIP_3 (place 12, score +0.5398); S2|w_ret_13w_change<0&d_wq_16_change>0 (place 26, score +0.4029); w_ret_13w_change<0&d_wq_16_change>0 || DIP1 (place 31, score +0.3730); B+C__none (place 41, score +0.3459).

Every trade (both exits, with the D1 entry on the same trade): `FINALISTS/fresh_3__D.csv`, `FINALISTS/fresh_3__ENS.csv`.

| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |
|---|---|---|---|---|---|---|
| D | original_d5 | +1.79 (202) | +1.34 (531) | +2.81 (249) | +0.77 (484) | 2020 -0.09 (119), 2021 +2.94 (102), 2022 +0.65 (112), 2023 +0.62 (84), 2024 +2.54 (100), 2025 +1.74 (139), 2026 +2.12 (77) |
| D | fresh | +2.36 (202) | +2.00 (531) | +4.04 (249) | +1.11 (484) | 2020 -1.79 (119), 2021 +4.09 (102), 2022 +0.44 (112), 2023 +1.93 (84), 2024 +3.56 (100), 2025 +4.47 (139), 2026 +1.94 (77) |
| ENS | original_d5 | +1.21 (234) | +1.65 (572) | +2.84 (252) | +0.92 (554) | 2020 +0.11 (101), 2021 +1.99 (114), 2022 +0.96 (126), 2023 +0.83 (111), 2024 +2.32 (110), 2025 +1.92 (147), 2026 +2.45 (97) |
| ENS | fresh | +2.46 (234) | +2.37 (572) | +3.98 (252) | +1.68 (554) | 2020 -0.96 (101), 2021 +3.30 (114), 2022 +1.37 (126), 2023 +1.83 (111), 2024 +3.27 (110), 2025 +4.46 (147), 2026 +2.69 (97) |

#### The 20 best eligible scores, fresh (before the overlap rule)

| # | setup | family | score | D net (fresh) | ENS net (fresh) |
|---:|---|---|---:|---:|---:|
| 1 | w_ret_13w_change<0&d_wq_40_change>0 || DIPATR1 * | confluence | +0.9567 | +2.44 | +2.17 |
| 2 | w_ret_13w_change<0&d_mdi14_change>0 || DIPATR1 | confluence | +0.8628 | +2.06 | +1.98 |
| 3 | w_ret_13w_change<0&d_mdi14_diff5_change>0 || GAPDOWN * | confluence | +0.8509 | +2.09 | +1.92 |
| 4 | w_ret_13w_change<0&d_wq_16_change>0 || DIPATR1 * | confluence | +0.7876 | +2.10 | +2.40 |
| 5 | w_ret_13w_change<0&d_wq_40_change>0 || DIP3 | confluence | +0.7017 | +1.95 | +2.07 |
| 6 | w_ret_13w_change<0&d_wq_40_change>0 || GAPDOWN | confluence | +0.6830 | +1.96 | +1.79 |
| 7 | w_ret_13w_change<0&d_wq_16_change>0 || DIP3 | confluence | +0.6500 | +1.80 | +2.03 |
| 8 | w_ret_13w_change<0&d_mdi14_change>0 || DIP3 | confluence | +0.6036 | +1.88 | +1.67 |
| 9 | X2|w_ret_13w_change<0&d_mdi14_change>0 | pair+dip | +0.5929 | +1.68 | +1.51 |
| 10 | S2|w_ret_13w_change<0&d_mdi14_diff5_change>0 | pair | +0.5889 | +1.49 | +1.25 |
| 11 | S2|w_ret_13w_change<0&x_z_d_downside_dev_60_change>0 | pair | +0.5713 | +1.20 | +1.23 |
| 12 | B+C&DIP_3 | label+dip | +0.5398 | +1.82 | +1.93 |
| 13 | w_ret_13w_change<0&d_dist_from_52wl_change<0 || DIPATR1 | confluence | +0.5068 | +1.84 | +2.16 |
| 14 | w_ret_13w_change<0&d_wq_16_change>0 || GAPDOWN | confluence | +0.5033 | +1.66 | +1.70 |
| 15 | w_ret_13w_change<0&d_wq_40_change>0 || DIP2 | confluence | +0.5011 | +1.64 | +1.92 |
| 16 | C || GAPDOWN | confluence | +0.4953 | +1.07 | +1.02 |
| 17 | w_ret_13w_change<0&d_mdi14_change>0 || DIP1 | confluence | +0.4946 | +1.58 | +1.30 |
| 18 | S2|d_wq_40_change>0&x_z_d_downside_dev_60_change>0 | pair | +0.4643 | +0.93 | +0.90 |
| 19 | S2|w_ret_13w_change<0&d_wq_40_change>0 | pair | +0.4555 | +1.28 | +1.13 |
| 20 | A+C&DIP_2 | label+dip | +0.4353 | +1.98 | +1.80 |

## Where the setups discussed so far stand

| setup | both exits: eligible / score / place | why not (first reasons) |
|---|---|---|
| A | yes / -0.0464 / 617 | - |
| B | yes / +0.2370 / 51 | - |
| C | yes / +0.1107 / 197 | - |
| A+B | yes / +0.1641 / 97 | - |
| A+C (= A+B+C) | yes / +0.3727 / 24 | - |
| B+C | yes / +0.3459 / 29 | - |
| A & 2% dip | yes / -0.2220 / 683 | - |
| B & 2% dip | yes / +0.3542 / 28 | - |
| C & 2% dip | no / -0.0721 / - | D: net <= 0 in more than one year |
| A+B & 2% dip | yes / +0.2045 / 61 | - |
| A+C & 2% dip | yes / +0.4353 / 14 | - |
| B+C & 2% dip | no / +0.3734 / - | D: net <= 0 in more than one year |
| 2% dip alone | yes / -0.0150 / 550 | - |
| WQ_44 up & 13w down + gap down + vol elevated | not tested in every engine | - |
| B + 1-ATR dip + bearish | no / +0.0483 / - | D: the context filter does not clearly keep better trades; ENS: the context filter does not clearly keep better trades |
| B + 3% dip + bearish | no / +0.5275 / - | D: the context filter does not clearly keep better trades; ENS: the context filter does not clearly keep better trades |

Families (eligible both exits / tested): confluence 48/2332, confluence-alone 1/85, control 0/3, feature+dip 37/180, label 6/6, label+confirmation 1/18, label+dip 14/24, pair 567/5506, pair+dip 5/9, price-only 5/13, single 4/106

Read with care: this ranks thousands of rules on the history they were found on; the winners' numbers will shrink going forward. The forward paper ledger is the test.
