# Setup tags (setuplab v0.7)

Freeze `FROZEN_SETUPS.json` sha256 `483f1539324f3ae5` - S1 Bad week + WQ-16 rising + 1-ATR dip, S2 Bad week + minus-DI 5-day change rising + gap down, S3 Bad week + WQ-40 rising + 3% dip, C1 Bad week + minus-DI rising + 2% dip, C2 B + 3% dip (bad week + EMA20 angle falling + 3% dip), C3 A+C, no dip (bad week + EMA20 angle falling + WQ-44 rising + Bollinger width rising), N1 Below the lower Bollinger band + 2% dip (any weekday)

Watchlist `C:\QuantData\setuplab\WL_R1_10\watchlist.parquet`, panel `C:\QuantData\cache_daily\panel_oc\panel.parquet`; 32076 picks, signal days 2020-01-16 .. 2026-09-15.

Files: `setup_tags.parquet/.csv` (one row per pick: `setups` = which setups entered and on which watch day, then per setup `su_<ID>_day / _entry_date / _entry / _net_d5 / _net_fresh / _status`), `setup_trades.parquet/.csv` (one row per entered setup), `TAGS.json`. Net % after 0.35 pp.

## Every setup against FINAL_001 (the same rule on the same data must give the same trades)

| setup | engine | exit | trades | net | D1 same trades | FINAL_001 trades | FINAL_001 net | same |
|---|---|---|---:|---:|---:|---:|---:|---|
| S1 | D | original_d5 | 733 | +1.4659 | -6.6636 | 733.0 | +1.4659 | yes |
| S1 | D | fresh | 733 | +2.1034 | -6.6636 | 733.0 | +2.1034 | yes |
| S2 | D | original_d5 | 1393 | +1.5948 | -1.9864 | 1393.0 | +1.5948 | yes |
| S2 | D | fresh | 1393 | +2.0907 | -1.9864 | 1393.0 | +2.0907 | yes |
| S3 | D | original_d5 | 1061 | +1.4931 | -5.5366 | 1061.0 | +1.4931 | yes |
| S3 | D | fresh | 1061 | +1.9453 | -5.5366 | 1061.0 | +1.9453 | yes |
| C1 | D | original_d5 | 2047 | +1.1875 | -5.0860 | 2047.0 | +1.1875 | yes |
| C1 | D | fresh | 2047 | +1.6790 | -5.0860 | 2047.0 | +1.6790 | yes |
| C2 | D | original_d5 | 1879 | +1.1668 | -5.8846 | 1879.0 | +1.1668 | yes |
| C2 | D | fresh | 1879 | +1.5511 | -5.8846 | 1879.0 | +1.5511 | yes |
| C3 | D | original_d5 | 1594 | +1.2917 | -1.5945 | 1594.0 | +1.2917 | yes |
| C3 | D | fresh | 1594 | +1.4537 | -1.5945 | 1594.0 | +1.4537 | yes |
| N1 | D | original_d5 | 1612 | +0.9376 | -5.0748 | 1612.0 | +0.9376 | yes |
| N1 | D | fresh | 1612 | +1.4146 | -5.0748 | 1612.0 | +1.4146 | yes |
| S1 | ENS | original_d5 | 806 | +1.5220 | -6.2803 | 806.0 | +1.5220 | yes |
| S1 | ENS | fresh | 806 | +2.3973 | -6.2803 | 806.0 | +2.3973 | yes |
| S2 | ENS | original_d5 | 1583 | +1.4988 | -1.7511 | 1583.0 | +1.4988 | yes |
| S2 | ENS | fresh | 1583 | +1.9207 | -1.7511 | 1583.0 | +1.9207 | yes |
| S3 | ENS | original_d5 | 1135 | +1.3937 | -5.4804 | 1135.0 | +1.3937 | yes |
| S3 | ENS | fresh | 1135 | +2.0719 | -5.4804 | 1135.0 | +2.0719 | yes |
| C1 | ENS | original_d5 | 2142 | +1.1353 | -4.9136 | 2142.0 | +1.1353 | yes |
| C1 | ENS | fresh | 2142 | +1.5083 | -4.9136 | 2142.0 | +1.5083 | yes |
| C2 | ENS | original_d5 | 1872 | +1.1696 | -5.7978 | 1872.0 | +1.1696 | yes |
| C2 | ENS | fresh | 1872 | +1.6871 | -5.7978 | 1872.0 | +1.6871 | yes |
| C3 | ENS | original_d5 | 1750 | +1.2850 | -1.7131 | 1750.0 | +1.2850 | yes |
| C3 | ENS | fresh | 1750 | +1.3880 | -1.7131 | 1750.0 | +1.3880 | yes |
| N1 | ENS | original_d5 | 1931 | +0.9099 | -4.8101 | 1931.0 | +0.9099 | yes |
| N1 | ENS | fresh | 1931 | +1.5119 | -4.8101 | 1931.0 | +1.5119 | yes |

**RECONCILED: every setup gives FINAL_001's trades and net.**

ATR check (the scan needs ATR14 / close for live picks): pick_meta's s_atr14 vs the panel's d_atr_pct / 100 at the signal day: D 3 of 15819 within 1e-6 (largest difference 1.70e-01); ENS 2 of 16257 within 1e-6 (largest difference 1.23e-01)
