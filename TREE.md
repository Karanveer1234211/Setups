# The entry tree - history (setuplab v1.1)

TREE.json sha256 `5cd4571765c2de80` (frozen 2026-11-09T12:58:00+05:30). Window 2021-01-01 .. 2026-09-22, Rs 5 L per book, 3 positions, no MTF, 0.35 pp costs; each number is the average of the first five sessions as start days; worst fall = the book marked daily; both = two books of Rs 2.5 L.

**RECONCILED: the same numbers as the declaration's history (within 0.05 points).**

Cut-offs (jumpy = s_atr14 above): 2021 5.7654% (declared 5.7654%: same); 2022 5.6417% (declared 5.6417%: same); 2023 5.7516% (declared 5.7516%: same); 2024 5.3513% (declared 5.3513%: same); 2025 5.4930% (declared 5.4930%: same); 2026 5.5220% (declared 5.5220%: same)

## Money

| | D baseline | D tree | ENS baseline | ENS tree | both baselines (Rs 2.5 L each) | both trees (Rs 2.5 L each) |
|---|---:|---:|---:|---:|---:|---:|
| A year | +58.3% (+52..+76) | +117.4% (+115..+122) | +79.5% (+35..+99) | +107.5% (+106..+111) | +72.8% (+50..+82) | +112.8% (+110..+116) |
| Rs 5 L became | Rs 72.2 L | Rs 423.9 L | Rs 169.4 L | Rs 324.0 L | Rs 120.8 L | Rs 374.0 L |
| Worst fall (marked daily) | 46.7% | 24.1% | 45.3% | 29.5% | 41.8% | 25.9% |
| Worst month | -25.2% | -20.1% | -24.6% | -13.3% | -24.0% | -17.2% |
| Longest wait for a new high | 13.3 months | 5.7 months | 10.5 months | 6.0 months | 10.9 months | 7.4 months |
| Losing months | 31% | 26% | 31% | 33% | 27% | 21% |

## Year by year (marked, year ends)

| | D baseline | D tree | ENS baseline | ENS tree | both baselines (Rs 2.5 L each) | both trees (Rs 2.5 L each) |
|---|---:|---:|---:|---:|---:|---:|
| 2021 | +89% | +151% | +84% | +82% | +87% | +117% |
| 2022 | +70% | +173% | +74% | +190% | +73% | +180% |
| 2023 | +25% | +15% | +79% | +58% | +54% | +34% |
| 2024 | +158% | +194% | +193% | +135% | +183% | +163% |
| 2025 | +22% | +132% | +51% | +177% | +41% | +153% |
| 2026 | +16% | +58% | +19% | +19% | +22% | +38% |

## Trades

| | D baseline | D tree | ENS baseline | ENS tree | both baselines (Rs 2.5 L each) | both trees (Rs 2.5 L each) |
|---|---:|---:|---:|---:|---:|---:|
| Trades a week | 2.8 | 2.8 | 2.8 | 2.8 | 5.7 | 5.6 |
| Trades that win | 52% | 54% | 52% | 53% | 52% | 53% |
| Mean trade | +1.12% | +1.75% | +1.36% | +1.67% | +1.24% | +1.71% |
| 1 trade in 20 loses at least | 11.9% | 8.3% | 10.9% | 9.5% | 11.5% | 9.0% |
| Days invested | 99% | 90% | 100% | 95% | 100% | 93% |
| Bought through a setup | 0% | 31% | 0% | 18% | 0% | 24% |

## 200 reruns (a random start day of the five, the same random 2% of each engine's picks dropped from every book)

| | median a year | 1 run in 10 below | median worst fall | 1 run in 10 above | beats its baseline |
|---|---:|---:|---:|---:|---:|
| D baseline | +56.3% | +48.6% | 45.5% | 56.3% | - |
| D tree | +115.1% | +107.2% | 24.1% | 26.4% | 100% |
| ENS baseline | +85.4% | +41.9% | 43.6% | 53.9% | - |
| ENS tree | +107.3% | +98.8% | 29.5% | 31.2% | 74% |
| both baselines (Rs 2.5 L each) | +76.8% | +57.8% | 37.1% | 53.0% | - |
| both trees (Rs 2.5 L each) | +111.6% | +105.8% | 24.3% | 26.9% | 100% |

## The tree's actions on the complete ranks 1-3 picks in the window

| engine | action | picks |
|---|---|---:|
| D | BUY AT OPEN (calm, opened up) | 953 |
| D | WAIT: calm, a better-ranked calm pick opened up -> a setup | 146 |
| D | WAIT: calm, a better-ranked calm pick opened up -> no setup: skipped | 593 |
| D | WAIT: calm, opened lower -> a setup | 216 |
| D | WAIT: calm, opened lower -> no setup: skipped | 377 |
| D | WAIT: jumpy -> a setup | 588 |
| D | WAIT: jumpy -> no setup: skipped | 1123 |
| ENS | BUY AT OPEN (calm) | 2561 |
| ENS | WAIT: jumpy -> a setup | 607 |
| ENS | WAIT: jumpy -> no setup: skipped | 990 |

In-sample: the frozen setups and the tree were chosen on this history. Only the forward paper ledger is clean evidence (TREE.json, forward_rule). The rupee totals assume unlimited liquidity.
