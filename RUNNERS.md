# Runners - the picks that do not dip (08 Nov 2026, setuplab v0.9)

Watchlist C:\QuantData\setuplab\WL_R1_10; panel C:\QuantData\cache_daily\panel_oc\panel.parquet; features features_final.txt. D: 15818 of 15818 settled picks complete (their bars give the watchlist's D1-D5 closes); ENS: 16256 of 16256 settled picks complete (their bars give the watchlist's D1-D5 closes).

**The rule (declared before any result):** runners v1, declared 8 Nov 2026 before any result on real picks. Karan: find which model picks will NOT dip and buy them at the model's open or on an event; 5-7 quality trades a week together with the dip setups; don't be conservative. PICKS: engines D and ENS, ranks 1-10, bought at the D1 open (the model's own price), sold at the D5 close, 0.35 pp costs; a pick whose own daily bars do not give the watchlist's D1-D5 closes is left out (counted). DIP = a close on D1-D4 at least 2% below the D1 open (Karan's choice: the closes a dip setup acts on); also measured: the intraday low 2% below on D1-D5, and a close 1 ATR below. RIGHT TAIL = the D5 close 5% or more above the D1 open (10% also shown). RUNNER = no dip and the right tail. A RULE = one to three conditions known at the signal close (a feature rose / fell on the signal day; a zone range at the signal close; the model's rank; the other engine picking it too; the weekday of D1; the market context and the stock's state at the pick) or at the D1 open (the gap, seen in the pre-open); it buys every pick it selects at the D1 open. SEARCH, in both engines: every single condition, every pair from different families, and the 150 best pairs with one more rank / agreement / weekday / context / gap condition; the 60 best by a quick 95% lower bound (day-clustered) get the full block bootstrap. A rule QUALIFIES when, in both engines: 25 or more trades a year; net per trade 95% interval above 0; its lift over every pick of the same days (net minus that day's mean over all the engine's picks) 95% interval above 0; net <= 0 in at most 2 of its years; EVERY CONDITION EARNS ITS PLACE: the rule's net per trade minus the net of the trades its simpler version (that condition dropped) adds, 95% interval above 0 (the quick screen applies the same test before the bootstrap, so a narrower rule never displaces the simpler one, with more trades, by luck). Score = the lower 95% bound of net per trade in the weaker engine. CANDIDATES for the forward paper test = the top 5 qualifiers that are not versions of each other (one's conditions within the other's, or 70% of the same D trades); the best 5 by score are listed too, qualified or not. Plain 95% per rule (don't be conservative): some rules pass by luck, so the whole search is replayed year by year 2022-2026 - choose the candidates with the picks whose D5 exit was before 1 January, judge their picks (each pick once) on that year: HOLDS when the pooled lift over all picks is above 0 out of sample (95%), WORSE when below, else NOT SHOWN. EVENTS on the candidates' picks and on all picks, each against the D1 open on the same picks: the breakout (a buy-stop 0.05% above the signal-day high, live on D1 and D2), the D2 open after a strong D1 (green, the close in the top 30% of its range), the D1 close after a strong D1. MONEY: Rs 5 L in 2 / 3 / 5 / 7 equal slots, profits reinvested, no MTF and MTF 2x (0.04% a day on the borrowed half), entries from 2022, one position per pick (its earliest entry); the dip arm = the frozen setups' trades in the newest ZONES run, IN or OUT of their picks zone; the same open: the source with the higher net per trade first, then the model's rank.

Rs a year = net % per trade x trades a year x Rs 1,000 (Rs 1 L a trade, before taxes).

## Verdict: the no-dip candidates (bought at the D1 open, sold at the D5 close)

| | rule | D trades a year | D net % per trade [95%] | D lift over all picks [95%] | D no dip | D runners | D Rs a year | ENS trades a year | ENS net % per trade [95%] | ENS lift over all picks [95%] | ENS no dip | ENS runners | ENS Rs a year |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | d_adx14 rose on the signal day & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & NIFTY above its 50-day average | 42 | +5.02 [+2.78, +7.20] | +0.47 [+0.17, +0.77] | 56.7% | 31.4% | 208,693 | 37 | +5.01 [+2.85, +7.11] | +0.67 [+0.13, +1.35] | 58.3% | 30.4% | 185,747 |
| R2 | d_dist_from_52wl fell on the signal day & d_intraday_ret_pct rose on the signal day & both engines have it in their ranks 1-3 | 53 | +2.89 [+1.76, +3.95] | +1.74 [+0.93, +2.50] | 54.5% | 30.7% | 152,635 | 53 | +2.89 [+1.76, +3.95] | +1.64 [+0.86, +2.42] | 54.5% | 30.7% | 152,635 |
| R3 | d_upside_vol_ratio rose on the signal day & VIXP India VIX percentile in its last 250 sessions: 66.6667 and above at the signal close & both engines have it in their ranks 1-3 | 26 | +3.73 [+1.56, +6.02] | +1.66 [+0.31, +2.97] | 51.7% | 34.3% | 96,272 | 26 | +3.73 [+1.56, +6.02] | +1.46 [+0.09, +2.80] | 51.7% | 34.3% | 96,272 |
| R4 | d_cmf20_rmean50 fell on the signal day & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & the other engine picked it too (its ranks 1-10) | 35 | +3.84 [+1.44, +6.14] | +0.71 [+0.09, +1.47] | 56.4% | 27.1% | 136,168 | 35 | +3.84 [+1.44, +6.14] | +0.81 [+0.11, +1.63] | 56.4% | 27.1% | 136,168 |
| R5 | ATRP ATR14 % of the close: 2 and above at the signal close & VIX5 India VIX 5-session change %: below -10 at the signal close & India VIX in the upper half of its last year | 153 | +3.16 [+0.92, +5.44] | +0.02 [+0.00, +0.05] | 57.5% | 28.8% | 482,378 | 158 | +3.01 [+0.98, +5.05] | +0.02 [+0.00, +0.06] | 57.4% | 28.1% | 473,989 |

**Out of sample (the whole search replayed year by year, the candidates' picks each once):** D **NOT SHOWN** - lift over all picks -0.15 [-0.57, +0.33], net +0.52 [-0.59, +1.72] per trade on 952 picks in 5 years; ENS **NOT SHOWN** - lift over all picks +0.03 [-0.40, +0.48], net +0.70 [-0.44, +1.97] per trade on 927 picks in 5 years

The best 5 by score, qualified or not (the open list):

| | rule | D trades a year | D net % per trade [95%] | D lift over all picks [95%] | D no dip | D runners | D Rs a year | ENS trades a year | ENS net % per trade [95%] | ENS lift over all picks [95%] | ENS no dip | ENS runners | ENS Rs a year |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B1 | d_adx14 rose on the signal day & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & NIFTY above its 50-day average | 42 | +5.02 [+2.78, +7.20] | +0.47 [+0.17, +0.77] | 56.7% | 31.4% | 208,693 | 37 | +5.01 [+2.85, +7.11] | +0.67 [+0.13, +1.35] | 58.3% | 30.4% | 185,747 |
| B2 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & the other engine picked it too (its ranks 1-10) & a bearish stock state at the pick (S08/S09) (does NOT qualify) | 29 | +4.98 [+2.23, +7.24] | +0.75 [-0.02, +1.86] | 58.7% | 32.1% | 146,481 | 29 | +4.98 [+2.23, +7.24] | +0.86 [+0.15, +1.84] | 58.7% | 32.1% | 146,481 |
| B3 | d_dist_from_52wl fell on the signal day & d_intraday_ret_pct rose on the signal day & both engines have it in their ranks 1-3 | 53 | +2.89 [+1.76, +3.95] | +1.74 [+0.93, +2.50] | 54.5% | 30.7% | 152,635 | 53 | +2.89 [+1.76, +3.95] | +1.64 [+0.86, +2.42] | 54.5% | 30.7% | 152,635 |
| B4 | TREND close vs EMA50 and EMA200: between at the signal close & RSI14 RSI 14: below 30 at the signal close (does NOT qualify) | 63 | +3.09 [+1.96, +4.20] | +1.17 [+0.48, +1.94] | 57.2% | 28.9% | 193,747 | 71 | +2.78 [+1.68, +3.93] | +0.86 [+0.14, +1.60] | 58.4% | 29.1% | 197,833 |
| B5 | d_donch_pos_50_rmean50 rose on the signal day & RSI14 RSI 14: 30 to 50 at the signal close & D1 opens 1% or more above the signal close (pre-open) (does NOT qualify) | 34 | +4.04 [+1.74, +6.20] | +0.68 [-0.43, +1.77] | 58.4% | 36.3% | 137,119 | 31 | +3.79 [+1.59, +5.78] | +0.87 [-0.33, +2.22] | 54.1% | 32.4% | 117,624 |

**Trades a week and money at a glance** (Rs 5 L, no MTF, from 2022; in-sample):

| engine | book | slots | trades a week | Rs 5 L became | a year | worst fall |
|---|---|---:|---:|---:|---:|---:|
| D | plan: ranks 1-3 at the D1 open | 3 | 2.8 | Rs 4,820,133 | +61.7% | 54.7% |
| D | plan: ranks 1-3 at the D1 open | 5 | 4.7 | Rs 3,500,126 | +51.1% | 44.2% |
| D | no-dip arm: the candidates at the D1 open | 3 | 1.4 | Rs 6,625,765 | +72.9% | 18.4% |
| D | no-dip arm: the candidates at the D1 open | 5 | 2.0 | Rs 4,819,939 | +61.7% | 13.2% |
| D | dip arm: S3 in its zone | 3 | 0.5 | Rs 1,428,525 | +24.9% | 19.3% |
| D | dip arm: S3 in its zone | 5 | 0.6 | Rs 1,073,428 | +17.6% | 8.0% |
| D | dip arm: all 7 setups (in-zone first) | 3 | 2.7 | Rs 890,204 | +13.0% | 42.2% |
| D | dip arm: all 7 setups (in-zone first) | 5 | 4.3 | Rs 1,180,030 | +20.0% | 39.8% |
| D | BOTH ARMS: no-dip + S3 in its zone | 3 | 1.6 | Rs 6,244,164 | +70.8% | 19.1% |
| D | BOTH ARMS: no-dip + S3 in its zone | 5 | 2.3 | Rs 5,781,468 | +68.0% | 19.6% |
| D | BOTH ARMS: no-dip + all 7 setups | 3 | 2.8 | Rs 4,123,496 | +56.4% | 32.1% |
| D | BOTH ARMS: no-dip + all 7 setups | 5 | 4.5 | Rs 3,952,197 | +55.0% | 25.9% |
| ENS | plan: ranks 1-3 at the D1 open | 3 | 2.8 | Rs 6,642,913 | +72.9% | 52.4% |
| ENS | plan: ranks 1-3 at the D1 open | 5 | 4.7 | Rs 5,843,180 | +68.2% | 45.0% |
| ENS | no-dip arm: the candidates at the D1 open | 3 | 1.4 | Rs 4,950,815 | +62.4% | 19.3% |
| ENS | no-dip arm: the candidates at the D1 open | 5 | 2.0 | Rs 4,307,611 | +57.7% | 15.2% |
| ENS | dip arm: S3 in its zone | 3 | 0.5 | Rs 1,432,239 | +24.9% | 12.7% |
| ENS | dip arm: S3 in its zone | 5 | 0.6 | Rs 1,109,130 | +18.4% | 7.8% |
| ENS | dip arm: all 7 setups (in-zone first) | 3 | 2.7 | Rs 1,700,007 | +29.6% | 31.5% |
| ENS | dip arm: all 7 setups (in-zone first) | 5 | 4.4 | Rs 1,852,369 | +31.9% | 26.6% |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 3 | 1.6 | Rs 8,616,255 | +82.7% | 17.7% |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 5 | 2.3 | Rs 6,051,351 | +69.5% | 17.2% |
| ENS | BOTH ARMS: no-dip + all 7 setups | 3 | 2.8 | Rs 3,131,870 | +47.4% | 35.2% |
| ENS | BOTH ARMS: no-dip + all 7 setups | 5 | 4.5 | Rs 4,538,733 | +59.5% | 31.8% |

## The year-by-year replay

| year | candidates chosen with exits before 1 January | D picks that year | D in the candidates | D net in them | D net all picks | D no dip in them | D no dip all | ENS picks that year | ENS in the candidates | ENS net in them | ENS net all picks | ENS no dip in them | ENS no dip all |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022 | F|d_donch_pos_50_rmean50>0 & Z|RSI14:0:1 & P|agree | 2460 | 71 | -0.23 | +0.61 | 52.1% | 51.6% | 2472 | 71 | -0.23 | +0.58 | 52.1% | 52.4% |
| 2023 | F|d_donch_pos_50_rmean50>0 & Z|RSI14:0:1 & P|top3; F|d_vol_yz_50>0 & Z|VIX5:0:0 & P|agree | 2424 | 81 | +1.15 | +0.65 | 65.4% | 67.1% | 2427 | 79 | +1.35 | +1.00 | 72.2% | 65.6% |
| 2024 | F|x_z_d_dvol_z252>0 & Z|TREND:1:1 & G|dn1; Z|VIX5:0:1 & P|agree & G|dn1; F|d_wq_26>0 & Z|RSI14:0:0 & P|agree | 2421 | 165 | +2.42 | +1.45 | 52.1% | 50.1% | 2487 | 180 | +2.51 | +1.12 | 51.7% | 49.7% |
| 2025 | Z|RSI14:0:0 & Z|IDX:1:1; F|d_adx14>0 & Z|IDX:1:1 & C|VOL_ELEV; Z|RSI14:0:0 & Z|VIX5:0:1 & P|agree; Z|VIX5:0:1 & P|agree3 & C|VIX_HIGH | 2202 | 548 | +0.36 | +0.21 | 48.2% | 49.6% | 2393 | 534 | +0.40 | +0.31 | 48.3% | 52.0% |
| 2026 | Z|RSI14:0:0 & Z|IDX:1:1; F|d_adx14>0 & Z|IDX:1:1 & C|VOL_ELEV; F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | 1446 | 87 | -2.04 | +0.40 | 35.6% | 48.8% | 1608 | 63 | -1.70 | +0.50 | 36.5% | 51.5% |

## Base rates (every complete pick bought at the D1 open, sold at the D5 close)

| engine | picks | no dip (a close 2% below) | dip by the intraday low 2% | dip by 1 ATR | D5 close +5% | +10% | runners | net all | net runners | net no dip | net dip | runners' share of the profit | ranks 1-3 no dip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| D | 15818 | 53.6% | 69.3% | 23.9% | 24.2% | 11.5% | 19.8% | +0.85 | +11.64 | +4.58 | -3.45 | 271% | 52.7% |
| ENS | 16256 | 54.9% | 68.6% | 23.1% | 24.1% | 11.1% | 20.1% | +0.90 | +11.31 | +4.41 | -3.37 | 251% | 53.3% |

## What marks a runner at the signal close (and the D1 open)

AUC = the chance a pick with the outcome scores higher on the measure than one without (0.5 = no information). SHOWN = both engines' 95% intervals off 0.5 the same way and q <= 0.10 in both. Above / below = the share of runners among picks above / below the measure's median. The 30 strongest:

| measure | SHOWN | D AUC [95%] | D above / below the median | ENS AUC [95%] | ENS above / below the median |
|---|---|---:|---:|---:|---:|
| zone ATRP | yes, higher -> more runners | 0.602 [0.579, 0.626] | 24.4% / 15.3% | 0.600 [0.579, 0.622] | 24.2% / 15.9% |
| d_atr_pct (level) | yes, higher -> more runners | 0.602 [0.579, 0.626] | 24.4% / 15.3% | 0.600 [0.579, 0.622] | 24.2% / 15.9% |
| d_vol_yz_50 (level) | yes, higher -> more runners | 0.599 [0.575, 0.623] | 24.3% / 15.4% | 0.601 [0.580, 0.622] | 24.2% / 15.9% |
| s_atr14 | yes, higher -> more runners | 0.598 [0.575, 0.620] | 24.1% / 15.6% | 0.596 [0.575, 0.617] | 24.1% / 16.1% |
| d_vol_yz_20 (level) | yes, higher -> more runners | 0.593 [0.571, 0.615] | 24.1% / 15.6% | 0.590 [0.570, 0.609] | 24.1% / 16.1% |
| d_range_pct (level) | yes, higher -> more runners | 0.591 [0.572, 0.611] | 24.1% / 15.6% | 0.589 [0.571, 0.607] | 24.0% / 16.2% |
| d_realvol_60 (level) | yes, higher -> more runners | 0.587 [0.564, 0.610] | 23.6% / 16.0% | 0.592 [0.571, 0.613] | 23.9% / 16.3% |
| d_ret_5d_roll_std (level) | yes, higher -> more runners | 0.586 [0.564, 0.608] | 23.7% / 16.0% | 0.590 [0.570, 0.610] | 23.8% / 16.4% |
| d_realvol_20 (level) | yes, higher -> more runners | 0.578 [0.556, 0.601] | 23.0% / 16.7% | 0.580 [0.560, 0.599] | 23.8% / 16.4% |
| d_bb_bw_20 (level) | yes, higher -> more runners | 0.577 [0.555, 0.599] | 23.3% / 16.4% | 0.585 [0.564, 0.606] | 23.8% / 16.4% |
| d_n_5pct_up_252 (level) | yes, higher -> more runners | 0.574 [0.552, 0.596] | 23.1% / 16.3% | 0.576 [0.556, 0.595] | 23.5% / 16.5% |
| snapshot pre_vix | yes, higher -> more runners | 0.573 [0.542, 0.605] | 22.7% / 16.9% | 0.564 [0.536, 0.592] | 22.7% / 17.5% |
| snapshot pre_state_atr_rank | yes, higher -> more runners | 0.566 [0.543, 0.588] | 23.2% / 16.5% | 0.561 [0.540, 0.583] | 23.2% / 16.9% |
| d_amihud_20 (level) | yes, higher -> more runners | 0.566 [0.546, 0.586] | 22.8% / 16.9% | 0.559 [0.541, 0.577] | 23.0% / 17.2% |
| d_n_5pct_up_60 (level) | yes, higher -> more runners | 0.561 [0.542, 0.580] | 22.6% / 16.4% | 0.558 [0.541, 0.576] | 23.0% / 16.8% |
| x_z_d_downside_dev_60 (level) | yes, higher -> more runners | 0.557 [0.537, 0.578] | 21.9% / 17.8% | 0.566 [0.548, 0.584] | 23.0% / 17.2% |
| d_amihud_60 (level) | yes, higher -> more runners | 0.565 [0.546, 0.585] | 22.8% / 16.9% | 0.557 [0.541, 0.573] | 22.7% / 17.4% |
| zone DD52 | yes, lower -> more runners | 0.450 [0.424, 0.475] | 17.2% / 22.5% | 0.444 [0.420, 0.468] | 17.1% / 23.1% |
| zone VIXP | yes, higher -> more runners | 0.561 [0.533, 0.589] | 22.9% / 16.8% | 0.547 [0.521, 0.573] | 22.2% / 17.9% |
| snapshot pre_vix_pct250 | yes, higher -> more runners | 0.561 [0.533, 0.588] | 22.9% / 16.8% | 0.547 [0.521, 0.573] | 22.2% / 17.9% |
| snapshot pre_nifty_minus_small_20 | yes, higher -> more runners | 0.549 [0.520, 0.577] | 21.9% / 17.7% | 0.547 [0.519, 0.574] | 21.7% / 18.4% |
| snapshot pre_nifty_minus_mid_20 | yes, higher -> more runners | 0.552 [0.525, 0.578] | 22.3% / 17.4% | 0.546 [0.520, 0.572] | 22.1% / 18.1% |
| d_slope_stability_rmean50 (level) | yes, lower -> more runners | 0.456 [0.436, 0.475] | 17.8% / 21.9% | 0.453 [0.436, 0.470] | 17.9% / 22.3% |
| snapshot pre_beta_small | yes, higher -> more runners | 0.544 [0.524, 0.564] | 21.4% / 18.3% | 0.553 [0.536, 0.570] | 22.2% / 18.0% |
| d_mdi14 (level) | yes, higher -> more runners | 0.543 [0.520, 0.567] | 22.3% / 17.4% | 0.551 [0.528, 0.574] | 23.1% / 17.0% |
| d_slope_stability (level) | yes, lower -> more runners | 0.459 [0.439, 0.478] | 17.6% / 22.1% | 0.458 [0.441, 0.475] | 18.0% / 22.1% |
| snapshot pre_beta_mid | yes, higher -> more runners | 0.541 [0.521, 0.561] | 21.5% / 18.2% | 0.548 [0.531, 0.565] | 21.8% / 18.4% |
| snapshot pre_state_vol_elevated | yes, higher -> more runners | 0.541 [0.523, 0.558] | 19.8% /  | 0.541 [0.524, 0.559] | 20.1% /  |
| snapshot pre_small_vs_ma50 | yes, lower -> more runners | 0.450 [0.419, 0.481] | 17.2% / 22.5% | 0.460 [0.431, 0.489] | 18.2% / 22.0% |
| d_dist_from_20h (level) | yes, lower -> more runners | 0.460 [0.437, 0.483] | 17.8% / 21.9% | 0.454 [0.430, 0.478] | 17.5% / 22.7% |

## What marks a pick that will dip (below 0.5 = less dipping)

AUC = the chance a pick with the outcome scores higher on the measure than one without (0.5 = no information). SHOWN = both engines' 95% intervals off 0.5 the same way and q <= 0.10 in both. Above / below = the share of dips among picks above / below the measure's median. The 30 strongest:

| measure | SHOWN | D AUC [95%] | D above / below the median | ENS AUC [95%] | ENS above / below the median |
|---|---|---:|---:|---:|---:|
| d_vol_yz_20 (level) | yes, higher -> more dips | 0.602 [0.579, 0.625] | 52.9% / 39.9% | 0.593 [0.574, 0.612] | 51.3% / 38.8% |
| d_atr_pct (level) | yes, higher -> more dips | 0.599 [0.575, 0.624] | 52.9% / 39.9% | 0.592 [0.571, 0.612] | 51.5% / 38.6% |
| zone ATRP | yes, higher -> more dips | 0.599 [0.575, 0.624] | 52.9% / 39.9% | 0.592 [0.571, 0.612] | 51.5% / 38.6% |
| s_atr14 | yes, higher -> more dips | 0.599 [0.576, 0.623] | 52.8% / 40.0% | 0.591 [0.571, 0.610] | 51.4% / 38.8% |
| x_z_d_downside_dev_60 (level) | yes, higher -> more dips | 0.599 [0.578, 0.620] | 53.3% / 39.5% | 0.588 [0.569, 0.607] | 51.6% / 38.5% |
| d_bb_bw_20 (level) | yes, higher -> more dips | 0.599 [0.578, 0.620] | 53.4% / 39.4% | 0.586 [0.567, 0.604] | 51.2% / 39.0% |
| d_realvol_20 (level) | yes, higher -> more dips | 0.597 [0.576, 0.619] | 53.1% / 39.7% | 0.585 [0.566, 0.604] | 50.8% / 39.3% |
| d_vol_yz_50 (level) | yes, higher -> more dips | 0.589 [0.564, 0.613] | 52.1% / 40.7% | 0.577 [0.557, 0.597] | 50.5% / 39.6% |
| d_ret_5d_roll_std (level) | yes, higher -> more dips | 0.589 [0.566, 0.611] | 52.6% / 40.2% | 0.576 [0.558, 0.595] | 50.5% / 39.7% |
| d_realvol_60 (level) | yes, higher -> more dips | 0.589 [0.566, 0.613] | 52.2% / 40.6% | 0.575 [0.556, 0.595] | 50.1% / 40.0% |
| d_range_pct (level) | yes, higher -> more dips | 0.584 [0.565, 0.604] | 52.4% / 40.4% | 0.572 [0.555, 0.588] | 50.4% / 39.8% |
| x_relvol_20 (level) | yes, higher -> more dips | 0.583 [0.560, 0.605] | 52.9% / 39.9% | 0.568 [0.548, 0.588] | 49.8% / 40.3% |
| snapshot pre_beta_small | yes, higher -> more dips | 0.567 [0.545, 0.588] | 51.0% / 41.8% | 0.567 [0.548, 0.586] | 50.0% / 40.1% |
| d_n_5pct_up_252 (level) | yes, higher -> more dips | 0.576 [0.556, 0.597] | 51.2% / 41.2% | 0.562 [0.546, 0.579] | 49.1% / 40.8% |
| snapshot pre_beta_home | yes, higher -> more dips | 0.559 [0.539, 0.578] | 50.8% / 42.0% | 0.562 [0.543, 0.582] | 49.9% / 40.2% |
| snapshot pre_state_atr_rank | yes, higher -> more dips | 0.559 [0.537, 0.580] | 50.5% / 42.3% | 0.556 [0.536, 0.577] | 49.2% / 40.9% |
| snapshot pre_state_cons_range_atr | yes, higher -> more dips | 0.562 [0.544, 0.581] | 51.1% / 41.7% | 0.554 [0.536, 0.573] | 49.2% / 40.9% |
| snapshot pre_beta_mid | yes, higher -> more dips | 0.554 [0.533, 0.575] | 50.4% / 42.4% | 0.558 [0.539, 0.577] | 49.6% / 40.5% |
| zone ATRX | yes, higher -> more dips | 0.553 [0.534, 0.572] | 50.3% / 42.4% | 0.554 [0.534, 0.574] | 48.7% / 41.4% |
| d_amihud_20 (level) | yes, higher -> more dips | 0.566 [0.546, 0.587] | 50.8% / 42.0% | 0.552 [0.536, 0.568] | 48.4% / 41.8% |
| snapshot pre_small_vs_ma50 | yes, lower -> more dips | 0.449 [0.423, 0.474] | 42.8% / 50.0% | 0.445 [0.421, 0.468] | 41.5% / 48.6% |
| snapshot pre_mid_vs_ma50 | yes, lower -> more dips | 0.450 [0.424, 0.475] | 42.7% / 50.1% | 0.443 [0.419, 0.466] | 40.9% / 49.3% |
| snapshot pre_nifty_vs_ma50 | yes, lower -> more dips | 0.451 [0.425, 0.477] | 43.1% / 49.7% | 0.442 [0.417, 0.468] | 41.2% / 49.0% |
| snapshot pre_env_code | yes, higher -> more dips | 0.549 [0.525, 0.572] | 48.6% / 41.8% | 0.549 [0.525, 0.573] | 47.0% / 41.0% |
| d_n_5pct_up_60 (level) | yes, higher -> more dips | 0.560 [0.540, 0.580] | 50.7% / 41.1% | 0.547 [0.531, 0.564] | 48.5% / 41.3% |
| d_amihud_60 (level) | yes, higher -> more dips | 0.565 [0.545, 0.585] | 50.6% / 42.2% | 0.547 [0.532, 0.562] | 48.3% / 41.8% |
| zone IDX | yes, lower -> more dips | 0.455 [0.431, 0.478] | 43.0% / 50.7% | 0.452 [0.430, 0.475] | 41.5% / 49.7% |
| d_dist_from_20h (level) | yes, lower -> more dips | 0.451 [0.431, 0.471] | 42.0% / 50.8% | 0.458 [0.438, 0.478] | 41.5% / 48.6% |
| zone DD52 | yes, lower -> more dips | 0.450 [0.425, 0.475] | 42.3% / 50.5% | 0.458 [0.436, 0.480] | 41.6% / 48.5% |
| d_mdi14 (level) | yes, higher -> more dips | 0.544 [0.523, 0.565] | 50.1% / 42.7% | 0.542 [0.521, 0.563] | 48.1% / 42.1% |

## Entries: the D1 open against the events, on the same picks

Per trade = the filled trades only; per pick = an unfilled pick counts 0 (cash); against the D1 open = the event's trade minus the D1-open trade on exactly the picks the event filled. All sold at the D5 close.

| picks of | engine | entry | filled | per trade [95%] | per pick [95%] | against the D1 open [95%] | no dip | runners | trades a year |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| ALL picks | D | D1 open (the model's own buy; AMO / pre-open) | 15818 of 15818 (100%) | +0.85 [+0.39, +1.31] | +0.85 [+0.39, +1.31] | +0.00 [+0.00, +0.00] | 53.6% | 19.8% | 2374 |
| ALL picks | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 8846 of 15818 (56%) | +0.93 [+0.50, +1.39] | +0.52 [+0.27, +0.79] | -1.98 [-2.12, -1.85] | 71.0% | 29.1% | 1327 |
| ALL picks | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 3756 of 15818 (24%) | +0.20 [-0.28, +0.69] | +0.05 [-0.07, +0.17] | -4.81 [-5.09, -4.55] | 86.8% | 42.6% | 564 |
| ALL picks | D | D1 close after a strong D1 (at the screen about 15:20) | 3756 of 15818 (24%) | +1.08 [+0.54, +1.62] | +0.26 [+0.13, +0.39] | -3.94 [-4.16, -3.73] | 86.8% | 42.6% | 564 |
| the no-dip arm (R1-R5) | D | D1 open (the model's own buy; AMO / pre-open) | 1812 of 1812 (100%) | +3.19 [+1.82, +4.67] | +3.19 [+1.82, +4.67] | +0.00 [+0.00, +0.00] | 56.3% | 29.1% | 272 |
| the no-dip arm (R1-R5) | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 1154 of 1812 (64%) | +2.73 [+1.27, +4.29] | +1.74 [+0.80, +2.78] | -2.39 [-2.70, -2.13] | 70.5% | 38.7% | 173 |
| the no-dip arm (R1-R5) | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 496 of 1812 (27%) | +1.56 [+0.04, +3.19] | +0.43 [+0.01, +0.93] | -6.31 [-6.87, -5.75] | 89.3% | 56.0% | 74 |
| the no-dip arm (R1-R5) | D | D1 close after a strong D1 (at the screen about 15:20) | 496 of 1812 (27%) | +2.85 [+1.22, +4.65] | +0.78 [+0.32, +1.34] | -5.02 [-5.43, -4.60] | 89.3% | 56.0% | 74 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | D | D1 open (the model's own buy; AMO / pre-open) | 277 of 277 (100%) | +5.02 [+2.78, +7.20] | +5.02 [+2.78, +7.20] | +0.00 [+0.00, +0.00] | 56.7% | 31.4% | 42 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 161 of 277 (58%) | +4.28 [+1.90, +6.58] | +2.48 [+1.06, +3.91] | -3.02 [-3.76, -2.38] | 70.2% | 44.1% | 24 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 84 of 277 (30%) | +2.32 [+0.28, +3.70] | +0.70 [+0.09, +1.10] | -6.22 [-7.25, -4.97] | 95.2% | 61.9% | 13 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | D | D1 close after a strong D1 (at the screen about 15:20) | 84 of 277 (30%) | +3.13 [+0.87, +4.72] | +0.95 [+0.27, +1.42] | -5.41 [-6.27, -4.35] | 95.2% | 61.9% | 13 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | D | D1 open (the model's own buy; AMO / pre-open) | 352 of 352 (100%) | +2.89 [+1.76, +3.95] | +2.89 [+1.76, +3.95] | +0.00 [+0.00, +0.00] | 54.5% | 30.7% | 53 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 191 of 352 (54%) | +2.12 [+0.92, +3.35] | +1.15 [+0.49, +1.85] | -3.91 [-4.37, -3.48] | 75.4% | 46.1% | 29 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 116 of 352 (33%) | +0.64 [-0.84, +2.13] | +0.21 [-0.29, +0.68] | -6.74 [-7.63, -5.88] | 87.1% | 52.6% | 17 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | D | D1 close after a strong D1 (at the screen about 15:20) | 116 of 352 (33%) | +1.92 [+0.38, +3.43] | +0.63 [+0.13, +1.12] | -5.47 [-6.12, -4.80] | 87.1% | 52.6% | 17 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | D | D1 open (the model's own buy; AMO / pre-open) | 172 of 172 (100%) | +3.73 [+1.56, +6.02] | +3.73 [+1.56, +6.02] | +0.00 [+0.00, +0.00] | 51.7% | 34.3% | 26 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 110 of 172 (64%) | +3.45 [+1.13, +6.04] | +2.21 [+0.71, +3.93] | -2.06 [-2.47, -1.66] | 63.6% | 40.9% | 17 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 48 of 172 (28%) | +3.86 [+1.15, +6.90] | +1.08 [+0.30, +2.09] | -5.94 [-7.08, -5.00] | 91.7% | 68.8% | 7 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | D | D1 close after a strong D1 (at the screen about 15:20) | 48 of 172 (28%) | +5.51 [+2.85, +8.42] | +1.54 [+0.69, +2.58] | -4.30 [-5.40, -3.45] | 91.7% | 68.8% | 7 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | D | D1 open (the model's own buy; AMO / pre-open) | 236 of 236 (100%) | +3.84 [+1.44, +6.14] | +3.84 [+1.44, +6.14] | +0.00 [+0.00, +0.00] | 56.4% | 27.1% | 35 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 129 of 236 (55%) | +2.62 [+0.09, +5.28] | +1.43 [+0.05, +2.89] | -3.50 [-4.27, -2.74] | 73.6% | 39.5% | 19 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 236 (29%) | +0.34 [-1.54, +1.89] | +0.10 [-0.44, +0.54] | -6.28 [-7.67, -5.01] | 92.6% | 48.5% | 10 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | D | D1 close after a strong D1 (at the screen about 15:20) | 68 of 236 (29%) | +1.08 [-0.83, +2.66] | +0.31 [-0.22, +0.77] | -5.54 [-6.76, -4.46] | 92.6% | 48.5% | 10 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | D | D1 open (the model's own buy; AMO / pre-open) | 1017 of 1017 (100%) | +3.16 [+0.92, +5.44] | +3.16 [+0.92, +5.44] | +0.00 [+0.00, +0.00] | 57.5% | 28.8% | 153 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 704 of 1017 (69%) | +2.92 [+0.70, +5.24] | +2.02 [+0.46, +3.74] | -1.82 [-2.14, -1.53] | 69.5% | 36.9% | 106 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 256 of 1017 (25%) | +1.99 [-0.69, +4.65] | +0.50 [-0.16, +1.29] | -6.32 [-7.19, -5.29] | 88.3% | 58.2% | 38 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | D | D1 close after a strong D1 (at the screen about 15:20) | 256 of 1017 (25%) | +3.52 [+0.61, +6.36] | +0.89 [+0.14, +1.77] | -4.78 [-5.41, -4.06] | 88.3% | 58.2% | 38 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D1 open (the model's own buy; AMO / pre-open) | 196 of 196 (100%) | +4.98 [+2.23, +7.24] | +4.98 [+2.23, +7.24] | +0.00 [+0.00, +0.00] | 58.7% | 32.1% | 29 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 109 of 196 (56%) | +3.43 [+0.76, +5.92] | +1.91 [+0.41, +3.43] | -3.83 [-4.56, -3.07] | 78.0% | 45.9% | 16 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 196 (35%) | +1.28 [-0.62, +2.81] | +0.45 [-0.23, +0.89] | -6.35 [-7.44, -5.21] | 94.1% | 54.4% | 10 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D1 close after a strong D1 (at the screen about 15:20) | 68 of 196 (35%) | +2.32 [+0.30, +3.97] | +0.81 [+0.10, +1.30] | -5.31 [-6.32, -4.28] | 94.1% | 54.4% | 10 |
| Z|TREND:1:1 & Z|RSI14:0:0 | D | D1 open (the model's own buy; AMO / pre-open) | 418 of 418 (100%) | +3.09 [+1.96, +4.20] | +3.09 [+1.96, +4.20] | +0.00 [+0.00, +0.00] | 57.2% | 28.9% | 63 |
| Z|TREND:1:1 & Z|RSI14:0:0 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 207 of 418 (50%) | +1.67 [+0.49, +2.82] | +0.83 [+0.25, +1.44] | -3.74 [-4.16, -3.32] | 77.8% | 41.1% | 31 |
| Z|TREND:1:1 & Z|RSI14:0:0 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 136 of 418 (33%) | -0.08 [-1.30, +1.24] | -0.03 [-0.43, +0.41] | -6.03 [-6.76, -5.25] | 86.8% | 47.8% | 20 |
| Z|TREND:1:1 & Z|RSI14:0:0 | D | D1 close after a strong D1 (at the screen about 15:20) | 136 of 418 (33%) | +1.08 [-0.27, +2.50] | +0.35 [-0.09, +0.81] | -4.87 [-5.49, -4.18] | 86.8% | 47.8% | 20 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | D | D1 open (the model's own buy; AMO / pre-open) | 226 of 226 (100%) | +4.04 [+1.74, +6.20] | +4.04 [+1.74, +6.20] | +0.00 [+0.00, +0.00] | 58.4% | 36.3% | 34 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 175 of 226 (77%) | +5.23 [+2.67, +7.48] | +4.05 [+1.97, +6.00] | -0.67 [-0.96, -0.47] | 69.1% | 45.1% | 26 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 78 of 226 (35%) | +3.77 [+0.99, +6.13] | +1.30 [+0.29, +2.23] | -6.28 [-7.56, -5.11] | 88.5% | 66.7% | 12 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | D | D1 close after a strong D1 (at the screen about 15:20) | 78 of 226 (35%) | +5.89 [+2.57, +8.67] | +2.03 [+0.78, +3.15] | -4.17 [-5.17, -3.43] | 88.5% | 66.7% | 12 |
| ALL picks | ENS | D1 open (the model's own buy; AMO / pre-open) | 16256 of 16256 (100%) | +0.90 [+0.43, +1.34] | +0.90 [+0.43, +1.34] | +0.00 [+0.00, +0.00] | 54.9% | 20.1% | 2439 |
| ALL picks | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 9140 of 16256 (56%) | +0.84 [+0.41, +1.27] | +0.47 [+0.22, +0.73] | -1.94 [-2.07, -1.81] | 71.6% | 28.9% | 1372 |
| ALL picks | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 3919 of 16256 (24%) | +0.05 [-0.42, +0.50] | +0.01 [-0.10, +0.12] | -4.54 [-4.80, -4.31] | 84.8% | 39.9% | 588 |
| ALL picks | ENS | D1 close after a strong D1 (at the screen about 15:20) | 3919 of 16256 (24%) | +0.81 [+0.28, +1.32] | +0.19 [+0.07, +0.32] | -3.78 [-3.98, -3.59] | 84.8% | 39.9% | 588 |
| the no-dip arm (R1-R5) | ENS | D1 open (the model's own buy; AMO / pre-open) | 1818 of 1818 (100%) | +3.07 [+1.77, +4.44] | +3.07 [+1.77, +4.44] | +0.00 [+0.00, +0.00] | 56.3% | 28.5% | 273 |
| the no-dip arm (R1-R5) | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 1131 of 1818 (62%) | +2.58 [+1.13, +4.10] | +1.61 [+0.69, +2.61] | -2.34 [-2.66, -2.07] | 71.4% | 38.2% | 170 |
| the no-dip arm (R1-R5) | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 504 of 1818 (28%) | +1.10 [-0.30, +2.54] | +0.31 [-0.08, +0.72] | -6.07 [-6.68, -5.44] | 88.3% | 52.8% | 76 |
| the no-dip arm (R1-R5) | ENS | D1 close after a strong D1 (at the screen about 15:20) | 504 of 1818 (28%) | +2.28 [+0.80, +3.82] | +0.63 [+0.22, +1.09] | -4.90 [-5.36, -4.43] | 88.3% | 52.8% | 76 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | ENS | D1 open (the model's own buy; AMO / pre-open) | 247 of 247 (100%) | +5.01 [+2.85, +7.11] | +5.01 [+2.85, +7.11] | +0.00 [+0.00, +0.00] | 58.3% | 30.4% | 37 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 132 of 247 (53%) | +3.93 [+1.35, +6.43] | +2.10 [+0.69, +3.59] | -3.27 [-4.00, -2.65] | 75.0% | 44.7% | 20 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 74 of 247 (30%) | +1.44 [-0.86, +3.24] | +0.43 [-0.31, +0.92] | -6.21 [-7.75, -4.64] | 91.9% | 54.1% | 11 |
| F|d_adx14>0 & Z|IDX:1:1 & C|NIFTY_UP | ENS | D1 close after a strong D1 (at the screen about 15:20) | 74 of 247 (30%) | +2.39 [-0.18, +4.40] | +0.71 [-0.06, +1.21] | -5.27 [-6.57, -3.98] | 91.9% | 54.1% | 11 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | ENS | D1 open (the model's own buy; AMO / pre-open) | 352 of 352 (100%) | +2.89 [+1.76, +3.95] | +2.89 [+1.76, +3.95] | +0.00 [+0.00, +0.00] | 54.5% | 30.7% | 53 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 191 of 352 (54%) | +2.12 [+0.92, +3.35] | +1.15 [+0.49, +1.85] | -3.91 [-4.37, -3.48] | 75.4% | 46.1% | 29 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 116 of 352 (33%) | +0.64 [-0.84, +2.13] | +0.21 [-0.29, +0.68] | -6.74 [-7.63, -5.88] | 87.1% | 52.6% | 17 |
| F|d_dist_from_52wl<0 & F|d_intraday_ret_pct>0 & P|agree3 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 116 of 352 (33%) | +1.92 [+0.38, +3.43] | +0.63 [+0.13, +1.12] | -5.47 [-6.12, -4.80] | 87.1% | 52.6% | 17 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | ENS | D1 open (the model's own buy; AMO / pre-open) | 172 of 172 (100%) | +3.73 [+1.56, +6.02] | +3.73 [+1.56, +6.02] | +0.00 [+0.00, +0.00] | 51.7% | 34.3% | 26 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 110 of 172 (64%) | +3.45 [+1.13, +6.04] | +2.21 [+0.71, +3.93] | -2.06 [-2.47, -1.66] | 63.6% | 40.9% | 17 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 48 of 172 (28%) | +3.86 [+1.15, +6.90] | +1.08 [+0.30, +2.09] | -5.94 [-7.08, -5.00] | 91.7% | 68.8% | 7 |
| F|d_upside_vol_ratio>0 & Z|VIXP:2:2 & P|agree3 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 48 of 172 (28%) | +5.51 [+2.85, +8.42] | +1.54 [+0.69, +2.58] | -4.30 [-5.40, -3.45] | 91.7% | 68.8% | 7 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | ENS | D1 open (the model's own buy; AMO / pre-open) | 236 of 236 (100%) | +3.84 [+1.44, +6.14] | +3.84 [+1.44, +6.14] | +0.00 [+0.00, +0.00] | 56.4% | 27.1% | 35 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 129 of 236 (55%) | +2.62 [+0.09, +5.28] | +1.43 [+0.05, +2.89] | -3.50 [-4.27, -2.74] | 73.6% | 39.5% | 19 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 236 (29%) | +0.34 [-1.54, +1.89] | +0.10 [-0.44, +0.54] | -6.28 [-7.67, -5.01] | 92.6% | 48.5% | 10 |
| F|d_cmf20_rmean50<0 & Z|IDX:1:1 & P|agree | ENS | D1 close after a strong D1 (at the screen about 15:20) | 68 of 236 (29%) | +1.08 [-0.83, +2.66] | +0.31 [-0.22, +0.77] | -5.54 [-6.76, -4.46] | 92.6% | 48.5% | 10 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D1 open (the model's own buy; AMO / pre-open) | 1051 of 1051 (100%) | +3.01 [+0.98, +5.05] | +3.01 [+0.98, +5.05] | +0.00 [+0.00, +0.00] | 57.4% | 28.1% | 158 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 705 of 1051 (67%) | +2.84 [+0.67, +5.04] | +1.90 [+0.42, +3.46] | -1.74 [-2.06, -1.43] | 70.6% | 36.5% | 106 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 273 of 1051 (26%) | +1.41 [-1.01, +3.70] | +0.37 [-0.24, +1.01] | -5.85 [-6.76, -4.77] | 87.5% | 54.2% | 41 |
| Z|ATRP:1:3 & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D1 close after a strong D1 (at the screen about 15:20) | 273 of 1051 (26%) | +2.65 [+0.12, +5.18] | +0.69 [+0.03, +1.39] | -4.61 [-5.33, -3.78] | 87.5% | 54.2% | 41 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D1 open (the model's own buy; AMO / pre-open) | 196 of 196 (100%) | +4.98 [+2.23, +7.24] | +4.98 [+2.23, +7.24] | +0.00 [+0.00, +0.00] | 58.7% | 32.1% | 29 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 109 of 196 (56%) | +3.43 [+0.76, +5.92] | +1.91 [+0.41, +3.43] | -3.83 [-4.56, -3.07] | 78.0% | 45.9% | 16 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 196 (35%) | +1.28 [-0.62, +2.81] | +0.45 [-0.23, +0.89] | -6.35 [-7.44, -5.21] | 94.1% | 54.4% | 10 |
| Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D1 close after a strong D1 (at the screen about 15:20) | 68 of 196 (35%) | +2.32 [+0.30, +3.97] | +0.81 [+0.10, +1.30] | -5.31 [-6.32, -4.28] | 94.1% | 54.4% | 10 |
| Z|TREND:1:1 & Z|RSI14:0:0 | ENS | D1 open (the model's own buy; AMO / pre-open) | 474 of 474 (100%) | +2.78 [+1.68, +3.93] | +2.78 [+1.68, +3.93] | +0.00 [+0.00, +0.00] | 58.4% | 29.1% | 71 |
| Z|TREND:1:1 & Z|RSI14:0:0 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 226 of 474 (48%) | +1.50 [+0.25, +2.71] | +0.71 [+0.12, +1.34] | -3.81 [-4.22, -3.38] | 80.5% | 43.4% | 34 |
| Z|TREND:1:1 & Z|RSI14:0:0 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 164 of 474 (35%) | -0.47 [-1.54, +0.67] | -0.16 [-0.55, +0.24] | -6.00 [-6.70, -5.33] | 86.0% | 48.8% | 25 |
| Z|TREND:1:1 & Z|RSI14:0:0 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 164 of 474 (35%) | +0.65 [-0.54, +1.85] | +0.22 [-0.19, +0.66] | -4.89 [-5.45, -4.29] | 86.0% | 48.8% | 25 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 207 of 207 (100%) | +3.79 [+1.59, +5.78] | +3.79 [+1.59, +5.78] | +0.00 [+0.00, +0.00] | 54.1% | 32.4% | 31 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 155 of 207 (75%) | +4.95 [+2.65, +7.10] | +3.71 [+1.84, +5.45] | -0.84 [-1.14, -0.60] | 67.1% | 41.3% | 23 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 66 of 207 (32%) | +3.57 [+0.55, +6.69] | +1.14 [+0.16, +2.23] | -6.23 [-7.73, -4.95] | 83.3% | 59.1% | 10 |
| F|d_donch_pos_50_rmean50>0 & Z|RSI14:1:1 & G|up1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 66 of 207 (32%) | +5.36 [+2.06, +8.81] | +1.71 [+0.60, +2.93] | -4.44 [-5.63, -3.44] | 83.3% | 59.1% | 10 |

## Money: the arms alone and together (one position per pick, Rs 5 L, profits reinvested, from 2022)

Dip arm: ZONES_20261108_001: 21538 setup trades, 7403 of them IN their picks zone. Worst fall = the largest fall from a peak, counted when trades close (open positions' daily swings would show more). In-sample: the candidates and the zones were chosen on these years. One slot holds a 5-session trade, so a slot carries about one trade a week.

| engine | book | slots | MTF | Rs 5 L became | a year | worst fall | trades a week | skipped (slots full) |
|---|---|---:|---|---:|---:|---:|---:|---:|
| D | plan: ranks 1-3 at the D1 open | 2 | none | Rs 4,550,811 | +59.7% | 46.5% | 1.9 | 2793 |
| D | plan: ranks 1-3 at the D1 open | 2 | 2x | Rs 8,877,182 | +84.0% | 75.6% | 1.9 | 2793 |
| D | plan: ranks 1-3 at the D1 open | 3 | none | Rs 4,820,133 | +61.7% | 54.7% | 2.8 | 2561 |
| D | plan: ranks 1-3 at the D1 open | 3 | 2x | Rs 10,673,077 | +91.3% | 83.0% | 2.8 | 2561 |
| D | plan: ranks 1-3 at the D1 open | 5 | none | Rs 3,500,126 | +51.1% | 44.2% | 4.7 | 2098 |
| D | plan: ranks 1-3 at the D1 open | 5 | 2x | Rs 7,906,770 | +79.5% | 72.3% | 4.7 | 2098 |
| D | plan: ranks 1-3 at the D1 open | 7 | none | Rs 4,249,148 | +57.4% | 40.4% | 6.6 | 1642 |
| D | plan: ranks 1-3 at the D1 open | 7 | 2x | Rs 12,608,602 | +98.2% | 67.9% | 6.6 | 1642 |
| D | no-dip arm: the candidates at the D1 open | 2 | none | Rs 7,643,220 | +78.3% | 28.4% | 1.1 | 1017 |
| D | no-dip arm: the candidates at the D1 open | 2 | 2x | Rs 49,535,535 | +164.9% | 51.4% | 1.1 | 1017 |
| D | no-dip arm: the candidates at the D1 open | 3 | none | Rs 6,625,765 | +72.9% | 18.4% | 1.4 | 927 |
| D | no-dip arm: the candidates at the D1 open | 3 | 2x | Rs 44,606,878 | +159.1% | 35.1% | 1.4 | 927 |
| D | no-dip arm: the candidates at the D1 open | 5 | none | Rs 4,819,939 | +61.7% | 13.2% | 2.0 | 792 |
| D | no-dip arm: the candidates at the D1 open | 5 | 2x | Rs 28,246,931 | +135.2% | 26.3% | 2.0 | 792 |
| D | no-dip arm: the candidates at the D1 open | 7 | none | Rs 3,154,437 | +47.8% | 16.5% | 2.4 | 702 |
| D | no-dip arm: the candidates at the D1 open | 7 | 2x | Rs 13,505,083 | +101.1% | 31.9% | 2.4 | 702 |
| D | dip arm: S3 in its zone | 2 | none | Rs 1,871,035 | +32.3% | 19.6% | 0.4 | 138 |
| D | dip arm: S3 in its zone | 2 | 2x | Rs 5,212,789 | +64.4% | 37.1% | 0.4 | 138 |
| D | dip arm: S3 in its zone | 3 | none | Rs 1,428,525 | +24.9% | 19.3% | 0.5 | 114 |
| D | dip arm: S3 in its zone | 3 | 2x | Rs 3,337,712 | +49.5% | 36.4% | 0.5 | 114 |
| D | dip arm: S3 in its zone | 5 | none | Rs 1,073,428 | +17.6% | 8.0% | 0.6 | 85 |
| D | dip arm: S3 in its zone | 5 | 2x | Rs 2,080,224 | +35.3% | 15.6% | 0.6 | 85 |
| D | dip arm: S3 in its zone | 7 | none | Rs 924,266 | +13.9% | 8.4% | 0.7 | 66 |
| D | dip arm: S3 in its zone | 7 | 2x | Rs 1,588,574 | +27.8% | 16.5% | 0.7 | 66 |
| D | dip arm: all 7 setups (in-zone first) | 2 | none | Rs 671,380 | +6.4% | 52.0% | 1.8 | 2736 |
| D | dip arm: all 7 setups (in-zone first) | 2 | 2x | Rs 295,094 | -10.6% | 86.1% | 1.8 | 2736 |
| D | dip arm: all 7 setups (in-zone first) | 3 | none | Rs 890,204 | +13.0% | 42.2% | 2.7 | 2523 |
| D | dip arm: all 7 setups (in-zone first) | 3 | 2x | Rs 662,417 | +6.1% | 73.7% | 2.7 | 2523 |
| D | dip arm: all 7 setups (in-zone first) | 5 | none | Rs 1,180,030 | +20.0% | 39.8% | 4.3 | 2138 |
| D | dip arm: all 7 setups (in-zone first) | 5 | 2x | Rs 1,324,636 | +22.9% | 67.4% | 4.3 | 2138 |
| D | dip arm: all 7 setups (in-zone first) | 7 | none | Rs 1,073,239 | +17.6% | 28.3% | 5.6 | 1800 |
| D | dip arm: all 7 setups (in-zone first) | 7 | 2x | Rs 1,210,569 | +20.6% | 52.7% | 5.6 | 1800 |
| D | BOTH ARMS: no-dip + S3 in its zone | 2 | none | Rs 7,755,971 | +78.8% | 29.4% | 1.2 | 1195 |
| D | BOTH ARMS: no-dip + S3 in its zone | 2 | 2x | Rs 45,958,218 | +160.7% | 54.1% | 1.2 | 1195 |
| D | BOTH ARMS: no-dip + S3 in its zone | 3 | none | Rs 6,244,164 | +70.8% | 19.1% | 1.6 | 1091 |
| D | BOTH ARMS: no-dip + S3 in its zone | 3 | 2x | Rs 36,482,300 | +148.3% | 38.5% | 1.6 | 1091 |
| D | BOTH ARMS: no-dip + S3 in its zone | 5 | none | Rs 5,781,468 | +68.0% | 19.6% | 2.3 | 924 |
| D | BOTH ARMS: no-dip + S3 in its zone | 5 | 2x | Rs 38,260,650 | +150.8% | 37.3% | 2.3 | 924 |
| D | BOTH ARMS: no-dip + S3 in its zone | 7 | none | Rs 4,560,721 | +59.8% | 18.2% | 2.8 | 807 |
| D | BOTH ARMS: no-dip + S3 in its zone | 7 | 2x | Rs 26,467,304 | +132.0% | 35.0% | 2.8 | 807 |
| D | BOTH ARMS: no-dip + all 7 setups | 2 | none | Rs 4,711,656 | +60.9% | 43.2% | 1.9 | 3671 |
| D | BOTH ARMS: no-dip + all 7 setups | 2 | 2x | Rs 12,574,520 | +98.1% | 73.0% | 1.9 | 3671 |
| D | BOTH ARMS: no-dip + all 7 setups | 3 | none | Rs 4,123,496 | +56.4% | 32.1% | 2.8 | 3451 |
| D | BOTH ARMS: no-dip + all 7 setups | 3 | 2x | Rs 11,889,559 | +95.8% | 57.9% | 2.8 | 3451 |
| D | BOTH ARMS: no-dip + all 7 setups | 5 | none | Rs 3,952,197 | +55.0% | 25.9% | 4.5 | 3027 |
| D | BOTH ARMS: no-dip + all 7 setups | 5 | 2x | Rs 12,784,925 | +98.8% | 47.7% | 4.5 | 3027 |
| D | BOTH ARMS: no-dip + all 7 setups | 7 | none | Rs 3,073,808 | +47.0% | 22.2% | 6.0 | 2650 |
| D | BOTH ARMS: no-dip + all 7 setups | 7 | 2x | Rs 8,637,544 | +82.9% | 42.4% | 6.0 | 2650 |
| ENS | plan: ranks 1-3 at the D1 open | 2 | none | Rs 19,296,990 | +116.6% | 40.3% | 1.9 | 2950 |
| ENS | plan: ranks 1-3 at the D1 open | 2 | 2x | Rs 158,594,949 | +238.3% | 68.5% | 1.9 | 2950 |
| ENS | plan: ranks 1-3 at the D1 open | 3 | none | Rs 6,642,913 | +72.9% | 52.4% | 2.8 | 2717 |
| ENS | plan: ranks 1-3 at the D1 open | 3 | 2x | Rs 22,293,065 | +123.4% | 81.1% | 2.8 | 2717 |
| ENS | plan: ranks 1-3 at the D1 open | 5 | none | Rs 5,843,180 | +68.2% | 45.0% | 4.7 | 2251 |
| ENS | plan: ranks 1-3 at the D1 open | 5 | 2x | Rs 21,748,376 | +122.2% | 73.1% | 4.7 | 2251 |
| ENS | plan: ranks 1-3 at the D1 open | 7 | none | Rs 5,289,811 | +64.7% | 35.2% | 6.6 | 1785 |
| ENS | plan: ranks 1-3 at the D1 open | 7 | 2x | Rs 18,201,927 | +114.0% | 60.8% | 6.6 | 1785 |
| ENS | no-dip arm: the candidates at the D1 open | 2 | none | Rs 8,597,469 | +82.6% | 28.4% | 1.1 | 1029 |
| ENS | no-dip arm: the candidates at the D1 open | 2 | 2x | Rs 59,587,210 | +175.0% | 54.7% | 1.1 | 1029 |
| ENS | no-dip arm: the candidates at the D1 open | 3 | none | Rs 4,950,815 | +62.4% | 19.3% | 1.4 | 940 |
| ENS | no-dip arm: the candidates at the D1 open | 3 | 2x | Rs 24,972,450 | +128.8% | 36.6% | 1.4 | 940 |
| ENS | no-dip arm: the candidates at the D1 open | 5 | none | Rs 4,307,611 | +57.7% | 15.2% | 2.0 | 808 |
| ENS | no-dip arm: the candidates at the D1 open | 5 | 2x | Rs 21,923,969 | +122.6% | 30.0% | 2.0 | 808 |
| ENS | no-dip arm: the candidates at the D1 open | 7 | none | Rs 3,112,297 | +47.2% | 16.0% | 2.3 | 721 |
| ENS | no-dip arm: the candidates at the D1 open | 7 | 2x | Rs 12,820,276 | +98.7% | 31.3% | 2.3 | 721 |
| ENS | dip arm: S3 in its zone | 2 | none | Rs 2,292,837 | +38.0% | 17.5% | 0.4 | 139 |
| ENS | dip arm: S3 in its zone | 2 | 2x | Rs 7,809,358 | +78.9% | 33.0% | 0.4 | 139 |
| ENS | dip arm: S3 in its zone | 3 | none | Rs 1,432,239 | +24.9% | 12.7% | 0.5 | 111 |
| ENS | dip arm: S3 in its zone | 3 | 2x | Rs 3,351,643 | +49.6% | 24.6% | 0.5 | 111 |
| ENS | dip arm: S3 in its zone | 5 | none | Rs 1,109,130 | +18.4% | 7.8% | 0.6 | 81 |
| ENS | dip arm: S3 in its zone | 5 | 2x | Rs 2,195,488 | +36.8% | 15.3% | 0.6 | 81 |
| ENS | dip arm: S3 in its zone | 7 | none | Rs 1,008,844 | +16.0% | 5.6% | 0.7 | 61 |
| ENS | dip arm: S3 in its zone | 7 | 2x | Rs 1,880,804 | +32.4% | 11.1% | 0.7 | 61 |
| ENS | dip arm: all 7 setups (in-zone first) | 2 | none | Rs 1,381,895 | +24.0% | 43.2% | 1.9 | 3115 |
| ENS | dip arm: all 7 setups (in-zone first) | 2 | 2x | Rs 1,480,920 | +25.8% | 72.2% | 1.9 | 3115 |
| ENS | dip arm: all 7 setups (in-zone first) | 3 | none | Rs 1,700,007 | +29.6% | 31.5% | 2.7 | 2895 |
| ENS | dip arm: all 7 setups (in-zone first) | 3 | 2x | Rs 2,394,349 | +39.3% | 59.1% | 2.7 | 2895 |
| ENS | dip arm: all 7 setups (in-zone first) | 5 | none | Rs 1,852,369 | +31.9% | 26.6% | 4.4 | 2492 |
| ENS | dip arm: all 7 setups (in-zone first) | 5 | 2x | Rs 3,180,977 | +47.9% | 51.0% | 4.4 | 2492 |
| ENS | dip arm: all 7 setups (in-zone first) | 7 | none | Rs 1,484,268 | +25.9% | 26.5% | 5.9 | 2129 |
| ENS | dip arm: all 7 setups (in-zone first) | 7 | 2x | Rs 2,187,080 | +36.7% | 48.4% | 5.9 | 2129 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 2 | none | Rs 8,811,332 | +83.5% | 22.3% | 1.2 | 1209 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 2 | 2x | Rs 58,119,336 | +173.6% | 41.7% | 1.2 | 1209 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 3 | none | Rs 8,616,255 | +82.7% | 17.7% | 1.6 | 1104 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 3 | 2x | Rs 67,057,496 | +182.0% | 33.8% | 1.6 | 1104 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 5 | none | Rs 6,051,351 | +69.5% | 17.2% | 2.3 | 939 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 5 | 2x | Rs 40,448,581 | +153.4% | 33.1% | 2.3 | 939 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 7 | none | Rs 4,454,775 | +58.9% | 16.2% | 2.8 | 822 |
| ENS | BOTH ARMS: no-dip + S3 in its zone | 7 | 2x | Rs 24,700,343 | +128.3% | 31.1% | 2.8 | 822 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 2 | none | Rs 1,972,170 | +33.7% | 36.9% | 1.9 | 4041 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 2 | 2x | Rs 2,772,711 | +43.7% | 63.7% | 1.9 | 4041 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 3 | none | Rs 3,131,870 | +47.4% | 35.2% | 2.8 | 3818 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 3 | 2x | Rs 7,323,628 | +76.5% | 60.9% | 2.8 | 3818 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 5 | none | Rs 4,538,733 | +59.5% | 31.8% | 4.5 | 3385 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 5 | 2x | Rs 17,076,274 | +111.1% | 57.7% | 4.5 | 3385 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 7 | none | Rs 3,881,889 | +54.3% | 20.8% | 6.1 | 2995 |
| ENS | BOTH ARMS: no-dip + all 7 setups | 7 | 2x | Rs 13,831,839 | +101.9% | 41.0% | 6.1 | 2995 |

## Limits

- Everything here is on the history the engines, the setups and the zones were studied on; the replay guards the search, not the list of conditions. Only the forward paper ledger is clean evidence.
- The D1 open and the gap are the cache's; a pre-open (AMO) order fills at the open price. The breakout fills at the stop (or the open above it) with no slippage; the D1-close entry fills at the official close.
- The money view ignores taxes and assumes every order fills; MTF needs the stock on the broker's list.
