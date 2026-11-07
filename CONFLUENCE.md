# setuplab - setups x logical confluences (setuplab v0.3)

Pool: NONE, B, A+B, d_wq_33_change<0&d_ema20_angle_deg_change<0, d_ema20_angle_deg_change<0&d_rsi14_obv_x_change>0, d_wq_33_change>0&w_ret_13w_change<0, d_ema20_angle_deg_change<0&d_mdi14_diff1_change<0, d_rsi14_obv_x_change<0&w_ret_13w_change<0, d_mdi14_diff1_change>0&w_ret_13w_change<0, d_bb_bw_20_change>0&w_ret_13w_change<0, d_wq_12_change<0&d_ema20_angle_deg_change<0, d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0, d_cmf20_rmean50_change<0&d_donch_pos_50_rmean50_change<0, d_cmf20_rmean50_change<0&w_ret_13w_change<0, d_bb_bw_20_change>0&d_donch_pos_50_rmean50_change<0, d_cmf20_rmean50_change<0&d_ema20_angle_deg_change<0.

Confluences (declared before the run): price DIP1, DIP2, DIP3, DIPATR1, GREEN, UPCLOSE, GAPDOWN, GAPUP; context BEARSTATE, BULLSTATE, NIFTY_ABOVE_MA50, NIFTY_BELOW_MA50, MKT_BULLISH, MKT_BEARISH, VIX_LOW, VIX_HIGH, BREADTH_WEAK, NOT_OVEREXT, VOL_ELEVATED; and every price x context pair.

Each row: the combination's own trades vs the model's D1 entry on the same ids; 'adds' = the same combination vs the confluence ALONE on the same ids (what the indicator setup adds); years = signal years with net per trade above 0. Net % after 0.35 pp; 95% block bootstrap over signal days. Exploratory: 1712 combinations on the history the setups came from - expect some to look good by chance.

## original_d5 exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 154 | +3.0393 | -7.0586 | +10.0978 [+9.0977, +11.0254] | +1.2757 [+0.5801, +1.9660] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 270 | +2.7186 | -0.1472 | +2.8658 [+1.8833, +3.7975] | +2.0873 [+1.3030, +2.9391] | 5/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 163 | +2.7029 | -5.6277 | +8.3306 [+7.1636, +9.4719] | +1.2740 [+0.6894, +1.8348] | 7/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 202 | +2.6677 | -0.2503 | +2.9180 [+2.1472, +3.6106] | +2.1455 [+1.4975, +2.8094] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 325 | +2.6053 | -0.3028 | +2.9081 [+1.9505, +3.7853] | +2.0170 [+1.2807, +2.8255] | 7/7 |
| A+B | DIP3&BEARSTATE | 247 | +2.5673 | -5.3854 | +7.9527 [+7.2004, +8.7206] | +1.9170 [+1.3754, +2.4964] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 412 | +2.5158 | -0.3502 | +2.8660 [+2.0694, +3.5952] | +2.2946 [+1.6958, +2.9535] | 7/7 |
| A+B | DIP2&BEARSTATE | 276 | +2.4996 | -4.7977 | +7.2974 [+6.5535, +8.0535] | +2.2853 [+1.7658, +2.8264] | 6/7 |
| A+B | GAPDOWN&VIX_LOW | 205 | +2.4953 | -1.5470 | +4.0424 [+3.0180, +5.0965] | +3.1056 [+2.1453, +4.1083] | 7/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 189 | +2.4928 | -0.8624 | +3.3552 [+2.4546, +4.1485] | +2.4426 [+1.6960, +3.1316] | 5/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | GAPDOWN&VIX_LOW | 279 | +2.4735 | -0.6374 | +3.1109 [+2.1550, +4.0009] | +2.1746 [+1.3371, +3.0206] | 6/7 |
| B | DIP3&BEARSTATE | 289 | +2.4615 | -5.1509 | +7.6124 [+6.9444, +8.2747] | +1.7724 [+1.2930, +2.2872] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VIX_LOW | 351 | +2.4590 | -0.4789 | +2.9378 [+2.1184, +3.7291] | +2.0890 [+1.3341, +2.8645] | 7/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&BREADTH_WEAK | 195 | +2.4479 | -7.4237 | +9.8716 [+8.9463, +10.7829] | +1.3338 [+0.7919, +1.8601] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 369 | +2.4473 | -0.4130 | +2.8603 [+2.0570, +3.6071] | +2.2371 [+1.5943, +2.9163] | 5/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 221 | +2.4342 | -0.2688 | +2.7030 [+1.7112, +3.6345] | +2.1401 [+1.4008, +2.9723] | 7/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | MKT_BEARISH | 393 | +2.4317 | +1.0926 | +1.3391 [+0.4321, +2.1234] | +1.3391 [+0.4321, +2.1234] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIP3&NIFTY_BELOW_MA50 | 173 | +2.4317 | -5.0961 | +7.5278 [+6.7715, +8.2528] | +1.7614 [+1.2268, +2.2977] | 6/7 |
| A+B | GAPDOWN&BEARSTATE | 258 | +2.4281 | -2.1431 | +4.5712 [+3.8058, +5.3432] | +3.5353 [+2.8374, +4.3044] | 6/7 |
| A+B | GAPDOWN&VOL_ELEVATED | 212 | +2.4261 | -1.9491 | +4.3752 [+3.5511, +5.2170] | +3.6051 [+2.7916, +4.4733] | 5/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 341 | +2.4220 | -1.1745 | +3.5965 [+2.8211, +4.3551] | +2.6194 [+1.9394, +3.3955] | 7/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VIX_LOW | 286 | +2.3924 | -0.1102 | +2.5025 [+1.5951, +3.3643] | +1.6242 [+0.8808, +2.3673] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIP3&BEARSTATE | 182 | +2.3899 | -4.0977 | +6.4876 [+5.7343, +7.1969] | +1.0912 [+0.5610, +1.6504] | 6/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 279 | +2.3734 | -1.0085 | +3.3819 [+2.5686, +4.1614] | +2.6932 [+1.9272, +3.5031] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | MKT_BEARISH | 405 | +2.3239 | +1.1535 | +1.1704 [+0.3403, +1.9930] | +1.1704 [+0.3403, +1.9930] | 7/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| VIX_HIGH | 2498 | +1.5745 | +1.5745 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| VOL_ELEVATED | 1777 | +1.5111 | +1.5111 | +0.0000 [+0.0000, +0.0000] | 5/7 |
| BEARSTATE | 1667 | +1.4673 | +1.4673 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| BREADTH_WEAK | 2480 | +1.3670 | +1.3670 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| GAPDOWN&VOL_ELEVATED | 1349 | +1.3474 | +0.9933 | +0.3541 [-0.0031, +0.7020] | 6/7 |
| GAPDOWN&BEARSTATE | 1261 | +1.3285 | +1.0427 | +0.2858 [-0.1065, +0.6363] | 7/7 |
| DIPATR1&VOL_ELEVATED | 372 | +1.3206 | -8.0759 | +9.3965 [+8.5594, +10.3812] | 5/7 |
| GAPUP&VIX_HIGH | 2433 | +1.2710 | +1.8803 | -0.6094 [-0.7876, -0.4406] | 6/7 |
| DIP2&BEARSTATE | 862 | +1.2498 | -3.2009 | +4.4507 [+4.1084, +4.8050] | 6/7 |
| DIP3&BEARSTATE | 730 | +1.2313 | -4.1840 | +5.4153 [+5.0457, +5.7738] | 6/7 |
| NIFTY_BELOW_MA50 | 1811 | +1.2286 | +1.2286 | +0.0000 [+0.0000, +0.0000] | 5/7 |
| NOT_OVEREXT | 4669 | +1.2050 | +1.2050 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIP2&VOL_ELEVATED | 921 | +1.1532 | -3.3291 | +4.4824 [+4.1551, +4.8107] | 5/7 |
| NIFTY_ABOVE_MA50 | 3153 | +1.1379 | +1.1379 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| MKT_BULLISH | 3153 | +1.1379 | +1.1379 | +0.0000 [+0.0000, +0.0000] | 7/7 |

## fresh exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 163 | +4.2242 | -5.6277 | +9.8519 [+8.1124, +11.6594] | +1.3081 [+0.5272, +2.0324] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&BREADTH_WEAK | 151 | +3.9881 | -7.6087 | +11.5968 [+9.5862, +13.6385] | +1.6193 [+0.8607, +2.4208] | 6/7 |
| B | DIPATR1&VIX_LOW | 177 | +3.7008 | -6.0841 | +9.7849 [+8.1317, +11.5118] | +1.5330 [+0.8914, +2.1875] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&MKT_BULLISH | 162 | +3.5458 | -5.2102 | +8.7560 [+7.2611, +10.4933] | +0.9857 [+0.4351, +1.5988] | 5/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&NIFTY_ABOVE_MA50 | 162 | +3.5458 | -5.2102 | +8.7560 [+7.2611, +10.4933] | +0.9857 [+0.4351, +1.5988] | 5/7 |
| A+B | DIP3&BREADTH_WEAK | 280 | +3.4904 | -6.0141 | +9.5045 [+8.1473, +10.8271] | +2.6806 [+2.0288, +3.3197] | 7/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 154 | +3.4676 | -7.0586 | +10.5262 [+8.7847, +12.5331] | +1.0281 [+0.1106, +1.9724] | 6/7 |
| A+B | DIP2&BEARSTATE | 276 | +3.4596 | -4.7977 | +8.2574 [+6.9387, +9.6347] | +2.4625 [+1.8064, +3.1463] | 7/7 |
| A+B | DIP3&VIX_LOW | 167 | +3.4466 | -5.5737 | +9.0204 [+7.2278, +10.7363] | +2.0826 [+1.3363, +2.7516] | 7/7 |
| B | DIPATR1&BREADTH_WEAK | 209 | +3.4160 | -7.5704 | +10.9864 [+9.4629, +12.5460] | +1.6237 [+1.0041, +2.2931] | 5/7 |
| A+B | DIP3&BEARSTATE | 247 | +3.4065 | -5.3854 | +8.7919 [+7.3863, +10.2790] | +2.0823 [+1.4619, +2.7632] | 5/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIP3&BEARSTATE | 182 | +3.3675 | -4.0977 | +7.4651 [+5.7543, +9.1132] | +1.1183 [+0.3560, +1.8920] | 7/7 |
| A+B | GAPUP&MKT_BEARISH | 195 | +3.3236 | -0.2345 | +3.5581 [+1.9098, +5.0008] | +3.0528 [+1.7442, +4.3175] | 7/7 |
| A+B | DIP2&BREADTH_WEAK | 322 | +3.3168 | -5.2240 | +8.5408 [+7.2292, +9.8407] | +2.7802 [+2.1113, +3.4239] | 7/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 199 | +3.3120 | -4.4687 | +7.7807 [+5.9791, +9.5546] | +1.6658 [+0.7958, +2.6115] | 7/7 |
| B | DIP3&BEARSTATE | 289 | +3.2523 | -5.1509 | +8.4032 [+7.0484, +9.8107] | +1.8189 [+1.2203, +2.4640] | 6/7 |
| B | DIP2&BEARSTATE | 326 | +3.2469 | -4.6573 | +7.9042 [+6.6556, +9.2259] | +2.1288 [+1.5237, +2.7785] | 7/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | DIPATR1&BREADTH_WEAK | 178 | +3.2442 | -8.0004 | +11.2446 [+9.2242, +13.3378] | +1.3959 [+0.4640, +2.3603] | 5/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | DIP3&VIX_LOW | 213 | +3.2328 | -5.3745 | +8.6073 [+6.8679, +10.3712] | +1.7166 [+0.9428, +2.4300] | 6/7 |
| B | GAPUP&MKT_BEARISH | 250 | +3.1738 | +0.0247 | +3.1491 [+1.7990, +4.4347] | +2.7280 [+1.5920, +3.8221] | 7/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP2&BEARSTATE | 230 | +3.1604 | -4.1125 | +7.2728 [+5.6697, +8.9330] | +2.0099 [+1.0736, +2.9556] | 7/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIP3&VIX_LOW | 234 | +3.1518 | -4.9368 | +8.0886 [+6.5888, +9.6239] | +1.6016 [+0.8362, +2.3195] | 6/7 |
| A+B | DIPATR1 | 209 | +3.1503 | -7.8294 | +10.9797 [+9.4863, +12.5493] | +1.6053 [+1.0111, +2.2683] | 5/7 |
| A+B | DIPATR1&NOT_OVEREXT | 209 | +3.1503 | -7.8294 | +10.9797 [+9.4863, +12.5493] | +1.6053 [+1.0111, +2.2683] | 5/7 |
| d_wq_12_change<0&d_ema20_angle_deg_change<0 | DIPATR1&MKT_BEARISH | 152 | +3.1195 | -9.2128 | +12.3322 [+10.3671, +14.6135] | +1.7859 [+0.9543, +2.7008] | 6/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| DIP2&BEARSTATE | 862 | +1.6342 | -3.2009 | +4.8352 [+4.1494, +5.5275] | 6/7 |
| VIX_HIGH | 2498 | +1.5745 | +1.5745 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| DIP2&BREADTH_WEAK | 1227 | +1.5510 | -3.4012 | +4.9522 [+4.3864, +5.5250] | 6/7 |
| DIP3&BEARSTATE | 730 | +1.5232 | -4.1840 | +5.7072 [+4.9120, +6.5228] | 6/7 |
| DIP2&VOL_ELEVATED | 921 | +1.5164 | -3.3291 | +4.8455 [+4.2214, +5.5349] | 5/7 |
| VOL_ELEVATED | 1777 | +1.5111 | +1.5111 | +0.0000 [+0.0000, +0.0000] | 5/7 |
| DIPATR1&MKT_BULLISH | 711 | +1.5089 | -5.3273 | +6.8362 [+6.1667, +7.5770] | 7/7 |
| DIPATR1&NIFTY_ABOVE_MA50 | 711 | +1.5089 | -5.3273 | +6.8362 [+6.1667, +7.5770] | 7/7 |
| DIPATR1&BREADTH_WEAK | 577 | +1.4802 | -7.2344 | +8.7146 [+7.7543, +9.7347] | 6/7 |
| DIP2&MKT_BULLISH | 1336 | +1.4690 | -2.9828 | +4.4518 [+4.0296, +4.9140] | 7/7 |
| DIP2&NIFTY_ABOVE_MA50 | 1336 | +1.4690 | -2.9828 | +4.4518 [+4.0296, +4.9140] | 7/7 |
| BEARSTATE | 1667 | +1.4673 | +1.4673 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| GAPDOWN&VIX_HIGH | 1792 | +1.4278 | +0.7331 | +0.6947 [+0.2722, +1.1172] | 6/7 |
| GAPDOWN&BEARSTATE | 1260 | +1.4198 | +1.0378 | +0.3820 [-0.1466, +0.9166] | 7/7 |
| DIP3&BREADTH_WEAK | 1020 | +1.3774 | -4.4367 | +5.8141 [+5.1793, +6.4851] | 6/7 |

