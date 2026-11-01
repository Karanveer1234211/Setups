# playbook v1.1 (BMPB2) - the long-position map by state, event and S05: ten playbooks on TradingView, the open entry beside every trade

Built 1 Nov 2026. Each pick's category = tl_state's state and shown event at its close T, the market regime, and S05
(overextension) measured on the chart at T. The LONG-POSITION MAP sends each category to one of ten playbooks (entry +
invalidation + structural stop + target + exits, every field a setting). The Pine strategy trades the playbooks on the
chart, shows the open entry (OPEN6: T+1 open to T+6 open) for the same pick from the chart's own bars, draws the
position's map for the pick you focus on (order, void line, stop, target, close-exit line) and lets you step through
the trades and record a verdict per trade. The Python side exports your picks for the chart and runs the chart's
exact rules on every pick.

| File | What it does |
|---|---|
| BigMove_Playbook.pine | The TradingView strategy (Pine v5) |
| playbook.py | `export` (picks + tl_state context -> Pine input per symbol, review sheets), `sim` (the chart's rules on every pick, per category vs OPEN6), `matrix` (all ten playbooks on every category), `--selftest` |
| pb_core.py | The rules in Python with TradingView's order semantics (the mirror) |
| env_playbook.bat | Session setup (calls v2engine's env_v2.bat; CRLF) |
| tests\ | test_playbook.py (the suite), pine_twin.py (the Pine's logic bar by bar), pine_lint.py (static checks of the Pine), pb_mutate.py (planted bugs), data\NSE_IRCTC_1D.json (396 real daily bars from TradingView) |

Reads production READ ONLY through v2engine 0.3's adapter (pick_meta's run, the cache, tl_state, tl_context).
Writes only under `%PB_OUT%`. Nothing in bigmove_deploy, tradelab, pathlab or v2engine is touched.

## What changed from v1.0

- Ten playbooks instead of six; the map's rules take an optional 4th part, S05: `STATE:EVENT[:REGIME[:S05]]=Pn`.
- Entries: SWHI (buy stop at the last confirmed swing high + O x ATR), STRNG (buy stop at the N-session high), LMRNG
  (limit at the N-session low), all re-set every evening.
- Invalidation while the entry waits (IV / IK): a close under T's low / the event level - IK x ATR(T), or under the
  last swing low / EMA50 - IK x ATR cancels the order: INVALID, no fallback. T itself is checked.
- Stops SWL (swing low - SK x ATR, only below the entry close) and RNG (N-session low - SK x ATR); targets SWH, RNGH,
  EMA50 (each + TK x ATR, only above the entry); time stop TS / TSP; close exit XC / XK (EMA20 / EMA50 / swing low).
- Swings by tl_state's rule (higher than the 3 bars before, not lower than the 3 after, known 3 sessions later).
- On the chart: the map table (rule -> playbook -> how many shown picks it took -> what the playbook does), the S05
  filter, the focus pick's working order each evening (orange dots), its void line (grey dashes), its close-exit line
  (purple dots); S05 in the list, the tooltips, the focus table and the logs (`PBHDR` has a new `s05` column).
- The config code is BMPB2. A v1.0 code (BMPB1) is refused by `sim`: its short form is relative to v1.0's defaults.

## Install (cmd)

Unzip so that `C:\Users\karanvsi\PyCharmMiscProject\playbook\` sits next to `v2engine\`, `tradelab\`, `pathlab\`
(replace the v1.0 files).

    call C:\Users\karanvsi\PyCharmMiscProject\playbook\env_playbook.bat
    python playbook.py --selftest quick

Expected: `92 checks, 0 failed` and last line `VERIFIED (playbook v1.1)` (about 30 seconds). `--selftest` without
`quick` runs 24,000 random cases instead of 6,000 (and lints the Pine where pynescript is installed).

## 1. Export (once; the v1.0 export works unchanged - the line format did not change)

    python playbook.py export --root %CACHE_DAILY_ROOT% --out %PB_OUT%

Default: engines D and ENS, ranks 1-3, signal days 2020-01-01 .. 2022-12-31 (the discovery years). Options:
`--engines D`, `--ranks 1-10`, `--from`, `--to`. Writes under `%PB_OUT%`:

- `pine\<SYMBOL>.txt` - one stock, every category (file name = TradingView's NSE ticker, e.g. `M_M` for M&M)
- `pine_by_category\<STATE>_<EVENT>.txt` - one category, every stock: paste once, then change the chart's symbol
- `review_picks.csv` and `by_category\<STATE>_<EVENT>.csv` - one row per pick (now with S05 from the cache's bars)
- `categories.csv`, `EXPORT.md`

## 2. On TradingView

1. Pine Editor: new script, replace everything with `BigMove_Playbook.pine`, Save, Add to chart.
2. Open the stock's daily chart (NSE:<SYMBOL>).
3. Settings > Inputs > Picks: paste a whole file (`pine\<SYMBOL>.txt`, or a `pine_by_category\` file and switch the
   chart's symbol). The audit table (top left) must say `OK` for the symbol and `1D OK`. Keep Properties as shipped
   (commission 0.175%, bar magnifier off).
4. Step through: `Focus pick #` = 1, 2, 3 ... Blue background = T, yellow = the order working, green = in the trade.
   Orange dots = the working order each evening (or the fixed trigger / limit), grey dashes = the void line, purple
   dashed = the event level, blue line = the entry, red / orange steps = stop / trail, purple dots = the close-exit
   line, green dashes = the target, grey dashed = the OPEN6 trade. Hover a label for the pick's full record.
5. The map table (right, middle) shows each rule, its playbook and how many of the shown picks it took; hover the
   playbook text for every field. Filters: State / Event / Regime / S05; Playbook = P1 .. P10 forces one playbook on
   every pick shown.
6. Record: `Findings` box, one line per trade, `D-20220314-1|BETTER|retest held`. Or fill the columns in the CSVs.
7. Pine Logs: first line `PBCFG` = the full config code; one `PBLOG` CSV line per pick (columns in `PBHDR`).

## 3. The chart's rules on every pick

    python playbook.py sim --root %CACHE_DAILY_ROOT% --out %PB_OUT% --code "BMPB2|P7=O:0.25"
    python playbook.py matrix --root %CACHE_DAILY_ROOT% --out %PB_OUT%

`sim` writes `%PB_OUT%\sim_<hash>\REPORT.md` (per category and playbook: net per pick with unfilled picks counted 0,
OPEN6 net per pick, the paired difference with its 95% block-bootstrap interval over signal days), `trades.csv` (now
with S05) and `summary.csv`. `--force P7` = that playbook on every pick. `matrix` = all ten playbooks on every
category: which playbook works where (in-sample: a hypothesis, not a finding).

## 4. The journal: every pick in tradelab's export, mapped (pb_journal.py)

    python playbook.py journal --root %CACHE_DAILY_ROOT% --out %PB_OUT% --export C:\QuantData\tradelab\export\TLX_20261025_001
    python playbook.py journal ... --all-years --spend-holdout      (every year 2015 .. 2026; spends 2023-25)

Reads the export's trades.parquet READ ONLY (the data behind TRADE_JOURNAL.xlsx, checked against outputs.sha256);
TRADE_JOURNAL.xlsx itself is never opened. Writes `%PB_OUT%\journal\PLAYBOOK_JOURNAL.xlsx` (+ playbook_journal.csv):
Trades (one row per pick: integrity, state / event / regime / S05, BigMove's own trade from the export, the mapped
playbook's order, fill, entry, stop, target, exit, net, OPEN6, selection and per-fill difference in bp, MFE / MAE /
capture, major winner kept, all ten playbooks' differences, the hindsight best, and your columns My verdict / Tags /
Note, carried over by trade id on every re-run), By category, Matrix, By year, Integrity, Read me. `--code` = a map
changed on the chart. Integrity: JOURNAL MATCHED, MISSING RECORD, NOT ON THE CACHE, SYMBOL MISMATCH, STATE DIFFERS,
EVENT DIFFERS, DATA MISMATCH (OPEN6 gross off by more than 0.2%), EVENT LEVEL UNVERIFIED. Summaries use matched picks
only. Verified on a fake export with each defect planted (p13a-d).

## The long-position map (shipped defaults - starting hypotheses from how each state and event should behave)

| rule (first match wins) | playbook | entry | void if | stop / target / exit |
|---|---|---|---|---|
| S08 / S09 (bearish), any event | P1 | the open (2020-22: S08 picks +4.2% D / +5.2% ENS a pick under OPEN6) | - | 5-session hold |
| any state, breakdown (BD_NEW / CONF / STALL) | P1 | the open | - | 5-session hold |
| any state, bear trap (FBD) | P4 | reclaim: buy stop at the breakdown level + 0.25 ATR, 5 sessions | - | stop T's low - 0.25 ATR |
| any state, failed breakout (FBO) | P3 | reclaim: buy stop at the level + 0.1 ATR, 10 sessions | - | stop T's low - 0.25 ATR |
| S01 / S02 / S03 with a breakout NEW / CONF | P2 | retest: limit at the breakout level + 0.25 ATR, 5 sessions | close < level - 0.25 ATR | stop level - 0.25 ATR |
| any state, stalled breakout | P5 | confirmation: buy stop at T's high + 0.1 ATR, 10 sessions | close < T's low - 0.5 ATR | stop T's low - 0.25 ATR |
| S01 overextended (S05 OV / EX) | P8 | trend pullback: limit at EMA20, re-set, 5 sessions | - | stop swing low - 0.25 ATR, trail (3%, 2 ATR), out on a close < EMA20 - 0.25 ATR, max 20 sessions |
| S01 | P1 | the open (= OPEN6) | - | 5-session hold |
| S02 / S03 / S06 | P7 | structure: buy stop at the last swing high + 0.1 ATR, re-set, 10 sessions | close < the last swing low | stop swing low - 0.25 ATR |
| S07 (range) | P9 | range floor: limit at the 20-session low + 0.25 ATR, re-set, 10 sessions | - | stop 20-session low - 0.25 ATR, target the 20-session high, 10 sessions |
| S12 (unstable) | P5 | confirmation above T's high | close < T's low - 0.5 ATR | stop T's low - 0.25 ATR |
| everything else | P1 | the open | - | 5-session hold |

P6 (limit at T's close - 1 ATR, 3 sessions) is kept from v1.0 and unmapped. Unless a row says otherwise the exit is
the plain 5-session hold (sell at the 6th session's open), so a playbook's difference from OPEN6 is mostly its entry
and its stop. Every number is a setting.

## The rules

Entry (orders placed at a close act from the next session; ATR = ta.atr(14) on the chart): OPEN / DELAY / STH / STPD
/ STLV / LMLV / LMTC / LMEMA (as v1.0) / SWHI buy stop at the last swing high + O x ATR / STRNG buy stop at the
N-session high + O x ATR / LMRNG limit at the N-session low + O x ATR (the last three re-set every evening) / SKIP.
STH / STLV whose trigger is at or below the last close are not placed or are cancelled; STPD / SWHI / STRNG place
nothing that evening. F = OPEN: nothing filled in the window -> market at the next open (not after INVALID).
Exits, in this order at a close: the hold H (X = OPEN next open, X = CLOSE that close), the time stop TS, the close
exit XC; protective stop / target placed at the entry session's close (the entry session has no stop); trail as v1.0.
A gap through a stop or target fills at the open; both inside one bar: open -> the nearer extreme -> the other ->
close (TradingView's rule without the magnifier). Net = (exit - entry - c x (entry + exit)) / entry, c = 0.175%.

## Checks the chart shows you

- TV check: TradingView's own net per trade vs the table's; anything above 0.0001% = Properties' commission differs.
- Data check: per pick, OPEN6 gross from the chart vs from the cache; above 0.2% is flagged.
- TradingView fills at prices rounded to the tick; `sim` does not round: up to one tick apart.
- S05 is measured on the chart's bars (ta.ema / ta.atr) and in `sim` on the cache's: a pick right at a threshold can
  differ (the review sheet shows the cache's S05).

## Verified here / not

- pb_core by hand: every fill rule, every entry (SWHI / STRNG / LMRNG included), every invalidation, stop, target,
  time stop and close exit, every status and fallback; swings (ties included), ranges and S05 by hand.
- The Pine's logic as a bar-by-bar twin with a TradingView-style broker (tests\pine_twin.py) = pb_core on 24,000
  random price paths x random playbooks (every field random), covering every entry, every status (INVALID included)
  and every exit reason (TSTOP and XCLOSE included); and on **real NSE bars from TradingView** (IRCTC, Jun 2021 - Dec
  2022, its 2021 spike and crash included): all ten shipped playbooks at every session as T, 3,740 cases, identical.
- The Pine itself: parsed (pynescript) and linted (built-in names and keyword arguments, declare-before-use, Pick
  fields, functions; 4 of 4 planted mistakes in the v1.1 code caught by the linter). **It has not been compiled by
  TradingView** - that happens the first time you add it to a chart. A compile error: send me the message and the line
  number.
- Exporter and sim on a fake production cache; a planted category effect is found, an absent one is not; null worlds
  flag 'better' at the expected rate. 10 new planted bugs (tests\pb_mutate.py), each caught.
- 89 checks (full, Pine linted), 0 failed, on Python 3.13 / numpy 2.5.3 / pandas 3.0.5; the quick suite (88) also on
  Python 3.12 / numpy 2.4.1 / pandas 2.3.3.
- Your cache has not been read with v1.1 yet.

## Discipline

2020-22 is the discovery period: what you see on the charts there is a hypothesis. `--to` after 2022-12-31 is refused
unless `--spend-holdout` (recorded in the ledger). To test a playbook on 2023-25: write its config code down first,
run it once.
