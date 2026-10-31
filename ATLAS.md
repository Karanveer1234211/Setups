# Behavioural Path Atlas - Phase 1 (sealed discovery map)

pathlab v1.1 run PL_20261031_001, report built 2026-10-31 19:12. **SEALED**: T0 from 2020-01-01 to 2022-12-31 only (windows run into January 2023). Nothing with a later T0 was read by the families, the atlas or this report; the 2023-25 pages stay closed until the candidate list is frozen. Declaration `ff4871f013f642ce`.

## Verdict first

- Daily paths: **no stable structure** - cells are described by the path measures alone.
-    0 of 13 daily families / regions occur more or less often than in the random-walk version of the same stock-days (candidate, 2020-2022).
- Intraday paths: **no separated families**; the paths form a continuum. They are described by **7 path regions** (a stable, reproduced partition of that continuum), not as distinct behaviours.
-    0 of 13 intraday families / regions occur more or less often than in the random-walk version of the same stock-days (candidate, 2020-2022).
- Does the state at T0 tell us about the daily path? **yes, in 2020-2022**: 0.00066 bits beyond the null (z 13.4).
- Does the regime at T0 tell us about the daily path? **not shown**: -0.00246 bits beyond the null (z -1.0).
- Does the state at T0 tell us about the intraday path? **yes, in 2020-2022**: 0.00172 bits beyond the null (z 13.2).
- Does the regime at T0 tell us about the intraday path? **not shown**: -0.00112 bits beyond the null (z -0.3).
- Cell comparisons (5,044): candidate 29, inconclusive 4,481, unstable 1, insufficient 533.
-    The candidates sit in 12 groups (one chance deviation in a group lights up several measures and baselines at once; count groups, not rows).
- False-discovery control: 30 of 4,537 sealed tests pass at 5%; about 1.5 of those are expected to be false - the 2023-25 walk-forward is what separates them.
- Integrity: the picks' paths match tradelab's export on 100.00% of 11,824 comparable picks (passed).
- Overlap check (every 5th T0 per stock): 99.7% of 702 estimates consistent -> PASS.

Every number below comes from the tables in this run folder. **candidate** = passed the 5% false-discovery control over the sealed tests (p from Student's t on the bootstrap standard error, degrees of freedom = separate 10-session stretches - 1) and its sign held in at least two thirds of its supported years. A candidate is an idea for the 2023-25 walk-forward test, not a finding: some are false (about 5% by the control's arithmetic, and they come in clumps, because one chance deviation in a cell moves several measures and baselines together). **inconclusive** = enough data, no clear difference; **insufficient** = below the minimum support; **unstable** = passed, but its sign flips in more than a third of its years. Associations, not causes.

## Data and coverage

| year | T0 rows | cash-like out | under 60 sessions out | eligible | complete windows | corporate-action suspects | all 5 sessions in 3-minute bars | D picks | ENS picks |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | 131,862 | 13 | 0 | 131,849 | 131,849 | 0 | 0 | 2,410 | 2,410 |
| 2021 | 191,916 | 47 | 0 | 191,869 | 191,864 | 0 | 38,306 | 2,480 | 2,480 |
| 2022 | 197,968 | 125 | 0 | 197,843 | 197,843 | 0 | 164,637 | 2,480 | 2,480 |

_T0 rows = panel_oc stock-days in the span plus every pick. Eligible = in the panel, not cash-like, 60+ sessions of bars. Complete = a bar on all five window sessions._

- Stocks: 1,001 built, 1,001 with eligible rows; 965 with a 3-minute file.
- 3-minute sessions by the usable test: ok 298,003, first high off the daily bar by > 0.5% 3,739, first low off the daily bar by > 0.5% 6,085, first open off the daily bar by > 0.5% 2,846, no 09:15 bar 1,040, under 80% of bars 933
- Corporate actions: 0 suspect sessions from the cache's ok.json files; 0 stocks without a usable ok.json used the 35% move fallback.
- Breadth for the regime labels: tradelab's saved copy (C:\QuantData\tradelab), built 2026-10-30T19:09:00.
- Eligible rows by state at T0: UNKNOWN 126,796, S01 44,815, S02 69,265, S03 45,237, S06 36,956, S07 87,562, S08 23,279, S09 87,385, S12 266
- Eligible rows by regime at T0: broad_bullish 178,847, narrow_bullish 152,792, mixed 69,584, broad_bearish 50,788, high_stress 69,550

## Path families - daily

519,398 paths (T0 up to the seal; reproduction halves Q1+Q3 259,069 and Q2+Q4 260,329); the search used a year-balanced sample of 298,256 with every state at least 5.6% of it (rare states repeated, common states thinned; the atlas itself is never weighted). 5 principal components keep 95.6% of the variation.

| k | stability ARI (mean / min) | reproduced | worst valley | explains | smallest group | result |
|---|---|---|---|---|---|---|
| 4 | 0.842 / 0.670 | 3/4 | 1.00 | 71.0% | 5.90% | - |
| 5 | 0.839 / 0.676 | 3/5 | 1.00 | 75.4% | 3.77% | - |
| 6 | 0.796 / 0.489 | 4/6 | 1.00 | 78.1% | 2.36% | - |
| 7 | 0.851 / 0.567 | 4/7 | 1.00 | 79.9% | 1.76% | - |
| 8 | 0.802 / 0.620 | 3/8 | 1.00 | 81.2% | 1.73% | - |
| 9 | 0.638 / 0.388 | 1/9 | 1.00 | 82.3% | 1.44% | - |
| 10 | 0.686 / 0.360 | 2/10 | 1.00 | 83.4% | 0.92% | - |
| 11 | 0.709 / 0.297 | 3/11 | 1.00 | 84.3% | 0.87% | - |
| 12 | 0.777 / 0.421 | 6/12 | 1.00 | 85.0% | 0.84% | - |
| 13 | 0.575 / 0.308 | 3/13 | 1.00 | 85.6% | 0.61% | - |
| 14 | 0.529 / 0.310 | 4/14 | 1.00 | 86.2% | 0.58% | - |
| 15 | 0.577 / 0.342 | 4/15 | 1.00 | 86.7% | 0.53% | - |
| 16 | 0.559 / 0.365 | 7/16 | 1.00 | 87.1% | 0.54% | - |

_Stable = mean ARI >= 0.75 over the date-block refits; reproduced = every centre found again between two separate fits on alternate quarters within half its spread; separated = between every group and its nearest neighbour the density dips to at most half the lower peak (worst valley <= 0.5; about 1 = no valley)._

Is there any separation at all along the main directions? component 1: two-peak D 0.40; component 2: two-peak D 0.09; component 3: two-peak D 0.00 (D >= 2 would mean two clean peaks).

**no stable structure**.

## Path families - intraday

202,265 paths (T0 up to the seal; reproduction halves Q1+Q3 83,180 and Q2+Q4 119,085); the search used a year-balanced sample of 151,860 with every state at least 5.6% of it (rare states repeated, common states thinned; the atlas itself is never weighted). 4 principal components keep 95.5% of the variation.

| k | stability ARI (mean / min) | reproduced | worst valley | explains | smallest group | result |
|---|---|---|---|---|---|---|
| 4 | 0.859 / 0.622 | 4/4 | 1.00 | 71.7% | 6.73% | regions |
| 5 | 0.871 / 0.541 | 5/5 | 1.00 | 75.8% | 4.30% | regions |
| 6 | 0.734 / 0.500 | 5/6 | 1.00 | 78.2% | 2.15% | - |
| 7 | 0.843 / 0.476 | 7/7 | 1.00 | 80.0% | 1.43% | regions |
| 8 | 0.762 / 0.538 | 7/8 | 1.00 | 81.4% | 1.41% | - |
| 9 | 0.719 / 0.418 | 9/9 | 1.00 | 82.6% | 1.36% | - |
| 10 | 0.571 / 0.292 | 6/10 | 1.00 | 83.6% | 1.08% | - |
| 11 | 0.549 / 0.278 | 5/11 | 1.00 | 84.5% | 1.17% | - |
| 12 | 0.556 / 0.292 | 12/12 | 1.00 | 85.3% | 0.81% | - |
| 13 | 0.725 / 0.362 | 2/13 | 1.00 | 86.0% | 0.83% | - |
| 14 | 0.625 / 0.351 | 2/14 | 1.00 | 86.5% | 0.78% | - |
| 15 | 0.603 / 0.349 | 2/15 | 1.00 | 87.0% | 0.66% | - |
| 16 | 0.528 / 0.386 | 3/16 | 1.00 | 87.4% | 0.46% | - |

_Stable = mean ARI >= 0.75 over the date-block refits; reproduced = every centre found again between two separate fits on alternate quarters within half its spread; separated = between every group and its nearest neighbour the density dips to at most half the lower peak (worst valley <= 0.5; about 1 = no valley)._

Is there any separation at all along the main directions? component 1: two-peak D 0.44; component 2: two-peak D 0.10; component 3: two-peak D 0.01 (D >= 2 would mean two clean peaks).

The same search on the random-walk paths at k = 7: worst valley 1.00, partition explains 80.5%.

| id | name (from the centre) | share of all paths | share of the fit sample | valley ratio | reproduction ratio | mixture agreement | found by | vs random walk 2020-22 | label |
|---|---|---|---|---|---|---|---|---|---|
| J01 | Quiet consolidation - strongest | 26.7% | 26.8% | 1.00 | 0.23 | 61% | both | +0.0 pp [-1.6 pp, +1.6 pp] | inconclusive |
| J02 | Quiet consolidation - second | 26.3% | 26.3% | 1.00 | 0.12 | 18% | k-means only | +1.1 pp [-1.0 pp, +3.4 pp] | inconclusive |
| J03 | Gradual drift down | 17.2% | 17.1% | 1.00 | 0.27 | 47% | k-means only | -0.7 pp [-4.1 pp, +2.7 pp] | inconclusive |
| J04 | Delayed expansion up | 17.1% | 17.0% | 1.00 | 0.11 | 40% | k-means only | -0.5 pp [-2.8 pp, +1.9 pp] | inconclusive |
| J05 | Immediate expansion and continuation - second | 6.5% | 6.5% | 1.00 | 0.18 | 38% | k-means only | -0.5 pp [-1.5 pp, +0.7 pp] | inconclusive |
| J06 | Persistent decline | 4.8% | 4.9% | 1.00 | 0.13 | 65% | both | +0.3 pp [-1.3 pp, +1.8 pp] | inconclusive |
| J07 | Immediate expansion and continuation - strongest | 1.3% | 1.4% | 1.00 | 0.11 | 63% | both | +0.2 pp [-0.0 pp, +0.6 pp] | inconclusive |

_Names follow the declared rules on each centre path; the data decides membership. 'vs random walk' = share minus the share of the same stock-days' random-walk paths in that group._

_(chart in ATLAS.html: centre path of each intraday region in ATR units from the T0 close (one shared scale; hover for values))_

Two peaks inside a group's 5-day close (a minority behaviour hiding in a group): none found.

## Do state and regime tell us anything?

Mutual information between what was known at T0 and which group the path fell in, against a null: states shuffled among the stocks of the same date (keeps each date's market), regimes shifted in time (keeps their run lengths). Excess = observed minus the null's mean. The random-walk row shows how much survives when every session is replaced by a random other session of the same stock: that part comes from WHICH stocks are in a state, not from WHEN.

| paths | period | rows | state MI (bits) | state excess | z | regime MI | regime excess | z | cell excess | z |
|---|---|---|---|---|---|---|---|---|---|---|
| daily | discovery | 519,398 | 0.00138 | +0.00066 | 13.4 | 0.00233 | -0.00246 | -1.0 | -0.00211 | -0.8 |
| daily | random walk all | 519,393 | 0.00016 | +0.00011 | 10.7 | 0.00002 | -0.00000 | -0.6 | +0.00012 | 4.4 |
| intraday | discovery | 202,265 | 0.00364 | +0.00172 | 13.2 | 0.00787 | -0.00112 | -0.3 | -0.00045 | -0.1 |
| intraday | random walk all | 202,265 | 0.00075 | +0.00057 | 15.5 | 0.00009 | +0.00000 | 0.2 | +0.00058 | 7.3 |

_Outcome: 5-day close quintile (r5_a, discovery cut points [-0.969, -0.268, 0.331, 1.162]): no stable families (daily); the 7 frozen intraday families (intraday). 200 shuffles / shifts each. Present = one-sided p under 0.05/6 in 2020-2022._

## The atlas - daily paths, 2020-2022

### Broad bullish (daily)

| state at T0 | observations | dates | stocks | effective n | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | the same after 35 bp round-trip costs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 19,827 | 262 | 862 | 456 | 49.3% [44.6%, 53.6%] | 0.20 [0.04, 0.35] | 1.46 [1.37, 1.54] | -1.08 [-1.21, -0.95] | 54.3% [49.5%, 59.0%] | 17.4% [14.1%, 21.0%] | -0.02% [-0.69%, 0.59%] |
| S02 Emerging bull | 37,113 | 262 | 899 | 380 | 51.8% [46.6%, 56.2%] | 0.25 [0.07, 0.42] | 1.54 [1.44, 1.64] | -1.03 [-1.19, -0.90] | 58.1% [53.2%, 62.5%] | 17.4% [14.5%, 20.2%] | 0.20% [-0.45%, 0.76%] |
| S03 Bull consolidation | 15,776 | 262 | 888 | 433 | 49.6% [44.9%, 54.1%] | 0.20 [0.03, 0.34] | 1.42 [1.33, 1.50] | -0.98 [-1.10, -0.86] | 57.2% [51.7%, 62.1%] | 14.1% [11.4%, 16.9%] | 0.01% [-0.65%, 0.57%] |
| S06 Reversal attempt | 16,635 | 255 | 772 | 199 | 53.7% [47.0%, 59.6%] | 0.29 [0.06, 0.50] | 1.52 [1.38, 1.66] | -0.93 [-1.10, -0.81] | 60.8% [54.3%, 66.8%] | 16.1% [12.4%, 20.2%] | 0.47% [-0.39%, 1.26%] |
| S07 Neutral range | 28,662 | 262 | 916 | 306 | 51.8% [46.0%, 57.0%] | 0.27 [0.09, 0.44] | 1.50 [1.38, 1.61] | -0.88 [-1.00, -0.79] | 61.6% [55.8%, 67.0%] | 12.7% [10.1%, 15.8%] | 0.27% [-0.42%, 0.87%] |
| S08 Bear continuation | 3,311 | 238 | 527 | 106 | 52.7% [44.2%, 60.6%] | 0.29 [-0.02, 0.60] | 1.50 [1.28, 1.77] | -0.86 [-1.03, -0.71] | 64.0% [54.8%, 71.7%] | 11.0% [7.9%, 14.9%] | 0.55% [-0.74%, 2.00%] |
| S09 Emerging bear | 10,973 | 262 | 876 | 273 | 47.1% [41.1%, 52.9%] | 0.08 [-0.10, 0.25] | 1.26 [1.15, 1.36] | -0.91 [-1.04, -0.80] | 57.1% [50.2%, 63.7%] | 10.1% [7.9%, 13.1%] | -0.36% [-1.01%, 0.27%] |
| S12 Unstable | 12 | 12 | 5 | 5 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 45,785 | 262 | 950 | 407 | 50.3% [45.2%, 54.8%] | 0.23 [0.06, 0.38] | 1.49 [1.40, 1.58] | -0.98 [-1.10, -0.87] | 58.0% [52.9%, 62.8%] | 14.6% [12.3%, 17.1%] | 0.12% [-0.53%, 0.69%] |

### Narrow bullish (daily)

| state at T0 | observations | dates | stocks | effective n | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | the same after 35 bp round-trip costs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 16,272 | 211 | 884 | 251 | 49.1% [43.2%, 54.4%] | 0.13 [-0.09, 0.33] | 1.38 [1.27, 1.48] | -1.10 [-1.28, -0.95] | 53.4% [47.9%, 58.9%] | 16.3% [12.9%, 19.6%] | -0.16% [-1.05%, 0.65%] |
| S02 Emerging bull | 17,707 | 211 | 894 | 206 | 48.6% [42.1%, 54.8%] | 0.10 [-0.12, 0.31] | 1.35 [1.24, 1.46] | -1.06 [-1.23, -0.91] | 53.6% [46.9%, 60.1%] | 13.7% [11.2%, 16.4%] | -0.25% [-1.11%, 0.55%] |
| S03 Bull consolidation | 18,586 | 211 | 907 | 273 | 50.9% [45.0%, 56.2%] | 0.22 [0.01, 0.41] | 1.42 [1.30, 1.54] | -1.02 [-1.19, -0.87] | 56.0% [49.2%, 62.6%] | 15.8% [13.0%, 18.7%] | 0.20% [-0.65%, 0.97%] |
| S06 Reversal attempt | 7,053 | 205 | 742 | 65 | 47.2% [35.6%, 59.0%] | 0.09 [-0.29, 0.47] | 1.31 [1.08, 1.54] | -1.03 [-1.26, -0.81] | 54.0% [42.4%, 65.5%] | 12.6% [9.0%, 17.6%] | -0.18% [-1.58%, 1.27%] |
| S07 Neutral range | 26,753 | 211 | 949 | 230 | 49.9% [44.0%, 55.7%] | 0.16 [-0.03, 0.36] | 1.32 [1.21, 1.44] | -0.97 [-1.13, -0.83] | 55.5% [48.5%, 62.7%] | 13.5% [11.5%, 16.1%] | -0.05% [-0.79%, 0.71%] |
| S08 Bear continuation | 4,356 | 197 | 577 | 105 | 56.5% [47.3%, 64.9%] | 0.37 [0.06, 0.67] | 1.47 [1.27, 1.68] | -0.88 [-1.08, -0.72] | 62.7% [52.8%, 71.1%] | 15.2% [11.9%, 19.2%] | 0.94% [-0.31%, 2.29%] |
| S09 Emerging bear | 24,318 | 211 | 940 | 195 | 52.2% [45.2%, 58.4%] | 0.14 [-0.07, 0.34] | 1.23 [1.13, 1.35] | -0.95 [-1.12, -0.81] | 56.2% [48.6%, 63.6%] | 15.3% [12.8%, 18.1%] | -0.06% [-0.86%, 0.70%] |
| S12 Unstable | 23 | 20 | 10 | 6 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 37,073 | 211 | 967 | 257 | 50.6% [45.1%, 56.1%] | 0.20 [0.00, 0.39] | 1.39 [1.28, 1.51] | -1.02 [-1.16, -0.88] | 55.6% [49.5%, 61.5%] | 16.1% [13.5%, 18.8%] | 0.10% [-0.67%, 0.88%] |

### Mixed (daily)

| state at T0 | observations | dates | stocks | effective n | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | the same after 35 bp round-trip costs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 3,925 | 100 | 622 | 108 | 48.3% [39.7%, 56.8%] | 0.07 [-0.26, 0.37] | 1.37 [1.21, 1.53] | -1.12 [-1.37, -0.88] | 51.9% [42.6%, 62.0%] | 17.2% [11.0%, 23.1%] | -0.42% [-1.99%, 1.04%] |
| S02 Emerging bull | 6,465 | 100 | 798 | 79 | 45.5% [34.2%, 54.9%] | -0.02 [-0.40, 0.31] | 1.34 [1.15, 1.53] | -1.13 [-1.43, -0.87] | 51.9% [40.5%, 62.8%] | 12.3% [7.5%, 17.5%] | -0.88% [-2.49%, 0.50%] |
| S03 Bull consolidation | 5,107 | 95 | 700 | 146 | 50.0% [42.6%, 57.2%] | 0.12 [-0.12, 0.35] | 1.32 [1.17, 1.49] | -1.01 [-1.22, -0.82] | 54.9% [45.4%, 64.8%] | 15.8% [11.7%, 20.0%] | -0.09% [-1.22%, 0.96%] |
| S06 Reversal attempt | 5,135 | 99 | 686 | 34 | 45.6% [29.4%, 61.7%] | -0.06 [-0.58, 0.39] | 1.19 [0.98, 1.41] | -1.00 [-1.38, -0.77] | 55.6% [39.1%, 68.9%] | 10.5% [5.7%, 19.5%] | -1.18% [-3.18%, 0.74%] |
| S07 Neutral range | 13,491 | 100 | 886 | 94 | 46.4% [37.0%, 55.5%] | 0.00 [-0.30, 0.29] | 1.24 [1.06, 1.41] | -1.01 [-1.24, -0.80] | 53.0% [42.2%, 63.9%] | 10.8% [8.2%, 14.1%] | -0.63% [-1.84%, 0.51%] |
| S08 Bear continuation | 3,905 | 99 | 577 | 50 | 56.2% [39.5%, 67.7%] | 0.20 [-0.27, 0.53] | 1.32 [1.10, 1.49] | -0.86 [-1.20, -0.64] | 62.5% [44.9%, 74.8%] | 11.7% [7.7%, 17.4%] | 0.30% [-1.58%, 1.56%] |
| S09 Emerging bear | 14,571 | 100 | 881 | 107 | 50.5% [40.9%, 59.1%] | 0.07 [-0.21, 0.31] | 1.21 [1.08, 1.35] | -0.92 [-1.15, -0.73] | 56.3% [45.5%, 66.5%] | 13.0% [8.9%, 17.8%] | -0.34% [-1.48%, 0.67%] |
| S12 Unstable | 22 | 20 | 11 | 12 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 16,697 | 100 | 901 | 106 | 47.1% [38.6%, 55.9%] | -0.00 [-0.29, 0.27] | 1.26 [1.11, 1.41] | -1.04 [-1.27, -0.82] | 54.1% [44.8%, 64.2%] | 12.4% [9.2%, 16.5%] | -0.57% [-1.73%, 0.53%] |

### Broad bearish (daily)

| state at T0 | observations | dates | stocks | effective n | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | the same after 35 bp round-trip costs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 1,678 | 69 | 410 | 40 | 53.3% [39.7%, 65.7%] | 0.11 [-0.39, 0.56] | 1.22 [0.97, 1.46] | -1.09 [-1.47, -0.76] | 51.4% [36.5%, 66.6%] | 17.3% [10.2%, 28.7%] | 0.07% [-2.56%, 2.33%] |
| S02 Emerging bull | 3,237 | 69 | 633 | 42 | 47.0% [34.8%, 61.2%] | -0.06 [-0.49, 0.42] | 1.13 [0.91, 1.41] | -1.14 [-1.47, -0.82] | 47.4% [33.9%, 64.0%] | 15.4% [10.0%, 25.1%] | -0.73% [-2.63%, 1.34%] |
| S03 Bull consolidation | 2,086 | 69 | 504 | 53 | 54.3% [41.9%, 65.4%] | 0.17 [-0.25, 0.53] | 1.22 [1.00, 1.41] | -0.99 [-1.32, -0.73] | 55.0% [40.1%, 68.6%] | 16.9% [9.6%, 26.8%] | 0.09% [-1.92%, 1.79%] |
| S06 Reversal attempt | 4,243 | 69 | 578 | 32 | 45.4% [32.1%, 59.1%] | -0.10 [-0.61, 0.32] | 1.00 [0.81, 1.23] | -1.06 [-1.53, -0.77] | 46.6% [28.6%, 60.8%] | 12.7% [8.4%, 20.4%] | -1.12% [-3.02%, 0.85%] |
| S07 Neutral range | 8,769 | 69 | 869 | 51 | 51.9% [39.9%, 64.1%] | 0.04 [-0.34, 0.42] | 1.12 [0.94, 1.32] | -1.01 [-1.34, -0.71] | 51.9% [38.0%, 67.5%] | 15.4% [10.0%, 23.7%] | -0.37% [-1.86%, 1.14%] |
| S08 Bear continuation | 4,185 | 69 | 565 | 54 | 50.9% [37.9%, 62.1%] | 0.08 [-0.31, 0.39] | 1.07 [0.88, 1.25] | -0.93 [-1.22, -0.72] | 53.7% [38.9%, 67.4%] | 13.9% [8.4%, 20.5%] | -0.26% [-1.88%, 1.09%] |
| S09 Emerging bear | 14,968 | 69 | 906 | 40 | 54.0% [39.2%, 67.6%] | 0.04 [-0.39, 0.43] | 1.07 [0.87, 1.26] | -1.01 [-1.37, -0.68] | 52.1% [35.5%, 69.9%] | 17.6% [10.9%, 27.3%] | -0.38% [-2.18%, 1.25%] |
| S12 Unstable | 42 | 24 | 11 | 6 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 11,365 | 69 | 896 | 60 | 50.0% [38.6%, 61.4%] | 0.03 [-0.33, 0.37] | 1.09 [0.92, 1.27] | -1.00 [-1.30, -0.75] | 50.9% [37.7%, 64.8%] | 15.0% [9.9%, 22.3%] | -0.44% [-1.93%, 1.00%] |

### High stress (daily)

| state at T0 | observations | dates | stocks | effective n | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | the same after 35 bp round-trip costs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 2,899 | 92 | 740 | 101 | 56.0% [47.7%, 63.8%] | 0.24 [-0.09, 0.53] | 1.42 [1.26, 1.58] | -1.10 [-1.40, -0.87] | 55.0% [47.2%, 64.1%] | 26.4% [17.5%, 36.7%] | 0.68% [-0.77%, 2.00%] |
| S02 Emerging bull | 4,407 | 100 | 807 | 130 | 55.8% [47.9%, 63.2%] | 0.33 [0.04, 0.58] | 1.46 [1.30, 1.64] | -1.00 [-1.21, -0.86] | 57.9% [50.3%, 64.7%] | 24.2% [16.5%, 32.8%] | 0.83% [-0.32%, 1.84%] |
| S03 Bull consolidation | 3,610 | 103 | 803 | 64 | 51.9% [42.3%, 61.2%] | 0.10 [-0.37, 0.50] | 1.39 [1.19, 1.59] | -1.25 [-1.77, -0.86] | 52.4% [41.5%, 64.2%] | 20.9% [14.6%, 27.8%] | -0.02% [-1.78%, 1.45%] |
| S06 Reversal attempt | 3,798 | 101 | 634 | 113 | 48.9% [43.9%, 59.4%] | 0.10 [-0.08, 0.40] | 1.13 [0.99, 1.46] | -0.90 [-1.09, -0.79] | 52.7% [46.6%, 61.2%] | 15.9% [10.6%, 25.4%] | -0.53% [-1.28%, 0.87%] |
| S07 Neutral range | 9,339 | 106 | 910 | 84 | 51.4% [42.8%, 58.7%] | 0.10 [-0.29, 0.39] | 1.29 [1.12, 1.44] | -1.14 [-1.53, -0.86] | 52.5% [42.5%, 62.0%] | 18.6% [13.3%, 23.3%] | -0.13% [-1.75%, 1.05%] |
| S08 Bear continuation | 7,462 | 105 | 633 | 26 | 54.5% [36.7%, 67.2%] | 0.05 [-0.69, 0.56] | 1.22 [0.97, 1.43] | -1.15 [-1.93, -0.67] | 54.0% [35.3%, 71.1%] | 18.5% [9.9%, 29.9%] | 0.26% [-4.31%, 3.64%] |
| S09 Emerging bear | 22,244 | 106 | 940 | 25 | 50.3% [36.1%, 64.4%] | -0.17 [-0.84, 0.41] | 1.14 [0.93, 1.36] | -1.37 [-2.03, -0.80] | 48.7% [34.7%, 64.9%] | 18.9% [10.3%, 30.8%] | -1.23% [-4.76%, 1.75%] |
| S12 Unstable | 158 | 60 | 38 | 24 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 15,355 | 106 | 938 | 113 | 53.3% [45.2%, 60.1%] | 0.12 [-0.18, 0.35] | 1.24 [1.13, 1.36] | -1.02 [-1.35, -0.79] | 55.0% [45.6%, 64.2%] | 20.7% [15.2%, 26.0%] | 0.17% [-1.34%, 1.44%] |

## The atlas - intraday paths, 2020-2022

### Broad bullish (intraday)

| state at T0 | observations | dates | stocks | effective n | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | first 30 minutes: move from the open | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 5,871 | 91 | 589 | 658 | 53.1% [44.6%, 59.9%] | 0.02 [-0.01, 0.05] | 4.5% [3.9%, 5.2%] | 2.9% [2.0%, 4.0%] | 57.4% [55.0%, 60.5%] | 3.0% [2.3%, 3.9%] |
| S02 Emerging bull | 14,350 | 91 | 825 | 1614 | 56.0% [48.4%, 62.1%] | 0.00 [-0.01, 0.03] | 4.5% [3.9%, 5.0%] | 2.5% [1.9%, 3.2%] | 57.2% [54.8%, 59.9%] | 3.3% [2.2%, 4.5%] |
| S03 Bull consolidation | 3,506 | 91 | 517 | 825 | 54.0% [46.3%, 60.9%] | 0.02 [-0.00, 0.05] | 3.7% [2.6%, 4.6%] | 2.2% [1.7%, 2.8%] | 59.1% [55.9%, 61.7%] | 2.3% [1.7%, 2.9%] |
| S06 Reversal attempt | 8,415 | 91 | 668 | 731 | 56.6% [45.6%, 65.4%] | 0.00 [-0.02, 0.03] | 3.4% [3.0%, 4.0%] | 1.9% [1.6%, 2.3%] | 57.4% [53.7%, 61.8%] | 2.2% [1.6%, 2.8%] |
| S07 Neutral range | 9,872 | 91 | 826 | 1241 | 58.2% [49.0%, 66.4%] | 0.02 [0.00, 0.04] | 3.5% [2.9%, 4.2%] | 1.8% [1.5%, 2.0%] | 57.9% [54.8%, 61.0%] | 2.2% [1.8%, 2.6%] |
| S08 Bear continuation | 1,386 | 91 | 286 | 900 | 58.0% [48.2%, 66.2%] | -0.00 [-0.03, 0.02] | 3.2% [2.2%, 4.2%] | 2.0% [1.1%, 3.2%] | 56.0% [51.8%, 60.0%] | 1.8% [1.0%, 2.5%] |
| S09 Emerging bear | 3,968 | 91 | 655 | 1066 | 52.9% [42.8%, 63.7%] | 0.00 [-0.02, 0.02] | 2.5% [2.1%, 3.0%] | 1.6% [1.3%, 1.9%] | 59.9% [57.1%, 62.5%] | 2.0% [1.5%, 2.5%] |
| S12 Unstable | 2 | 2 | 1 | 8 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 13,816 | 91 | 880 | 1436 | 55.1% [47.2%, 62.7%] | 0.01 [-0.00, 0.03] | 4.1% [3.4%, 4.8%] | 2.5% [2.0%, 3.0%] | 57.2% [54.3%, 60.0%] | 2.7% [2.2%, 3.2%] |

### Narrow bullish (intraday)

| state at T0 | observations | dates | stocks | effective n | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | first 30 minutes: move from the open | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 3,724 | 66 | 604 | 218 | 45.6% [35.8%, 57.5%] | 0.00 [-0.05, 0.06] | 4.2% [3.5%, 5.1%] | 3.8% [1.9%, 6.4%] | 58.3% [52.9%, 63.1%] | 4.7% [3.4%, 6.2%] |
| S02 Emerging bull | 6,833 | 66 | 795 | 357 | 51.3% [39.8%, 63.7%] | 0.01 [-0.04, 0.05] | 4.8% [4.0%, 5.7%] | 3.4% [1.7%, 6.1%] | 57.5% [53.5%, 61.7%] | 4.2% [3.4%, 5.0%] |
| S03 Bull consolidation | 3,477 | 66 | 572 | 516 | 47.9% [34.8%, 59.9%] | -0.00 [-0.04, 0.03] | 3.4% [3.0%, 3.9%] | 3.1% [1.9%, 5.5%] | 60.5% [56.8%, 64.3%] | 4.4% [3.3%, 6.0%] |
| S06 Reversal attempt | 3,828 | 66 | 613 | 213 | 50.9% [36.5%, 67.1%] | -0.00 [-0.05, 0.04] | 3.3% [2.6%, 4.3%] | 2.7% [1.7%, 4.6%] | 58.0% [52.6%, 63.4%] | 3.1% [2.3%, 4.1%] |
| S07 Neutral range | 8,343 | 66 | 863 | 433 | 51.2% [39.0%, 65.0%] | -0.00 [-0.03, 0.03] | 2.9% [2.5%, 3.4%] | 2.4% [1.5%, 3.6%] | 58.3% [54.1%, 62.0%] | 2.8% [2.1%, 3.5%] |
| S08 Bear continuation | 1,642 | 66 | 356 | 347 | 57.3% [40.6%, 70.9%] | -0.00 [-0.04, 0.04] | 2.9% [2.1%, 3.7%] | 2.0% [1.3%, 3.0%] | 59.9% [55.0%, 65.2%] | 2.5% [1.7%, 3.3%] |
| S09 Emerging bear | 7,024 | 66 | 806 | 596 | 47.5% [33.8%, 61.8%] | -0.02 [-0.04, 0.01] | 2.1% [1.7%, 2.7%] | 2.4% [1.6%, 3.5%] | 60.4% [56.7%, 63.9%] | 3.0% [2.2%, 3.9%] |
| S12 Unstable | 2 | 2 | 1 | 8 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 10,541 | 66 | 888 | 377 | 51.4% [39.4%, 64.8%] | 0.00 [-0.03, 0.04] | 3.6% [3.2%, 4.0%] | 2.9% [1.7%, 4.7%] | 59.0% [54.4%, 62.9%] | 3.8% [3.1%, 4.6%] |

### Mixed (intraday)

| state at T0 | observations | dates | stocks | effective n | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | first 30 minutes: move from the open | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 1,237 | 46 | 332 | 258 | 45.1% [33.6%, 60.0%] | 0.01 [-0.03, 0.05] | 3.8% [2.8%, 4.7%] | 2.2% [1.3%, 3.5%] | 61.5% [55.8%, 67.6%] | 2.8% [1.6%, 4.2%] |
| S02 Emerging bull | 2,682 | 46 | 628 | 315 | 49.8% [36.2%, 64.3%] | 0.02 [-0.02, 0.05] | 3.2% [2.5%, 4.0%] | 2.1% [1.5%, 3.0%] | 60.2% [55.6%, 64.5%] | 2.9% [1.7%, 4.2%] |
| S03 Bull consolidation | 1,476 | 46 | 360 | 295 | 45.5% [31.2%, 60.5%] | -0.01 [-0.04, 0.03] | 2.9% [2.0%, 4.0%] | 1.8% [1.1%, 2.7%] | 62.4% [57.2%, 68.0%] | 2.8% [1.7%, 3.5%] |
| S06 Reversal attempt | 2,743 | 46 | 564 | 169 | 55.3% [31.1%, 74.1%] | -0.00 [-0.04, 0.05] | 2.5% [1.7%, 3.5%] | 1.3% [0.9%, 1.7%] | 60.8% [52.9%, 67.2%] | 3.1% [2.0%, 4.1%] |
| S07 Neutral range | 6,251 | 46 | 781 | 385 | 47.6% [33.4%, 64.5%] | -0.00 [-0.03, 0.03] | 2.7% [2.4%, 3.1%] | 1.2% [0.9%, 1.5%] | 60.0% [54.6%, 65.4%] | 3.0% [2.3%, 3.7%] |
| S08 Bear continuation | 2,513 | 46 | 476 | 217 | 64.1% [38.6%, 80.4%] | 0.03 [-0.01, 0.07] | 1.5% [1.0%, 2.2%] | 1.6% [1.1%, 2.3%] | 50.9% [44.3%, 61.8%] | 2.4% [1.6%, 3.0%] |
| S09 Emerging bear | 6,222 | 46 | 809 | 476 | 54.4% [38.7%, 70.8%] | 0.01 [-0.02, 0.03] | 2.2% [1.7%, 2.6%] | 1.2% [0.8%, 1.8%] | 56.8% [50.2%, 63.5%] | 2.3% [1.7%, 3.1%] |
| S12 Unstable | 6 | 6 | 3 | 13 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 7,385 | 46 | 834 | 365 | 51.6% [36.5%, 69.2%] | -0.01 [-0.04, 0.03] | 2.6% [2.2%, 3.0%] | 1.6% [1.0%, 2.6%] | 59.1% [53.5%, 64.8%] | 3.1% [2.4%, 3.9%] |

### Broad bearish (intraday)

| state at T0 | observations | dates | stocks | effective n | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | first 30 minutes: move from the open | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 1,170 | 54 | 322 | 298 | 51.5% [36.4%, 67.8%] | -0.00 [-0.04, 0.04] | 3.5% [2.4%, 4.7%] | 3.0% [1.7%, 4.2%] | 58.7% [51.9%, 65.4%] | 3.4% [1.8%, 5.1%] |
| S02 Emerging bull | 2,169 | 54 | 524 | 293 | 45.3% [30.3%, 64.9%] | -0.01 [-0.05, 0.03] | 3.1% [1.9%, 4.4%] | 3.4% [2.2%, 4.6%] | 58.6% [53.4%, 63.3%] | 5.3% [3.1%, 7.8%] |
| S03 Bull consolidation | 1,547 | 54 | 404 | 319 | 54.3% [38.3%, 69.1%] | -0.02 [-0.05, 0.02] | 3.2% [2.1%, 4.6%] | 3.1% [2.4%, 4.0%] | 57.3% [51.9%, 63.5%] | 3.5% [2.1%, 5.2%] |
| S06 Reversal attempt | 1,822 | 54 | 436 | 168 | 36.2% [21.3%, 59.6%] | -0.07 [-0.11, -0.01] | 2.3% [1.6%, 3.1%] | 2.7% [1.9%, 3.5%] | 61.6% [54.6%, 66.8%] | 4.7% [3.1%, 6.3%] |
| S07 Neutral range | 6,752 | 54 | 810 | 256 | 51.4% [35.9%, 67.1%] | -0.03 [-0.06, 0.02] | 2.5% [2.1%, 3.0%] | 2.1% [1.4%, 2.9%] | 57.2% [52.9%, 61.5%] | 3.5% [2.2%, 5.2%] |
| S08 Bear continuation | 2,850 | 54 | 479 | 208 | 51.5% [34.4%, 66.6%] | -0.05 [-0.09, -0.00] | 1.8% [1.3%, 2.6%] | 1.9% [1.3%, 2.8%] | 56.5% [52.5%, 62.1%] | 3.1% [2.3%, 4.4%] |
| S09 Emerging bear | 11,546 | 54 | 866 | 229 | 52.7% [36.2%, 70.0%] | -0.02 [-0.06, 0.02] | 2.4% [1.7%, 3.3%] | 2.0% [1.4%, 2.8%] | 57.3% [52.5%, 62.6%] | 3.3% [2.1%, 4.8%] |
| S12 Unstable | 41 | 23 | 11 | 21 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 7,607 | 54 | 851 | 309 | 49.4% [34.2%, 64.5%] | -0.04 [-0.07, 0.00] | 2.6% [2.1%, 3.2%] | 2.4% [1.8%, 3.3%] | 57.2% [52.8%, 61.8%] | 3.7% [2.6%, 4.9%] |

### High stress (intraday)

| state at T0 | observations | dates | stocks | effective n | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | first 30 minutes: move from the open | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon |
|---|---|---|---|---|---|---|---|---|---|---|
| S01 Strong bull | 1,027 | 45 | 415 | 39 | 52.6% [43.4%, 63.4%] | -0.01 [-0.13, 0.15] | 5.4% [3.6%, 7.7%] | 12.1% [5.3%, 20.9%] | 49.1% [37.8%, 57.8%] | 5.6% [2.9%, 8.4%] |
| S02 Emerging bull | 2,036 | 45 | 594 | 58 | 55.3% [44.7%, 63.6%] | -0.01 [-0.11, 0.11] | 5.2% [3.8%, 7.1%] | 7.5% [3.0%, 15.9%] | 50.9% [37.3%, 58.5%] | 5.7% [3.8%, 7.7%] |
| S03 Bull consolidation | 1,150 | 45 | 421 | 47 | 50.6% [39.2%, 63.4%] | -0.07 [-0.19, 0.05] | 4.3% [2.7%, 6.0%] | 8.8% [3.6%, 17.5%] | 53.0% [40.4%, 61.8%] | 5.9% [2.8%, 9.5%] |
| S06 Reversal attempt | 1,343 | 45 | 422 | 57 | 48.8% [40.4%, 62.7%] | -0.01 [-0.11, 0.11] | 3.0% [1.9%, 5.2%] | 4.9% [1.5%, 13.7%] | 55.9% [39.8%, 64.2%] | 5.9% [3.2%, 9.4%] |
| S07 Neutral range | 4,875 | 45 | 761 | 135 | 54.1% [41.4%, 65.1%] | -0.01 [-0.09, 0.04] | 3.8% [2.9%, 5.1%] | 6.5% [2.7%, 14.4%] | 53.4% [46.2%, 58.4%] | 4.7% [3.4%, 6.7%] |
| S08 Bear continuation | 2,790 | 45 | 437 | 113 | 56.1% [41.6%, 68.9%] | -0.02 [-0.10, 0.03] | 3.0% [1.8%, 5.5%] | 3.5% [1.8%, 9.1%] | 54.6% [47.4%, 60.7%] | 4.8% [3.2%, 8.0%] |
| S09 Emerging bear | 9,812 | 45 | 862 | 145 | 57.3% [43.8%, 70.6%] | -0.00 [-0.07, 0.05] | 3.4% [2.5%, 5.1%] | 4.8% [2.6%, 10.5%] | 48.9% [43.1%, 55.3%] | 4.6% [3.3%, 6.9%] |
| S12 Unstable | 60 | 27 | 19 | 26 | insufficient | insufficient | insufficient | insufficient | insufficient | insufficient |
| UNKNOWN Unknown | 6,553 | 45 | 850 | 156 | 52.6% [42.0%, 62.8%] | -0.03 [-0.09, 0.03] | 3.9% [2.9%, 5.8%] | 5.7% [2.5%, 13.0%] | 55.3% [46.2%, 60.9%] | 4.5% [3.0%, 6.9%] |

### Where each intraday region is more or less common

Each cell: the group's share in that state x regime minus its share in everything (percentage points, 2020-2022). Blue = more often, red = less often, a ring = candidate against everything. '-' = below the minimum support.

_(chart in ATLAS.html: J01: share by cell minus overall share)_

_(chart in ATLAS.html: J02: share by cell minus overall share)_

_(chart in ATLAS.html: J03: share by cell minus overall share)_

_(chart in ATLAS.html: J04: share by cell minus overall share)_

_(chart in ATLAS.html: J05: share by cell minus overall share)_

_(chart in ATLAS.html: J06: share by cell minus overall share)_

_(chart in ATLAS.html: J07: share by cell minus overall share)_

## Candidates (2020-2022, sealed)

| paths | group | measure | against | value | difference [95%] | q | years against the sign |
|---|---|---|---|---|---|---|---|
| daily | S09 Emerging bear (all regimes) | reached +2 ATR at some point in the 5 sessions | everything | 16.7% | -4.2 pp [-5.5 pp, -3.0 pp] | 0.0000 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | best high of the window from C0 (MFE) | same regime, all states | 1.26 | -0.23 [-0.29, -0.15] | 0.0002 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | reached +2 ATR at some point in the 5 sessions | same regime, all states | 18.7% | -5.7 pp [-7.4 pp, -3.8 pp] | 0.0002 | 0/3 |
| daily | S09 Emerging bear (all regimes) | best high of the window from C0 (MFE) | everything | 1.18 | -0.16 [-0.22, -0.11] | 0.0002 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | after -1 ATR came first: ended above C0 | same regime, all states | 10.1% | -5.0 pp [-6.6 pp, -3.2 pp] | 0.0008 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | reached +1 ATR at some point in the 5 sessions | same regime, all states | 44.8% | -7.2 pp [-9.5 pp, -4.4 pp] | 0.0012 | 0/3 |
| daily | S09 Emerging bear x Narrow bullish | best high of the window from C0 (MFE) | same regime, all states | 1.23 | -0.11 [-0.16, -0.06] | 0.0095 | 0/3 |
| daily | S09 Emerging bear x Narrow bullish | reached +2 ATR at some point in the 5 sessions | same regime, all states | 18.0% | -3.1 pp [-4.4 pp, -1.7 pp] | 0.0095 | 0/3 |
| daily | S07 Neutral range (all regimes) | after -1 ATR came first: ended above C0 | everything | 13.6% | -1.8 pp [-2.6 pp, -1.0 pp] | 0.0095 | 0/3 |
| daily | S02 Emerging bull (all regimes) | best high of the window from C0 (MFE) | everything | 1.45 | +0.11 [+0.06, +0.16] | 0.0182 | 0/3 |
| daily | S01 Strong bull x Broad bullish | reached -1 ATR at some point in the 5 sessions | same regime, all states | 44.9% | +5.5 pp [+3.0 pp, +7.9 pp] | 0.0182 | 0/3 |
| daily | S02 Emerging bull (all regimes) | reached +2 ATR at some point in the 5 sessions | everything | 23.6% | +2.6 pp [+1.3 pp, +3.9 pp] | 0.0288 | 0/3 |
| daily | S07 Neutral range x Broad bullish | reached -1 ATR at some point in the 5 sessions | same regime, all states | 34.8% | -4.6 pp [-6.7 pp, -2.4 pp] | 0.0321 | 0/3 |
| daily | S02 Emerging bull x Broad bullish | best high of the window from C0 (MFE) | everything | 1.54 | +0.20 [+0.10, +0.29] | 0.0330 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | after -1 ATR came first: ended above C0 | everything | 10.1% | -5.4 pp [-7.6 pp, -2.5 pp] | 0.0330 | 0/3 |
| daily | S09 Emerging bear x Broad bullish | after -1 ATR came first: ended above C0 | interaction | 10.1% | -5.4 pp [-7.9 pp, -2.6 pp] | 0.0346 | 0/3 |
| intraday | S02 Emerging bull (all regimes) | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | everything | 4.4% | +1.1 pp [+0.8 pp, +1.4 pp] | 0.0002 | 0/2 |
| intraday | S09 Emerging bear (all regimes) | share of 3-minute paths in intraday region J07 | everything | 0.7% | -0.6 pp [-0.8 pp, -0.4 pp] | 0.0003 | 0/2 |
| intraday | S09 Emerging bear x Narrow bullish | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | same regime, all states | 2.1% | -1.3 pp [-1.6 pp, -0.9 pp] | 0.0008 | 0/1 |
| intraday | S01 Strong bull (all regimes) | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | everything | 4.3% | +1.0 pp [+0.7 pp, +1.4 pp] | 0.0019 | 0/2 |
| intraday | S07 Neutral range (all regimes) | after -1 ATR came first: back to C0 later (3-minute) | everything | 29.8% | -3.3 pp [-4.6 pp, -2.0 pp] | 0.0095 | 0/2 |
| intraday | S07 Neutral range x Broad bullish | after -1 ATR came first: back to C0 later (3-minute) | same regime, all states | 27.3% | -5.8 pp [-7.5 pp, -3.6 pp] | 0.0097 | 0/1 |
| intraday | S09 Emerging bear (all regimes) | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | everything | 2.6% | -0.7 pp [-1.1 pp, -0.4 pp] | 0.0131 | 0/2 |
| intraday | S09 Emerging bear x Broad bullish | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | same regime, all states | 2.5% | -1.4 pp [-1.9 pp, -0.9 pp] | 0.0180 | 0/1 |
| intraday | S02 Emerging bull (all regimes) | share of 3-minute paths in intraday region J07 | everything | 2.0% | +0.7 pp [+0.4 pp, +1.0 pp] | 0.0200 | 0/2 |
| intraday | S08 Bear continuation x Mixed | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | everything | 1.5% | -1.8 pp [-2.4 pp, -1.1 pp] | 0.0288 | 0/0 |
| intraday | S02 Emerging bull x Narrow bullish | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | same regime, all states | 4.8% | +1.4 pp [+0.9 pp, +2.0 pp] | 0.0288 | 0/1 |
| intraday | S09 Emerging bear x Broad bearish | share of 3-minute paths in intraday region J07 | everything | 0.4% | -0.9 pp [-1.3 pp, -0.6 pp] | 0.0288 | 0/1 |
| intraday | S09 Emerging bear x Narrow bullish | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | everything | 2.1% | -1.2 pp [-1.6 pp, -0.6 pp] | 0.0360 | 0/1 |

_29 candidates in 12 groups. 'interaction' = (cell - same state) - (same regime - everything). A strong effect in one state also shifts the 'everything' and 'same regime' baselines, so small opposite differences elsewhere are its mirror image, not separate candidates._

Unstable: 1 (passed, but the sign flips in more than a third of the supported years; in labels.csv).

## Event pages: state x tl_state event x event age

145 of 330 pages meet the minimum support (each state and all states x the event shown at T0 with its status x age bins [[0, 2], [3, 5], [6, 10], [11, 99]] sessions since the event started). Each page is tested against the same state with no event at T0 on r5_a, r10_a, mfe10_a, mae10_a, dly1, ddly5; the event tests are their own false-discovery family. All pages and values: atlas/daily/event_pages.csv.

| page | measure | page value | same state, no event | difference [95%] | q | years against the sign |
|---|---|---|---|---|---|---|
| all states / S04 breakout NEW, age 0-2 | best high of 10 sessions from C0 | 2.31 | 2.02 | +0.29 [+0.18, +0.39] | 0.0003 | 0/3 |
| S01 / S04 breakout NEW, age 0-2 | best high of 10 sessions from C0 | 2.40 | 1.99 | +0.41 [+0.24, +0.57] | 0.0032 | 0/3 |
| UNKNOWN / S04 breakout NEW, age 0-2 | best high of 10 sessions from C0 | 2.33 | 2.02 | +0.31 [+0.18, +0.44] | 0.0032 | 0/3 |
| S03 / S04 breakout NEW, age 0-2 | best high of 10 sessions from C0 | 2.42 | 2.11 | +0.31 [+0.18, +0.44] | 0.0032 | 0/3 |
| all states / failed breakdown (bear trap), age 0-2 | best high of 10 sessions from C0 | 1.72 | 2.02 | -0.30 [-0.43, -0.17] | 0.0032 | 0/3 |
| UNKNOWN / S04 breakout NEW, age 0-2 | worst low of 10 sessions from C0 | -1.64 | -1.37 | -0.26 [-0.38, -0.15] | 0.0032 | 0/3 |
| S07 / S04 breakout NEW, age 0-2 | best high of 10 sessions from C0 | 2.36 | 2.06 | +0.30 [+0.17, +0.44] | 0.0041 | 0/3 |
| all states / failed breakdown (bear trap), age 3-5 | best high of 10 sessions from C0 | 1.76 | 2.02 | -0.26 [-0.39, -0.13] | 0.0112 | 0/3 |
| S07 / S11 failed breakout, age 11-99 | best high of 10 sessions from C0 | 1.75 | 2.06 | -0.31 [-0.47, -0.16] | 0.0132 | 0/3 |
| S01 / S04 breakout NEW, age 0-2 | worst low of 10 sessions from C0 | -1.71 | -1.47 | -0.24 [-0.36, -0.13] | 0.0132 | 0/3 |
| S07 / S10 breakdown NEW, age 0-2 | best high of 10 sessions from C0 | 1.72 | 2.06 | -0.33 [-0.51, -0.17] | 0.0137 | 0/3 |
| S03 / S10 breakdown NEW, age 0-2 | best high of 10 sessions from C0 | 1.80 | 2.11 | -0.31 [-0.46, -0.15] | 0.0137 | 0/3 |
| all states / S10 breakdown CONFIRMED, age 3-5 | best high of 10 sessions from C0 | 1.66 | 2.02 | -0.37 [-0.55, -0.19] | 0.0137 | 0/3 |
| S07 / S11 failed breakout, age 6-10 | best high of 10 sessions from C0 | 1.78 | 2.06 | -0.28 [-0.43, -0.13] | 0.0225 | 0/3 |
| all states / S04 breakout NEW, age 0-2 | worst low of 10 sessions from C0 | -1.61 | -1.41 | -0.20 [-0.31, -0.09] | 0.0239 | 0/3 |
| all states / S10 breakdown CONFIRMED, age 6-10 | best high of 10 sessions from C0 | 1.72 | 2.02 | -0.31 [-0.47, -0.13] | 0.0279 | 0/3 |
| S07 / S10 breakdown NEW, age 3-5 | best high of 10 sessions from C0 | 1.62 | 2.06 | -0.44 [-0.67, -0.18] | 0.0412 | 0/0 |

_17 event candidates on 14 pages (first 80 by q; all in event_tests.csv)._

| page | paths | dates | 5-day close from C0 | 10-day close from C0 | best high of 10 sessions from C0 | worst low of 10 sessions from C0 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) |
|---|---|---|---|---|---|---|---|---|
| all states / S04 breakout NEW, age 0-2 | 48,480 | 739 | 0.18 [0.06, 0.29] | 0.38 [0.15, 0.59] | 2.31 [2.19, 2.43] | -1.61 [-1.76, -1.48] | 0.14% [-0.34%, 0.58%] | 0.27% [-0.16%, 0.70%] |
| all states / S10 breakdown NEW, age 0-2 | 39,718 | 727 | 0.01 [-0.31, 0.28] | 0.00 [-0.56, 0.47] | 1.74 [1.57, 1.92] | -1.67 [-2.20, -1.25] | -0.22% [-1.95%, 1.23%] | -0.02% [-1.06%, 1.06%] |
| all states / S11 failed breakout, age 6-10 | 32,382 | 742 | 0.14 [-0.01, 0.27] | 0.29 [0.04, 0.52] | 1.93 [1.79, 2.06] | -1.42 [-1.60, -1.25] | 0.23% [-0.42%, 0.81%] | 0.04% [-0.53%, 0.64%] |
| all states / failed breakdown (bear trap), age 6-10 | 27,229 | 735 | 0.15 [-0.01, 0.31] | 0.25 [-0.04, 0.53] | 1.86 [1.69, 2.04] | -1.34 [-1.56, -1.14] | 0.45% [-0.38%, 1.33%] | -0.17% [-0.86%, 0.52%] |
| S09 / S10 breakdown NEW, age 0-2 | 25,146 | 704 | -0.02 [-0.36, 0.28] | -0.07 [-0.68, 0.44] | 1.69 [1.51, 1.88] | -1.70 [-2.29, -1.24] | -0.40% [-2.38%, 1.24%] | -0.07% [-1.23%, 1.25%] |
| all states / S04 breakout CONFIRMED, age 6-10 | 23,490 | 718 | 0.21 [0.07, 0.35] | 0.36 [0.12, 0.59] | 2.07 [1.92, 2.21] | -1.46 [-1.62, -1.30] | 0.63% [0.02%, 1.22%] | -0.34% [-0.88%, 0.22%] |
| all states / S11 failed breakout, age 3-5 | 21,030 | 737 | 0.15 [0.02, 0.28] | 0.28 [0.05, 0.51] | 1.96 [1.82, 2.09] | -1.46 [-1.62, -1.30] | 0.30% [-0.26%, 0.81%] | -0.13% [-0.60%, 0.36%] |
| all states / S04 breakout CONFIRMED, age 3-5 | 20,570 | 714 | 0.20 [0.07, 0.32] | 0.39 [0.15, 0.60] | 2.20 [2.06, 2.33] | -1.54 [-1.70, -1.40] | 0.45% [-0.08%, 0.93%] | 0.08% [-0.38%, 0.62%] |
| all states / failed breakdown (bear trap), age 3-5 | 19,350 | 724 | 0.06 [-0.10, 0.22] | 0.21 [-0.09, 0.46] | 1.76 [1.62, 1.90] | -1.37 [-1.60, -1.17] | 0.13% [-0.68%, 0.89%] | 0.20% [-0.49%, 0.96%] |
| S02 / S04 breakout NEW, age 0-2 | 15,224 | 705 | 0.17 [0.03, 0.29] | 0.41 [0.14, 0.65] | 2.29 [2.14, 2.42] | -1.59 [-1.78, -1.44] | 0.15% [-0.38%, 0.62%] | 0.37% [-0.09%, 0.85%] |
| UNKNOWN / S04 breakout NEW, age 0-2 | 14,639 | 711 | 0.17 [0.05, 0.28] | 0.34 [0.10, 0.56] | 2.33 [2.21, 2.44] | -1.64 [-1.79, -1.50] | 0.20% [-0.32%, 0.65%] | 0.12% [-0.38%, 0.64%] |
| all states / S10 breakdown CONFIRMED, age 6-10 | 13,576 | 671 | 0.03 [-0.18, 0.23] | 0.14 [-0.22, 0.44] | 1.72 [1.55, 1.89] | -1.40 [-1.70, -1.16] | 0.12% [-1.12%, 1.38%] | 0.28% [-0.81%, 1.34%] |
| all states / S10 breakdown CONFIRMED, age 3-5 | 13,497 | 674 | -0.01 [-0.38, 0.30] | -0.03 [-0.55, 0.42] | 1.66 [1.47, 1.84] | -1.56 [-2.07, -1.14] | -0.65% [-2.87%, 1.21%] | 0.61% [-1.25%, 2.96%] |
| all states / S11 failed breakout, age 11-99 | 12,682 | 717 | 0.17 [0.01, 0.30] | 0.29 [0.01, 0.54] | 1.96 [1.81, 2.11] | -1.39 [-1.59, -1.22] | 0.32% [-0.39%, 0.92%] | -0.10% [-0.72%, 0.55%] |
| all states / S04 breakout CONFIRMED, age 11-99 | 11,376 | 698 | 0.17 [0.01, 0.31] | 0.29 [-0.00, 0.53] | 1.97 [1.82, 2.12] | -1.44 [-1.64, -1.27] | 0.43% [-0.27%, 1.04%] | -0.29% [-0.93%, 0.40%] |
| all states / failed breakdown (bear trap), age 11-99 | 10,114 | 643 | 0.16 [-0.06, 0.35] | 0.26 [-0.05, 0.55] | 1.90 [1.70, 2.12] | -1.37 [-1.62, -1.15] | 0.43% [-0.43%, 1.19%] | -0.57% [-1.45%, 0.47%] |
| S09 / S10 breakdown CONFIRMED, age 3-5 | 9,826 | 636 | -0.07 [-0.45, 0.25] | -0.12 [-0.66, 0.32] | 1.57 [1.40, 1.74] | -1.61 [-2.15, -1.18] | -0.94% [-3.18%, 0.88%] | 0.60% [-1.37%, 3.11%] |
| S09 / failed breakdown (bear trap), age 6-10 | 8,677 | 658 | 0.11 [-0.06, 0.27] | 0.16 [-0.16, 0.46] | 1.74 [1.56, 1.92] | -1.35 [-1.61, -1.13] | 0.27% [-0.66%, 1.18%] | -0.27% [-1.01%, 0.47%] |
| S02 / S11 failed breakout, age 6-10 | 8,535 | 709 | 0.15 [-0.01, 0.30] | 0.32 [0.05, 0.58] | 2.01 [1.85, 2.17] | -1.42 [-1.61, -1.25] | 0.26% [-0.43%, 0.86%] | 0.04% [-0.58%, 0.65%] |
| S09 / failed breakdown (bear trap), age 3-5 | 8,396 | 646 | 0.04 [-0.13, 0.20] | 0.11 [-0.18, 0.38] | 1.67 [1.53, 1.81] | -1.39 [-1.65, -1.18] | -0.06% [-0.90%, 0.76%] | 0.05% [-0.71%, 0.85%] |
| all states / S11 failed breakout, age 0-2 | 8,014 | 711 | 0.08 [-0.05, 0.21] | 0.22 [-0.01, 0.44] | 1.94 [1.80, 2.07] | -1.55 [-1.71, -1.39] | 0.01% [-0.54%, 0.54%] | 0.29% [-0.19%, 0.84%] |
| all states / failed breakdown (bear trap), age 0-2 | 7,990 | 647 | 0.05 [-0.17, 0.26] | 0.12 [-0.21, 0.40] | 1.72 [1.58, 1.88] | -1.43 [-1.76, -1.18] | -0.20% [-1.26%, 0.75%] | 0.48% [-0.73%, 1.78%] |
| UNKNOWN / S04 breakout CONFIRMED, age 3-5 | 7,167 | 672 | 0.22 [0.07, 0.34] | 0.37 [0.12, 0.60] | 2.24 [2.09, 2.38] | -1.55 [-1.71, -1.40] | 0.57% [-0.06%, 1.12%] | -0.07% [-0.57%, 0.49%] |
| S02 / S04 breakout CONFIRMED, age 6-10 | 7,149 | 688 | 0.24 [0.07, 0.40] | 0.42 [0.13, 0.68] | 2.13 [1.95, 2.31] | -1.44 [-1.63, -1.26] | 0.68% [-0.06%, 1.33%] | -0.21% [-0.91%, 0.49%] |
| UNKNOWN / S04 breakout CONFIRMED, age 6-10 | 7,081 | 682 | 0.20 [0.05, 0.35] | 0.35 [0.11, 0.58] | 2.06 [1.90, 2.21] | -1.45 [-1.62, -1.29] | 0.62% [-0.04%, 1.26%] | -0.39% [-0.98%, 0.26%] |
| S01 / S04 breakout NEW, age 0-2 | 6,972 | 652 | 0.19 [0.04, 0.34] | 0.42 [0.13, 0.67] | 2.40 [2.23, 2.58] | -1.71 [-1.88, -1.55] | 0.24% [-0.43%, 0.85%] | 0.22% [-0.41%, 0.83%] |
| S02 / S04 breakout CONFIRMED, age 3-5 | 6,915 | 670 | 0.19 [0.04, 0.33] | 0.42 [0.16, 0.66] | 2.19 [2.03, 2.33] | -1.50 [-1.70, -1.33] | 0.41% [-0.18%, 0.92%] | 0.21% [-0.33%, 0.81%] |
| S01 / S11 failed breakout, age 6-10 | 6,736 | 681 | 0.12 [-0.04, 0.27] | 0.35 [0.08, 0.61] | 1.98 [1.81, 2.15] | -1.46 [-1.66, -1.28] | 0.22% [-0.55%, 0.93%] | 0.36% [-0.41%, 1.15%] |
| S07 / failed breakdown (bear trap), age 6-10 | 6,632 | 637 | 0.13 [-0.04, 0.31] | 0.24 [-0.05, 0.53] | 1.94 [1.74, 2.15] | -1.41 [-1.59, -1.23] | 0.20% [-0.52%, 0.97%] | 0.07% [-0.62%, 0.82%] |
| S01 / S04 breakout CONFIRMED, age 6-10 | 6,524 | 673 | 0.18 [0.05, 0.32] | 0.37 [0.14, 0.59] | 2.06 [1.92, 2.21] | -1.52 [-1.68, -1.35] | 0.56% [-0.10%, 1.23%] | -0.19% [-0.86%, 0.53%] |
| all states / S10 breakdown CONFIRMED, age 11-99 | 6,416 | 568 | 0.17 [-0.11, 0.39] | 0.22 [-0.11, 0.54] | 1.82 [1.62, 2.01] | -1.32 [-1.59, -1.07] | 0.79% [-0.53%, 1.95%] | -0.84% [-1.93%, 0.50%] |
| UNKNOWN / S11 failed breakout, age 6-10 | 6,414 | 704 | 0.14 [-0.01, 0.28] | 0.29 [0.05, 0.52] | 1.87 [1.73, 2.02] | -1.38 [-1.57, -1.21] | 0.29% [-0.37%, 0.89%] | -0.02% [-0.63%, 0.57%] |
| UNKNOWN / S10 breakdown NEW, age 0-2 | 6,136 | 634 | 0.10 [-0.13, 0.32] | 0.21 [-0.17, 0.57] | 1.85 [1.67, 2.05] | -1.53 [-1.85, -1.26] | 0.30% [-0.77%, 1.30%] | 0.03% [-0.84%, 0.91%] |
| S02 / S11 failed breakout, age 3-5 | 6,002 | 666 | 0.20 [0.03, 0.34] | 0.32 [0.05, 0.58] | 2.02 [1.86, 2.18] | -1.45 [-1.63, -1.28] | 0.51% [-0.15%, 1.07%] | -0.35% [-0.89%, 0.23%] |
| S09 / S10 breakdown CONFIRMED, age 6-10 | 5,862 | 594 | -0.05 [-0.25, 0.13] | 0.00 [-0.37, 0.31] | 1.60 [1.47, 1.74] | -1.48 [-1.81, -1.22] | -0.43% [-1.62%, 0.69%] | 0.40% [-0.64%, 1.40%] |
| UNKNOWN / failed breakdown (bear trap), age 6-10 | 5,534 | 625 | 0.12 [-0.07, 0.30] | 0.23 [-0.08, 0.52] | 1.80 [1.61, 1.99] | -1.33 [-1.56, -1.11] | 0.27% [-0.61%, 1.22%] | 0.04% [-0.77%, 0.86%] |
| UNKNOWN / S11 failed breakout, age 3-5 | 5,073 | 665 | 0.10 [-0.05, 0.23] | 0.21 [-0.04, 0.45] | 1.89 [1.75, 2.02] | -1.48 [-1.66, -1.30] | 0.08% [-0.51%, 0.65%] | -0.07% [-0.64%, 0.51%] |
| S06 / S04 breakout NEW, age 0-2 | 4,985 | 579 | 0.09 [-0.10, 0.25] | 0.27 [-0.09, 0.57] | 2.11 [1.89, 2.33] | -1.55 [-1.77, -1.40] | -0.45% [-1.17%, 0.26%] | 0.63% [-0.20%, 1.49%] |
| S09 / failed breakdown (bear trap), age 0-2 | 4,264 | 541 | 0.03 [-0.20, 0.24] | 0.05 [-0.32, 0.36] | 1.66 [1.52, 1.81] | -1.46 [-1.82, -1.17] | -0.32% [-1.47%, 0.69%] | 0.40% [-0.93%, 1.86%] |
| S08 / failed breakdown (bear trap), age 6-10 | 4,242 | 543 | 0.30 [0.05, 0.51] | 0.43 [0.02, 0.77] | 1.97 [1.72, 2.24] | -1.21 [-1.51, -0.98] | 1.43% [-0.07%, 3.01%] | -0.83% [-1.96%, 0.28%] |

_The 40 largest supported event pages (descriptive)._

## The delay curve: does waiting help?

dly_d = entry at the open of T+d, exit at the open of T+d+5, net of 35 bp (d = 1 is BigMove's OPEN6 timing). Every d uses the same paths (all 15 sessions present, no corporate-action suspect), so the differences are paired. Tests: per group and d = 2..10, the mean of dly_d - dly_1 against zero; their own false-discovery family.

| group | d=1 | d=2 | d=3 | d=4 | d=5 | d=6 | d=7 | d=8 | d=9 | d=10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Everything | 0.25% | 0.25% | 0.25% | 0.24% | 0.24% | 0.24% | 0.23% | 0.23% | 0.22% | 0.22% |
| S01 Strong bull (all regimes) | 0.32% | 0.34% | 0.36% | 0.40% | 0.43% | 0.44% | 0.44% | 0.43% | 0.40% | 0.36% |
| S02 Emerging bull (all regimes) | 0.33% | 0.33% | 0.33% | 0.34% | 0.35% | 0.34% | 0.30% | 0.26% | 0.23% | 0.20% |
| S03 Bull consolidation (all regimes) | 0.45% | 0.47% | 0.48% | 0.47% | 0.47% | 0.48% | 0.47% | 0.46% | 0.45% | 0.44% |
| S06 Reversal attempt (all regimes) | 0.18% | 0.19% | 0.19% | 0.18% | 0.15% | 0.13% | 0.08% | 0.04% | 0.01% | 0.00% |
| S07 Neutral range (all regimes) | 0.27% | 0.27% | 0.27% | 0.24% | 0.21% | 0.19% | 0.19% | 0.17% | 0.16% | 0.15% |
| S08 Bear continuation (all regimes) | 0.77% | 0.79% | 0.77% | 0.71% | 0.66% | 0.64% | 0.63% | 0.65% | 0.67% | 0.66% |
| S09 Emerging bear (all regimes) | -0.23% | -0.24% | -0.25% | -0.22% | -0.19% | -0.17% | -0.13% | -0.07% | -0.03% | 0.01% |
| S12 Unstable (all regimes) | 1.98% | 2.06% | 2.01% | 1.77% | 1.23% | 0.87% | 0.41% | 0.54% | 0.63% | 0.70% |
| UNKNOWN Unknown (all regimes) | 0.37% | 0.34% | 0.32% | 0.31% | 0.30% | 0.28% | 0.28% | 0.28% | 0.28% | 0.28% |
| Broad bullish (all states) | 0.53% | 0.41% | 0.27% | 0.16% | 0.09% | 0.02% | 0.02% | 0.10% | 0.17% | 0.22% |
| Narrow bullish (all states) | 0.37% | 0.39% | 0.55% | 0.60% | 0.58% | 0.57% | 0.53% | 0.42% | 0.31% | 0.21% |
| Mixed (all states) | -0.21% | -0.38% | -0.41% | -0.44% | -0.44% | -0.36% | -0.16% | -0.06% | -0.08% | -0.16% |
| Broad bearish (all states) | -0.10% | 0.33% | 0.49% | 0.57% | 0.65% | 0.56% | 0.36% | 0.23% | 0.28% | 0.65% |
| High stress (all states) | 0.03% | 0.11% | 0.01% | 0.12% | 0.26% | 0.42% | 0.42% | 0.42% | 0.45% | 0.32% |

_Mean net return of the delayed trade (point estimates; intervals for every group in delay_curve.csv)._

No delay passes the false-discovery control with a stable yearly sign: on these pages, waiting neither helps nor hurts beyond chance.

## Daily paths in detail (margins)

### Distributions (ATR units from C0, 2020-2026)

| group | measure | 5th | 25th | median | 75th | 95th |
|---|---|---|---|---|---|---|
| Everything | 5-day close | -2.11 [-2.36, -1.89] | -0.76 [-0.90, -0.64] | +0.02 [-0.08, +0.12] | +0.91 [+0.79, +1.01] | +2.75 [+2.60, +2.91] |
| Everything | MFE | +0.11 [+0.06, +0.13] | +0.48 [+0.44, +0.51] | +0.98 [+0.92, +1.04] | +1.79 [+1.70, +1.89] | +3.81 [+3.64, +3.98] |
| Everything | MAE | -2.86 [-3.16, -2.62] | -1.46 [-1.61, -1.33] | -0.78 [-0.87, -0.71] | -0.33 [-0.38, -0.30] | +0.05 [+0.04, +0.07] |
| Broad bullish (all states) | 5-day close | -1.93 [-2.17, -1.72] | -0.73 [-0.89, -0.59] | +0.03 [-0.11, +0.16] | +0.98 [+0.81, +1.11] | +3.06 [+2.86, +3.24] |
| Broad bullish (all states) | MFE | +0.15 [+0.12, +0.17] | +0.51 [+0.47, +0.56] | +1.05 [+0.97, +1.13] | +1.97 [+1.85, +2.09] | +4.25 [+4.06, +4.45] |
| Broad bullish (all states) | MAE | -2.69 [-3.02, -2.40] | -1.40 [-1.58, -1.26] | -0.77 [-0.88, -0.69] | -0.33 [-0.39, -0.29] | +0.05 [+0.03, +0.07] |
| Narrow bullish (all states) | 5-day close | -2.05 [-2.35, -1.76] | -0.76 [-0.96, -0.58] | +0.02 [-0.15, +0.18] | +0.92 [+0.73, +1.11] | +2.86 [+2.61, +3.08] |
| Narrow bullish (all states) | MFE | +0.11 [+0.07, +0.13] | +0.47 [+0.42, +0.52] | +0.97 [+0.88, +1.07] | +1.80 [+1.66, +1.95] | +3.89 [+3.64, +4.12] |
| Narrow bullish (all states) | MAE | -2.81 [-3.17, -2.47] | -1.46 [-1.70, -1.26] | -0.78 [-0.93, -0.67] | -0.33 [-0.42, -0.27] | +0.04 [+0.01, +0.07] |
| Mixed (all states) | 5-day close | -2.18 [-2.54, -1.73] | -0.84 [-1.16, -0.55] | -0.05 [-0.33, +0.19] | +0.81 [+0.53, +1.03] | +2.46 [+2.14, +2.74] |
| Mixed (all states) | MFE | +0.10 [+0.02, +0.15] | +0.47 [+0.39, +0.56] | +0.94 [+0.80, +1.08] | +1.70 [+1.51, +1.88] | +3.49 [+3.18, +3.82] |
| Mixed (all states) | MAE | -2.82 [-3.17, -2.32] | -1.47 [-1.82, -1.16] | -0.78 [-1.02, -0.61] | -0.32 [-0.45, -0.24] | +0.06 [+0.01, +0.09] |
| Broad bearish (all states) | 5-day close | -2.19 [-2.70, -1.45] | -0.77 [-1.24, -0.32] | +0.04 [-0.32, +0.33] | +0.80 [+0.49, +1.05] | +2.21 [+1.89, +2.49] |
| Broad bearish (all states) | MFE | +0.00 [-0.09, +0.13] | +0.42 [+0.32, +0.56] | +0.85 [+0.68, +1.04] | +1.50 [+1.27, +1.71] | +2.99 [+2.71, +3.27] |
| Broad bearish (all states) | MAE | -2.87 [-3.36, -2.10] | -1.49 [-1.98, -1.05] | -0.76 [-1.12, -0.56] | -0.33 [-0.49, -0.23] | +0.05 [-0.02, +0.09] |
| High stress (all states) | 5-day close | -2.62 [-3.77, -1.56] | -0.76 [-1.37, -0.41] | +0.07 [-0.25, +0.29] | +0.90 [+0.65, +1.11] | +2.47 [+2.19, +2.75] |
| High stress (all states) | MFE | +0.00 [-0.22, +0.16] | +0.48 [+0.38, +0.59] | +0.97 [+0.83, +1.12] | +1.71 [+1.53, +1.88] | +3.35 [+3.10, +3.61] |
| High stress (all states) | MAE | -3.60 [-5.32, -2.35] | -1.58 [-2.24, -1.19] | -0.83 [-1.15, -0.63] | -0.35 [-0.51, -0.25] | +0.09 [+0.01, +0.14] |
| S01 Strong bull (all regimes) | 5-day close | -2.14 [-2.35, -1.94] | -0.80 [-0.94, -0.68] | +0.00 [-0.11, +0.10] | +0.93 [+0.81, +1.03] | +3.02 [+2.84, +3.20] |
| S01 Strong bull (all regimes) | MFE | +0.13 [+0.10, +0.14] | +0.49 [+0.46, +0.53] | +1.01 [+0.95, +1.07] | +1.86 [+1.77, +1.94] | +4.08 [+3.88, +4.28] |
| S01 Strong bull (all regimes) | MAE | -2.95 [-3.18, -2.71] | -1.58 [-1.72, -1.43] | -0.88 [-0.98, -0.80] | -0.39 [-0.44, -0.34] | +0.05 [+0.04, +0.07] |
| S02 Emerging bull (all regimes) | 5-day close | -2.06 [-2.28, -1.86] | -0.80 [-0.95, -0.67] | +0.02 [-0.10, +0.12] | +0.96 [+0.82, +1.07] | +2.99 [+2.81, +3.15] |
| S02 Emerging bull (all regimes) | MFE | +0.13 [+0.10, +0.14] | +0.51 [+0.48, +0.55] | +1.05 [+0.98, +1.11] | +1.93 [+1.81, +2.03] | +4.14 [+3.94, +4.34] |
| S02 Emerging bull (all regimes) | MAE | -2.84 [-3.14, -2.58] | -1.51 [-1.67, -1.37] | -0.84 [-0.94, -0.77] | -0.37 [-0.43, -0.33] | +0.04 [+0.02, +0.06] |
| S03 Bull consolidation (all regimes) | 5-day close | -2.00 [-2.22, -1.81] | -0.74 [-0.86, -0.62] | +0.02 [-0.08, +0.11] | +0.95 [+0.83, +1.06] | +2.94 [+2.76, +3.12] |
| S03 Bull consolidation (all regimes) | MFE | +0.13 [+0.10, +0.15] | +0.48 [+0.45, +0.52] | +0.99 [+0.93, +1.06] | +1.87 [+1.77, +1.97] | +4.01 [+3.81, +4.20] |
| S03 Bull consolidation (all regimes) | MAE | -2.84 [-3.10, -2.58] | -1.45 [-1.61, -1.30] | -0.79 [-0.89, -0.70] | -0.34 [-0.39, -0.30] | +0.04 [+0.02, +0.06] |
| S06 Reversal attempt (all regimes) | 5-day close | -2.05 [-2.34, -1.77] | -0.77 [-0.99, -0.61] | +0.00 [-0.17, +0.17] | +0.91 [+0.69, +1.11] | +2.71 [+2.43, +3.00] |
| S06 Reversal attempt (all regimes) | MFE | +0.09 [+0.03, +0.13] | +0.48 [+0.42, +0.54] | +0.98 [+0.87, +1.11] | +1.79 [+1.61, +1.97] | +3.77 [+3.43, +4.14] |
| S06 Reversal attempt (all regimes) | MAE | -2.70 [-2.99, -2.41] | -1.40 [-1.62, -1.24] | -0.77 [-0.90, -0.67] | -0.33 [-0.40, -0.28] | +0.05 [+0.02, +0.08] |
| S07 Neutral range (all regimes) | 5-day close | -2.02 [-2.24, -1.80] | -0.75 [-0.89, -0.61] | +0.01 [-0.10, +0.12] | +0.89 [+0.76, +1.02] | +2.78 [+2.60, +2.97] |
| S07 Neutral range (all regimes) | MFE | +0.11 [+0.07, +0.13] | +0.46 [+0.43, +0.50] | +0.95 [+0.88, +1.03] | +1.79 [+1.68, +1.91] | +3.87 [+3.69, +4.09] |
| S07 Neutral range (all regimes) | MAE | -2.72 [-2.97, -2.49] | -1.39 [-1.54, -1.25] | -0.74 [-0.84, -0.67] | -0.32 [-0.37, -0.28] | +0.04 [+0.03, +0.06] |
| S08 Bear continuation (all regimes) | 5-day close | -2.19 [-2.84, -1.74] | -0.68 [-0.97, -0.45] | +0.14 [-0.08, +0.31] | +1.01 [+0.81, +1.19] | +2.66 [+2.39, +2.97] |
| S08 Bear continuation (all regimes) | MFE | +0.04 [-0.08, +0.13] | +0.48 [+0.41, +0.55] | +0.99 [+0.88, +1.10] | +1.78 [+1.63, +1.93] | +3.58 [+3.32, +3.88] |
| S08 Bear continuation (all regimes) | MAE | -2.94 [-3.93, -2.40] | -1.36 [-1.69, -1.11] | -0.68 [-0.84, -0.56] | -0.26 [-0.34, -0.21] | +0.09 [+0.06, +0.13] |
| S09 Emerging bear (all regimes) | 5-day close | -2.35 [-3.01, -1.84] | -0.77 [-1.03, -0.57] | +0.04 [-0.12, +0.17] | +0.83 [+0.70, +0.95] | +2.28 [+2.15, +2.43] |
| S09 Emerging bear (all regimes) | MFE | +0.05 [-0.05, +0.12] | +0.45 [+0.40, +0.51] | +0.92 [+0.84, +1.00] | +1.62 [+1.53, +1.71] | +3.16 [+3.02, +3.34] |
| S09 Emerging bear (all regimes) | MAE | -3.15 [-4.02, -2.57] | -1.49 [-1.78, -1.26] | -0.76 [-0.91, -0.65] | -0.30 [-0.37, -0.26] | +0.07 [+0.05, +0.09] |
| S12 Unstable (all regimes) | 5-day close | -2.71 [-3.73, -1.07] | -0.57 [-1.16, -0.21] | +0.19 [-0.27, +0.55] | +1.00 [+0.33, +1.52] | +3.91 [+2.10, +4.78] |
| S12 Unstable (all regimes) | MFE | +0.09 [-0.07, +0.22] | +0.48 [+0.27, +0.64] | +0.93 [+0.58, +1.29] | +1.72 [+1.16, +2.25] | +4.63 [+2.62, +6.00] |
| S12 Unstable (all regimes) | MAE | -3.34 [-4.08, -1.55] | -1.23 [-1.97, -0.88] | -0.61 [-0.98, -0.48] | -0.29 [-0.46, -0.18] | +0.10 [-0.01, +0.22] |
| UNKNOWN Unknown (all regimes) | 5-day close | -2.05 [-2.23, -1.87] | -0.75 [-0.88, -0.63] | +0.01 [-0.09, +0.11] | +0.91 [+0.79, +1.01] | +2.81 [+2.64, +2.97] |
| UNKNOWN Unknown (all regimes) | MFE | +0.12 [+0.08, +0.13] | +0.48 [+0.45, +0.52] | +0.99 [+0.92, +1.05] | +1.82 [+1.72, +1.91] | +3.89 [+3.69, +4.08] |
| UNKNOWN Unknown (all regimes) | MAE | -2.78 [-2.99, -2.59] | -1.45 [-1.59, -1.32] | -0.79 [-0.87, -0.71] | -0.34 [-0.38, -0.30] | +0.05 [+0.04, +0.07] |

_Intervals: the bootstrap distribution of each group's CDF on a 0.1 ATR grid, inverted at each quantile._

### Timing of the window's high and low (everything)

_(chart in ATLAS.html: share of paths whose 5-day high came in each session)_

_(chart in ATLAS.html: share of paths whose 5-day low came in each session)_

### Excursions, order, recovery, continuation by state (all regimes)

| group | reached +1 ATR at some point in the 5 sessions | reached -1 ATR at some point in the 5 sessions | reached +2 ATR at some point in the 5 sessions | reached -2 ATR at some point in the 5 sessions | ord_a1_1: both reached in one session, order unknown at daily resolution | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: back to C0 later | after -1 ATR came first: went on to +1 ATR | after reaching -2 ATR: ended above C0 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | after a session-1 close >= +0.5 ATR: ended below C0 | after a session-1 close <= -0.5 ATR: session 5 closed lower still | after a session-1 close <= -0.5 ATR: ended above C0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Everything | 49.1% | 40.3% | 21.0% | 13.7% | 0.6% | 55.6% | 35.4% | 10.7% | 5.4% | 49.7% | 21.0% | 49.2% | 24.1% |
| S01 Strong bull (all regimes) | 50.3% | 44.8% | 22.3% | 15.6% | 0.8% | 53.7% | 38.8% | 12.1% | 6.5% | 49.7% | 22.4% | 47.9% | 25.0% |
| S02 Emerging bull (all regimes) | 51.9% | 42.7% | 23.6% | 14.2% | 0.8% | 55.9% | 37.4% | 12.0% | 6.0% | 48.9% | 21.6% | 49.1% | 24.2% |
| S03 Bull consolidation (all regimes) | 49.7% | 40.4% | 22.6% | 13.4% | 0.7% | 55.9% | 35.9% | 10.9% | 6.3% | 50.7% | 21.1% | 48.4% | 24.0% |
| S06 Reversal attempt (all regimes) | 49.3% | 39.3% | 20.9% | 12.1% | 0.5% | 56.5% | 32.7% | 10.0% | 4.7% | 49.6% | 22.1% | 50.6% | 23.4% |
| S07 Neutral range (all regimes) | 48.0% | 38.2% | 21.0% | 12.3% | 0.4% | 56.5% | 32.0% | 9.0% | 4.8% | 50.3% | 20.2% | 49.9% | 23.1% |
| S08 Bear continuation (all regimes) | 49.8% | 35.8% | 20.4% | 13.2% | 0.4% | 58.5% | 34.1% | 10.5% | 4.9% | 53.9% | 18.1% | 49.0% | 25.3% |
| S09 Emerging bear (all regimes) | 46.5% | 40.0% | 16.7% | 15.1% | 0.5% | 53.6% | 35.8% | 10.4% | 5.0% | 49.0% | 20.7% | 49.5% | 24.9% |
| S12 Unstable (all regimes) | 45.5% | 33.1% | 20.6% | 11.7% | 0.4% | 57.1% | 35.8% | 9.9% | 6.7% | 56.1% | 8.8% | 55.0% | 22.5% |
| UNKNOWN Unknown (all regimes) | 49.5% | 40.4% | 21.5% | 13.3% | 0.7% | 55.8% | 35.9% | 10.8% | 5.4% | 49.1% | 21.1% | 49.1% | 24.0% |

_Point estimates; intervals for every cell are in atlas/daily/stats.csv. Daily resolution cannot order two levels reached in the same session (the tie column); the 3-minute atlas resolves most of them._

## Intraday detail (3-minute bars)

| group | first 15 minutes: move from the open | first 30 minutes: move from the open | first hour: move from the open | first hour: range | session 1 opened with an up drive (+0.25 ATR in 30 minutes) | session 1 opened with a down drive (-0.25 ATR in 30 minutes) | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | session 1: the high came before the low | session 1: fell in the morning, rose in the afternoon | session 1: rose in the morning, fell in the afternoon | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | +1 and -1 ATR first reached in the same 3-minute bar | trading minutes to the first touch of +1 ATR (of those touched) | trading minutes to the first touch of -1 ATR (of those touched) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Everything | 0.00 | -0.00 | -0.01 | 0.60 | 18.8% | 20.6% | 3.3% | 2.8% | 57.2% | 3.4% | 7.1% | 52.8% | 0.0% | 680 | 768 |
| Broad bullish (all states) | 0.02 | 0.01 | 0.01 | 0.61 | 19.8% | 19.6% | 3.9% | 2.3% | 57.6% | 2.6% | 8.3% | 55.7% | 0.0% | 643 | 822 |
| Narrow bullish (all states) | -0.00 | -0.00 | -0.01 | 0.61 | 19.5% | 20.9% | 3.4% | 2.8% | 58.9% | 3.6% | 6.2% | 50.2% | 0.0% | 660 | 766 |
| Mixed (all states) | -0.00 | 0.00 | -0.02 | 0.54 | 16.5% | 16.9% | 2.6% | 1.5% | 58.7% | 2.8% | 6.6% | 51.9% | 0.0% | 698 | 819 |
| Broad bearish (all states) | -0.03 | -0.03 | -0.02 | 0.57 | 16.3% | 22.2% | 2.5% | 2.3% | 57.5% | 3.6% | 6.7% | 50.3% | 0.0% | 761 | 676 |
| High stress (all states) | 0.00 | -0.01 | -0.01 | 0.65 | 21.1% | 23.8% | 3.7% | 5.8% | 52.2% | 4.9% | 7.1% | 54.7% | 0.0% | 683 | 708 |
| S01 Strong bull (all regimes) | 0.01 | 0.01 | 0.01 | 0.65 | 21.9% | 21.1% | 4.3% | 3.8% | 57.5% | 3.7% | 7.7% | 50.0% | 0.0% | 628 | 735 |
| S02 Emerging bull (all regimes) | 0.01 | 0.00 | 0.00 | 0.65 | 21.0% | 21.7% | 4.4% | 3.1% | 57.2% | 3.8% | 7.9% | 53.4% | 0.0% | 649 | 760 |
| S03 Bull consolidation (all regimes) | 0.00 | -0.01 | -0.01 | 0.61 | 19.3% | 21.1% | 3.5% | 3.3% | 59.1% | 3.6% | 6.4% | 50.7% | 0.0% | 668 | 767 |
| S06 Reversal attempt (all regimes) | -0.00 | -0.01 | -0.01 | 0.59 | 18.2% | 20.9% | 3.1% | 2.3% | 58.4% | 3.1% | 7.4% | 52.6% | 0.0% | 685 | 791 |
| S07 Neutral range (all regimes) | 0.00 | -0.00 | -0.00 | 0.58 | 18.0% | 19.3% | 3.1% | 2.5% | 57.6% | 3.1% | 6.9% | 53.0% | 0.0% | 687 | 792 |
| S08 Bear continuation (all regimes) | -0.00 | -0.01 | -0.01 | 0.56 | 17.2% | 20.1% | 2.4% | 2.3% | 55.2% | 3.1% | 6.4% | 57.2% | 0.0% | 708 | 772 |
| S09 Emerging bear (all regimes) | -0.00 | -0.01 | -0.01 | 0.57 | 18.0% | 20.3% | 2.6% | 2.6% | 55.9% | 3.3% | 6.7% | 53.3% | 0.0% | 719 | 741 |
| S12 Unstable (all regimes) | 0.05 | 0.02 | 0.03 | 0.55 | 20.3% | 16.1% | 0.8% | 0.8% | 53.0% | 3.4% | 5.9% | 48.7% | 0.0% | 548 | 699 |
| UNKNOWN Unknown (all regimes) | -0.00 | -0.01 | -0.01 | 0.60 | 18.6% | 20.8% | 3.5% | 2.9% | 57.6% | 3.4% | 7.1% | 52.4% | 0.0% | 671 | 776 |

_(chart in ATLAS.html: half-hour of the day in which the 5-session high fell (all sessions pooled))_

_(chart in ATLAS.html: half-hour of the day in which the 5-session low fell)_

## Transitions inside the window (description only)

Share of paths whose tl_state state at the session-5 close equals the state at T0 (all regimes): S01 55%, S02 53%, S03 45%, S06 52%, S07 44%, S08 54%, S09 51%, S12 26%, UNKNOWN 46%.

| state at T0 | state sequence over the window (repeats collapsed) | paths | share |
|---|---|---|---|
| S01 | S01 | 23,628 | 53.0% |
| S01 | S01 > UNKNOWN | 6,931 | 15.5% |
| S01 | S01 > S03 | 6,196 | 13.9% |
| S01 | S01 > S07 | 1,478 | 3.3% |
| S02 | S02 | 34,909 | 50.6% |
| S02 | S02 > S01 | 7,758 | 11.3% |
| S02 | S02 > UNKNOWN | 7,145 | 10.4% |
| S02 | S02 > S07 | 5,598 | 8.1% |
| S03 | S03 | 17,970 | 39.8% |
| S03 | S03 > UNKNOWN | 8,664 | 19.2% |
| S03 | S03 > S07 | 4,173 | 9.2% |
| S03 | S03 > S09 | 3,999 | 8.9% |
| S06 | S06 | 17,414 | 47.2% |
| S06 | S06 > S02 | 6,412 | 17.4% |
| S06 | S06 > S07 | 3,858 | 10.5% |
| S06 | S06 > UNKNOWN | 3,162 | 8.6% |
| S07 | S07 | 31,820 | 36.6% |
| S07 | S07 > UNKNOWN | 15,255 | 17.5% |
| S07 | S07 > S09 | 13,464 | 15.5% |
| S07 | S07 > S02 | 8,327 | 9.6% |
| S08 | S08 | 12,459 | 53.7% |
| S08 | S08 > UNKNOWN | 4,140 | 17.8% |
| S08 | S08 > S06 | 3,065 | 13.2% |
| S08 | S08 > S07 | 1,012 | 4.4% |
| S09 | S09 | 40,766 | 46.8% |
| S09 | S09 > UNKNOWN | 14,493 | 16.6% |
| S09 | S09 > S07 | 11,842 | 13.6% |
| S09 | S09 > S08 | 6,710 | 7.7% |
| S12 | S12 | 61 | 23.7% |
| S12 | S12 > UNKNOWN | 38 | 14.8% |
| S12 | S12 > S06 | 36 | 14.0% |
| S12 | S12 > S07 | 34 | 13.2% |
| UNKNOWN | UNKNOWN | 51,194 | 40.5% |
| UNKNOWN | UNKNOWN > S09 | 13,047 | 10.3% |
| UNKNOWN | UNKNOWN > S07 | 12,096 | 9.6% |
| UNKNOWN | UNKNOWN > S02 | 9,867 | 7.8% |

| regime at T0 | regime by session 5 | paths | mean 5-day close (ATR) | 5-day close up | mean MFE | mean MAE |
|---|---|---|---|---|---|---|
| broad_bearish | held | 15,593 | -0.15 | 42.7% | 0.90 | -1.18 |
| broad_bearish | improved | 26,068 | +0.58 | 69.5% | 1.38 | -0.57 |
| broad_bearish | worsened | 8,912 | -1.26 | 12.9% | 0.60 | -2.03 |
| broad_bullish | held | 109,403 | +0.59 | 61.9% | 1.65 | -0.73 |
| broad_bullish | worsened | 68,691 | -0.34 | 33.2% | 1.21 | -1.37 |
| high_stress | held | 35,368 | -0.28 | 46.7% | 1.14 | -1.40 |
| high_stress | improved | 33,904 | +0.36 | 58.0% | 1.34 | -0.93 |
| mixed | held | 25,653 | +0.21 | 52.7% | 1.37 | -0.82 |
| mixed | improved | 21,761 | +0.68 | 69.7% | 1.54 | -0.62 |
| mixed | worsened | 21,904 | -0.83 | 21.6% | 0.85 | -1.61 |
| narrow_bullish | held | 79,364 | +0.12 | 47.8% | 1.28 | -1.00 |
| narrow_bullish | improved | 44,404 | +0.84 | 71.5% | 1.76 | -0.55 |
| narrow_bullish | worsened | 28,373 | -0.76 | 24.8% | 0.90 | -1.75 |

_The regime change is observed after T0 (it explains what happened; it is never a classifier)._

## BigMove's picks against the universe (descriptive)

| paths | picks | measure | picks | picks' value [95%] | vs same-day same-cell non-picks [95%] |
|---|---|---|---|---|---|
| daily | D ranks 1-3 | 5-day close above C0 | 2,181 | 56.2% [52.0%, 60.1%] | +5.5 pp [+2.8 pp, +8.4 pp] |
| daily | D ranks 1-3 | 5-day close from C0 | 2,181 | 0.37 [0.23, 0.50] | +0.24 [+0.15, +0.33] |
| daily | D ranks 1-3 | best high of the window from C0 (MFE) | 2,181 | 1.50 [1.40, 1.62] | +0.17 [+0.09, +0.25] |
| daily | D ranks 1-3 | worst low of the window from C0 (MAE) | 2,181 | -0.97 [-1.07, -0.89] | +0.06 [+0.00, +0.13] |
| daily | D ranks 1-3 | reached +1 ATR at some point in the 5 sessions | 2,181 | 54.8% [51.3%, 58.4%] | +5.9 pp [+3.1 pp, +8.6 pp] |
| daily | D ranks 1-3 | reached -1 ATR at some point in the 5 sessions | 2,181 | 40.1% [36.2%, 44.5%] | -0.6 pp [-2.9 pp, +1.8 pp] |
| daily | D ranks 1-3 | reached +2 ATR at some point in the 5 sessions | 2,181 | 26.7% [23.9%, 29.5%] | +5.9 pp [+3.8 pp, +7.8 pp] |
| daily | D ranks 1-3 | reached -2 ATR at some point in the 5 sessions | 2,181 | 12.6% [9.8%, 15.9%] | -1.6 pp [-3.4 pp, +0.4 pp] |
| daily | D ranks 1-3 | +1 ATR before -1 ATR (of the paths where one came first) | 1,830 | 58.5% [54.4%, 62.4%] | +2.7 pp [+0.1 pp, +5.3 pp] |
| daily | D ranks 1-3 | after -1 ATR came first: ended above C0 | 759 | 20.7% [16.6%, 24.8%] | +4.8 pp [+1.5 pp, +8.3 pp] |
| daily | D ranks 1-3 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 533 | 54.6% [49.5%, 59.5%] | +4.6 pp [+1.1 pp, +8.4 pp] |
| daily | D ranks 1-3 | after a session-1 close >= +0.5 ATR: ended below C0 | 533 | 16.1% [12.4%, 20.0%] | -4.8 pp [-8.0 pp, -1.8 pp] |
| daily | D ranks 1-3 | BigMove's trade: session-1 open to session-5 close, before costs | 2,181 | 1.67% [0.75%, 2.53%] | +1.41% [+0.93%, +1.94%] |
| daily | D ranks 1-3 | 10-day close from C0 | 2,181 | 0.53 [0.27, 0.79] | +0.27 [+0.12, +0.42] |
| daily | D ranks 1-3 | best high of 10 sessions from C0 | 2,181 | 2.20 [2.02, 2.38] | +0.22 [+0.11, +0.34] |
| daily | D ranks 1-3 | worst low of 10 sessions from C0 | 2,181 | -1.36 [-1.52, -1.22] | +0.12 [+0.03, +0.24] |
| daily | D ranks 1-3 | 10-day close above C0 | 2,181 | 57.9% [52.9%, 62.8%] | +5.5 pp [+2.6 pp, +8.6 pp] |
| daily | D ranks 1-3 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 2,181 | 1.87% [0.84%, 2.82%] | +1.59% [+1.06%, +2.18%] |
| daily | D ranks 1-3 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 2,181 | 1.41% [0.40%, 2.36%] | +1.12% [+0.56%, +1.72%] |
| daily | D ranks 1-3 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 2,181 | 0.98% [0.07%, 1.89%] | +0.69% [+0.17%, +1.27%] |
| daily | D ranks 1-3 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 2,181 | 0.88% [0.01%, 1.78%] | +0.58% [+0.05%, +1.14%] |
| daily | D ranks 1-3 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 2,181 | 0.68% [-0.25%, 1.67%] | +0.41% [-0.13%, +1.00%] |
| daily | D ranks 1-3 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 2,181 | 0.55% [-0.41%, 1.58%] | +0.30% [-0.25%, +0.90%] |
| daily | D ranks 1-3 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 2,181 | 0.48% [-0.50%, 1.50%] | +0.23% [-0.31%, +0.81%] |
| daily | D ranks 1-3 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 2,181 | 0.39% [-0.58%, 1.38%] | +0.15% [-0.36%, +0.67%] |
| daily | D ranks 1-3 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 2,181 | 0.29% [-0.72%, 1.31%] | +0.05% [-0.47%, +0.55%] |
| daily | D ranks 1-3 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 2,181 | 0.37% [-0.61%, 1.39%] | +0.13% [-0.40%, +0.64%] |
| daily | D ranks 1-3 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 2,181 | -0.46% [-0.70%, -0.19%] | -0.48% [-0.70%, -0.24%] |
| daily | D ranks 1-3 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 2,181 | -0.88% [-1.32%, -0.39%] | -0.91% [-1.26%, -0.51%] |
| daily | D ranks 1-3 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 2,181 | -0.99% [-1.63%, -0.31%] | -1.02% [-1.52%, -0.50%] |
| daily | D ranks 1-3 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 2,181 | -1.19% [-1.95%, -0.32%] | -1.19% [-1.77%, -0.59%] |
| daily | D ranks 1-3 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 2,181 | -1.31% [-2.24%, -0.27%] | -1.29% [-1.95%, -0.60%] |
| daily | D ranks 1-3 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 2,181 | -1.39% [-2.40%, -0.27%] | -1.36% [-2.04%, -0.65%] |
| daily | D ranks 1-3 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 2,181 | -1.48% [-2.56%, -0.33%] | -1.45% [-2.12%, -0.74%] |
| daily | D ranks 1-3 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 2,181 | -1.58% [-2.73%, -0.39%] | -1.55% [-2.25%, -0.85%] |
| daily | D ranks 1-3 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 2,181 | -1.49% [-2.72%, -0.24%] | -1.47% [-2.23%, -0.74%] |
| daily | ENS ranks 1-3 | 5-day close above C0 | 2,194 | 58.3% [54.3%, 62.0%] | +7.6 pp [+4.9 pp, +10.2 pp] |
| daily | ENS ranks 1-3 | 5-day close from C0 | 2,194 | 0.40 [0.26, 0.55] | +0.27 [+0.17, +0.36] |
| daily | ENS ranks 1-3 | best high of the window from C0 (MFE) | 2,194 | 1.51 [1.40, 1.62] | +0.17 [+0.09, +0.25] |
| daily | ENS ranks 1-3 | worst low of the window from C0 (MAE) | 2,194 | -0.94 [-1.04, -0.86] | +0.09 [+0.02, +0.16] |
| daily | ENS ranks 1-3 | reached +1 ATR at some point in the 5 sessions | 2,194 | 56.4% [53.0%, 59.8%] | +7.4 pp [+4.7 pp, +9.8 pp] |
| daily | ENS ranks 1-3 | reached -1 ATR at some point in the 5 sessions | 2,194 | 37.3% [33.5%, 41.6%] | -3.2 pp [-5.7 pp, -0.6 pp] |
| daily | ENS ranks 1-3 | reached +2 ATR at some point in the 5 sessions | 2,194 | 26.6% [23.6%, 29.6%] | +5.6 pp [+3.3 pp, +8.0 pp] |
| daily | ENS ranks 1-3 | reached -2 ATR at some point in the 5 sessions | 2,194 | 12.1% [9.5%, 15.3%] | -1.9 pp [-4.0 pp, +0.1 pp] |
| daily | ENS ranks 1-3 | +1 ATR before -1 ATR (of the paths where one came first) | 1,836 | 61.1% [56.9%, 64.9%] | +5.0 pp [+2.3 pp, +7.5 pp] |
| daily | ENS ranks 1-3 | after -1 ATR came first: ended above C0 | 715 | 21.0% [17.5%, 24.6%] | +5.7 pp [+3.1 pp, +8.5 pp] |
| daily | ENS ranks 1-3 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 562 | 54.4% [49.2%, 59.7%] | +5.7 pp [+1.9 pp, +9.7 pp] |
| daily | ENS ranks 1-3 | after a session-1 close >= +0.5 ATR: ended below C0 | 562 | 17.6% [14.0%, 21.7%] | -4.1 pp [-7.3 pp, -0.8 pp] |
| daily | ENS ranks 1-3 | BigMove's trade: session-1 open to session-5 close, before costs | 2,194 | 1.96% [1.15%, 2.80%] | +1.68% [+1.18%, +2.22%] |
| daily | ENS ranks 1-3 | 10-day close from C0 | 2,194 | 0.64 [0.37, 0.89] | +0.38 [+0.24, +0.53] |
| daily | ENS ranks 1-3 | best high of 10 sessions from C0 | 2,194 | 2.28 [2.08, 2.47] | +0.30 [+0.18, +0.43] |
| daily | ENS ranks 1-3 | worst low of 10 sessions from C0 | 2,194 | -1.35 [-1.51, -1.20] | +0.13 [+0.01, +0.25] |
| daily | ENS ranks 1-3 | 10-day close above C0 | 2,194 | 59.8% [54.9%, 64.4%] | +7.2 pp [+4.1 pp, +10.1 pp] |
| daily | ENS ranks 1-3 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 2,194 | 2.18% [1.24%, 3.11%] | +1.88% [+1.32%, +2.48%] |
| daily | ENS ranks 1-3 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 2,194 | 1.54% [0.54%, 2.50%] | +1.25% [+0.72%, +1.86%] |
| daily | ENS ranks 1-3 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 2,194 | 1.29% [0.30%, 2.27%] | +1.01% [+0.44%, +1.59%] |
| daily | ENS ranks 1-3 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 2,194 | 1.08% [0.12%, 2.05%] | +0.78% [+0.25%, +1.38%] |
| daily | ENS ranks 1-3 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 2,194 | 0.99% [0.04%, 1.97%] | +0.69% [+0.17%, +1.24%] |
| daily | ENS ranks 1-3 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 2,194 | 0.73% [-0.20%, 1.67%] | +0.45% [-0.02%, +0.95%] |
| daily | ENS ranks 1-3 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 2,194 | 0.56% [-0.40%, 1.47%] | +0.29% [-0.16%, +0.75%] |
| daily | ENS ranks 1-3 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 2,194 | 0.50% [-0.49%, 1.45%] | +0.23% [-0.26%, +0.66%] |
| daily | ENS ranks 1-3 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 2,194 | 0.54% [-0.45%, 1.49%] | +0.26% [-0.21%, +0.72%] |
| daily | ENS ranks 1-3 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 2,194 | 0.58% [-0.38%, 1.53%] | +0.30% [-0.17%, +0.78%] |
| daily | ENS ranks 1-3 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 2,194 | -0.64% [-0.90%, -0.39%] | -0.63% [-0.87%, -0.39%] |
| daily | ENS ranks 1-3 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 2,194 | -0.88% [-1.31%, -0.45%] | -0.87% [-1.25%, -0.47%] |
| daily | ENS ranks 1-3 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 2,194 | -1.10% [-1.67%, -0.50%] | -1.10% [-1.59%, -0.59%] |
| daily | ENS ranks 1-3 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 2,194 | -1.19% [-1.91%, -0.46%] | -1.19% [-1.76%, -0.64%] |
| daily | ENS ranks 1-3 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 2,194 | -1.45% [-2.29%, -0.61%] | -1.43% [-2.07%, -0.81%] |
| daily | ENS ranks 1-3 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 2,194 | -1.61% [-2.56%, -0.66%] | -1.59% [-2.24%, -0.94%] |
| daily | ENS ranks 1-3 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 2,194 | -1.68% [-2.75%, -0.58%] | -1.66% [-2.35%, -0.95%] |
| daily | ENS ranks 1-3 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 2,194 | -1.64% [-2.80%, -0.46%] | -1.62% [-2.34%, -0.89%] |
| daily | ENS ranks 1-3 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 2,194 | -1.60% [-2.80%, -0.37%] | -1.58% [-2.32%, -0.88%] |
| daily | D ranks 4-10 | 5-day close above C0 | 5,112 | 54.7% [50.8%, 58.2%] | +4.0 pp [+2.3 pp, +5.6 pp] |
| daily | D ranks 4-10 | 5-day close from C0 | 5,112 | 0.32 [0.18, 0.46] | +0.19 [+0.12, +0.24] |
| daily | D ranks 4-10 | best high of the window from C0 (MFE) | 5,112 | 1.51 [1.41, 1.60] | +0.16 [+0.11, +0.22] |
| daily | D ranks 4-10 | worst low of the window from C0 (MAE) | 5,112 | -0.97 [-1.07, -0.89] | +0.05 [+0.01, +0.10] |
| daily | D ranks 4-10 | reached +1 ATR at some point in the 5 sessions | 5,112 | 54.0% [50.7%, 56.9%] | +4.6 pp [+2.9 pp, +6.3 pp] |
| daily | D ranks 4-10 | reached -1 ATR at some point in the 5 sessions | 5,112 | 38.8% [34.8%, 43.3%] | -1.6 pp [-3.1 pp, -0.3 pp] |
| daily | D ranks 4-10 | reached +2 ATR at some point in the 5 sessions | 5,112 | 25.4% [22.9%, 27.9%] | +4.4 pp [+2.8 pp, +5.9 pp] |
| daily | D ranks 4-10 | reached -2 ATR at some point in the 5 sessions | 5,112 | 13.8% [11.3%, 16.7%] | -0.1 pp [-1.5 pp, +1.2 pp] |
| daily | D ranks 4-10 | +1 ATR before -1 ATR (of the paths where one came first) | 4,230 | 59.5% [55.2%, 63.4%] | +3.4 pp [+1.9 pp, +4.9 pp] |
| daily | D ranks 4-10 | after -1 ATR came first: ended above C0 | 1,714 | 17.1% [14.4%, 19.9%] | +2.1 pp [+0.2 pp, +4.1 pp] |
| daily | D ranks 4-10 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 1,138 | 51.6% [46.9%, 56.0%] | +2.2 pp [-0.6 pp, +4.9 pp] |
| daily | D ranks 4-10 | after a session-1 close >= +0.5 ATR: ended below C0 | 1,138 | 19.7% [16.6%, 23.4%] | -2.5 pp [-4.8 pp, -0.4 pp] |
| daily | D ranks 4-10 | BigMove's trade: session-1 open to session-5 close, before costs | 5,112 | 1.21% [0.42%, 1.97%] | +0.95% [+0.61%, +1.29%] |
| daily | D ranks 4-10 | 10-day close from C0 | 5,111 | 0.54 [0.25, 0.80] | +0.26 [+0.16, +0.37] |
| daily | D ranks 4-10 | best high of 10 sessions from C0 | 5,111 | 2.25 [2.08, 2.44] | +0.26 [+0.17, +0.36] |
| daily | D ranks 4-10 | worst low of 10 sessions from C0 | 5,111 | -1.39 [-1.57, -1.23] | +0.09 [+0.02, +0.17] |
| daily | D ranks 4-10 | 10-day close above C0 | 5,111 | 57.1% [52.3%, 61.5%] | +4.5 pp [+2.6 pp, +6.5 pp] |
| daily | D ranks 4-10 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 5,111 | 1.31% [0.41%, 2.16%] | +1.03% [+0.65%, +1.40%] |
| daily | D ranks 4-10 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 5,111 | 0.97% [0.07%, 1.83%] | +0.69% [+0.32%, +1.05%] |
| daily | D ranks 4-10 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 5,111 | 0.83% [-0.09%, 1.65%] | +0.54% [+0.18%, +0.91%] |
| daily | D ranks 4-10 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 5,111 | 0.77% [-0.14%, 1.60%] | +0.49% [+0.13%, +0.84%] |
| daily | D ranks 4-10 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 5,111 | 0.73% [-0.20%, 1.57%] | +0.44% [+0.08%, +0.79%] |
| daily | D ranks 4-10 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 5,111 | 0.61% [-0.32%, 1.44%] | +0.30% [-0.05%, +0.62%] |
| daily | D ranks 4-10 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 5,111 | 0.54% [-0.40%, 1.36%] | +0.23% [-0.11%, +0.55%] |
| daily | D ranks 4-10 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 5,111 | 0.57% [-0.36%, 1.41%] | +0.25% [-0.09%, +0.60%] |
| daily | D ranks 4-10 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 5,111 | 0.58% [-0.35%, 1.44%] | +0.27% [-0.06%, +0.62%] |
| daily | D ranks 4-10 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 5,111 | 0.67% [-0.26%, 1.57%] | +0.38% [+0.04%, +0.73%] |
| daily | D ranks 4-10 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 5,111 | -0.33% [-0.54%, -0.11%] | -0.34% [-0.49%, -0.19%] |
| daily | D ranks 4-10 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 5,111 | -0.48% [-0.84%, -0.10%] | -0.49% [-0.72%, -0.25%] |
| daily | D ranks 4-10 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 5,111 | -0.53% [-1.02%, -0.02%] | -0.54% [-0.83%, -0.26%] |
| daily | D ranks 4-10 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 5,111 | -0.58% [-1.18%, 0.06%] | -0.59% [-0.92%, -0.26%] |
| daily | D ranks 4-10 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 5,111 | -0.70% [-1.41%, 0.06%] | -0.74% [-1.08%, -0.37%] |
| daily | D ranks 4-10 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 5,111 | -0.76% [-1.58%, 0.10%] | -0.80% [-1.19%, -0.41%] |
| daily | D ranks 4-10 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 5,111 | -0.73% [-1.62%, 0.22%] | -0.78% [-1.20%, -0.33%] |
| daily | D ranks 4-10 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 5,111 | -0.73% [-1.69%, 0.35%] | -0.76% [-1.19%, -0.30%] |
| daily | D ranks 4-10 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 5,111 | -0.63% [-1.66%, 0.54%] | -0.65% [-1.09%, -0.14%] |
| daily | ENS ranks 4-10 | 5-day close above C0 | 5,118 | 55.6% [51.5%, 59.3%] | +4.9 pp [+3.2 pp, +6.3 pp] |
| daily | ENS ranks 4-10 | 5-day close from C0 | 5,118 | 0.32 [0.17, 0.46] | +0.17 [+0.12, +0.22] |
| daily | ENS ranks 4-10 | best high of the window from C0 (MFE) | 5,118 | 1.49 [1.39, 1.59] | +0.14 [+0.09, +0.20] |
| daily | ENS ranks 4-10 | worst low of the window from C0 (MAE) | 5,118 | -0.97 [-1.06, -0.88] | +0.06 [+0.01, +0.11] |
| daily | ENS ranks 4-10 | reached +1 ATR at some point in the 5 sessions | 5,118 | 54.6% [51.2%, 57.8%] | +5.4 pp [+3.7 pp, +7.1 pp] |
| daily | ENS ranks 4-10 | reached -1 ATR at some point in the 5 sessions | 5,118 | 37.8% [33.6%, 42.1%] | -2.4 pp [-3.9 pp, -0.9 pp] |
| daily | ENS ranks 4-10 | reached +2 ATR at some point in the 5 sessions | 5,118 | 25.2% [22.7%, 28.0%] | +4.2 pp [+2.7 pp, +5.7 pp] |
| daily | ENS ranks 4-10 | reached -2 ATR at some point in the 5 sessions | 5,118 | 12.2% [9.7%, 15.1%] | -1.7 pp [-3.0 pp, -0.5 pp] |
| daily | ENS ranks 4-10 | +1 ATR before -1 ATR (of the paths where one came first) | 4,221 | 60.1% [55.7%, 64.2%] | +3.5 pp [+1.7 pp, +5.2 pp] |
| daily | ENS ranks 4-10 | after -1 ATR came first: ended above C0 | 1,685 | 19.1% [16.2%, 21.9%] | +3.5 pp [+1.7 pp, +5.5 pp] |
| daily | ENS ranks 4-10 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 1,078 | 50.4% [45.7%, 54.4%] | +0.4 pp [-2.8 pp, +3.5 pp] |
| daily | ENS ranks 4-10 | after a session-1 close >= +0.5 ATR: ended below C0 | 1,078 | 21.1% [17.8%, 24.6%] | -0.7 pp [-2.7 pp, +1.6 pp] |
| daily | ENS ranks 4-10 | BigMove's trade: session-1 open to session-5 close, before costs | 5,118 | 1.20% [0.41%, 1.95%] | +0.92% [+0.64%, +1.21%] |
| daily | ENS ranks 4-10 | 10-day close from C0 | 5,118 | 0.54 [0.27, 0.80] | +0.27 [+0.16, +0.36] |
| daily | ENS ranks 4-10 | best high of 10 sessions from C0 | 5,118 | 2.21 [2.02, 2.40] | +0.22 [+0.13, +0.32] |
| daily | ENS ranks 4-10 | worst low of 10 sessions from C0 | 5,118 | -1.37 [-1.54, -1.22] | +0.10 [+0.03, +0.18] |
| daily | ENS ranks 4-10 | 10-day close above C0 | 5,118 | 58.4% [53.7%, 63.1%] | +5.8 pp [+4.2 pp, +7.5 pp] |
| daily | ENS ranks 4-10 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 5,118 | 1.30% [0.41%, 2.14%] | +1.02% [+0.70%, +1.34%] |
| daily | ENS ranks 4-10 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 5,118 | 1.09% [0.21%, 1.96%] | +0.82% [+0.46%, +1.20%] |
| daily | ENS ranks 4-10 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 5,118 | 0.95% [0.09%, 1.81%] | +0.68% [+0.31%, +1.08%] |
| daily | ENS ranks 4-10 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 5,118 | 0.82% [-0.04%, 1.64%] | +0.55% [+0.19%, +0.92%] |
| daily | ENS ranks 4-10 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 5,118 | 0.67% [-0.19%, 1.49%] | +0.41% [+0.04%, +0.75%] |
| daily | ENS ranks 4-10 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 5,118 | 0.68% [-0.18%, 1.47%] | +0.41% [+0.07%, +0.74%] |
| daily | ENS ranks 4-10 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 5,118 | 0.66% [-0.18%, 1.42%] | +0.36% [+0.06%, +0.67%] |
| daily | ENS ranks 4-10 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 5,118 | 0.69% [-0.15%, 1.43%] | +0.38% [+0.09%, +0.69%] |
| daily | ENS ranks 4-10 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 5,118 | 0.68% [-0.15%, 1.43%] | +0.37% [+0.07%, +0.66%] |
| daily | ENS ranks 4-10 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 5,118 | 0.75% [-0.07%, 1.53%] | +0.43% [+0.14%, +0.74%] |
| daily | ENS ranks 4-10 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 5,118 | -0.21% [-0.41%, 0.01%] | -0.20% [-0.37%, -0.03%] |
| daily | ENS ranks 4-10 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 5,118 | -0.36% [-0.68%, 0.00%] | -0.34% [-0.56%, -0.13%] |
| daily | ENS ranks 4-10 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 5,118 | -0.48% [-0.93%, -0.02%] | -0.47% [-0.74%, -0.20%] |
| daily | ENS ranks 4-10 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 5,118 | -0.63% [-1.16%, -0.05%] | -0.61% [-0.90%, -0.32%] |
| daily | ENS ranks 4-10 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 5,118 | -0.62% [-1.28%, 0.09%] | -0.61% [-0.95%, -0.27%] |
| daily | ENS ranks 4-10 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 5,118 | -0.64% [-1.42%, 0.15%] | -0.66% [-1.01%, -0.30%] |
| daily | ENS ranks 4-10 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 5,118 | -0.61% [-1.47%, 0.30%] | -0.63% [-1.01%, -0.24%] |
| daily | ENS ranks 4-10 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 5,118 | -0.62% [-1.52%, 0.38%] | -0.65% [-1.03%, -0.26%] |
| daily | ENS ranks 4-10 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 5,118 | -0.56% [-1.54%, 0.55%] | -0.59% [-1.00%, -0.16%] |
| daily | D ranks 1-10 | 5-day close above C0 | 7,293 | 55.2% [51.3%, 58.6%] | +4.4 pp [+2.9 pp, +6.1 pp] |
| daily | D ranks 1-10 | 5-day close from C0 | 7,293 | 0.34 [0.19, 0.47] | +0.20 [+0.15, +0.26] |
| daily | D ranks 1-10 | best high of the window from C0 (MFE) | 7,293 | 1.51 [1.41, 1.60] | +0.16 [+0.12, +0.21] |
| daily | D ranks 1-10 | worst low of the window from C0 (MAE) | 7,293 | -0.97 [-1.07, -0.89] | +0.06 [+0.01, +0.11] |
| daily | D ranks 1-10 | reached +1 ATR at some point in the 5 sessions | 7,293 | 54.2% [51.3%, 57.0%] | +5.0 pp [+3.4 pp, +6.5 pp] |
| daily | D ranks 1-10 | reached -1 ATR at some point in the 5 sessions | 7,293 | 39.2% [35.3%, 43.5%] | -1.3 pp [-2.8 pp, +0.1 pp] |
| daily | D ranks 1-10 | reached +2 ATR at some point in the 5 sessions | 7,293 | 25.8% [23.4%, 28.2%] | +4.8 pp [+3.5 pp, +6.1 pp] |
| daily | D ranks 1-10 | reached -2 ATR at some point in the 5 sessions | 7,293 | 13.4% [10.9%, 16.5%] | -0.6 pp [-2.0 pp, +0.8 pp] |
| daily | D ranks 1-10 | +1 ATR before -1 ATR (of the paths where one came first) | 6,060 | 59.2% [55.1%, 62.8%] | +3.2 pp [+1.6 pp, +4.7 pp] |
| daily | D ranks 1-10 | after -1 ATR came first: ended above C0 | 2,473 | 18.2% [15.6%, 20.9%] | +2.9 pp [+1.2 pp, +5.0 pp] |
| daily | D ranks 1-10 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 1,671 | 52.5% [48.3%, 56.5%] | +3.0 pp [+0.7 pp, +5.3 pp] |
| daily | D ranks 1-10 | after a session-1 close >= +0.5 ATR: ended below C0 | 1,671 | 18.6% [15.7%, 21.8%] | -3.3 pp [-5.2 pp, -1.4 pp] |
| daily | D ranks 1-10 | BigMove's trade: session-1 open to session-5 close, before costs | 7,293 | 1.35% [0.52%, 2.13%] | +1.09% [+0.76%, +1.44%] |
| daily | D ranks 1-10 | 10-day close from C0 | 7,292 | 0.53 [0.27, 0.78] | +0.26 [+0.16, +0.37] |
| daily | D ranks 1-10 | best high of 10 sessions from C0 | 7,292 | 2.24 [2.07, 2.41] | +0.25 [+0.17, +0.34] |
| daily | D ranks 1-10 | worst low of 10 sessions from C0 | 7,292 | -1.38 [-1.55, -1.23] | +0.10 [+0.03, +0.18] |
| daily | D ranks 1-10 | 10-day close above C0 | 7,292 | 57.3% [52.6%, 61.7%] | +4.8 pp [+2.9 pp, +6.8 pp] |
| daily | D ranks 1-10 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 7,292 | 1.47% [0.57%, 2.34%] | +1.20% [+0.83%, +1.59%] |
| daily | D ranks 1-10 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 7,292 | 1.10% [0.18%, 1.97%] | +0.82% [+0.45%, +1.21%] |
| daily | D ranks 1-10 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 7,292 | 0.87% [-0.02%, 1.69%] | +0.59% [+0.24%, +0.95%] |
| daily | D ranks 1-10 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 7,292 | 0.80% [-0.05%, 1.63%] | +0.51% [+0.17%, +0.88%] |
| daily | D ranks 1-10 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 7,292 | 0.72% [-0.16%, 1.58%] | +0.43% [+0.07%, +0.80%] |
| daily | D ranks 1-10 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 7,292 | 0.59% [-0.32%, 1.47%] | +0.30% [-0.06%, +0.66%] |
| daily | D ranks 1-10 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 7,292 | 0.52% [-0.38%, 1.38%] | +0.23% [-0.11%, +0.59%] |
| daily | D ranks 1-10 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 7,292 | 0.52% [-0.41%, 1.40%] | +0.22% [-0.11%, +0.57%] |
| daily | D ranks 1-10 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 7,292 | 0.49% [-0.44%, 1.39%] | +0.20% [-0.15%, +0.57%] |
| daily | D ranks 1-10 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 7,292 | 0.58% [-0.34%, 1.49%] | +0.30% [-0.04%, +0.66%] |
| daily | D ranks 1-10 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 7,292 | -0.37% [-0.55%, -0.17%] | -0.38% [-0.52%, -0.24%] |
| daily | D ranks 1-10 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 7,292 | -0.60% [-0.93%, -0.22%] | -0.61% [-0.82%, -0.40%] |
| daily | D ranks 1-10 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 7,292 | -0.67% [-1.15%, -0.16%] | -0.69% [-0.97%, -0.41%] |
| daily | D ranks 1-10 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 7,292 | -0.76% [-1.36%, -0.10%] | -0.77% [-1.09%, -0.44%] |
| daily | D ranks 1-10 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 7,292 | -0.88% [-1.60%, -0.09%] | -0.90% [-1.26%, -0.51%] |
| daily | D ranks 1-10 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 7,292 | -0.95% [-1.78%, -0.06%] | -0.97% [-1.37%, -0.55%] |
| daily | D ranks 1-10 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 7,292 | -0.96% [-1.86%, 0.03%] | -0.98% [-1.40%, -0.53%] |
| daily | D ranks 1-10 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 7,292 | -0.98% [-1.99%, 0.08%] | -1.00% [-1.44%, -0.52%] |
| daily | D ranks 1-10 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 7,292 | -0.89% [-1.95%, 0.26%] | -0.89% [-1.36%, -0.38%] |
| daily | ENS ranks 1-10 | 5-day close above C0 | 7,312 | 56.4% [52.4%, 59.8%] | +5.7 pp [+4.1 pp, +7.2 pp] |
| daily | ENS ranks 1-10 | 5-day close from C0 | 7,312 | 0.34 [0.20, 0.48] | +0.20 [+0.15, +0.25] |
| daily | ENS ranks 1-10 | best high of the window from C0 (MFE) | 7,312 | 1.50 [1.41, 1.59] | +0.15 [+0.11, +0.20] |
| daily | ENS ranks 1-10 | worst low of the window from C0 (MAE) | 7,312 | -0.96 [-1.05, -0.87] | +0.07 [+0.02, +0.12] |
| daily | ENS ranks 1-10 | reached +1 ATR at some point in the 5 sessions | 7,312 | 55.2% [52.0%, 58.1%] | +6.0 pp [+4.4 pp, +7.6 pp] |
| daily | ENS ranks 1-10 | reached -1 ATR at some point in the 5 sessions | 7,312 | 37.7% [33.8%, 41.8%] | -2.6 pp [-4.1 pp, -1.1 pp] |
| daily | ENS ranks 1-10 | reached +2 ATR at some point in the 5 sessions | 7,312 | 25.6% [23.2%, 28.3%] | +4.6 pp [+3.3 pp, +6.0 pp] |
| daily | ENS ranks 1-10 | reached -2 ATR at some point in the 5 sessions | 7,312 | 12.2% [9.8%, 15.1%] | -1.7 pp [-3.2 pp, -0.5 pp] |
| daily | ENS ranks 1-10 | +1 ATR before -1 ATR (of the paths where one came first) | 6,057 | 60.4% [56.1%, 64.1%] | +3.9 pp [+2.3 pp, +5.5 pp] |
| daily | ENS ranks 1-10 | after -1 ATR came first: ended above C0 | 2,400 | 19.6% [16.9%, 22.3%] | +4.2 pp [+2.4 pp, +5.9 pp] |
| daily | ENS ranks 1-10 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | 1,640 | 51.8% [47.8%, 55.6%] | +2.2 pp [-0.2 pp, +4.6 pp] |
| daily | ENS ranks 1-10 | after a session-1 close >= +0.5 ATR: ended below C0 | 1,640 | 19.9% [16.9%, 23.2%] | -1.8 pp [-3.7 pp, +0.1 pp] |
| daily | ENS ranks 1-10 | BigMove's trade: session-1 open to session-5 close, before costs | 7,312 | 1.43% [0.65%, 2.18%] | +1.15% [+0.85%, +1.47%] |
| daily | ENS ranks 1-10 | 10-day close from C0 | 7,312 | 0.57 [0.30, 0.83] | +0.30 [+0.21, +0.39] |
| daily | ENS ranks 1-10 | best high of 10 sessions from C0 | 7,312 | 2.23 [2.05, 2.42] | +0.24 [+0.16, +0.33] |
| daily | ENS ranks 1-10 | worst low of 10 sessions from C0 | 7,312 | -1.36 [-1.53, -1.22] | +0.11 [+0.03, +0.20] |
| daily | ENS ranks 1-10 | 10-day close above C0 | 7,312 | 58.8% [54.2%, 63.4%] | +6.2 pp [+4.5 pp, +7.8 pp] |
| daily | ENS ranks 1-10 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) | 7,312 | 1.57% [0.68%, 2.41%] | +1.28% [+0.94%, +1.65%] |
| daily | ENS ranks 1-10 | entry at the open of T+2, exit at the open of T+7, net of 35 bp | 7,312 | 1.23% [0.35%, 2.10%] | +0.95% [+0.58%, +1.37%] |
| daily | ENS ranks 1-10 | entry at the open of T+3, exit at the open of T+8, net of 35 bp | 7,312 | 1.05% [0.17%, 1.90%] | +0.78% [+0.40%, +1.21%] |
| daily | ENS ranks 1-10 | entry at the open of T+4, exit at the open of T+9, net of 35 bp | 7,312 | 0.90% [0.04%, 1.72%] | +0.62% [+0.26%, +1.02%] |
| daily | ENS ranks 1-10 | entry at the open of T+5, exit at the open of T+10, net of 35 bp | 7,312 | 0.77% [-0.09%, 1.61%] | +0.49% [+0.14%, +0.85%] |
| daily | ENS ranks 1-10 | entry at the open of T+6, exit at the open of T+11, net of 35 bp | 7,312 | 0.70% [-0.17%, 1.52%] | +0.42% [+0.10%, +0.75%] |
| daily | ENS ranks 1-10 | entry at the open of T+7, exit at the open of T+12, net of 35 bp | 7,312 | 0.63% [-0.23%, 1.40%] | +0.34% [+0.04%, +0.63%] |
| daily | ENS ranks 1-10 | entry at the open of T+8, exit at the open of T+13, net of 35 bp | 7,312 | 0.63% [-0.22%, 1.41%] | +0.34% [+0.03%, +0.63%] |
| daily | ENS ranks 1-10 | entry at the open of T+9, exit at the open of T+14, net of 35 bp | 7,312 | 0.64% [-0.23%, 1.44%] | +0.33% [+0.03%, +0.64%] |
| daily | ENS ranks 1-10 | entry at the open of T+10, exit at the open of T+15, net of 35 bp | 7,312 | 0.70% [-0.14%, 1.50%] | +0.39% [+0.09%, +0.71%] |
| daily | ENS ranks 1-10 | waiting 1 session(s): entry at T+2 minus entry at T+1 (same paths) | 7,312 | -0.34% [-0.52%, -0.14%] | -0.33% [-0.47%, -0.19%] |
| daily | ENS ranks 1-10 | waiting 2 session(s): entry at T+3 minus entry at T+1 (same paths) | 7,312 | -0.51% [-0.80%, -0.19%] | -0.50% [-0.70%, -0.31%] |
| daily | ENS ranks 1-10 | waiting 3 session(s): entry at T+4 minus entry at T+1 (same paths) | 7,312 | -0.67% [-1.09%, -0.22%] | -0.66% [-0.92%, -0.39%] |
| daily | ENS ranks 1-10 | waiting 4 session(s): entry at T+5 minus entry at T+1 (same paths) | 7,312 | -0.80% [-1.33%, -0.22%] | -0.79% [-1.07%, -0.50%] |
| daily | ENS ranks 1-10 | waiting 5 session(s): entry at T+6 minus entry at T+1 (same paths) | 7,312 | -0.87% [-1.55%, -0.17%] | -0.86% [-1.21%, -0.51%] |
| daily | ENS ranks 1-10 | waiting 6 session(s): entry at T+7 minus entry at T+1 (same paths) | 7,312 | -0.93% [-1.73%, -0.13%] | -0.94% [-1.31%, -0.56%] |
| daily | ENS ranks 1-10 | waiting 7 session(s): entry at T+8 minus entry at T+1 (same paths) | 7,312 | -0.93% [-1.84%, 0.01%] | -0.94% [-1.35%, -0.53%] |
| daily | ENS ranks 1-10 | waiting 8 session(s): entry at T+9 minus entry at T+1 (same paths) | 7,312 | -0.93% [-1.89%, 0.10%] | -0.94% [-1.34%, -0.53%] |
| daily | ENS ranks 1-10 | waiting 9 session(s): entry at T+10 minus entry at T+1 (same paths) | 7,312 | -0.87% [-1.89%, 0.25%] | -0.89% [-1.28%, -0.45%] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J01 | 713 | 27.1% [23.1%, 30.9%] | +0.2 pp [-3.6 pp, +3.8 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J02 | 713 | 26.1% [22.2%, 30.4%] | +0.4 pp [-3.5 pp, +4.4 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J03 | 713 | 12.3% [9.2%, 15.6%] | -5.4 pp [-8.0 pp, -2.6 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J04 | 713 | 18.7% [15.0%, 22.8%] | +2.3 pp [-1.2 pp, +6.0 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J05 | 713 | 9.1% [6.7%, 11.6%] | +2.8 pp [+0.6 pp, +5.0 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J06 | 713 | 4.8% [2.4%, 8.1%] | -0.9 pp [-2.9 pp, +1.8 pp] |
| intraday | D ranks 1-3 | share of 3-minute paths in intraday region J07 | 713 | 2.0% [1.0%, 3.1%] | +0.5 pp [-0.5 pp, +1.5 pp] |
| intraday | D ranks 1-3 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 607 | 55.0% [49.4%, 61.1%] | +3.6 pp [-0.5 pp, +7.1 pp] |
| intraday | D ranks 1-3 | first 30 minutes: move from the open | 849 | 0.04 [0.00, 0.07] | +0.04 [+0.01, +0.07] |
| intraday | D ranks 1-3 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 849 | 5.1% [3.6%, 6.8%] | +1.7 pp [+0.2 pp, +3.4 pp] |
| intraday | D ranks 1-3 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 849 | 3.8% [2.2%, 5.5%] | +0.8 pp [-0.7 pp, +2.4 pp] |
| intraday | D ranks 1-3 | session 1: the high came before the low | 815 | 47.7% [44.1%, 51.3%] | -9.6 pp [-13.5 pp, -5.7 pp] |
| intraday | D ranks 1-3 | after -1 ATR came first: back to C0 later (3-minute) | 273 | 45.1% [37.1%, 53.7%] | +11.3 pp [+3.7 pp, +19.7 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J01 | 735 | 24.1% [21.0%, 27.3%] | -2.6 pp [-5.4 pp, +0.3 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J02 | 735 | 26.0% [22.3%, 30.1%] | +0.4 pp [-3.3 pp, +3.9 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J03 | 735 | 14.1% [9.9%, 18.5%] | -3.3 pp [-6.4 pp, +0.1 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J04 | 735 | 19.0% [15.7%, 22.5%] | +2.3 pp [-0.8 pp, +5.4 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J05 | 735 | 9.1% [6.3%, 12.3%] | +2.6 pp [+0.1 pp, +5.2 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J06 | 735 | 5.0% [2.6%, 8.3%] | -0.4 pp [-2.4 pp, +2.1 pp] |
| intraday | ENS ranks 1-3 | share of 3-minute paths in intraday region J07 | 735 | 2.6% [1.3%, 4.0%] | +1.0 pp [-0.1 pp, +2.3 pp] |
| intraday | ENS ranks 1-3 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 619 | 58.0% [52.0%, 64.8%] | +6.1 pp [+1.8 pp, +9.9 pp] |
| intraday | ENS ranks 1-3 | first 30 minutes: move from the open | 873 | 0.08 [0.05, 0.11] | +0.08 [+0.06, +0.11] |
| intraday | ENS ranks 1-3 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 873 | 4.0% [2.7%, 5.5%] | +0.8 pp [-0.4 pp, +2.2 pp] |
| intraday | ENS ranks 1-3 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 873 | 3.8% [2.4%, 5.4%] | +0.7 pp [-0.6 pp, +2.3 pp] |
| intraday | ENS ranks 1-3 | session 1: the high came before the low | 835 | 44.4% [40.9%, 48.0%] | -12.6 pp [-16.3 pp, -9.2 pp] |
| intraday | ENS ranks 1-3 | after -1 ATR came first: back to C0 later (3-minute) | 260 | 41.5% [35.1%, 49.3%] | +8.9 pp [+2.8 pp, +16.1 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J01 | 1,711 | 22.3% [19.7%, 25.0%] | -4.1 pp [-6.0 pp, -2.4 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J02 | 1,711 | 25.7% [22.6%, 28.8%] | -0.2 pp [-2.7 pp, +2.5 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J03 | 1,711 | 17.1% [13.0%, 21.1%] | -0.0 pp [-2.6 pp, +2.4 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J04 | 1,711 | 18.6% [15.5%, 22.0%] | +1.1 pp [-1.0 pp, +3.1 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J05 | 1,711 | 9.4% [7.6%, 11.1%] | +2.7 pp [+1.3 pp, +4.1 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J06 | 1,711 | 4.6% [3.1%, 6.3%] | -0.3 pp [-1.5 pp, +0.8 pp] |
| intraday | D ranks 4-10 | share of 3-minute paths in intraday region J07 | 1,711 | 2.3% [1.2%, 3.5%] | +0.9 pp [-0.0 pp, +2.0 pp] |
| intraday | D ranks 4-10 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 1,455 | 58.4% [52.5%, 64.7%] | +4.8 pp [+2.2 pp, +7.7 pp] |
| intraday | D ranks 4-10 | first 30 minutes: move from the open | 2,046 | 0.05 [0.03, 0.07] | +0.05 [+0.04, +0.07] |
| intraday | D ranks 4-10 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 2,046 | 4.7% [3.7%, 5.7%] | +1.3 pp [+0.3 pp, +2.3 pp] |
| intraday | D ranks 4-10 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 2,046 | 3.6% [2.7%, 4.7%] | +0.7 pp [-0.1 pp, +1.5 pp] |
| intraday | D ranks 4-10 | session 1: the high came before the low | 1,987 | 50.6% [47.7%, 53.6%] | -6.3 pp [-8.7 pp, -3.8 pp] |
| intraday | D ranks 4-10 | after -1 ATR came first: back to C0 later (3-minute) | 605 | 39.3% [34.5%, 44.5%] | +6.2 pp [+1.9 pp, +10.6 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J01 | 1,722 | 23.3% [20.4%, 26.1%] | -3.4 pp [-5.6 pp, -1.1 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J02 | 1,722 | 28.5% [25.7%, 31.2%] | +2.6 pp [+0.3 pp, +4.8 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J03 | 1,722 | 14.8% [11.7%, 17.8%] | -2.4 pp [-4.3 pp, -0.6 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J04 | 1,722 | 17.9% [15.2%, 20.6%] | +0.7 pp [-1.0 pp, +2.5 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J05 | 1,722 | 8.9% [7.4%, 10.6%] | +2.4 pp [+1.1 pp, +3.9 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J06 | 1,722 | 4.9% [3.2%, 6.9%] | -0.1 pp [-1.1 pp, +1.0 pp] |
| intraday | ENS ranks 4-10 | share of 3-minute paths in intraday region J07 | 1,722 | 1.6% [0.8%, 2.5%] | +0.2 pp [-0.4 pp, +0.9 pp] |
| intraday | ENS ranks 4-10 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 1,456 | 58.3% [52.6%, 63.9%] | +4.6 pp [+1.8 pp, +7.5 pp] |
| intraday | ENS ranks 4-10 | first 30 minutes: move from the open | 2,054 | 0.05 [0.03, 0.07] | +0.05 [+0.03, +0.07] |
| intraday | ENS ranks 4-10 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 2,054 | 4.6% [3.6%, 5.6%] | +1.3 pp [+0.4 pp, +2.2 pp] |
| intraday | ENS ranks 4-10 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 2,054 | 3.2% [2.0%, 4.7%] | +0.3 pp [-0.5 pp, +1.4 pp] |
| intraday | ENS ranks 4-10 | session 1: the high came before the low | 1,995 | 52.0% [49.4%, 54.6%] | -5.2 pp [-7.5 pp, -2.9 pp] |
| intraday | ENS ranks 4-10 | after -1 ATR came first: back to C0 later (3-minute) | 607 | 41.0% [36.0%, 46.9%] | +7.8 pp [+3.4 pp, +12.3 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J01 | 2,424 | 23.7% [21.4%, 26.0%] | -2.9 pp [-4.5 pp, -1.3 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J02 | 2,424 | 25.8% [23.1%, 28.5%] | +0.0 pp [-2.4 pp, +2.4 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J03 | 2,424 | 15.7% [12.1%, 19.1%] | -1.6 pp [-3.8 pp, +0.4 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J04 | 2,424 | 18.6% [15.8%, 21.7%] | +1.4 pp [-0.4 pp, +3.3 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J05 | 2,424 | 9.3% [7.7%, 11.0%] | +2.8 pp [+1.5 pp, +4.1 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J06 | 2,424 | 4.7% [3.0%, 6.5%] | -0.5 pp [-1.6 pp, +0.7 pp] |
| intraday | D ranks 1-10 | share of 3-minute paths in intraday region J07 | 2,424 | 2.2% [1.3%, 3.1%] | +0.8 pp [+0.1 pp, +1.5 pp] |
| intraday | D ranks 1-10 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 2,062 | 57.4% [52.1%, 63.1%] | +4.5 pp [+2.2 pp, +6.8 pp] |
| intraday | D ranks 1-10 | first 30 minutes: move from the open | 2,895 | 0.05 [0.03, 0.07] | +0.05 [+0.03, +0.07] |
| intraday | D ranks 1-10 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 2,895 | 4.8% [3.8%, 5.8%] | +1.4 pp [+0.5 pp, +2.4 pp] |
| intraday | D ranks 1-10 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 2,895 | 3.7% [2.7%, 4.7%] | +0.7 pp [-0.1 pp, +1.5 pp] |
| intraday | D ranks 1-10 | session 1: the high came before the low | 2,802 | 49.8% [47.5%, 52.2%] | -7.3 pp [-9.2 pp, -5.2 pp] |
| intraday | D ranks 1-10 | after -1 ATR came first: back to C0 later (3-minute) | 878 | 41.1% [36.5%, 45.9%] | +7.8 pp [+3.4 pp, +12.2 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J01 | 2,457 | 23.6% [21.1%, 26.0%] | -3.1 pp [-5.0 pp, -1.2 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J02 | 2,457 | 27.8% [25.1%, 30.4%] | +1.9 pp [-0.2 pp, +4.0 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J03 | 2,457 | 14.6% [11.4%, 17.6%] | -2.7 pp [-4.4 pp, -0.9 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J04 | 2,457 | 18.2% [16.0%, 20.7%] | +1.2 pp [-0.4 pp, +2.9 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J05 | 2,457 | 9.0% [7.2%, 10.8%] | +2.4 pp [+1.2 pp, +3.7 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J06 | 2,457 | 5.0% [3.1%, 7.2%] | -0.2 pp [-1.4 pp, +1.2 pp] |
| intraday | ENS ranks 1-10 | share of 3-minute paths in intraday region J07 | 2,457 | 1.9% [1.1%, 2.8%] | +0.4 pp [-0.1 pp, +1.1 pp] |
| intraday | ENS ranks 1-10 | +1 ATR before -1 ATR, 3-minute resolution (of those resolved) | 2,075 | 58.2% [52.8%, 63.8%] | +5.1 pp [+2.5 pp, +7.7 pp] |
| intraday | ENS ranks 1-10 | first 30 minutes: move from the open | 2,927 | 0.06 [0.04, 0.08] | +0.06 [+0.05, +0.08] |
| intraday | ENS ranks 1-10 | session 1: rallied 0.5 ATR then gave 0.5 ATR back before 10:15 | 2,927 | 4.4% [3.5%, 5.3%] | +1.1 pp [+0.4 pp, +1.9 pp] |
| intraday | ENS ranks 1-10 | session 1: fell 0.5 ATR then won 0.5 ATR back before 10:15 | 2,927 | 3.4% [2.3%, 4.7%] | +0.5 pp [-0.3 pp, +1.4 pp] |
| intraday | ENS ranks 1-10 | session 1: the high came before the low | 2,830 | 49.8% [47.3%, 52.2%] | -7.4 pp [-9.6 pp, -5.2 pp] |
| intraday | ENS ranks 1-10 | after -1 ATR came first: back to C0 later (3-minute) | 867 | 41.2% [36.7%, 46.4%] | +8.1 pp [+4.0 pp, +12.6 pp] |

_What the model adds beyond state and regime, measured on the same dates and cells, against stocks the same engine did not pick at any rank that day. Ranks 4-10 replicate ranks 1-3 on picks that were not traded. No labels here: the picks are judged by the forward paper test, not by this table._

## ETFs (kept out of the atlas)

6 ETFs by NSE's ETF list C:\QuantData\pathlab\ref\eq_etfseclist.csv (355 names, 6 of them in the panel) plus the name rule (BEES / ETF / IETF endings: ETFs the cache holds under an older name). They are out of the families and every atlas table; their paths are summarised here only (descriptive).

| regime | paths | 5-day close above C0 | 5-day close from C0 | best high of the window from C0 (MFE) | worst low of the window from C0 (MAE) | reached +1 ATR at some point in the 5 sessions | reached -1 ATR at some point in the 5 sessions | reached +2 ATR at some point in the 5 sessions | reached -2 ATR at some point in the 5 sessions | +1 ATR before -1 ATR (of the paths where one came first) | after -1 ATR came first: ended above C0 | after a session-1 close >= +0.5 ATR: session 5 closed higher still | after a session-1 close >= +0.5 ATR: ended below C0 | BigMove's trade: session-1 open to session-5 close, before costs | 10-day close from C0 | entry at the open of T+1, exit at the open of T+6, net of 35 bp (BigMove's OPEN6 timing) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_bullish | 753 | 56.7% [48.6%, 64.6%] | 0.12 [-0.07, 0.31] | 1.60 [1.41, 1.81] | -1.01 [-1.26, -0.80] | 61.4% [55.0%, 67.4%] | 33.6% [26.9%, 40.5%] | 27.5% [22.2%, 33.1%] | 14.1% [9.6%, 19.0%] | 69.6% [62.5%, 76.0%] | 15.0% [8.6%, 23.0%] | 50.5% [38.5%, 61.2%] | 24.3% [15.6%, 34.0%] | -0.16% [-0.54%, 0.21%] | 0.04 [-0.30, 0.36] | 0.02% [-0.35%, 0.38%] |
| narrow_bullish | 646 | 56.3% [48.8%, 62.8%] | 0.25 [-0.02, 0.49] | 1.84 [1.47, 2.26] | -0.96 [-1.14, -0.81] | 56.2% [49.3%, 62.8%] | 34.5% [27.7%, 42.0%] | 30.8% [23.4%, 38.6%] | 15.3% [10.2%, 21.4%] | 67.0% [59.2%, 73.8%] | 21.1% [12.5%, 30.8%] | 60.6% [50.4%, 69.2%] | 19.3% [11.9%, 28.2%] | -0.03% [-0.59%, 0.47%] | 0.64 [0.16, 1.10] | 0.17% [-0.45%, 0.71%] |
| mixed | 266 | 48.9% [39.1%, 58.5%] | 0.08 [-0.14, 0.31] | 1.53 [1.31, 1.78] | -0.93 [-1.13, -0.77] | 60.2% [51.3%, 68.6%] | 34.6% [27.4%, 41.8%] | 22.9% [15.8%, 30.4%] | 11.3% [6.8%, 16.7%] | 67.0% [59.0%, 75.2%] | 14.3% [5.8%, 25.5%] | 52.4% [29.1%, 74.2%] | 28.6% [12.9%, 47.2%] | -0.22% [-0.79%, 0.35%] | 0.18 [-0.26, 0.63] | -0.27% [-0.84%, 0.29%] |
| broad_bearish | 215 | 53.0% [42.3%, 66.1%] | 0.17 [-0.06, 0.49] | 1.38 [1.04, 1.91] | -0.77 [-0.91, -0.66] | 49.3% [40.0%, 61.0%] | 29.8% [21.7%, 39.2%] | 19.5% [10.8%, 32.4%] | 4.2% [1.4%, 8.0%] | 64.8% [56.8%, 73.1%] | 17.6% [4.9%, 36.4%] | 52.0% [25.0%, 77.8%] | 12.0% [0.0%, 35.7%] | -0.19% [-0.85%, 0.56%] | 0.39 [0.05, 0.75] | -0.19% [-0.90%, 0.64%] |
| high_stress | 278 | 54.3% [43.5%, 63.1%] | 0.01 [-0.47, 0.33] | 1.46 [1.15, 1.73] | -1.16 [-1.69, -0.82] | 53.2% [42.6%, 62.4%] | 40.6% [31.6%, 52.0%] | 23.0% [14.6%, 31.2%] | 18.3% [9.6%, 29.4%] | 59.5% [48.0%, 68.4%] | 21.2% [10.2%, 33.9%] | 48.8% [31.7%, 66.7%] | 19.5% [6.5%, 37.5%] | -0.43% [-1.90%, 0.68%] | -0.01 [-1.00, 0.62] | -0.01% [-1.67%, 1.23%] |
| all | 2,158 | 55.0% [50.3%, 59.7%] | 0.15 [0.01, 0.28] | 1.62 [1.45, 1.82] | -0.98 [-1.11, -0.87] | 57.4% [53.3%, 61.6%] | 34.5% [30.5%, 38.8%] | 26.6% [22.7%, 30.6%] | 13.7% [10.6%, 16.9%] | 66.8% [62.6%, 71.0%] | 17.9% [13.1%, 23.0%] | 54.0% [47.5%, 60.3%] | 21.6% [16.8%, 27.2%] | -0.17% [-0.49%, 0.13%] | 0.27 [0.00, 0.52] | 0.01% [-0.34%, 0.32%] |

## Validation

- Point in time: states (tl_state) and regimes (tl_context) use bars up to the T0 close only; path values use only sessions after T0. pathlab's test suite scrambles every bar after T0 and checks that every T0 value is unchanged.
- Overlapping windows: intervals from circular blocks of 10 consecutive T0 dates, all stocks of a drawn date together, 2,000 resamples, seed 7. Non-overlapping check: 99.7% of 702 estimates inside the every-5th-T0 sample's interval (need 90%) -> PASS; median interval width ratio 1.09 (about sqrt(5) = 2.24 if overlapping windows were independent; less means the main intervals already carry the overlap).
- Many comparisons: Benjamini-Hochberg 5% over every test of a period: discovery: 30 of 4,537 pass, about 1.5 expected false.
- Sealed: families, atlas and report read T0 up to 2022-12-31 only; pathlab's suite scrambles every later row and checks that every table is unchanged. The walk-forward (2023, 2024, 2025) runs on the frozen candidate list only.
- p-values: Student's t with (separate 10-session stretches - 1) degrees of freedom on the bootstrap standard error (the normal reference was too generous in the tails in synthetic no-effect worlds).
- Minimum support: described with 200 dates and 1,000 paths over 2020-2026 (intraday 100 / 300); labelled only with 50 dates, 250 paths and 8 separate 10-session stretches in EACH period (intraday 30 / 150 / 6).
- Integrity against tradelab's export: 11,824 of 11,824 comparable picks match (100.00%; required 99.5%).
- Absent world from your own data: the random-walk version of every path goes through the same code. What state or regime information survives there comes from which stocks sit in a state (composition), not from timing.

## Limitations and open questions

- Survivorship: stocks delisted before the cache was built are missing, so paths that ended in delisting are under-represented (likely fewer persistent declines - an inference, not measured).
- No AMFI lists: liquidity tiers (60-session median turnover at T0) stand in for market-cap segments.
- 3-minute bars start 2021-10-01 and cover only the stocks with a 3-minute file; the intraday atlas is a subset, and covered stocks may differ from the rest.
- Breadth counts the cached survivors, not NSE's official advance/decline; the regime labels carry this.
- States and regimes are research defaults (declared 24-25 Oct); the atlas tests whether they carry information, it does not assume it.
- Families from k-means are groups of similar shapes; 'separated' requires two modes between neighbours. Regions are a partition of a continuum and must not be read as distinct behaviours.
- Nothing here is a trading rule. Phase 2 (what predicts a path) does not start until this atlas is reviewed.
- Not in this build: walk-forward folds 2023 / 2024 / 2025 and the 2026 labels (built with 'unseal', after the candidate list is frozen).
- Not in this build: the two new nulls (shared donor days; shuffled order) - the random-walk null stays as declared.
- Not in this build: empirical-Bayes pooled estimates and the rare-path rates.
- Not in this build: the 12-number event lens and the 14-point intraday grid for the family vectors.
- Not in this build: the survivorship rerun (coverage COV_20261025_002: 0 of 1,436 stocks stop trading inside the cache).

## Files in this run

| file | what it holds |
|---|---|
| atlas/labels.csv | every comparison with its discovery, confirmation and all-period values and its label |
| atlas/tests.csv | every test: difference, interval, p, q, false-discovery pass |
| atlas/daily/stats.csv, atlas/intraday/stats.csv | every measure x group x period: value, 95% interval, n, dates |
| atlas/*/support.csv, n_eff.csv | observations, dates, stocks, effective sample size per group |
| atlas/daily/quantiles.csv, family_quantiles.csv | distribution quantiles (with intervals) and inside each family |
| atlas/*/years.csv, tiers.csv | year-by-year and liquidity-tier values with intervals |
| atlas/*/vs_random_walk.csv | every measure against its random-walk version |
| atlas/*/mutual_information.json | the headline information tests |
| atlas/daily/transitions_*.csv | state transitions, sequences, regime changes |
| atlas/*/picks.csv | D and ENS picks (ranks 1-3, 4-10, 1-10) against the universe |
| atlas/daily/event_pages.csv, event_tests.csv | every event page and its tests against the same state with no event |
| atlas/daily/delay_curve.csv, delay_tests.csv | the delayed trade d = 1..10 per group, and the gain over T+1 |
| atlas/daily/etf.csv | ETF paths by regime (kept out of the atlas) |
| families/*/families.json, k_scan_table.csv | the family search, chosen k, centres, names, checks |
| audit/audit.md | what the audit found |
| summary.json, outputs.sha256 | the run in one file; every file's hash |
