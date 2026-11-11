# BigMove — CONSOLIDATED SDE × stock state × volatility × frozen setups

**One consolidated research report.** Full-universe historical exploratory results, not a live strategy or OOS.
Frozen setup hash: `483f1539324f3ae5c06756b00b32c189f5eb995f73956a681673f005ce399c8f`. The code uses the original `setuplab.trigger()` and its seven unchanged setups.
Universe: 1,505 stock symbols; 1,365,771 eligible hypothetical D0 watches; cost 0.35 percentage points round-trip.

## 1. Research contract / definitions

SDE10 = (C[t]-C[t-10]) / sum(|C[j]-C[j-1]|, j=t-9..t). NEG: strictly below -0.5. POS: strictly above +0.5. Exactly +/-0.5 is MID.
Primary SDE, states, volatility and liquidity are observed **at the last COMPLETED close before each setup entry**. D0 values are separately shown; they are not interchangeable when multiple synthetic watches generate the same entry.
**Ten structural states:** 5 slow SMA50/SMA200 regimes × position above/below EMA20. States do NOT depend on SDE. Classification requires 220 daily observations; otherwise UNCLASSIFIED.
**Three additional volatility states:** simple ATR14/close compared with prior up to 252 historical sessions (minimum 60), with rolling 33rd and 67th percentile thresholds. These are RELATIVE volatility states, not absolute ATR bands.
**Trade universe slices:** point-in-time signal-close screen, price >= ₹50; ADV20 >= ₹5 crore/day; high-liquidity >=₹25 crore/day; ATR% >=3% and >=6%; above/below SMA200; >=1 ATR 10-session decline; near 52-week high. The last two are explicitly exploratory and may correlate mechanically with SDE.

### 10 structural stock states
| State | Rule |
|---|---|
| S01_BULL_ADVANCING | SMA50/SMA200 > 1.02; SMA200 rising over 20 sessions; close >= EMA20 |
| S02_BULL_PULLBACK | SMA50/SMA200 > 1.02; SMA200 rising over 20 sessions; close < EMA20 |
| S03_BULL_WEAKENING_UP | SMA50/SMA200 > 1.02; SMA200 flat/falling; close >= EMA20 |
| S04_BULL_WEAKENING_DOWN | SMA50/SMA200 > 1.02; SMA200 flat/falling; close < EMA20 |
| S05_BALANCED_UP_LEG | 0.98 <= SMA50/SMA200 <= 1.02; close >= EMA20 |
| S06_BALANCED_DOWN_LEG | 0.98 <= SMA50/SMA200 <= 1.02; close < EMA20 |
| S07_BEAR_STABILIZING_UP | SMA50/SMA200 < 0.98; SMA200 flat/rising; close >= EMA20 |
| S08_BEAR_STABILIZING_DOWN | SMA50/SMA200 < 0.98; SMA200 flat/rising; close < EMA20 |
| S09_BEAR_RALLY | SMA50/SMA200 < 0.98; SMA200 falling over 20 sessions; close >= EMA20 |
| S10_BEAR_CONTINUATION | SMA50/SMA200 < 0.98; SMA200 falling over 20 sessions; close < EMA20 |

### 3 volatility states
| Volatility state | Rule |
|---|---|
| V1_QUIET | Current ATR14% below prior 252-session 33rd percentile |
| V2_NORMAL | Current ATR14% between prior 33rd and 67th percentiles |
| V3_EXPANSION | Current ATR14% above prior 252-session 67th percentile |

## 2. Data quality and event accounting
- Independent setup events (unique stock + setup + entry): **254,914**.
- First-setup-wins events (unique stock + entry): **106,591**.
- Missing stock-state labels (first wins): **10,051**.
- Missing volatility-state labels (first wins): **3,048**.
- Missing traded-value context (first wins): **169**.

## 3. All cached setup entries: pre-entry SDE (FIRST SETUP WINS)
| sde_bucket_signal | n |
|---|---|
| MID | 68,263 |
| NEG_LT_-0.5 | 36,271 |
| POS_GT_+0.5 | 2,057 |

### SDE bucket performance (first wins)
| sde_bucket_signal | n | avg_net_pct | median_net_pct | win_pct | severe_loss_pct | severe_win_pct | avg_vs_d1_same_exit_pp | avg_d1_d5_pct | avg_atr_pct | avg_turnover_cr |
|---|---|---|---|---|---|---|---|---|---|---|
| MID | 68,263 | -0.033 | -0.426 | 45.270 | 12.822 | 13.107 | 2.072 | -2.127 | 4.077 | 74.066 |
| NEG_LT_-0.5 | 36,271 | 0.612 | 0.188 | 51.700 | 12.804 | 18.059 | 2.572 | -2.023 | 4.080 | 61.236 |
| POS_GT_+0.5 | 2,057 | -0.208 | -0.491 | 43.024 | 14.584 | 12.688 | 0.678 | -0.889 | 3.863 | 93.921 |

### SDE bucket performance (each setup independently)
| sde_bucket_signal | n | avg_net_pct | median_net_pct | win_pct | severe_loss_pct | severe_win_pct | avg_vs_d1_same_exit_pp | avg_d1_d5_pct | avg_atr_pct | avg_turnover_cr |
|---|---|---|---|---|---|---|---|---|---|---|
| MID | 161,200 | 0.151 | -0.239 | 47.181 | 10.942 | 12.909 | 3.265 | -3.131 | 4.194 | 71.386 |
| NEG_LT_-0.5 | 90,501 | 0.770 | 0.336 | 53.292 | 10.772 | 17.467 | 3.650 | -2.927 | 4.155 | 60.498 |
| POS_GT_+0.5 | 3,213 | -0.321 | -0.621 | 42.515 | 13.974 | 11.858 | 1.632 | -1.957 | 4.146 | 90.369 |

## 4. How universe filters change performance (FIRST SETUP WINS)
| universe | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct | avg_turnover_cr |
|---|---|---|---|---|---|---|
| ALL_CACHED | MID | 68,263 | -0.033 | 45.270 | 12.822 | 74.066 |
| ALL_CACHED | NEG_LT_-0.5 | 36,271 | 0.612 | 51.700 | 12.804 | 61.236 |
| ALL_CACHED | POS_GT_+0.5 | 2,057 | -0.208 | 43.024 | 14.584 | 93.921 |
| PRICE_GE_50 | MID | 62,568 | -0.018 | 45.578 | 12.574 | 77.404 |
| PRICE_GE_50 | NEG_LT_-0.5 | 32,577 | 0.578 | 51.705 | 12.610 | 64.913 |
| PRICE_GE_50 | POS_GT_+0.5 | 1,899 | -0.212 | 42.970 | 14.271 | 98.635 |
| LIQUID_5CR | MID | 47,901 | -0.032 | 45.667 | 12.302 | 100.107 |
| LIQUID_5CR | NEG_LT_-0.5 | 23,272 | 0.570 | 51.964 | 12.195 | 89.689 |
| LIQUID_5CR | POS_GT_+0.5 | 1,481 | -0.166 | 43.619 | 13.977 | 125.211 |
| LIQUID_25CR | MID | 25,498 | -0.095 | 46.043 | 12.181 | 177.370 |
| LIQUID_25CR | NEG_LT_-0.5 | 11,515 | 0.589 | 52.453 | 11.324 | 169.076 |
| LIQUID_25CR | POS_GT_+0.5 | 906 | -0.110 | 43.488 | 12.583 | 196.632 |
| LIQUID_ATR_GE_3 | MID | 35,086 | 0.111 | 47.039 | 14.080 | 79.816 |
| LIQUID_ATR_GE_3 | NEG_LT_-0.5 | 16,650 | 0.890 | 54.535 | 13.670 | 73.723 |
| LIQUID_ATR_GE_3 | POS_GT_+0.5 | 981 | -0.069 | 44.648 | 17.941 | 94.015 |
| LIQUID_ATR_GE_6 | MID | 4,539 | 0.783 | 50.606 | 18.286 | 88.333 |
| LIQUID_ATR_GE_6 | NEG_LT_-0.5 | 2,366 | 2.227 | 62.511 | 16.948 | 75.626 |
| LIQUID_ATR_GE_6 | POS_GT_+0.5 | 85 | 0.894 | 48.235 | 17.647 | 81.127 |
| LIQUID_ATR3_ABOVE_SMA200 | MID | 21,026 | -0.006 | 45.976 | 14.092 | 91.487 |
| LIQUID_ATR3_ABOVE_SMA200 | NEG_LT_-0.5 | 6,453 | 0.935 | 55.168 | 12.893 | 84.182 |
| LIQUID_ATR3_ABOVE_SMA200 | POS_GT_+0.5 | 807 | 0.039 | 45.849 | 18.092 | 100.319 |
| LIQUID_ATR3_BELOW_SMA200 | MID | 11,897 | 0.362 | 49.458 | 13.861 | 66.543 |
| LIQUID_ATR3_BELOW_SMA200 | NEG_LT_-0.5 | 9,280 | 0.885 | 54.353 | 14.170 | 70.443 |
| LIQUID_ATR3_BELOW_SMA200 | POS_GT_+0.5 | 102 | -0.644 | 41.176 | 16.667 | 83.513 |
| LIQUID_ATR3_DIP_1ATR | MID | 15,852 | 0.372 | 50.000 | 14.806 | 80.556 |
| LIQUID_ATR3_DIP_1ATR | NEG_LT_-0.5 | 16,616 | 0.899 | 54.592 | 13.637 | 73.839 |
| LIQUID_ATR3_NEAR_52W_HIGH | MID | 63 | -1.046 | 41.270 | 17.460 | 214.721 |
| LIQUID_ATR3_NEAR_52W_HIGH | POS_GT_+0.5 | 72 | -0.262 | 44.444 | 22.222 | 205.453 |
| LIQUID_ATR3_AWAY_FROM_HIGH | MID | 35,023 | 0.113 | 47.049 | 14.074 | 79.573 |
| LIQUID_ATR3_AWAY_FROM_HIGH | NEG_LT_-0.5 | 16,650 | 0.890 | 54.535 | 13.670 | 73.723 |
| LIQUID_ATR3_AWAY_FROM_HIGH | POS_GT_+0.5 | 909 | -0.054 | 44.664 | 17.602 | 85.188 |

## 5. Ten stock states × SDE (FIRST SETUP WINS)
| state_signal | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct |
|---|---|---|---|---|---|
| S01_BULL_ADVANCING | MID | 8,322 | -0.181 | 42.610 | 12.629 |
| S01_BULL_ADVANCING | NEG_LT_-0.5 | 71 | -0.895 | 40.845 | 11.268 |
| S01_BULL_ADVANCING | POS_GT_+0.5 | 1,053 | -0.234 | 43.685 | 16.049 |
| S02_BULL_PULLBACK | MID | 24,817 | 0.051 | 47.367 | 13.217 |
| S02_BULL_PULLBACK | NEG_LT_-0.5 | 14,394 | 0.870 | 54.905 | 12.311 |
| S02_BULL_PULLBACK | POS_GT_+0.5 | 6 | -4.992 | 0.000 | 50.000 |
| S03_BULL_WEAKENING_UP | MID | 526 | -0.562 | 38.973 | 13.688 |
| S03_BULL_WEAKENING_UP | POS_GT_+0.5 | 61 | 0.830 | 60.656 | 6.557 |
| S04_BULL_WEAKENING_DOWN | MID | 2,553 | -0.352 | 41.206 | 10.850 |
| S04_BULL_WEAKENING_DOWN | NEG_LT_-0.5 | 1,686 | 0.251 | 47.983 | 10.676 |
| S04_BULL_WEAKENING_DOWN | POS_GT_+0.5 | 1 | -4.362 | 0.000 | 0.000 |
| S05_BALANCED_UP_LEG | MID | 1,126 | 0.078 | 42.806 | 8.348 |
| S05_BALANCED_UP_LEG | NEG_LT_-0.5 | 4 | -3.745 | 0.000 | 25.000 |
| S05_BALANCED_UP_LEG | POS_GT_+0.5 | 183 | 0.101 | 46.995 | 11.475 |
| S06_BALANCED_DOWN_LEG | MID | 5,409 | -0.174 | 43.834 | 10.852 |
| S06_BALANCED_DOWN_LEG | NEG_LT_-0.5 | 3,842 | 0.149 | 48.256 | 11.348 |
| S06_BALANCED_DOWN_LEG | POS_GT_+0.5 | 5 | -0.005 | 40.000 | 0.000 |
| S07_BEAR_STABILIZING_UP | MID | 591 | -0.422 | 42.132 | 12.521 |
| S07_BEAR_STABILIZING_UP | NEG_LT_-0.5 | 3 | 4.688 | 66.667 | 0.000 |
| S07_BEAR_STABILIZING_UP | POS_GT_+0.5 | 96 | -0.929 | 40.625 | 18.750 |
| S08_BEAR_STABILIZING_DOWN | MID | 3,284 | 0.000 | 46.072 | 15.560 |
| S08_BEAR_STABILIZING_DOWN | NEG_LT_-0.5 | 2,442 | 0.680 | 51.392 | 14.169 |
| S09_BEAR_RALLY | MID | 2,208 | -0.213 | 41.984 | 10.598 |
| S09_BEAR_RALLY | NEG_LT_-0.5 | 22 | 1.199 | 40.909 | 13.636 |
| S09_BEAR_RALLY | POS_GT_+0.5 | 351 | -0.573 | 39.601 | 14.245 |
| S10_BEAR_CONTINUATION | MID | 12,953 | 0.128 | 46.175 | 12.746 |
| S10_BEAR_CONTINUATION | NEG_LT_-0.5 | 10,518 | 0.511 | 49.667 | 13.396 |
| S10_BEAR_CONTINUATION | POS_GT_+0.5 | 13 | 1.043 | 53.846 | 0.000 |
| UNCLASSIFIED | MID | 6,474 | -0.144 | 43.590 | 14.242 |
| UNCLASSIFIED | NEG_LT_-0.5 | 3,289 | 0.513 | 50.684 | 14.868 |
| UNCLASSIFIED | POS_GT_+0.5 | 288 | 0.207 | 39.931 | 12.153 |

## 6. Three volatility states × SDE (FIRST SETUP WINS)
| vol_state_signal | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct |
|---|---|---|---|---|---|
| V1_QUIET | MID | 20,985 | -0.482 | 41.039 | 11.537 |
| V1_QUIET | NEG_LT_-0.5 | 11,852 | -0.058 | 46.532 | 12.032 |
| V1_QUIET | POS_GT_+0.5 | 753 | -0.315 | 42.895 | 12.483 |
| V2_NORMAL | MID | 20,274 | -0.186 | 44.634 | 13.219 |
| V2_NORMAL | NEG_LT_-0.5 | 10,337 | 0.458 | 51.253 | 13.321 |
| V2_NORMAL | POS_GT_+0.5 | 611 | -0.291 | 43.535 | 14.894 |
| V3_EXPANSION | MID | 25,026 | 0.493 | 49.676 | 13.402 |
| V3_EXPANSION | NEG_LT_-0.5 | 13,119 | 1.350 | 56.811 | 12.890 |
| V3_EXPANSION | POS_GT_+0.5 | 586 | -0.096 | 43.515 | 16.894 |
| V_UNKNOWN | MID | 1,978 | -0.375 | 40.950 | 15.066 |
| V_UNKNOWN | NEG_LT_-0.5 | 963 | 0.462 | 50.467 | 15.576 |
| V_UNKNOWN | POS_GT_+0.5 | 107 | 0.403 | 38.318 | 14.953 |

## 7. Each frozen setup × pre-entry SDE (INDEPENDENT SETUP EVENTS)
| setup | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct |
|---|---|---|---|---|---|
| C1 | MID | 36,262 | 0.049 | 46.040 | 10.421 |
| C1 | NEG_LT_-0.5 | 15,303 | 0.639 | 52.604 | 9.619 |
| C1 | POS_GT_+0.5 | 498 | -0.331 | 41.968 | 12.851 |
| C2 | MID | 33,485 | 0.078 | 46.343 | 9.918 |
| C2 | NEG_LT_-0.5 | 14,477 | 0.723 | 52.974 | 9.014 |
| C2 | POS_GT_+0.5 | 435 | -0.801 | 38.621 | 15.402 |
| C3 | MID | 14,054 | 0.278 | 48.677 | 14.907 |
| C3 | NEG_LT_-0.5 | 8,736 | 0.856 | 53.663 | 13.370 |
| C3 | POS_GT_+0.5 | 813 | -0.387 | 39.729 | 15.129 |
| N1 | MID | 21,398 | 0.083 | 47.131 | 15.174 |
| N1 | NEG_LT_-0.5 | 27,591 | 0.774 | 53.057 | 13.483 |
| N1 | POS_GT_+0.5 | 6 | 5.112 | 83.333 | 0.000 |
| S1 | MID | 19,851 | 0.259 | 48.013 | 6.806 |
| S1 | NEG_LT_-0.5 | 9,956 | 0.847 | 54.118 | 6.519 |
| S1 | POS_GT_+0.5 | 155 | -1.124 | 36.129 | 14.839 |
| S2 | MID | 14,524 | 0.362 | 50.117 | 13.454 |
| S2 | NEG_LT_-0.5 | 3,975 | 0.907 | 55.296 | 14.063 |
| S2 | POS_GT_+0.5 | 885 | 0.245 | 49.492 | 12.429 |
| S3 | MID | 21,626 | 0.183 | 46.735 | 8.744 |
| S3 | NEG_LT_-0.5 | 10,463 | 0.817 | 53.503 | 8.372 |
| S3 | POS_GT_+0.5 | 421 | -0.655 | 39.667 | 14.727 |

## 8. 10 × 3 state-volatility grid (FIRST SETUP WINS)
| state_signal | vol_state_signal | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct |
|---|---|---|---|---|---|---|
| S01_BULL_ADVANCING | V1_QUIET | MID | 2,074 | -0.073 | 43.394 | 10.174 |
| S01_BULL_ADVANCING | V1_QUIET | NEG_LT_-0.5 | 12 | -1.737 | 25.000 | 8.333 |
| S01_BULL_ADVANCING | V1_QUIET | POS_GT_+0.5 | 394 | -0.203 | 43.655 | 13.452 |
| S01_BULL_ADVANCING | V2_NORMAL | MID | 2,549 | -0.395 | 40.761 | 13.103 |
| S01_BULL_ADVANCING | V2_NORMAL | NEG_LT_-0.5 | 9 | -2.087 | 55.556 | 33.333 |
| S01_BULL_ADVANCING | V2_NORMAL | POS_GT_+0.5 | 336 | -0.348 | 45.833 | 16.369 |
| S01_BULL_ADVANCING | V3_EXPANSION | MID | 3,699 | -0.094 | 43.444 | 13.679 |
| S01_BULL_ADVANCING | V3_EXPANSION | NEG_LT_-0.5 | 50 | -0.478 | 42.000 | 8.000 |
| S01_BULL_ADVANCING | V3_EXPANSION | POS_GT_+0.5 | 323 | -0.154 | 41.486 | 18.885 |
| S02_BULL_PULLBACK | V1_QUIET | MID | 6,905 | -0.462 | 42.766 | 12.223 |
| S02_BULL_PULLBACK | V1_QUIET | NEG_LT_-0.5 | 4,038 | 0.190 | 49.554 | 11.342 |
| S02_BULL_PULLBACK | V1_QUIET | POS_GT_+0.5 | 2 | -3.688 | 0.000 | 50.000 |
| S02_BULL_PULLBACK | V2_NORMAL | MID | 7,863 | -0.095 | 46.738 | 13.188 |
| S02_BULL_PULLBACK | V2_NORMAL | NEG_LT_-0.5 | 4,210 | 0.631 | 53.658 | 12.660 |
| S02_BULL_PULLBACK | V2_NORMAL | POS_GT_+0.5 | 1 | -10.498 | 0.000 | 100.000 |
| S02_BULL_PULLBACK | V3_EXPANSION | MID | 10,049 | 0.518 | 51.020 | 13.922 |
| S02_BULL_PULLBACK | V3_EXPANSION | NEG_LT_-0.5 | 6,146 | 1.480 | 59.274 | 12.707 |
| S02_BULL_PULLBACK | V3_EXPANSION | POS_GT_+0.5 | 3 | -4.025 | 0.000 | 33.333 |
| S03_BULL_WEAKENING_UP | V1_QUIET | MID | 198 | -0.501 | 38.384 | 11.111 |
| S03_BULL_WEAKENING_UP | V1_QUIET | POS_GT_+0.5 | 27 | 0.053 | 59.259 | 11.111 |
| S03_BULL_WEAKENING_UP | V2_NORMAL | MID | 183 | -0.701 | 40.984 | 13.115 |
| S03_BULL_WEAKENING_UP | V2_NORMAL | POS_GT_+0.5 | 22 | 2.581 | 63.636 | 0.000 |
| S03_BULL_WEAKENING_UP | V3_EXPANSION | MID | 145 | -0.469 | 37.241 | 17.931 |
| S03_BULL_WEAKENING_UP | V3_EXPANSION | POS_GT_+0.5 | 12 | -0.631 | 58.333 | 8.333 |
| S04_BULL_WEAKENING_DOWN | V1_QUIET | MID | 1,279 | -0.562 | 39.171 | 9.304 |
| S04_BULL_WEAKENING_DOWN | V1_QUIET | NEG_LT_-0.5 | 807 | -0.213 | 43.990 | 10.781 |
| S04_BULL_WEAKENING_DOWN | V2_NORMAL | MID | 717 | -0.270 | 42.538 | 11.018 |
| S04_BULL_WEAKENING_DOWN | V2_NORMAL | NEG_LT_-0.5 | 489 | 0.475 | 51.534 | 10.634 |
| S04_BULL_WEAKENING_DOWN | V2_NORMAL | POS_GT_+0.5 | 1 | -4.362 | 0.000 | 0.000 |
| S04_BULL_WEAKENING_DOWN | V3_EXPANSION | MID | 557 | 0.022 | 44.165 | 14.183 |
| S04_BULL_WEAKENING_DOWN | V3_EXPANSION | NEG_LT_-0.5 | 390 | 0.929 | 51.795 | 10.513 |
| S05_BALANCED_UP_LEG | V1_QUIET | MID | 403 | -0.425 | 39.206 | 8.933 |
| S05_BALANCED_UP_LEG | V1_QUIET | NEG_LT_-0.5 | 2 | -0.703 | 0.000 | 0.000 |
| S05_BALANCED_UP_LEG | V1_QUIET | POS_GT_+0.5 | 84 | 0.548 | 52.381 | 7.143 |
| S05_BALANCED_UP_LEG | V2_NORMAL | MID | 339 | 0.053 | 42.773 | 8.850 |
| S05_BALANCED_UP_LEG | V2_NORMAL | POS_GT_+0.5 | 53 | -0.615 | 35.849 | 13.208 |
| S05_BALANCED_UP_LEG | V3_EXPANSION | MID | 384 | 0.627 | 46.615 | 7.292 |
| S05_BALANCED_UP_LEG | V3_EXPANSION | NEG_LT_-0.5 | 2 | -6.786 | 0.000 | 50.000 |
| S05_BALANCED_UP_LEG | V3_EXPANSION | POS_GT_+0.5 | 46 | 0.112 | 50.000 | 17.391 |
| S06_BALANCED_DOWN_LEG | V1_QUIET | MID | 2,290 | -0.575 | 39.956 | 10.393 |
| S06_BALANCED_DOWN_LEG | V1_QUIET | NEG_LT_-0.5 | 1,651 | -0.415 | 44.579 | 12.538 |
| S06_BALANCED_DOWN_LEG | V1_QUIET | POS_GT_+0.5 | 1 | -1.876 | 0.000 | 0.000 |
| S06_BALANCED_DOWN_LEG | V2_NORMAL | MID | 1,628 | -0.213 | 43.120 | 11.609 |
| S06_BALANCED_DOWN_LEG | V2_NORMAL | NEG_LT_-0.5 | 1,097 | 0.159 | 48.131 | 11.121 |
| S06_BALANCED_DOWN_LEG | V2_NORMAL | POS_GT_+0.5 | 3 | 0.762 | 66.667 | 0.000 |
| S06_BALANCED_DOWN_LEG | V3_EXPANSION | MID | 1,491 | 0.486 | 50.570 | 10.731 |
| S06_BALANCED_DOWN_LEG | V3_EXPANSION | NEG_LT_-0.5 | 1,094 | 0.989 | 53.931 | 9.781 |
| S06_BALANCED_DOWN_LEG | V3_EXPANSION | POS_GT_+0.5 | 1 | -0.436 | 0.000 | 0.000 |
| S07_BEAR_STABILIZING_UP | V1_QUIET | MID | 184 | -0.457 | 40.761 | 11.413 |
| S07_BEAR_STABILIZING_UP | V1_QUIET | POS_GT_+0.5 | 42 | -0.862 | 35.714 | 16.667 |
| S07_BEAR_STABILIZING_UP | V2_NORMAL | MID | 208 | -0.549 | 44.231 | 14.423 |
| S07_BEAR_STABILIZING_UP | V2_NORMAL | NEG_LT_-0.5 | 1 | -1.287 | 0.000 | 0.000 |
| S07_BEAR_STABILIZING_UP | V2_NORMAL | POS_GT_+0.5 | 31 | -1.933 | 35.484 | 25.806 |
| S07_BEAR_STABILIZING_UP | V3_EXPANSION | MID | 199 | -0.256 | 41.206 | 11.558 |
| S07_BEAR_STABILIZING_UP | V3_EXPANSION | NEG_LT_-0.5 | 2 | 7.675 | 100.000 | 0.000 |
| S07_BEAR_STABILIZING_UP | V3_EXPANSION | POS_GT_+0.5 | 23 | 0.299 | 56.522 | 13.043 |
| S08_BEAR_STABILIZING_DOWN | V1_QUIET | MID | 1,004 | -0.935 | 38.347 | 16.036 |
| S08_BEAR_STABILIZING_DOWN | V1_QUIET | NEG_LT_-0.5 | 813 | -0.002 | 45.756 | 15.006 |
| S08_BEAR_STABILIZING_DOWN | V2_NORMAL | MID | 1,081 | -0.131 | 46.161 | 16.744 |
| S08_BEAR_STABILIZING_DOWN | V2_NORMAL | NEG_LT_-0.5 | 794 | 0.655 | 52.519 | 13.728 |
| S08_BEAR_STABILIZING_DOWN | V3_EXPANSION | MID | 1,199 | 0.902 | 52.460 | 14.095 |
| S08_BEAR_STABILIZING_DOWN | V3_EXPANSION | NEG_LT_-0.5 | 835 | 1.369 | 55.808 | 13.772 |
| S09_BEAR_RALLY | V1_QUIET | MID | 744 | -0.238 | 43.011 | 9.677 |
| S09_BEAR_RALLY | V1_QUIET | NEG_LT_-0.5 | 4 | 2.804 | 50.000 | 0.000 |
| S09_BEAR_RALLY | V1_QUIET | POS_GT_+0.5 | 139 | -0.816 | 37.410 | 11.511 |
| S09_BEAR_RALLY | V2_NORMAL | MID | 662 | -0.031 | 43.807 | 9.970 |
| S09_BEAR_RALLY | V2_NORMAL | NEG_LT_-0.5 | 8 | -0.702 | 37.500 | 12.500 |
| S09_BEAR_RALLY | V2_NORMAL | POS_GT_+0.5 | 104 | 0.024 | 41.346 | 12.500 |
| S09_BEAR_RALLY | V3_EXPANSION | MID | 802 | -0.340 | 39.526 | 11.970 |
| S09_BEAR_RALLY | V3_EXPANSION | NEG_LT_-0.5 | 10 | 2.078 | 40.000 | 20.000 |
| S09_BEAR_RALLY | V3_EXPANSION | POS_GT_+0.5 | 108 | -0.835 | 40.741 | 19.444 |
| S10_BEAR_CONTINUATION | V1_QUIET | MID | 4,449 | -0.637 | 38.705 | 11.598 |
| S10_BEAR_CONTINUATION | V1_QUIET | NEG_LT_-0.5 | 3,789 | -0.106 | 45.051 | 11.982 |
| S10_BEAR_CONTINUATION | V1_QUIET | POS_GT_+0.5 | 2 | -1.770 | 0.000 | 0.000 |
| S10_BEAR_CONTINUATION | V2_NORMAL | MID | 3,711 | -0.270 | 44.112 | 14.093 |
| S10_BEAR_CONTINUATION | V2_NORMAL | NEG_LT_-0.5 | 3,092 | 0.341 | 49.191 | 14.618 |
| S10_BEAR_CONTINUATION | V2_NORMAL | POS_GT_+0.5 | 2 | -1.176 | 50.000 | 0.000 |
| S10_BEAR_CONTINUATION | V3_EXPANSION | MID | 4,793 | 1.145 | 54.705 | 12.769 |
| S10_BEAR_CONTINUATION | V3_EXPANSION | NEG_LT_-0.5 | 3,637 | 1.298 | 54.880 | 13.830 |
| S10_BEAR_CONTINUATION | V3_EXPANSION | POS_GT_+0.5 | 9 | 2.162 | 66.667 | 0.000 |
| UNCLASSIFIED | V1_QUIET | MID | 1,455 | -0.294 | 41.718 | 12.440 |
| UNCLASSIFIED | V1_QUIET | NEG_LT_-0.5 | 736 | -0.252 | 46.060 | 13.179 |
| UNCLASSIFIED | V1_QUIET | POS_GT_+0.5 | 62 | -0.688 | 38.710 | 12.903 |
| UNCLASSIFIED | V2_NORMAL | MID | 1,333 | -0.063 | 44.261 | 14.029 |
| UNCLASSIFIED | V2_NORMAL | NEG_LT_-0.5 | 637 | 0.194 | 49.137 | 16.484 |
| UNCLASSIFIED | V2_NORMAL | POS_GT_+0.5 | 58 | -0.226 | 37.931 | 12.069 |
| UNCLASSIFIED | V3_EXPANSION | MID | 1,708 | 0.186 | 47.717 | 14.988 |
| UNCLASSIFIED | V3_EXPANSION | NEG_LT_-0.5 | 953 | 1.369 | 55.509 | 14.376 |
| UNCLASSIFIED | V3_EXPANSION | POS_GT_+0.5 | 61 | 1.184 | 45.902 | 6.557 |
| UNCLASSIFIED | V_UNKNOWN | MID | 1,978 | -0.375 | 40.950 | 15.066 |
| UNCLASSIFIED | V_UNKNOWN | NEG_LT_-0.5 | 963 | 0.462 | 50.467 | 15.576 |
| UNCLASSIFIED | V_UNKNOWN | POS_GT_+0.5 | 107 | 0.403 | 38.318 | 14.953 |

## 9. Strongest conditional cells (minimum 100 distinct events per NEG and MID group)
CAUTION: these are retrospective rankings among many cells; **not** tuned rules or independent confirmation.
| universe | state_signal | vol_state_signal | n_NEG_LT_-0.5 | n_MID | lift_neg_vs_mid_pp |
|---|---|---|---|---|---|
| LIQUID_ATR_GE_6 | UNCLASSIFIED | V3_EXPANSION | 149.000 | 347.000 | +1.629 |
| LIQUID_25CR | UNCLASSIFIED | V3_EXPANSION | 119.000 | 262.000 | +1.600 |
| LIQUID_ATR3_BELOW_SMA200 | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 202.000 | 289.000 | +1.326 |
| LIQUID_ATR_GE_6 | S02_BULL_PULLBACK | V3_EXPANSION | 1412.000 | 1897.000 | +1.290 |
| LIQUID_ATR3_AWAY_FROM_HIGH | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 204.000 | 294.000 | +1.265 |
| LIQUID_ATR_GE_3 | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 204.000 | 294.000 | +1.265 |
| LIQUID_ATR3_DIP_1ATR | S04_BULL_WEAKENING_DOWN | V2_NORMAL | 204.000 | 182.000 | +1.256 |
| PRICE_GE_50 | UNCLASSIFIED | V3_EXPANSION | 779.000 | 1473.000 | +1.250 |
| LIQUID_25CR | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 162.000 | 220.000 | +1.216 |
| ALL_CACHED | UNCLASSIFIED | V3_EXPANSION | 953.000 | 1708.000 | +1.183 |
| LIQUID_ATR3_ABOVE_SMA200 | S02_BULL_PULLBACK | V1_QUIET | 1005.000 | 2175.000 | +1.100 |
| LIQUID_25CR | S08_BEAR_STABILIZING_DOWN | V2_NORMAL | 234.000 | 357.000 | +1.092 |
| LIQUID_ATR3_DIP_1ATR | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 204.000 | 181.000 | +1.071 |
| LIQUID_ATR_GE_3 | S06_BALANCED_DOWN_LEG | V2_NORMAL | 442.000 | 722.000 | +1.061 |
| LIQUID_ATR3_AWAY_FROM_HIGH | S06_BALANCED_DOWN_LEG | V2_NORMAL | 442.000 | 722.000 | +1.061 |
| LIQUID_ATR3_BELOW_SMA200 | S04_BULL_WEAKENING_DOWN | V3_EXPANSION | 165.000 | 162.000 | +1.055 |
| LIQUID_ATR_GE_3 | S02_BULL_PULLBACK | V1_QUIET | 1343.000 | 2505.000 | +1.039 |
| LIQUID_ATR3_AWAY_FROM_HIGH | S02_BULL_PULLBACK | V1_QUIET | 1343.000 | 2505.000 | +1.039 |
| LIQUID_ATR3_DIP_1ATR | S02_BULL_PULLBACK | V1_QUIET | 1339.000 | 1347.000 | +1.027 |
| LIQUID_ATR3_BELOW_SMA200 | S02_BULL_PULLBACK | V2_NORMAL | 643.000 | 549.000 | +1.000 |
| LIQUID_ATR3_ABOVE_SMA200 | S02_BULL_PULLBACK | V3_EXPANSION | 3224.000 | 6683.000 | +0.967 |
| ALL_CACHED | S02_BULL_PULLBACK | V3_EXPANSION | 6146.000 | 10049.000 | +0.963 |
| LIQUID_ATR3_AWAY_FROM_HIGH | S02_BULL_PULLBACK | V3_EXPANSION | 4689.000 | 7833.000 | +0.959 |
| LIQUID_ATR_GE_3 | S02_BULL_PULLBACK | V3_EXPANSION | 4689.000 | 7833.000 | +0.959 |
| LIQUID_ATR_GE_3 | S04_BULL_WEAKENING_DOWN | V3_EXPANSION | 238.000 | 348.000 | +0.947 |
| LIQUID_ATR3_AWAY_FROM_HIGH | S04_BULL_WEAKENING_DOWN | V3_EXPANSION | 238.000 | 348.000 | +0.947 |
| ALL_CACHED | S08_BEAR_STABILIZING_DOWN | V1_QUIET | 813.000 | 1004.000 | +0.934 |
| LIQUID_ATR_GE_3 | UNCLASSIFIED | V3_EXPANSION | 396.000 | 885.000 | +0.929 |
| LIQUID_ATR3_AWAY_FROM_HIGH | UNCLASSIFIED | V3_EXPANSION | 396.000 | 885.000 | +0.929 |
| LIQUID_5CR | UNCLASSIFIED | V3_EXPANSION | 414.000 | 922.000 | +0.925 |
| ALL_CACHED | S04_BULL_WEAKENING_DOWN | V3_EXPANSION | 390.000 | 557.000 | +0.908 |
| PRICE_GE_50 | S02_BULL_PULLBACK | V3_EXPANSION | 5712.000 | 9480.000 | +0.905 |
| LIQUID_25CR | S10_BEAR_CONTINUATION | V2_NORMAL | 735.000 | 1024.000 | +0.901 |
| LIQUID_5CR | S02_BULL_PULLBACK | V3_EXPANSION | 5033.000 | 8561.000 | +0.880 |
| LIQUID_ATR3_DIP_1ATR | UNCLASSIFIED | V3_EXPANSION | 396.000 | 344.000 | +0.846 |

## 10. Same-date controls (first wins; compare only dates with both SDE groups)
| universe | scope | comparison | matched_cells | matched_weeks | mean_daily_diff_pp | ci95_lo | ci95_hi |
|---|---|---|---|---|---|---|---|
| ALL_CACHED | ENTRY_DAY | NEG_vs_MID | 1,202 | 298 | +0.174 | -0.014 | 0.368 |
| ALL_CACHED | ENTRY_DAY | NEG_vs_POS | 274 | 268 | -0.546 | -0.973 | -0.059 |
| ALL_CACHED | ENTRY_DAY_SETUP | NEG_vs_MID | 2,531 | 297 | +0.233 | 0.098 | 0.363 |
| ALL_CACHED | ENTRY_DAY_SETUP | NEG_vs_POS | 611 | 261 | -0.234 | -0.655 | 0.170 |
| PRICE_GE_50 | ENTRY_DAY | NEG_vs_MID | 1,182 | 297 | +0.114 | -0.074 | 0.315 |
| PRICE_GE_50 | ENTRY_DAY | NEG_vs_POS | 267 | 264 | -0.313 | -0.757 | 0.105 |
| PRICE_GE_50 | ENTRY_DAY_SETUP | NEG_vs_MID | 2,469 | 297 | +0.195 | 0.063 | 0.326 |
| PRICE_GE_50 | ENTRY_DAY_SETUP | NEG_vs_POS | 573 | 257 | -0.161 | -0.561 | 0.248 |
| LIQUID_5CR | ENTRY_DAY | NEG_vs_MID | 1,114 | 296 | +0.197 | -0.004 | 0.403 |
| LIQUID_5CR | ENTRY_DAY | NEG_vs_POS | 241 | 241 | -0.220 | -0.699 | 0.251 |
| LIQUID_5CR | ENTRY_DAY_SETUP | NEG_vs_MID | 2,289 | 296 | +0.221 | 0.084 | 0.372 |
| LIQUID_5CR | ENTRY_DAY_SETUP | NEG_vs_POS | 462 | 237 | -0.140 | -0.605 | 0.385 |
| LIQUID_25CR | ENTRY_DAY | NEG_vs_MID | 914 | 290 | +0.277 | 0.011 | 0.541 |
| LIQUID_25CR | ENTRY_DAY | NEG_vs_POS | 201 | 201 | -0.180 | -0.831 | 0.580 |
| LIQUID_25CR | ENTRY_DAY_SETUP | NEG_vs_MID | 1,751 | 290 | +0.375 | 0.168 | 0.577 |
| LIQUID_25CR | ENTRY_DAY_SETUP | NEG_vs_POS | 275 | 181 | -0.207 | -0.966 | 0.642 |
| LIQUID_ATR_GE_3 | ENTRY_DAY | NEG_vs_MID | 987 | 296 | +0.377 | 0.133 | 0.637 |
| LIQUID_ATR_GE_3 | ENTRY_DAY | NEG_vs_POS | 223 | 223 | -0.087 | -0.657 | 0.505 |
| LIQUID_ATR_GE_3 | ENTRY_DAY_SETUP | NEG_vs_MID | 2,014 | 295 | +0.291 | 0.112 | 0.470 |
| LIQUID_ATR_GE_3 | ENTRY_DAY_SETUP | NEG_vs_POS | 362 | 209 | +0.056 | -0.572 | 0.700 |
| LIQUID_ATR_GE_6 | ENTRY_DAY | NEG_vs_MID | 324 | 206 | +0.287 | -0.330 | 0.934 |
| LIQUID_ATR_GE_6 | ENTRY_DAY | NEG_vs_POS | 37 | 37 | -1.281 | -4.263 | 1.735 |
| LIQUID_ATR_GE_6 | ENTRY_DAY_SETUP | NEG_vs_MID | 541 | 183 | +0.711 | 0.098 | 1.345 |
| LIQUID_ATR_GE_6 | ENTRY_DAY_SETUP | NEG_vs_POS | 20 | 20 | -1.895 | -4.932 | 0.952 |
| LIQUID_ATR3_ABOVE_SMA200 | ENTRY_DAY | NEG_vs_MID | 733 | 276 | +0.591 | 0.260 | 0.924 |
| LIQUID_ATR3_ABOVE_SMA200 | ENTRY_DAY | NEG_vs_POS | 196 | 196 | -0.103 | -0.766 | 0.542 |
| LIQUID_ATR3_ABOVE_SMA200 | ENTRY_DAY_SETUP | NEG_vs_MID | 1,442 | 275 | +0.460 | 0.211 | 0.700 |
| LIQUID_ATR3_ABOVE_SMA200 | ENTRY_DAY_SETUP | NEG_vs_POS | 257 | 170 | +0.335 | -0.447 | 1.120 |
| LIQUID_ATR3_BELOW_SMA200 | ENTRY_DAY | NEG_vs_MID | 718 | 275 | +0.071 | -0.223 | 0.357 |
| LIQUID_ATR3_BELOW_SMA200 | ENTRY_DAY | NEG_vs_POS | 47 | 47 | +0.093 | -1.221 | 1.339 |
| LIQUID_ATR3_BELOW_SMA200 | ENTRY_DAY_SETUP | NEG_vs_MID | 1,261 | 259 | +0.178 | -0.094 | 0.451 |
| LIQUID_ATR3_BELOW_SMA200 | ENTRY_DAY_SETUP | NEG_vs_POS | 38 | 33 | +0.779 | -0.757 | 2.423 |
| LIQUID_ATR3_DIP_1ATR | ENTRY_DAY | NEG_vs_MID | 966 | 295 | +0.431 | 0.173 | 0.701 |
| LIQUID_ATR3_DIP_1ATR | ENTRY_DAY | NEG_vs_POS | 0 | — | — | — | — |
| LIQUID_ATR3_DIP_1ATR | ENTRY_DAY_SETUP | NEG_vs_MID | 1,872 | 292 | +0.287 | 0.097 | 0.504 |
| LIQUID_ATR3_DIP_1ATR | ENTRY_DAY_SETUP | NEG_vs_POS | 0 | — | — | — | — |
| LIQUID_ATR3_NEAR_52W_HIGH | ENTRY_DAY | NEG_vs_MID | 0 | — | — | — | — |
| LIQUID_ATR3_NEAR_52W_HIGH | ENTRY_DAY | NEG_vs_POS | 0 | — | — | — | — |
| LIQUID_ATR3_NEAR_52W_HIGH | ENTRY_DAY_SETUP | NEG_vs_MID | 0 | — | — | — | — |
| LIQUID_ATR3_NEAR_52W_HIGH | ENTRY_DAY_SETUP | NEG_vs_POS | 0 | — | — | — | — |
| LIQUID_ATR3_AWAY_FROM_HIGH | ENTRY_DAY | NEG_vs_MID | 987 | 296 | +0.376 | 0.133 | 0.637 |
| LIQUID_ATR3_AWAY_FROM_HIGH | ENTRY_DAY | NEG_vs_POS | 215 | 215 | -0.121 | -0.658 | 0.479 |
| LIQUID_ATR3_AWAY_FROM_HIGH | ENTRY_DAY_SETUP | NEG_vs_MID | 2,014 | 295 | +0.290 | 0.112 | 0.470 |
| LIQUID_ATR3_AWAY_FROM_HIGH | ENTRY_DAY_SETUP | NEG_vs_POS | 345 | 199 | -0.002 | -0.625 | 0.627 |

## 11. Year-by-year stability (first wins; pre-entry SDE)
| year | sde_bucket_signal | n | avg_net_pct | win_pct | severe_loss_pct |
|---|---|---|---|---|---|
| 2021.000 | MID | 9,938 | -0.006 | 45.230 | 12.306 |
| 2021.000 | NEG_LT_-0.5 | 4,376 | 0.799 | 53.451 | 10.878 |
| 2021.000 | POS_GT_+0.5 | 352 | -0.443 | 40.625 | 20.455 |
| 2022.000 | MID | 9,753 | -0.322 | 43.945 | 16.067 |
| 2022.000 | NEG_LT_-0.5 | 6,921 | 0.603 | 53.128 | 16.833 |
| 2022.000 | POS_GT_+0.5 | 342 | -0.370 | 41.520 | 14.620 |
| 2023.000 | MID | 9,392 | 0.102 | 46.167 | 8.092 |
| 2023.000 | NEG_LT_-0.5 | 4,044 | 0.578 | 51.805 | 10.089 |
| 2023.000 | POS_GT_+0.5 | 340 | 0.625 | 53.529 | 9.118 |
| 2024.000 | MID | 14,426 | -0.027 | 44.136 | 13.857 |
| 2024.000 | NEG_LT_-0.5 | 7,357 | 1.080 | 54.492 | 11.445 |
| 2024.000 | POS_GT_+0.5 | 418 | -0.507 | 39.713 | 16.986 |
| 2025.000 | MID | 13,753 | 0.202 | 49.182 | 12.775 |
| 2025.000 | NEG_LT_-0.5 | 7,362 | 0.761 | 53.301 | 11.478 |
| 2025.000 | POS_GT_+0.5 | 297 | -0.012 | 46.465 | 9.091 |
| 2026.000 | MID | 11,001 | -0.221 | 42.314 | 13.153 |
| 2026.000 | NEG_LT_-0.5 | 6,211 | -0.217 | 43.600 | 14.619 |
| 2026.000 | POS_GT_+0.5 | 308 | -0.464 | 37.013 | 15.909 |

## 12. Entry-time versus D0 and overlap limitations
The report always distinguishes pre-entry SDE/state from D0 SDE/state. Consecutive D0 windows share future returns. A unique stock-entry event is not automatically an independent investment opportunity. Independent setup events can overlap when multiple rules trigger on the same stock and date.
Only first-trigger unique events are closest to an event-level strategy; even those ignore capital occupancy, fees beyond 35bp, fills, price limits and delisting/survivorship bias. Same-date comparisons reduce date confounding but do not establish causality or remove stock dependencies.
The 2021–2026 period has already been mined for frozen setups and SDE. Conditioning on past studies introduces multiple-testing bias. A genuinely independent prospective sample is needed before using any state/SDE interaction to trade.

## 13. Full-case files and how to read the CONSO
`CONSO_REPORT.html` is the **single self-contained consolidated report** with full filterable tables and charts. The complete 7-setup × 10-state × 3-volatility × 3-SDE grid is in `independent_setups_ALL_CASES.csv` and `first_setup_wins_ALL_CASES.csv` for each universe. The same cells by year appear in `*_ALL_CASES_BY_YEAR.csv`; all individual records are in `*_UNIQUE_EVENTS_WITH_STATES.csv`.

**No frozen code, production data, or portfolio rules were modified.**
