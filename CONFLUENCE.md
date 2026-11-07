# setuplab - setups x logical confluences (setuplab v0.4)

Pool: NONE, B, A+B, d_ema20_angle_deg_change<0&d_rsi14_obv_x_change>0, d_wq_33_change<0&d_ema20_angle_deg_change<0, d_wq_33_change>0&w_ret_13w_change<0, d_ema20_angle_deg_change<0&d_mdi14_diff1_change<0, d_rsi14_obv_x_change<0&w_ret_13w_change<0, d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0, d_mdi14_diff1_change>0&w_ret_13w_change<0, d_bb_bw_20_change>0&w_ret_13w_change<0, d_wq_44_change>0&w_ret_13w_change<0, d_cmf20_rmean50_change<0&d_donch_pos_50_rmean50_change<0, d_cmf20_rmean50_change<0&w_ret_13w_change<0, d_wq_12_change>0&w_ret_13w_change<0, d_cmf20_rmean50_change<0&d_ema20_angle_deg_change<0.

Confluences (declared before the run): price DIP1, DIP2, DIP3, DIPATR1, GREEN, UPCLOSE, GAPDOWN, GAPUP; context BEARSTATE, BULLSTATE, NIFTY_ABOVE_MA50, NIFTY_BELOW_MA50, MKT_BULLISH, MKT_BEARISH, VIX_LOW, VIX_HIGH, BREADTH_WEAK, NOT_OVEREXT, VOL_ELEVATED; and every price x context pair.

Each row: the combination's own trades vs the model's D1 entry on the same ids; 'adds' = the same combination vs the confluence ALONE on the same ids (what the indicator setup adds); years = signal years with net per trade above 0. Net % after 0.35 pp; 95% block bootstrap over signal days. Exploratory: 1712 combinations on the history the setups came from - expect some to look good by chance.

## original_d5 exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 534 | +2.9418 | +0.0550 | +2.8868 [+2.1682, +3.5530] | +1.7480 [+1.1484, +2.3347] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&MKT_BEARISH | 432 | +2.6818 | -0.6441 | +3.3259 [+2.4975, +4.1696] | +2.0680 [+1.4106, +2.7567] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 493 | +2.6610 | -0.2090 | +2.8700 [+2.1019, +3.6171] | +1.8980 [+1.2865, +2.5433] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&NIFTY_BELOW_MA50 | 634 | +2.5086 | -0.7306 | +3.2392 [+2.5603, +3.8829] | +1.9537 [+1.4333, +2.4752] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 241 | +2.3694 | -7.2018 | +9.5713 [+8.7153, +10.3526] | +1.5168 [+0.9641, +2.0238] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 385 | +2.3328 | -5.4193 | +7.7521 [+6.9635, +8.4728] | +2.0093 [+1.4349, +2.5739] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 239 | +2.3284 | -7.6660 | +9.9944 [+9.1134, +10.8216] | +1.1246 [+0.6554, +1.5596] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 470 | +2.3142 | -4.9224 | +7.2366 [+6.6151, +7.8327] | +1.5417 [+1.0824, +2.0020] | 7/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 511 | +2.1603 | -0.6258 | +2.7861 [+2.1469, +3.4035] | +2.0091 [+1.4685, +2.5653] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP2&MKT_BEARISH | 445 | +2.1026 | -4.8559 | +6.9584 [+6.1728, +7.6931] | +2.1757 [+1.5694, +2.7346] | 6/7 |
| B | DIPATR1&BEARSTATE | 398 | +2.0634 | -7.7481 | +9.8114 [+8.9959, +10.6322] | +1.3128 [+0.9472, +1.6657] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&MKT_BEARISH | 404 | +2.0561 | -1.2502 | +3.3063 [+2.4158, +4.1318] | +2.3428 [+1.6247, +3.0973] | 5/7 |
| A+B | GAPDOWN&VIX_LOW | 531 | +2.0533 | -2.0310 | +4.0842 [+3.4021, +4.7979] | +2.6662 [+2.0022, +3.3812] | 5/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | GAPDOWN&VIX_LOW | 736 | +2.0477 | -1.0178 | +3.0656 [+2.4794, +3.6531] | +1.8683 [+1.3611, +2.4204] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&VIX_LOW | 534 | +2.0424 | -4.4713 | +6.5138 [+6.0443, +6.9767] | +1.2345 [+0.7936, +1.6356] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&VOL_ELEVATED | 507 | +2.0410 | -5.3257 | +7.3667 [+6.7664, +7.9698] | +1.5225 [+1.0118, +1.9967] | 7/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 520 | +2.0349 | -1.1276 | +3.1625 [+2.4944, +3.8036] | +2.1403 [+1.5759, +2.6846] | 6/7 |
| d_rsi14_obv_x_change<0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 225 | +2.0154 | -7.3306 | +9.3460 [+8.2837, +10.4261] | +1.0402 [+0.6088, +1.4928] | 6/7 |
| A+B | DIPATR1&BEARSTATE | 358 | +2.0147 | -7.9201 | +9.9348 [+9.0386, +10.8285] | +1.3259 [+0.9354, +1.7187] | 6/7 |
| B | DIP3&BEARSTATE | 777 | +2.0092 | -5.5105 | +7.5197 [+6.9017, +8.1145] | +1.7546 [+1.3837, +2.1032] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 340 | +2.0069 | -5.5088 | +7.5157 [+6.8027, +8.1995] | +1.2022 [+0.8470, +1.5364] | 6/7 |
| A+B | GAPUP&MKT_BEARISH | 661 | +1.9944 | -0.2791 | +2.2735 [+1.4682, +2.9735] | +2.0952 [+1.5358, +2.6320] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&MKT_BEARISH | 217 | +1.9791 | -7.9145 | +9.8936 [+8.8257, +10.8637] | +1.4956 [+0.9984, +2.0022] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&BREADTH_WEAK | 831 | +1.9644 | -0.8605 | +2.8249 [+2.3064, +3.3377] | +1.6742 [+1.2748, +2.0973] | 5/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 388 | +1.9594 | -5.6471 | +7.6065 [+6.7757, +8.3778] | +1.2011 [+0.8763, +1.5226] | 5/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| BEARSTATE | 4635 | +1.2491 | +1.2491 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| VOL_ELEVATED | 5040 | +1.2013 | +1.2013 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| VIX_HIGH | 7909 | +1.1049 | +1.1049 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| DIP3&BEARSTATE | 1985 | +0.9845 | -4.3750 | +5.3595 [+5.0079, +5.7468] | 6/7 |
| BREADTH_WEAK | 7902 | +0.9466 | +0.9466 | +0.0000 [+0.0000, +0.0000] | 5/7 |
| DIPATR1&VOL_ELEVATED | 1037 | +0.9449 | -8.2519 | +9.1968 [+8.4210, +10.1361] | 5/7 |
| DIP2&BEARSTATE | 2375 | +0.8988 | -3.4088 | +4.3076 [+3.9819, +4.6597] | 6/7 |
| GAPUP&BEARSTATE | 4476 | +0.8946 | +1.5550 | -0.6603 [-0.8514, -0.4848] | 7/7 |
| NOT_OVEREXT | 15236 | +0.8908 | +0.8908 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| DIPATR1&BEARSTATE | 1104 | +0.8672 | -7.3628 | +8.2300 [+7.4303, +9.2100] | 6/7 |
| NIFTY_BELOW_MA50 | 5892 | +0.8626 | +0.8626 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| GAPUP&VIX_HIGH | 7734 | +0.8543 | +1.3496 | -0.4953 [-0.6120, -0.3826] | 6/7 |
| MKT_BULLISH | 9926 | +0.8472 | +0.8472 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| NIFTY_ABOVE_MA50 | 9926 | +0.8472 | +0.8472 | +0.0000 [+0.0000, +0.0000] | 7/7 |
| GAPDOWN&VOL_ELEVATED | 3946 | +0.8455 | +0.6163 | +0.2292 [-0.0625, +0.5191] | 6/7 |

## fresh exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)

| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] | years net > 0 |
|---|---|---:|---:|---:|---|---|---:|
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 257 | +3.7355 | -7.3358 | +11.0713 [+9.5435, +12.5967] | +1.5515 [+0.8993, +2.1847] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 239 | +3.5999 | -7.6660 | +11.2659 [+9.3938, +13.1318] | +1.0836 [+0.3201, +1.8775] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 388 | +3.5233 | -5.6471 | +9.1705 [+7.5098, +10.8545] | +1.4318 [+0.9142, +1.9975] | 5/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 227 | +3.4597 | -7.5838 | +11.0434 [+9.5190, +12.5779] | +1.1170 [+0.6304, +1.6422] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 438 | +3.3363 | -5.9352 | +9.2715 [+8.0717, +10.4265] | +1.6618 [+1.1442, +2.1554] | 7/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 295 | +3.3257 | -7.6395 | +10.9652 [+9.1450, +12.8678] | +1.5224 [+0.8335, +2.2279] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP2&MKT_BEARISH | 483 | +3.3127 | -4.4848 | +7.7975 [+6.2430, +9.2441] | +2.1528 [+1.4547, +2.8602] | 7/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 419 | +3.2939 | -5.1594 | +8.4534 [+6.8022, +10.0013] | +1.9485 [+1.2207, +2.6997] | 7/7 |
| A+B | DIPATR1&VIX_LOW | 351 | +3.2697 | -6.1068 | +9.3765 [+7.7888, +10.9378] | +1.6562 [+1.1729, +2.1611] | 4/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIPATR1&MKT_BEARISH | 200 | +3.2597 | -7.5891 | +10.8488 [+8.9490, +12.7334] | +1.3869 [+0.6844, +2.1287] | 6/7 |
| d_donch_pos_50_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 530 | +3.2399 | -5.9617 | +9.2016 [+7.9569, +10.4623] | +1.4896 [+0.9763, +1.9555] | 5/7 |
| d_wq_12_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 335 | +3.2365 | -5.8862 | +9.1228 [+7.7234, +10.5169] | +1.5229 [+0.9762, +2.0808] | 5/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&BEARSTATE | 493 | +3.2229 | -0.2090 | +3.4319 [+2.2437, +4.5832] | +1.7203 [+1.0364, +2.4141] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&VOL_ELEVATED | 534 | +3.2218 | +0.0550 | +3.1668 [+2.1880, +4.1095] | +1.6098 [+0.8808, +2.3291] | 7/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIPATR1&BEARSTATE | 241 | +3.1956 | -7.2018 | +10.3974 [+8.5065, +12.2538] | +1.3756 [+0.4737, +2.2820] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | DIP3&MKT_BEARISH | 385 | +3.1531 | -5.4193 | +8.5724 [+6.8230, +10.2169] | +2.0130 [+1.1227, +2.8369] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIP3&BEARSTATE | 550 | +3.1317 | -4.9987 | +8.1304 [+6.7806, +9.4586] | +1.6775 [+1.1081, +2.2300] | 7/7 |
| B | DIPATR1&BEARSTATE | 398 | +3.1277 | -7.7481 | +10.8758 [+9.3917, +12.4229] | +1.4965 [+0.8778, +2.1126] | 6/7 |
| d_wq_44_change>0&w_ret_13w_change<0 | GAPDOWN&MKT_BEARISH | 432 | +3.1076 | -0.6441 | +3.7517 [+2.5171, +5.0606] | +2.3255 [+1.5273, +3.2374] | 5/7 |
| d_bb_bw_20_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 410 | +3.0900 | -6.1204 | +9.2104 [+7.8118, +10.5517] | +1.4813 [+0.9257, +2.0121] | 6/7 |
| d_mdi14_diff1_change>0&w_ret_13w_change<0 | DIPATR1&VIX_LOW | 338 | +3.0875 | -5.5382 | +8.6256 [+7.3007, +9.8428] | +1.3198 [+0.8732, +1.8255] | 5/7 |
| A+B | DIPATR1&BEARSTATE | 358 | +3.0630 | -7.9201 | +10.9831 [+9.3741, +12.6840] | +1.5061 [+0.8983, +2.1322] | 6/7 |
| d_cmf20_rmean50_change<0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 297 | +3.0196 | -8.1995 | +11.2191 [+9.4949, +13.0481] | +0.8316 [+0.0835, +1.6091] | 6/7 |
| d_wq_33_change>0&w_ret_13w_change<0 | DIPATR1&VOL_ELEVATED | 273 | +3.0190 | -8.5268 | +11.5457 [+9.6291, +13.5293] | +1.3339 [+0.7401, +2.0430] | 6/7 |
| B | DIPATR1&VIX_LOW | 548 | +3.0157 | -5.9463 | +8.9619 [+7.7151, +10.1872] | +1.5400 [+1.1407, +1.9691] | 6/7 |

### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)

| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |
|---|---:|---:|---:|---|---:|
| DIPATR1&VOL_ELEVATED | 1037 | +1.4407 | -8.2519 | +9.6926 [+8.6644, +10.7738] | 6/7 |
| DIP3&BEARSTATE | 1985 | +1.3521 | -4.3750 | +5.7271 [+5.0294, +6.3763] | 5/7 |
| DIPATR1&BREADTH_WEAK | 1969 | +1.2829 | -6.7986 | +8.0815 [+7.2428, +8.9175] | 6/7 |
| DIP2&BEARSTATE | 2375 | +1.2607 | -3.4088 | +4.6695 [+4.0737, +5.2586] | 5/7 |
| BEARSTATE | 4635 | +1.2491 | +1.2491 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| DIP3&BREADTH_WEAK | 3253 | +1.2263 | -4.4549 | +5.6812 [+5.1378, +6.1990] | 6/7 |
| VOL_ELEVATED | 5040 | +1.2013 | +1.2013 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| DIPATR1&BEARSTATE | 1104 | +1.1617 | -7.3628 | +8.5245 [+7.5241, +9.5500] | 5/7 |
| DIP3&MKT_BEARISH | 1554 | +1.1525 | -4.8066 | +5.9591 [+5.0595, +6.8208] | 5/7 |
| DIP2&MKT_BEARISH | 1830 | +1.1226 | -3.8810 | +5.0037 [+4.2303, +5.7894] | 5/7 |
| VIX_HIGH | 7909 | +1.1049 | +1.1049 | +0.0000 [+0.0000, +0.0000] | 6/7 |
| DIP2&BREADTH_WEAK | 3968 | +1.0843 | -3.4811 | +4.5654 [+4.0714, +5.0258] | 6/7 |
| DIPATR1&MKT_BEARISH | 878 | +1.0701 | -8.1322 | +9.2023 [+7.8090, +10.7528] | 6/7 |
| DIP3&VOL_ELEVATED | 2175 | +1.0628 | -4.6372 | +5.6999 [+5.1130, +6.2947] | 6/7 |
| DIPATR1&NIFTY_ABOVE_MA50 | 2337 | +1.0593 | -5.2855 | +6.3447 [+5.8022, +6.9078] | 6/7 |

