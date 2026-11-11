# BigMove full universe | Extreme SDE x EXACT frozen setup definitions

Frozen source validated: `483f1539324f3ae5c06756b00b32c189f5eb995f73956a681673f005ce399c8f`; evaluator: original `setuplab.trigger` (nine-decimal comparison / missing semantics).
Scanned 1,505 cached stock files/panel symbols, 1,365,771 eligible synthetic D0 sessions.
Every stock/date is eligible (not only BigMove Top-3). Costs = 0.35 pp round trip. No portfolio constraint.

## Independent setup events (unique symbol + setup + entry date)

## All seven independent setups

| Signal-close SDE10 | N | Mean setup return | Win rate | Loss >=5% |
|---|---:|---:|---:|---:|
| NEG_LT_-0.5 | 90,501 | +0.770% | 53.3% | 10.8% |
| MID | 161,200 | +0.151% | 47.2% | 10.9% |
| POS_GT_+0.5 | 3,213 | -0.321% | 42.5% | 14.0% |

See `*_events_setup_x_signal_sde.csv` for setup-specific groups and `*_candidates_*` for the D0-SDE universe.

## First setup wins

| Signal-close SDE10 | N | Mean setup return | Win rate | Loss >=5% |
|---|---:|---:|---:|---:|
| NEG_LT_-0.5 | 36,271 | +0.579% | 51.6% | 12.1% |
| MID | 68,263 | -0.067% | 45.1% | 12.0% |
| POS_GT_+0.5 | 2,057 | -0.217% | 42.6% | 14.0% |

See `*_events_setup_x_signal_sde.csv` for setup-specific groups and `*_candidates_*` for the D0-SDE universe.

## Interpretation

The pre-entry SDE signal-close groups are most meaningful for unique entry events. A signal is known at the prior close; S2 also needs the next open to gap down.

D0 SDE is valid in the candidate-level watch tests but is not unique when multiple earlier D0s lead to the same trade. Avoid inferring significance from overlapping windows.

**No live modifications.** Neither the user's production files nor the frozen research source is written to.
