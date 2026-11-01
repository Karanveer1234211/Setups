# execlab discovery

execlab v1.1 | declaration c5709fdac075a289 | 2026-11-01 14:26
Period (signal days): 2020-01-01 .. 2022-12-31 | data loaded up to 2022-12-30 (2023-25 not loaded) | ranks [1, 2, 3] | engines D, ENS
Settings changed from the declaration: none

Net = stage E's zerodha_base, fully net. Intervals: 95% block bootstrap (2000 draws, 10-session blocks). Evaluation of every record in discovery uses models that never saw it (purged cross-fitting).

## Engine D

2196 selections, 2048 with a path ending inside the period, 148 listed as OUT_OF_PERIOD. memory n/a.

### Research ledger (every selection on its own, no budgets)

| book | net / selection (unfilled 0) | vs OPEN6 | vs PLAN | traded | win | median held | majors captured | majors missed | bad avoided | false triggers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN6 (every selection) | +1.57% [+0.56, +2.59] | +0.00% [+0.00, +0.00] | +0.64% [+0.49, +0.79] | 2048 | 53.9% | 5 | 109.4% of 362 | 0 | 0 of 444 | 944 (46.1%) |
| general/0bp | +2.25% [+0.96, +3.78] | +0.68% [-0.63, +2.24] | +1.32% [+0.04, +2.87] | 1343 | 48.5% | 8 | 45.8% of 362 | 133 | 136 of 444 | 692 (51.5%) |
| general/25bp | +2.15% [+0.89, +3.66] | +0.59% [-0.72, +2.13] | +1.23% [-0.02, +2.74] | 1344 | 48.7% | 7 | 40.7% of 362 | 135 | 127 of 444 | 689 (51.3%) |
| general/50bp | +2.14% [+0.91, +3.55] | +0.57% [-0.68, +2.10] | +1.21% [-0.07, +2.71] | 1288 | 48.3% | 7 | 43.9% of 362 | 144 | 153 of 444 | 666 (51.7%) |
| general/100bp | +2.40% [+1.16, +3.88] | +0.83% [-0.46, +2.38] | +1.47% [+0.19, +3.01] | 1186 | 49.8% | 8 | 40.9% of 362 | 159 | 170 of 444 | 595 (50.2%) |
| state/0bp | +2.00% [+0.53, +3.70] | +0.43% [-0.96, +2.00] | +1.07% [-0.31, +2.66] | 1379 | 48.6% | 7 | 39.3% of 362 | 135 | 120 of 444 | 709 (51.4%) |
| state/25bp | +2.30% [+0.79, +4.03] | +0.74% [-0.68, +2.35] | +1.38% [-0.04, +3.04] | 1346 | 49.8% | 8 | 43.6% of 362 | 134 | 134 of 444 | 676 (50.2%) |
| state/50bp | +2.37% [+0.86, +4.11] | +0.80% [-0.61, +2.40] | +1.44% [+0.05, +3.09] | 1245 | 51.2% | 8 | 40.2% of 362 | 140 | 151 of 444 | 607 (48.8%) |
| state/100bp | +2.09% [+0.69, +3.72] | +0.52% [-0.84, +2.08] | +1.16% [-0.18, +2.70] | 1175 | 49.9% | 8 | 41.0% of 362 | 157 | 163 of 444 | 589 (50.1%) |
| state_event/0bp | +1.65% [+0.39, +3.08] | +0.08% [-1.09, +1.43] | +0.72% [-0.45, +2.12] | 1298 | 48.6% | 7 | 49.7% of 362 | 139 | 161 of 444 | 667 (51.4%) |
| state_event/25bp | +1.64% [+0.41, +3.02] | +0.07% [-1.01, +1.37] | +0.71% [-0.38, +2.01] | 1320 | 48.4% | 6 | 48.6% of 362 | 132 | 145 of 444 | 681 (51.6%) |
| state_event/50bp | +1.39% [+0.15, +2.75] | -0.18% [-1.38, +1.18] | +0.46% [-0.73, +1.83] | 1196 | 49.4% | 7 | 35.5% of 362 | 166 | 175 of 444 | 605 (50.6%) |
| state_event/100bp | +1.88% [+0.74, +3.22] | +0.31% [-0.78, +1.60] | +0.95% [-0.16, +2.26] | 1074 | 49.5% | 8 | 41.6% of 362 | 179 | 207 of 444 | 542 (50.5%) |

### Execution ledger (Rs 10 lakh, 1/8 of equity, <= 2 entries a day, <= 6 in 5 sessions, <= 8 open, one per stock)

| book | CAGR | worst DD | Sharpe | CAGR at -25% DD | trades | daily excess vs OPEN_SB | Romano-Wolf p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN_SB | +64.2% | -39.0% | 2.12 | +35.0% (x0.59) | 784 | - | - |
| PLAN_native | +41.8% | -48.6% | 1.27 | +18.2% (x0.44) | 2043 | -5.15 bp [-12.86, +2.44] | - |
| general/0bp | +36.3% | -40.3% | 1.29 | +20.2% (x0.57) | 419 | -7.26 bp [-18.93, +4.45] | 0.977 |
| general/25bp | +13.8% | -45.7% | 0.62 | +7.4% (x0.48) | 426 | -14.49 bp [-26.40, -3.30] | 0.994 |
| general/50bp | +21.8% | -40.5% | 0.88 | +12.7% (x0.56) | 426 | -11.84 bp [-22.75, -1.93] | 0.994 |
| general/100bp | +42.9% | -38.6% | 1.53 | +24.8% (x0.60) | 419 | -5.51 bp [-16.64, +4.58] | 0.976 |
| state/0bp | +36.0% | -42.5% | 1.32 | +18.6% (x0.53) | 445 | -7.46 bp [-19.76, +3.49] | 0.977 |
| state/25bp | +40.4% | -43.0% | 1.41 | +20.5% (x0.52) | 450 | -6.09 bp [-17.75, +4.61] | 0.976 |
| state/50bp | +30.6% | -45.0% | 1.15 | +15.0% (x0.49) | 434 | -9.01 bp [-21.21, +2.11] | 0.986 |
| state/100bp | +37.8% | -41.6% | 1.34 | +20.2% (x0.55) | 428 | -6.84 bp [-18.87, +4.42] | 0.977 |
| state_event/0bp | +38.5% | -43.9% | 1.33 | +19.0% (x0.50) | 464 | -6.58 bp [-18.91, +5.41] | 0.976 |
| state_event/25bp | +19.5% | -46.6% | 0.80 | +9.7% (x0.47) | 465 | -12.54 bp [-25.08, -0.58] | 0.990 |
| state_event/50bp | +38.1% | -43.1% | 1.33 | +19.3% (x0.52) | 414 | -6.73 bp [-18.73, +4.94] | 0.976 |
| state_event/100bp | +29.9% | -43.0% | 1.14 | +15.5% (x0.52) | 400 | -9.30 bp [-21.24, +1.56] | 0.986 |

Probability of backtest overfitting (CSCV, 12 configurations): 0.87

**Candidates (declared rule: per engine, the configurations (variant x hurdle) whose discovery portfolio beats OPEN_SB on mean daily return with a Romano-Wolf adjusted p-value under 0.20 across the engine's configurations, whose own CAGR and net per selection are above 0, best first, at most 5; none passes = nothing is frozen for that engine): none**

### general vs state vs state + event

Best configuration of each variant (by mean daily excess over OPEN_SB): general = general/100bp, state = state/25bp, state_event = state_event/0bp.

Per cell: the policy's net per selection (unfilled = 0) and its difference from OPEN6 with the 95% block bootstrap interval; * = Benjamini-Hochberg q <= 0.10 within the variant's table. Groups under 30 selections are pooled as 'other'. A state is tl_state's confirmed state at T, the event its shown event at T.

By state:

| group | selections | OPEN6 | PLAN | general | state | state_event |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2048 | +1.57% | +0.93% | +2.40% (+0.83% [-0.46, +2.38]) | +2.30% (+0.74% [-0.68, +2.35]) | +1.65% (+0.08% [-1.09, +1.43]) |
| S01 | 368 | +0.93% | +0.44% | +0.04% (-0.90% [-2.51, +0.81]) | +0.65% (-0.28% [-2.28, +2.12]) | +1.10% (+0.17% [-1.43, +1.94]) |
| S02 | 150 | +0.82% | +0.25% | +0.17% (-0.65% [-3.70, +2.70]) | -1.09% (-1.91% [-5.40, +1.57]) | -1.14% (-1.96% [-5.11, +1.59]) |
| S03 | 144 | +2.51% | +1.89% | +0.43% (-2.07% [-5.49, +0.93]) | -1.55% (-4.06% [-7.31, -1.21]) * | -0.01% (-2.51% [-6.17, +0.35]) |
| S06 | 63 | +3.37% | +2.91% | +6.55% (+3.18% [-0.66, +7.04]) | +5.52% (+2.15% [-0.46, +4.81]) | +4.60% (+1.23% [-2.42, +4.89]) |
| S07 | 68 | +1.73% | +1.12% | +1.41% (-0.33% [-1.92, +1.33]) | +0.32% (-1.41% [-3.85, +0.91]) | -1.05% (-2.78% [-4.99, -0.88]) * |
| S08 | 178 | +4.20% | +3.26% | +9.94% (+5.73% [+0.40, +11.15]) | +11.20% (+7.00% [+2.15, +13.01]) * | +8.93% (+4.73% [+0.26, +9.54]) |
| S09 | 542 | +0.82% | +0.18% | +2.25% (+1.43% [-1.16, +4.60]) | +0.20% (-0.62% [-2.53, +1.26]) | +0.88% (+0.07% [-2.27, +2.59]) |
| UNKNOWN | 534 | +1.60% | +0.92% | +2.47% (+0.87% [-0.97, +2.85]) | +4.47% (+2.87% [-0.05, +5.79]) | +1.61% (+0.01% [-1.75, +1.88]) |
| other | 1 | +9.13% | +4.00% | +0.00% (-9.13% (too few days)) | +5.51% (-3.61% (too few days)) | +0.00% (-9.13% (too few days)) |

By state | event:

| group | selections | OPEN6 | PLAN | general | state | state_event |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2048 | +1.57% | +0.93% | +2.40% (+0.83% [-0.46, +2.38]) | +2.30% (+0.74% [-0.68, +2.35]) | +1.65% (+0.08% [-1.09, +1.43]) |
| S01|none | 37 | -1.07% | -1.44% | -0.97% (+0.10% [-1.97, +2.18]) | +0.30% (+1.37% [-1.29, +4.43]) | +0.60% (+1.67% [-0.54, +3.94]) |
| S01|breakout | 239 | +0.66% | +0.18% | +0.42% (-0.24% [-2.13, +1.83]) | +1.03% (+0.38% [-1.88, +3.13]) | +1.18% (+0.52% [-1.13, +2.57]) |
| S01|failed_bo | 76 | +2.60% | +2.17% | +0.58% (-2.02% [-4.26, +0.32]) | -0.08% (-2.69% [-5.15, -0.12]) | +1.64% (-0.96% [-4.92, +3.46]) |
| S02|none | 30 | +0.95% | +0.51% | +0.25% (-0.69% [-1.70, +0.39]) | +1.91% (+0.96% [-1.11, +3.54]) | +0.34% (-0.60% [-3.11, +1.93]) |
| S02|breakout | 99 | +1.17% | +0.54% | +1.55% (+0.37% [-4.24, +5.17]) | -0.07% (-1.24% [-5.77, +3.37]) | -1.19% (-2.36% [-6.83, +2.51]) |
| S03|none | 106 | +2.13% | +1.58% | -1.17% (-3.31% [-6.85, -0.03]) | -2.31% (-4.45% [-8.17, -1.12]) | -1.55% (-3.68% [-7.58, -0.57]) |
| S06|none | 31 | +2.81% | +2.57% | +6.66% (+3.85% [-2.60, +10.44]) | +5.48% (+2.67% [-1.65, +7.75]) | +4.01% (+1.19% [-3.62, +6.25]) |
| S07|none | 47 | +1.75% | +1.05% | +2.33% (+0.58% [-1.53, +2.56]) | +0.72% (-1.02% [-3.18, +0.79]) | +0.06% (-1.69% [-3.66, +0.02]) |
| S08|breakdown | 129 | +3.44% | +2.40% | +8.69% (+5.25% [+0.22, +10.94]) | +10.03% (+6.59% [+0.57, +13.60]) | +5.70% (+2.26% [-1.79, +7.09]) |
| S08|bear_trap | 36 | +6.34% | +5.45% | +12.79% (+6.45% [-3.61, +14.78]) | +14.39% (+8.05% [+2.16, +12.42]) * | +17.89% (+11.55% [+6.79, +15.35]) * |
| S09|breakdown | 506 | +0.83% | +0.20% | +2.24% (+1.41% [-1.29, +4.61]) | +0.04% (-0.79% [-2.79, +1.10]) | +0.91% (+0.08% [-2.27, +2.69]) |
| UNKNOWN|none | 154 | +1.60% | +0.92% | +3.41% (+1.81% [-1.62, +5.42]) | +3.56% (+1.96% [-1.32, +6.11]) | +2.20% (+0.60% [-1.25, +2.59]) |
| UNKNOWN|breakout | 203 | +0.91% | +0.32% | +0.95% (+0.04% [-2.67, +2.88]) | +2.20% (+1.29% [-3.52, +5.45]) | +1.21% (+0.29% [-2.38, +3.03]) |
| UNKNOWN|failed_bo | 44 | -0.19% | -0.63% | +2.92% (+3.11% [-1.23, +7.82]) | +4.43% (+4.62% [+0.29, +9.41]) | +1.09% (+1.28% [-2.63, +5.68]) |
| UNKNOWN|breakdown | 106 | +2.89% | +1.88% | +2.86% (-0.03% [-4.15, +4.94]) | +10.45% (+7.56% [-0.10, +16.65]) | +1.00% (-1.89% [-6.88, +3.60]) |
| other | 205 | +2.61% | +1.94% | +2.88% (+0.27% [-3.11, +4.88]) | +1.59% (-1.02% [-4.06, +2.62]) | +2.54% (-0.08% [-2.92, +3.55]) |

### general/100bp in detail

Orders traded: OPEN 430, BSTOP 132, BHIGH 77, LDIP 116, LDEEP 36, ODIP 139, LVL_RT 155, LVL_RC 76, SWHI 25. Exits: EXIT 592, STOP1 62, STOP2 11, TP2 82, FORCED 138, STOP_SW 129, STOP_LV 172. Mean MFE +12.6%, MAE -5.3%.
Majors: 362 (PLAN profit +5580.0%), 203 traded, profit captured +40.9%; bad trades avoided 170 of 444 (loss avoided +1852.1% of PLAN net); opportunity cost: OPEN6 net of the 862 records not traded = +0.783% per selection.

Per-state cards (the best configuration's own choices by tl_state state at T):

| state | selections | traded | abandoned | orders used | exits | vs OPEN6 |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2048 | 1186 | 821 | OPEN 36%, LVL_RT 13%, ODIP 12% | EXIT 50%, STOP_LV 15%, FORCED 12% | +0.83% [-0.46, +2.38] |
| S01 | 368 | 217 | 144 | LVL_RT 22%, OPEN 19%, ODIP 12% | EXIT 70%, STOP_LV 11%, FORCED 8% | -0.90% [-2.51, +0.81] |
| S02 | 150 | 92 | 56 | OPEN 33%, LVL_RT 29%, BHIGH 11% | EXIT 39%, STOP_LV 27%, TP2 10% | -0.65% [-3.70, +2.70] |
| S03 | 144 | 68 | 76 | OPEN 53%, BSTOP 12%, ODIP 9% | EXIT 47%, FORCED 19%, STOP1 16% | -2.07% [-5.49, +0.93] |
| S06 | 63 | 52 | 11 | OPEN 52%, ODIP 19%, BSTOP 10% | EXIT 63%, FORCED 13%, STOP_SW 10% | +3.18% [-0.66, +7.04] |
| S07 | 68 | 32 | 34 | OPEN 28%, SWHI 19%, ODIP 16% | EXIT 56%, TP2 16%, STOP_SW 9% | -0.33% [-1.92, +1.33] |
| S08 | 178 | 131 | 43 | OPEN 56%, BSTOP 14%, ODIP 14% | EXIT 34%, TP2 20%, FORCED 18% | +5.73% [+0.40, +11.15] |
| S09 | 542 | 298 | 228 | OPEN 40%, LDIP 15%, ODIP 14% | EXIT 43%, STOP_LV 18%, STOP_SW 14% | +1.43% [-1.16, +4.60] |
| UNKNOWN | 534 | 296 | 228 | OPEN 32%, LVL_RT 16%, BSTOP 14% | EXIT 51%, STOP_LV 15%, FORCED 12% | +0.87% [-0.97, +2.85] |
| other | 1 | 0 | 1 | - | - | -9.13% (too few days) |

Entry lag cohorts:

| lag | trades | mean net | median held | win |
| --- | --- | --- | --- | --- |
| T+1 | 660 | +4.88% | 8 | 51% |
| T+2 | 198 | +2.76% | 8 | 47% |
| T+3 | 109 | +3.11% | 5 | 51% |
| T+4 | 76 | +5.08% | 4 | 50% |
| T+5 | 36 | +4.29% | 10 | 47% |
| T+6 | 22 | +4.21% | 6 | 45% |
| T+7 | 25 | +2.63% | 10 | 40% |
| T+8 | 24 | +0.12% | 10 | 42% |
| T+9 | 14 | +1.64% | 18 | 64% |
| T+10 | 22 | +3.57% | 10 | 41% |

Abandons by close: T+0 498, T+1 146, T+2 66, T+3 44, T+4 25, T+5 17, T+6 8, T+7 8, T+8 5, T+9 4

Setup cards (the policy's own choices as rules; value = those records vs their OPEN6):

| # | rule | rows | decided | policy did | vs OPEN6 |
| --- | --- | --- | --- | --- | --- |
| 1 | ema20_gap <= 0.03856 AND dist_hi60 > -0.5459 AND day > 0.5 | 1644 | 536 | ENTER_SWHI 18%, WAIT 15%, ENTER_LVL_RC 13% | +1.17% [-0.49, +3.13] |
| 2 | ema20_gap <= 0.03856 AND dist_hi60 > -0.5459 AND day <= 0.5 | 1219 | 685 | ABANDON 30%, ENTER_OPEN 13%, ENTER_LVL_RC 9% | -0.10% [-1.78, +1.58] |
| 3 | ema20_gap > 0.03856 AND swh_atr > -2.744 AND range15_atr > 3.691 | 994 | 441 | ENTER_LVL_RT 31%, ABANDON 16%, WAIT 10% | -1.29% [-3.35, +0.63] |
| 4 | ema20_gap > 0.03856 AND swh_atr <= -2.744 AND score <= 0.01724 | 218 | 70 | ENTER_LDEEP 27%, WAIT 17%, ENTER_BHIGH 13% | -3.76% [-7.42, +0.11] |
| 5 | ema20_gap > 0.03856 AND swh_atr <= -2.744 AND score > 0.01724 | 185 | 55 | WAIT 39%, ENTER_LVL_RT 12%, ENTER_LDEEP 11% | -0.49% [-4.84, +3.75] |
| 6 | ema20_gap <= 0.03856 AND dist_hi60 <= -0.5459 AND day <= 0.5 | 162 | 118 | ENTER_OPEN 59%, WAIT 15%, ENTER_LDIP 9% | +14.32% [+6.68, +20.58] |
| 7 | ema20_gap > 0.03856 AND swh_atr > -2.744 AND range15_atr <= 3.691 | 155 | 106 | ABANDON 27%, ENTER_OPEN 23%, ENTER_ODIP 9% | -1.67% [-4.87, +1.54] |
| 8 | ema20_gap <= 0.03856 AND dist_hi60 <= -0.5459 AND day > 0.5 | 141 | 37 | WAIT 48%, ENTER_ODIP 15%, ENTER_LDIP 13% | +13.20% [+5.31, +20.69] |

Exit cards (hold decisions of the traded positions):

| # | rule | rows | policy did |
| --- | --- | --- | --- |
| 1 | ema50_gap > -0.06404 AND clv > 0.197 AND ret1 <= 0.04681 | 7810 | KEEP 62%, TP2 14%, STOP2 11% |
| 2 | ema50_gap <= -0.06404 AND ema50_gap > -0.23 AND ema20_gap > -0.08408 | 2250 | TP2 27%, KEEP 23%, STOP2 20% |
| 3 | ema50_gap > -0.06404 AND clv <= 0.197 AND flow20 > 0.01583 | 1951 | KEEP 43%, TP2 32%, STOP2 10% |
| 4 | ema50_gap > -0.06404 AND clv > 0.197 AND ret1 > 0.04681 | 1386 | TP2 36%, KEEP 26%, STOP2 17% |
| 5 | ema50_gap <= -0.06404 AND ema50_gap <= -0.23 AND range15_atr > 3.693 | 958 | TP2 35%, STOP1 20%, KEEP 15% |
| 6 | ema50_gap <= -0.06404 AND ema50_gap > -0.23 AND ema20_gap <= -0.08408 | 724 | STOP1 45%, STOP_SW 18%, STOP2 11% |
| 7 | ema50_gap > -0.06404 AND clv <= 0.197 AND flow20 <= 0.01583 | 657 | TP2 62%, KEEP 15%, STOP2 9% |
| 8 | ema50_gap <= -0.06404 AND ema50_gap <= -0.23 AND range15_atr <= 3.693 | 626 | TP2 73%, STOP1 9%, KEEP 8% |

Intraday (exploratory, 3-minute bars, 0 open entries with usable bars):

fewer than 30 open entries with usable 3-minute bars on the entry session

Learning (value at the start by policy-iteration step):

- hold general: +0.0104 -> +0.0166 -> +0.0284 -> +0.0246
- watch general 0bp: +0.0280 -> +0.0241 -> +0.0234 -> +0.0225
- watch general 25bp: +0.0255 -> +0.0218 -> +0.0242 -> +0.0199
- watch general 50bp: +0.0230 -> +0.0196 -> +0.0225 -> +0.0183
- watch general 100bp: +0.0180 -> +0.0181 -> +0.0169 -> +0.0182
- hold state: +0.0104 -> +0.0161 -> +0.0283 -> +0.0245
- watch state 0bp: +0.0255 -> +0.0272 -> +0.0241 -> +0.0200
- watch state 25bp: +0.0230 -> +0.0256 -> +0.0246 -> +0.0214
- watch state 50bp: +0.0205 -> +0.0234 -> +0.0213 -> +0.0207
- watch state 100bp: +0.0155 -> +0.0187 -> +0.0175 -> +0.0152
- hold state_event: +0.0104 -> +0.0155 -> +0.0232 -> +0.0173
- watch state_event 0bp: +0.0195 -> +0.0183 -> +0.0162 -> +0.0165
- watch state_event 25bp: +0.0170 -> +0.0177 -> +0.0132 -> +0.0148
- watch state_event 50bp: +0.0145 -> +0.0155 -> +0.0137 -> +0.0109
- watch state_event 100bp: +0.0095 -> +0.0133 -> +0.0100 -> +0.0136

## Engine ENS

2208 selections, 2052 with a path ending inside the period, 156 listed as OUT_OF_PERIOD. memory n/a.

### Research ledger (every selection on its own, no budgets)

| book | net / selection (unfilled 0) | vs OPEN6 | vs PLAN | traded | win | median held | majors captured | majors missed | bad avoided | false triggers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN6 (every selection) | +2.02% [+1.02, +2.99] | +0.00% [+0.00, +0.00] | +0.64% [+0.48, +0.79] | 2052 | 55.9% | 5 | 110.1% of 373 | 0 | 0 of 397 | 904 (44.1%) |
| general/0bp | +3.07% [+1.73, +4.61] | +1.06% [+0.05, +2.15] | +1.70% [+0.67, +2.81] | 1593 | 53.5% | 6 | 67.7% of 373 | 85 | 91 of 397 | 741 (46.5%) |
| general/25bp | +3.06% [+1.65, +4.62] | +1.04% [+0.04, +2.15] | +1.68% [+0.65, +2.85] | 1521 | 54.4% | 6 | 71.8% of 373 | 83 | 101 of 397 | 694 (45.6%) |
| general/50bp | +3.14% [+1.75, +4.73] | +1.13% [+0.12, +2.25] | +1.77% [+0.73, +2.93] | 1457 | 54.8% | 6 | 72.3% of 373 | 98 | 113 of 397 | 658 (45.2%) |
| general/100bp | +2.82% [+1.48, +4.31] | +0.80% [-0.17, +1.92] | +1.44% [+0.45, +2.60] | 1310 | 55.4% | 6 | 63.6% of 373 | 128 | 142 of 397 | 584 (44.6%) |
| state/0bp | +2.64% [+1.14, +4.19] | +0.62% [-0.44, +1.82] | +1.26% [+0.18, +2.47] | 1380 | 54.1% | 6 | 67.8% of 373 | 129 | 109 of 397 | 634 (45.9%) |
| state/25bp | +2.55% [+1.09, +4.12] | +0.53% [-0.53, +1.71] | +1.18% [+0.10, +2.40] | 1338 | 53.1% | 6 | 67.4% of 373 | 138 | 117 of 397 | 627 (46.9%) |
| state/50bp | +2.40% [+1.10, +3.74] | +0.39% [-0.65, +1.52] | +1.03% [+0.03, +2.15] | 1281 | 53.5% | 5 | 57.9% of 373 | 140 | 134 of 397 | 596 (46.5%) |
| state/100bp | +2.71% [+1.31, +4.27] | +0.69% [-0.39, +1.93] | +1.33% [+0.26, +2.58] | 1163 | 55.7% | 6 | 65.3% of 373 | 167 | 144 of 397 | 515 (44.3%) |
| state_event/0bp | +3.17% [+1.49, +4.99] | +1.15% [-0.07, +2.54] | +1.79% [+0.55, +3.20] | 1377 | 54.0% | 7 | 68.5% of 373 | 121 | 114 of 397 | 633 (46.0%) |
| state_event/25bp | +3.25% [+1.57, +5.12] | +1.23% [+0.03, +2.61] | +1.88% [+0.64, +3.31] | 1359 | 54.6% | 7 | 69.9% of 373 | 123 | 126 of 397 | 617 (45.4%) |
| state_event/50bp | +3.32% [+1.68, +5.13] | +1.30% [+0.04, +2.73] | +1.95% [+0.68, +3.42] | 1307 | 54.0% | 8 | 66.2% of 373 | 132 | 135 of 397 | 601 (46.0%) |
| state_event/100bp | +3.24% [+1.66, +5.02] | +1.23% [+0.03, +2.55] | +1.87% [+0.67, +3.20] | 1219 | 55.5% | 8 | 70.6% of 373 | 141 | 154 of 397 | 543 (44.5%) |

### Execution ledger (Rs 10 lakh, 1/8 of equity, <= 2 entries a day, <= 6 in 5 sessions, <= 8 open, one per stock)

| book | CAGR | worst DD | Sharpe | CAGR at -25% DD | trades | daily excess vs OPEN_SB | Romano-Wolf p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPEN_SB | +94.2% | -34.0% | 2.88 | +59.9% (x0.70) | 799 | - | - |
| PLAN_native | +72.8% | -39.7% | 1.93 | +38.9% (x0.58) | 2050 | -3.92 bp [-10.65, +2.63] | - |
| general/0bp | +65.9% | -28.4% | 2.14 | +55.7% (x0.87) | 558 | -6.20 bp [-15.40, +3.40] | 0.989 |
| general/25bp | +85.0% | -23.5% | 2.59 | +85.0% (x1.00) | 555 | -1.86 bp [-11.57, +7.05] | 0.939 |
| general/50bp | +80.0% | -32.7% | 2.41 | +54.8% (x0.73) | 525 | -2.85 bp [-12.21, +6.62] | 0.961 |
| general/100bp | +63.9% | -33.8% | 2.05 | +42.9% (x0.71) | 520 | -6.63 bp [-16.99, +4.03] | 0.989 |
| state/0bp | +61.7% | -35.0% | 2.04 | +39.1% (x0.67) | 543 | -7.23 bp [-16.64, +2.04] | 0.989 |
| state/25bp | +61.2% | -28.3% | 2.07 | +52.0% (x0.87) | 518 | -7.41 bp [-17.66, +3.38] | 0.989 |
| state/50bp | +45.8% | -35.5% | 1.59 | +29.4% (x0.66) | 498 | -11.30 bp [-21.53, -1.29] | 0.989 |
| state/100bp | +61.2% | -28.8% | 2.11 | +50.7% (x0.85) | 482 | -7.45 bp [-17.62, +3.03] | 0.989 |
| state_event/0bp | +72.9% | -42.8% | 2.26 | +34.4% (x0.52) | 478 | -4.46 bp [-14.96, +6.28] | 0.973 |
| state_event/25bp | +66.0% | -33.9% | 2.13 | +43.6% (x0.70) | 471 | -6.14 bp [-15.89, +3.68] | 0.989 |
| state_event/50bp | +71.7% | -37.1% | 2.28 | +41.4% (x0.63) | 432 | -4.83 bp [-15.81, +5.69] | 0.976 |
| state_event/100bp | +59.7% | -45.6% | 1.93 | +26.4% (x0.48) | 435 | -7.61 bp [-18.68, +3.91] | 0.989 |

Probability of backtest overfitting (CSCV, 12 configurations): 0.71

**Candidates (declared rule: per engine, the configurations (variant x hurdle) whose discovery portfolio beats OPEN_SB on mean daily return with a Romano-Wolf adjusted p-value under 0.20 across the engine's configurations, whose own CAGR and net per selection are above 0, best first, at most 5; none passes = nothing is frozen for that engine): none**

### general vs state vs state + event

Best configuration of each variant (by mean daily excess over OPEN_SB): general = general/25bp, state = state/0bp, state_event = state_event/0bp.

Per cell: the policy's net per selection (unfilled = 0) and its difference from OPEN6 with the 95% block bootstrap interval; * = Benjamini-Hochberg q <= 0.10 within the variant's table. Groups under 30 selections are pooled as 'other'. A state is tl_state's confirmed state at T, the event its shown event at T.

By state:

| group | selections | OPEN6 | PLAN | general | state | state_event |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2052 | +2.02% | +1.37% | +3.06% (+1.04% [+0.04, +2.15]) | +2.64% (+0.62% [-0.44, +1.82]) | +3.17% (+1.15% [-0.07, +2.54]) |
| S01 | 344 | +1.34% | +0.76% | +1.89% (+0.55% [-0.75, +2.06]) | -0.39% (-1.73% [-2.98, -0.45]) * | +1.76% (+0.42% [-1.42, +2.83]) |
| S02 | 138 | -0.35% | -0.78% | +3.18% (+3.54% [+0.84, +6.04]) * | +1.84% (+2.19% [-1.44, +5.65]) | +2.13% (+2.49% [-0.04, +4.98]) |
| S03 | 214 | +2.09% | +1.56% | +1.16% (-0.93% [-2.77, +0.89]) | +0.79% (-1.30% [-3.73, +0.93]) | +0.90% (-1.20% [-3.94, +1.16]) |
| S06 | 53 | +2.92% | +1.83% | +5.69% (+2.77% [-0.14, +5.67]) | +7.70% (+4.78% [+1.39, +7.89]) * | +7.29% (+4.37% [+0.47, +9.03]) |
| S07 | 64 | +1.97% | +1.41% | +1.97% (+0.00% [-1.62, +2.05]) | +4.73% (+2.76% [+0.01, +5.68]) | +3.53% (+1.57% [-0.49, +3.90]) |
| S08 | 185 | +5.17% | +4.13% | +10.86% (+5.68% [+1.79, +9.05]) * | +10.20% (+5.03% [+0.95, +8.67]) * | +12.20% (+7.03% [+2.28, +11.51]) * |
| S09 | 480 | +1.64% | +1.11% | +0.97% (-0.67% [-2.53, +1.18]) | +0.93% (-0.70% [-2.23, +0.93]) | +0.81% (-0.82% [-2.82, +1.35]) |
| UNKNOWN | 573 | +2.17% | +1.47% | +3.53% (+1.36% [-0.16, +2.98]) | +3.62% (+1.44% [-0.38, +3.47]) | +3.74% (+1.57% [-0.32, +3.55]) |
| other | 1 | +9.13% | +4.00% | +5.17% (-3.95% (too few days)) | +0.00% (-9.13% (too few days)) | +0.00% (-9.13% (too few days)) |

By state | event:

| group | selections | OPEN6 | PLAN | general | state | state_event |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2052 | +2.02% | +1.37% | +3.06% (+1.04% [+0.04, +2.15]) | +2.64% (+0.62% [-0.44, +1.82]) | +3.17% (+1.15% [-0.07, +2.54]) |
| S01|none | 55 | -2.04% | -2.53% | +1.27% (+3.31% [+0.23, +6.67]) | -1.34% (+0.70% [-2.60, +4.02]) | -0.88% (+1.16% [-1.01, +4.17]) |
| S01|breakout | 174 | +1.59% | +0.92% | +1.29% (-0.30% [-2.26, +2.01]) | -1.21% (-2.79% [-4.70, -0.75]) * | +1.76% (+0.17% [-2.16, +2.73]) |
| S01|failed_bo | 102 | +2.44% | +2.08% | +2.56% (+0.12% [-1.53, +2.17]) | +1.62% (-0.82% [-2.22, +0.80]) | +3.07% (+0.63% [-2.16, +4.50]) |
| S02|breakout | 89 | -1.15% | -1.65% | +3.64% (+4.78% [+1.27, +7.99]) * | +1.19% (+2.34% [-1.60, +6.10]) | +2.71% (+3.86% [+0.42, +7.29]) |
| S03|none | 153 | +1.34% | +0.84% | +0.66% (-0.68% [-2.18, +0.99]) | -0.13% (-1.47% [-4.09, +0.85]) | -0.39% (-1.73% [-4.23, +0.43]) |
| S06|none | 36 | +2.78% | +1.66% | +5.53% (+2.75% [-0.36, +6.01]) | +9.40% (+6.63% [+3.36, +9.62]) * | +8.43% (+5.65% [+2.29, +9.48]) * |
| S07|none | 37 | +2.28% | +1.76% | +3.14% (+0.86% [-1.93, +4.64]) | +4.50% (+2.22% [-1.04, +6.02]) | +4.56% (+2.29% [-1.19, +5.90]) |
| S08|breakdown | 137 | +4.89% | +3.68% | +9.66% (+4.78% [+0.63, +9.03]) | +8.23% (+3.34% [-0.00, +7.01]) | +10.51% (+5.62% [+0.24, +11.15]) |
| S08|bear_trap | 35 | +5.68% | +5.27% | +12.74% (+7.06% [-0.62, +14.61]) | +14.64% (+8.97% [+0.56, +16.84]) | +13.86% (+8.18% [+1.54, +14.26]) * |
| S09|breakdown | 438 | +1.40% | +0.90% | +1.04% (-0.36% [-2.45, +1.80]) | +0.95% (-0.45% [-2.11, +1.27]) | +0.68% (-0.72% [-2.98, +1.79]) |
| UNKNOWN|none | 191 | +1.54% | +0.90% | +3.19% (+1.64% [-0.16, +3.61]) | +3.77% (+2.23% [+0.12, +4.61]) | +3.49% (+1.95% [-0.79, +4.82]) |
| UNKNOWN|breakout | 177 | +2.14% | +1.51% | +1.63% (-0.51% [-2.65, +2.01]) | +0.90% (-1.24% [-2.87, +0.36]) | +0.86% (-1.28% [-2.87, +0.33]) |
| UNKNOWN|failed_bo | 63 | +0.17% | -0.29% | -0.19% (-0.36% [-1.78, +1.16]) | -0.95% (-1.12% [-2.43, +0.22]) | +0.27% (+0.10% [-1.78, +1.99]) |
| UNKNOWN|breakdown | 119 | +3.83% | +2.93% | +7.89% (+4.07% [-0.55, +9.31]) | +8.79% (+4.96% [-0.42, +11.05]) | +9.54% (+5.71% [-0.15, +12.11]) |
| other | 246 | +3.32% | +2.56% | +3.77% (+0.45% [-1.43, +2.39]) | +4.11% (+0.79% [-1.28, +3.10]) | +4.37% (+1.05% [-0.84, +3.39]) |

### general/25bp in detail

Orders traded: OPEN 792, BSTOP 138, BHIGH 111, LDIP 100, LDEEP 27, ODIP 182, LVL_RT 59, LVL_RC 69, SWHI 43. Exits: EXIT 959, STOP1 72, STOP2 9, TP2 107, FORCED 43, STOP_SW 163, STOP_LV 168. Mean MFE +10.1%, MAE -4.1%.
Majors: 373 (PLAN profit +5672.5%), 290 traded, profit captured +71.8%; bad trades avoided 101 of 397 (loss avoided +989.5% of PLAN net); opportunity cost: OPEN6 net of the 531 records not traded = +0.365% per selection.

Per-state cards (the best configuration's own choices by tl_state state at T):

| state | selections | traded | abandoned | orders used | exits | vs OPEN6 |
| --- | --- | --- | --- | --- | --- | --- |
| all | 2052 | 1521 | 503 | OPEN 52%, ODIP 12%, BSTOP 9% | EXIT 63%, STOP_LV 11%, STOP_SW 11% | +1.04% [+0.04, +2.15] |
| S01 | 344 | 236 | 103 | OPEN 44%, BSTOP 13%, ODIP 9% | EXIT 62%, STOP_LV 18%, STOP_SW 8% | +0.55% [-0.75, +2.06] |
| S02 | 138 | 107 | 29 | OPEN 47%, ODIP 11%, LVL_RT 10% | EXIT 77%, STOP_LV 12%, TP2 7% | +3.54% [+0.84, +6.04] |
| S03 | 214 | 170 | 44 | OPEN 55%, ODIP 22%, SWHI 8% | EXIT 58%, STOP1 12%, STOP_SW 12% | -0.93% [-2.77, +0.89] |
| S06 | 53 | 50 | 3 | OPEN 70%, BSTOP 8%, ODIP 6% | EXIT 62%, TP2 14%, STOP_SW 10% | +2.77% [-0.14, +5.67] |
| S07 | 64 | 43 | 20 | OPEN 51%, ODIP 23%, BSTOP 9% | EXIT 63%, STOP_SW 12%, TP2 9% | +0.00% [-1.62, +2.05] |
| S08 | 185 | 177 | 8 | OPEN 73%, BSTOP 11%, BHIGH 6% | EXIT 58%, STOP_SW 14%, TP2 10% | +5.68% [+1.79, +9.05] |
| S09 | 480 | 310 | 160 | OPEN 46%, BSTOP 13%, BHIGH 11% | EXIT 60%, STOP_LV 15%, STOP_SW 15% | -0.67% [-2.53, +1.18] |
| UNKNOWN | 573 | 427 | 136 | OPEN 51%, ODIP 14%, LDIP 9% | EXIT 66%, TP2 10%, STOP_SW 9% | +1.36% [-0.16, +2.98] |
| other | 1 | 1 | 0 | ODIP 100% | EXIT 100% | -3.95% (too few days) |

Entry lag cohorts:

| lag | trades | mean net | median held | win |
| --- | --- | --- | --- | --- |
| T+1 | 940 | +5.24% | 6 | 57% |
| T+2 | 254 | +3.49% | 5 | 53% |
| T+3 | 120 | +2.23% | 6 | 54% |
| T+4 | 73 | -0.19% | 4 | 44% |
| T+5 | 42 | +1.19% | 6 | 45% |
| T+6 | 29 | +1.93% | 4 | 48% |
| T+7 | 22 | -0.37% | 4 | 36% |
| T+8 | 22 | +1.20% | 5 | 32% |
| T+9 | 6 | +0.71% | 6 | 17% |
| T+10 | 13 | +5.49% | 12 | 62% |

Abandons by close: T+0 266, T+1 97, T+2 50, T+3 31, T+4 19, T+5 19, T+6 10, T+7 4, T+8 4, T+9 3

Setup cards (the policy's own choices as rules; value = those records vs their OPEN6):

| # | rule | rows | decided | policy did | vs OPEN6 |
| --- | --- | --- | --- | --- | --- |
| 1 | ema50_gap > -0.2874 AND day <= 0.5 AND range15_atr > 3.43 | 1449 | 753 | ENTER_OPEN 19%, ABANDON 15%, ENTER_LDIP 9% | +0.21% [-0.79, +1.27] |
| 2 | ema50_gap > -0.2874 AND day > 0.5 AND m10_atr > -1.205 | 1356 | 530 | ENTER_LVL_RT 15%, WAIT 13%, ENTER_SWHI 13% | -0.47% [-1.80, +0.93] |
| 3 | ema50_gap > -0.2874 AND day > 0.5 AND m10_atr <= -1.205 | 970 | 312 | WAIT 16%, ENTER_LVL_RC 15%, ENTER_LDEEP 13% | +1.37% [-0.37, +3.23] |
| 4 | ema50_gap > -0.2874 AND day <= 0.5 AND range15_atr <= 3.43 | 469 | 325 | ENTER_OPEN 43%, ENTER_ODIP 16%, ABANDON 11% | +1.48% [-0.23, +3.32] |
| 5 | ema50_gap <= -0.2874 | 145 | 132 | ENTER_OPEN 86%, ABANDON 3%, ENTER_ODIP 3% | +9.92% [+4.77, +14.14] |

Exit cards (hold decisions of the traded positions):

| # | rule | rows | policy did |
| --- | --- | --- | --- |
| 1 | dist_hi20 > -0.1212 AND vol_ratio <= 1.139 AND adv_log > 7.658 | 4492 | KEEP 47%, TP2 34%, STOP_SW 7% |
| 2 | dist_hi20 > -0.1212 AND vol_ratio > 1.139 AND ret1 <= 0.03619 | 3482 | KEEP 58%, TP2 16%, STOP_SW 7% |
| 3 | dist_hi20 <= -0.1212 AND swl_atr > -0.1587 AND ema20_atr > -1.259 | 2205 | TP2 31%, KEEP 28%, STOP2 12% |
| 4 | dist_hi20 > -0.1212 AND vol_ratio <= 1.139 AND adv_log <= 7.658 | 1775 | TP2 50%, KEEP 25%, STOP1 7% |
| 5 | dist_hi20 > -0.1212 AND vol_ratio > 1.139 AND ret1 > 0.03619 | 1400 | KEEP 37%, TP2 29%, STOP2 10% |
| 6 | dist_hi20 <= -0.1212 AND swl_atr <= -0.1587 AND ema50_gap > -0.2311 | 1004 | STOP1 33%, TP2 18%, EXIT 18% |
| 7 | dist_hi20 <= -0.1212 AND swl_atr > -0.1587 AND ema20_atr <= -1.259 | 875 | STOP_SW 35%, TP2 24%, KEEP 16% |
| 8 | dist_hi20 <= -0.1212 AND swl_atr <= -0.1587 AND ema50_gap <= -0.2311 | 551 | STOP2 30%, KEEP 28%, TP2 20% |

Intraday (exploratory, 3-minute bars, 0 open entries with usable bars):

fewer than 30 open entries with usable 3-minute bars on the entry session

Learning (value at the start by policy-iteration step):

- hold general: +0.0109 -> +0.0235 -> +0.0278 -> +0.0247
- watch general 0bp: +0.0353 -> +0.0301 -> +0.0304 -> +0.0307
- watch general 25bp: +0.0328 -> +0.0279 -> +0.0279 -> +0.0287
- watch general 50bp: +0.0303 -> +0.0254 -> +0.0247 -> +0.0279
- watch general 100bp: +0.0253 -> +0.0218 -> +0.0219 -> +0.0218
- hold state: +0.0109 -> +0.0225 -> +0.0286 -> +0.0224
- watch state 0bp: +0.0325 -> +0.0282 -> +0.0291 -> +0.0264
- watch state 25bp: +0.0300 -> +0.0249 -> +0.0247 -> +0.0239
- watch state 50bp: +0.0275 -> +0.0234 -> +0.0238 -> +0.0209
- watch state 100bp: +0.0225 -> +0.0224 -> +0.0215 -> +0.0214
- hold state_event: +0.0109 -> +0.0216 -> +0.0316 -> +0.0296
- watch state_event 0bp: +0.0374 -> +0.0317 -> +0.0317 -> +0.0317
- watch state_event 25bp: +0.0349 -> +0.0302 -> +0.0282 -> +0.0309
- watch state_event 50bp: +0.0324 -> +0.0286 -> +0.0300 -> +0.0300
- watch state_event 100bp: +0.0274 -> +0.0263 -> +0.0273 -> +0.0265

## Files

Per engine in its own folder (<engine>\): ledger_research.csv, ledger_execution.csv, configs.csv, daily_returns.csv, state_tables.csv, cards_setup.csv, cards_exit.csv, section.md, models.pkl. Combined here: ledger_research.csv, ledger_execution.csv, configs.csv, state_tables.csv, RUN.json, candidates.json, models.pkl.

