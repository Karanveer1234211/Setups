# setuplab - setups x logical confluences (setuplab v0.4)

Pool: NONE, B, A+B, d_ema20_angle_deg_change<0&d_rsi14_obv_x_change>0, d_wq_33_change<0&d_ema20_angle_deg_change<0, d_ema20_angle_deg_change<0&d_mdi14_diff1_change<0, d_wq_33_change>0&w_ret_13w_change<0, d_rsi14_obv_x_change<0&w_ret_13w_change<0, d_mdi14_diff1_change>0&w_ret_13w_change<0, d_bb_bw_20_change>0&w_ret_13w_change<0, d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0, d_wq_44_change>0&w_ret_13w_change<0, d_cmf20_rmean50_change<0&d_donch_pos_50_rmean50_change<0, d_bb_bw_20_change>0&d_donch_pos_50_rmean50_change<0, d_cmf20_rmean50_change<0&w_ret_13w_change<0, d_donch_pos_50_rmean50_change<0&d_ema20_angle_deg_change<0.

Confluences (declared before the run): price DIP1, DIP2, DIP3, DIPATR1, GREEN, UPCLOSE, GAPDOWN, GAPUP; context BEARSTATE, BULLSTATE, NIFTY_ABOVE_MA50, NIFTY_BELOW_MA50, MKT_BULLISH, MKT_BEARISH, VIX_LOW, VIX_HIGH, BREADTH_WEAK, NOT_OVEREXT, VOL_ELEVATED; and every price x context pair.

Each row: the combination's own trades vs the model's D1 entry on the same ids; 'adds' = the same combination vs the confluence ALONE on the same ids (what the indicator setup adds); years = signal years with net per trade above 0. Net % after 0.35 pp; 95% block bootstrap over signal days. Exploratory: 1712 combinations on the history the setups came from - expect some to look good by chance.

## original_d5 exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 560 | +3.1416 | +0.2189 | +2.9226 [+2.1787, +3.6427] | +1.8320 [+1.2104, +2.5029] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 523 | +2.8413 | -0.0462 | +2.8875 [+2.1332, +3.6684] | +1.7822 [+1.1670, +2.3890] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 251 | +2.5019 | -6.9834 | +9.4854 [+8.4865, +10.3627] | +1.3565 [+0.7811, +1.8812] | 5/7 |
| B | DIPATR1&BEARSTATE | 406 | +2.4717 | -7.2956 | +9.7673 [+8.9123, +10.6360] | +1.3096 [+0.8746, +1.7599] | 6/7 |
| A+B | DIPATR1&BEARSTATE | 380 | +2.4377 | -7.3481 | +9.7858 [+8.8923, +10.7269] | +1.2698 [+0.8181, +1.7497] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 472 | +2.3391 | -4.9410 | +7.2801 [+6.5976, +7.8899] | +1.5640 [+1.0369, +2.0563] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 381 | +2.2919 | -5.6411 | +7.9330 [+7.1362, +8.6940] | +1.8924 [+1.3205, +2.4072] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 549 | +2.2904 | -0.5077 | +2.7981 [+2.1205, +3.4701] | +1.8761 [+1.3415, +2.4392] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&BEARSTATE | 551 | +2.2788 | -4.2546 | +6.5333 [+5.8603, +7.1493] | +1.8197 [+1.2787, +2.3139] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&VOL_ELEVATED | 596 | +2.2606 | -4.1597 | +6.4202 [+5.8079, +6.9982] | +1.5138 [+1.0098, +1.9852] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&MKT_BEARISH | 441 | +2.2605 | -4.8822 | +7.1427 [+6.3836, +7.8585] | +2.1588 [+1.5971, +2.6749] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&VOL_ELEVATED | 502 | +2.2515 | -4.9787 | +7.2302 [+6.5799, +7.8311] | +1.3471 [+0.8461, +1.7940] | 7/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 1100 | +2.2224 | -0.3756 | +2.5980 [+2.0109, +3.1752] | +1.8336 [+1.3496, +2.3549] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 464 | +2.1899 | -7.2981 | +9.4879 [+8.6634, +10.3016] | +1.2069 [+0.8092, +1.6264] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&MKT_BEARISH | 437 | +2.1869 | -1.2187 | +3.4056 [+2.5011, +4.2587] | +2.3165 [+1.5739, +3.0647] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 233 | +2.1845 | -7.5951 | +9.7796 [+8.7293, +10.7246] | +1.1256 [+0.6348, +1.6266] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 1020 | +2.1702 | -0.3911 | +2.5612 [+1.8531, +3.2298] | +1.8473 [+1.2672, +2.4736] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP1&VOL_ELEVATED | 696 | +2.1701 | -3.4826 | +5.6527 [+5.0126, +6.2847] | +1.6028 [+1.1070, +2.0627] | 7/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 802 | +2.1657 | -0.0479 | +2.2136 [+1.4881, +2.9402] | +1.4177 [+0.8666, +2.0614] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 534 | +2.1619 | -0.5732 | +2.7351 [+2.1442, +3.3235] | +1.7543 [+1.2565, +2.2917] | 7/7 |
| B | DIP3&BEARSTATE | 754 | +2.1231 | -5.4916 | +7.6147 [+7.0344, +8.1852] | +1.7764 [+1.3694, +2.2022] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 233 | +2.1157 | -6.7241 | +8.8399 [+7.8335, +9.8470] | +0.7677 [+0.2693, +1.2626] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 896 | +2.0970 | -0.2841 | +2.3811 [+1.7653, +2.9504] | +1.4884 [+1.0446, +1.9890] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 307 | +2.0915 | -7.1400 | +9.2316 [+8.2937, +10.1614] | +1.1845 [+0.7263, +1.6537] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP1&BEARSTATE | 645 | +2.0900 | -3.6474 | +5.7375 [+5.0492, +6.3951] | +1.9139 [+1.3888, +2.4060] | 7/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| VOL_ELEVATED | 4854 | +1.5174 | +1.5174 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| BEARSTATE | 4631 | +1.4750 | +1.4750 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| VIX_HIGH | 8135 | +1.1734 | +1.1734 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIP3&BEARSTATE | 1915 | +1.1288 | -4.1643 | +5.2932 [+4.9452, +5.6836] | 6/7 |
| GAPDOWN&VOL_ELEVATED | 3793 | +1.0900 | +0.9450 | +0.1450 [-0.1633, +0.4274] | 7/7 |
| DIP3&VOL_ELEVATED | 2055 | +1.0670 | -4.2314 | +5.2985 [+4.9317, +5.6943] | 6/7 |
| GAPUP&BEARSTATE | 4479 | +1.0660 | +1.7721 | -0.7061 [-0.8781, -0.5419] | 7/7 |
| DIP2&VOL_ELEVATED | 2445 | +1.0588 | -3.2939 | +4.3528 [+4.0025, +4.7262] | 7/7 |
| DIP2&BEARSTATE | 2270 | +1.0501 | -3.2664 | +4.3165 [+3.9790, +4.6954] | 6/7 |
| BREADTH_WEAK | 8118 | +1.0115 | +1.0115 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| GAPDOWN&BEARSTATE | 3605 | +0.9737 | +0.8712 | +0.1025 [-0.2135, +0.3949] | 7/7 |
| MKT_BEARISH | 3401 | +0.9630 | +0.9630 | +0.0000 [+0.0000, +0.0000] | 5/7 |
| GAPUP&VOL_ELEVATED | 4714 | +0.9504 | +1.8167 | -0.8663 [-1.0516, -0.6954] | 6/7 |
| DIP1&BEARSTATE | 2732 | +0.9439 | -2.3660 | +3.3099 [+2.9955, +3.6581] | 7/7 |
| DIP1&VOL_ELEVATED | 2891 | +0.9253 | -2.4656 | +3.3908 [+3.0548, +3.7323] | 7/7 |

## fresh exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 251 | +3.3729 | -6.9834 | +10.3563 [+8.2685, +12.3931] | +1.2342 [+0.2457, +2.2049] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 233 | +3.3204 | -7.5951 | +10.9155 [+9.0779, +12.7458] | +1.0492 [+0.3803, +1.7353] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 523 | +3.2513 | -0.0462 | +3.2975 [+2.2115, +4.4288] | +1.6238 [+0.9873, +2.2858] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 381 | +3.2224 | -5.6411 | +8.8636 [+7.1227, +10.5040] | +1.7986 [+0.9275, +2.6327] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 255 | +3.2156 | -7.2281 | +10.4437 [+8.9319, +11.9368] | +1.4718 [+0.8490, +2.0826] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 627 | +3.2122 | -5.7573 | +8.9695 [+7.7542, +10.2048] | +1.3904 [+0.8393, +2.0013] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 560 | +3.1954 | +0.2189 | +2.9765 [+2.0025, +3.9981] | +1.7093 [+1.0147, +2.4009] | 6/7 |
| B | DIPATR1&BEARSTATE | 406 | +3.1475 | -7.2956 | +10.4430 [+8.8055, +12.1186] | +1.3253 [+0.6903, +1.9702] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 307 | +3.1466 | -7.1400 | +10.2866 [+8.3347, +12.3574] | +1.3827 [+0.6146, +2.1747] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 472 | +3.0938 | -4.9410 | +8.0349 [+6.6523, +9.4379] | +1.5234 [+0.7444, +2.2983] | 7/7 |
| A+B | DIPATR1&BEARSTATE | 380 | +3.0738 | -7.3481 | +10.4219 [+8.7512, +12.1719] | +1.2645 [+0.6222, +1.8701] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 430 | +3.0411 | -5.3734 | +8.4145 [+7.0072, +9.8587] | +1.1387 [+0.6585, +1.6428] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&BEARSTATE | 551 | +3.0153 | -4.2546 | +7.2698 [+5.9794, +8.5596] | +1.7695 [+0.9796, +2.5224] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 405 | +2.9824 | -5.5861 | +8.5685 [+7.2111, +9.9738] | +1.3275 [+0.6074, +2.1283] | 7/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 292 | +2.9757 | -8.0282 | +11.0040 [+8.8993, +12.9639] | +0.9941 [+0.3126, +1.6904] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&MKT_BEARISH | 441 | +2.9685 | -4.8822 | +7.8507 [+6.2019, +9.4150] | +1.9277 [+0.9882, +2.7366] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 494 | +2.9432 | -6.0574 | +9.0006 [+7.7441, +10.3011] | +1.4530 [+0.8419, +2.1789] | 7/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 518 | +2.9127 | -5.1856 | +8.0983 [+6.8069, +9.3130] | +1.5953 [+0.9624, +2.2134] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&VOL_ELEVATED | 502 | +2.8618 | -4.9787 | +7.8405 [+6.5109, +9.1734] | +1.2625 [+0.6355, +1.8942] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 396 | +2.8484 | -7.1141 | +9.9625 [+8.1760, +11.6711] | +1.0721 [+0.4149, +1.6483] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 410 | +2.8339 | -5.5026 | +8.3365 [+6.5312, +10.0421] | +1.9088 [+1.1064, +2.7047] | 7/7 |
| B | DIPATR1&VIX_LOW | 611 | +2.8306 | -5.7410 | +8.5717 [+7.3123, +9.8394] | +1.2935 [+0.7754, +1.8832] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&MKT_BEARISH | 222 | +2.8130 | -8.1530 | +10.9660 [+8.8638, +13.0888] | +1.5902 [+0.5978, +2.6295] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 233 | +2.8024 | -6.7241 | +9.5265 [+7.7668, +11.4222] | +0.6693 [-0.0748, +1.4221] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&VOL_ELEVATED | 596 | +2.7910 | -4.1597 | +6.9506 [+5.7490, +8.1600] | +1.2481 [+0.6107, +1.8885] | 7/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| DIP3&BEARSTATE | 1915 | +1.5410 | -4.1643 | +5.7053 [+5.0323, +6.3457] | 5/7 |
| VOL_ELEVATED | 4854 | +1.5174 | +1.5174 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIP2&VOL_ELEVATED | 2445 | +1.4825 | -3.2939 | +4.7764 [+4.1619, +5.3982] | 6/7 |
| DIP3&VOL_ELEVATED | 2055 | +1.4773 | -4.2314 | +5.7087 [+5.0278, +6.4017] | 6/7 |
| BEARSTATE | 4631 | +1.4750 | +1.4750 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIP2&BEARSTATE | 2270 | +1.4287 | -3.2664 | +4.6951 [+4.1331, +5.2586] | 5/7 |
| DIP3&MKT_BEARISH | 1553 | +1.3464 | -4.6663 | +6.0127 [+5.0641, +6.9768] | 6/7 |
| DIP2&MKT_BEARISH | 1817 | +1.3081 | -3.7832 | +5.0913 [+4.3087, +5.8912] | 6/7 |
| DIP1&BEARSTATE | 2732 | +1.2959 | -2.3660 | +3.6619 [+3.1958, +4.1308] | 6/7 |
| DIP1&VOL_ELEVATED | 2891 | +1.2301 | -2.4656 | +3.6957 [+3.1789, +4.2268] | 6/7 |
| DIP3&BREADTH_WEAK | 3160 | +1.2091 | -4.4533 | +5.6624 [+5.1188, +6.2177] | 6/7 |
| VIX_HIGH | 8135 | +1.1734 | +1.1734 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIPATR1&VOL_ELEVATED | 963 | +1.1723 | -8.0081 | +9.1803 [+8.0599, +10.3604] | 6/7 |
| DIPATR1&BREADTH_WEAK | 1957 | +1.1408 | -6.6998 | +7.8406 [+7.0558, +8.6748] | 6/7 |
| GAPUP&BEARSTATE | 4479 | +1.1281 | +1.7721 | -0.6440 [-0.8838, -0.4035] | 6/7 |

