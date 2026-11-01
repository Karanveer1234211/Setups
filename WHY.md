# Why the engines pick what they pick (exploratory, 2020-01-01 .. 2022-12-31)

execlab v1.1 | panel panel_oc | 2026-11-01 15:34 | 241 usable panel features (label firewall applied)

Each feature is the stock's percentile among that day's panel stocks (0 lowest, 1 highest). Picks = an engine's ranks 1-3; controls = 40 random other panel stocks a day. A surrogate model of the engine, not the engine's own models: the AUC says how much of the selection the panel explains (0.5 = nothing, 1 = all); additive = every feature on its own; full = with interactions. Intervals: 95% block bootstrap over signal days.

## Engine D

2211 picks, 29480 controls. Out-of-fold AUC: additive 0.877, full 0.923 (interaction gap +0.046).

Signature (top 25 by the additive surrogate's mean |term|; * = BH q <= 0.10 that the picks' mean percentile differs from 0.5):

| feature | picks' mean percentile | top decile | bottom decile | importance | flag |
| --- | --- | --- | --- | --- | --- |
| D_ema20_angle_deg | 0.386 [0.335, 0.436] | 20% | 44% | 1.171 | * |
| D_donch_pos_50_rmean50 | 0.632 [0.588, 0.673] | 34% | 14% | 0.350 | * |
| D_vol_yz_50 | 0.755 [0.722, 0.787] | 36% | 5% | 0.287 | * |
| D_n_5pct_up_252 | 0.708 [0.673, 0.741] | 36% | 5% | 0.282 | * |
| W_ret_13w | 0.621 [0.570, 0.668] | 40% | 20% | 0.240 | * |
| D_dist_from_52wl | 0.577 [0.533, 0.620] | 21% | 15% | 0.239 | * |
| D_bb_bw_20 | 0.744 [0.706, 0.779] | 45% | 7% | 0.218 | * |
| D_sma200 | 0.323 [0.293, 0.355] | 6% | 31% | 0.164 | * |
| D_WQ_29 | 0.619 [0.583, 0.654] | 36% | 13% | 0.158 | * |
| D_WQ_16 | 0.667 [0.644, 0.687] | 22% | 4% | 0.158 | * |
| D_slope_stability | 0.391 [0.361, 0.419] | 9% | 24% | 0.149 | * |
| D_cmf20_rmean50 | 0.616 [0.584, 0.648] | 30% | 10% | 0.142 | * |
| D_realvol_ratio_20_60 | 0.439 [0.410, 0.467] | 9% | 18% | 0.134 | * |
| D_adx14 | 0.689 [0.659, 0.718] | 29% | 4% | 0.132 | * |
| D_breakout_low_20 | 0.602 [0.583, 0.622] | 20% | 0% | 0.105 | * |
| D_upside_vol_ratio | 0.579 [0.544, 0.613] | 24% | 12% | 0.099 | * |
| D_atr_pct | 0.756 [0.719, 0.790] | 39% | 6% | 0.099 | * |
| Comb_ATRhigh__EMA20neg | 0.618 [0.594, 0.641] | 14% | 0% | 0.082 | * |
| D_realvol_20 | 0.651 [0.615, 0.685] | 22% | 9% | 0.056 | * |
| D_WQ_26 | 0.562 [0.537, 0.585] | 16% | 8% | 0.048 | * |
| D_WQ_13 | 0.648 [0.625, 0.668] | 20% | 4% | 0.043 | * |
| D_atr14 | 0.376 [0.346, 0.406] | 7% | 26% | 0.041 | * |
| D_lh_run | 0.605 [0.584, 0.626] | 25% | 1% | 0.038 | * |
| D_WQ_40 | 0.590 [0.565, 0.613] | 26% | 10% | 0.033 | * |
| D_rsi14_z252 | 0.403 [0.363, 0.444] | 12% | 31% | 0.025 | * |

Interactions (Friedman's H^2 under the full surrogate; 0 = additive, 1 = purely joint):

| feature a | feature b | H^2 |
| --- | --- | --- |
| D_donch_pos_50_rmean50 | D_bb_bw_20 | 0.058 |
| D_vol_yz_50 | D_n_5pct_up_252 | 0.056 |
| D_ema20_angle_deg | W_ret_13w | 0.037 |
| D_ema20_angle_deg | D_bb_bw_20 | 0.022 |
| D_ema20_angle_deg | D_vol_yz_50 | 0.020 |
| D_vol_yz_50 | D_dist_from_52wl | 0.014 |
| W_ret_13w | D_sma200 | 0.012 |
| D_n_5pct_up_252 | D_bb_bw_20 | 0.008 |
| D_ema20_angle_deg | D_sma200 | 0.006 |
| D_vol_yz_50 | W_ret_13w | 0.006 |

## Engine ENS

2211 picks, 29480 controls. Out-of-fold AUC: additive 0.879, full 0.920 (interaction gap +0.041).

Signature (top 25 by the additive surrogate's mean |term|; * = BH q <= 0.10 that the picks' mean percentile differs from 0.5):

| feature | picks' mean percentile | top decile | bottom decile | importance | flag |
| --- | --- | --- | --- | --- | --- |
| D_ema20_angle_deg | 0.340 [0.297, 0.382] | 14% | 45% | 1.058 | * |
| D_donch_pos_50_rmean50 | 0.664 [0.623, 0.699] | 38% | 11% | 0.494 | * |
| D_dist_from_52wl | 0.600 [0.556, 0.640] | 26% | 13% | 0.388 | * |
| D_WQ_29 | 0.686 [0.656, 0.718] | 41% | 9% | 0.332 | * |
| D_adx14 | 0.682 [0.659, 0.705] | 27% | 3% | 0.297 | * |
| D_vol_yz_50 | 0.719 [0.685, 0.750] | 28% | 4% | 0.258 | * |
| D_sma200 | 0.371 [0.342, 0.401] | 7% | 27% | 0.252 | * |
| D_WQ_16 | 0.692 [0.675, 0.708] | 22% | 2% | 0.235 | * |
| D_realvol_ratio_20_60 | 0.412 [0.384, 0.440] | 8% | 20% | 0.176 | * |
| D_cmf20_rmean50 | 0.628 [0.595, 0.659] | 30% | 9% | 0.169 | * |
| D_bb_bw_20 | 0.686 [0.643, 0.729] | 37% | 9% | 0.139 | * |
| D_breakout_low_20 | 0.609 [0.591, 0.629] | 21% | 0% | 0.106 | * |
| D_ema20_angle_z252 | 0.308 [0.277, 0.339] | 7% | 38% | 0.101 | * |
| D_n_5pct_up_252 | 0.670 [0.641, 0.697] | 29% | 5% | 0.099 | * |
| D_mdi14_diff1 | 0.660 [0.644, 0.678] | 26% | 3% | 0.079 | * |
| D_lh_run | 0.640 [0.621, 0.660] | 27% | 0% | 0.063 | * |
| Comb_ATRhigh__EMA20neg | 0.623 [0.603, 0.643] | 13% | 0% | 0.063 | * |
| W_ret_13w | 0.634 [0.586, 0.676] | 37% | 17% | 0.061 | * |
| D_ema_stack_20_50_100 | 0.576 [0.557, 0.595] | 1% | 1% | 0.052 | * |
| D_amihud_20 | 0.573 [0.549, 0.597] | 16% | 4% | 0.031 | * |
| D_upside_vol_ratio | 0.571 [0.537, 0.601] | 20% | 10% | 0.022 | * |
| D_realvol_20 | 0.604 [0.565, 0.640] | 17% | 10% | 0.011 | * |
| D_WQ_12 | 0.579 [0.568, 0.591] | 14% | 6% | 0.011 | * |
| D_WQ_33 | 0.625 [0.607, 0.643] | 24% | 3% | 0.010 | * |
| D_ema20 | 0.400 [0.371, 0.430] | 8% | 23% | 0.000 | * |

Interactions (Friedman's H^2 under the full surrogate; 0 = additive, 1 = purely joint):

| feature a | feature b | H^2 |
| --- | --- | --- |
| D_vol_yz_50 | D_WQ_16 | 0.031 |
| D_ema20_angle_deg | D_WQ_29 | 0.024 |
| D_dist_from_52wl | D_vol_yz_50 | 0.018 |
| D_sma200 | D_WQ_16 | 0.016 |
| D_donch_pos_50_rmean50 | D_sma200 | 0.011 |
| D_dist_from_52wl | D_sma200 | 0.009 |
| D_ema20_angle_deg | D_dist_from_52wl | 0.009 |
| D_donch_pos_50_rmean50 | D_dist_from_52wl | 0.008 |
| D_dist_from_52wl | D_WQ_16 | 0.007 |
| D_ema20_angle_deg | D_adx14 | 0.007 |

## Files

why_features.csv (every feature's signature), why_picks.csv (every pick's top 5 drivers: feature, the pick's percentile, its log-odds term), why_pairs.csv, RUN.json.

