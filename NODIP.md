# No-dip study v2 - which picks will not dip (09 Nov 2026, setuplab v1.0)

Watchlist C:\QuantData\setuplab\WL_R1_10; panel C:\QuantData\cache_daily\panel_oc\panel.parquet; features features_final.txt. D: 15818 of 15818 settled picks complete; ENS: 16256 of 16256 settled picks complete; pooled 25831 stock-days, 6243 of them picked by both engines (counted once).

**The rule (declared before any result):** nodip v2, declared 8 Nov 2026 before any result (Karan: test it as rigorously as the setups - which features and combinations help most and how they behaved in the sessions before the pick; be very open, we are exploring). PICKS: engines D and ENS, ranks 1-10, bought at the D1 open, sold at the D5 close, 0.35 pp costs, judged on the POOLED picks: a stock-day picked by both engines counts once (its best rank); each engine is also checked on its own. DIP = a close on D1-D4 at least 2% below the D1 open; RUNNER = no dip and the D5 close 5% or more above the D1 open. THREE LISTS from the same search: no-dip (target = the share of picks with no dip), runner (the runner share), money (net % per trade). CONDITIONS, all known at the signal close or the D1 open: for each of the 60 features - its level at the signal close (low third, high third, lower half, upper half; the cut-offs come from the picks of the window the rule is chosen on, never from later ones), its move on the signal day (rose / fell), its move on the session before the pick (rose / fell) and the two together (rose twice, fell twice, turned up, turned down); the stock's own candles into the pick (green / red signal day, a close in the top / bottom third of its range, a gap up / down, a 2% rise / fall, up / down over 3 sessions, two higher / lower closes in a row); the 12 zone measures; the model's rank, both engines picking it, D1's weekday, the market context and the stock's state at the pick, the gap at the D1 open. SEARCH: stage 1 every single condition; stage 2 every pair from different families (a feature's level may pair with its own moves); stage 3 the 150 best earning pairs of each list with one more rank / agreement / weekday / context / gap condition. Per list, the 5,000 best by a quick day-clustered lower bound of its target are tested for every condition earning its place (quick) and the first 60 that pass get the full block bootstrap. A rule QUALIFIES for its list when, on the pooled picks: 25 or more trades a year; its target's excess over all picks of the same days (resampled together) has a 95% interval above 0; net per trade at the D1 open 95% above 0; every condition earns its place on the target (the rule minus the trades its simpler version adds, 95% above 0); net <= 0 in at most 2 of its years; and in each engine on its own the target beats that engine's picks and the net is above 0. Score = the lower 95% bound of the target. CANDIDATES: per list the top 5 qualifiers that are not versions of each other (conditions within, or 70% of the same trades); the 10 best by score are listed too, qualified or not. Plain 95% per rule (be very open): the whole search is replayed year by year 2022-2026 (chosen with the picks whose D5 exit was before 1 January - the cut-offs too - and judged on that year); per list HOLDS when the chosen rules' target beats all picks out of sample (95%), WORSE when below, else NOT SHOWN. MONEY, apples to apples: Rs 5 L in 2 / 3 / 5 / 7 equal slots, profits reinvested, no MTF and MTF 2x, entries from 2022, one position per pick, the same open by the model's rank: the baseline (each engine's ranks 1-3 at the D1 open) against each list's arm OUT OF SAMPLE (each year the rules chosen from the years before), the arm in-sample (the candidates) and the out-of-sample arm with S3 in its zone (the newest ZONES run; in-sample). ENTRIES: the D1 open against the breakout, the D2 open after a strong D1 and the D1 close after a strong D1, on the same picks.

Shares are % of picks; net is % per trade after 0.35 pp costs. 'vs all' = the rule minus all picks of the same days. Rs a year = net x trades a year x Rs 1,000 (Rs 1 L a trade).

**How to read the candidates (be very open, plain 95%):** with 360,000 rules some qualify by luck. Two columns separate them: 'years better than all picks' (in-sample consistency) and 'replay' - the years in which the replay chose the SAME rule from the years before, and how it did in that year against all picks (out of sample). A candidate with replay years that beat all picks has out-of-sample support; 'never chosen' = in-sample only.

## At a glance: out of sample, apples to apples

- **no-dip list: HOLDS.** Each year's rules chosen from the years before took 1261 picks in 2022-2026: no-dip share 70.3% vs 54.6% for all picks (difference [95%]: +11.5 pts to +19.6 pts); net +0.64 vs +0.60 per trade (difference [95%]: -0.49 to +0.54).
- **runner list: HOLDS.** Each year's rules chosen from the years before took 693 picks in 2022-2026: runner share 24.5% vs 18.1% for all picks (difference [95%]: +2.7 pts to +10.8 pts); net +0.90 vs +0.60 per trade (difference [95%]: -0.94 to +1.63).
- **money list: NOT SHOWN.** Each year's rules chosen from the years before took 862 picks in 2022-2026: net % per trade at the D1 open +1.27 vs +0.60 for all picks (difference [95%]: -0.73 to +1.87); net +1.27 vs +0.60 per trade (difference [95%]: -0.73 to +1.87).

Money, Rs 5 L from 2022, no MTF (out-of-sample arms: each year only rules chosen from the years before; the baseline needs no choosing; MTF 2x and 2 / 7 slots in the full table):

| engine | book | 3 slots: a year | worst fall | trades a week | 5 slots: a year | worst fall | trades a week |
|---|---|---:|---:|---:|---:|---:|---:|
| D | baseline: ranks 1-3 at the D1 open | +61.7% | 54.7% | 2.8 | +51.1% | 44.2% | 4.7 |
| D | no-dip arm, out of sample | +12.4% | 26.0% | 1.2 | +8.4% | 19.0% | 1.7 |
| D | no-dip arm, out of sample + S3 in its zone | +33.9% | 28.3% | 1.6 | +28.3% | 16.0% | 2.2 |
| D | runner arm, out of sample | +18.4% | 31.8% | 1.1 | +10.9% | 29.1% | 1.4 |
| D | runner arm, out of sample + S3 in its zone | +28.2% | 31.8% | 1.3 | +18.8% | 32.4% | 1.7 |
| D | money arm, out of sample | +7.9% | 43.2% | 0.9 | +7.1% | 34.8% | 1.3 |
| D | money arm, out of sample + S3 in its zone | +17.6% | 45.5% | 1.1 | +15.7% | 31.5% | 1.6 |
| ENS | baseline: ranks 1-3 at the D1 open | +73.0% | 52.4% | 2.8 | +68.4% | 45.0% | 4.7 |
| ENS | no-dip arm, out of sample | +37.4% | 27.7% | 1.4 | +24.0% | 23.3% | 2.0 |
| ENS | no-dip arm, out of sample + S3 in its zone | +63.4% | 28.3% | 1.8 | +40.8% | 25.0% | 2.5 |
| ENS | runner arm, out of sample | +23.4% | 43.4% | 1.1 | +19.4% | 37.3% | 1.4 |
| ENS | runner arm, out of sample + S3 in its zone | +29.3% | 41.9% | 1.3 | +31.2% | 37.3% | 1.8 |
| ENS | money arm, out of sample | +8.5% | 32.3% | 0.8 | +9.7% | 24.7% | 1.2 |
| ENS | money arm, out of sample + S3 in its zone | +24.3% | 30.8% | 1.1 | +20.9% | 27.1% | 1.6 |

## Base rates (every complete pick at the D1 open, sold at the D5 close)

| table | picks | no dip | runners | net per trade | ranks 1-3: no dip | ranks 1-3: net |
|---|---:|---:|---:|---:|---:|---:|
| D | 15818 | 53.6% | 19.8% | +0.85 | 52.7% | +1.24 |
| ENS | 16256 | 54.9% | 20.1% | +0.90 | 53.3% | +1.27 |
| pooled | 25831 | 54.7% | 19.4% | +0.80 | 53.7% | +1.22 |

## The no-dip list (in-sample: chosen on all the years) - target: no-dip share (never a close 2% below the D1 open on D1-D4)

| | rule | trades a year | no-dip share [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| N1 | d_donch_pos_50_rmean50 in its high third at the signal close (> 0.777783) & w_ret_13w in its lower half at the signal close (<= 16.4325) & D1 opens below the signal close (pre-open) | 31 | 80.4% [74.6%, 85.8%] | +25.6 pts [+20.1 pts, +31.0 pts] | 80.4% | 9.6% | +0.57 [+0.09, +1.10] | D 82.8% / ENS 78.1% | 17,853 | 4 of 4 | never chosen |
| N2 | ATRP ATR14 % of the close: below 3 at the signal close & a bullish stock state at the pick (S01-S03) & D1 opens below the signal close (pre-open) | 109 | 77.7% [73.9%, 81.5%] | +23.0 pts [+19.1 pts, +27.1 pts] | 77.7% | 8.7% | +0.38 [+0.05, +0.73] | D 75.6% / ENS 77.3% | 41,971 | 7 of 7 | never chosen |
| N3 | d_slope_stability in its high third at the signal close (> 5.05058) & ATRP ATR14 % of the close: below 3 at the signal close & D1 opens below the signal close (pre-open) | 97 | 78.4% [73.7%, 83.0%] | +23.7 pts [+19.2 pts, +28.5 pts] | 78.4% | 7.9% | +0.38 [+0.03, +0.74] | D 79.3% / ENS 75.2% | 36,483 | 7 of 7 | never chosen |
| N4 | w_ret_13w in its lower half at the signal close (<= 16.4325) & x_z_d_downside_dev_60 in its low third at the signal close (<= -0.187485) & the model's rank 1 | 36 | 78.4% [73.4%, 83.3%] | +23.7 pts [+18.5 pts, +28.7 pts] | 78.4% | 14.5% | +1.30 [+0.40, +2.49] | D 80.1% / ENS 74.5% | 47,064 | 4 of 4 | never chosen |
| N5 | d_adx14 fell on the session before the pick and on the signal day & ATRP ATR14 % of the close: 2 to 3 at the signal close & D1 opens below the signal close (pre-open) | 69 | 77.2% [72.5%, 81.8%] | +22.4 pts [+17.7 pts, +27.0 pts] | 77.2% | 9.1% | +0.58 [+0.12, +1.06] | D 79.0% / ENS 76.0% | 39,902 | 7 of 7 | never chosen |

Open list - the 10 best by score, qualified or not:

| | rule | trades a year | no-dip share [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B1 | d_realvol_ratio_20_60 in its high third at the signal close (> 1.04055) & ATRP ATR14 % of the close: below 2 at the signal close & India VIX in the lower half of its last year (does NOT qualify) | 35 | 87.1% [79.2%, 92.7%] | +32.4 pts [+24.7 pts, +38.2 pts] | 87.1% | 4.3% | +0.32 [-0.22, +0.80] | D 89.8% / ENS 82.1% | 11,087 | 2 of 2 | never chosen |
| B2 | d_wq_29 fell on the session before the pick and on the signal day & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 45 | 84.7% [78.9%, 89.6%] | +30.0 pts [+24.3 pts, +35.2 pts] | 84.7% | 4.0% | +0.13 [-0.24, +0.46] | D 84.1% / ENS 86.7% | 5,794 | 5 of 5 | never chosen |
| B3 | d_ret_5d_roll_std rose on the session before the pick & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 90 | 82.6% [77.7%, 87.1%] | +27.9 pts [+22.8 pts, +32.6 pts] | 82.6% | 6.4% | +0.18 [-0.26, +0.57] | D 83.8% / ENS 80.2% | 15,783 | 7 of 7 | never chosen |
| B4 | d_vol_yz_50 rose on the session before the pick & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 83 | 82.1% [77.1%, 86.8%] | +27.4 pts [+22.3 pts, +32.3 pts] | 82.1% | 5.8% | +0.27 [-0.13, +0.64] | D 83.2% / ENS 79.3% | 22,548 | 7 of 7 | never chosen |
| B5 | ATRP ATR14 % of the close: below 2 at the signal close & RSI14 RSI 14: below 50 at the signal close (does NOT qualify) | 34 | 83.9% [76.8%, 89.8%] | +29.2 pts [+22.0 pts, +35.2 pts] | 83.9% | 4.5% | +0.12 [-0.44, +0.62] | D 88.1% / ENS 82.2% | 4,044 | 5 of 5 | 2024 +50.9 pts |
| B6 | d_cmf20_rmean50 in its lower half at the signal close (<= -0.0140144) & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 80 | 81.6% [76.8%, 86.0%] | +26.9 pts [+22.1 pts, +31.6 pts] | 81.6% | 6.4% | +0.14 [-0.25, +0.50] | D 81.0% / ENS 83.9% | 11,283 | 6 of 6 | never chosen |
| B7 | d_slope_stability rose on the session before the pick and on the signal day & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 62 | 82.2% [76.7%, 87.5%] | +27.4 pts [+22.1 pts, +33.1 pts] | 82.2% | 5.1% | +0.04 [-0.36, +0.43] | D 83.7% / ENS 80.2% | 2,736 | 4 of 4 | never chosen |
| B8 | d_amihud_20 rose on the session before the pick and on the signal day & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 51 | 82.5% [76.5%, 87.6%] | +27.8 pts [+21.9 pts, +33.2 pts] | 82.5% | 4.4% | +0.36 [-0.05, +0.70] | D 82.2% / ENS 82.2% | 18,395 | 5 of 5 | never chosen |
| B9 | d_wq_12 in its upper half at the signal close (> 0.05) & ATRP ATR14 % of the close: below 2 at the signal close (does NOT qualify) | 112 | 81.3% [76.4%, 85.4%] | +26.5 pts [+21.9 pts, +30.8 pts] | 81.3% | 5.9% | +0.07 [-0.30, +0.40] | D 82.6% / ENS 79.8% | 7,867 | 7 of 7 | never chosen |
| B10 | d_slope_stability in its high third at the signal close (> 5.05058) & ATRP ATR14 % of the close: below 3 at the signal close & NIFTY below its 50-day average (does NOT qualify) | 60 | 83.2% [76.3%, 88.2%] | +28.4 pts [+21.5 pts, +33.7 pts] | 83.2% | 7.5% | +0.62 [-0.01, +1.08] | D 85.3% / ENS 80.3% | 36,858 | 5 of 5 | never chosen |

## The runner list (in-sample: chosen on all the years) - target: runner share (no dip and the D5 close 5% or more above the D1 open)

| | rule | trades a year | runner share [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| U1 | w_ret_13w fell on the signal day & a bearish stock state at the pick (S08/S09) & D1 opens 1% or more below the signal close (pre-open) | 29 | 43.5% [34.6%, 52.3%] | +24.2 pts [+15.9 pts, +32.4 pts] | 65.8% | 43.5% | +4.41 [+2.11, +6.78] | D 42.4% / ENS 45.0% | 127,639 | 7 of 7 | 2023 +36.7 pts, 2024 +19.8 pts, 2025 +18.8 pts, 2026 +9.1 pts |
| U2 | d_ll_run in its high third at the signal close (> 2) & D1 (the buy day) is a Tuesday & D1 opens 1% or more below the signal close (pre-open) | 28 | 40.3% [32.4%, 48.5%] | +21.0 pts [+13.0 pts, +29.0 pts] | 63.4% | 40.3% | +3.73 [+1.85, +5.95] | D 40.0% / ENS 43.0% | 104,006 | 7 of 7 | 2026 +11.0 pts |
| U3 | D1 (the buy day) is a Tuesday & volatility elevated at the pick & D1 opens 1% or more below the signal close (pre-open) | 34 | 38.8% [30.6%, 48.2%] | +19.5 pts [+11.6 pts, +28.4 pts] | 59.4% | 38.8% | +4.11 [+2.29, +6.06] | D 37.8% / ENS 41.6% | 138,303 | 6 of 6 | never chosen |
| U4 | d_mdi14 in its upper half at the signal close (> 19.0334) & the signal day rose 2% or more & D1 (the buy day) is a Tuesday | 29 | 41.5% [30.3%, 51.5%] | +22.2 pts [+11.1 pts, +32.0 pts] | 63.1% | 41.5% | +3.83 [+1.32, +6.12] | D 36.8% / ENS 46.1% | 112,062 | 5 of 6 | 2026 +13.7 pts |
| U5 | d_wq_26 in its upper half at the signal close (> -0.579066) & D1 (the buy day) is a Tuesday & D1 opens 1% or more below the signal close (pre-open) | 28 | 38.2% [29.8%, 46.2%] | +18.8 pts [+10.3 pts, +26.7 pts] | 64.5% | 38.2% | +3.40 [+1.76, +4.96] | D 35.5% / ENS 40.0% | 94,771 | 6 of 7 | 2026 +12.5 pts |

Open list - the 10 best by score, qualified or not:

| | rule | trades a year | runner share [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B1 | w_ret_13w fell on the signal day & a bearish stock state at the pick (S08/S09) & D1 opens 1% or more below the signal close (pre-open) | 29 | 43.5% [34.6%, 52.3%] | +24.2 pts [+15.9 pts, +32.4 pts] | 65.8% | 43.5% | +4.41 [+2.11, +6.78] | D 42.4% / ENS 45.0% | 127,639 | 7 of 7 | 2023 +36.7 pts, 2024 +19.8 pts, 2025 +18.8 pts, 2026 +9.1 pts |
| B2 | d_ll_run in its high third at the signal close (> 2) & D1 (the buy day) is a Tuesday & D1 opens 1% or more below the signal close (pre-open) | 28 | 40.3% [32.4%, 48.5%] | +21.0 pts [+13.0 pts, +29.0 pts] | 63.4% | 40.3% | +3.73 [+1.85, +5.95] | D 40.0% / ENS 43.0% | 104,006 | 7 of 7 | 2026 +11.0 pts |
| B3 | D1 (the buy day) is a Tuesday & volatility elevated at the pick & D1 opens 1% or more below the signal close (pre-open) | 34 | 38.8% [30.6%, 48.2%] | +19.5 pts [+11.6 pts, +28.4 pts] | 59.4% | 38.8% | +4.11 [+2.29, +6.06] | D 37.8% / ENS 41.6% | 138,303 | 6 of 6 | never chosen |
| B4 | d_mdi14 in its upper half at the signal close (> 19.0334) & the signal day rose 2% or more & D1 (the buy day) is a Tuesday | 29 | 41.5% [30.3%, 51.5%] | +22.2 pts [+11.1 pts, +32.0 pts] | 63.1% | 41.5% | +3.83 [+1.32, +6.12] | D 36.8% / ENS 46.1% | 112,062 | 5 of 6 | 2026 +13.7 pts |
| B5 | d_wq_26 in its upper half at the signal close (> -0.579066) & D1 (the buy day) is a Tuesday & D1 opens 1% or more below the signal close (pre-open) | 28 | 38.2% [29.8%, 46.2%] | +18.8 pts [+10.3 pts, +26.7 pts] | 64.5% | 38.2% | +3.40 [+1.76, +4.96] | D 35.5% / ENS 40.0% | 94,771 | 6 of 7 | 2026 +12.5 pts |
| B6 | d_ema20_angle_deg in its low third at the signal close (<= -0.226484) & RS20 20-session return minus Smallcap 250's (pts): 5 and above at the signal close | 29 | 37.2% [29.8%, 44.7%] | +17.8 pts [+10.5 pts, +25.2 pts] | 56.5% | 37.2% | +3.03 [+1.24, +4.82] | D 38.4% / ENS 35.0% | 86,905 | 5 of 6 | never chosen |
| B7 | d_range_pct in its high third at the signal close (> 4.90722) & d_dist_from_52wl fell on the session before the pick and on the signal day & D1 opens 1% or more below the signal close (pre-open) | 116 | 34.3% [29.7%, 39.4%] | +15.0 pts [+10.8 pts, +19.4 pts] | 55.5% | 34.3% | +3.06 [+1.49, +4.62] | D 35.8% / ENS 35.0% | 355,306 | 7 of 7 | never chosen |
| B8 | d_ema20_angle_z252 in its low third at the signal close (<= -0.793322) & RS20 20-session return minus Smallcap 250's (pts): 5 and above at the signal close & India VIX in the upper half of its last year (does NOT qualify) | 26 | 38.2% [28.9%, 47.7%] | +18.8 pts [+9.7 pts, +28.0 pts] | 52.0% | 38.2% | +2.69 [-0.01, +5.51] | D 42.2% / ENS 36.2% | 69,845 | 5 of 5 | never chosen |
| B9 | d_wq_35 rose on the session before the pick and on the signal day & the other engine picked it too (its ranks 1-10) & D1 opens 1% or more below the signal close (pre-open) | 42 | 35.0% [28.8%, 41.7%] | +15.6 pts [+9.9 pts, +21.9 pts] | 54.3% | 35.0% | +3.31 [+1.85, +4.88] | D 35.0% / ENS 35.0% | 139,113 | 7 of 7 | never chosen |
| B10 | d_mdi14 in its upper half at the signal close (> 19.0334) & d_n_5pct_up_60 rose on the signal day | 25 | 40.2% [27.9%, 50.6%] | +20.9 pts [+9.4 pts, +30.7 pts] | 56.2% | 40.2% | +4.21 [+1.00, +6.92] | D 36.4% / ENS 39.3% | 106,714 | 5 of 5 | never chosen |

## The money list (in-sample: chosen on all the years) - target: net % per trade at the D1 open

| | rule | trades a year | net % per trade at the D1 open [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| M1 | d_atr_pct rose on the session before the pick and on the signal day & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & NIFTY above its 50-day average | 31 | +5.03 [+2.35, +7.68] | +4.23 [+1.55, +6.80] | 56.9% | 33.8% | +5.03 [+2.35, +7.68] | D +5.05 / ENS +5.34 | 153,958 | 4 of 4 | never chosen |
| M2 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & the other engine picked it too (its ranks 1-10) & a bearish stock state at the pick (S08/S09) | 29 | +4.98 [+2.23, +7.24] | +4.18 [+1.47, +6.37] | 58.7% | 32.1% | +4.98 [+2.23, +7.24] | D +4.98 / ENS +4.98 | 146,481 | 5 of 6 | never chosen |
| M3 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 0 to 1 at the signal close & a bearish stock state at the pick (S08/S09) & NIFTY above its 50-day average | 43 | +4.89 [+2.08, +7.60] | +4.09 [+1.33, +6.74] | 56.3% | 29.0% | +4.89 [+2.08, +7.60] | D +5.21 / ENS +5.11 | 209,978 | 4 of 4 | never chosen |
| M4 | d_upside_vol_ratio rose on the session before the pick and on the signal day & VIX5 India VIX 5-session change %: below -10 at the signal close & India VIX in the upper half of its last year | 65 | +4.05 [+2.00, +6.00] | +3.25 [+1.35, +5.08] | 63.7% | 34.0% | +4.05 [+2.00, +6.00] | D +4.59 / ENS +4.01 | 264,436 | 6 of 6 | 2026 +1.99 |
| M5 | d_atr_pct in its upper half at the signal close (> 4.67053) & d_realvol_20 in its low third at the signal close (<= 33.7557) & India VIX in the upper half of its last year | 34 | +4.31 [+1.97, +6.94] | +3.51 [+1.30, +5.96] | 58.4% | 29.2% | +4.31 [+1.97, +6.94] | D +4.54 / ENS +3.54 | 146,202 | 5 of 6 | never chosen |

Open list - the 10 best by score, qualified or not:

| | rule | trades a year | net % per trade at the D1 open [95%] | vs all picks [95%] | no dip | runners | net [95%] | D / ENS alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| B1 | RSI14 RSI 14: below 30 at the signal close & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & NIFTY above its 50-day average (does NOT qualify) | 33 | +5.14 [+2.47, +8.02] | +4.34 [+1.67, +7.13] | 57.5% | 29.9% | +5.14 [+2.47, +8.02] | D +5.62 / ENS +5.59 | 170,529 | 4 of 4 | never chosen |
| B2 | d_atr_pct rose on the session before the pick and on the signal day & IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & NIFTY above its 50-day average | 31 | +5.03 [+2.35, +7.68] | +4.23 [+1.55, +6.80] | 56.9% | 33.8% | +5.03 [+2.35, +7.68] | D +5.05 / ENS +5.34 | 153,958 | 4 of 4 | never chosen |
| B3 | TREND close vs EMA50 and EMA200: between at the signal close & RSI14 RSI 14: below 30 at the signal close & volatility elevated at the pick (does NOT qualify) | 49 | +3.61 [+2.28, +4.83] | +2.81 [+1.53, +3.96] | 56.6% | 30.5% | +3.61 [+2.28, +4.83] | D +3.51 / ENS +3.52 | 176,289 | 5 of 7 | never chosen |
| B4 | IDX NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many): 1 at the signal close & the other engine picked it too (its ranks 1-10) & a bearish stock state at the pick (S08/S09) | 29 | +4.98 [+2.23, +7.24] | +4.18 [+1.47, +6.37] | 58.7% | 32.1% | +4.98 [+2.23, +7.24] | D +4.98 / ENS +4.98 | 146,481 | 5 of 6 | never chosen |
| B5 | x_relvol_20 in its low third at the signal close (<= 2.35963) & RET20 20-session return %: below -10 at the signal close & NIFTY above its 50-day average (does NOT qualify) | 56 | +4.91 [+2.23, +7.40] | +4.11 [+1.48, +6.50] | 63.6% | 36.4% | +4.91 [+2.23, +7.40] | D +5.79 / ENS +4.18 | 273,603 | 6 of 6 | never chosen |
| B6 | d_upside_vol_ratio rose on the session before the pick and on the signal day & VIX5 India VIX 5-session change %: below -10 at the signal close & India VIX in the upper half of its last year | 65 | +4.05 [+2.00, +6.00] | +3.25 [+1.35, +5.08] | 63.7% | 34.0% | +4.05 [+2.00, +6.00] | D +4.59 / ENS +4.01 | 264,436 | 6 of 6 | 2026 +1.99 |
| B7 | d_atr_pct in its upper half at the signal close (> 4.67053) & d_realvol_20 in its low third at the signal close (<= 33.7557) & India VIX in the upper half of its last year | 34 | +4.31 [+1.97, +6.94] | +3.51 [+1.30, +5.96] | 58.4% | 29.2% | +4.31 [+1.97, +6.94] | D +4.54 / ENS +3.54 | 146,202 | 5 of 6 | never chosen |
| B8 | d_atr_pct in its high third at the signal close (> 5.33687) & x_relvol_20 in its low third at the signal close (<= 2.35963) & NIFTY above its 50-day average (does NOT qualify) | 47 | +5.73 [+1.83, +8.55] | +4.92 [+1.03, +7.61] | 63.1% | 43.3% | +5.73 [+1.83, +8.55] | D +5.81 / ENS +5.55 | 268,086 | 5 of 5 | never chosen |
| B9 | x_relvol_20 in its low third at the signal close (<= 2.35963) & the signal day rose 2% or more & not overextended at the pick | 87 | +3.94 [+1.79, +6.04] | +3.13 [+1.10, +5.03] | 57.2% | 32.6% | +3.94 [+1.79, +6.04] | D +4.02 / ENS +4.28 | 343,999 | 6 of 7 | never chosen |
| B10 | d_donch_pos_50_rmean50 in its low third at the signal close (<= 0.515133) & d_n_5pct_up_60 rose on the signal day | 29 | +4.59 [+1.78, +7.13] | +3.78 [+1.18, +6.20] | 56.8% | 38.5% | +4.59 [+1.78, +7.13] | D +3.63 / ENS +5.14 | 132,150 | 6 of 6 | never chosen |

## The year-by-year replay (each year: cut-offs and rules from the years before)

| year | list | rules chosen | picks in them | no dip in them / all | runners in them / all | net in them / all |
|---|---|---|---:|---:|---:|---:|
| 2022 | no-dip | V|x_relvol_20:L3 & Z|DD52:1:1 & C|VIX_HIGH; V|d_atr_pct:L3 & B|d_slope_stability:updn & C|VIX_HIGH; Z|ATRP:1:1 & Z|TREND:0:1 & C|BREADTH_UP; Z|ATRP:0:1 & Z|TREND:0:0; Z|DD52:1:1 & Z|IDX:0:1 & W|1 | 284 | 62.0% / 52.2% | 22.5% / 20.5% | +1.32 / +0.51 |
| 2022 | runner | V|d_ema20_angle_deg:L3 & B|d_donch_pos_50_rmean50:up1 & G|dn1; V|d_mdi14_rrank20:L3 & Z|NIFTY20:0:0 & C|BEARSTATE; B|w_ret_13w:dn1 & W|3; Z|VIX5:1:1 & P|agree & G|dn1; Z|VIX5:0:0 & Z|NIFTY20:0:0 & W|2 | 305 | 49.8% / 52.2% | 21.3% / 20.5% | +0.14 / +0.51 |
| 2022 | money | Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VIX_HIGH; V|d_ema20_angle_deg:H3 & P|alone & C|MKT_BEAR | 103 | 45.6% / 52.2% | 26.2% / 20.5% | +1.12 / +0.51 |
| 2023 | no-dip | V|d_upside_vol_ratio:L3 & Z|ATRP:0:1 & C|BREADTH_UP; Z|ATRP:0:1 & Z|TREND:0:0; V|d_vol_yz_20:L3 & B|d_wq_29:updn & G|dn0; V|d_dist_from_52wl:L3 & Z|ATRP:1:1; V|d_ema20_angle_z252:H3 & Z|RET20:1:1 & C|BREADTH_UP | 626 | 77.8% / 67.0% | 11.8% / 13.3% | +0.94 / +0.72 |
| 2023 | runner | B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1; B|d_amihud_20:dnup & C|VIX_LOW & G|dn1; Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VIX_HIGH; Z|RSI14:0:0 & Z|VIX5:0:1 & G|dn1; V|d_mdi14_rrank10:H3 & W|1 & G|dn1 | 69 | 52.2% / 67.0% | 29.0% / 13.3% | +1.20 / +0.72 |
| 2023 | money | Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VIX_HIGH; V|d_amihud_60:H3 & Z|VIX5:0:0 & C|BEARSTATE; B|d_realvol_20:upup & Z|VIX5:0:0 & C|VIX_HIGH; B|d_slope_stability:up0 & Z|VIX5:0:0 & C|VIX_HIGH; B|d_adx14:upup & Z|VIX5:0:0 & C|VIX_HIGH | 45 | 66.7% / 67.0% | 24.4% / 13.3% | +3.08 / +0.72 |
| 2024 | no-dip | Z|ATRP:0:0 & Z|RSI14:0:1; V|d_atr_pct:L3 & V|d_dist_from_52wl:L3 & P|top3; V|d_dist_from_52wl:L3 & Z|ATRP:1:1 & C|NIFTY_UP; Z|ATRP:0:1 & Z|RSI14:0:1 & P|top3; V|d_atr_pct:L3 & Z|TREND:0:0 & C|BREADTH_UP | 13 | 61.5% / 49.1% | 15.4% / 21.1% | -1.21 / +1.03 |
| 2024 | runner | B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1; Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VIX_HIGH; V|d_slope_stability_rmean50:L3 & P|rank1 & G|dn1; Z|RSI14:0:0 & Z|VIX5:0:1 & G|dn1; B|d_amihud_20:dnup & C|VIX_LOW & G|dn1 | 132 | 47.7% / 49.1% | 25.0% / 21.1% | +1.33 / +1.03 |
| 2024 | money | Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VIX_HIGH; V|d_slope_stability_rmean50:L3 & Z|VIX5:0:0 & C|BEARSTATE; V|d_amihud_60:H3 & Z|VIX5:0:0 & C|BEARSTATE; V|d_mdi14_rrank20:LO & Z|RSI14:0:0 & P|agree; B|d_slope_stability:up0 & Z|VIX5:0:0 & C|VIX_HIGH | 271 | 53.1% / 49.1% | 29.5% / 21.1% | +2.92 / +1.03 |
| 2025 | no-dip | Z|ATRP:0:1 & Z|RSI14:0:1 & P|top3; V|d_dist_from_52wl:L3 & Z|ATRP:1:1 & C|BREADTH_UP; V|d_upside_vol_ratio:L3 & Z|ATRP:1:1 & C|BREADTH_UP; V|d_dist_from_52wl:LO & Z|ATRP:1:1 & P|top3; Z|ATRP:0:1 & Z|TREND:0:0 | 161 | 66.5% / 51.3% | 5.6% / 17.9% | -0.14 / +0.20 |
| 2025 | runner | B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1; B|w_ret_13w:dn0 & C|VOL_ELEV & G|dn1; Z|RSI14:0:0 & Z|VIX5:1:1 & G|dn1; V|d_wq_33:H3 & W|1 & G|dn1; B|d_dist_from_52wl:dndn & W|1 & G|dn1 | 146 | 55.5% / 51.3% | 28.8% / 17.9% | +2.19 / +0.20 |
| 2025 | money | Z|RSI14:0:0 & Z|IDX:1:1; B|d_cpr_width_pct:upup & Z|RSI14:0:0 & G|up1; V|d_adx14:H3 & P|agree3 & C|VOL_ELEV; V|d_mdi14_rrank20:LO & Z|RSI14:0:0 & P|agree; Z|IDX:1:1 & C|BEARSTATE & C|VOL_ELEV | 284 | 46.5% / 51.3% | 16.2% / 17.9% | +0.09 / +0.20 |
| 2026 | no-dip | Z|ATRP:1:1 & Z|TREND:0:1 & C|BREADTH_UP; V|d_dist_from_52wl:L3 & Z|ATRP:1:1 & C|BREADTH_UP; V|d_realvol_20:L3 & V|x_z_d_downside_dev_60:L3 & C|VOL_ELEV; V|d_upside_vol_ratio:L3 & Z|ATRP:0:1; V|x_z_d_downside_dev_60:L3 & Z|RSI14:1:1 & P|top3 | 177 | 61.0% / 51.0% | 7.9% / 17.5% | -0.70 / +0.43 |
| 2026 | runner | B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1; V|d_ll_run:H3 & W|1 & G|dn1; V|d_mdi14:HI & X|bigup & W|1; B|d_vol_yz_20:up1 & W|1 & G|dn1; V|d_wq_26:HI & W|1 & G|dn1 | 41 | 51.2% / 51.0% | 24.4% / 17.5% | +0.15 / +0.43 |
| 2026 | money | Z|RSI14:0:0 & Z|IDX:1:1; V|d_wq_40:H3 & Z|IDX:1:1 & P|agree; B|d_adx14:upup & Z|IDX:1:1 & C|NIFTY_UP; B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH; Z|VIX5:0:0 & Z|NIFTY20:0:0 & C|VOL_ELEV | 159 | 50.3% / 51.0% | 21.4% / 17.5% | +0.13 / +0.43 |

## Stage 1: what separates the picks that do NOT dip (single conditions, by the lower bound of the no-dip share)

| condition | trades a year | no dip [lower bound] | runners [lower bound] | net [lower bound] | D no dip / net | ENS no dip / net |
|---|---:|---:|---:|---:|---:|---:|
| ATRP ATR14 % of the close: below 2 at the signal close | 228 | 78.8% [75.9%] | 5.1% [4.0%] | +0.02 [-0.18] | 79.6% / +0.13 | 77.9% / -0.19 |
| ATRP ATR14 % of the close: below 3 at the signal close | 728 | 72.7% [70.8%] | 9.6% [8.6%] | +0.29 [+0.13] | 74.2% / +0.31 | 70.4% / +0.23 |
| ATRP ATR14 % of the close: 2 to 3 at the signal close | 500 | 69.9% [67.9%] | 11.6% [10.4%] | +0.42 [+0.22] | 70.9% / +0.43 | 68.0% / +0.36 |
| d_atr_pct in its low third at the signal close (<= 3.93264) | 1292 | 66.6% [65.1%] | 12.8% [11.9%] | +0.41 [+0.25] | 67.5% / +0.34 | 65.1% / +0.46 |
| d_realvol_20 in its low third at the signal close (<= 33.7557) | 1292 | 66.3% [64.8%] | 13.6% [12.7%] | +0.60 [+0.43] | 66.7% / +0.58 | 65.1% / +0.64 |
| x_z_d_downside_dev_60 in its low third at the signal close (<= -0.187485) | 1292 | 66.2% [64.7%] | 14.2% [13.4%] | +0.64 [+0.49] | 66.7% / +0.73 | 65.0% / +0.63 |
| d_vol_yz_20 in its low third at the signal close (<= 0.0268583) | 1292 | 66.1% [64.5%] | 12.8% [11.9%] | +0.39 [+0.23] | 66.3% / +0.28 | 64.9% / +0.44 |
| d_bb_bw_20 in its low third at the signal close (<= 0.139628) | 1292 | 65.4% [63.9%] | 13.6% [12.7%] | +0.44 [+0.28] | 66.3% / +0.39 | 64.2% / +0.45 |
| d_realvol_60 in its low third at the signal close (<= 40.5976) | 1292 | 65.3% [63.7%] | 13.4% [12.5%] | +0.49 [+0.31] | 65.5% / +0.47 | 63.7% / +0.52 |
| d_range_pct in its low third at the signal close (<= 2.79633) | 1292 | 64.9% [63.5%] | 13.9% [13.0%] | +0.44 [+0.26] | 65.5% / +0.41 | 63.6% / +0.48 |
| d_ret_5d_roll_std in its low third at the signal close (<= 5.20104) | 1292 | 64.7% [63.2%] | 13.2% [12.4%] | +0.47 [+0.29] | 65.1% / +0.46 | 63.2% / +0.45 |
| d_vol_yz_50 in its low third at the signal close (<= 0.0290626) | 1292 | 64.5% [62.9%] | 12.6% [11.8%] | +0.36 [+0.19] | 64.2% / +0.31 | 63.0% / +0.37 |
| x_relvol_20 in its low third at the signal close (<= 2.35963) | 1292 | 64.0% [62.2%] | 17.5% [16.1%] | +1.16 [+0.85] | 63.8% / +1.24 | 63.0% / +1.23 |
| ATRP ATR14 % of the close: below 4.5 at the signal close | 1774 | 63.1% [61.7%] | 14.7% [13.9%] | +0.48 [+0.32] | 62.9% / +0.45 | 62.5% / +0.51 |
| d_n_5pct_up_252 in its low third at the signal close (<= 9) | 1345 | 63.0% [61.5%] | 14.0% [13.1%] | +0.51 [+0.31] | 62.9% / +0.54 | 61.6% / +0.51 |
| RET20 20-session return %: 0 to 10 at the signal close | 1172 | 62.8% [61.2%] | 15.4% [14.4%] | +0.59 [+0.40] | 63.4% / +0.58 | 61.5% / +0.58 |
| x_z_d_downside_dev_60 in its lower half at the signal close (<= 0.347878) | 1938 | 62.1% [60.7%] | 16.7% [15.9%] | +0.79 [+0.63] | 61.9% / +0.88 | 61.4% / +0.79 |
| d_atr_pct in its lower half at the signal close (<= 4.67053) | 1938 | 61.8% [60.4%] | 15.1% [14.3%] | +0.48 [+0.32] | 61.4% / +0.47 | 61.4% / +0.52 |
| d_vol_yz_20 in its lower half at the signal close (<= 0.032401) | 1938 | 61.8% [60.4%] | 15.5% [14.7%] | +0.63 [+0.46] | 61.1% / +0.63 | 61.0% / +0.65 |
| d_bb_bw_20 in its lower half at the signal close (<= 0.203649) | 1938 | 61.7% [60.3%] | 16.0% [15.1%] | +0.57 [+0.40] | 62.1% / +0.56 | 61.0% / +0.58 |
| RET20 20-session return %: -10 to 10 at the signal close | 1811 | 61.7% [60.3%] | 15.7% [14.8%] | +0.56 [+0.38] | 61.8% / +0.52 | 61.1% / +0.59 |
| d_realvol_20 in its lower half at the signal close (<= 42.8542) | 1938 | 61.6% [60.2%] | 16.0% [15.1%] | +0.67 [+0.50] | 61.1% / +0.71 | 60.5% / +0.67 |
| d_n_5pct_up_60 in its low third at the signal close (<= 1) | 1355 | 61.3% [59.7%] | 14.9% [13.9%] | +0.55 [+0.34] | 60.7% / +0.59 | 59.8% / +0.59 |
| RS20 20-session return minus Smallcap 250's (pts): -5 to 5 at the signal close | 1112 | 61.3% [59.7%] | 15.0% [14.0%] | +0.52 [+0.33] | 62.3% / +0.52 | 59.6% / +0.54 |
| ATRX ATR14 % / its mean of the last 50 sessions: below 0.85 at the signal close | 712 | 61.6% [59.7%] | 19.7% [18.0%] | +1.07 [+0.74] | 60.4% / +1.02 | 62.7% / +1.11 |
| d_ret_5d_roll_std in its lower half at the signal close (<= 6.47866) | 1938 | 61.1% [59.7%] | 15.7% [14.9%] | +0.62 [+0.44] | 60.6% / +0.65 | 60.2% / +0.65 |
| d_range_pct in its lower half at the signal close (<= 3.7296) | 1938 | 60.9% [59.6%] | 15.3% [14.5%] | +0.48 [+0.30] | 60.7% / +0.45 | 60.2% / +0.55 |
| d_vol_yz_50 in its lower half at the signal close (<= 0.0340667) | 1938 | 60.9% [59.5%] | 15.1% [14.2%] | +0.50 [+0.33] | 60.0% / +0.44 | 60.3% / +0.59 |
| d_realvol_60 in its lower half at the signal close (<= 48.3442) | 1938 | 60.8% [59.4%] | 15.6% [14.7%] | +0.59 [+0.42] | 60.0% / +0.61 | 59.9% / +0.62 |
| ATRP ATR14 % of the close: 2 to 4.5 at the signal close | 1547 | 60.8% [59.4%] | 16.1% [15.3%] | +0.54 [+0.37] | 59.6% / +0.51 | 61.0% / +0.58 |

## Stage 1: what marks the runners (single conditions, by the lower bound of the runner share)

| condition | trades a year | no dip [lower bound] | runners [lower bound] | net [lower bound] | D no dip / net | ENS no dip / net |
|---|---:|---:|---:|---:|---:|---:|
| D1 opens 1% or more below the signal close (pre-open) | 390 | 53.0% [49.9%] | 27.3% [24.7%] | +1.44 [+0.76] | 51.4% / +1.39 | 52.9% / +1.62 |
| d_vol_yz_50 in its high third at the signal close (> 0.0385226) | 1292 | 47.9% [46.1%] | 24.8% [23.3%] | +1.26 [+0.84] | 47.6% / +1.31 | 48.8% / +1.44 |
| d_atr_pct in its high third at the signal close (> 5.33687) | 1292 | 46.9% [44.9%] | 24.9% [23.2%] | +1.29 [+0.82] | 47.0% / +1.31 | 47.7% / +1.48 |
| d_range_pct in its high third at the signal close (> 4.90722) | 1292 | 48.3% [46.4%] | 24.6% [23.1%] | +1.33 [+0.92] | 47.4% / +1.31 | 49.6% / +1.55 |
| d_vol_yz_20 in its high third at the signal close (> 0.0376302) | 1292 | 46.0% [44.2%] | 24.0% [22.5%] | +1.10 [+0.68] | 45.9% / +1.12 | 47.0% / +1.34 |
| d_vol_yz_50 in its upper half at the signal close (> 0.0340667) | 1938 | 48.6% [47.0%] | 23.6% [22.3%] | +1.11 [+0.77] | 48.3% / +1.20 | 49.3% / +1.23 |
| the signal day rose 2% or more | 370 | 48.7% [46.0%] | 24.8% [22.3%] | +1.13 [+0.57] | 47.2% / +1.05 | 50.5% / +1.36 |
| d_ret_5d_roll_std in its high third at the signal close (> 7.94039) | 1292 | 47.7% [45.9%] | 23.8% [22.3%] | +1.11 [+0.71] | 47.2% / +1.08 | 48.8% / +1.38 |
| d_bb_bw_20 in its high third at the signal close (> 0.280797) | 1292 | 46.7% [44.9%] | 23.8% [22.3%] | +1.13 [+0.71] | 46.0% / +1.07 | 47.8% / +1.41 |
| d_realvol_60 in its high third at the signal close (> 55.4191) | 1292 | 47.5% [45.7%] | 23.7% [22.2%] | +1.07 [+0.66] | 47.0% / +1.04 | 48.7% / +1.26 |
| d_atr_pct in its upper half at the signal close (> 4.67053) | 1938 | 47.7% [46.0%] | 23.6% [22.2%] | +1.13 [+0.77] | 47.4% / +1.15 | 48.5% / +1.29 |
| both engines have it in their ranks 1-3 | 248 | 49.7% [47.1%] | 24.3% [22.1%] | +1.44 [+0.93] | 49.7% / +1.44 | 49.7% / +1.44 |
| d_range_pct in its upper half at the signal close (> 3.7296) | 1938 | 48.6% [47.0%] | 23.4% [22.1%] | +1.13 [+0.80] | 47.8% / +1.18 | 49.5% / +1.27 |
| d_n_5pct_up_252 in its high third at the signal close (> 17) | 1216 | 49.0% [47.3%] | 23.4% [22.1%] | +1.03 [+0.71] | 48.3% / +1.01 | 50.2% / +1.20 |
| ATRP ATR14 % of the close: 4.5 and above at the signal close | 2102 | 47.7% [46.1%] | 23.3% [22.0%] | +1.08 [+0.74] | 47.4% / +1.12 | 48.4% / +1.24 |
| the model's rank 1 | 410 | 53.0% [51.0%] | 23.7% [21.9%] | +1.38 [+1.02] | 52.5% / +1.30 | 52.7% / +1.52 |
| d_vol_yz_20 in its upper half at the signal close (> 0.032401) | 1938 | 47.7% [46.1%] | 23.2% [21.9%] | +0.98 [+0.64] | 47.6% / +1.03 | 48.6% / +1.17 |
| d_realvol_60 in its upper half at the signal close (> 48.3442) | 1938 | 48.7% [47.1%] | 23.1% [21.9%] | +1.01 [+0.68] | 48.2% / +1.06 | 49.8% / +1.20 |
| d_amihud_60 in its high third at the signal close (> 0.00415061) | 1292 | 50.0% [48.3%] | 23.2% [21.8%] | +1.15 [+0.80] | 48.6% / +1.09 | 50.6% / +1.34 |
| volatility elevated at the pick | 1113 | 48.5% [46.4%] | 23.6% [21.8%] | +1.22 [+0.74] | 48.2% / +1.20 | 49.6% / +1.52 |
| RET20 20-session return %: below -10 at the signal close | 1102 | 47.7% [45.4%] | 23.6% [21.7%] | +1.24 [+0.72] | 47.0% / +1.19 | 48.6% / +1.45 |
| d_ret_5d_roll_std in its upper half at the signal close (> 6.47866) | 1938 | 48.4% [46.8%] | 23.0% [21.7%] | +0.99 [+0.66] | 47.7% / +1.02 | 49.5% / +1.16 |
| d_amihud_20 in its high third at the signal close (> 0.00347092) | 1292 | 49.4% [47.7%] | 23.1% [21.7%] | +1.14 [+0.77] | 48.3% / +1.13 | 49.9% / +1.35 |
| d_n_5pct_up_252 in its upper half at the signal close (> 13) | 1860 | 49.6% [48.1%] | 22.9% [21.7%] | +1.00 [+0.70] | 48.8% / +1.02 | 50.7% / +1.10 |
| d_ema20_angle_deg in its low third at the signal close (<= -0.226484) | 1292 | 48.1% [46.0%] | 23.3% [21.6%] | +1.12 [+0.66] | 47.4% / +1.07 | 48.9% / +1.34 |
| d_atr_pct rose on the session before the pick and on the signal day | 968 | 51.3% [49.2%] | 23.2% [21.5%] | +1.28 [+0.86] | 50.6% / +1.37 | 51.9% / +1.49 |
| d_dist_from_20h in its low third at the signal close (<= -3.52374) | 1292 | 48.7% [46.6%] | 23.2% [21.5%] | +1.17 [+0.71] | 47.8% / +1.16 | 49.5% / +1.36 |
| d_realvol_20 in its upper half at the signal close (> 42.8542) | 1938 | 47.9% [46.3%] | 22.7% [21.5%] | +0.94 [+0.61] | 47.5% / +0.97 | 48.9% / +1.16 |
| d_n_5pct_up_60 in its high third at the signal close (> 4) | 1208 | 49.4% [47.7%] | 22.8% [21.5%] | +0.92 [+0.60] | 49.0% / +0.91 | 50.8% / +1.09 |
| d_bb_bw_20 in its upper half at the signal close (> 0.203649) | 1938 | 47.8% [46.2%] | 22.7% [21.4%] | +1.04 [+0.70] | 47.1% / +1.07 | 48.9% / +1.22 |

## The model's own pairs (the WHY study's interactions): the best pair of their conditions

| features | best pair (by the no-dip lower bound) | trades | no dip [lower bound] | runners | net [lower bound] |
|---|---|---:|---:|---:|---:|
| d_donch_pos_50_rmean50 x d_bb_bw_20 | d_bb_bw_20 in its low third at the signal close (<= 0.139628) & d_donch_pos_50_rmean50 in its lower half at the signal close (<= 0.67066) | 3364 | 67.4% [65.3%] | 14.1% | +0.58 [+0.31] |
| d_vol_yz_50 x d_n_5pct_up_252 | d_n_5pct_up_252 in its low third at the signal close (<= 9) & d_vol_yz_50 in its low third at the signal close (<= 0.0290626) | 6279 | 67.7% [65.9%] | 10.5% | +0.21 [+0.04] |
| d_ema20_angle_deg x w_ret_13w | d_ema20_angle_deg in its upper half at the signal close (> 0.0164276) & w_ret_13w in its lower half at the signal close (<= 16.4325) | 4504 | 64.1% [62.1%] | 15.4% | +0.64 [+0.37] |
| d_ema20_angle_deg x d_bb_bw_20 | d_bb_bw_20 in its low third at the signal close (<= 0.139628) & d_ema20_angle_deg rose on the signal day | 3675 | 66.1% [64.2%] | 15.7% | +0.78 [+0.55] |
| d_ema20_angle_deg x d_vol_yz_50 | d_ema20_angle_deg in its upper half at the signal close (> 0.0164276) & d_vol_yz_50 in its low third at the signal close (<= 0.0290626) | 4894 | 68.5% [66.7%] | 12.1% | +0.47 [+0.30] |
| d_vol_yz_50 x d_dist_from_52wl | d_dist_from_52wl in its high third at the signal close (> 13.4956) & d_vol_yz_50 in its low third at the signal close (<= 0.0290626) | 3928 | 69.3% [67.3%] | 12.1% | +0.47 [+0.27] |
| d_n_5pct_up_252 x d_bb_bw_20 | d_bb_bw_20 in its low third at the signal close (<= 0.139628) & d_n_5pct_up_252 in its low third at the signal close (<= 9) | 5235 | 70.8% [69.0%] | 10.0% | +0.22 [+0.05] |
| d_vol_yz_50 x w_ret_13w | d_vol_yz_50 in its low third at the signal close (<= 0.0290626) & w_ret_13w rose on the session before the pick | 742 | 67.4% [62.8%] | 10.6% | +0.39 [-0.05] |
| d_vol_yz_50 x d_wq_16 | d_vol_yz_50 in its low third at the signal close (<= 0.0290626) & d_wq_16 in its low third at the signal close (<= -0.380422) | 3637 | 68.8% [66.8%] | 11.1% | +0.26 [+0.06] |
| d_ema20_angle_deg x d_wq_29 | d_wq_29 in its lower half at the signal close (<= 0.665899) & d_ema20_angle_deg turned up (fell the session before the pick, rose on the signal day) | 2845 | 59.5% [57.2%] | 19.0% | +0.96 [+0.59] |
| d_ema20_angle_deg x d_dist_from_52wl | d_dist_from_52wl in its high third at the signal close (> 13.4956) & d_ema20_angle_deg rose on the signal day | 3301 | 59.5% [57.5%] | 18.7% | +0.80 [+0.50] |
| d_donch_pos_50_rmean50 x d_dist_from_52wl | d_dist_from_52wl in its high third at the signal close (> 13.4956) & d_donch_pos_50_rmean50 in its lower half at the signal close (<= 0.67066) | 2023 | 61.5% [59.1%] | 16.4% | +0.66 [+0.32] |
| d_dist_from_52wl x d_wq_16 | d_dist_from_52wl in its high third at the signal close (> 13.4956) & d_wq_16 in its low third at the signal close (<= -0.380422) | 3413 | 60.4% [58.3%] | 14.6% | +0.44 [+0.17] |
| d_ema20_angle_deg x d_adx14 | d_adx14 in its low third at the signal close (<= 25.0636) & d_ema20_angle_deg in its upper half at the signal close (> 0.0164276) | 4793 | 60.4% [58.3%] | 16.3% | +0.62 [+0.36] |

## Entries: the D1 open against the events, on the same picks

| picks of | engine | entry | filled | per trade [95%] | against the D1 open [95%] | no dip | runners |
|---|---|---|---:|---:|---:|---:|---:|
| ALL picks | D | D1 open (the model's own buy; AMO / pre-open) | 15818 of 15818 | +0.85 [+0.39, +1.31] | +0.00 [+0.00, +0.00] | 53.6% | 19.8% |
| ALL picks | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 8846 of 15818 | +0.93 [+0.50, +1.39] | -1.98 [-2.12, -1.85] | 71.0% | 29.1% |
| ALL picks | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 3756 of 15818 | +0.20 [-0.28, +0.69] | -4.81 [-5.09, -4.55] | 86.8% | 42.6% |
| ALL picks | D | D1 close after a strong D1 (at the screen about 15:20) | 3756 of 15818 | +1.08 [+0.54, +1.62] | -3.94 [-4.16, -3.73] | 86.8% | 42.6% |
| no-dip arm, out of sample | D | D1 open (the model's own buy; AMO / pre-open) | 669 of 669 | +0.54 [-0.05, +1.10] | +0.00 [+0.00, +0.00] | 71.3% | 13.0% |
| no-dip arm, out of sample | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 412 of 669 | +0.61 [+0.03, +1.19] | -1.16 [-1.56, -0.88] | 82.3% | 17.5% |
| no-dip arm, out of sample | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 173 of 669 | +0.26 [-0.54, +1.01] | -2.84 [-3.53, -2.26] | 91.3% | 30.6% |
| no-dip arm, out of sample | D | D1 close after a strong D1 (at the screen about 15:20) | 173 of 669 | +0.65 [-0.15, +1.39] | -2.46 [-3.14, -1.94] | 91.3% | 30.6% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | D | D1 open (the model's own buy; AMO / pre-open) | 122 of 122 | +0.88 [+0.19, +1.72] | +0.00 [+0.00, +0.00] | 82.8% | 11.5% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 55 of 122 | +0.35 [-0.62, +1.63] | -1.35 [-1.78, -1.04] | 92.7% | 18.2% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 26 of 122 | +0.52 [-0.52, +1.85] | -1.52 [-2.01, -1.08] | 88.5% | 23.1% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | D | D1 close after a strong D1 (at the screen about 15:20) | 26 of 122 | +0.73 [-0.34, +2.14] | -1.31 [-1.57, -1.07] | 88.5% | 23.1% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | D | D1 open (the model's own buy; AMO / pre-open) | 426 of 426 | +0.23 [-0.19, +0.69] | +0.00 [+0.00, +0.00] | 75.6% | 8.2% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 192 of 426 | +0.19 [-0.27, +0.73] | -1.26 [-1.38, -1.15] | 91.7% | 13.5% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 107 of 426 | -0.20 [-0.89, +0.52] | -2.17 [-2.50, -1.85] | 92.5% | 18.7% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | D | D1 close after a strong D1 (at the screen about 15:20) | 107 of 426 | +0.05 [-0.68, +0.79] | -1.92 [-2.20, -1.65] | 92.5% | 18.7% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | D | D1 open (the model's own buy; AMO / pre-open) | 387 of 387 | +0.39 [-0.01, +0.80] | +0.00 [+0.00, +0.00] | 79.3% | 7.0% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 199 of 387 | +0.22 [-0.19, +0.61] | -1.16 [-1.28, -1.05] | 93.0% | 11.1% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 115 of 387 | -0.15 [-0.75, +0.56] | -1.68 [-1.94, -1.45] | 90.4% | 12.2% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | D | D1 close after a strong D1 (at the screen about 15:20) | 115 of 387 | +0.06 [-0.54, +0.76] | -1.47 [-1.72, -1.27] | 90.4% | 12.2% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | D | D1 open (the model's own buy; AMO / pre-open) | 156 of 156 | +1.44 [+0.24, +3.01] | +0.00 [+0.00, +0.00] | 80.1% | 13.5% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 100 of 156 | +2.00 [+0.50, +4.09] | -0.78 [-1.08, -0.58] | 87.0% | 19.0% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 36 of 156 | +1.58 [-0.08, +3.78] | -2.04 [-2.98, -1.40] | 97.2% | 25.0% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | D | D1 close after a strong D1 (at the screen about 15:20) | 36 of 156 | +2.20 [+0.35, +4.70] | -1.42 [-1.93, -1.04] | 97.2% | 25.0% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | D | D1 open (the model's own buy; AMO / pre-open) | 210 of 210 | +0.54 [+0.07, +1.04] | +0.00 [+0.00, +0.00] | 79.0% | 8.6% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 106 of 210 | +0.44 [-0.19, +1.08] | -1.33 [-1.47, -1.20] | 92.5% | 13.2% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 61 of 210 | -0.07 [-0.88, +0.81] | -2.02 [-2.46, -1.62] | 95.1% | 16.4% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | D | D1 close after a strong D1 (at the screen about 15:20) | 61 of 210 | +0.27 [-0.57, +1.15] | -1.68 [-2.11, -1.29] | 95.1% | 16.4% |
| runner arm, out of sample | D | D1 open (the model's own buy; AMO / pre-open) | 506 of 506 | +0.78 [-0.70, +2.47] | +0.00 [+0.00, +0.00] | 48.2% | 23.5% |
| runner arm, out of sample | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 177 of 506 | +0.01 [-1.75, +1.91] | -5.66 [-6.71, -4.71] | 75.7% | 39.0% |
| runner arm, out of sample | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 123 of 506 | -0.82 [-2.77, +1.34] | -7.10 [-8.26, -6.07] | 82.1% | 48.8% |
| runner arm, out of sample | D | D1 close after a strong D1 (at the screen about 15:20) | 123 of 506 | +0.04 [-2.05, +2.42] | -6.24 [-7.16, -5.43] | 82.1% | 48.8% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | D | D1 open (the model's own buy; AMO / pre-open) | 144 of 144 | +3.73 [+1.03, +6.60] | +0.00 [+0.00, +0.00] | 62.5% | 42.4% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 64 of 144 | +2.57 [-0.98, +6.26] | -7.45 [-8.32, -6.62] | 90.6% | 64.1% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 52 of 144 | +1.35 [-2.14, +4.73] | -8.25 [-9.96, -6.76] | 90.4% | 69.2% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | D | D1 close after a strong D1 (at the screen about 15:20) | 52 of 144 | +2.06 [-1.45, +5.72] | -7.54 [-8.72, -6.57] | 90.4% | 69.2% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | D | D1 open (the model's own buy; AMO / pre-open) | 130 of 130 | +3.73 [+1.25, +6.57] | +0.00 [+0.00, +0.00] | 60.0% | 40.0% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 51 of 130 | +2.61 [-0.60, +6.66] | -7.83 [-8.88, -6.81] | 94.1% | 62.7% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 42 of 130 | +1.59 [-1.45, +5.64] | -8.57 [-10.17, -7.36] | 92.9% | 69.0% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | D | D1 close after a strong D1 (at the screen about 15:20) | 42 of 130 | +2.75 [-0.41, +6.99] | -7.41 [-8.79, -6.37] | 92.9% | 69.0% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | D | D1 open (the model's own buy; AMO / pre-open) | 164 of 164 | +4.27 [+2.13, +6.57] | +0.00 [+0.00, +0.00] | 59.1% | 37.8% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 60 of 164 | +2.22 [-0.80, +5.61] | -8.16 [-9.05, -7.31] | 93.3% | 61.7% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 51 of 164 | +1.49 [-1.96, +4.86] | -7.68 [-9.38, -6.31] | 96.1% | 64.7% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | D | D1 close after a strong D1 (at the screen about 15:20) | 51 of 164 | +2.07 [-1.30, +5.53] | -7.10 [-8.33, -6.13] | 96.1% | 64.7% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | D | D1 open (the model's own buy; AMO / pre-open) | 136 of 136 | +2.24 [-0.11, +4.36] | +0.00 [+0.00, +0.00] | 57.4% | 36.8% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 115 of 136 | +2.78 [+0.62, +4.76] | -0.74 [-1.02, -0.51] | 66.1% | 42.6% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 47 of 136 | +1.30 [-1.31, +3.46] | -5.14 [-6.31, -4.12] | 78.7% | 57.4% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | D | D1 close after a strong D1 (at the screen about 15:20) | 47 of 136 | +3.24 [+0.57, +5.66] | -3.21 [-4.21, -2.48] | 78.7% | 57.4% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | D | D1 open (the model's own buy; AMO / pre-open) | 121 of 121 | +3.24 [+1.34, +5.27] | +0.00 [+0.00, +0.00] | 60.3% | 35.5% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 37 of 121 | +1.37 [-1.71, +4.60] | -8.07 [-9.04, -6.93] | 94.6% | 67.6% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 42 of 121 | +1.46 [-1.56, +5.08] | -6.51 [-7.78, -5.11] | 90.5% | 66.7% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | D | D1 close after a strong D1 (at the screen about 15:20) | 42 of 121 | +1.92 [-0.97, +5.24] | -6.06 [-7.00, -5.06] | 90.5% | 66.7% |
| money arm, out of sample | D | D1 open (the model's own buy; AMO / pre-open) | 655 of 655 | +1.29 [-0.39, +2.77] | +0.00 [+0.00, +0.00] | 49.2% | 21.7% |
| money arm, out of sample | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 358 of 655 | +1.17 [-0.71, +2.97] | -2.25 [-2.60, -1.93] | 69.8% | 33.2% |
| money arm, out of sample | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 160 of 655 | +0.69 [-1.20, +2.42] | -5.74 [-6.43, -4.88] | 90.6% | 48.1% |
| money arm, out of sample | D | D1 close after a strong D1 (at the screen about 15:20) | 160 of 655 | +1.75 [-0.18, +3.58] | -4.67 [-5.23, -4.00] | 90.6% | 48.1% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | D | D1 open (the model's own buy; AMO / pre-open) | 147 of 147 | +5.05 [+2.37, +7.56] | +0.00 [+0.00, +0.00] | 57.1% | 33.3% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 66 of 147 | +3.73 [+0.13, +7.08] | -5.22 [-6.41, -4.09] | 81.8% | 53.0% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 56 of 147 | +1.21 [-1.19, +3.35] | -7.06 [-8.26, -5.54] | 91.1% | 58.9% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | D | D1 close after a strong D1 (at the screen about 15:20) | 56 of 147 | +2.15 [-0.53, +4.56] | -6.12 [-7.32, -4.66] | 91.1% | 58.9% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D1 open (the model's own buy; AMO / pre-open) | 196 of 196 | +4.98 [+2.23, +7.24] | +0.00 [+0.00, +0.00] | 58.7% | 32.1% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 109 of 196 | +3.43 [+0.76, +5.92] | -3.83 [-4.56, -3.07] | 78.0% | 45.9% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 196 | +1.28 [-0.62, +2.81] | -6.35 [-7.44, -5.21] | 94.1% | 54.4% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | D | D1 close after a strong D1 (at the screen about 15:20) | 68 of 196 | +2.32 [+0.30, +3.97] | -5.31 [-6.32, -4.28] | 94.1% | 54.4% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | D | D1 open (the model's own buy; AMO / pre-open) | 212 of 212 | +5.21 [+2.33, +7.62] | +0.00 [+0.00, +0.00] | 56.6% | 30.7% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 112 of 212 | +4.20 [+0.92, +7.21] | -3.40 [-4.02, -2.81] | 75.0% | 43.8% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 67 of 212 | +2.07 [+0.23, +3.48] | -6.24 [-7.15, -4.89] | 94.0% | 58.2% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | D | D1 close after a strong D1 (at the screen about 15:20) | 67 of 212 | +2.95 [+0.82, +4.64] | -5.35 [-6.18, -4.11] | 94.0% | 58.2% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | D | D1 open (the model's own buy; AMO / pre-open) | 268 of 268 | +4.59 [+2.21, +6.86] | +0.00 [+0.00, +0.00] | 63.1% | 34.7% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 204 of 268 | +4.17 [+1.86, +6.50] | -1.69 [-2.00, -1.39] | 74.0% | 42.2% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 70 of 268 | +3.92 [+1.02, +6.78] | -6.36 [-7.75, -4.87] | 90.0% | 67.1% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | D | D1 close after a strong D1 (at the screen about 15:20) | 70 of 268 | +5.61 [+2.42, +8.90] | -4.67 [-5.53, -3.69] | 90.0% | 67.1% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | D | D1 open (the model's own buy; AMO / pre-open) | 147 of 147 | +4.54 [+1.68, +7.77] | +0.00 [+0.00, +0.00] | 55.8% | 26.5% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | D | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 87 of 147 | +4.54 [+1.26, +8.62] | -2.80 [-3.41, -2.33] | 75.9% | 37.9% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | D | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 35 of 147 | +1.87 [-1.77, +6.25] | -7.66 [-10.46, -5.34] | 85.7% | 60.0% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | D | D1 close after a strong D1 (at the screen about 15:20) | 35 of 147 | +3.60 [-0.49, +8.81] | -5.93 [-8.05, -4.06] | 85.7% | 60.0% |
| ALL picks | ENS | D1 open (the model's own buy; AMO / pre-open) | 16256 of 16256 | +0.90 [+0.43, +1.34] | +0.00 [+0.00, +0.00] | 54.9% | 20.1% |
| ALL picks | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 9140 of 16256 | +0.84 [+0.41, +1.27] | -1.94 [-2.07, -1.81] | 71.6% | 28.9% |
| ALL picks | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 3919 of 16256 | +0.05 [-0.42, +0.50] | -4.54 [-4.80, -4.31] | 84.8% | 39.9% |
| ALL picks | ENS | D1 close after a strong D1 (at the screen about 15:20) | 3919 of 16256 | +0.81 [+0.28, +1.32] | -3.78 [-3.98, -3.59] | 84.8% | 39.9% |
| no-dip arm, out of sample | ENS | D1 open (the model's own buy; AMO / pre-open) | 768 of 768 | +0.73 [+0.10, +1.36] | +0.00 [+0.00, +0.00] | 68.6% | 13.4% |
| no-dip arm, out of sample | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 480 of 768 | +0.64 [-0.21, +1.48] | -1.17 [-1.44, -0.95] | 79.4% | 17.7% |
| no-dip arm, out of sample | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 199 of 768 | -0.21 [-1.11, +0.65] | -2.83 [-3.28, -2.40] | 91.0% | 21.6% |
| no-dip arm, out of sample | ENS | D1 close after a strong D1 (at the screen about 15:20) | 199 of 768 | +0.13 [-0.77, +1.00] | -2.49 [-2.88, -2.14] | 91.0% | 21.6% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | ENS | D1 open (the model's own buy; AMO / pre-open) | 128 of 128 | +0.53 [-0.15, +1.27] | +0.00 [+0.00, +0.00] | 78.1% | 8.6% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 63 of 128 | -0.12 [-1.05, +0.85] | -1.46 [-1.90, -1.13] | 93.7% | 15.9% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 32 of 128 | -0.25 [-0.93, +0.41] | -1.94 [-2.74, -1.27] | 93.8% | 12.5% |
| N1: V|d_donch_pos_50_rmean50:H3 & V|w_ret_13w:LO & G|dn0 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 32 of 128 | -0.21 [-0.91, +0.47] | -1.90 [-2.59, -1.32] | 93.8% | 12.5% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | ENS | D1 open (the model's own buy; AMO / pre-open) | 409 of 409 | +0.41 [-0.01, +0.81] | +0.00 [+0.00, +0.00] | 77.3% | 8.8% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 213 of 409 | +0.23 [-0.32, +0.79] | -1.27 [-1.36, -1.19] | 89.2% | 12.7% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 109 of 409 | -0.45 [-1.04, +0.11] | -1.91 [-2.22, -1.63] | 92.7% | 11.9% |
| N2: Z|ATRP:0:1 & C|BULLSTATE & G|dn0 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 109 of 409 | -0.31 [-0.90, +0.27] | -1.77 [-2.06, -1.50] | 92.7% | 11.9% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | ENS | D1 open (the model's own buy; AMO / pre-open) | 326 of 326 | +0.26 [-0.22, +0.73] | +0.00 [+0.00, +0.00] | 75.2% | 8.6% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 164 of 326 | -0.07 [-0.55, +0.43] | -1.28 [-1.41, -1.16] | 88.4% | 12.2% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 80 of 326 | -0.64 [-1.23, -0.12] | -1.71 [-2.06, -1.42] | 88.8% | 10.0% |
| N3: V|d_slope_stability:H3 & Z|ATRP:0:1 & G|dn0 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 80 of 326 | -0.55 [-1.17, -0.01] | -1.62 [-1.91, -1.36] | 88.8% | 10.0% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 94 of 94 | +0.88 [-0.13, +2.09] | +0.00 [+0.00, +0.00] | 74.5% | 14.9% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 64 of 94 | +0.57 [-0.57, +2.05] | -0.99 [-1.48, -0.68] | 81.2% | 15.6% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 20 of 94 | +0.10 [-2.13, +2.75] | -3.78 [-6.89, -1.98] | 90.0% | 25.0% |
| N4: V|w_ret_13w:LO & V|x_z_d_downside_dev_60:L3 & P|rank1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 20 of 94 | +0.72 [-1.70, +3.40] | -3.16 [-5.52, -1.63] | 90.0% | 25.0% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | ENS | D1 open (the model's own buy; AMO / pre-open) | 312 of 312 | +0.70 [+0.10, +1.35] | +0.00 [+0.00, +0.00] | 76.0% | 10.3% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 171 of 312 | +0.37 [-0.49, +1.35] | -1.35 [-1.46, -1.24] | 85.4% | 14.6% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 77 of 312 | -0.11 [-0.87, +0.60] | -1.96 [-2.36, -1.61] | 94.8% | 20.8% |
| N5: B|d_adx14:dndn & Z|ATRP:1:1 & G|dn0 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 77 of 312 | +0.08 [-0.69, +0.78] | -1.77 [-2.13, -1.44] | 94.8% | 20.8% |
| runner arm, out of sample | ENS | D1 open (the model's own buy; AMO / pre-open) | 538 of 538 | +1.20 [-0.42, +2.97] | +0.00 [+0.00, +0.00] | 51.9% | 25.8% |
| runner arm, out of sample | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 188 of 538 | +1.24 [-0.37, +3.02] | -5.24 [-6.57, -4.25] | 80.3% | 42.6% |
| runner arm, out of sample | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 143 of 538 | -0.17 [-2.10, +1.97] | -6.98 [-8.04, -6.03] | 83.2% | 51.0% |
| runner arm, out of sample | ENS | D1 close after a strong D1 (at the screen about 15:20) | 143 of 538 | +0.75 [-1.28, +3.14] | -6.06 [-6.90, -5.27] | 83.2% | 51.0% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 151 of 151 | +4.95 [+2.51, +7.68] | +0.00 [+0.00, +0.00] | 66.2% | 45.0% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 62 of 151 | +3.92 [+0.20, +7.89] | -7.14 [-8.02, -6.34] | 90.3% | 66.1% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 53 of 151 | +2.80 [-0.22, +5.76] | -8.31 [-10.09, -6.70] | 90.6% | 71.7% |
| U1: B|w_ret_13w:dn0 & C|BEARSTATE & G|dn1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 53 of 151 | +3.66 [+0.36, +7.05] | -7.45 [-8.69, -6.36] | 90.6% | 71.7% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 149 of 149 | +4.12 [+1.84, +6.80] | +0.00 [+0.00, +0.00] | 65.1% | 43.0% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 52 of 149 | +2.71 [-0.45, +6.69] | -7.74 [-8.77, -6.74] | 92.3% | 65.4% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 48 of 149 | +1.95 [-0.97, +5.29] | -7.91 [-9.53, -6.58] | 91.7% | 70.8% |
| U2: V|d_ll_run:H3 & W|1 & G|dn1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 48 of 149 | +2.97 [+0.01, +6.54] | -6.88 [-8.21, -5.87] | 91.7% | 70.8% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 161 of 161 | +4.46 [+2.35, +6.80] | +0.00 [+0.00, +0.00] | 61.5% | 41.6% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 49 of 161 | +2.70 [-0.62, +6.44] | -8.22 [-9.33, -7.12] | 89.8% | 65.3% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 45 of 161 | +2.76 [-0.04, +5.79] | -8.08 [-10.07, -6.43] | 97.8% | 73.3% |
| U3: W|1 & C|VOL_ELEV & G|dn1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 45 of 161 | +3.50 [+0.67, +6.85] | -7.34 [-8.82, -6.12] | 97.8% | 73.3% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 102 of 102 | +4.67 [+1.73, +7.32] | +0.00 [+0.00, +0.00] | 67.6% | 46.1% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 91 of 102 | +4.85 [+1.97, +7.53] | -0.66 [-0.93, -0.42] | 72.5% | 49.5% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 45 of 102 | +1.48 [-1.75, +4.43] | -5.16 [-6.10, -4.37] | 86.7% | 53.3% |
| U4: V|d_mdi14:HI & X|bigup & W|1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 45 of 102 | +3.27 [-0.16, +6.44] | -3.37 [-4.10, -2.70] | 86.7% | 53.3% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | ENS | D1 open (the model's own buy; AMO / pre-open) | 130 of 130 | +3.30 [+1.34, +5.17] | +0.00 [+0.00, +0.00] | 65.4% | 40.0% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 39 of 130 | +2.20 [-0.54, +5.13] | -7.07 [-8.16, -6.06] | 94.9% | 66.7% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 40 of 130 | +0.85 [-1.97, +3.58] | -6.46 [-7.65, -5.19] | 82.5% | 62.5% |
| U5: V|d_wq_26:HI & W|1 & G|dn1 | ENS | D1 close after a strong D1 (at the screen about 15:20) | 40 of 130 | +1.68 [-1.15, +4.39] | -5.63 [-6.51, -4.69] | 82.5% | 62.5% |
| money arm, out of sample | ENS | D1 open (the model's own buy; AMO / pre-open) | 591 of 591 | +1.39 [-0.42, +2.97] | +0.00 [+0.00, +0.00] | 49.9% | 23.5% |
| money arm, out of sample | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 322 of 591 | +1.19 [-0.93, +3.12] | -2.30 [-2.61, -2.03] | 70.5% | 33.9% |
| money arm, out of sample | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 141 of 591 | +0.90 [-1.34, +2.87] | -5.32 [-5.95, -4.60] | 89.4% | 51.1% |
| money arm, out of sample | ENS | D1 close after a strong D1 (at the screen about 15:20) | 141 of 591 | +1.76 [-0.51, +3.89] | -4.46 [-5.05, -3.82] | 89.4% | 51.1% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | ENS | D1 open (the model's own buy; AMO / pre-open) | 161 of 161 | +5.34 [+2.32, +8.23] | +0.00 [+0.00, +0.00] | 57.1% | 34.8% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 67 of 161 | +4.80 [+0.85, +8.43] | -5.36 [-6.51, -4.25] | 88.1% | 59.7% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 65 of 161 | +1.60 [-0.81, +3.74] | -6.98 [-8.49, -5.36] | 92.3% | 60.0% |
| M1: B|d_atr_pct:upup & Z|IDX:1:1 & C|NIFTY_UP | ENS | D1 close after a strong D1 (at the screen about 15:20) | 65 of 161 | +2.52 [-0.07, +4.94] | -6.06 [-7.34, -4.74] | 92.3% | 60.0% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D1 open (the model's own buy; AMO / pre-open) | 196 of 196 | +4.98 [+2.23, +7.24] | +0.00 [+0.00, +0.00] | 58.7% | 32.1% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 109 of 196 | +3.43 [+0.76, +5.92] | -3.83 [-4.56, -3.07] | 78.0% | 45.9% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 196 | +1.28 [-0.62, +2.81] | -6.35 [-7.44, -5.21] | 94.1% | 54.4% |
| M2: Z|IDX:1:1 & P|agree & C|BEARSTATE | ENS | D1 close after a strong D1 (at the screen about 15:20) | 68 of 196 | +2.32 [+0.30, +3.97] | -5.31 [-6.32, -4.28] | 94.1% | 54.4% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | ENS | D1 open (the model's own buy; AMO / pre-open) | 204 of 204 | +5.11 [+1.92, +8.03] | +0.00 [+0.00, +0.00] | 56.9% | 28.9% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 105 of 204 | +3.51 [-0.03, +6.98] | -3.64 [-4.27, -2.97] | 75.2% | 41.0% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 68 of 204 | +1.41 [-0.90, +3.30] | -6.15 [-7.61, -4.40] | 91.2% | 50.0% |
| M3: Z|IDX:0:1 & C|BEARSTATE & C|NIFTY_UP | ENS | D1 close after a strong D1 (at the screen about 15:20) | 68 of 204 | +2.28 [-0.27, +4.57] | -5.29 [-6.48, -3.95] | 91.2% | 50.0% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D1 open (the model's own buy; AMO / pre-open) | 253 of 253 | +4.01 [+1.52, +6.37] | +0.00 [+0.00, +0.00] | 63.6% | 34.4% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 185 of 253 | +3.78 [+0.96, +6.48] | -1.49 [-1.87, -1.17] | 74.1% | 42.7% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 70 of 253 | +2.48 [-0.89, +5.66] | -5.82 [-6.96, -4.35] | 88.6% | 65.7% |
| M4: B|d_upside_vol_ratio:upup & Z|VIX5:0:0 & C|VIX_HIGH | ENS | D1 close after a strong D1 (at the screen about 15:20) | 70 of 253 | +3.80 [+0.14, +7.30] | -4.50 [-5.39, -3.37] | 88.6% | 65.7% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | ENS | D1 open (the model's own buy; AMO / pre-open) | 145 of 145 | +3.54 [+1.11, +6.28] | +0.00 [+0.00, +0.00] | 60.7% | 31.0% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | ENS | breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT) | 87 of 145 | +2.79 [-0.06, +6.21] | -2.82 [-3.37, -2.31] | 80.5% | 43.7% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | ENS | D2 open after a strong D1 (green, close in the top 30% of its range; AMO) | 42 of 145 | +1.51 [-0.85, +4.00] | -5.70 [-6.99, -4.62] | 88.1% | 57.1% |
| M5: V|d_atr_pct:HI & V|d_realvol_20:L3 & C|VIX_HIGH | ENS | D1 close after a strong D1 (at the screen about 15:20) | 42 of 145 | +3.34 [+0.92, +5.93] | -3.86 [-4.83, -3.08] | 88.1% | 57.1% |

## Money in full (Rs 5 L from 2022; one position per pick; worst fall counted on closed trades)

Dip arm: ZONES_20261108_001: 21538 setup trades, 7403 of them IN their picks zone (S3 and its zone were chosen on these years: in-sample).

| engine | book | slots | MTF | Rs 5 L became | a year | worst fall | trades a week | skipped |
|---|---|---:|---|---:|---:|---:|---:|---:|
| D | baseline: ranks 1-3 at the D1 open | 2 | none | Rs 4,550,811 | +59.7% | 46.5% | 1.9 | 2793 |
| D | baseline: ranks 1-3 at the D1 open | 2 | 2x | Rs 8,877,182 | +84.0% | 75.6% | 1.9 | 2793 |
| D | baseline: ranks 1-3 at the D1 open | 3 | none | Rs 4,820,133 | +61.7% | 54.7% | 2.8 | 2561 |
| D | baseline: ranks 1-3 at the D1 open | 3 | 2x | Rs 10,673,077 | +91.3% | 83.0% | 2.8 | 2561 |
| D | baseline: ranks 1-3 at the D1 open | 5 | none | Rs 3,500,126 | +51.1% | 44.2% | 4.7 | 2098 |
| D | baseline: ranks 1-3 at the D1 open | 5 | 2x | Rs 7,906,770 | +79.5% | 72.3% | 4.7 | 2098 |
| D | baseline: ranks 1-3 at the D1 open | 7 | none | Rs 4,249,148 | +57.4% | 40.4% | 6.6 | 1642 |
| D | baseline: ranks 1-3 at the D1 open | 7 | 2x | Rs 12,608,602 | +98.2% | 67.9% | 6.6 | 1642 |
| D | no-dip arm, out of sample | 2 | none | Rs 1,026,032 | +16.5% | 32.6% | 0.9 | 452 |
| D | no-dip arm, out of sample | 2 | 2x | Rs 1,255,798 | +21.6% | 58.6% | 0.9 | 452 |
| D | no-dip arm, out of sample | 3 | none | Rs 868,861 | +12.4% | 26.0% | 1.2 | 371 |
| D | no-dip arm, out of sample | 3 | 2x | Rs 1,008,279 | +16.0% | 48.4% | 1.2 | 371 |
| D | no-dip arm, out of sample | 5 | none | Rs 730,989 | +8.4% | 19.0% | 1.7 | 246 |
| D | no-dip arm, out of sample | 5 | 2x | Rs 806,761 | +10.7% | 36.1% | 1.7 | 246 |
| D | no-dip arm, out of sample | 7 | none | Rs 766,406 | +9.5% | 15.3% | 2.1 | 152 |
| D | no-dip arm, out of sample | 7 | 2x | Rs 932,302 | +14.1% | 29.8% | 2.1 | 152 |
| D | no-dip arm, in-sample (N1-N5) | 2 | none | Rs 682,249 | +6.8% | 17.3% | 0.7 | 468 |
| D | no-dip arm, in-sample (N1-N5) | 2 | 2x | Rs 704,319 | +7.5% | 35.7% | 0.7 | 468 |
| D | no-dip arm, in-sample (N1-N5) | 3 | none | Rs 717,399 | +8.0% | 12.6% | 0.9 | 413 |
| D | no-dip arm, in-sample (N1-N5) | 3 | 2x | Rs 829,941 | +11.3% | 27.0% | 0.9 | 413 |
| D | no-dip arm, in-sample (N1-N5) | 5 | none | Rs 705,841 | +7.6% | 8.7% | 1.3 | 324 |
| D | no-dip arm, in-sample (N1-N5) | 5 | 2x | Rs 839,254 | +11.6% | 19.4% | 1.3 | 324 |
| D | no-dip arm, in-sample (N1-N5) | 7 | none | Rs 685,897 | +6.9% | 7.3% | 1.5 | 259 |
| D | no-dip arm, in-sample (N1-N5) | 7 | 2x | Rs 816,491 | +11.0% | 16.5% | 1.5 | 259 |
| D | no-dip arm, out of sample + S3 in its zone | 2 | none | Rs 3,330,906 | +49.5% | 31.3% | 1.1 | 616 |
| D | no-dip arm, out of sample + S3 in its zone | 2 | 2x | Rs 10,562,066 | +90.9% | 56.2% | 1.1 | 616 |
| D | no-dip arm, out of sample + S3 in its zone | 3 | none | Rs 1,979,516 | +33.9% | 28.3% | 1.6 | 508 |
| D | no-dip arm, out of sample + S3 in its zone | 3 | 2x | Rs 4,396,956 | +58.5% | 51.0% | 1.6 | 508 |
| D | no-dip arm, out of sample + S3 in its zone | 5 | none | Rs 1,620,217 | +28.3% | 16.0% | 2.2 | 345 |
| D | no-dip arm, out of sample + S3 in its zone | 5 | 2x | Rs 3,552,991 | +51.5% | 30.6% | 2.2 | 345 |
| D | no-dip arm, out of sample + S3 in its zone | 7 | none | Rs 1,378,347 | +24.0% | 12.3% | 2.7 | 226 |
| D | no-dip arm, out of sample + S3 in its zone | 7 | 2x | Rs 2,791,936 | +44.0% | 24.5% | 2.7 | 226 |
| D | runner arm, out of sample | 2 | none | Rs 785,172 | +10.0% | 41.7% | 0.8 | 302 |
| D | runner arm, out of sample | 2 | 2x | Rs 436,700 | -2.8% | 70.9% | 0.8 | 302 |
| D | runner arm, out of sample | 3 | none | Rs 1,111,114 | +18.4% | 31.8% | 1.1 | 243 |
| D | runner arm, out of sample | 3 | 2x | Rs 1,187,133 | +20.1% | 57.1% | 1.1 | 243 |
| D | runner arm, out of sample | 5 | none | Rs 813,206 | +10.9% | 29.1% | 1.4 | 164 |
| D | runner arm, out of sample | 5 | 2x | Rs 793,931 | +10.3% | 55.3% | 1.4 | 164 |
| D | runner arm, out of sample | 7 | none | Rs 788,578 | +10.1% | 21.9% | 1.6 | 114 |
| D | runner arm, out of sample | 7 | 2x | Rs 858,722 | +12.1% | 41.7% | 1.6 | 114 |
| D | runner arm, in-sample (U1-U5) | 2 | none | Rs 1,739,231 | +30.2% | 27.7% | 0.7 | 105 |
| D | runner arm, in-sample (U1-U5) | 2 | 2x | Rs 2,945,883 | +45.6% | 58.6% | 0.7 | 105 |
| D | runner arm, in-sample (U1-U5) | 3 | none | Rs 1,830,475 | +31.7% | 25.2% | 0.8 | 71 |
| D | runner arm, in-sample (U1-U5) | 3 | 2x | Rs 4,056,611 | +55.9% | 53.4% | 0.8 | 71 |
| D | runner arm, in-sample (U1-U5) | 5 | none | Rs 1,406,448 | +24.5% | 16.0% | 0.9 | 38 |
| D | runner arm, in-sample (U1-U5) | 5 | 2x | Rs 3,007,032 | +46.3% | 31.0% | 0.9 | 38 |
| D | runner arm, in-sample (U1-U5) | 7 | none | Rs 1,209,162 | +20.6% | 14.3% | 1.0 | 17 |
| D | runner arm, in-sample (U1-U5) | 7 | 2x | Rs 2,403,581 | +39.5% | 28.0% | 1.0 | 17 |
| D | runner arm, out of sample + S3 in its zone | 2 | none | Rs 1,113,838 | +18.5% | 41.7% | 0.9 | 483 |
| D | runner arm, out of sample + S3 in its zone | 2 | 2x | Rs 814,279 | +10.9% | 71.5% | 0.9 | 483 |
| D | runner arm, out of sample + S3 in its zone | 3 | none | Rs 1,611,724 | +28.2% | 31.8% | 1.3 | 404 |
| D | runner arm, out of sample + S3 in its zone | 3 | 2x | Rs 2,297,524 | +38.2% | 62.4% | 1.3 | 404 |
| D | runner arm, out of sample + S3 in its zone | 5 | none | Rs 1,125,215 | +18.8% | 32.4% | 1.7 | 297 |
| D | runner arm, out of sample + S3 in its zone | 5 | 2x | Rs 1,415,946 | +24.7% | 63.4% | 1.7 | 297 |
| D | runner arm, out of sample + S3 in its zone | 7 | none | Rs 1,048,215 | +17.0% | 22.5% | 2.0 | 224 |
| D | runner arm, out of sample + S3 in its zone | 7 | 2x | Rs 1,446,431 | +25.3% | 42.6% | 2.0 | 224 |
| D | money arm, out of sample | 2 | none | Rs 646,060 | +5.6% | 53.4% | 0.6 | 497 |
| D | money arm, out of sample | 2 | 2x | Rs 480,498 | -0.8% | 80.8% | 0.6 | 497 |
| D | money arm, out of sample | 3 | none | Rs 715,930 | +7.9% | 43.2% | 0.9 | 432 |
| D | money arm, out of sample | 3 | 2x | Rs 663,773 | +6.2% | 70.7% | 0.9 | 432 |
| D | money arm, out of sample | 5 | none | Rs 690,283 | +7.1% | 34.8% | 1.3 | 327 |
| D | money arm, out of sample | 5 | 2x | Rs 678,245 | +6.7% | 60.2% | 1.3 | 327 |
| D | money arm, out of sample | 7 | none | Rs 704,213 | +7.5% | 29.2% | 1.7 | 245 |
| D | money arm, out of sample | 7 | 2x | Rs 750,974 | +9.0% | 53.0% | 1.7 | 245 |
| D | money arm, in-sample (M1-M5) | 2 | none | Rs 7,654,773 | +78.3% | 15.2% | 0.5 | 388 |
| D | money arm, in-sample (M1-M5) | 2 | 2x | Rs 66,451,379 | +181.9% | 30.4% | 0.5 | 388 |
| D | money arm, in-sample (M1-M5) | 3 | none | Rs 5,346,576 | +65.3% | 14.5% | 0.7 | 343 |
| D | money arm, in-sample (M1-M5) | 3 | 2x | Rs 34,491,671 | +145.3% | 29.3% | 0.7 | 343 |
| D | money arm, in-sample (M1-M5) | 5 | none | Rs 3,387,466 | +50.0% | 11.3% | 1.0 | 266 |
| D | money arm, in-sample (M1-M5) | 5 | 2x | Rs 15,864,917 | +108.1% | 22.8% | 1.0 | 266 |
| D | money arm, in-sample (M1-M5) | 7 | none | Rs 2,388,380 | +39.3% | 12.0% | 1.3 | 208 |
| D | money arm, in-sample (M1-M5) | 7 | 2x | Rs 8,623,312 | +82.9% | 23.9% | 1.3 | 208 |
| D | money arm, out of sample + S3 in its zone | 2 | none | Rs 1,458,467 | +25.5% | 54.1% | 0.8 | 660 |
| D | money arm, out of sample + S3 in its zone | 2 | 2x | Rs 2,054,515 | +34.9% | 81.2% | 0.8 | 660 |
| D | money arm, out of sample + S3 in its zone | 3 | none | Rs 1,073,732 | +17.6% | 45.5% | 1.1 | 582 |
| D | money arm, out of sample + S3 in its zone | 3 | 2x | Rs 1,376,710 | +23.9% | 72.6% | 1.1 | 582 |
| D | money arm, out of sample + S3 in its zone | 5 | none | Rs 996,589 | +15.7% | 31.5% | 1.6 | 459 |
| D | money arm, out of sample + S3 in its zone | 5 | 2x | Rs 1,361,034 | +23.6% | 56.6% | 1.6 | 459 |
| D | money arm, out of sample + S3 in its zone | 7 | none | Rs 997,164 | +15.8% | 30.5% | 2.0 | 358 |
| D | money arm, out of sample + S3 in its zone | 7 | 2x | Rs 1,458,037 | +25.5% | 55.1% | 2.0 | 358 |
| ENS | baseline: ranks 1-3 at the D1 open | 2 | none | Rs 19,296,990 | +116.9% | 40.3% | 1.9 | 2950 |
| ENS | baseline: ranks 1-3 at the D1 open | 2 | 2x | Rs 158,594,949 | +239.0% | 68.5% | 1.9 | 2950 |
| ENS | baseline: ranks 1-3 at the D1 open | 3 | none | Rs 6,642,913 | +73.0% | 52.4% | 2.8 | 2717 |
| ENS | baseline: ranks 1-3 at the D1 open | 3 | 2x | Rs 22,293,065 | +123.7% | 81.1% | 2.8 | 2717 |
| ENS | baseline: ranks 1-3 at the D1 open | 5 | none | Rs 5,843,180 | +68.4% | 45.0% | 4.7 | 2251 |
| ENS | baseline: ranks 1-3 at the D1 open | 5 | 2x | Rs 21,748,376 | +122.5% | 73.1% | 4.7 | 2251 |
| ENS | baseline: ranks 1-3 at the D1 open | 7 | none | Rs 5,289,811 | +64.9% | 35.2% | 6.6 | 1785 |
| ENS | baseline: ranks 1-3 at the D1 open | 7 | 2x | Rs 18,201,927 | +114.3% | 60.8% | 6.6 | 1785 |
| ENS | no-dip arm, out of sample | 2 | none | Rs 2,730,715 | +43.3% | 29.5% | 1.0 | 518 |
| ENS | no-dip arm, out of sample | 2 | 2x | Rs 7,458,970 | +77.3% | 54.6% | 1.0 | 518 |
| ENS | no-dip arm, out of sample | 3 | none | Rs 2,237,498 | +37.4% | 27.7% | 1.4 | 421 |
| ENS | no-dip arm, out of sample | 3 | 2x | Rs 5,542,315 | +66.5% | 52.2% | 1.4 | 421 |
| ENS | no-dip arm, out of sample | 5 | none | Rs 1,379,795 | +24.0% | 23.3% | 2.0 | 266 |
| ENS | no-dip arm, out of sample | 5 | 2x | Rs 2,485,722 | +40.5% | 44.8% | 2.0 | 266 |
| ENS | no-dip arm, out of sample | 7 | none | Rs 1,016,175 | +16.2% | 17.8% | 2.5 | 159 |
| ENS | no-dip arm, out of sample | 7 | 2x | Rs 1,504,757 | +26.3% | 35.0% | 2.5 | 159 |
| ENS | no-dip arm, in-sample (N1-N5) | 2 | none | Rs 904,479 | +13.4% | 12.1% | 0.8 | 386 |
| ENS | no-dip arm, in-sample (N1-N5) | 2 | 2x | Rs 1,169,169 | +19.7% | 28.8% | 0.8 | 386 |
| ENS | no-dip arm, in-sample (N1-N5) | 3 | none | Rs 797,411 | +10.4% | 11.2% | 1.2 | 308 |
| ENS | no-dip arm, in-sample (N1-N5) | 3 | 2x | Rs 961,141 | +14.9% | 23.6% | 1.2 | 308 |
| ENS | no-dip arm, in-sample (N1-N5) | 5 | none | Rs 752,385 | +9.0% | 8.9% | 1.6 | 199 |
| ENS | no-dip arm, in-sample (N1-N5) | 5 | 2x | Rs 914,755 | +13.7% | 19.6% | 1.6 | 199 |
| ENS | no-dip arm, in-sample (N1-N5) | 7 | none | Rs 716,201 | +7.9% | 7.4% | 1.9 | 129 |
| ENS | no-dip arm, in-sample (N1-N5) | 7 | 2x | Rs 857,137 | +12.1% | 16.5% | 1.9 | 129 |
| ENS | no-dip arm, out of sample + S3 in its zone | 2 | none | Rs 7,803,318 | +79.0% | 30.0% | 1.3 | 692 |
| ENS | no-dip arm, out of sample + S3 in its zone | 2 | 2x | Rs 48,734,365 | +164.0% | 55.2% | 1.3 | 692 |
| ENS | no-dip arm, out of sample + S3 in its zone | 3 | none | Rs 5,072,083 | +63.4% | 28.3% | 1.8 | 570 |
| ENS | no-dip arm, out of sample + S3 in its zone | 3 | 2x | Rs 24,588,800 | +128.4% | 53.1% | 1.8 | 570 |
| ENS | no-dip arm, out of sample + S3 in its zone | 5 | none | Rs 2,513,363 | +40.8% | 25.0% | 2.5 | 381 |
| ENS | no-dip arm, out of sample + S3 in its zone | 5 | 2x | Rs 7,529,175 | +77.7% | 47.3% | 2.5 | 381 |
| ENS | no-dip arm, out of sample + S3 in its zone | 7 | none | Rs 1,746,926 | +30.4% | 17.9% | 3.1 | 247 |
| ENS | no-dip arm, out of sample + S3 in its zone | 7 | 2x | Rs 4,150,761 | +56.6% | 34.8% | 3.1 | 247 |
| ENS | runner arm, out of sample | 2 | none | Rs 1,049,001 | +17.0% | 41.7% | 0.9 | 328 |
| ENS | runner arm, out of sample | 2 | 2x | Rs 735,510 | +8.5% | 75.5% | 0.9 | 328 |
| ENS | runner arm, out of sample | 3 | none | Rs 1,348,140 | +23.4% | 43.4% | 1.1 | 265 |
| ENS | runner arm, out of sample | 3 | 2x | Rs 1,477,017 | +25.8% | 78.5% | 1.1 | 265 |
| ENS | runner arm, out of sample | 5 | none | Rs 1,152,023 | +19.4% | 37.3% | 1.4 | 188 |
| ENS | runner arm, out of sample | 5 | 2x | Rs 1,331,876 | +23.1% | 69.5% | 1.4 | 188 |
| ENS | runner arm, out of sample | 7 | none | Rs 1,022,185 | +16.4% | 32.1% | 1.6 | 132 |
| ENS | runner arm, out of sample | 7 | 2x | Rs 1,270,622 | +21.9% | 60.5% | 1.6 | 132 |
| ENS | runner arm, in-sample (U1-U5) | 2 | none | Rs 1,940,177 | +33.3% | 31.4% | 0.7 | 108 |
| ENS | runner arm, in-sample (U1-U5) | 2 | 2x | Rs 3,243,355 | +48.6% | 57.1% | 0.7 | 108 |
| ENS | runner arm, in-sample (U1-U5) | 3 | none | Rs 1,672,118 | +29.2% | 25.0% | 0.8 | 74 |
| ENS | runner arm, in-sample (U1-U5) | 3 | 2x | Rs 3,244,505 | +48.7% | 46.1% | 0.8 | 74 |
| ENS | runner arm, in-sample (U1-U5) | 5 | none | Rs 1,367,742 | +23.8% | 18.3% | 0.9 | 38 |
| ENS | runner arm, in-sample (U1-U5) | 5 | 2x | Rs 2,770,037 | +43.8% | 34.7% | 0.9 | 38 |
| ENS | runner arm, in-sample (U1-U5) | 7 | none | Rs 1,339,198 | +23.2% | 13.4% | 1.0 | 18 |
| ENS | runner arm, in-sample (U1-U5) | 7 | 2x | Rs 2,913,460 | +45.3% | 25.9% | 1.0 | 18 |
| ENS | runner arm, out of sample + S3 in its zone | 2 | none | Rs 1,439,888 | +25.1% | 42.3% | 1.0 | 515 |
| ENS | runner arm, out of sample + S3 in its zone | 2 | 2x | Rs 1,323,037 | +22.9% | 76.1% | 1.0 | 515 |
| ENS | runner arm, out of sample + S3 in its zone | 3 | none | Rs 1,679,453 | +29.3% | 41.9% | 1.3 | 434 |
| ENS | runner arm, out of sample + S3 in its zone | 3 | 2x | Rs 2,216,351 | +37.1% | 77.4% | 1.3 | 434 |
| ENS | runner arm, out of sample + S3 in its zone | 5 | none | Rs 1,799,203 | +31.2% | 37.3% | 1.8 | 321 |
| ENS | runner arm, out of sample + S3 in its zone | 5 | 2x | Rs 3,098,015 | +47.2% | 68.8% | 1.8 | 321 |
| ENS | runner arm, out of sample + S3 in its zone | 7 | none | Rs 1,427,042 | +24.9% | 33.3% | 2.1 | 240 |
| ENS | runner arm, out of sample + S3 in its zone | 7 | 2x | Rs 2,303,118 | +38.2% | 61.9% | 2.1 | 240 |
| ENS | money arm, out of sample | 2 | none | Rs 947,297 | +14.5% | 37.3% | 0.6 | 445 |
| ENS | money arm, out of sample | 2 | 2x | Rs 1,032,034 | +16.6% | 65.1% | 0.6 | 445 |
| ENS | money arm, out of sample | 3 | none | Rs 735,181 | +8.5% | 32.3% | 0.8 | 386 |
| ENS | money arm, out of sample | 3 | 2x | Rs 705,240 | +7.6% | 57.6% | 0.8 | 386 |
| ENS | money arm, out of sample | 5 | none | Rs 774,502 | +9.7% | 24.7% | 1.2 | 288 |
| ENS | money arm, out of sample | 5 | 2x | Rs 868,079 | +12.4% | 46.6% | 1.2 | 288 |
| ENS | money arm, out of sample | 7 | none | Rs 831,018 | +11.4% | 24.4% | 1.5 | 214 |
| ENS | money arm, out of sample | 7 | 2x | Rs 1,046,049 | +16.9% | 44.8% | 1.5 | 214 |
| ENS | money arm, in-sample (M1-M5) | 2 | none | Rs 1,623,024 | +28.4% | 20.0% | 0.5 | 394 |
| ENS | money arm, in-sample (M1-M5) | 2 | 2x | Rs 3,269,589 | +48.9% | 39.9% | 0.5 | 394 |
| ENS | money arm, in-sample (M1-M5) | 3 | none | Rs 2,049,448 | +34.9% | 12.4% | 0.7 | 346 |
| ENS | money arm, in-sample (M1-M5) | 3 | 2x | Rs 5,739,913 | +67.8% | 24.9% | 0.7 | 346 |
| ENS | money arm, in-sample (M1-M5) | 5 | none | Rs 1,655,756 | +28.9% | 10.9% | 1.0 | 271 |
| ENS | money arm, in-sample (M1-M5) | 5 | 2x | Rs 4,119,378 | +56.4% | 21.6% | 1.0 | 271 |
| ENS | money arm, in-sample (M1-M5) | 7 | none | Rs 1,484,622 | +25.9% | 13.4% | 1.2 | 210 |
| ENS | money arm, in-sample (M1-M5) | 7 | 2x | Rs 3,445,173 | +50.6% | 26.4% | 1.2 | 210 |
| ENS | money arm, out of sample + S3 in its zone | 2 | none | Rs 1,453,366 | +25.4% | 38.8% | 0.8 | 604 |
| ENS | money arm, out of sample + S3 in its zone | 2 | 2x | Rs 2,221,441 | +37.2% | 66.4% | 0.8 | 604 |
| ENS | money arm, out of sample + S3 in its zone | 3 | none | Rs 1,397,017 | +24.3% | 30.8% | 1.1 | 529 |
| ENS | money arm, out of sample + S3 in its zone | 3 | 2x | Rs 2,356,680 | +38.9% | 55.4% | 1.1 | 529 |
| ENS | money arm, out of sample + S3 in its zone | 5 | none | Rs 1,224,670 | +20.9% | 27.1% | 1.6 | 408 |
| ENS | money arm, out of sample + S3 in its zone | 5 | 2x | Rs 1,985,746 | +34.0% | 50.5% | 1.6 | 408 |
| ENS | money arm, out of sample + S3 in its zone | 7 | none | Rs 1,165,364 | +19.6% | 23.6% | 1.9 | 316 |
| ENS | money arm, out of sample + S3 in its zone | 7 | 2x | Rs 1,990,595 | +34.0% | 44.2% | 1.9 | 316 |

## Limits

- Exploratory: thousands of rules on 2020-2026. The replay guards the search (out of sample year by year); the in-sample lists do not. Only the forward paper ledger is clean evidence.
- The in-sample books use rules chosen on these years; the out-of-sample books use, each year, only rules chosen before it. The dip arm (S3 in its zone) is in-sample in every book.
- Fills: the D1 open (AMO) at the open price; no taxes; MTF needs the stock on the broker's list.
