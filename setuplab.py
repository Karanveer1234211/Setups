"""
setuplab.py - setuplab v1.1: entry setups for the engines' picks, compared trade by trade with the model's D1 entry.

v1.1 (9 Nov 2026) - the entry tree (TREE.json beside this file; never written by the tool):
    python setuplab.py tree --data <watchlist folder> --out C:\\QuantData\\setuplab
                            every past pick tagged CALM / JUMPY (ATR cut-off from earlier years), with the tree's
                            action, gap, dip / runner marks and its first frozen setup; the four books (D / ENS tree
                            and baseline) and both together -> TREE\\TREE_<date>_<nnn> (TREE.md, tree_tags, trades;
                            reconciled against the declaration's history)
    python setuplab.py tree --data ... --out ... --root %CACHE_DAILY_ROOT% --cutoff-year 2027
                            record a new year's cut-off once (before its first session) for the nightly scan
    scan (unchanged command): also names the tree's orders for the next open per book, keeps the forward books
                            (tree_ledger.jsonl, on time before 09:00 IST) and tags tonight's picks -> the Tree
                            section at the top of SCAN_<date>.md, tree_<date>.csv, tree_book.csv

v0.7 (8 Nov 2026) - the FROZEN setups (FROZEN_SETUPS.json beside this file; never written by the tool):
    python setuplab.py frozen                    check the freeze file (sha256) and list its setups
    python setuplab.py tag  --data <watchlist folder> --features <panel.parquet> --out C:\\QuantData\\setuplab
                            every past pick tagged: which frozen setups entered, on which watch day, both exits,
                            D1 on the same pick -> TAGS\\TAGS_<date>_<nnn> (reconciled against FINAL_001)
    python setuplab.py scan --root %CACHE_DAILY_ROOT% --out C:\\QuantData\\setuplab [--all-missing] [--date ...]
                            the nightly scan (tradelab's env): the last five sessions' picks of the paper ledger
                            against every frozen setup -> scan\\SCAN_<date>.md, scan_<date>.csv, tv_<date>.txt
                            (TradingView import) and the hash-chained, on-time setup_ledger.jsonl

v1.0 (8 Nov 2026) - nodip: the no-dip study v2 (three lists, levels and the session before the pick, pooled engines,
    the replay and the out-of-sample money book):
    python setuplab.py nodip (the same arguments as runners) -> NODIP\\NODIP_<date>_<nnn>

v0.9 (8 Nov 2026) - runners: which picks will NOT dip (tradelab's env, read only):
    python setuplab.py runners --root %CACHE_DAILY_ROOT% --data <watchlist folder> --features <panel.parquet>
                            --out C:\\QuantData\\setuplab   -> RUNNERS\\RUNNERS_<date>_<nnn> (RUNNERS.md, the
                            candidates, what marks a runner, the entries, the replay, the money view)

    python setuplab.py run --data <folder with watchlist.parquet + calendar.parquet> --features <features.parquet>
                           --out <output folder> [--engine D] [--setups default|<setups.json>]
    python setuplab.py reproduce --data ... --features ... --ledgers <folder of delivered *.csv.gz>
    python setuplab.py --selftest

What it does (the rules of the ChatGPT backtester, backtest.pyz, re-implemented vectorised):
  * a setup = a list of conditions, ALL required, read at the open of watch day k (k = 1..5 after the pick):
      <feature>          the feature's value at the previous completed session (k-1; D0 = the signal day)
      <feature>_change   that value minus the session before (stored *_change column if the file has one)
      gap_pct            today's open vs the previous close, %
      pc_vs_d1           the previous close vs the D1 open, %          (known from D2 on; False on D1)
      pc_vs_d1_atr       the same in units of the pick's ATR14 at the signal (s_atr14)
      prev_intraday      the previous session's close vs its open, %   (D2 on)
      prev_ret           the previous session's close vs the close before, %  (D2 on)
      day                the watch day number (blind controls)
      weekday            the watch day's weekday, 0 = Monday (weekly features change on Mondays: their setups
                         can only fire on a Tuesday open - the TUE controls separate the feature from the weekday)
    numbers are rounded to 9 decimals before comparing; 0 does not pass > 0 or < 0
  * entry at the FIRST open whose conditions all hold; a False condition = not today; a missing value with no
    False = the trade is "Missing signal data" (as the original engine); no qualifying open = "No entry"
  * exits: original_d5 = the pick's D5 close; fresh = the close 4 sessions after the entry day (5 sessions held)
  * net % = exit / entry - 1 (in %) - 0.35 (cost)
  * the comparison is Karan's: each setup's OWN filled trades against the model's D1 entry (blind D1, same exit
    rule) on exactly those trade ids. 95% circular block bootstrap over signal days (10-day blocks, 2,000 draws).
    Under original_d5 both legs sell at the same D5 close, so the whole difference is the entry price; under
    fresh the exit moves with the entry, and "after-entry" = setup net minus the D1 trade held from the same
    entry-day open would be the same as the setup itself - so we report the entry discount beside the lift.
  * controls on the same ids: price-only dip entries and bounce markers (no indicators), to see whether a
    setup's conditions add anything beyond "buy after the price has come down"
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import itertools
import json
import re
import sys
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "setuplab v1.1"
WATCH = 5               # watch days D1..D5
PATH = 10               # sessions of path in the watchlist (close_1..close_10)
COST = 0.35
EXITS = ("original_d5", "fresh")
OPS = {">": np.greater, "<": np.less, ">=": np.greater_equal, "<=": np.less_equal}
PRICE_FIELDS = ("gap_pct", "pc_vs_d1", "pc_vs_d1_atr", "prev_intraday", "prev_ret", "day", "weekday")


# ---------------------------------------------------------------------------------------------------- data
class Book:
    """Engine D's picks with their D1..D10 opens / closes and every feature at the previous session of each watch
    day. Arrays are (trades, PATH + 1) with column k = watch day k (column 0 unused for prices)."""

    def __init__(self, wl: pd.DataFrame, cal: pd.Series, feats: pd.DataFrame | None, engine="D", feature_cols=None,
                 ranks=None):
        wl = wl[wl["engine"] == engine].copy() if engine and "engine" in wl.columns else wl.copy()
        self.engine = engine or "ALL"
        if ranks:
            wl = wl[wl["rank"].isin(ranks)]
        wl = wl.sort_values(["signal_day", "rank", "trade_id"]).reset_index(drop=True)
        self.wl = wl
        self.n = len(wl)
        self.ids = wl["trade_id"].astype(str).to_numpy()
        self.signal_day = pd.to_datetime(wl["signal_day"]).dt.normalize().to_numpy()
        self.ok = (wl["status"].astype(str) == "ok").to_numpy() & np.isfinite(wl["net_bp"].astype(float).to_numpy())
        cal = pd.to_datetime(pd.Series(cal)).dt.normalize().sort_values().drop_duplicates().reset_index(drop=True)
        self.cal = cal.to_numpy()
        pos = {d: i for i, d in enumerate(cal)}
        e1 = pd.to_datetime(wl["entry_day"]).dt.normalize()
        self.i1 = np.array([pos.get(d, -1) for d in e1], dtype=np.int64)
        if (self.i1 < 0).any():
            raise ValueError("%d entry days are not in the calendar" % int((self.i1 < 0).sum()))
        ent = wl["entry"].astype(float).to_numpy()
        sc = wl["signal_close"].astype(float).to_numpy()
        O = np.full((self.n, PATH + 1), np.nan)
        C = np.full((self.n, PATH + 1), np.nan)
        PC = np.full((self.n, PATH + 1), np.nan)
        for k in range(1, PATH + 1):
            C[:, k] = ent * (1 + wl["close_%d" % k].astype(float).to_numpy())
            PC[:, k] = sc if k == 1 else ent * (1 + wl["close_%d" % (k - 1)].astype(float).to_numpy())
            O[:, k] = ent if k == 1 else PC[:, k] * (1 + wl["overnight_%d" % k].astype(float).to_numpy())
        # a session past the calendar's end does not exist
        for k in range(1, PATH + 1):
            gone = self.i1 + k - 1 >= len(self.cal)
            O[gone, k] = C[gone, k] = PC[gone, k] = np.nan
        self.O, self.C, self.PC = O, C, PC
        self.sc, self.ent = sc, ent
        self.atr = wl["s_atr14"].astype(float).to_numpy() if "s_atr14" in wl.columns else np.full(self.n, np.nan)
        self.symbols = wl["symbol"].astype(str).str.strip().str.upper().to_numpy()
        self.state = wl["pre_state"].astype(str).to_numpy() if "pre_state" in wl.columns else np.array([""] * self.n)
        self.rank = wl["rank"].astype(int).to_numpy()
        self.engine_arr = wl["engine"].astype(str).to_numpy() if "engine" in wl.columns else \
            np.array([self.engine] * self.n)
        # year index and the two halves of the period (split at the median signal day of the settled picks)
        yrs = pd.DatetimeIndex(self.signal_day).year.to_numpy()
        self.yi = (yrs - yrs.min()) if self.n else yrs
        okd = self.signal_day[self.ok] if self.ok.any() else self.signal_day
        self.split_day = np.sort(okd)[len(okd) // 2] if len(okd) else None
        self.half = (self.signal_day > self.split_day).astype(int) if len(okd) else np.zeros(self.n, int)
        self.span_years = max(1e-9, (okd.max() - okd.min()) / np.timedelta64(365, "D")) if len(okd) else 1.0
        self.features = []
        self.F = {}
        if feats is not None:
            self._join(feats, feature_cols)

    PER_TRADE = ("ids", "signal_day", "ok", "i1", "O", "C", "PC", "sc", "ent", "atr", "symbols", "state", "rank",
                 "engine_arr", "yi", "half")

    def take(self, mask, engine=None):
        """The same book restricted to some picks (e.g. one engine); shares the split day and the span."""
        b = object.__new__(Book)
        b.__dict__.update({k: v for k, v in self.__dict__.items() if k != "_cache"})
        for k in self.PER_TRADE:
            setattr(b, k, getattr(self, k)[mask])
        b.F = {k: v[mask] for k, v in self.F.items()}
        b.wl = self.wl[mask].reset_index(drop=True)
        b.n = int(np.sum(mask))
        b.engine = engine or self.engine
        return b

    def attach(self, path, cols, chunk=8, log=lambda *a: None):
        """Read the feature columns from a big panel a few at a time, only the picks' stocks and only the dates the
        watch windows need (+ 120 days for the changes): memory stays small whatever the panel's size.
        Returns (attached, missing)."""
        import pyarrow.parquet as pq
        names = pq.read_schema(path).names
        low = {c.lower(): c for c in names}
        dk = low.get("timestamp") or low.get("date")
        if "symbol" not in low or not dk:
            raise ValueError("the feature file needs symbol and timestamp (or date) columns")
        want, miss = [], []
        for c in cols:
            (want if c.lower() in low else miss).append(c.lower())
        want = list(dict.fromkeys(want))
        syms = sorted(set(self.symbols))
        first = pd.Timestamp(self.cal[max(0, int(self.i1.min()) - 2)]) - pd.Timedelta(days=120) if self.n else None
        for i in range(0, len(want), chunk):
            part = want[i:i + chunk]
            rc = [low["symbol"], dk] + [low[c] for c in part] + [low[c + "_change"] for c in part
                                                                 if c + "_change" in low]
            F = None
            try:
                F = pq.read_table(path, columns=rc, filters=[(low["symbol"], "in", syms)]).to_pandas()
            except Exception:
                F = None
            if F is None or len(F) == 0:
                F = pd.read_parquet(path, columns=rc)
            self._join(F, part, append=True, min_date=first)
            del F
            log(" features: %d of %d attached" % (min(i + chunk, len(want)), len(want)))
        return want, miss

    def _join(self, feats, feature_cols, append=False, min_date=None):
        f = feats.copy()
        if any(n is not None for n in f.index.names):                 # symbol / date stored as the index
            f = f.reset_index()
        f.columns = [str(c).lower() for c in f.columns]
        dk = "timestamp" if "timestamp" in f.columns else "date"
        if "symbol" not in f.columns or dk not in f.columns:
            raise ValueError("the feature file needs symbol and timestamp (or date) columns")
        f["symbol"] = f["symbol"].astype(str).str.strip().str.upper()
        t = pd.to_datetime(f[dk])
        if t.dt.tz is not None:                                         # a zoned clock -> Indian dates, no zone
            t = t.dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
        f[dk] = t.dt.normalize()
        base = [c for c in (feature_cols or f.columns) if c not in ("symbol", dk) and not c.endswith("_change")]
        f = f[f["symbol"].isin(set(self.symbols))]
        if min_date is not None:
            f = f[f[dk] >= min_date]
        if f.duplicated(["symbol", dk]).any():
            raise ValueError("duplicated symbol/date rows in the feature file")
        f = f.sort_values(["symbol", dk])
        for c in base:
            if c + "_change" not in f.columns:            # the change = this session minus the symbol's previous row
                f[c + "_change"] = f.groupby("symbol")[c].diff()
        cols = base + [c + "_change" for c in base]
        # previous-session date of each watch day k (k = 0: the session before the signal day, v1.0, only on request)
        rows, ks, keys_s, keys_d = [], [], [], []
        for k in range(0 if getattr(self, "prev_session", False) else 1, WATCH + 1):
            j = self.i1 + k - 2
            ok = (j >= 0) & (j < len(self.cal))
            rows.append(np.flatnonzero(ok))
            ks.append(np.full(ok.sum(), k))
            keys_s.append(self.symbols[ok])
            keys_d.append(self.cal[j[ok]])
        L = pd.DataFrame({"row": np.concatenate(rows), "k": np.concatenate(ks), "symbol": np.concatenate(keys_s),
                          dk: np.concatenate(keys_d)})
        M = L.merge(f[["symbol", dk] + cols], on=["symbol", dk], how="left")
        for c in cols:
            A = np.full((self.n, WATCH + 1), np.nan)
            A[M["row"].to_numpy(), M["k"].to_numpy()] = pd.to_numeric(M[c], errors="coerce").to_numpy(float)
            self.F[c] = A
        self.features = (list(self.features) if append else []) + [c for c in base if c not in
                                                                   (self.features if append else [])]

    def field(self, name):
        """(trades, WATCH + 1) values of a condition field at the open of each watch day (cached)."""
        if name in self.F:
            return self.F[name]
        cache = self.__dict__.setdefault("_cache", {})
        if name not in cache:
            cache[name] = self._field(name)
        return cache[name]

    def _field(self, name):
        A = np.full((self.n, WATCH + 1), np.nan)
        if name.startswith("snap:"):                  # the pick's snapshot at the signal close (watchlist pre_*)
            col = name[5:]
            if col not in self.wl.columns:
                raise KeyError("no column %s in the watchlist" % col)
            v = pd.to_numeric(self.wl[col], errors="coerce").astype(float).to_numpy()
            A[:, 1:] = v[:, None]
        elif name == "gap_pct":
            A[:, 1:] = (self.O[:, 1:WATCH + 1] / self.PC[:, 1:WATCH + 1] - 1) * 100
        elif name == "day":
            A[:, 1:] = np.arange(1, WATCH + 1)[None, :]
        elif name == "pc_vs_d1":
            A[:, 2:] = (self.C[:, 1:WATCH] / self.O[:, [1]] - 1) * 100
            A[:, 1] = 0.0                          # nothing to compare on D1: a dip test (< 0) is False there
        elif name == "weekday":
            for k in range(1, WATCH + 1):
                j = np.minimum(self.i1 + k - 1, len(self.cal) - 1)
                A[:, k] = pd.DatetimeIndex(self.cal[j]).weekday
        elif name == "pc_vs_d1_atr":
            A[:, 2:] = (self.C[:, 1:WATCH] / self.O[:, [1]] - 1) / self.atr[:, None]
            A[:, 1] = 0.0
        elif name == "prev_intraday":
            A[:, 2:] = (self.C[:, 1:WATCH] / self.O[:, 1:WATCH] - 1) * 100
            A[:, 1] = 0.0
        elif name == "prev_ret":
            prev = np.column_stack([self.sc, self.C[:, 1:WATCH]])
            A[:, 2:] = (self.C[:, 1:WATCH] / prev[:, :WATCH - 1] - 1) * 100
            A[:, 1] = 0.0
        else:
            raise KeyError("unknown field %s" % name)
        return A


# ---------------------------------------------------------------------------------------------------- replay
def trigger(book: Book, conds):
    """First watch day whose conditions all hold. Returns (day, status) arrays: day 0 = none.
    status: 'Filled' candidates (day > 0), 'No entry', 'Missing signal data'."""
    n = book.n
    day = np.zeros(n, dtype=np.int64)
    missing = np.zeros(n, dtype=bool)
    done = ~book.ok.copy()
    for k in range(1, WATCH + 1):
        sess = np.isfinite(book.O[:, k])
        newly_missing = ~done & ~sess                       # watch session unavailable
        missing |= newly_missing
        done |= newly_missing
        anyF = np.zeros(n, dtype=bool)
        anyN = np.zeros(n, dtype=bool)
        for fld, op, val in conds:
            a = book.field(fld)[:, k]
            nan = np.isnan(a)
            r = OPS[op](np.round(np.where(nan, 0, a), 9), round(float(val), 9))
            anyF |= ~nan & ~r
            anyN |= nan
        hit = ~done & ~anyF & ~anyN
        miss = ~done & ~anyF & anyN
        day[hit] = k
        missing |= miss
        done |= hit | miss
    status = np.where(~book.ok, "Unsettled",
                      np.where(missing, "Missing signal data", np.where(day > 0, "Filled", "No entry")))
    return day, status


def exits(book: Book, day, status, mode):
    a = exits_arr(book, day, status, mode)
    return pd.DataFrame({"trade_id": book.ids, "signal_day": book.signal_day, "pre_state": book.state,
                         "rank": book.rank, "status": a["st"], "day": a["day"], "price": a["price"], "exit_day": a["exit_day"],
                         "ret": a["ret"], "trade_dd": a["dd"]})


def exits_arr(book: Book, day, status, mode):
    """Vectorised exit: buy at the entry day's open, sell at the exit close; drawdown over entry + closes.
    Returns plain arrays (compact: thousands of setups can be compared without holding their tables)."""
    n = book.n
    st = status.copy()
    f = status == "Filled"
    k = np.where(f, day, 1)
    e = np.where(f, 5 if mode == "original_d5" else day + 4, 1)
    rows = np.arange(n)
    kk, ee = np.clip(k, 1, PATH), np.clip(e, 1, PATH)
    Ok = book.O[rows, kk]
    j = np.arange(1, PATH + 1)[None, :]
    win = (j >= kk[:, None]) & (j <= ee[:, None])
    Cw = book.C[:, 1:]
    bad = (win & ~np.isfinite(Cw)).any(1) | ~np.isfinite(Ok) | (e > PATH)
    ok = f & ~bad
    st[f & bad] = "Missing exit data"
    with np.errstate(invalid="ignore", divide="ignore"):
        peak = np.maximum(np.maximum.accumulate(np.where(win, Cw, -np.inf), axis=1), Ok[:, None])
        ddj = np.where(win, 100 * (1 - Cw / peak), -np.inf).max(1)
        dd = np.where(ok, np.maximum(ddj, 0.0), np.nan)
        ret = np.where(ok, (book.C[rows, ee] / Ok - 1) * 100 - COST, np.nan)
    return {"st": st, "f": ok, "day": np.where(day > 0, day, np.nan).astype(float),
            "price": np.where(ok, Ok, np.nan), "exit_day": np.where(ok, e, 0), "ret": ret, "dd": dd}


def replay2(book, conds):
    """Both exits from one trigger pass, as arrays."""
    d, s = trigger(book, conds)
    return {m: exits_arr(book, d, s, m) for m in EXITS}


def arr_of(df):
    st = df["status"].to_numpy()
    return {"st": st, "f": st == "Filled", "day": df["day"].to_numpy(float), "price": df["price"].to_numpy(float),
            "ret": df["ret"].to_numpy(float), "dd": df["trade_dd"].to_numpy(float)}


def coverage(a, ok):
    st = a["st"][ok]
    return {"eligible": int(ok.sum()), "filled": int((st == "Filled").sum()), "no_entry": int((st == "No entry").sum()),
            "missing": int(np.char.startswith(st.astype(str), "Missing").sum())}


def replay(book, conds, mode):
    d, s = trigger(book, conds)
    return exits(book, d, s, mode)


# ---------------------------------------------------------------------------------------------------- setups
RULES = {"A": [("d_bb_bw_20_change", ">", 0), ("w_ret_13w_change", "<", 0)],
         "B": [("d_ema20_angle_deg_change", "<", 0), ("w_ret_13w_change", "<", 0)],
         "C": [("d_ema20_angle_deg_change", "<", 0), ("d_wq_44_change", ">", 0)]}
CONF = {"none": [], "positive_open_gap": [("gap_pct", ">", 0)],
        "positive_EMA_slope": [("d_ema20_angle_deg", ">", 0)], "declining_minus_DI": [("d_mdi14_diff1", "<", 0)]}


def abc_setups():
    out = {}
    for r in range(1, 4):
        for sub in itertools.combinations("ABC", r):
            for cn, extra in CONF.items():
                conds = list(dict.fromkeys(sum([RULES[x] for x in sub], []) + extra))
                out["+".join(sub) + "__" + cn] = conds
    return out


def control_setups():
    out = {"Blind_D%d" % k: [("day", "<=", k), ("day", ">=", k)] for k in (1, 2, 3)}
    for x in (0, 1, 2, 3, 5):                                    # price-only dip: prior close X% under the D1 open
        out["DIP_%d" % x] = [("pc_vs_d1", "<", -x if x else 0)] if x else [("pc_vs_d1", "<", 0)]
    out["BOUNCE_green"] = [("pc_vs_d1", "<", 0), ("prev_intraday", ">", 0)]      # down from D1, then a green day
    out["BOUNCE_upclose"] = [("pc_vs_d1", "<", 0), ("prev_ret", ">", 0)]         # down from D1, then an up close
    out["BOUNCE_dip2_green"] = [("pc_vs_d1", "<", -2), ("prev_intraday", ">", 0)]
    out["TUE"] = [("weekday", ">=", 1), ("weekday", "<=", 1)]                      # the first Tuesday open
    out["TUE_DIP_2"] = [("weekday", ">=", 1), ("weekday", "<=", 1), ("pc_vs_d1", "<", -2)]
    for x in (0.5, 1.0, 1.5):                                    # the dip in the stock's own ATR units
        out["DIPATR_%g" % x] = [("pc_vs_d1_atr", "<", -x)]
    return out


def labels():
    """The six distinct A/B/C labels (A+B+C has exactly A+C's conditions: A+C implies B)."""
    out = {}
    for r in range(1, 4):
        for sub in itertools.combinations("ABC", r):
            conds = list(dict.fromkeys(sum([RULES[x] for x in sub], [])))
            if frozenset(conds) not in {frozenset(v) for v in out.values()}:
                out["+".join(sub)] = conds
    return out


DIPS = {"DIP_1": [("pc_vs_d1", "<", -1)], "DIP_2": [("pc_vs_d1", "<", -2)], "DIP_3": [("pc_vs_d1", "<", -3)],
        "DIPATR_1": [("pc_vs_d1_atr", "<", -1)]}


def combo_setups(have=lambda c: True):
    """EVERY A/B/C label with each price dip (v0.5, 7 Nov: v0.2-v0.4 paired dips with B and A+B only)."""
    out = {}
    for ln, lc in labels().items():
        if have(lc):
            for dn, dc in DIPS.items():
                out["%s&%s" % (ln, dn)] = lc + dc
    return out


def explore(book, v1, boot, log=print, di=None, d1=None):
    """What adds most on top of a price dip (7 Nov, exploratory, chosen after the first run - a hypothesis search,
    not a test): every single feature condition, the 10 best pairs of the space and B / A+B, each AND a 2% dip
    (and B / A+B AND a 1-ATR dip); each compared on the same trades with the dip alone and with D1."""
    st = {"DIP_2": [("pc_vs_d1", "<", -2)], "DIPATR_1": [("pc_vs_d1_atr", "<", -1)],
          "Blind_D1": [("day", "<=", 1), ("day", ">=", 1)]}
    dip = ("pc_vs_d1", "<", -2)
    for f in book.features:
        for kind in ("", "_change"):
            for op in (">", "<"):
                st["X1|%s%s%s0" % (f, kind, op)] = [(f + kind, op, 0), dip]
    sp = v1[(v1.exit == "original_d5") & v1.setup.str.startswith("S2|")].sort_values("lift_pp", ascending=False)
    space = space_setups(book.features)
    for nm in sp.setup.head(10):
        st["X2|" + nm[3:]] = space[nm] + [dip]
    if all(c[0] in book.F for c in RULES["A"] + RULES["B"]):
        ab = list(dict.fromkeys(RULES["A"] + RULES["B"]))
        st["XA|B&DIPATR_1"] = RULES["B"] + [("pc_vs_d1_atr", "<", -1)]
        st["XA|A+B&DIPATR_1"] = ab + [("pc_vs_d1_atr", "<", -1)]
    di = boot.index(book.signal_day) if di is None else di
    bases = {k: replay2(book, st[k]) for k in ("DIP_2", "DIPATR_1", "Blind_D1")}
    d1 = d1 or bases["Blind_D1"]
    rows, srows = [], []
    fam = {"X1": "feature+dip", "X2": "pair+dip", "XA": "label+dip"}
    for nm in st:
        if not nm.startswith("X"):
            continue
        base = "DIPATR_1" if "DIPATR" in nm else "DIP_2"
        R = replay2(book, st[nm])
        for mode in EXITS:
            r = paired_fast(R[mode], bases[base][mode], boot, di)
            r1 = paired_fast(R[mode], bases["Blind_D1"][mode], boot, di)
            if r and r1:
                rows.append({"setup": nm, "exit": mode, "vs": base, **r, "lift_vs_D1": r1["lift_pp"],
                             "lo_vs_D1": r1["lo"], "hi_vs_D1": r1["hi"]})
            q = stats(R[mode], d1[mode], boot, di, book, bases[base][mode])
            if q:
                srows.append({"family": fam[nm[:2]], "setup": nm, "conds": canon(st[nm]), "twin": base,
                              "twin_conds": canon(st[base]), "exit": mode, **q})
    X = pd.DataFrame(rows)
    log(" exploration: %d setups on top of a dip" % (len(st) - 3))
    return X, srows


# ---------------------------------------------------------------------------------------------------- confluences
# Declared 7 Nov 2026, 10:30 IST, BEFORE any confluence run. Price confluences read the path known at that open;
# context confluences read the pick's snapshot at the signal close (watchlist pre_* columns). Median splits use
# the picks' own snapshot values (no outcomes).
PRICE_CONF = {"DIP1": [("pc_vs_d1", "<", -1)], "DIP2": [("pc_vs_d1", "<", -2)], "DIP3": [("pc_vs_d1", "<", -3)],
              "DIPATR1": [("pc_vs_d1_atr", "<", -1)], "GREEN": [("prev_intraday", ">", 0)],
              "UPCLOSE": [("prev_ret", ">", 0)], "GAPDOWN": [("gap_pct", "<", 0)], "GAPUP": [("gap_pct", ">", 0)]}


def context_conf(book):
    med = lambda c: float(np.nanmedian(pd.to_numeric(book.wl[c], errors="coerce"))) if c in book.wl else np.nan
    out = {"BEARSTATE": [("snap:pre_state_bearish", ">", 0.5)], "BULLSTATE": [("snap:pre_state_bullish", ">", 0.5)],
           "NIFTY_ABOVE_MA50": [("snap:pre_nifty_vs_ma50", ">", 0)],
           "NIFTY_BELOW_MA50": [("snap:pre_nifty_vs_ma50", "<", 0)],
           "MKT_BULLISH": [("snap:pre_env_code", "<=", 1)], "MKT_BEARISH": [("snap:pre_env_code", ">=", 3)],
           "VIX_LOW": [("snap:pre_vix_pct250", "<", med("pre_vix_pct250"))],
           "VIX_HIGH": [("snap:pre_vix_pct250", ">=", med("pre_vix_pct250"))],
           "BREADTH_WEAK": [("snap:pre_ad_ratio_10", "<", med("pre_ad_ratio_10"))],
           "NOT_OVEREXT": [("snap:pre_state_overextended", "<", 0.5)],
           "VOL_ELEVATED": [("snap:pre_state_vol_elevated", ">", 0.5)],
           "TOP3": [("snap:rank", "<=", 3)]}                    # v0.6: the ranks traded today (declared 7 Nov 13:00)
    return {k: v for k, v in out.items() if all(f[5:] in book.wl.columns and np.isfinite(t) for f, _, t in v)
            and not (k == "TOP3" and len(set(book.rank)) < 2)}


def make_pool(book, v1s, pool_n=10):
    """The setups that meet the confluences: NONE (the confluence alone), every A/B/C label, and from EACH engine's
    pair space its top pool_n by lift over D1 and top pool_n by net per trade (n >= 300, interval above 0,
    original_d5) - the union, so every engine tests exactly the same combinations."""
    space = space_setups(book.features)
    pool = {"NONE": []}
    for ln, lc in labels().items():                       # every A/B/C label, equally (v0.5)
        if all(c[0] in book.F for c in lc):
            pool[ln] = lc
    for v1 in v1s:
        sp = v1[(v1.exit == "original_d5") & v1.setup.str.startswith("S2|") & (v1.n >= 300) & (v1.lo > 0)]
        for nm in list(sp.sort_values("lift_pp", ascending=False).setup.head(pool_n)) + \
                list(sp.sort_values("setup_net", ascending=False).setup.head(pool_n)):
            if nm in space and frozenset(space[nm]) not in {frozenset(v) for v in pool.values()}:
                pool.setdefault(nm[3:], space[nm])
    return pool


def confluence(book, v1, boot, out, log=print, pool_n=10, di=None, pool=None):
    """Setups x logical confluences. Pool: make_pool (shared across engines in a multi-engine run). Each setup x
    each confluence (single, or one price x one context), vs D1 and vs the confluence alone on the same trade ids."""
    pool = make_pool(book, [v1], pool_n) if pool is None else pool
    ctx = context_conf(book)
    confs = {**PRICE_CONF, **ctx}
    for a, b in itertools.product(PRICE_CONF, ctx):
        confs[a + "&" + b] = PRICE_CONF[a] + ctx[b]
    st = {"Blind_D1": [("day", "<=", 1), ("day", ">=", 1)]}
    for pn, pc in pool.items():
        for cn, cc in confs.items():
            st["%s || %s" % (pn, cn)] = list(dict.fromkeys(pc + cc))
    log(" confluence: %d setups x %d confluences = %d combinations" % (len(pool), len(confs), len(st) - 1))
    di = boot.index(book.signal_day) if di is None else di
    d1 = replay2(book, st["Blind_D1"])
    alone = {cn: replay2(book, st["NONE || " + cn]) for cn in confs}       # the confluences alone, kept
    # a context filter (the pick's snapshot) only chooses WHICH trades: test it as keeps-vs-drops on its parent
    # (the same setup and price confluence without the filter)
    pick_mask = {}
    for cx, cc in ctx.items():
        msk = np.ones(book.n, bool)
        for f, op, v in cc:
            a = book.field(f)[:, 1]
            msk &= np.isfinite(a) & OPS[op](np.round(np.where(np.isfinite(a), a, 0), 9), round(float(v), 9))
        pick_mask[cx] = msk
    parents = {}

    def parent_of(pn, cn):
        if cn in ctx:
            pc, cx = [], cn
        elif "&" in cn and cn.split("&", 1)[1] in ctx:
            pc, cx = PRICE_CONF[cn.split("&", 1)[0]], cn.split("&", 1)[1]
        else:
            return None, None
        conds = list(dict.fromkeys(pool[pn] + pc)) or D1_CONDS
        k = canon(conds)
        if k not in parents:
            parents[k] = replay2(book, conds)
        return parents[k], cx
    rows, srows = [], []
    t0 = time.time()
    for i, name in enumerate(st):
        if name == "Blind_D1":
            continue
        pn, cn = name.split(" || ")
        R = alone[cn] if pn == "NONE" else replay2(book, st[name])
        for mode in EXITS:
            r = stats(R[mode], d1[mode], boot, di, book, None if pn == "NONE" else alone[cn][mode])
            if not r:
                continue
            par, cx = parent_of(pn, cn)
            if par is not None:
                pa = par[mode]
                keep = pa["f"] & pick_mask[cx]
                drop = pa["f"] & ~pick_mask[cx]
                if keep.sum() > 1 and drop.sum() > 1:
                    lo95, hi95, sd = boot.ci_diff(di[keep], pa["ret"][keep], di[drop], pa["ret"][drop])
                    r.update({"filter_gain": float(pa["ret"][keep].mean() - pa["ret"][drop].mean()),
                              "filter_lo": lo95, "filter_hi": hi95, "filter_sd": sd, "filter_kept": int(keep.sum()),
                              "filter_dropped": int(drop.sum())})
            row = {"setup": pn, "confluence": cn, "exit": mode, **r}
            if "adds" in r:
                row.update({"adds_over_conf": r["adds"]})
            rows.append(row)
            srows.append({"family": "confluence-alone" if pn == "NONE" else "confluence", "setup": name,
                          "conds": canon(st[name]), "twin": "" if pn == "NONE" else "NONE || " + cn,
                          "twin_conds": "" if pn == "NONE" else canon(st["NONE || " + cn]), "exit": mode, **r})
        if (i + 1) % 500 == 0:
            log(" confluence: %d of %d (%.0f s)" % (i + 1, len(st) - 1, time.time() - t0))
    X = pd.DataFrame(rows)
    SR = pd.DataFrame(srows)
    if "filter_gain" in X:
        # every filter test of the run counts: one-sided p from the bootstrap, Benjamini-Hochberg q over all of them
        X["filter_p"] = filter_p(X["filter_gain"], X["filter_sd"])
        X["filter_q"] = bh_q(X["filter_p"])
        SR["filter_p"], SR["filter_q"] = X["filter_p"].to_numpy(), X["filter_q"].to_numpy()
        m = X["filter_p"].notna()
        log(" confluence: %d context-filter tests; %d keep clearly better trades (false discovery rate %.0f%%)" % (
            int(m.sum()), int((X["filter_q"] <= LB_FDR).sum()), 100 * LB_FDR))
    X.to_csv(out / "confluence.csv", index=False)
    L = ["# setuplab - setups x logical confluences (%s) - engine %s, ranks %d-%d, %d picks" % (
        VERSION, book.engine, min(book.rank), max(book.rank), book.n), "",
         "Pool: %s." % ", ".join(pool), "",
         "Confluences (declared before the run): price %s; context %s; and every price x context pair." % (
             ", ".join(PRICE_CONF), ", ".join(ctx)), "",
         "Each row: the combination's own trades vs the model's D1 entry on the same ids; 'adds' = the same "
         "combination vs the confluence ALONE on the same ids (what the indicator setup adds); years = signal years "
         "with net per trade above 0. Net %% after 0.35 pp; 95%% block bootstrap over signal days. Exploratory: "
         "%d combinations on the history the setups came from - expect some to look good by chance." % (len(st) - 1),
         ""]
    for mode in EXITS:
        m = X[(X.exit == mode) & (X.n >= 150)]
        best = m[(m.setup != "NONE") & (m.lo > 0)].sort_values("setup_net", ascending=False).head(25)
        L += ["## %s exit - top 25 combinations by net per trade (n >= 150, lift over D1 interval above 0)" % mode,
              "", "| setup | confluence | n | net | D1 | lift over D1 [95%] | adds over the confluence alone [95%] "
              "| years net > 0 |", "|---|---|---:|---:|---:|---|---|---:|"]
        for _, r in best.iterrows():
            L.append("| %s | %s | %d | %+.4f | %+.4f | %+.4f [%+.4f, %+.4f] | %s | %d/%d |" % (
                r.setup, r.confluence, r.n, r.setup_net, r.control_net, r.lift_pp, r.lo, r.hi,
                ("%+.4f [%+.4f, %+.4f]" % (r.adds_over_conf, r.adds_lo, r.adds_hi)) if pd.notna(
                    r.get("adds_over_conf")) else "-", r.years_net_pos, r.years))
        base = m[m.setup == "NONE"].sort_values("setup_net", ascending=False).head(15)
        L += ["", "### The confluences ALONE (no indicator setup) - top 15 by net per trade (n >= 150)", "",
              "| confluence | n | net | D1 | lift over D1 [95%] | years net > 0 |", "|---|---:|---:|---:|---|---:|"]
        for _, r in base.iterrows():
            L.append("| %s | %d | %+.4f | %+.4f | %+.4f [%+.4f, %+.4f] | %d/%d |" % (
                r.confluence, r.n, r.setup_net, r.control_net, r.lift_pp, r.lo, r.hi, r.years_net_pos, r.years))
        L.append("")
    (out / "CONFLUENCE.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    SR.to_csv(out / "setups_confluence.csv", index=False)
    (out / "confluence.done").write_text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n", encoding="utf-8")
    log(" confluence: wrote CONFLUENCE.md, confluence.csv, setups_confluence.csv")
    return X


def filter_p(gain, sd):
    """One-sided p-value of 'the filter keeps better trades than it drops' (normal approximation, bootstrap sd)."""
    g, s_ = np.asarray(gain, float), np.asarray(sd, float)
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.where(s_ > 0, g / s_, np.nan)
    return np.array([0.5 * math.erfc(v / math.sqrt(2)) if np.isfinite(v) else np.nan for v in z])


def bh_q(p):
    """Benjamini-Hochberg q-values (the false discovery rate at which each test would pass)."""
    p = np.asarray(p, float)
    q = np.full(p.shape, np.nan)
    ok = np.isfinite(p)
    m = int(ok.sum())
    if m:
        o = np.argsort(p[ok])
        r = p[ok][o] * m / np.arange(1, m + 1)
        r = np.minimum(np.minimum.accumulate(r[::-1])[::-1], 1.0)
        qq = np.empty(m)
        qq[o] = r
        q[ok] = qq
    return q


def space_setups(features):
    """Every single-feature change direction and every pair of change directions (the A/B/C family)."""
    out = {}
    for f in features:
        for op in (">", "<"):
            out["S1|%s_change%s0" % (f, op)] = [(f + "_change", op, 0)]
    for f, g in itertools.combinations(features, 2):
        for a, b in itertools.product((">", "<"), repeat=2):
            out["S2|%s_change%s0&%s_change%s0" % (f, a, g, b)] = [(f + "_change", a, 0), (g + "_change", b, 0)]
    return out


# ---------------------------------------------------------------------------------------------------- statistics
class Boot:
    """Circular block bootstrap over signal days, shared index draws so every comparison uses the same resamples."""

    def __init__(self, days, B=2000, block=10, seed=7):
        self.days = np.sort(np.unique(days))
        self.pos = {d: i for i, d in enumerate(self.days)}
        n = len(self.days)
        rng = np.random.default_rng(seed)
        nb = int(np.ceil(n / block))
        st = rng.integers(0, n, size=(B, nb))
        self.ix = ((st[:, :, None] + np.arange(block)[None, None, :]) % n).reshape(B, -1)[:, :n]
        # M[b, d] = how often day d is in resample b: a resample's sum = M @ per-day sums (same draws, faster)
        flat = (np.arange(B)[:, None] * n + self.ix).ravel()
        self.M = np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)

    def ci(self, days, vals):
        return self.ci_idx(np.array([self.pos[d] for d in days]), vals)

    def index(self, days):
        return np.array([self.pos.get(d, -1) for d in days])

    def ci_diff(self, da, va, db, vb):
        """mean(va) - mean(vb), both groups resampled with the same days (dependence kept): the 95% percentile
        interval and the bootstrap standard deviation (for a widened interval)."""
        n = len(self.days)
        X = self.M @ np.column_stack([np.bincount(da, weights=va, minlength=n), np.bincount(da, minlength=n),
                                      np.bincount(db, weights=vb, minlength=n), np.bincount(db, minlength=n)])
        with np.errstate(invalid="ignore", divide="ignore"):
            d = X[:, 0] / np.where(X[:, 1] > 0, X[:, 1], np.nan) - X[:, 2] / np.where(X[:, 3] > 0, X[:, 3], np.nan)
        return float(np.nanpercentile(d, 2.5)), float(np.nanpercentile(d, 97.5)), float(np.nanstd(d))

    def ci_idx(self, di, vals):
        s = np.bincount(di, weights=vals, minlength=len(self.days))
        c = np.bincount(di, minlength=len(self.days)).astype(float)
        S, Cn = self.M @ s, self.M @ c
        m = S / np.where(Cn > 0, Cn, np.nan)
        return float(np.nanpercentile(m, 2.5)), float(np.nanpercentile(m, 97.5))


def paired(a: pd.DataFrame, b: pd.DataFrame, boot: Boot):
    """a's filled trades vs b's on exactly the ids both filled (a = setup, b = control)."""
    A = a[a.status == "Filled"].set_index("trade_id")
    Bf = b[b.status == "Filled"].set_index("trade_id")
    ids = A.index.intersection(Bf.index)
    if len(ids) == 0:
        return None
    x, y = A.loc[ids], Bf.loc[ids]
    lift = x["ret"].to_numpy() - y["ret"].to_numpy()
    lo, hi = boot.ci(x["signal_day"].to_numpy(), lift) if len(ids) > 1 else (np.nan, np.nan)
    disc = (y["price"].to_numpy() / x["price"].to_numpy() - 1) * 100     # % the setup bought under the control
    return {"n": len(ids), "control_net": float(y["ret"].mean()), "setup_net": float(x["ret"].mean()),
            "lift_pp": float(lift.mean()), "lo": lo, "hi": hi, "setup_better_pct": float(100 * (lift > 0).mean()),
            "entry_cheaper_pct": float(np.mean(disc)), "setup_dd": float(x["trade_dd"].mean()),
            "control_dd": float(y["trade_dd"].mean()), "setup_p5": float(np.percentile(x["ret"], 5)),
            "control_p5": float(np.percentile(y["ret"], 5)),
            "mean_entry_day": float(x["day"].mean())}


def paired_fast(a, b, boot, di):
    """paired() on aligned arrays from the same book (same numbers; no tables)."""
    m = a["f"] & b["f"]
    n = int(m.sum())
    if n == 0:
        return None
    x, y = a["ret"][m], b["ret"][m]
    lift = x - y
    lo, hi = boot.ci_idx(di[m], lift) if n > 1 else (np.nan, np.nan)
    disc = (b["price"][m] / a["price"][m] - 1) * 100
    return {"n": n, "control_net": float(np.mean(y)), "setup_net": float(np.mean(x)), "lift_pp": float(lift.mean()),
            "lo": lo, "hi": hi, "setup_better_pct": float(100 * (lift > 0).mean()),
            "entry_cheaper_pct": float(np.mean(disc)), "setup_dd": float(np.mean(a["dd"][m])),
            "control_dd": float(np.mean(b["dd"][m])), "setup_p5": float(np.percentile(x, 5)),
            "control_p5": float(np.percentile(y, 5)), "mean_entry_day": float(np.mean(a["day"][m]))}


def stats(a, base, boot, di, book, twin=None):
    """Everything the comparison and the leaderboard need for one setup and one exit, on aligned arrays:
    the setup's own filled trades vs D1 (base) on the same ids - n, net and its 95% interval, the lift and its
    interval, years with net > 0, the two halves of the period, coverage; and, when the setup has an
    indicator-free twin (the same dip / confluence without the indicator conditions), what the indicators add."""
    m = a["f"] & base["f"]
    n = int(m.sum())
    if n == 0:
        return None
    x, y = a["ret"][m], base["ret"][m]
    lift = x - y
    lo, hi = boot.ci_idx(di[m], lift) if n > 1 else (np.nan, np.nan)
    nlo, nhi = boot.ci_idx(di[m], x) if n > 1 else (np.nan, np.nan)
    disc = (base["price"][m] / a["price"][m] - 1) * 100
    r = {"n": n, "control_net": float(np.mean(y)), "setup_net": float(np.mean(x)), "lift_pp": float(lift.mean()),
         "lo": lo, "hi": hi, "net_lo": nlo, "net_hi": nhi, "setup_better_pct": float(100 * (lift > 0).mean()),
         "entry_cheaper_pct": float(np.mean(disc)), "setup_dd": float(np.mean(a["dd"][m])),
         "control_dd": float(np.mean(base["dd"][m])), "setup_p5": float(np.percentile(x, 5)),
         "control_p5": float(np.percentile(y, 5)), "mean_entry_day": float(np.mean(a["day"][m]))}
    ys = book.yi[m]
    sm, ct = np.bincount(ys, weights=x), np.bincount(ys)
    r["years_net_pos"] = int(((ct > 0) & (sm > 0)).sum())
    r["years"] = int((ct > 0).sum())
    for h in (0, 1):
        hm = book.half[m] == h
        r["half%d_n" % (h + 1)] = int(hm.sum())
        r["half%d_net" % (h + 1)] = float(x[hm].mean()) if hm.any() else np.nan
    r.update(coverage(a, book.ok))
    r["fill_pct"] = 100.0 * r["filled"] / max(1, r["eligible"])
    r["trades_per_year"] = n / book.span_years
    if twin is not None:
        m2 = a["f"] & twin["f"]
        n2 = int(m2.sum())
        if n2:
            d = a["ret"][m2] - twin["ret"][m2]
            alo, ahi = boot.ci_idx(di[m2], d) if n2 > 1 else (np.nan, np.nan)
            r.update({"adds": float(d.mean()), "adds_lo": alo, "adds_hi": ahi, "adds_n": n2,
                      "twin_net": float(np.mean(twin["ret"][m2]))})
    return r


def canon(conds):
    """A setup's identity: its conditions, sorted (the same rule found by two routes counts once)."""
    return json.dumps(sorted([[f, op, float(v)] for f, op, v in dict.fromkeys(conds)]))


def uncanon(text):
    return [(f, op, v) for f, op, v in json.loads(text)]


# ---------------------------------------------------------------------------------------------------- build
def watchlist_rows(picks, bars, cal_days):
    """The watchlist (ChatGPT's format) from each stock's own daily bars.
    picks: rows with trade_id, engine, rank, symbol, signal_day, j (the signal bar's index in the stock's own bars);
    bars: symbol -> (o, c, cal_index of each own bar); cal_days: the session calendar.
    entry = the next own bar's open (D1); close_k = own bar j+k's close / entry - 1; overnight_k (k >= 2) = own bar
    j+k's open / own bar j+k-1's close - 1; missing bars past the data's end are NaN."""
    out = []
    for p in picks:
        o, c, ci = bars[p["symbol"]]
        j = int(p["j"])
        n = len(c)
        if j + 1 >= n:
            continue
        ent, sc = float(o[j + 1]), float(c[j])
        row = {"trade_id": p["trade_id"], "engine": p["engine"], "rank": int(p["rank"]), "symbol": p["symbol"],
               "signal_day": pd.Timestamp(p["signal_day"]), "entry_day": str(pd.Timestamp(cal_days[ci[j + 1]]).date()),
               "signal_close": sc, "entry": ent}
        for k in range(1, PATH + 1):
            row["close_%d" % k] = float(c[j + k]) / ent - 1 if j + k < n else np.nan
            row["overnight_%d" % k] = (0.0 if k == 1 else (float(o[j + k]) / float(c[j + k - 1]) - 1)
                                       if j + k < n else np.nan)
        out.append(row)
    return pd.DataFrame(out)


def check_watchlists(W, ref_path):
    """The built watchlist vs ChatGPT's (ranks 1-3): entry, signal close, the ten closes and gaps."""
    C = pd.read_parquet(ref_path)
    C["trade_id"] = C["trade_id"].astype(str)
    W = W.copy()
    W["trade_id"] = W["trade_id"].astype(str)
    M = W.merge(C, on="trade_id", suffixes=("", "_ref"))
    cols = ["entry", "signal_close"] + ["close_%d" % k for k in range(1, PATH + 1)] + \
           ["overnight_%d" % k for k in range(2, PATH + 1)]
    cols = [c for c in cols if c in M and c + "_ref" in M]
    diff = np.column_stack([(M[c].astype(float) - M[c + "_ref"].astype(float)).abs().to_numpy() for c in cols]) \
        if cols and len(M) else np.zeros((0, 1))
    same = np.all(np.isnan(diff) | (diff < 1e-6), axis=1) if len(M) else np.zeros(0, bool)
    verdict = "MATCHED" if len(M) and same.mean() >= 0.995 else "DIFFERS"
    text = ("check vs %s: %d of its %d picks are in this watchlist, %d identical on entry / closes / gaps (%.2f%%), "
            "largest difference %.2e -> %s" % (Path(ref_path).name, len(M), len(C), int(same.sum()),
                                                100 * same.mean() if len(M) else 0,
                                                np.nanmax(diff) if diff.size and len(M) else np.nan, verdict))
    return {"common": int(len(M)), "reference": int(len(C)), "identical": int(same.sum()), "verdict": verdict,
            "text": text}


def cmd_build(a, log=print):
    """picks (pick_meta, any ranks) + each stock's bars (the daily cache, through playbook's reader = v2engine's
    adapter, READ ONLY) + the context (tradelab's export trades.parquet: status, net_bp, s_atr14, pre_*)."""
    try:
        import playbook as PB
    except ImportError:
        print("REFUSED: playbook is not importable - run  call ...\\playbook\\env_playbook.bat  first")
        return 3
    ex = Path(a.export)
    if not (ex / "trades.parquet").is_file():
        print("REFUSED: no trades.parquet in %s" % ex)
        return 3
    T = pd.read_parquet(ex / "trades.parquet")
    T["trade_id"] = T["trade_id"].astype(str)
    ranks = a.ranks_list or list(range(1, 11))
    engines = [e.strip() for e in a.engines.split(",") if e.strip()]
    d_from = str(pd.to_datetime(T["signal_day"]).min().date())
    d_to = a.to or str(pd.to_datetime(T["signal_day"]).max().date())
    log("%s build: engines %s, ranks %s, signal days %s .. %s" % (VERSION, engines, ranks, d_from, d_to))
    picks, own, data = PB.load(a.root, a.pm_run, engines, ranks, d_from, d_to, log=log,
                               stage_e_any=a.stage_e_any, costs=a.costs)
    cal_days = np.asarray(data.cal.days)
    bars = {s: (ob.o, ob.c, idx) for s, (idx, ob) in own.items()}
    P = [{"trade_id": p.id, "engine": p.engine, "rank": p.rank, "symbol": p.symbol, "signal_day": p.T, "j": p.t_own}
         for p in picks]
    W = watchlist_rows(P, bars, cal_days)
    keep = [c for c in T.columns if c.startswith("pre_") or c in ("status", "net_bp", "s_atr14", "entry", "score",
                                                                    "open6_status", "open6_net_bp")]
    W = W.merge(T[["trade_id"] + keep].rename(columns={"entry": "export_entry"}), on="trade_id", how="left")
    W["status"] = W["status"].fillna("not in the export")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    W.to_parquet(out / "watchlist.parquet", index=False)
    first = W["signal_day"].min() - pd.Timedelta(days=10)
    pd.DataFrame({"date": pd.to_datetime(cal_days[cal_days >= np.datetime64(first)])}).to_parquet(
        out / "calendar.parquet", index=False)
    d = (W["entry"] / W["export_entry"] - 1).abs()
    log(" %d picks (%s); entry vs the export's recorded entry: %d of %d within 1e-6, largest difference %.2e" % (
        len(W), ", ".join("%s %d" % kv for kv in W.groupby("engine").size().items()), int((d < 1e-6).sum()),
        int(d.notna().sum()), float(d.max()) if d.notna().any() else np.nan))
    if a.check:
        res = check_watchlists(W, a.check)
        log(" " + res["text"])
        print("BUILD CHECK " + res["verdict"])
    log(" wrote %s" % out)
    return 0


# ---------------------------------------------------------------------------------------------------- commands
RAW_LEVEL = re.compile(r"^d_(sma|ema)\d+$|^d_atr(14|30)$|^d_cpr_(pivot|bc|tc)$|^d_(support|resistance)\d+$|vpoc|"
                       r"^d_breakout_(high|low)_\d+$|^d_obv$|macd|midpoint_slope|dollar_vol$|_code$|_trend$|"
                       r"^d_dow$|^comb_|prev_inside_day|ema_stack|^label_|(^|_)(open|high|low|close|vwap)$")


def pick_features(why_csv, top, panel, engine="D"):
    """The engine's top features by the WHY surrogate's importance (why_features.csv), skipping raw price levels /
    price-scaled values, categorical codes, the day of week, combined flags and anything not in the panel.
    Returns (chosen, skipped-with-reason)."""
    import pyarrow.parquet as pq
    W = pd.read_csv(why_csv)
    if "engine" in W.columns:
        W = W[W["engine"] == engine]
    W = W.sort_values("importance", ascending=False)
    have = {c.lower() for c in pq.read_schema(panel).names}
    chosen, skipped = [], []
    for f in W["feature"].astype(str):
        if len(chosen) >= top:
            break
        lf = f.lower()
        if RAW_LEVEL.search(lf):
            skipped.append((f, "raw level / code / flag"))
        elif lf not in have:
            skipped.append((f, "not in the panel"))
        else:
            chosen.append(f)
    return chosen, skipped


REQUIRED = ("d_ema20_angle_deg", "w_ret_13w", "d_bb_bw_20", "d_wq_44", "d_mdi14_diff1")   # A/B/C + confirmations


def read_columns_file(path):
    """One feature name per line; '#' starts a comment."""
    out = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            out.append(ln)
    return list(dict.fromkeys(out))


def load(data, features, engine="D", feature_cols=None, ranks=None, log=lambda *a: None, chunk=8, prev=False):
    """engine None = every engine in the watchlist (split later with Book.take). feature_cols: read only these
    columns, a few at a time (the big panel); a missing column is skipped and listed, except the A/B/C ones.
    prev=True (v1.0): feature column 0 = the session before the signal day."""
    wl = pd.read_parquet(Path(data) / "watchlist.parquet")
    cal = pd.read_parquet(Path(data) / "calendar.parquet")["date"]
    if features and feature_cols:
        book = Book(wl, cal, None, engine, None, ranks)
        book.prev_session = bool(prev)
        want, miss = book.attach(features, feature_cols, chunk, log)
        book.missing_features = miss
        need = [c for c in REQUIRED if c in [x.lower() for x in feature_cols] and c not in book.features]
        if need:
            raise ValueError("the A/B/C features are not in the feature file: " + ", ".join(need))
        if not book.features:
            raise ValueError("none of the feature columns is in the feature file")
        return book
    F = pd.read_parquet(features) if features else None
    book = Book(wl, cal, F, engine, feature_cols, ranks)
    book.missing_features = []
    return book


def cmd_reproduce(book, ledgers):
    setups = {**abc_setups(), "Blind_D1": [("day", "<=", 1), ("day", ">=", 1)],
              "Blind_D3": [("day", "<=", 3), ("day", ">=", 3)]}
    worst = 0.0
    bad = []
    n = 0
    for name, conds in setups.items():
        for mode in EXITS:
            fn = Path(ledgers) / (("%s__%s.csv.gz" % (name, mode)) if not name.startswith("Blind")
                                  else ("%s_%s.csv.gz" % (name, mode)))
            if not fn.is_file():
                bad.append((name, mode, "no ledger"))
                continue
            L = pd.read_csv(fn).set_index("trade_id")
            R = replay(book, conds, mode).set_index("trade_id")
            ids = L.index.intersection(R.index)
            st_ok = (L.loc[ids, "status"].astype(str) == R.loc[ids, "status"].astype(str))
            f = ids[(L.loc[ids, "status"] == "Filled").to_numpy()]
            dret = np.abs(L.loc[f, "ret"].to_numpy(float) - R.loc[f, "ret"].to_numpy(float))
            dday = (L.loc[f, "day"].to_numpy(float) != R.loc[f, "day"].to_numpy(float)).sum()
            w = float(np.nanmax(dret)) if len(dret) else 0.0
            worst = max(worst, w)
            n += 1
            if (~st_ok).sum() or dday or w > 1e-6 or len(ids) != len(L):
                bad.append((name, mode, "status %d, day %d, ret %.2e, ids %d/%d" % (int((~st_ok).sum()), int(dday), w,
                                                                                  len(ids), len(L))))
    return n, bad, worst


def run_all(book, setups, boot):
    led = {}
    for name, conds in setups.items():
        for mode in EXITS:
            led[(name, mode)] = replay(book, conds, mode)
    return led


def compare(led, names, controls, boot):
    rows = []
    for name in names:
        for mode in EXITS:
            for ctl in controls:
                if ctl == name:
                    continue
                r = paired(led[(name, mode)], led[(ctl, mode)], boot)
                if r:
                    rows.append({"setup": name, "exit": mode, "control": ctl, **r})
    return pd.DataFrame(rows)


def family_twin(name):
    """The family of a setup of the small set and its indicator-free twin (None when it has none)."""
    if name.startswith("Blind_"):
        return "control", None
    if name in control_setups():
        return "price-only", None
    if "&" in name and name.split("&", 1)[1] in DIPS:
        return "label+dip", name.split("&", 1)[1]
    return ("label", None) if name.endswith("__none") else ("label+confirmation", None)


def stage1(book, out, log=print):
    """Every setup except the confluences: controls, A/B/C labels (+ confirmations, + dips), the pair space, the
    dip exploration. Writes the report files and setups_stage1.csv (one row per setup and exit, for the
    leaderboard). Returns v1, v2, the rows, the bootstrap and the day index."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    have = lambda conds: all(f in book.F or f in PRICE_FIELDS for f, _, _ in conds)
    abc = {k: v for k, v in abc_setups().items() if have(v)}       # A/B/C only when their features are loaded
    ctl = control_setups()
    space = space_setups(book.features)
    combo = combo_setups(have)
    setups = {**ctl, **abc, **combo}
    log("%s: engine %s, %d trades, %d setups (%d A/B/C, %d controls, %d combos, %d feature-space), 2 exits" % (
        VERSION, book.engine, book.n, len(setups) + len(space), len(abc), len(ctl), len(combo), len(space)))
    led = run_all(book, setups, None)
    boot = Boot(book.signal_day[book.ok])
    di = boot.index(book.signal_day)
    arrs = {k: {m: arr_of(led[(k, m)]) for m in EXITS} for k in setups}
    d1 = arrs["Blind_D1"]
    v1rows, srows = [], []

    def add(name, family, conds, R, twin=None):
        for m in EXITS:
            r = stats(R[m], d1[m], boot, di, book, arrs[twin][m] if twin else None)
            if r:
                v1rows.append({"setup": name, "exit": m, "control": "Blind_D1", **r})
                srows.append({"family": family, "setup": name, "conds": canon(conds), "twin": twin or "",
                              "twin_conds": canon(setups[twin]) if twin else "", "exit": m, **r})
    # 1. every setup vs the model's D1 entry on its own trades (the pair space streamed: compared, then dropped)
    for k, c in setups.items():
        fam, tw = family_twin(k)
        add(k, fam, c, arrs[k], tw)
    for i, (name, conds) in enumerate(space.items()):
        add(name, "single" if name.startswith("S1|") else "pair", conds, replay2(book, conds))
        if (i + 1) % 1000 == 0:
            log(" pair space: %d of %d (%.0f s)" % (i + 1, len(space), time.time() - t0))
    v1 = pd.DataFrame(v1rows)
    log(" replayed in %.0f s" % (time.time() - t0))
    # 2. A/B/C and the combos vs the price-only controls on the same trades
    keys = [k for k in abc if k.endswith("__none")] + list(combo)
    v2 = compare(led, keys, [c for c in ctl if c != "Blind_D1"], boot)
    # by signal year: the key setups vs D1 and vs the 2% dip on the same trades
    yrs = []
    key_names = [k + "__none" for k in labels() if k + "__none" in abc] + [k for k in combo if k.endswith("&DIP_2")]
    for name in key_names:
        for mode in EXITS:
            a = led[(name, mode)]
            a = a[a.status == "Filled"].set_index("trade_id")
            for c in ("Blind_D1", "DIP_2"):
                b = led[(c, mode)]
                b = b[b.status == "Filled"].set_index("trade_id")
                ids = a.index.intersection(b.index)
                z = pd.DataFrame({"year": pd.to_datetime(a.loc[ids, "signal_day"]).dt.year,
                                  "setup": a.loc[ids, "ret"], "lift": a.loc[ids, "ret"] - b.loc[ids, "ret"]})
                for y, g in z.groupby("year"):
                    yrs.append({"setup": name, "exit": mode, "control": c, "year": y, "n": len(g),
                                "setup_net": g.setup.mean(), "lift_pp": g.lift.mean()})
    yrs = pd.DataFrame(yrs)
    yrs.to_csv(out / "by_year.csv", index=False)
    sts = by_state(led, key_names + ["DIP_2"], boot)
    sts.to_csv(out / "by_state.csv", index=False)
    rks = None
    if len(set(book.rank)) > 1:
        rks = by_rank(led, key_names + ["DIP_2"], boot)
        rks.to_csv(out / "by_rank.csv", index=False)
    # rank of each setup's lift inside the feature space (same exit)
    sp = v1[v1.setup.str.startswith("S2|")]
    for mode in EXITS:
        ref = np.sort(sp[sp.exit == mode]["lift_pp"].to_numpy())
        m = v1.exit == mode
        v1.loc[m, "pct_of_pair_space"] = [100 * np.searchsorted(ref, x, side="right") / max(1, len(ref))
                                          for x in v1.loc[m, "lift_pp"]]
    X, xrows = explore(book, v1, boot, log, di, d1)
    srows += xrows
    X.to_csv(out / "explore_on_dip.csv", index=False)
    v1.to_csv(out / "vs_D1.csv", index=False)
    v2.to_csv(out / "vs_price_controls.csv", index=False)
    (out / "ledgers").mkdir(exist_ok=True)
    for (name, mode), d in led.items():
        if not name.startswith("S"):
            d.to_csv(out / "ledgers" / ("%s__%s.csv.gz" % (name, mode)), index=False)
    report(v1, v2, out, book, yrs, X, sts, rks)
    S1 = pd.DataFrame(srows)
    S1.to_csv(out / "setups_stage1.csv", index=False)
    (out / "stage1.done").write_text(time.strftime("%Y-%m-%d %H:%M:%S") + "\n", encoding="utf-8")
    log(" stage 1 written (%.0f s)" % (time.time() - t0))
    return v1, v2, S1, boot, di


def cmd_run(book, out, log=print, with_confluence=False):
    """One engine: stage 1 (+ the confluences with its own pool), files in out."""
    t0 = time.time()
    out = Path(out)
    v1, v2, S1, boot, di = stage1(book, out, log)
    if with_confluence:
        confluence(book, v1, boot, out, log, di=di)
    log(" wrote %s (%.0f s)" % (out, time.time() - t0))
    return v1, v2


def cmd_run_multi(books, out, log=print, with_confluence=True):
    """Several engines in one run: stage 1 for each (resumed when its stage1.done exists), ONE confluence pool for
    all (the union of each engine's choice, POOL.json), the confluences for each (resumed likewise), then the
    leaderboard across engines."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    for e, b in books.items():
        d = out / e
        if (d / "stage1.done").is_file() and (d / "vs_D1.csv").is_file():
            log(" %s: stage 1 already done - resumed from %s" % (e, d))
            boot = Boot(b.signal_day[b.ok])
            res[e] = (pd.read_csv(d / "vs_D1.csv"), boot, boot.index(b.signal_day))
        else:
            v1, v2, S1, boot, di = stage1(b, d, log)
            res[e] = (v1, boot, di)
    if with_confluence:
        pf = out / "POOL.json"
        if pf.is_file():
            pool = {k: [tuple(c) for c in v] for k, v in json.loads(pf.read_text(encoding="utf-8")).items()}
            log(" confluence pool: %d setups (from POOL.json)" % len(pool))
        else:
            pool = make_pool(next(iter(books.values())), [r[0] for r in res.values()])
            pf.write_text(json.dumps(pool, indent=1), encoding="utf-8")
            log(" confluence pool: %d setups, the same for every engine (POOL.json)" % len(pool))
        for e, b in books.items():
            d = out / e
            if (d / "confluence.done").is_file():
                log(" %s: confluences already done - resumed" % e)
                continue
            v1, boot, di = res[e]
            confluence(b, v1, boot, d, log, di=di, pool=pool)
    return leaderboard(books, out, log)


# ---------------------------------------------------------------------------------------------------- leaderboard
LB_MIN_N = 300
LB_MIN_YEARS = 6
LB_OVERLAP = 0.70
LB_TOP = 3
LB_FDR = 0.05
FAMILY_ORDER = ("label", "label+dip", "label+confirmation", "price-only", "control", "single", "pair", "feature+dip",
                "pair+dip", "confluence", "confluence-alone")
LB_RULE = [
    "Declared 7 Nov 2026 (13:00 IST) before the final run, applied by the code - nobody picks by eye.",
    "Universe: every setup of the run - controls and price-only rules, the A/B/C labels (with and without "
    "confirmations and dips), every single feature and pair, the dip exploration, every setup x confluence and every "
    "confluence alone - each counted once by its conditions, and only if it was tested in every engine of the run.",
    "ELIGIBLE (for one exit) when in EVERY engine: (1) at least %d trades; (2) the lift over the model's D1 entry on its "
    "own trades has a 95%% interval above 0 (Karan's comparison); (3) when it has an indicator-free twin (the same dip "
    "/ confluence without the indicator conditions), the indicators add with a 95%% interval above 0; (4) trades in at "
    "least %d signal years and net per trade above 0 in all but at most one; (5) net per trade above 0 in both halves "
    "of the period." % (LB_MIN_N, LB_MIN_YEARS),
    "(6) A context filter (a condition on the pick's snapshot at the signal: state, market, NIFTY, VIX, breadth, the "
    "volatility flag, the rank) only chooses WHICH trades to take: it must keep better trades than it drops - the same "
    "setup's trades with the filter minus those without it - and pass after counting EVERY filter test of the run "
    "(thousands: each setup meets every context filter, alone and with each price confluence): a false discovery "
    "rate of at most 5% (Benjamini-Hochberg), in every engine. Otherwise a filter that kept a lucky subset would "
    "float a setup to the top: a filtered setup gets no more chances to pass by luck than a plain one.",
    "SCORE = the lower end of the 95% interval of net per trade (after 0.35 pp) in the worst engine: money per trade, "
    "marked down for small samples and for disagreement between the engines.",
    "Lists: BOTH EXITS (eligible under original_d5 AND fresh; score = the lower of the two) is the main list; each "
    "exit on its own follows.",
    "Top %d = the best scores, skipping VERSIONS of a setup already chosen: a setup whose rule (leaving out the "
    "context filters) contains the other's rule or is contained in it, or whose trades overlap %d%% or more with it "
    "(of the smaller set, first engine). Different setups, not versions of one." % (LB_TOP, int(LB_OVERLAP * 100)),
]
D1_CONDS = [("day", "<=", 1), ("day", ">=", 1)]


def lb_table(out, engines):
    """One row per setup (by its conditions) and exit, with every engine's numbers side by side (engine:field)."""
    per = {}
    for e in engines:
        parts = [pd.read_csv(Path(out) / e / f) for f in ("setups_stage1.csv", "setups_confluence.csv")
                 if (Path(out) / e / f).is_file()]
        T = pd.concat(parts, ignore_index=True)
        for c in ("twin", "twin_conds"):
            T[c] = T[c].fillna("").astype(str)
        T["_fam"] = T["family"].map({f: i for i, f in enumerate(FAMILY_ORDER)}).fillna(99)
        per[e] = T.sort_values("_fam", kind="stable").drop_duplicates(["conds", "exit"], keep="first")
    keys, meta = ["conds", "exit"], ["family", "setup", "twin", "twin_conds", "_fam"]
    W = per[engines[0]][keys + meta[:-1]].copy()
    for e in engines:
        T = per[e].set_index(keys)
        W = W.join(T[[c for c in T.columns if c not in meta]].add_prefix(e + ":"), on=keys, how="inner")
    return W.reset_index(drop=True)


def rank_rows(W, engines, min_n=LB_MIN_N, min_years=LB_MIN_YEARS):
    """The declared eligibility (with the reasons a setup fails) and the score."""
    W = W.copy()
    twin = W["twin_conds"].fillna("").astype(str).to_numpy() != ""
    filt = W["conds"].astype(str).str.contains('"snap:', regex=False).to_numpy()
    ok = np.ones(len(W), bool)
    why = [[] for _ in range(len(W))]

    def flag(bad, text):
        bad = np.asarray(bad, bool)
        ok[bad] = False
        for i in np.flatnonzero(bad):
            why[i].append(text)
    for e in engines:
        g = lambda c: pd.to_numeric(W["%s:%s" % (e, c)], errors="coerce").to_numpy(float) if \
            "%s:%s" % (e, c) in W else np.full(len(W), np.nan)
        flag(~(g("n") >= min_n), "%s: fewer than %d trades" % (e, min_n))
        flag(~(g("lo") > 0), "%s: lift over D1 not clearly above 0" % e)
        flag(twin & ~(g("adds_lo") > 0), "%s: the indicators add nothing clear over the same entry without them" % e)
        flag(~(g("years") >= min_years), "%s: trades in fewer than %d years" % (e, min_years))
        flag(~(g("years_net_pos") >= g("years") - 1), "%s: net <= 0 in more than one year" % e)
        flag(~((g("half1_net") > 0) & (g("half2_net") > 0)), "%s: net <= 0 in one half of the period" % e)
        flag(filt & ~(g("filter_q") <= LB_FDR), "%s: the context filter does not clearly keep better trades" % e)
    W["eligible"] = ok
    W["why_not"] = ["; ".join(x) for x in why]
    W["score"] = np.nanmin(np.vstack([pd.to_numeric(W["%s:net_lo" % e], errors="coerce") for e in engines]), axis=0)
    W["min_net"] = np.nanmin(np.vstack([pd.to_numeric(W["%s:setup_net" % e], errors="coerce") for e in engines]),
                             axis=0)
    return W


def both_exits(R):
    """Main list: eligible under both exits; score = the lower of the two."""
    o = R[R.exit == "original_d5"].set_index("conds")
    f = R[R.exit == "fresh"].set_index("conds")
    j = o[["setup", "family", "twin_conds", "eligible", "score", "why_not"]].join(
        f[["eligible", "score", "why_not"]], rsuffix="_fresh", how="inner")
    j["eligible_both"] = j["eligible"] & j["eligible_fresh"]
    j["score_both"] = np.minimum(j["score"], j["score_fresh"])
    return j.reset_index()


def overlap(a, b):
    return len(a & b) / max(1, min(len(a), len(b)))


def core(key):
    """A setup's rule without its context filters (the conditions that decide the entry)."""
    try:
        return frozenset(tuple(c) for c in json.loads(key) if not str(c[0]).startswith("snap:"))
    except (TypeError, ValueError):
        return frozenset([key])


def is_version(a, b, ids, thr=LB_OVERLAP):
    ca, cb = core(a), core(b)
    return ca <= cb or cb <= ca or overlap(ids(a), ids(b)) >= thr


def versions_skipped(chosen, order, ids, limit=200, k=5):
    """For each chosen setup, the best-placed setups (of the first `limit`) skipped as its versions."""
    out = {c: [] for c in chosen}
    for key in order[:limit]:
        if key in out:
            continue
        for c in chosen:
            if is_version(key, c, ids):
                if len(out[c]) < k:
                    out[c].append(key)
                break
    return out


def pick_diverse(order, ids, thr=LB_OVERLAP, k=LB_TOP):
    """Walk down the ranking; keep a setup unless it is a version of one already kept."""
    chosen = []
    for key in order:
        if ids(key) and not any(is_version(key, c, ids, thr) for c in chosen):
            chosen.append(key)
        if len(chosen) == k:
            break
    return chosen


WORDS = {"pre_state_bearish": "a bearish state at the pick (S08/S09)",
         "pre_state_bullish": "a bullish state at the pick (S01-S03)",
         "pre_state_overextended": "overextended at the pick", "pre_state_vol_elevated": "volatility elevated at the pick",
         "pre_nifty_vs_ma50": "NIFTY vs its 50-day average at the pick", "pre_env_code": "the market environment code",
         "pre_vix_pct250": "VIX's 250-day percentile at the pick", "pre_ad_ratio_10": "10-day breadth at the pick",
         "rank": "the model's rank"}


def describe(conds):
    """The conditions in words (an A/B/C label is named when all its conditions are there)."""
    conds = list(dict.fromkeys(conds))
    out, used = [], set()
    labs = sorted(labels().items(), key=lambda kv: -len(kv[1]))
    for ln, lc in labs:
        if set(lc) <= set(conds) and not set(lc) <= used:
            out.append("%s (%s)" % (ln, " and ".join(describe_one(c) for c in lc)))
            used |= set(lc)
            break
    for c in conds:
        if c not in used:
            out.append(describe_one(c))
    return "; ".join(out)


def describe_one(c):
    f, op, v = c
    v = float(v)
    if f == "pc_vs_d1":
        return "yesterday's close below the D1 open" if v == 0 else "yesterday's close more than %g%% below the D1 " \
            "open" % -v
    if f == "pc_vs_d1_atr":
        return "yesterday's close more than %g ATR below the D1 open" % -v
    if f == "gap_pct":
        return "opens below yesterday's close (gap down)" if op == "<" else "opens above yesterday's close (gap up)"
    if f == "prev_intraday":
        return "yesterday closed above its open"
    if f == "prev_ret":
        return "yesterday closed up"
    if f == "day":
        return "watch day %s %g" % (op, v)
    if f == "weekday":
        return "weekday %s %g (1 = Tuesday)" % (op, v)
    if f.startswith("snap:"):
        k = f[5:]
        if k in ("pre_state_bearish", "pre_state_bullish", "pre_state_vol_elevated"):
            return WORDS[k]
        if k == "pre_state_overextended":
            return "not overextended at the pick"
        if k == "rank":
            return "the model's rank %s %g" % (op, v)
        return "%s %s %.4g" % (WORDS.get(k, k), op, v)
    if f.endswith("_change"):
        return "%s %s on the previous session" % (f[:-7], "rose" if op == ">" else "fell")
    return "%s %s %g on the previous session" % (f, "above" if op == ">" else "below", v)


def _sub(a, mask):
    b = dict(a)
    b["f"] = a["f"] & mask
    return b


def positions(b, a):
    """Open positions per market session (entry open to exit close): the average over the sessions from the first
    entry to the last exit, the maximum, and the most entries on one session."""
    k = np.flatnonzero(a["f"])
    if not len(k):
        return {}
    s = b.i1[k] + a["day"][k].astype(int) - 1
    x = b.i1[k] + a["exit_day"][k].astype(int) - 1
    lo = int(s.min())
    d = np.zeros(int(x.max()) - lo + 2)
    np.add.at(d, s - lo, 1)
    np.add.at(d, x - lo + 1, -1)
    op = np.cumsum(d)[:-1]
    return {"pos_avg": float(op.mean()), "pos_max": int(op.max()), "entries_max_day": int(np.bincount(s - lo).max())}


def finalist_ledger(b, R, D):
    """Every trade of a chosen setup (both exits) next to the model's D1 entry on the same trade. Dates are market
    sessions counted from D1 (a stock that skipped a session in its watch window is off by the skipped days)."""
    cal = pd.DatetimeIndex(b.cal)
    parts = []
    for m in EXITS:
        a, d = R[m], D[m]
        k = np.flatnonzero(a["f"])
        ed, xd = a["day"][k].astype(int), a["exit_day"][k].astype(int)
        dd = lambda off: cal[np.clip(b.i1[k] + off - 1, 0, len(cal) - 1)].strftime("%Y-%m-%d")
        parts.append(pd.DataFrame({
            "exit_mode": m, "trade_id": b.ids[k], "engine": b.engine_arr[k], "symbol": b.symbols[k], "rank": b.rank[k],
            "pre_state": b.state[k], "signal_day": pd.DatetimeIndex(b.signal_day[k]).strftime("%Y-%m-%d"),
            "d1_date": dd(1), "entry_watch_day": ed, "entry_date": dd(ed), "entry_price": a["price"][k],
            "exit_date": dd(xd), "exit_price": b.C[k, xd], "net_pct": a["ret"][k], "trade_dd_pct": a["dd"][k],
            "d1_entry_price": d["price"][k], "d1_net_pct": np.where(d["f"][k], d["ret"][k], np.nan),
            "lift_pp": np.where(d["f"][k], a["ret"][k] - d["ret"][k], np.nan)}))
    return pd.concat(parts, ignore_index=True)


def finalist(books, conds, twin_conds, cache):
    """A chosen setup in every engine and exit: all trades, rank bands, bearish vs other states, each year."""
    out = {}
    for e, b in books.items():
        if e not in cache:
            boot = Boot(b.signal_day[b.ok])
            cache[e] = (boot, boot.index(b.signal_day), replay2(b, D1_CONDS))
        boot, di, D = cache[e]
        R = replay2(b, conds)
        T = replay2(b, twin_conds) if twin_conds else None
        years = pd.DatetimeIndex(b.signal_day).year.to_numpy()
        bear = np.isin(b.state, ["S08", "S09"])
        out[(e, "ledger")] = finalist_ledger(b, R, D)
        for m in EXITS:
            groups = {"ranks 1-3": b.rank <= 3, "ranks 4-10": b.rank > 3, "bearish state": bear, "other states": ~bear}
            out[(e, m)] = {"all": stats(R[m], D[m], boot, di, b, T[m] if T else None), "positions": positions(b, R[m]),
                           "groups": {g: stats(_sub(R[m], k), D[m], boot, di, b) for g, k in groups.items()},
                           "years": {int(y): stats(_sub(R[m], years == y), D[m], boot, di, b)
                                     for y in sorted(set(years))}}
    return out


def _f(x, nd=4):
    return "-" if x is None or not np.isfinite(x) else ("%+." + str(nd) + "f") % x


def leaderboard(books, out, log=print):
    """The declared rule over every setup of the run, across the engines. Writes LEADERBOARD.md,
    leaderboard.csv and FREEZE_CANDIDATES.json."""
    out = Path(out)
    engines = list(books)
    R = rank_rows(lb_table(out, engines), engines)
    B = both_exits(R)
    first = books[engines[0]]
    ids_cache = {}

    def ids(conds):
        if conds not in ids_cache:
            a = replay2(first, uncanon(conds))["original_d5"]
            ids_cache[conds] = set(first.ids[a["f"]])
        return ids_cache[conds]
    lists = {}
    elig_b = B[B.eligible_both].sort_values(["score_both", "score"], ascending=False)
    lists["both exits"] = (elig_b, pick_diverse(list(elig_b.conds), ids), "score_both")
    for m in EXITS:
        el = R[(R.exit == m) & R.eligible].sort_values(["score", "min_net"], ascending=False)
        lists[m] = (el, pick_diverse(list(el.conds), ids), "score")
    cache = {}
    (out / "FINALISTS").mkdir(exist_ok=True)

    def row(conds, m):
        x = R[(R.conds == conds) & (R.exit == m)]
        return x.iloc[0] if len(x) else pd.Series(dtype=object)
    L = ["# setuplab leaderboard - the declared rule over every setup (%s)" % VERSION, "",
         "Engines %s; %s. %d setups x 2 exits tested in every engine; eligible: both exits %d, original_d5 %d, "
         "fresh %d." % (", ".join(engines), ", ".join("%s %d picks" % (e, books[e].n) for e in engines),
                        R.conds.nunique(), int(B.eligible_both.sum()), int(R[(R.exit == "original_d5")].eligible.sum()),
                        int(R[(R.exit == "fresh")].eligible.sum())), "", "## The rule", ""] + \
        ["- " + t for t in LB_RULE] + [""]
    freeze = {"version": VERSION, "rule": LB_RULE, "engines": engines, "lists": {}}
    for lname, (el, chosen, sc) in lists.items():
        order = list(el.conds)
        skipped = versions_skipped(chosen, order, ids)
        eli = el.drop_duplicates("conds").set_index("conds")
        L += ["## %s - the top %d" % (lname.upper() if lname == "both exits" else lname + " exit", LB_TOP), ""]
        if not chosen:
            L += ["No setup meets the rule.", ""]
        freeze["lists"][lname] = []
        for rk, conds in enumerate(chosen, 1):
            r0 = row(conds, "original_d5")
            r0 = r0 if len(r0) else row(conds, "fresh")
            det = finalist(books, uncanon(conds), uncanon(r0.twin_conds) if r0.twin_conds else None, cache)
            title = "### %d. %s  (%s)" % (rk, r0.setup, r0.family)
            L += [title, "", "**Rule:** %s. Watch D1-D5 after the pick, buy at the first open where all hold; "
                  "exit original_d5 = the pick's D5 close, fresh = the close 4 sessions after entry; 0.35 pp costs." %
                  describe(uncanon(conds)), "",
                  "| engine | exit | trades | per year | fill % | net | net 95% | D1 same trades | lift over D1 [95%] "
                  "| indicators add [95%] | years net > 0 | 1st / 2nd half | open positions avg / max (entries one day) |",
                  "|---|---|---:|---:|---:|---:|---|---:|---|---|---:|---|---|"]
            item = {"rank": rk, "setup": r0.setup, "family": r0.family, "conds": uncanon(conds),
                    "description": describe(uncanon(conds)), "twin_conds": uncanon(r0.twin_conds) if
                    r0.twin_conds else None, "stats": {}}
            for e in engines:
                for m in EXITS:
                    a = det[(e, m)]["all"]
                    if not a:
                        continue
                    item["stats"]["%s %s" % (e, m)] = {k: (float(v) if isinstance(v, (int, float, np.floating,
                                                                                       np.integer)) else v)
                                                       for k, v in a.items()}
                    po = det[(e, m)]["positions"]
                    item["stats"]["%s %s" % (e, m)].update(po)
                    L.append("| %s | %s | %d | %.0f | %.1f | %s | %s .. %s | %s | %s [%s, %s] | %s | %d/%d | %s / %s | %s |" % (
                        e, m, a["n"], a["trades_per_year"], a["fill_pct"], _f(a["setup_net"]), _f(a["net_lo"]),
                        _f(a["net_hi"]), _f(a["control_net"]), _f(a["lift_pp"]), _f(a["lo"]), _f(a["hi"]),
                        ("%s [%s, %s]" % (_f(a["adds"]), _f(a["adds_lo"]), _f(a["adds_hi"]))) if "adds" in a else "-",
                        a["years_net_pos"], a["years"], _f(a["half1_net"], 2), _f(a["half2_net"], 2),
                        ("%.1f / %d (%d)" % (po["pos_avg"], po["pos_max"], po["entries_max_day"])) if po else "-"))
            if any(str(c[0]).startswith("snap:") for c in uncanon(conds)):
                fx = []
                for e in engines:
                    for m in EXITS:
                        q = row(conds, m)
                        g = lambda c: float(pd.to_numeric(pd.Series([q.get("%s:%s" % (e, c))]), errors="coerce").iloc[0])
                        fx.append("%s %s %s [%s, %s], q %s (kept %s, dropped %s)" % (
                            e, m, _f(g("filter_gain")), _f(g("filter_lo")), _f(g("filter_hi")),
                            "-" if not np.isfinite(g("filter_q")) else "%.4f" % g("filter_q"),
                            "-" if not np.isfinite(g("filter_kept")) else "%d" % g("filter_kept"),
                            "-" if not np.isfinite(g("filter_dropped")) else "%d" % g("filter_dropped")))
                        item.setdefault("filter", {})["%s %s" % (e, m)] = {
                            k: float(g(k)) for k in ("filter_gain", "filter_lo", "filter_hi", "filter_p", "filter_q",
                                                     "filter_kept", "filter_dropped")}
                L += ["", "**Context filter (rule 6)** - the parent setup's trades WITH the filter minus those "
                      "WITHOUT it, net per trade [95%%], q = the false discovery rate over all the run's filter tests "
                      "(passes at <= %.2f): " % LB_FDR + "; ".join(fx) + "."]
            if skipped.get(conds):
                L += ["", "**Versions skipped** (eligible, but the same rule with conditions or context filters added "
                      "or removed, or 70%%+ the same trades): %s." % "; ".join(
                          "%s (place %d, score %s)" % (eli.loc[v, "setup"], order.index(v) + 1, _f(eli.loc[v, sc]))
                          for v in skipped[conds])]
                item["versions_skipped"] = [eli.loc[v, "setup"] for v in skipped[conds]]
            slug = "%s_%d" % (lname.replace(" ", "_"), rk)
            for e in engines:
                det[(e, "ledger")].to_csv(out / "FINALISTS" / ("%s__%s.csv" % (slug, e)), index=False)
            item["ledgers"] = ["FINALISTS/%s__%s.csv" % (slug, e) for e in engines]
            L += ["", "Every trade (both exits, with the D1 entry on the same trade): %s." % ", ".join(
                "`%s`" % x for x in item["ledgers"])]
            L += ["", "| engine | exit | ranks 1-3 | ranks 4-10 | bearish state | other states | by year (net, trades) |",
                  "|---|---|---|---|---|---|---|"]
            for e in engines:
                for m in EXITS:
                    g = det[(e, m)]["groups"]
                    cell = lambda x: "-" if not x else "%s (%d)" % (_f(x["setup_net"], 2), x["n"])
                    yy = ", ".join("%d %s (%d)" % (y, _f(v["setup_net"], 2), v["n"]) for y, v in
                                   det[(e, m)]["years"].items() if v)
                    L.append("| %s | %s | %s | %s | %s | %s | %s |" % (e, m, cell(g["ranks 1-3"]), cell(g["ranks 4-10"]),
                                                                       cell(g["bearish state"]),
                                                                       cell(g["other states"]), yy))
            L.append("")
            freeze["lists"][lname].append(item)
        # the table of the leading eligible setups (no overlap rule)
        L += ["#### The 20 best eligible scores, %s (before the overlap rule)" % lname, "",
              "| # | setup | family | score | %s |" % " | ".join("%s net (%s)" % (e, "orig / fresh" if lname ==
                                                                                "both exits" else lname)
                                                                for e in engines), "|---:|---|---|---:|" +
              "---:|" * len(engines)]
        for i, (_, r) in enumerate(el.head(20).iterrows(), 1):
            nets = []
            for e in engines:
                if lname == "both exits":
                    o, f = row(r.conds, "original_d5"), row(r.conds, "fresh")
                    nets.append("%s / %s" % (_f(o["%s:setup_net" % e], 2), _f(f["%s:setup_net" % e], 2)))
                else:
                    nets.append(_f(r["%s:setup_net" % e], 2))
            L.append("| %d | %s%s | %s | %s | %s |" % (i, r.setup, " *" if r.conds in chosen else "", r.family,
                                                        _f(r[sc], 4), " | ".join(nets)))
        L.append("")
    # where the setups discussed so far stand
    refs = {"A": labels()["A"], "B": labels()["B"], "C": labels()["C"], "A+B": labels()["A+B"],
            "A+C (= A+B+C)": labels()["A+C"], "B+C": labels()["B+C"]}
    for ln in ("A", "B", "C", "A+B", "A+C", "B+C"):
        refs["%s & 2%% dip" % ln] = labels()[ln] + DIPS["DIP_2"]
    refs["2% dip alone"] = DIPS["DIP_2"]
    refs["WQ_44 up & 13w down + gap down + vol elevated"] = [("d_wq_44_change", ">", 0), ("w_ret_13w_change", "<", 0),
                                                            ("gap_pct", "<", 0), ("snap:pre_state_vol_elevated", ">", 0.5)]
    refs["B + 1-ATR dip + bearish"] = labels()["B"] + DIPS["DIPATR_1"] + [("snap:pre_state_bearish", ">", 0.5)]
    refs["B + 3% dip + bearish"] = labels()["B"] + DIPS["DIP_3"] + [("snap:pre_state_bearish", ">", 0.5)]
    L += ["## Where the setups discussed so far stand", "",
          "| setup | both exits: eligible / score / place | why not (first reasons) |", "|---|---|---|"]
    order_b = list(elig_b.conds)
    for name, c in refs.items():
        k = canon(c)
        r = B[B.conds == k]
        if r.empty:
            L.append("| %s | not tested in every engine | - |" % name)
            continue
        r = r.iloc[0]
        place = (order_b.index(k) + 1) if k in order_b else None
        why = "; ".join(dict.fromkeys(y for x in (r.why_not, r.why_not_fresh) if isinstance(x, str) and x
                                      for y in x.split("; ")))[:300]
        L.append("| %s | %s / %s / %s | %s |" % (name, "yes" if r.eligible_both else "no", _f(r.score_both),
                                                 place or "-", why or "-"))
    L += ["", "Families (eligible both exits / tested): " + ", ".join(
        "%s %d/%d" % (f, int(g.eligible_both.sum()), len(g)) for f, g in B.groupby("family")), "",
          "Read with care: this ranks thousands of rules on the history they were found on; the winners' numbers "
          "will shrink going forward. The forward paper ledger is the test."]
    (out / "LEADERBOARD.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    R.to_csv(out / "leaderboard.csv", index=False)
    B.to_csv(out / "leaderboard_both_exits.csv", index=False)
    (out / "FREEZE_CANDIDATES.json").write_text(json.dumps(freeze, indent=1, default=str), encoding="utf-8")
    log(" leaderboard: %d eligible in both exits; wrote LEADERBOARD.md, FREEZE_CANDIDATES.json" %
        int(B.eligible_both.sum()))
    return R, B


def by_group(led, names, boot, key, label):
    """Like by_state, for any grouping of the trades (key: ledger -> group labels)."""
    rows = []
    for name in names:
        for mode in EXITS:
            a = led[(name, mode)]
            ga = key(a)
            for ctl in ("Blind_D1", "DIP_2"):
                if ctl == name:
                    continue
                b = led[(ctl, mode)]
                gb = key(b)
                for g in sorted(pd.unique(ga)):
                    r = paired(a[ga == g], b[gb == g], boot)
                    if r:
                        rows.append({"setup": name, "exit": mode, "control": ctl, label: g, **r})
    return pd.DataFrame(rows)


def by_rank(led, names, boot):
    one = by_group(led, names, boot, lambda d: d["rank"].map(lambda r: "rank %02d" % r).to_numpy(), "group")
    band = by_group(led, names, boot, lambda d: np.where(d["rank"].to_numpy() <= 3, "ranks 1-3", "ranks 4-10"),
                    "group")
    return pd.concat([band, one], ignore_index=True)


def by_state(led, names, boot):
    """Each setup's own trades vs D1 (and vs the 2% dip) on the same ids, split by the pick's stock state at the
    signal (pre_state from the watchlist: nomination context, not the state on the entry day)."""
    rows = []
    for name in names:
        for mode in EXITS:
            a = led[(name, mode)]
            for ctl in ("Blind_D1", "DIP_2"):
                if ctl == name:
                    continue
                b = led[(ctl, mode)]
                for st in sorted(a.pre_state.astype(str).unique()):
                    r = paired(a[a.pre_state.astype(str) == st], b[b.pre_state.astype(str) == st], boot)
                    if r:
                        rows.append({"setup": name, "exit": mode, "control": ctl, "state": st, **r})
    return pd.DataFrame(rows)


def _fmt(r):
    return "%d | %+.4f | %+.4f | **%+.4f** | %+.4f .. %+.4f | %.1f | %.4f" % (
        r["n"], r["control_net"], r["setup_net"], r["lift_pp"], r["lo"], r["hi"], r["setup_better_pct"],
        r["entry_cheaper_pct"])


def report(v1, v2, out, book, yrs=None, X=None, sts=None, rks=None):
    L = ["# setuplab - setups vs the model's D1 entry on the same trades (%s)" % VERSION, "",
         "Engine %s, ranks %s, %d picks, %d settled. Net %% per trade after 0.35 pp. Each row: the setup's OWN filled trades "
         "against the model buying the same trade ids at the D1 open (same exit rule). 95%% circular block bootstrap "
         "over signal days (10-day blocks, 2,000 draws). 'Cheaper' = how far under the control's entry the setup "
         "bought, on average." % (book.engine, "%d-%d" % (min(book.rank), max(book.rank)) if book.n else "-",
                                   book.n, int(book.ok.sum())), ""]
    hdr = "| setup | n | D1 net | setup net | lift pp | 95% interval | setup better % | entry cheaper % |"
    sep = "|---|---:|---:|---:|---:|---|---:|---:|"
    for mode in EXITS:
        L += ["## %s exit" % mode, "", "### A/B/C and the price-only controls", "", hdr, sep]
        sub = v1[(v1.exit == mode) & ~v1.setup.str.startswith("S")]
        for _, r in sub.sort_values("lift_pp", ascending=False).iterrows():
            L.append("| %s | %s |" % (r["setup"], _fmt(r)))
        sp = v1[(v1.exit == mode) & v1.setup.str.startswith("S2|")].sort_values("lift_pp", ascending=False)
        L += ["", "### The whole pair space of the %d features (%d setups; A/B/C's family) - top 15 and bottom 5" %
              (len(book.features), len(sp)), "", hdr, sep]
        for _, r in pd.concat([sp.head(15), sp.tail(5)]).iterrows():
            L.append("| %s | %s |" % (r["setup"][3:], _fmt(r)))
        L += ["", "Pair space: lift above 0 with the interval above 0 in %d of %d setups; median lift %+.4f pp." % (
            int((sp.lo > 0).sum()), len(sp), sp.lift_pp.median()), ""]
        own = sp[(sp.n >= 300) & (sp.lo > 0)].sort_values("setup_net", ascending=False).head(15)
        L += ["### Pair space - top 15 by net per trade (n >= 300, lift interval above 0)", "", hdr, sep]
        for _, r in own.iterrows():
            L.append("| %s | %s |" % (r["setup"][3:], _fmt(r)))
        L.append("")
        L += ["### A/B/C against the price-only controls (same trade ids, both filled)", "",
              "| setup | control | n | control net | setup net | lift pp | 95% interval | setup better % | entry cheaper % |",
              "|---|---|---:|---:|---:|---:|---|---:|---:|"]
        for _, r in (v2[v2.exit == mode] if len(v2) else v2).iterrows():
            L.append("| %s | %s | %s |" % (r["setup"], r["control"], _fmt(r)))
        L.append("")
        if yrs is not None and len(yrs):
            L += ["### By signal year (lift pp on the same trades; setup net in brackets)", ""]
            ys = sorted(yrs.year.unique())
            L += ["| setup | vs | " + " | ".join(str(y) for y in ys) + " |", "|---|---|" + "---:|" * len(ys)]
            for (nm, c), g in yrs[yrs.exit == mode].groupby(["setup", "control"], sort=False):
                g = g.set_index("year")
                L.append("| %s | %s | " % (nm, c) + " | ".join(
                    ("%+.2f (%+.2f, n %d)" % (g.loc[y, "lift_pp"], g.loc[y, "setup_net"], g.loc[y, "n"]))
                    if y in g.index else "-" for y in ys) + " |")
            L.append("")
    labs = [ln for ln in labels() if ln + "__none" in set(v1.setup)]
    if labs:
        L += ["## Every A/B/C label, treated the same (A+B+C = A+C: identical conditions)", "",
              "Net % per trade on the label's own trades (original_d5 / fresh), its lift over D1 on those trades "
              "[95%], and what the label adds over the same dip ALONE on the same trades [95%].", ""]
        for mode in EXITS:
            L += ["### %s exit" % mode, "", "| label | entry | n | net | lift over D1 [95%] | adds over the dip alone [95%] |",
                  "|---|---|---:|---:|---|---|"]
            for ln in labs:
                for dn in [None] + list(DIPS):
                    nm = ln + "__none" if dn is None else "%s&%s" % (ln, dn)
                    r = v1[(v1.setup == nm) & (v1.exit == mode)]
                    if r.empty:
                        continue
                    r = r.iloc[0]
                    a = v2[(v2.setup == nm) & (v2.exit == mode) & (v2.control == dn)] if dn and len(v2) else []
                    adds = ("%+.4f [%+.4f, %+.4f]" % (a.lift_pp.iloc[0], a.lo.iloc[0], a.hi.iloc[0])) if len(a) else "-"
                    L.append("| %s | %s | %d | %+.4f | %+.4f [%+.4f, %+.4f] | %s |" % (
                        ln, dn or "no dip", r.n, r.setup_net, r.lift_pp, r.lo, r.hi, adds))
            L.append("")
    if rks is not None and len(rks):
        L += ["## By rank (the model's rank on the signal day)", "",
              "Each cell: lift over D1 on the setup's own trades [95% interval] / net per trade / trades.", ""]
        for mode in EXITS:
            sub = rks[(rks.exit == mode) & (rks.control == "Blind_D1")]
            names = list(dict.fromkeys(sub.setup))
            L += ["### %s exit" % mode, "", "| group | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
            for g in list(dict.fromkeys(sub.group)):
                cells = []
                for nm in names:
                    r = sub[(sub.setup == nm) & (sub.group == g)]
                    cells.append("-" if r.empty else "%+.2f [%+.2f, %+.2f] / %+.2f / %d" % (
                        r.lift_pp.iloc[0], r.lo.iloc[0], r.hi.iloc[0], r.setup_net.iloc[0], r.n.iloc[0]))
                L.append("| %s | " % g + " | ".join(cells) + " |")
            L.append("")
    if sts is not None and len(sts):
        L += ["## By stock state at the signal (pre_state; nomination context)", "",
              "Each cell: lift over D1 on the setup's own trades [95% interval] / the setup's net per trade / trades. "
              "States with under 30 trades are noisy.", ""]
        for mode in EXITS:
            sub = sts[(sts.exit == mode) & (sts.control == "Blind_D1")]
            names = list(dict.fromkeys(sub.setup))
            L += ["### %s exit" % mode, "", "| state | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
            for st in sorted(sub.state.unique()):
                cells = []
                for nm in names:
                    r = sub[(sub.setup == nm) & (sub.state == st)]
                    cells.append("-" if r.empty else "%+.2f [%+.2f, %+.2f] / %+.2f / %d" % (
                        r.lift_pp.iloc[0], r.lo.iloc[0], r.hi.iloc[0], r.setup_net.iloc[0], r.n.iloc[0]))
                L.append("| %s | " % st + " | ".join(cells) + " |")
            L.append("")
    if X is not None and len(X):
        L += ["## Exploration: what adds most on top of a price dip (hypotheses, chosen after looking)", "",
              "Each row: the condition AND the dip, its own trades vs the dip alone on the same ids (lift), and vs D1. "
              "Sorted by lift over the dip; n >= 150 only. X1 = one feature condition, X2 = one of the 10 best pairs "
              "of the space, XA = B / A+B with a 1-ATR dip.", ""]
        for mode in EXITS:
            sub = X[(X.exit == mode) & (X.n >= 150)].sort_values("lift_pp", ascending=False)
            L += ["### %s exit - top 15 of %d (interval above 0 over the dip: %d)" % (
                mode, len(sub), int((sub.lo > 0).sum())), "",
                  "| setup | over | n | dip net | setup net | lift over dip | 95% interval | lift over D1 | 95% interval |",
                  "|---|---|---:|---:|---:|---:|---|---:|---|"]
            for _, r in sub.head(15).iterrows():
                L.append("| %s | %s | %d | %+.4f | %+.4f | **%+.4f** | %+.4f .. %+.4f | %+.4f | %+.4f .. %+.4f |" % (
                    r.setup, r.vs, r.n, r.control_net, r.setup_net, r.lift_pp, r.lo, r.hi, r.lift_vs_D1, r.lo_vs_D1,
                    r.hi_vs_D1))
            L.append("")
    L += ["Controls: DIP_x = the first open D2..D5 after a close more than x% under the D1 open (DIP_0: any close under "
          "it); BOUNCE_green = under the D1 open, then a green day; BOUNCE_upclose = under it, then an up close; "
          "BOUNCE_dip2_green = more than 2% under it, then a green day; DIPATR_x = a close more than x ATR14 (at the "
          "signal) under the D1 open. No indicators in any control.",
          "Exploratory: the same history the setups were found on. Under original_d5 both legs sell at the same D5 "
          "close, so a lift there is entirely the entry price."]
    (out / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ==================================================================================================== v0.7
# The FROZEN setups (FROZEN_SETUPS.json, shipped next to this file): tags on every past pick (tag) and the nightly
# scan of the last five days' picks (scan). Both use the backtest's own rules (Book.field, OPS, trigger, exits_arr).
FROZEN_FILE = "FROZEN_SETUPS.json"
IST = _dt.timezone(_dt.timedelta(hours=5, minutes=30))     # a fixed offset: no time-zone database needed on Windows
ON_TIME_HOUR = 9            # a scan record counts only if written before 09:00 IST of the session it names (paper rule)
SCAN_BACK = 9               # a scan reads picks up to 9 sessions back: 5 to buy from + 4 for open fresh exits
FORWARD_FROM = "2026-11-06"  # the last session before the freeze: its scan names the first forward entries
SCAN_WORDS = {
    "FIRES": "every condition holds at tonight's close: buy at the next open",
    "ARMED": "every condition known tonight holds: buy at the next open only if that open is %s",
    "ENTERED": "entered earlier in the pick's window (entry shown); exits pending or settled",
    "WATCHING": "a condition fails tonight; the pick's window has days left",
    "EXPIRED": "the pick's five-day window ended without an entry",
    "NO DATA": "a value the setup needs is missing (bar, feature or ATR) - nothing is assumed"}
SCAN_COLS = ["scan_date", "setup", "name", "status", "trade_id", "engine", "rank", "symbol", "signal_day",
             "next_watch_day", "close_tonight", "rule_at_open", "open_threshold", "entered_day", "entry_date", "entry",
             "mark_pct", "atr_source", "primary_exit", "zone"]


def _canon_json(obj):
    return json.dumps(obj, sort_keys=True)


def frozen_hash(doc):
    return hashlib.sha256(_canon_json({k: v for k, v in doc.items() if k != "sha256"}).encode()).hexdigest()


def setup_hash(s):
    return hashlib.sha256(_canon_json({"id": s["id"], "conds": s["conds"]}).encode()).hexdigest()


def load_frozen(path=None):
    """The freeze file - shipped next to setuplab.py, never written by the tool. A changed file is refused."""
    p = Path(path) if path else Path(__file__).resolve().with_name(FROZEN_FILE)
    if not p.is_file():
        raise ValueError("no freeze file at %s (it ships next to setuplab.py)" % p)
    doc = json.loads(p.read_text(encoding="utf-8"))
    if doc.get("sha256") != frozen_hash(doc):
        raise ValueError("%s was changed after the freeze (its sha256 does not match its content) - restore the "
                         "shipped file" % p)
    for s in doc["setups"]:
        if s.get("sha256") != setup_hash(s):
            raise ValueError("setup %s in %s was changed after the freeze" % (s.get("id"), p))
    return p, doc


def frozen_conds(doc):
    return {s["id"]: [(str(c[0]), str(c[1]), float(c[2])) for c in s["conds"]] for s in doc["setups"]}


def base_name(f):
    return f[:-7] if f.endswith("_change") else f


def frozen_features(doc):
    out = []
    for s in doc["setups"]:
        for f, _, _ in s["conds"]:
            if f in PRICE_FIELDS or f.startswith("snap:"):
                continue
            out.append(base_name(f))
    return list(dict.fromkeys(out))


def new_run_dir(base, prefix):
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    day = time.strftime("%Y%m%d")
    for i in range(1, 1000):
        d = base / ("%s_%s_%03d" % (prefix, day, i))
        if not d.exists():
            d.mkdir()
            return d
    raise ValueError("no free run folder under %s" % base)


def write_hashes(folder, names):
    lines = []
    for nm in names:
        h = hashlib.sha256((Path(folder) / nm).read_bytes()).hexdigest()
        lines.append("%s  %s" % (h, nm))
    (Path(folder) / "outputs.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _days(book, idx):
    """Calendar dates (YYYY-MM-DD text) at calendar positions idx; '' outside the calendar."""
    idx = np.asarray(idx, dtype=np.int64)
    ok = (idx >= 0) & (idx < len(book.cal))
    out = np.full(len(idx), "", dtype=object)
    if ok.any():
        out[ok] = pd.DatetimeIndex(book.cal[idx[ok]]).strftime("%Y-%m-%d").to_numpy()
    return out


def tag_book(book, conds, doc):
    """One engine's book: each frozen setup's entry on every pick (watch day, date, price) and both exits, with the
    model's D1 trade on the same pick. Returns (wide: one row per pick, long: one row per entered setup, recon)."""
    n = book.n
    rows = np.arange(n)
    d1 = replay2(book, D1_CONDS)
    eng = str(book.engine_arr[0]) if n else book.engine
    W = pd.DataFrame({"trade_id": book.ids, "engine": book.engine_arr, "rank": book.rank, "symbol": book.symbols,
                      "signal_day": pd.DatetimeIndex(book.signal_day).strftime("%Y-%m-%d"), "settled": book.ok,
                      "d1_net_d5": d1["original_d5"]["ret"], "d1_net_fresh": d1["fresh"]["ret"]})
    meta = {s["id"]: s for s in doc["setups"]}
    fired = [[] for _ in range(n)]
    longs, recon = [], []
    for sid, cc in conds.items():
        day, st = trigger(book, cc)
        R = {m: exits_arr(book, day, st, m) for m in EXITS}
        has = st == "Filled"
        k = np.where(has, day, 1)
        price = np.where(has, book.O[rows, np.clip(k, 1, PATH)], np.nan)
        ent_date = np.where(has, _days(book, book.i1 + k - 1), "")
        x5 = np.where(has, _days(book, book.i1 + 4), "")
        xf = np.where(has, _days(book, book.i1 + k + 3), "")
        W["su_%s_day" % sid] = np.where(has, k, np.nan)
        W["su_%s_entry_date" % sid] = ent_date
        W["su_%s_entry" % sid] = price
        W["su_%s_net_d5" % sid] = R["original_d5"]["ret"]
        W["su_%s_net_fresh" % sid] = R["fresh"]["ret"]
        W["su_%s_status" % sid] = st
        pe = meta[sid]["primary_exit"]
        for i in np.flatnonzero(has):
            fired[i].append("%s@D%d" % (sid, k[i]))
            longs.append({"trade_id": book.ids[i], "engine": book.engine_arr[i], "rank": int(book.rank[i]),
                          "symbol": book.symbols[i], "signal_day": W.at[i, "signal_day"], "setup": sid,
                          "name": meta[sid]["name"], "watch_day": int(k[i]), "entry_date": ent_date[i],
                          "entry": float(price[i]), "exit_d5_date": x5[i], "exit_fresh_date": xf[i],
                          "net_d5": float(R["original_d5"]["ret"][i]), "net_fresh": float(R["fresh"]["ret"][i]),
                          "d1_net_d5": float(d1["original_d5"]["ret"][i]), "primary_exit": pe,
                          "net_primary": float(R[pe]["ret"][i]),
                          "settled": bool(np.isfinite(R[pe]["ret"][i]))})
        for m in EXITS:
            mm = R[m]["f"] & d1[m]["f"]
            nn = int(mm.sum())
            net = float(np.mean(R[m]["ret"][mm])) if nn else np.nan
            ctl = float(np.mean(d1[m]["ret"][mm])) if nn else np.nan
            ref = meta[sid]["final_001"].get("%s %s" % (eng, m), {})
            same = (nn == int(ref.get("n") or -1) and ref.get("setup_net") is not None
                    and abs(net - float(ref["setup_net"])) < 2e-6)
            recon.append({"setup": sid, "engine": eng, "exit": m, "n": nn, "net": net, "d1_same": ctl,
                          "final_001_n": ref.get("n"), "final_001_net": ref.get("setup_net"), "same": bool(same)})
    W["setups"] = [" ".join(x) for x in fired]
    W["n_setups"] = [len(x) for x in fired]
    return W, pd.DataFrame(longs), recon


def cmd_tag(a, log=print):
    """Tags every pick of a research watchlist (setuplab build's watchlist.parquet + calendar.parquet) with the
    frozen setups, using the panel the backtest used. Writes TAGS_<date>_<nnn> under --out."""
    try:
        fp, doc = load_frozen(a.frozen)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    conds, feats = frozen_conds(doc), frozen_features(doc)
    run = new_run_dir(Path(a.out) / "TAGS", "TAGS")
    log("%s tag: freeze %s (sha256 %s), %d setups; watchlist %s; panel %s -> %s" % (
        VERSION, fp.name, doc["sha256"][:16], len(conds), a.data, a.features, run))
    engines = [e.strip() for e in a.engines.split(",") if e.strip()]
    Ws, Ls, recon, atr = [], [], [], []
    for e in engines:
        try:
            book = load(a.data, a.features, e, feats + ["d_atr_pct"], None, log, a.chunk)
        except ValueError as ex:
            print("REFUSED: %s" % ex)
            return 3
        if book.n == 0:
            print("REFUSED: no picks of engine %s in the watchlist" % e)
            return 3
        miss = [f for f in feats if f not in book.features]
        if miss:
            print("REFUSED: the panel lacks %s (needed by the frozen setups)" % ", ".join(miss))
            return 3
        W, L, R = tag_book(book, conds, doc)
        Ws.append(W)
        Ls.append(L)
        recon += R
        if "d_atr_pct" in book.F:                       # is pick_meta's s_atr14 the panel's ATR% / 100? (the scan
            pa = book.F["d_atr_pct"][:, 1] / 100.0      # needs an ATR for the live picks)
            ok = np.isfinite(pa) & np.isfinite(book.atr)
            d = np.abs(pa[ok] - book.atr[ok])
            atr.append({"engine": e, "compared": int(ok.sum()), "within_1e-6": int((d < 1e-6).sum()),
                        "max_abs_diff": float(d.max()) if ok.any() else np.nan})
        log(" %s: %d picks, %d entered setups" % (e, book.n, len(L)))
    W = pd.concat(Ws, ignore_index=True)
    L = pd.concat(Ls, ignore_index=True) if Ls else pd.DataFrame()
    Rc = pd.DataFrame(recon)
    W.to_parquet(run / "setup_tags.parquet", index=False)
    W.to_csv(run / "setup_tags.csv", index=False)
    L.to_parquet(run / "setup_trades.parquet", index=False)
    L.to_csv(run / "setup_trades.csv", index=False)
    rec_ok = bool(Rc["same"].all()) if len(Rc) else False
    meta = {"version": VERSION, "made": _dt.datetime.now(IST).isoformat(timespec="seconds"),
            "frozen_file": str(fp), "frozen_sha256": doc["sha256"],
            "setups": [{"id": s["id"], "name": s["name"], "primary_exit": s["primary_exit"],
                        "sha256": s["sha256"]} for s in doc["setups"]],
            "watchlist": str(Path(a.data) / "watchlist.parquet"), "panel": str(a.features), "engines": engines,
            "picks": int(len(W)), "signal_days": [str(W["signal_day"].min()), str(W["signal_day"].max())],
            "reconciled_with_final_001": rec_ok, "atr_check": atr}
    (run / "TAGS.json").write_text(json.dumps(meta, indent=1, default=str), encoding="utf-8")
    md = ["# Setup tags (%s)" % VERSION, "",
          "Freeze `%s` sha256 `%s` - %s" % (fp.name, doc["sha256"][:16], ", ".join(
              "%s %s" % (s["id"], s["name"]) for s in doc["setups"])), "",
          "Watchlist `%s`, panel `%s`; %d picks, signal days %s .. %s." % (
              meta["watchlist"], meta["panel"], len(W), meta["signal_days"][0], meta["signal_days"][1]), "",
          "Files: `setup_tags.parquet/.csv` (one row per pick: `setups` = which setups entered and on which watch day, "
          "then per setup `su_<ID>_day / _entry_date / _entry / _net_d5 / _net_fresh / _status`), "
          "`setup_trades.parquet/.csv` (one row per entered setup), `TAGS.json`. Net % after 0.35 pp.", "",
          "## Every setup against FINAL_001 (the same rule on the same data must give the same trades)", "",
          "| setup | engine | exit | trades | net | D1 same trades | FINAL_001 trades | FINAL_001 net | same |",
          "|---|---|---|---:|---:|---:|---:|---:|---|"]
    for r in recon:
        md.append("| %s | %s | %s | %d | %+.4f | %+.4f | %s | %s | %s |" % (
            r["setup"], r["engine"], r["exit"], r["n"], r["net"], r["d1_same"], r["final_001_n"],
            "%+.4f" % r["final_001_net"] if r["final_001_net"] is not None else "-", "yes" if r["same"] else "NO"))
    md += ["", "**%s**" % ("RECONCILED: every setup gives FINAL_001's trades and net." if rec_ok else
                          "DIFFERS from FINAL_001 - expected only when the watchlist or the panel is not FINAL_001's "
                          "(e.g. later dates); otherwise send this file."), ""]
    if atr:
        md += ["ATR (information): pick_meta's s_atr14 is a simple 14-session ATR / close, the panel's d_atr_pct a "
               "Wilder one, so they differ by definition. The scan uses pick_meta's card or the simple ATR from the bars "
               "(v0.8); `setuplab zones --data` checks that one. s_atr14 vs d_atr_pct / 100 at the signal day: " + "; ".join(
                   "%s %d of %d within 1e-6 (largest difference %.2e)" % (x["engine"], x["within_1e-6"],
                                                                         x["compared"], x["max_abs_diff"])
                   for x in atr), ""]
    else:
        md += ["ATR check: the panel has no d_atr_pct column.", ""]
    (run / "TAGS.md").write_text("\n".join(md), encoding="utf-8")
    write_hashes(run, ["setup_tags.parquet", "setup_tags.csv", "setup_trades.parquet", "setup_trades.csv",
                       "TAGS.json", "TAGS.md"])
    log(" %s" % ("RECONCILED with FINAL_001" if rec_ok else "DIFFERS from FINAL_001 (see TAGS.md)"))
    log(" wrote %s" % run)
    print("TAGS %s" % ("RECONCILED" if rec_ok else "WRITTEN (not FINAL_001's data)"))
    return 0


# ---------------------------------------------------------------------------------------------------- the scan
def read_paper_ledger(root):
    """paper\\ledger.jsonl -> the paper test's recorded picks, with tradelab tl_watch's reader rules: a record needs
    date, engine, rank, symbol and score; the first record of each date, engine and rank is kept."""
    p = Path(root) / "paper" / "ledger.jsonl"
    if not p.is_file():
        raise ValueError("paper ledger not found: %s" % p)
    recs = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(r, dict) and all(k in r for k in ("date", "engine", "rank", "symbol", "score")):
            recs.append({"date": str(r["date"])[:10], "engine": str(r["engine"]), "rank": int(r["rank"]),
                         "symbol": str(r["symbol"]).strip(), "score": float(r["score"]),
                         "recorded_at": str(r.get("recorded_at") or "")})
    if not recs:
        raise ValueError("%s holds no watchlist records (date, engine, rank, symbol, score)" % p)
    L = pd.DataFrame(recs).drop_duplicates(["date", "engine", "rank"], keep="first").reset_index(drop=True)
    L["signal_day"] = pd.to_datetime(L["date"]).dt.normalize()
    return L


def tv_name(sym):
    """TradingView's NSE ticker (playbook's rule): '&' and '-' become '_' (M&M -> M_M)."""
    return "".join(ch if ch.isalnum() else "_" for ch in str(sym).upper())


def next_weekday(d):
    d = pd.Timestamp(d).normalize() + pd.Timedelta(days=1)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    return d


def pm_atr(root, day):
    """pick_meta's forward card for a signal day: {(engine, rank, symbol): s_atr14} when the card has that column."""
    p = Path(root) / "research2" / "pick_meta" / "forward" / ("PM_cards_%s.csv" % pd.Timestamp(day).strftime("%Y%m%d"))
    if not p.is_file():
        return {}
    try:
        df = pd.read_csv(p)
    except Exception:
        return {}
    low = {c.lower(): c for c in df.columns}
    if not {"engine", "rank", "symbol", "s_atr14"} <= set(low):
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            out[(str(r[low["engine"]]), int(r[low["rank"]]), str(r[low["symbol"]]).strip())] = float(r[low["s_atr14"]])
        except (TypeError, ValueError):
            continue
    return out


def live_book(picks, bars, cal_days, T, root):
    """A Book of live picks with every bar up to session T and ONE extra session after T (the next open, its prices
    unknown), so Book.field gives each watch day's values exactly as in the backtest.
    picks: DataFrame trade_id, engine, rank, symbol, signal_day. bars: symbol -> (dates, o, c) up to T.
    Returns (book, kstar, dropped) - kstar = the next open's watch day per pick (in the book's order); dropped =
    [(trade_id, why)] for picks that cannot be read."""
    T = np.datetime64(pd.Timestamp(T).date(), "D")
    nxt = np.datetime64(next_weekday(T).date(), "D")
    cal = np.concatenate([cal_days[cal_days <= T], [nxt]])
    rows, kst, dropped = [], {}, []
    for p in picks.itertuples(index=False):
        b = bars.get(p.symbol)
        sday = np.datetime64(pd.Timestamp(p.signal_day).date(), "D")
        if b is None:
            dropped.append((p.trade_id, "no daily bars in the cache"))
            continue
        dates, o, c = b
        m = dates <= T
        dates, o, c = dates[m], o[m], c[m]
        js = np.flatnonzero(dates == sday)
        if not len(js):
            dropped.append((p.trade_id, "no bar on the signal day"))
            continue
        j = int(js[0])
        nT = len(dates)
        ent = float(o[j + 1]) if j + 1 < nT else np.nan
        eday = dates[j + 1] if j + 1 < nT else nxt
        row = {"trade_id": p.trade_id, "engine": p.engine, "rank": int(p.rank), "symbol": p.symbol,
               "signal_day": pd.Timestamp(sday), "entry_day": str(pd.Timestamp(eday).date()), "signal_close": float(c[j]),
               "entry": ent, "status": "ok", "net_bp": 0.0}
        for k in range(1, PATH + 1):
            row["close_%d" % k] = float(c[j + k]) / ent - 1 if j + k < nT and np.isfinite(ent) else np.nan
            row["overnight_%d" % k] = (0.0 if k == 1 else float(o[j + k]) / float(c[j + k - 1]) - 1) \
                if j + k < nT else np.nan
        rows.append(row)
        kst[p.trade_id] = nT - 1 - j + 1               # own bars after the signal bar up to T, + 1
    wl = pd.DataFrame(rows)
    if wl.empty:
        return None, np.zeros(0, dtype=np.int64), dropped
    book = Book(wl, pd.Series(cal), None, engine=None)
    kstar = np.array([kst[t] for t in book.ids], dtype=np.int64)
    return book, kstar, dropped


def live_eval(book, conds, kstar):
    """Each pick's state for the next open (watch day kstar): the backtest's rule (trigger) on the days already
    past, then tonight's verdict - FIRES / ARMED (only the open's gap is unknown) / WATCHING / EXPIRED / NO DATA.
    Returns (status, entered watch day)."""
    n = book.n
    status = np.full(n, "", dtype=object)
    day = np.zeros(n, dtype=np.int64)
    done = np.zeros(n, dtype=bool)
    for k in range(1, WATCH + 1):
        anyF = np.zeros(n, dtype=bool)
        gapN = np.zeros(n, dtype=bool)
        othN = np.zeros(n, dtype=bool)
        for fld, op, val in conds:
            a = book.field(fld)[:, k]
            nan = np.isnan(a)
            r = OPS[op](np.round(np.where(nan, 0, a), 9), round(float(val), 9))
            anyF |= ~nan & ~r
            if fld == "gap_pct":
                gapN |= nan
            else:
                othN |= nan
        past = ~done & (kstar > k)
        sess = np.isfinite(book.O[:, k])
        gone = past & ~sess
        status[gone] = "NO DATA"
        done |= gone
        hit = past & sess & ~anyF & ~gapN & ~othN
        miss = past & sess & ~anyF & (gapN | othN)
        status[hit] = "ENTERED"
        day[hit] = k
        status[miss] = "NO DATA"
        done |= hit | miss
        cur = ~done & (kstar == k)
        status[cur & ~anyF & ~gapN & ~othN] = "FIRES"
        status[cur & ~anyF & gapN & ~othN] = "ARMED"
        status[cur & ~anyF & othN] = "NO DATA"
        status[cur & anyF] = "WATCHING" if k < WATCH else "EXPIRED"
        done |= cur
    status[~done] = "EXPIRED"
    return status, day


def gap_threshold(conds, close):
    """For an ARMED setup: the open's price rule, e.g. ('below', 123.4) for gap_pct < 0."""
    for f, op, v in conds:
        if f == "gap_pct":
            word = {"<": "below", "<=": "at or below", ">": "above", ">=": "at or above"}[op]
            return word, close * (1 + float(v) / 100.0)
    return "", np.nan


def on_time_deadline(T, cal_days):
    """09:00 IST of the session after T: the calendar's when it is already known (a late scan), else the next
    weekday (a holiday only moves the real session later, so the record is still on time)."""
    T = np.datetime64(pd.Timestamp(T).date(), "D")
    later = cal_days[cal_days > T]
    d = pd.Timestamp(later[0]) if len(later) else next_weekday(T)
    return _dt.datetime(d.year, d.month, d.day, ON_TIME_HOUR, 0, tzinfo=IST)


def ledger_lines(path):
    p = Path(path)
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def ledger_append(path, rec):
    """Hash-chained: each record carries the previous record's sha256 and its own."""
    old = ledger_lines(path)
    prev = old[-1]["sha256"] if old else "0" * 64
    for i, r in enumerate(old):                       # the chain must be intact before anything is added
        want = old[i - 1]["sha256"] if i else "0" * 64
        body = {k: v for k, v in r.items() if k != "sha256"}
        if r.get("prev") != want or r.get("sha256") != hashlib.sha256(_canon_json(body).encode()).hexdigest():
            raise ValueError("%s: record %d does not match the chain - the ledger was edited" % (path, i + 1))
    rec = dict(rec, prev=prev)
    rec["sha256"] = hashlib.sha256(_canon_json(rec).encode()).hexdigest()
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(_canon_json(rec) + "\n")
    return rec


class LiveData:
    """Bars, calendar and panel for the scan: tradelab's readers (stage E's bar loader, read only) and panel_live."""

    def __init__(self, root, stage_e_any=False, panel="panel_live"):
        try:
            import tl_data as TD
        except ImportError as e:
            raise ValueError("cannot import tradelab's tl_data (%s) - start with tradelab's env_tradelab.bat" % e)
        self.root = Path(root)
        self.TD = TD
        self.market = TD.Market(self.root, TD.Production(stage_e_any=stage_e_any))
        self.cal = np.asarray(self.market.cal).astype("datetime64[D]")
        self.panel = self.root / panel / "panel.parquet" if panel else None
        if panel and not self.panel.is_file():
            raise ValueError("%s not found (the scan reads the nightly panel)" % self.panel)

    def bars(self, symbols):
        self.market.load(list(symbols))
        out = {}
        for s in symbols:
            ds = self.market.series(s)
            if ds is not None:
                out[s] = (np.asarray(ds.dates).astype("datetime64[D]"), np.asarray(ds.o, float),
                          np.asarray(ds.c, float))
        return out

    def ohlcv(self, symbols):
        """symbol -> (dates, open, high, low, close, volume) of the stock's own daily bars (v0.8: the zones)."""
        self.market.load(list(symbols))
        out = {}
        for s in symbols:
            ds = self.market.series(s)
            if ds is not None:
                out[s] = (np.asarray(ds.dates).astype("datetime64[D]"), np.asarray(ds.o, float),
                          np.asarray(ds.h, float), np.asarray(ds.l, float), np.asarray(ds.c, float),
                          np.asarray(ds.v, float))
        return out

    def index_closes(self, names):
        """{key: cache symbol} -> {key: (dates, closes)}; a missing index file is refused (the zones need all four)."""
        out = {}
        for k, sym in names.items():
            ds = self.market.series(sym)
            if ds is None:
                raise ValueError("%s daily bars are not in the cache (the zones need NIFTY50, NIFTYMIDCAP150, "
                                 "NIFTYSMLCAP250 and INDIAVIX)" % sym)
            out[k] = (np.asarray(ds.dates).astype("datetime64[D]"), np.asarray(ds.c, float))
        return out

    def forget(self, symbols):
        """Drop symbols' bars from memory (the whole-market pass reads every stock once)."""
        keep = {v for _, v in ZONE_INDEX} | {"NIFTY50"}
        for s in symbols:
            if s not in keep:
                self.market.daily.pop(s, None)


def scan_day(T, doc, conds, feats, L, data, out, log=print):
    """One evening: every pick of the last SCAN_BACK sessions up to T against every frozen setup."""
    T = np.datetime64(pd.Timestamp(T).date(), "D")
    cal = data.cal
    iT = int(np.searchsorted(cal, T, side="right")) - 1
    if iT < 0 or cal[iT] != T:
        raise ValueError("%s is not a session in the cache's calendar" % T)
    first = cal[max(0, iT - SCAN_BACK)]
    P = L[(L["signal_day"] >= pd.Timestamp(first)) & (L["signal_day"] <= pd.Timestamp(T))].copy()
    P["trade_id"] = ["%s-%s-%d" % (e, pd.Timestamp(d).strftime("%Y%m%d"), r)
                     for e, d, r in zip(P["engine"], P["signal_day"], P["rank"])]
    bars = data.bars(sorted(P["symbol"].unique()))
    book, kstar, dropped = live_book(P, bars, cal, T, data.root)
    meta = {s["id"]: s for s in doc["setups"]}
    rows = []
    byid = P.set_index("trade_id")
    for tid, why in dropped:
        p = byid.loc[tid]
        for sid in conds:
            rows.append({"scan_date": str(pd.Timestamp(T).date()), "setup": sid, "name": meta[sid]["name"],
                         "status": "NO DATA", "trade_id": tid, "engine": p["engine"], "rank": int(p["rank"]),
                         "symbol": p["symbol"], "signal_day": str(pd.Timestamp(p["signal_day"]).date()),
                         "next_watch_day": "", "close_tonight": np.nan, "rule_at_open": why, "open_threshold": np.nan,
                         "entered_day": "", "entry_date": "", "entry": np.nan, "mark_pct": np.nan, "atr_source": "",
                         "primary_exit": meta[sid]["primary_exit"]})
    if book is None or book.n == 0:
        return pd.DataFrame(rows, columns=SCAN_COLS), P
    book.attach(data.panel, feats + ["d_atr_pct"], chunk=8)
    miss = [f for f in feats if f not in book.features]
    if miss:
        raise ValueError("%s lacks %s (the frozen setups read them)" % (data.panel, ", ".join(miss)))
    live = kstar <= WATCH
    if live.any():
        rr = np.flatnonzero(live)
        seen = np.zeros(len(rr), dtype=bool)
        for f in feats:
            seen |= np.isfinite(book.F[f][rr, kstar[rr]])
        if not seen.any():
            raise ValueError("%s has no row for %s yet (the scan reads tonight's features from it): run the scan again "
                             "once the nightly panel is updated (it is retried by --all-missing)" % (
                                 data.panel, pd.Timestamp(T).date()))
    # ATR14 / close at the pick: pick_meta's card when it has s_atr14, else the panel's d_atr_pct / 100
    src = np.full(book.n, "", dtype=object)
    atr = np.full(book.n, np.nan)
    cards = {}
    for i in range(book.n):
        d = pd.Timestamp(book.signal_day[i])
        if d not in cards:
            cards[d] = pm_atr(data.root, d)
        v = cards[d].get((str(book.engine_arr[i]), int(book.rank[i]), str(book.symbols[i])))
        if v is not None and np.isfinite(v):
            atr[i], src[i] = v, "pick_meta"
    fill = ~np.isfinite(atr)
    if fill.any():
        sa = signal_atr(data, book, np.flatnonzero(fill))
        ok = np.isfinite(sa)
        idx = np.flatnonzero(fill)[ok]
        atr[idx], src[idx] = sa[ok], "bars"
    book.atr = atr
    book.__dict__.pop("_cache", None)
    rws = np.arange(book.n)
    cT = book.PC[rws, np.clip(kstar, 1, PATH)]          # tonight's close = the previous close of the next open
    for sid, cc in conds.items():
        if any(base_name(f) in miss for f, _, _ in cc):
            st, day = np.full(book.n, "NO DATA", dtype=object), np.zeros(book.n, dtype=np.int64)
        else:
            st, day = live_eval(book, cc, kstar)
        word, _ = gap_threshold(cc, 1.0)
        for i in range(book.n):
            k = int(kstar[i])
            r = {"scan_date": str(pd.Timestamp(T).date()), "setup": sid, "name": meta[sid]["name"],
                 "status": st[i], "trade_id": book.ids[i], "engine": book.engine_arr[i], "rank": int(book.rank[i]),
                 "symbol": book.symbols[i], "signal_day": str(pd.Timestamp(book.signal_day[i]).date()),
                 "next_watch_day": k if k <= WATCH else "", "close_tonight": float(cT[i]) if k <= PATH else np.nan,
                 "rule_at_open": "", "open_threshold": np.nan, "entered_day": "", "entry_date": "", "entry": np.nan,
                 "mark_pct": np.nan, "atr_source": src[i] if any(f == "pc_vs_d1_atr" for f, _, _ in cc) else "",
                 "primary_exit": meta[sid]["primary_exit"]}
            if st[i] == "ARMED":
                w, thr = gap_threshold(cc, float(cT[i]))
                r["rule_at_open"], r["open_threshold"] = "open %s %.2f" % (w, thr), thr
            if st[i] == "ENTERED":
                kk = int(day[i])
                r["entered_day"] = kk
                r["entry_date"] = str(pd.Timestamp(book.cal[book.i1[i] + kk - 1]).date())
                r["entry"] = float(book.O[i, kk])
                last = min(k - 1, PATH)
                if last >= kk and np.isfinite(book.C[i, last]):
                    r["mark_pct"] = (float(book.C[i, last]) / r["entry"] - 1) * 100
            rows.append(r)
    S = pd.DataFrame(rows, columns=SCAN_COLS)
    return S, P


def atr_simple(h, l, c):
    """ATR14 / close as pick_meta's s_atr14 (the label contract, panel_build): a SIMPLE 14-session mean of the true
    range from the second bar, divided by the close. Not D_atr_pct (Wilder): v0.8 found the two agree on 3 of 15,819
    picks, so S1's 1-ATR dip must use this one wherever s_atr14 is not recorded."""
    h, l, c = (np.asarray(x, float) for x in (h, l, c))
    tr = np.full(len(c), np.nan)
    if len(c) > 1:
        tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    a = pd.Series(tr).rolling(14, min_periods=14).mean().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        return a / np.where(c == 0, np.nan, c)


def signal_atr(data, book, rows):
    """s_atr14 at the signal day for book rows without one, from the stock's bars (atr_simple)."""
    out = np.full(len(rows), np.nan)
    if not hasattr(data, "ohlcv") or not len(rows):
        return out
    bars = data.ohlcv(sorted({str(book.symbols[i]) for i in rows}))
    for k, i in enumerate(rows):
        b = bars.get(str(book.symbols[i]))
        if b is None:
            continue
        dates = np.asarray(b[0]).astype("datetime64[D]")
        j = int(np.searchsorted(dates, np.datetime64(pd.Timestamp(book.signal_day[i]).date(), "D")))
        if j < len(dates) and dates[j] == np.datetime64(pd.Timestamp(book.signal_day[i]).date(), "D"):
            out[k] = atr_simple(b[2], b[3], b[4])[j]
    return out


def zone_flags(S, data, zdoc, T):
    """v0.8: each FIRES / ARMED / ENTERED row IN or OUT of its setup's picks zone (SETUP_ZONES.json), read at the
    close before the entry: tonight's close for FIRES / ARMED, the close before the entry day for ENTERED. Blank =
    the setup has no zone (or no zones file)."""
    S = S.copy()
    S["zone"] = ""
    if zdoc is None or S.empty:
        return S
    zones = {sid: zone_parse(((zdoc["setups"].get(sid) or {}).get("picks") or {}).get("zone", ""))
             for sid in S["setup"].unique()}
    need = S["status"].isin(["FIRES", "ARMED", "ENTERED"]).to_numpy() & S["setup"].map(
        lambda x: bool(zones.get(x))).to_numpy()
    if not need.any():
        return S
    M = market_dims(data.index_closes(dict(ZONE_INDEX)))
    bars = data.ohlcv(sorted(S.loc[need, "symbol"].unique()))
    T = np.datetime64(pd.Timestamp(T).date(), "D")
    cache, out = {}, S["zone"].to_numpy(dtype=object, copy=True)
    for i in np.flatnonzero(need):
        r = S.iloc[i]
        if r["symbol"] not in bars:
            out[i] = "OUT"
            continue
        if r["symbol"] not in cache:
            dates, o, h, l, c, v = bars[r["symbol"]]
            dates = np.asarray(dates).astype("datetime64[D]")
            cache[r["symbol"]] = (dates, zone_buckets(zone_values(dates, o, h, l, c, v, M)))
        dates, B = cache[r["symbol"]]
        if r["status"] == "ENTERED":
            j = int(np.searchsorted(dates, np.datetime64(str(r["entry_date"]), "D"))) - 1
        else:
            j = int(np.searchsorted(dates, T, side="right")) - 1
            if j >= 0 and dates[j] != T:
                j = -1
        inside = j >= 0 and all(lo <= B[dim][j] <= hi for dim, lo, hi in zones[r["setup"]])
        out[i] = "IN" if inside else "OUT"
    S["zone"] = out
    return S


def forward_record(L, data, doc, conds, feats, ledger_path, T, since=FORWARD_FROM):
    """The forward record: every setup entry a scan named ON TIME (FIRES / ARMED, the scan date on or after
    FORWARD_FROM) that the bars then show was entered on that watch day; both exits and D1 on the same pick."""
    recs = [r for r in ledger_lines(ledger_path) if r.get("event") == "scan" and r.get("on_time")
            and r.get("scan_date", "") >= since]
    named, zoned = {}, {}
    for r in recs:
        for x in r.get("named", []):
            named.setdefault((x["trade_id"], x["setup"]), (int(x["watch_day"]), r["scan_date"]))
            zoned.setdefault((x["trade_id"], x["setup"]), x.get("zone", ""))
    if not named:
        return pd.DataFrame()
    ids = sorted({t for t, _ in named})
    P = L.copy()
    P["trade_id"] = ["%s-%s-%d" % (e, pd.Timestamp(d).strftime("%Y%m%d"), r)
                     for e, d, r in zip(P["engine"], P["signal_day"], P["rank"])]
    P = P[P["trade_id"].isin(ids)]
    bars = data.bars(sorted(P["symbol"].unique()))
    book, kstar, _ = live_book(P, bars, data.cal, T, data.root)
    if book is None:
        return pd.DataFrame()
    book.attach(data.panel, feats + ["d_atr_pct"], chunk=8)
    atr = np.full(book.n, np.nan)
    for i in range(book.n):
        v = pm_atr(data.root, book.signal_day[i]).get((str(book.engine_arr[i]), int(book.rank[i]),
                                                        str(book.symbols[i])))
        if v is not None:
            atr[i] = v
    fill = ~np.isfinite(atr)
    if fill.any():
        atr[np.flatnonzero(fill)] = signal_atr(data, book, np.flatnonzero(fill))
    book.atr = atr
    book.__dict__.pop("_cache", None)
    meta = {s["id"]: s for s in doc["setups"]}
    rows = []
    d1d, d1s = trigger_all(book, D1_CONDS)
    d1 = exits_arr(book, d1d, d1s, "original_d5")
    for sid, cc in conds.items():
        st, day = live_eval(book, cc, np.full(book.n, WATCH + 1, dtype=np.int64))
        status = np.where(st == "ENTERED", "Filled", "No entry")
        R = {m: exits_arr(book, day, status, m) for m in EXITS}
        for i in range(book.n):
            key = (book.ids[i], sid)
            if key not in named:
                continue
            k_named, sdate = named[key]
            entered = st[i] == "ENTERED" and int(day[i]) == k_named
            pe = meta[sid]["primary_exit"]
            rows.append({"setup": sid, "trade_id": book.ids[i], "engine": book.engine_arr[i],
                         "rank": int(book.rank[i]), "symbol": book.symbols[i],
                         "signal_day": str(pd.Timestamp(book.signal_day[i]).date()), "named_on": sdate,
                         "named_watch_day": k_named, "entered": bool(entered),
                         "entry_date": str(pd.Timestamp(book.cal[book.i1[i] + k_named - 1]).date())
                         if entered else "", "entry": float(book.O[i, k_named]) if entered else np.nan,
                         "net_d5": float(R["original_d5"]["ret"][i]) if entered else np.nan,
                         "net_fresh": float(R["fresh"]["ret"][i]) if entered else np.nan,
                         "d1_net_d5": float(d1["ret"][i]), "primary_exit": pe, "zone": zoned.get(key, ""),
                         "net_primary": float(R[pe]["ret"][i]) if entered else np.nan})
    F = pd.DataFrame(rows)
    if len(F):
        F["settled"] = F["entered"] & np.isfinite(F["net_primary"].astype(float))
    return F


def trigger_all(book, conds):
    """trigger() for books whose picks are not settled yet (every pick is evaluated)."""
    ok = book.ok
    book.ok = np.ones(book.n, dtype=bool)
    try:
        return trigger(book, conds)
    finally:
        book.ok = ok


def scan_page(T, S, F, doc, rec, out_csv, tv_file, zdoc=None):
    """SCAN_<date>.md: what to do at the next open, positions, and the forward record so far."""
    d = str(pd.Timestamp(T).date())
    L = ["# Setup scan - picks of the last five sessions, tonight %s (%s)" % (d, VERSION), "",
         "Freeze sha256 `%s`. Recorded %s - %s (%s)." % (
             doc["sha256"][:16], rec["recorded_at"], "ON TIME" if rec["on_time"] else "LATE: counts for nothing",
             "deadline %s" % rec["deadline"]), ""]
    if S.empty:
        L += ["No picks in the last five sessions.", ""]
    else:
        act = S[S["status"].isin(["FIRES", "ARMED"])].sort_values(["setup", "engine", "rank"])
        L += ["## At the next open", ""]
        if act.empty:
            L += ["Nothing fires.", ""]
        else:
            L += ["| setup | what to do | stock | engine / rank | signal day | watch day | tonight's close | zone |",
                  "|---|---|---|---|---|---:|---:|---|"]
            for r in act.itertuples(index=False):
                what = "BUY at the open" if r.status == "FIRES" else "BUY at the open only if %s" % r.rule_at_open
                L.append("| %s | %s | %s | %s %d | %s | D%s | %.2f | %s |" % (
                    r.setup, what, r.symbol, r.engine, r.rank, r.signal_day, r.next_watch_day, r.close_tonight,
                    getattr(r, "zone", "") or "-"))
            L.append("")
        pos = S[S["status"] == "ENTERED"].sort_values(["setup", "entry_date"])
        if len(pos):
            L += ["## Entered (exits: original_d5 = the pick's D5 close; fresh = 4 sessions after the entry)", "",
                  "| setup | stock | engine / rank | signal day | entered | price | now % (gross) |",
                  "|---|---|---|---|---|---:|---:|"]
            for r in pos.itertuples(index=False):
                L.append("| %s | %s | %s %d | %s | %s (D%s) | %.2f | %s |" % (
                    r.setup, r.symbol, r.engine, r.rank, r.signal_day, r.entry_date, r.entered_day, r.entry,
                    "%+.2f" % r.mark_pct if np.isfinite(r.mark_pct) else "-"))
            L.append("")
        cnt = S.pivot_table(index="setup", columns="status", values="trade_id", aggfunc="count", fill_value=0)
        L += ["## Every pick of the last five sessions (counts)", "",
              "| setup | " + " | ".join(cnt.columns) + " |", "|---|" + "---:|" * len(cnt.columns)]
        for sid, r in cnt.iterrows():
            L.append("| %s | " % sid + " | ".join(str(int(x)) for x in r.to_numpy()) + " |")
        L += [""]
    L += ["## Forward record since the freeze (entries named on time; the judge is at month 6 / 12)", ""]
    if F is None or F.empty:
        L += ["No on-time entries yet.", ""]
    else:
        L += ["| setup | named | entered | settled | mean net at its primary exit | D1 on the same picks | "
              "settled IN its zone | mean net IN its zone |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for s in doc["setups"]:
            g = F[F["setup"] == s["id"]]
            st = g[g["settled"]]
            zi = st[st["zone"] == "IN"] if "zone" in st.columns else st.iloc[:0]
            L.append("| %s | %d | %d | %d | %s | %s | %d | %s |" % (
                s["id"], len(g), int(g["entered"].sum()), len(st),
                "%+.4f" % st["net_primary"].mean() if len(st) else "-",
                "%+.4f" % st["d1_net_d5"].mean() if len(st) and st["d1_net_d5"].notna().any() else "-",
                len(zi), "%+.4f" % zi["net_primary"].mean() if len(zi) else "-"))
        L += [""]
    L += ["Statuses: " + "; ".join("%s = %s" % (k, (v % "below / above the threshold") if "%s" in v else v)
                                   for k, v in SCAN_WORDS.items()), "",
          "Files: `%s` (every pick x setup), `%s` (import into TradingView: Watchlist menu, Import list)." % (
              Path(out_csv).name, Path(tv_file).name),
          "Setups: " + "; ".join("%s %s (primary exit %s)" % (s["id"], s["name"], s["primary_exit"])
                                 for s in doc["setups"]), ""]
    if zdoc is not None:
        L += ["Zones (SETUP_ZONES.json sha256 %s; IN / OUT = the close before the entry inside / outside the setup's "
              "picks zone; a zone is a hypothesis - the forward record keeps every entry): " % zdoc["sha256"][:16] +
              "; ".join("%s %s (out of sample: %s)" % (
                  sid, (r.get("picks") or {}).get("text", "-"), " / ".join(
                      v["verdict"] for v in ((r.get("picks") or {}).get("out_of_sample") or {}).values()) or "-")
                  for sid, r in zdoc["setups"].items()), ""]
    else:
        L += ["Zones: none (run setuplab zones to add each setup's zone).", ""]
    return "\n".join(L)


def tv_text(S):
    """TradingView import: one section per setup and action, NSE tickers."""
    parts = []
    if S.empty:
        return ""
    for sid in sorted(S["setup"].unique()):
        for stt, label in (("FIRES", "buy at open"), ("ARMED", "buy if the open meets its rule")):
            g = S[(S["setup"] == sid) & (S["status"] == stt)]
            if len(g):
                parts.append("###%s %s" % (sid, label))
                parts += ["NSE:%s" % tv_name(s) for s in dict.fromkeys(g["symbol"])]
    w = S[S["status"] == "ENTERED"]
    if len(w):
        parts.append("###Entered (open setup positions)")
        parts += ["NSE:%s" % tv_name(s) for s in dict.fromkeys(w["symbol"])]
    return ",".join(parts)


def cmd_scan(a, log=print):
    """The nightly scan (after Run Now): the last five sessions' picks against every frozen setup."""
    try:
        fp, doc = load_frozen(a.frozen)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    conds, feats = frozen_conds(doc), frozen_features(doc)
    out = Path(a.out) / "scan"
    out.mkdir(parents=True, exist_ok=True)
    try:
        data = LiveData(a.root, a.stage_e_any, a.panel)
        log("%s scan: freeze %s (sha256 %s); bars through %s; panel %s" % (
            VERSION, fp.name, doc["sha256"][:16], pd.Timestamp(data.cal[-1]).date(), data.panel))
        L = read_paper_ledger(a.root)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    try:
        zrun, zdoc = load_zones(a.out)
    except ValueError as e:
        zrun, zdoc = None, None
        log(" zones NOT used: %s" % e)
    tdoc, listed = None, None
    try:
        tpath, tdoc = load_tree(getattr(a, "tree", None) or None)
        log(" tree: %s (sha256 %s)" % (tpath.name, tdoc["sha256"][:16]))
    except ValueError as e:
        log(" tree NOT used: %s" % e)
    if tdoc is not None:
        try:
            listed = etf_list(a.root)
            log(" ETFs: %s" % ("NSE's list + the name rule" if listed is not None else
                               "the name rule and TREE.json's names"))
        except Exception as e:                            # NSE's ETF list unreadable: the name rule only
            log(" NSE's ETF list not read (%s: %s) - the name rule and TREE.json's names only" % (
                type(e).__name__, e))
    if zdoc is not None:
        log(" zones: %s (sha256 %s): %s" % (zrun.name, zdoc["sha256"][:16], "; ".join(
            "%s %s" % (sid, (r.get("picks") or {}).get("zone") or "-") for sid, r in zdoc["setups"].items())))
    cal = data.cal
    if a.date:
        days = [np.datetime64(pd.Timestamp(a.date).date(), "D")]
    else:
        last = cal[-1]
        days = [last]
        if a.all_missing:
            days = [d for d in cal if np.datetime64(FORWARD_FROM, "D") <= d <= last]
    lp = out / "setup_ledger.jsonl"
    rc = 0
    for T in days:
        tag = pd.Timestamp(T).strftime("%Y%m%d")
        page, csv, tv = out / ("SCAN_%s.md" % tag), out / ("scan_%s.csv" % tag), out / ("tv_%s.txt" % tag)
        if page.is_file() and not a.force:
            log(" %s: already scanned (SCAN_%s.md) - skipped; --force rescans (the ledger keeps the first record)" % (
                pd.Timestamp(T).date(), tag))
            continue
        try:
            S, P = scan_day(T, doc, conds, feats, L, data, out, log)
        except ValueError as e:
            print("REFUSED (%s): %s" % (pd.Timestamp(T).date(), e))
            rc = 3
            continue
        try:
            S = zone_flags(S, data, zdoc, T)
        except Exception as e:                    # a zone problem never stops the scan: the rows stay without zone
            log(" %s: zones not applied (%s: %s)" % (pd.Timestamp(T).date(), type(e).__name__, e))
            S = S.copy()
            S["zone"] = ""
        now = _dt.datetime.now(IST)
        dl = on_time_deadline(T, cal)
        named = [] if S.empty else [
            {"setup": r.setup, "status": r.status, "trade_id": r.trade_id, "symbol": r.symbol,
             "watch_day": int(r.next_watch_day), "close_tonight": round(float(r.close_tonight), 4),
             "rule_at_open": r.rule_at_open, "zone": r.zone}
            for r in S[S["status"].isin(["FIRES", "ARMED"])].itertuples(index=False)]
        rec = {"event": "scan", "scan_date": str(pd.Timestamp(T).date()), "recorded_at": now.isoformat(timespec="seconds"),
               "deadline": dl.isoformat(timespec="minutes"), "on_time": now < dl, "tool": VERSION,
               "frozen_sha256": doc["sha256"], "zones_sha256": zdoc["sha256"] if zdoc else None,
               "picks": int(len(P)), "named": named}
        old = [r for r in ledger_lines(lp) if r.get("event") == "scan" and r.get("scan_date") == rec["scan_date"]]
        if not old:
            try:
                ledger_append(lp, rec)
            except ValueError as e:
                print("REFUSED: %s" % e)
                return 3
        else:
            rec = old[0]
        F = forward_record(L, data, doc, conds, feats, lp, T)
        S.to_csv(csv, index=False)
        tv.write_text(tv_text(S) + "\n", encoding="utf-8")
        if F is not None and len(F):
            F.to_csv(out / "forward_trades.csv", index=False)
        ttxt = ""
        if tdoc is not None and str(pd.Timestamp(T).date()) >= TREE_FROM:
            try:
                ttxt, trec = tree_evening(T, tdoc, doc, L, data, S, F, out, listed, log=log)
                log(" %s: tree %s" % (pd.Timestamp(T).date(), ("orders named (%s)" % (
                    "on time" if trec["on_time"] else "LATE")) if trec else "no orders"))
            except Exception as e:                    # the tree never stops the setup scan
                ttxt = ("## Tree\n\nNOT built tonight (%s: %s) - the setup scan below is unaffected; send this "
                        "line.\n" % (type(e).__name__, e))
                log(" %s: tree NOT built (%s: %s)" % (pd.Timestamp(T).date(), type(e).__name__, e))
        page.write_text((ttxt + "\n" if ttxt else "") + scan_page(T, S, F, doc, rec, csv, tv, zdoc), encoding="utf-8")
        act = 0 if S.empty else int(S["status"].isin(["FIRES", "ARMED"]).sum())
        log(" %s: %d picks, %d setup entries named for the next open (%s) -> %s" % (
            pd.Timestamp(T).date(), len(P), act, "on time" if rec["on_time"] else "LATE", page))
    return rc


# ===================================================================================== v0.8: zones and the whole market
ZONES_FILE = "SETUP_ZONES.json"
ZONE_RULE = ("zones v1, declared 8 Nov 2026 before any zone result. Every dimension is read at the close before the "
             "entry (the close the setup's own conditions are read at). A candidate is one range of one dimension, or "
             "two ranges of two dimensions. It must keep %d trades a year in each population. It QUALIFIES when, in "
             "every population (picks: D and ENS; the whole market: one), inside minus outside (net %% per trade) has "
             "a 95%% interval above 0 and the check (picks: the lift over the model's D1 entry on the same picks; the "
             "whole market: the excess over buying every stock at the same open) has a 95%% interval above 0. The "
             "winner is the qualifying zone whose net per trade has the highest strict lower bound (mean - 3.29 "
             "bootstrap standard deviations, 99.9%%) in its weakest population - the strict level only RANKS the "
             "qualifiers, so a narrow lucky slice does not beat a broad real one. None qualifies = no zone. Plain 95%% per candidate (Karan's choice, 8 Nov): about 1 in 20 "
             "candidates passes by luck, so the same search is replayed year by year (choose with exits before "
             "1 Jan, judge on that year): HOLDS only if inside beats outside out of sample." % 40)
# (id, what, edges ascending - bucket = how many edges are at or below the value - or None for a code, bucket labels)
ZONE_DIMS = (
    ("ATRP", "ATR14 % of the close", (2.0, 3.0, 4.5), ("<2", "2-3", "3-4.5", ">=4.5")),
    ("ATRX", "ATR14 % / its mean of the last 50 sessions", (0.85, 1.15), ("<0.85", "0.85-1.15", ">=1.15")),
    ("TREND", "close vs EMA50 and EMA200", None, ("below both", "between", "above both")),
    ("RET20", "20-session return %", (-10.0, 0.0, 10.0), ("<-10", "-10 to 0", "0 to 10", ">=10")),
    ("RSI14", "RSI 14", (30.0, 50.0, 70.0), ("<30", "30-50", "50-70", ">=70")),
    ("DD52", "% from the highest close of the last 252 sessions", (-30.0, -15.0, -5.0),
     ("<-30", "-30 to -15", "-15 to -5", ">=-5")),
    ("RVOL", "volume / mean volume of the 20 sessions before", (0.7, 1.5), ("<0.7", "0.7-1.5", ">=1.5")),
    ("RS20", "20-session return minus Smallcap 250's (pts)", (-5.0, 5.0), ("<-5", "-5 to 5", ">=5")),
    ("IDX", "NIFTY 50, Midcap 150, Smallcap 250 closing at or above their 50-session mean (how many)", None,
     ("0", "1", "2", "3")),
    ("VIXP", "India VIX percentile in its last 250 sessions", (100.0 / 3, 200.0 / 3), ("<33", "33-67", ">=67")),
    ("VIX5", "India VIX 5-session change %", (-10.0, 10.0), ("<-10", "-10 to 10", ">=10")),
    ("NIFTY20", "NIFTY 50 20-session return %", (-3.0, 3.0), ("<-3", "-3 to 3", ">=3")),
)
ZDIM = {d[0]: d for d in ZONE_DIMS}
ZONE_INDEX = (("nifty", "NIFTY50"), ("mid", "NIFTYMIDCAP150"), ("small", "NIFTYSMLCAP250"), ("vix", "INDIAVIX"))
ZONE_MIN_PER_YEAR = 40       # trades a year a zone must keep in each population (month 12 can then reach 30)
ZONE_FINALISTS = 40          # the best by a quick strict lower bound get the full block bootstrap
ZONE_RANK_Z = 3.29           # ranking only: mean - 3.29 standard deviations (99.9%); qualifying stays plain 95%
ZONE_WF_YEARS = (2022, 2023, 2024, 2025, 2026)
MARKET_FROM = np.datetime64("2020-01-01")
PINE_CODE_TAG = "BMSZ1"


def stock_dims(o, h, l, c, v):
    """The stock's own zone values at every bar's close (ATR, RSI and EMA exactly as production's features_daily)."""
    h, l, c, v = (pd.Series(np.asarray(x, float)) for x in (h, l, c, v))
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    atrp = tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean() / c.replace(0, np.nan) * 100
    e50 = c.ewm(span=50, adjust=False, min_periods=50).mean()
    e200 = c.ewm(span=200, adjust=False, min_periods=200).mean()
    trend = np.where((c > e50) & (c > e200), 2.0, np.where((c < e50) & (c < e200), 0.0, 1.0))
    trend[(e50.isna() | e200.isna() | c.isna()).to_numpy()] = np.nan
    d = c.diff()
    ag = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    al = (-d.clip(upper=0)).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    rsi = 100 - 100 / (1 + ag / al.replace(0, np.nan))
    warm = ag.notna() & al.notna()
    rsi = rsi.mask(warm & (al == 0) & (ag > 0), 100.0).mask(warm & (ag == 0) & (al > 0), 0.0) \
        .mask(warm & (ag == 0) & (al == 0), 50.0)
    vm = v.shift(1).rolling(20, min_periods=20).mean()
    out = {"ATRP": atrp, "ATRX": atrp / atrp.rolling(50, min_periods=50).mean(), "TREND": pd.Series(trend),
           "RET20": (c / c.shift(20) - 1) * 100, "RSI14": rsi,
           "DD52": (c / c.rolling(252, min_periods=252).max() - 1) * 100, "RVOL": v / vm.replace(0, np.nan)}
    return {k: pd.to_numeric(x, errors="coerce").replace([np.inf, -np.inf], np.nan).to_numpy(float)
            for k, x in out.items()}


def pct_rank_window(x, window=250, minp=60):
    """tradelab tl_context's rolling_pct_rank: the share of the last `window` values (today included) at or below
    today's; blank with fewer than minp values."""
    x = np.asarray(x, float)
    out = np.full(len(x), np.nan)
    for i in range(len(x)):
        if np.isfinite(x[i]):
            a = x[max(0, i - window + 1):i + 1]
            a = a[np.isfinite(a)]
            if len(a) >= minp:
                out[i] = float(np.mean(a <= x[i]))
    return out


def market_dims(idx):
    """idx: nifty / mid / small / vix -> (dates, closes). -> by date: IDX, VIXP, VIX5, NIFTY20 and SMALL20 (for RS20).
    Each index's measures run over its own sessions; a date an input lacks stays blank."""
    S = {k: pd.Series(np.asarray(cl, float), index=pd.DatetimeIndex(np.asarray(d).astype("datetime64[D]")))
         for k, (d, cl) in idx.items()}
    cols = {}
    for k in ("nifty", "mid", "small"):
        s = S[k]
        m = s.rolling(50, min_periods=50).mean()
        cols["up_" + k] = (s >= m).astype(float).where(m.notna() & s.notna())
    cols["NIFTY20"] = (S["nifty"] / S["nifty"].shift(20) - 1) * 100
    cols["SMALL20"] = (S["small"] / S["small"].shift(20) - 1) * 100
    vx = S["vix"]
    cols["VIXP"] = pd.Series(pct_rank_window(vx.to_numpy()) * 100, index=vx.index)
    cols["VIX5"] = (vx / vx.shift(5) - 1) * 100
    M = pd.DataFrame(cols)
    M["IDX"] = M[["up_nifty", "up_mid", "up_small"]].sum(axis=1, min_count=3)
    return M[["IDX", "VIXP", "VIX5", "NIFTY20", "SMALL20"]].replace([np.inf, -np.inf], np.nan)


def zone_values(dates, o, h, l, c, v, M):
    """Every zone dimension at every bar's close of one stock (M = market_dims)."""
    z = stock_dims(o, h, l, c, v)
    m = M.reindex(pd.DatetimeIndex(np.asarray(dates).astype("datetime64[D]")))
    for k in ("IDX", "VIXP", "VIX5", "NIFTY20"):
        z[k] = m[k].to_numpy(float)
    z["RS20"] = z["RET20"] - m["SMALL20"].to_numpy(float)
    return z


def zone_buckets(z):
    """dimension -> int8 bucket of every value (-1 = unknown)."""
    out = {}
    for dim, _, edges, labels in ZONE_DIMS:
        x = np.asarray(z[dim], float)
        b = np.full(len(x), -1, np.int8)
        ok = np.isfinite(x)
        if edges is None:
            b[ok] = np.clip(np.round(x[ok]), 0, len(labels) - 1).astype(np.int8)
        else:
            b[ok] = np.searchsorted(np.asarray(edges, float), x[ok], side="right").astype(np.int8)
        out[dim] = b
    return out


def _zone_ranges():
    R = []
    for dim, _, _, labels in ZONE_DIMS:
        for lo in range(len(labels)):
            for hi in range(lo, len(labels)):
                if not (lo == 0 and hi == len(labels) - 1):
                    R.append((dim, lo, hi))
    return R


ZONE_RANGES = _zone_ranges()


def zone_key(zone):
    return "+".join("%s:%d:%d" % r for r in zone) if zone else ""


def zone_parse(text):
    if not text:
        return ()
    out = []
    for part in str(text).split("+"):
        dim, lo, hi = part.split(":")
        if dim not in ZDIM or not 0 <= int(lo) <= int(hi) < len(ZDIM[dim][3]):
            raise ValueError("not a zone: %s" % text)
        out.append((dim, int(lo), int(hi)))
    return tuple(out)


def zone_text(zone):
    """A zone in words, e.g. 'ATR14 % of the close 3 and above & India VIX percentile below 33'."""
    if not zone:
        return "no zone (the setup alone)"
    parts = []
    for dim, lo, hi in zone:
        _, what, edges, labels = ZDIM[dim]
        if edges is None:
            v = labels[lo] if lo == hi else "%s to %s" % (labels[lo], labels[hi])
        elif lo == 0:
            v = "below %g" % edges[hi]
        elif hi == len(labels) - 1:
            v = "%g and above" % edges[lo - 1]
        else:
            v = "%g to %g" % (edges[lo - 1], edges[hi])
        parts.append("%s %s: %s" % (dim, what, v))
    return " & ".join(parts)


def zone_mask(zone, B):
    """Which rows are inside the zone (B: dimension -> buckets; an unknown bucket is outside)."""
    n = len(next(iter(B.values())))
    m = np.ones(n, bool)
    for dim, lo, hi in zone:
        b = np.asarray(B[dim])
        m &= (b >= lo) & (b <= hi)
    return m


def _mfield(fld, k, D, e, x, o, c, F, atrf, dates):
    """A condition field at watch day k of every pseudo-pick D (entry bar e, decision bar x = e - 1); setuplab's
    Book.field on the stock's own bars."""
    if fld in F:
        return F[fld][x]
    if fld == "gap_pct":
        return (o[e] / c[e - 1] - 1) * 100
    if fld in ("pc_vs_d1", "pc_vs_d1_atr", "prev_intraday", "prev_ret"):
        if k == 1:
            return np.zeros(len(D))
        if fld == "pc_vs_d1":
            return (c[x] / o[D + 1] - 1) * 100
        if fld == "pc_vs_d1_atr":
            return (c[x] / o[D + 1] - 1) / atrf[D]
        if fld == "prev_intraday":
            return (c[x] / o[x] - 1) * 100
        return (c[x] / c[x - 1] - 1) * 100
    if fld == "day":
        return np.full(len(D), float(k))
    if fld == "weekday":
        return pd.DatetimeIndex(np.asarray(dates)[e]).weekday.to_numpy(float)
    raise KeyError("unknown field %s" % fld)


def market_entries(dates, o, c, F, atrf, setups, d_ok):
    """Every first qualifying open of every pseudo-pick of one stock: each own bar d with d_ok[d] is a signal day,
    its watch days are the next five own bars, and setuplab's trigger rule applies (a False condition = not that
    day; unknown with no False = the pseudo-pick stops). F: feature (and feature_change) -> values on the bars
    (blank = no panel row); atrf: ATR14 as a fraction at each bar. -> {setup: unique sorted entry bars}"""
    o, c = np.asarray(o, float), np.asarray(c, float)
    n = len(c)
    D = np.flatnonzero(np.asarray(d_ok, bool)[:max(n - 1, 0)])
    out = {}
    for sid, conds in setups.items():
        done = np.zeros(len(D), bool)
        hit = np.zeros(len(D), np.int64)
        for k in range(1, WATCH + 1):
            e = D + k
            sess = e < n
            ee = np.where(sess, e, n - 1)
            sess &= np.isfinite(o[ee])
            done |= ~sess
            x = ee - 1
            anyF = np.zeros(len(D), bool)
            anyN = np.zeros(len(D), bool)
            with np.errstate(invalid="ignore", divide="ignore"):
                for fld, op, val in conds:
                    a = np.asarray(_mfield(fld, k, D, ee, x, o, c, F, atrf, dates), float)
                    nan = np.isnan(a)
                    r = OPS[op](np.round(np.where(nan, 0, a), 9), round(float(val), 9))
                    anyF |= ~nan & ~r
                    anyN |= nan
            h = ~done & ~anyF & ~anyN
            m = ~done & ~anyF & anyN
            hit[h] = k
            done |= h | m
        out[sid] = np.unique((D + hit)[hit > 0])
    return out


def panel_frame(path, feats, d_from, symbols=None, log=print):
    """The panel's rows from d_from on: symbol, date and the features (lower-case names; read in batches)."""
    import pyarrow.parquet as pq
    pf = pq.ParquetFile(path)
    names = pf.schema_arrow.names
    low = {n.lower(): n for n in names}
    want = list(dict.fromkeys([f.lower() for f in feats] + ["d_atr_pct"]))
    miss = [f for f in want if f not in low]
    if miss:
        raise ValueError("%s lacks %s" % (path, ", ".join(miss)))
    tk = low.get("timestamp", low.get("date"))
    if "symbol" not in low or tk is None:
        raise ValueError("%s needs symbol and timestamp (or date) columns" % path)
    parts = []
    for b in pf.iter_batches(batch_size=400_000, columns=[low["symbol"], tk] + [low[f] for f in want]):
        f = b.to_pandas()
        f.columns = ["symbol", "date"] + want
        t = pd.to_datetime(f["date"])
        if t.dt.tz is not None:
            t = t.dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
        f["date"] = t.dt.normalize().to_numpy().astype("datetime64[D]")
        f = f[f["date"] >= d_from]
        f["symbol"] = f["symbol"].astype(str).str.strip().str.upper()
        if symbols is not None:
            f = f[f["symbol"].isin(symbols)]
        for c in want:
            f[c] = pd.to_numeric(f[c], errors="coerce").astype(np.float64)
        parts.append(f)
    P = pd.concat(parts, ignore_index=True).sort_values(["symbol", "date"], kind="mergesort")
    if P.duplicated(["symbol", "date"]).any():
        raise ValueError("duplicated symbol/date rows in %s" % path)
    P["symbol"] = P["symbol"].astype("category")
    log(" panel: %d rows, %d stocks, %s .. %s" % (len(P), P["symbol"].nunique(), P["date"].min(), P["date"].max()))
    return P.reset_index(drop=True), want


def align_panel(Psym, want, dates):
    """One stock's panel rows on its own bars: feature and feature_change (this row minus the stock's previous
    panel row, as setuplab) -> arrays on the bars; and whether each bar has a panel row."""
    pd_ = Psym["date"].to_numpy().astype("datetime64[D]")
    dates = np.asarray(dates).astype("datetime64[D]")
    pos = np.searchsorted(pd_, dates)
    pos_c = np.minimum(pos, max(len(pd_) - 1, 0))
    have = (pos < len(pd_)) & (pd_[pos_c] == dates) if len(pd_) else np.zeros(len(dates), bool)
    F = {}
    for f in want:
        v = Psym[f].to_numpy(float)
        ch = np.concatenate([[np.nan], np.diff(v)]) if len(v) else v
        F[f] = np.where(have, v[pos_c], np.nan) if len(v) else np.full(len(dates), np.nan)
        F[f + "_change"] = np.where(have, ch[pos_c], np.nan) if len(v) else np.full(len(dates), np.nan)
    return F, have


def market_symbol(dates, o, h, l, c, v, Fsym, have, setups, M, d_from):
    """One stock in the whole-market study: its setups' trades (held 5 sessions: the fresh exit), the zone at the
    close before each entry, and its buy-everything rows (every open it was in the universe the evening before)."""
    dates = np.asarray(dates).astype("datetime64[D]")
    o, c = np.asarray(o, float), np.asarray(c, float)
    n = len(c)
    z = zone_buckets(zone_values(dates, o, h, l, c, v, M))
    atrf = atr_simple(h, l, c)                    # pick_meta's s_atr14 definition, not the panel's Wilder ATR
    d_ok = have & (dates >= d_from)
    ent = market_entries(dates, o, c, Fsym, atrf, setups, d_ok)
    rows = []
    for sid, e in ent.items():
        e = e[e + 4 < n]
        if not len(e):
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            net = (c[e + 4] / o[e] - 1) * 100 - COST
        rows.append(pd.DataFrame({"setup": sid, "day": dates[e], "exit": dates[e + 4], "net": net,
                                  **{d: z[d][e - 1] for d in z}}))
    i = np.arange(1, max(n - 4, 1))
    i = i[(i + 4 < n) & have[i - 1] & (dates[i] >= d_from)] if n > 5 else np.array([], int)
    with np.errstate(invalid="ignore", divide="ignore"):
        bench = (c[i + 4] / o[i] - 1) * 100 - COST if len(i) else np.array([])
    ok = np.isfinite(bench)
    return (pd.concat(rows, ignore_index=True) if rows else None), (dates[i][ok], bench[ok])


# ------------------------------------------------------------------------------------------------- the search
def _years(days):
    days = np.asarray(days).astype("datetime64[D]")
    return max(0.5, float((days.max() - days.min()).astype(int)) / 365.25) if len(days) else 0.5


def zone_screen(di, net, B, nd):
    """Every candidate's trades inside, mean net inside and a quick lower bound (signal days as clusters)."""
    nb = {d[0]: len(d[3]) for d in ZONE_DIMS}

    def stats(S, N):
        n = N.sum()
        if n <= 1:
            return n, np.nan, np.nan
        m = S.sum() / n
        r = S - m * N
        g = int((N > 0).sum())
        se = np.sqrt((r * r).sum() * g / max(g - 1, 1)) / n
        return n, m, m - ZONE_RANK_Z * se

    cube = {}
    for d in nb:
        b = np.where(B[d] < 0, nb[d], B[d]).astype(np.int64)
        cube[d] = b
    res_n, res_m, res_lb = [], [], []
    one = {}
    for d in nb:
        code = di * (nb[d] + 1) + cube[d]
        S = np.bincount(code, weights=net, minlength=nd * (nb[d] + 1)).reshape(nd, nb[d] + 1)
        N = np.bincount(code, minlength=nd * (nb[d] + 1)).reshape(nd, nb[d] + 1).astype(float)
        one[d] = (S, N)
    for dim, lo, hi in ZONE_RANGES:
        S, N = one[dim]
        n, m, lb = stats(S[:, lo:hi + 1].sum(1), N[:, lo:hi + 1].sum(1))
        res_n.append(n), res_m.append(m), res_lb.append(lb)
    dims = [d[0] for d in ZONE_DIMS]
    byd = {}
    for r in ZONE_RANGES:
        byd.setdefault(r[0], []).append(r)
    for i, d1 in enumerate(dims):
        for d2 in dims[i + 1:]:
            n1, n2 = nb[d1] + 1, nb[d2] + 1
            code = (di * n1 + cube[d1]) * n2 + cube[d2]
            S = np.bincount(code, weights=net, minlength=nd * n1 * n2).reshape(nd, n1, n2)
            N = np.bincount(code, minlength=nd * n1 * n2).reshape(nd, n1, n2).astype(float)
            S1 = {r: S[:, r[1]:r[2] + 1, :] for r in byd[d1]}
            N1 = {r: N[:, r[1]:r[2] + 1, :] for r in byd[d1]}
            for r1 in byd[d1]:
                s1, n1_ = S1[r1].sum(1), N1[r1].sum(1)
                for r2 in byd[d2]:
                    n, m, lb = stats(s1[:, r2[1]:r2[2] + 1].sum(1), n1_[:, r2[1]:r2[2] + 1].sum(1))
                    res_n.append(n), res_m.append(m), res_lb.append(lb)
    return np.array(res_n), np.array(res_m), np.array(res_lb)


def _cands():
    singles = [(r,) for r in ZONE_RANGES]
    dims = [d[0] for d in ZONE_DIMS]
    byd = {}
    for r in ZONE_RANGES:
        byd.setdefault(r[0], []).append(r)
    pairs = [(r1, r2) for i, d1 in enumerate(dims) for d2 in dims[i + 1:] for r1 in byd[d1] for r2 in byd[d2]]
    return singles + pairs


ZONE_CANDS = _cands()        # the order zone_screen returns its numbers in


def zone_eval(boot, di, net, chk, m):
    """Inside the zone (m): mean net per trade with its 95% interval, inside minus outside, the check inside."""
    nd = len(boot.days)
    cols = np.column_stack([np.bincount(di[m], weights=net[m], minlength=nd), np.bincount(di[m], minlength=nd),
                            np.bincount(di[~m], weights=net[~m], minlength=nd), np.bincount(di[~m], minlength=nd),
                            np.bincount(di[m], weights=chk[m], minlength=nd)]).astype(float)
    X = boot.M @ cols
    with np.errstate(invalid="ignore", divide="ignore"):
        mi = X[:, 0] / np.where(X[:, 1] > 0, X[:, 1], np.nan)
        mo = X[:, 2] / np.where(X[:, 3] > 0, X[:, 3], np.nan)
        mc = X[:, 4] / np.where(X[:, 1] > 0, X[:, 1], np.nan)
    pc = lambda a: (float(np.nanpercentile(a, 2.5)), float(np.nanpercentile(a, 97.5))) if np.isfinite(a).any() \
        else (np.nan, np.nan)
    n_in, n_out = int(m.sum()), int((~m).sum())
    r = {"n": n_in, "n_out": n_out, "net": float(net[m].mean()) if n_in else np.nan,
         "net_out": float(net[~m].mean()) if n_out else np.nan, "chk": float(chk[m].mean()) if n_in else np.nan}
    r["lo"], r["hi"] = pc(mi)
    r["strict"] = r["net"] - ZONE_RANK_Z * float(np.nanstd(mi)) if n_in else np.nan
    r["diff"] = r["net"] - r["net_out"] if n_in and n_out else np.nan
    r["diff_lo"], r["diff_hi"] = pc(mi - mo) if n_in and n_out else (np.nan, np.nan)
    r["chk_lo"], r["chk_hi"] = pc(mc)
    return r


def _pop(name, days, exits, net, chk, B):
    days = np.asarray(days).astype("datetime64[D]")
    return {"name": name, "days": days, "exit": np.asarray(exits).astype("datetime64[D]"),
            "net": np.asarray(net, float), "chk": np.asarray(chk, float), "B": {k: np.asarray(v) for k, v in B.items()}}


def _zsub(p, m):
    return {"name": p["name"], "days": p["days"][m], "exit": p["exit"][m], "net": p["net"][m], "chk": p["chk"][m],
            "B": {k: v[m] for k, v in p["B"].items()}}


def choose_zone(pops, min_per_year=ZONE_MIN_PER_YEAR, finalists=ZONE_FINALISTS):
    """The declared rule on populations (each: days, net, chk, buckets). -> (zone or None, {pop: eval} of the
    winner, finalists table, {pop: eval} of the setup alone)."""
    prep = []
    for p in pops:
        if len(p["net"]) < 30:
            return None, {}, pd.DataFrame(), {}
        boot = Boot(p["days"])
        di = np.searchsorted(boot.days, p["days"])
        prep.append((p, boot, di, min_per_year * _years(p["days"])))
    base = {p["name"]: zone_eval(b, di, p["net"], p["chk"], np.ones(len(di), bool)) for p, b, di, _ in prep}
    scr = [zone_screen(di, p["net"], p["B"], len(b.days)) for p, b, di, _ in prep]
    elig = np.all([s[0] >= mn for s, (_, _, _, mn) in zip(scr, prep)], axis=0)
    score = np.min([s[2] for s in scr], axis=0)
    base_lb = min(base[p["name"]]["lo"] for p, _, _, _ in prep)
    ok = elig & np.isfinite(score)
    order = [int(i) for i in np.argsort(-np.where(ok, score, -np.inf)) if ok[i]][:finalists]
    rows = []
    best, best_key = None, None
    for i in order:
        z = ZONE_CANDS[i]
        ev = {}
        for p, b, di, mn in prep:
            ev[p["name"]] = zone_eval(b, di, p["net"], p["chk"], zone_mask(z, p["B"]))
        qual = all(e["n"] >= mn and e["diff_lo"] > 0 and e["chk_lo"] > 0 for e, (_, _, _, mn) in
                   zip(ev.values(), prep))
        sc = min(e["strict"] for e in ev.values())
        row = {"zone": zone_key(z), "text": zone_text(z), "qualifies": bool(qual), "score": sc,
               "screen": float(score[i])}
        for nm, e in ev.items():
            row.update({"%s_%s" % (nm, k): v for k, v in e.items()})
        rows.append(row)
        key = (sc, sum(e["n"] for e in ev.values()))
        if qual and (best is None or key > best_key):
            best, best_key = (z, ev), key
    T = pd.DataFrame(rows)
    if len(T):
        T = T.sort_values(["qualifies", "score"], ascending=[False, False]).reset_index(drop=True)
    if best is None:
        return None, {}, T, base
    return best[0], best[1], T, base


def walk_forward(pops, years=ZONE_WF_YEARS, min_per_year=ZONE_MIN_PER_YEAR):
    """The search replayed: for each year, choose with the trades that had exited before 1 Jan, judge on that year.
    -> (rows by year, {pop: pooled inside minus outside with its 95% interval and the verdict})"""
    rows, pool = [], {p["name"]: [] for p in pops}
    for Y in years:
        cut, nxt = np.datetime64("%d-01-01" % Y), np.datetime64("%d-01-01" % (Y + 1))
        train = [_zsub(p, p["exit"] < cut) for p in pops]
        test = [_zsub(p, (p["days"] >= cut) & (p["days"] < nxt)) for p in pops]
        if any(len(t["net"]) < 30 for t in train) or any(len(t["net"]) == 0 for t in test):
            rows.append({"year": Y, "zone": "", "text": "too few trades to choose", "chosen": False})
            continue
        z, _, _, _ = choose_zone(train, min_per_year)
        row = {"year": Y, "zone": zone_key(z), "text": zone_text(z), "chosen": z is not None}
        for t in test:
            row["%s_n" % t["name"]] = len(t["net"])
            row["%s_net_all" % t["name"]] = float(t["net"].mean())
            if z is not None:
                m = zone_mask(z, t["B"])
                row["%s_n_in" % t["name"]] = int(m.sum())
                row["%s_net_in" % t["name"]] = float(t["net"][m].mean()) if m.any() else np.nan
                row["%s_net_out" % t["name"]] = float(t["net"][~m].mean()) if (~m).any() else np.nan
                pool[t["name"]].append((t["days"], t["net"], m))
        rows.append(row)
    res = {}
    for nm, parts in pool.items():
        if not parts:
            res[nm] = {"years": 0, "verdict": "NO ZONE CHOSEN"}
            continue
        d = np.concatenate([x[0] for x in parts])
        v = np.concatenate([x[1] for x in parts])
        m = np.concatenate([x[2] for x in parts])
        if not m.any() or m.all():
            res[nm] = {"years": len(parts), "n_in": int(m.sum()), "verdict": "NOT SHOWN"}
            continue
        boot = Boot(d)
        e = zone_eval(boot, np.searchsorted(boot.days, d), v, v, m)
        verdict = "HOLDS" if e["diff_lo"] > 0 else ("WORSE" if e["diff_hi"] < 0 else "NOT SHOWN")
        res[nm] = {"years": len(parts), "n_in": e["n"], "n_out": e["n_out"], "net_in": e["net"],
                   "net_out": e["net_out"], "diff": e["diff"], "diff_lo": e["diff_lo"], "diff_hi": e["diff_hi"],
                   "verdict": verdict}
    return pd.DataFrame(rows), res


# ------------------------------------------------------------------------------------------------- the zones command
def read_hashed_run(folder, files):
    """A run folder's files, refused when one does not match its outputs.sha256."""
    folder = Path(folder)
    rec = {}
    hf = folder / "outputs.sha256"
    if hf.is_file():
        for ln in hf.read_text(encoding="utf-8").splitlines():
            parts = ln.split("  ", 1)
            if len(parts) == 2:
                rec[parts[1].strip()] = parts[0].strip()
    for f in files:
        h = hashlib.sha256((folder / f).read_bytes()).hexdigest()
        if rec.get(f) != h:
            raise ValueError("%s does not match %s - refusing" % (folder / f, hf))
    return rec


def latest_run(base, prefix, need):
    runs = sorted(p for p in (Path(base) / prefix).glob(prefix + "_*") if all((p / f).is_file() for f in need))
    return runs[-1] if runs else None


def picks_zone_table(doc, tags_dir, ohlcv, M, log=print):
    """Every tagged setup entry of D and ENS with its net at the primary exit, the lift over the model's D1 entry on
    the same pick, and the zone at the close before its entry."""
    read_hashed_run(tags_dir, ["setup_tags.parquet", "setup_trades.parquet"])
    L = pd.read_parquet(Path(tags_dir) / "setup_trades.parquet")
    W = pd.read_parquet(Path(tags_dir) / "setup_tags.parquet")[["trade_id", "d1_net_d5", "d1_net_fresh"]]
    L = L.merge(W[["trade_id"] + [c for c in ("d1_net_d5", "d1_net_fresh") if c not in L.columns]], on="trade_id",
                how="left")
    pe = {s["id"]: s["primary_exit"] for s in doc["setups"]}
    d5 = L["setup"].map(pe).eq("original_d5").to_numpy()
    L["net"] = np.where(d5, L["net_d5"], L["net_fresh"])
    L["chk"] = L["net"] - np.where(d5, L["d1_net_d5"], L["d1_net_fresh"])
    L["day"] = pd.to_datetime(L["entry_date"]).to_numpy().astype("datetime64[D]")
    L["exit"] = pd.to_datetime(np.where(d5, L["exit_d5_date"], L["exit_fresh_date"])).to_numpy().astype("datetime64[D]")
    for d in ZDIM:
        L[d] = np.int8(-1)
    syms = sorted(L["symbol"].astype(str).unique())
    found = 0
    for i in range(0, len(syms), 100):
        bars = ohlcv(syms[i:i + 100])
        for s, (dates, o, h, l, c, v) in bars.items():
            dates = np.asarray(dates).astype("datetime64[D]")
            z = zone_buckets(zone_values(dates, o, h, l, c, v, M))
            rows = np.flatnonzero(L["symbol"].to_numpy() == s)
            j = np.searchsorted(dates, L["day"].to_numpy()[rows])
            ok = (j > 0) & (j < len(dates))
            ok[ok] &= dates[j[ok]] == L["day"].to_numpy()[rows][ok]
            for d in z:
                col = L[d].to_numpy(copy=True)
                col[rows[ok]] = z[d][j[ok] - 1]
                L[d] = col
            found += int(ok.sum())
    keep = np.isfinite(L["net"].to_numpy(float)) & np.isfinite(L["chk"].to_numpy(float)) & ~pd.isna(L["exit"])
    log(" picks: %d setup entries of %d picks (%d settled); the zone at the close before the entry found for %d" % (
        len(L), L["trade_id"].nunique(), int(keep.sum()), found))
    return L[keep].reset_index(drop=True)


def market_zone_table(doc, setups, panel_path, ohlcv, forget, M, log=print, d_from=MARKET_FROM, symbols=None):
    """The whole market: every stock-day in the panel from d_from as a pseudo-pick, each setup's trades held 5
    sessions, their zones, and the excess over buying every stock at the same open (same hold)."""
    feats = frozen_features(doc)
    P, want = panel_frame(panel_path, feats, d_from - np.timedelta64(400, "D"), symbols, log)
    idx = P.groupby("symbol", sort=False, observed=True).indices
    syms = sorted(idx)
    trades, bdays, bvals, done = [], [], [], 0
    for i in range(0, len(syms), 100):
        chunk = syms[i:i + 100]
        bars = ohlcv(chunk)
        for s in chunk:
            if s not in bars:
                continue
            dates, o, h, l, c, v = bars[s]
            dates = np.asarray(dates).astype("datetime64[D]")
            F, have = align_panel(P.iloc[idx[s]], want, dates)
            T, (bd, bv) = market_symbol(dates, o, h, l, c, v, F, have, setups, M, d_from)
            if T is not None:
                T.insert(0, "symbol", s)
                trades.append(T)
            bdays.append(bd)
            bvals.append(bv)
            done += 1
        forget(chunk)
        log(" market: %d of %d stocks" % (min(i + 100, len(syms)), len(syms)))
    if not trades:
        raise ValueError("no setup ever entered in the whole market - check the panel and the bars")
    T = pd.concat(trades, ignore_index=True)
    b = pd.Series(np.concatenate(bvals)).groupby(np.concatenate(bdays)).mean()
    T["bench"] = b.reindex(pd.DatetimeIndex(T["day"].to_numpy())).to_numpy(float)
    T["chk"] = T["net"] - T["bench"]
    log(" market: %d stocks, %d setup trades (%s)" % (done, len(T), ", ".join(
        "%s %d" % (k, v) for k, v in T["setup"].value_counts().reindex([s["id"] for s in doc["setups"]]).fillna(0)
        .astype(int).items())))
    return T, b


def pops_of(T, names, col="pop"):
    out = []
    for nm in names:
        S = T[T[col] == nm] if col in T.columns else T
        out.append(_pop(nm, S["day"], S["exit"], S["net"], S["chk"], {d: S[d].to_numpy() for d in ZDIM}))
    return out


def rupees(net, per_year):
    """Rs a year at Rs 1 lakh a trade: net % x trades a year x Rs 1,000."""
    return net * per_year * 1000.0 if np.isfinite(net) else np.nan


def zone_section(sid, name, part, pops, zone, ev, base, T, wf, wfres, chk_name):
    yrs = {p["name"]: _years(p["days"]) for p in pops}
    fm = lambda x, nd=2: "" if x is None or not np.isfinite(x) else ("%+.*f" % (nd, x))
    L = ["### %s - %s" % (part, "the zone: " + zone_text(zone) if zone else "no zone qualified"), "",
         "| | " + " | ".join("%s trades/yr | %s net %% per trade [95%%] | %s Rs a year at Rs 1 L a trade | %s %s [95%%]"
                             % (n, n, n, n, chk_name) for n in yrs) + " |",
         "|---|" + "---:|" * (4 * len(yrs))]

    def line(label, e, n_key="n"):
        cells = []
        for nm in yrs:
            x = e.get(nm)
            if not x:
                cells += ["", "", "", ""]
                continue
            py = x[n_key] / yrs[nm]
            cells += ["%.0f" % py, "%s [%s, %s]" % (fm(x["net"]), fm(x["lo"]), fm(x["hi"])),
                      "{:,.0f}".format(rupees(x["net"], py)), "%s [%s, %s]" % (fm(x["chk"]), fm(x["chk_lo"]),
                                                                              fm(x["chk_hi"]))]
        return "| %s | %s |" % (label, " | ".join(cells))
    L.append(line("the setup alone", base))
    if zone:
        L.append(line("inside the zone", ev))
        L.append("| outside the zone | " + " | ".join(
            "%.0f | %s | %s | " % (ev[nm]["n_out"] / yrs[nm], fm(ev[nm]["net_out"]),
                                   "{:,.0f}".format(rupees(ev[nm]["net_out"], ev[nm]["n_out"] / yrs[nm])))
            for nm in yrs) + "|")
        L += ["", "Inside minus outside (net %% per trade): %s." % "; ".join(
            "%s %s [%s, %s]" % (nm, fm(ev[nm]["diff"]), fm(ev[nm]["diff_lo"]), fm(ev[nm]["diff_hi"])) for nm in yrs)]
    q = int(T["qualifies"].sum()) if len(T) else 0
    L += ["", "Candidates tested: %d; finalists bootstrapped: %d; qualifying: %d." % (len(ZONE_CANDS), len(T), q), "",
          "**Out of sample (the search replayed year by year):** " + "; ".join(
              "%s %s%s" % (nm, r["verdict"], (" - inside %s vs outside %s, inside minus outside %s [%s, %s], %d "
                                               "years with a zone" % (fm(r["net_in"]), fm(r["net_out"]),
                                                                      fm(r["diff"]), fm(r["diff_lo"]),
                                                                      fm(r["diff_hi"]), r["years"]))
                                              if "diff" in r else "") for nm, r in wfres.items()), "",
          "| year | zone chosen with exits before 1 Jan | " + " | ".join(
              "%s trades | %s in zone | %s net in zone | %s net all" % (n, n, n, n) for n in yrs) + " |",
          "|---|---|" + "---:|" * (4 * len(yrs))]
    for r in wf.to_dict("records"):
        cells = []
        for nm in yrs:
            cells += [str(int(r["%s_n" % nm])) if np.isfinite(r.get("%s_n" % nm, np.nan)) else "",
                      str(int(r["%s_n_in" % nm])) if np.isfinite(r.get("%s_n_in" % nm, np.nan)) else "",
                      fm(r.get("%s_net_in" % nm, np.nan)), fm(r.get("%s_net_all" % nm, np.nan))]
        L.append("| %s | %s | %s |" % (r["year"], r["text"] if r.get("chosen") else "none (%s)" % r["text"],
                                       " | ".join(cells)))
    return L


def _clean(x):
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if not np.isfinite(x) else round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def zones_hash(doc):
    return hashlib.sha256(_canon_json({k: v for k, v in doc.items() if k != "sha256"}).encode()).hexdigest()


def load_zones(base):
    """The newest zones run's SETUP_ZONES.json (hash-checked) -> (folder, doc) or (None, None)."""
    run = latest_run(base, "ZONES", [ZONES_FILE])
    if run is None:
        return None, None
    doc = json.loads((run / ZONES_FILE).read_text(encoding="utf-8"))
    if doc.get("sha256") != zones_hash(doc):
        raise ValueError("%s was changed after it was written - refusing (rerun setuplab zones)" % (run / ZONES_FILE))
    return run, doc


def pine_code(doc_z, ids):
    return PINE_CODE_TAG + "|" + "|".join("%s=%s" % (s, (doc_z["setups"][s]["market"] or {}).get("zone", ""))
                                          for s in ids)


def cmd_zones(a, log=print, data=None):
    fp, doc = load_frozen(a.frozen or None)
    conds = frozen_conds(doc)
    ids = [s["id"] for s in doc["setups"]]
    out = Path(a.out)
    tags = latest_run(out, "TAGS", ["setup_tags.parquet", "setup_trades.parquet"])
    if tags is None:
        print("REFUSED: no TAGS run under %s - run setuplab tag first" % (out / "TAGS"))
        return 3
    t0 = time.time()
    if data is None:
        data = LiveData(a.root, a.stage_e_any, panel=None)
    log("%s zones: freeze %s (sha256 %s); tags %s; panel %s" % (VERSION, fp.name, doc["sha256"][:16], tags.name,
                                                                  a.features))
    idx = data.index_closes(dict(ZONE_INDEX))
    M = market_dims(idx)
    LT = picks_zone_table(doc, tags, data.ohlcv, M, log)
    LT["pop"] = LT["engine"].astype(str)
    atr_line = "not checked (give --data <watchlist folder>)"
    if getattr(a, "data", None) and (Path(a.data) / "watchlist.parquet").is_file():
        WL = pd.read_parquet(Path(a.data) / "watchlist.parquet", columns=["symbol", "signal_day", "s_atr14"])
        WL["d"] = pd.to_datetime(WL["signal_day"]).to_numpy().astype("datetime64[D]")
        got, n_ok, n = [], 0, 0
        syms = sorted(WL["symbol"].astype(str).unique())
        for i in range(0, len(syms), 100):
            for s_, (dates, o, h, l, c, v) in data.ohlcv(syms[i:i + 100]).items():
                dates = np.asarray(dates).astype("datetime64[D]")
                g = WL[WL["symbol"] == s_]
                j = np.searchsorted(dates, g["d"].to_numpy())
                okj = (j < len(dates))
                okj[okj] &= dates[j[okj]] == g["d"].to_numpy()[okj]
                sa = atr_simple(h, l, c)
                x = g["s_atr14"].to_numpy(float)[okj]
                y = sa[j[okj]]
                m = np.isfinite(x) & np.isfinite(y)
                n += int(m.sum())
                n_ok += int((np.abs(x[m] - y[m]) < 1e-6).sum())
            data.forget(syms[i:i + 100])
        share = n_ok / n if n else np.nan
        atr_line = "%d of %d picks: pick_meta's s_atr14 = the simple ATR14 / close from the bars (within 1e-6)%s" % (
            n_ok, n, "" if share >= 0.99 else " - WARNING: below 99%: the whole market's and the chart's S1 use a "
                                              "different ATR from the picks' S1; send ZONES.md")
        log(" ATR check: " + atr_line)
    MT = None
    if not a.picks_only:
        MT, _ = market_zone_table(doc, conds, a.features, data.ohlcv, data.forget, M, log)
    run = new_run_dir(out / "ZONES", "ZONES")
    res = {"atr_check": atr_line, "file": ZONES_FILE, "tool": VERSION, "made_at": _dt.datetime.now(IST).isoformat(timespec="seconds"),
           "rule": ZONE_RULE, "dims": [list(d) for d in ZONE_DIMS], "freeze_sha256": doc["sha256"],
           "tags_run": tags.name, "panel": str(a.features), "whole_market": MT is not None, "setups": {}}
    md = ["# Setup zones - %s (%s)" % (time.strftime("%d %b %Y"), VERSION), "",
          "Freeze %s (sha256 %s); tags %s; whole market: %s." % (
              fp.name, doc["sha256"][:16], tags.name,
              "every stock-day in %s from %s (held 5 sessions)" % (a.features, MARKET_FROM) if MT is not None
              else "not run (--picks-only)"), "",
          "**The rule (declared before any zone result):** " + ZONE_RULE, "",
          "**ATR check** (S1's 1-ATR dip; the whole market and the chart compute the ATR themselves): " + atr_line, "",
          "Money: Rs a year at Rs 1 L a trade = net %% per trade x trades a year x Rs 1,000 (one position of Rs 1 L per "
          "trade, no compounding, skipped trades in cash).", "", "## Verdicts", "",
          "| setup | picks: zone | picks: out of sample (D / ENS) | whole market: zone | whole market: out of sample |",
          "|---|---|---|---|---|"]
    body, fin_all, wf_all = [], [], []
    for s in doc["setups"]:
        sid = s["id"]
        r = {"name": s["name"], "primary_exit": s["primary_exit"]}
        body += ["", "## %s - %s" % (sid, s["name"]), ""]
        parts = [("picks", pops_of(LT[LT["setup"] == sid], ["D", "ENS"]), "lift over D1")]
        if MT is not None:
            S = MT[MT["setup"] == sid]
            parts.append(("market", [_pop("MKT", S["day"], S["exit"], S["net"], S["chk"],
                                          {d: S[d].to_numpy() for d in ZDIM})], "excess"))
        for part, pops, chk in parts:
            z, ev, T, base = choose_zone(pops)
            wf, wfres = walk_forward(pops)
            T.insert(0, "part", part), T.insert(0, "setup", sid)
            wf.insert(0, "part", part), wf.insert(0, "setup", sid)
            fin_all.append(T), wf_all.append(wf)
            r[part] = _clean({"zone": zone_key(z), "text": zone_text(z), "inside": ev, "alone": base,
                              "out_of_sample": wfres,
                              "holds": bool(z is not None and all(v["verdict"] == "HOLDS" for v in wfres.values()))})
            if not base:
                body += ["### %s - too few trades" % part, ""]
                continue
            body += zone_section(sid, s["name"], "Picks (D and ENS, primary exit %s)" % s["primary_exit"]
                                 if part == "picks" else "Whole market (every stock, held 5 sessions)",
                                 pops, z, ev, base, T, wf, wfres, chk) + [""]
        if MT is None:
            r["market"] = None
        res["setups"][sid] = r
        vv = lambda p: "" if not r.get(p) else " / ".join(x["verdict"] for x in r[p]["out_of_sample"].values())
        md.append("| %s | %s | %s | %s | %s |" % (
            sid, (r["picks"] or {}).get("text", ""), vv("picks"),
            (r["market"] or {}).get("text", "not run") if r.get("market") is not None else "not run", vv("market")))
    md += ["", "HOLDS = inside beat outside out of sample (95%). NOT SHOWN = it did not. A zone is a hypothesis "
               "until the forward record (ON TIME scans) confirms it; the nightly scan marks every setup IN ZONE or "
               "OUTSIDE and the forward record keeps both."] + body
    res["pine_code"] = pine_code(res, ids)
    res["sha256"] = zones_hash(res)
    (run / ZONES_FILE).write_text(json.dumps(res, indent=1), encoding="utf-8")
    (run / "ZONES.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (run / "PINE_ZONE_CODE.txt").write_text(res["pine_code"] + "\n", encoding="ascii")
    pd.concat(fin_all, ignore_index=True).to_csv(run / "zone_finalists.csv", index=False)
    pd.concat(wf_all, ignore_index=True).to_csv(run / "walk_forward.csv", index=False)
    LT.drop(columns=["pop"]).to_parquet(run / "picks_zone_trades.parquet", index=False)
    names = [ZONES_FILE, "ZONES.md", "PINE_ZONE_CODE.txt", "zone_finalists.csv", "walk_forward.csv",
             "picks_zone_trades.parquet"]
    if MT is not None:
        MT.to_parquet(run / "market_zone_trades.parquet", index=False)
        names.append("market_zone_trades.parquet")
    write_hashes(run, names)
    for sid, r in res["setups"].items():
        for part in ("picks", "market"):
            if r.get(part):
                log(" %s %-6s %s%s" % (sid, part, r[part]["text"], "  (out of sample: %s)" % " / ".join(
                    v["verdict"] for v in r[part]["out_of_sample"].values())))
    log(" pine code: %s" % res["pine_code"])
    log("ZONES WRITTEN -> %s (%.1f min)" % (run, (time.time() - t0) / 60))
    return 0


# ======================================================================================== v0.9: runners (no dip)
RUN_FILE = "RUNNER_CANDIDATES.json"
RUN_DIP = 2.0                 # % - a close this far below the D1 open is a dip (Karan, 8 Nov: a close 2% below)
RUN_RT = 5.0                  # % - the D5 close this far above the D1 open = the right tail (10% also measured)
RUN_RT2 = 10.0
RUN_MIN_PER_YEAR = 25         # trades a year a rule must keep in each engine
RUN_MAX_BAD_YEARS = 2         # years with net <= 0 a rule may have
RUN_FINALISTS = 60            # the best by the quick screen get the full block bootstrap
RUN_TRIPLE_PAIRS = 150        # the best pairs that get a third (rank / agreement / weekday / context / gap) condition
RUN_TOP = 5
RUN_OVERLAP = 0.70
RUN_Z = 1.96
RUN_WF_YEARS = (2022, 2023, 2024, 2025, 2026)
RUN_WF_MIN = 300              # picks a training window needs in each engine
RUN_ALIGN_TOL = 1e-4          # a pick's own bars must give the watchlist's D1-D5 closes (relative difference)
RUN_MONEY_FROM = np.datetime64("2022-01-01")
RUN_CAPITAL = 5e5             # Rs 5 L
RUN_SLOTS = (2, 3, 5, 7)
RUN_MTF_DAY = 0.0004          # Zerodha MTF: 0.04% a day on the borrowed amount
RUN_STOP_BUF = 0.0005         # the breakout buy-stop sits 0.05% above the signal-day high
RUN_STRONG = 0.7              # a strong D1: green and the close in the top 30% of the day's range
RUN_ANAT_B = 200              # day-block resamples for the AUC's standard deviation
RUN_RULE = (
    "runners v1, declared 8 Nov 2026 before any result on real picks. Karan: find which model picks will NOT dip and "
    "buy them at the model's open or on an event; 5-7 quality trades a week together with the dip setups; don't be "
    "conservative. PICKS: engines D and ENS, ranks 1-10, bought at the D1 open (the model's own price), sold at the "
    "D5 close, 0.35 pp costs; a pick whose own daily bars do not give the watchlist's D1-D5 closes is left out "
    "(counted). DIP = a close on D1-D4 at least 2% below the D1 open (Karan's choice: the closes a dip setup acts "
    "on); also measured: the intraday low 2% below on D1-D5, and a close 1 ATR below. RIGHT TAIL = the D5 close 5% "
    "or more above the D1 open (10% also shown). RUNNER = no dip and the right tail. A RULE = one to three "
    "conditions known at the signal close (a feature rose / fell on the signal day; a zone range at the signal "
    "close; the model's rank; the other engine picking it too; the weekday of D1; the market context and the "
    "stock's state at the pick) or at the D1 open (the gap, seen in the pre-open); it buys every pick it selects at "
    "the D1 open. SEARCH, in both engines: every single condition, every pair from different families, and the 150 "
    "best pairs with one more rank / agreement / weekday / context / gap condition; the 60 best by a quick 95% lower "
    "bound (day-clustered) get the full block bootstrap. A rule QUALIFIES when, in both engines: 25 or more trades a "
    "year; net per trade 95% interval above 0; its lift over every pick of the same days (net minus that day's mean "
    "over all the engine's picks) 95% interval above 0; net <= 0 in at most 2 of its years; EVERY CONDITION EARNS ITS "
    "PLACE: the rule's net per trade minus the net of the trades its simpler version (that condition dropped) adds, "
    "95% interval above 0 (the quick screen applies the same test before the bootstrap, so a narrower rule never "
    "displaces the simpler one, with more trades, by luck). Score = the lower 95% bound of net per trade in the "
    "weaker engine. CANDIDATES for the forward paper test = the top 5 qualifiers that "
    "are not versions of each other (one's conditions within the other's, or 70% of the same D trades); the best 5 "
    "by score are listed too, qualified or not. Plain 95% per rule (don't be conservative): some rules pass by luck, "
    "so the whole search is replayed year by year 2022-2026 - choose the candidates with the picks whose D5 exit was "
    "before 1 January, judge their picks (each pick once) on that year: HOLDS when the pooled lift over all picks is "
    "above 0 out of sample (95%), WORSE when below, else NOT SHOWN. EVENTS on the candidates' picks and on all "
    "picks, each against the D1 open on the same picks: the breakout (a buy-stop 0.05% above the signal-day high, "
    "live on D1 and D2), the D2 open after a strong D1 (green, the close in the top 30% of its range), the D1 close "
    "after a strong D1. MONEY: Rs 5 L in 2 / 3 / 5 / 7 equal slots, profits reinvested, no MTF and MTF 2x (0.04% a "
    "day on the borrowed half), entries from 2022, one position per pick (its earliest entry); the dip arm = the "
    "frozen setups' trades in the newest ZONES run, IN or OUT of their picks zone; the same open: the source with "
    "the higher net per trade first, then the model's rank.")
CTX_ATOMS = (
    ("BULLSTATE", "pre_state_bullish", ">", 0.5, "state", "a bullish stock state at the pick (S01-S03)"),
    ("BEARSTATE", "pre_state_bearish", ">", 0.5, "state", "a bearish stock state at the pick (S08/S09)"),
    ("NIFTY_UP", "pre_nifty_vs_ma50", ">", 0.0, "nifty", "NIFTY above its 50-day average"),
    ("NIFTY_DN", "pre_nifty_vs_ma50", "<", 0.0, "nifty", "NIFTY below its 50-day average"),
    ("MKT_BULL", "pre_env_code", "<=", 1.0, "env", "a bullish market (tl_context: broad or narrow bullish)"),
    ("MKT_BEAR", "pre_env_code", ">=", 3.0, "env", "a bearish market (tl_context: broad bearish / high stress)"),
    ("VIX_LOW", "pre_vix_pct250", "<", 0.5, "vix", "India VIX in the lower half of its last year"),
    ("VIX_HIGH", "pre_vix_pct250", ">=", 0.5, "vix", "India VIX in the upper half of its last year"),
    ("BREADTH_UP", "pre_ad_ratio_10", ">=", 0.5, "breadth", "more stocks rising than falling over 10 days"),
    ("BREADTH_DN", "pre_ad_ratio_10", "<", 0.5, "breadth", "more stocks falling than rising over 10 days"),
    ("NOT_OVEREXT", "pre_state_overextended", "<", 0.5, "overext", "not overextended at the pick"),
    ("VOL_ELEV", "pre_state_vol_elevated", ">", 0.5, "volstate", "volatility elevated at the pick"))
RUN_CTX_GROUPS = {"rank", "agree", "weekday", "gap", "state", "nifty", "env", "vix", "breadth", "overext", "volstate"}
RUN_OPS = dict(OPS, **{"==": np.equal})
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
EVENT_WORDS = {"E0": "D1 open (the model's own buy; AMO / pre-open)",
               "E1": "breakout: buy-stop 0.05% above the signal-day high, live D1-D2 (GTT)",
               "E2": "D2 open after a strong D1 (green, close in the top 30% of its range; AMO)",
               "E3": "D1 close after a strong D1 (at the screen about 15:20)"}


def _bci(boot, days, vals):
    """The 95% block-bootstrap interval of a mean (days: among the boot's days)."""
    return boot.ci_idx(np.searchsorted(boot.days, np.asarray(days)), np.asarray(vals, float))


def run_bars(book, ohlcv, forget, M, before=0):
    """Per pick, from the stock's own daily bars: opens / highs / lows / closes of D-before..D5 (D0 = the signal day,
    Dk = its k-th own bar after it; column k + before) and every zone value at the D0 close."""
    n = book.n
    H, L, Cb, Ob = (np.full((n, 6 + before), np.nan) for _ in range(4))
    Z = {d[0]: np.full(n, np.nan) for d in ZONE_DIMS}
    sd = np.asarray(book.signal_day).astype("datetime64[D]")
    rows_of = pd.Series(np.arange(n)).groupby(book.symbols).indices
    syms = sorted(rows_of)
    for i in range(0, len(syms), 100):
        part = syms[i:i + 100]
        for s_, (dates, o, h, l, c, v) in ohlcv(part).items():
            rows = np.asarray(rows_of.get(s_, []), dtype=np.int64)
            dates = np.asarray(dates).astype("datetime64[D]")
            if not len(rows) or not len(dates):
                continue
            j = np.searchsorted(dates, sd[rows])
            ok = j < len(dates)
            ok[ok] &= dates[j[ok]] == sd[rows][ok]
            rows, j = rows[ok], j[ok]
            if not len(rows):
                continue
            o, h, l, c = (np.asarray(x, float) for x in (o, h, l, c))
            for k in range(-before, 6):
                v_ = (j + k >= 0) & (j + k < len(dates))
                jj, cc = j[v_] + k, k + before
                H[rows[v_], cc], L[rows[v_], cc], Cb[rows[v_], cc], Ob[rows[v_], cc] = h[jj], l[jj], c[jj], o[jj]
            if M is not None:
                z = zone_values(dates, o, h, l, c, v, M)
                for dn in Z:
                    Z[dn][rows] = z[dn][j]
        forget(part)
    return {"H": H, "L": L, "Cb": Cb, "Ob": Ob, "Z": Z, "before": before}


def runner_labels(O1, C, H, L, atr):
    """C / H / L: (n, 6), column k = Dk (0 = the signal day), all finite. -> the labels and outcomes."""
    lo4 = C[:, 1:5].min(1)
    r = C[:, 5] / O1 - 1
    fa = np.isfinite(atr)
    out = {"dip": lo4 <= O1 * (1 - RUN_DIP / 100), "dip_low": L[:, 1:6].min(1) <= O1 * (1 - RUN_DIP / 100),
           "dip_atr": fa & (lo4 <= O1 * (1 - np.where(fa, atr, 0.0))),
           "rt5": r * 100 >= RUN_RT, "rt10": r * 100 >= RUN_RT2, "net": r * 100 - COST,
           "mfe": (H[:, 1:6].max(1) / O1 - 1) * 100, "mae": (L[:, 1:6].min(1) / O1 - 1) * 100}
    out["runner"] = ~out["dip"] & out["rt5"]
    return out


def run_sub(P, m):
    """The same table for some picks (the day index is rebuilt by run_index)."""
    out = {}
    for k, v in P.items():
        if k in ("days", "counts"):
            out[k] = v
        elif isinstance(v, dict):
            out[k] = {kk: (vv[m] if isinstance(vv, np.ndarray) and len(vv) == len(m) else vv) for kk, vv in v.items()}
        elif isinstance(v, np.ndarray) and v.ndim and len(v) == len(m):
            out[k] = v[m]
        else:
            out[k] = v
    return out


def run_index(P):
    """Day index, the lift (net minus the day's mean net over every pick of the table), years."""
    P["days"] = np.unique(P["day"])
    P["di"] = np.searchsorted(P["days"], P["day"])
    nd = len(P["days"])
    s = np.bincount(P["di"], weights=P["net"], minlength=nd)
    c = np.bincount(P["di"], minlength=nd)
    P["lift"] = P["net"] - (s / np.maximum(c, 1))[P["di"]]
    P["year"] = pd.DatetimeIndex(P["day"]).year.to_numpy()
    P["years"] = _years(P["day"])
    return P


def runner_table(book, bars, others, name):
    """Every complete pick of one engine (book: that engine's picks; bars: their rows of run_bars): the labels, the
    net, the lift and every condition field. others: {(signal day, symbol): the other engine's rank}."""
    C = np.column_stack([book.sc] + [book.C[:, k] for k in range(1, 6)])
    O1 = book.O[:, 1]
    b0 = int(bars.get("before", 0))
    with np.errstate(invalid="ignore", divide="ignore"):
        scale = book.sc / bars["Cb"][:, b0]          # a later price adjustment in the cache scales a stock's bars
        Hx, Lx, Cx = (bars[k] * scale[:, None] for k in ("H", "L", "Cb"))
        H, L, Cb = (x[:, b0:b0 + 6] for x in (Hx, Lx, Cx))
        dev = np.abs(Cb[:, 1:6] / C[:, 1:6] - 1)
        have = np.isfinite(Cb).all(1) & np.isfinite(H).all(1) & np.isfinite(L).all(1)
        aligned = have & np.isfinite(dev).all(1) & (np.where(np.isfinite(dev), dev, 1.0) <= RUN_ALIGN_TOL).all(1)
        scaled = aligned & (np.abs(np.where(np.isfinite(scale), scale, 1.0) - 1) > 1e-6)
    keep = book.ok & aligned & np.isfinite(O1) & np.isfinite(book.O[:, 2]) & np.isfinite(C).all(1)
    cal = np.asarray(book.cal).astype("datetime64[D]")
    sd = np.asarray(book.signal_day).astype("datetime64[D]")
    P = {"name": name, "ids": book.ids, "symbols": book.symbols, "day": sd, "d1": cal[book.i1],
         "d5": cal[np.minimum(book.i1 + 4, len(cal) - 1)], "ent": book.i1.astype(np.int64),
         "ex": (book.i1 + 4).astype(np.int64), "rank": book.rank.astype(float), "atr": book.atr, "O": book.O, "C": C,
         "H": H, "L": L, "gap_d1": (O1 / book.sc - 1) * 100,
         "weekday_d1": pd.DatetimeIndex(cal[book.i1]).weekday.to_numpy().astype(float)}
    o_rank = np.array([others.get((d, s), np.nan) for d, s in zip(sd, book.symbols)], float)
    fo = np.isfinite(o_rank)
    P["agree"] = fo.astype(float)
    P["agree3"] = (fo & (np.where(fo, o_rank, 99) <= 3) & (book.rank <= 3)).astype(float)
    P["fc"] = {f: book.F[f + "_change"][:, 1] for f in book.features if f + "_change" in book.F}
    P["fv"] = {f: book.F[f][:, 1] for f in book.features if f in book.F}
    P["zv"] = {k: np.asarray(v, float) for k, v in bars["Z"].items()}
    P["zb"] = zone_buckets(P["zv"])
    if getattr(book, "prev_session", False):           # v1.0: the session before the pick
        P["fvp"] = {f: book.F[f][:, 0] for f in book.features if f in book.F}
        P["fcp"] = {f: book.F[f + "_change"][:, 0] for f in book.features if f + "_change" in book.F}
    if b0 >= 3 and "Ob" in bars:                        # v1.0: the stock's own candles before the pick
        Ox = bars["Ob"] * scale[:, None]
        c0, c1, c2, c3 = Cx[:, b0], Cx[:, b0 - 1], Cx[:, b0 - 2], Cx[:, b0 - 3]
        o0, h0, l0 = Ox[:, b0], Hx[:, b0], Lx[:, b0]
        with np.errstate(invalid="ignore", divide="ignore"):
            rg = h0 - l0
            ok3 = np.isfinite(c0) & np.isfinite(c1) & np.isfinite(c2)
            P["px"] = {"body0": (c0 / o0 - 1) * 100, "pos0": np.where(rg > 0, (c0 - l0) / np.where(rg > 0, rg, 1), np.nan),
                       "gap0": (o0 / c1 - 1) * 100, "ret1": (c0 / c1 - 1) * 100, "ret3": (c0 / c3 - 1) * 100,
                       "run": np.where(ok3, np.where((c0 > c1) & (c1 > c2), 2.0, np.where((c0 < c1) & (c1 < c2), -2.0,
                                                                                        0.0)), np.nan)}
    P["snap"] = {}
    for c in book.wl.columns:
        if str(c).startswith("pre_"):
            x = pd.to_numeric(book.wl[c], errors="coerce").to_numpy(float)
            if np.isfinite(x).any():
                P["snap"][str(c)] = x
    P = run_sub(P, keep)
    P.update(runner_labels(P["O"][:, 1], P["C"], P["H"], P["L"], P["atr"]))
    P["counts"] = {"settled": int(book.ok.sum()), "with_bars": int((book.ok & have).sum()),
                   "aligned": int((book.ok & aligned).sum()), "rescaled": int((book.ok & scaled).sum()),
                   "complete": int(keep.sum())}
    return run_index(P)


def run_atoms(P):
    """Every single condition: (id, family, machine condition, words)."""
    A = []
    for f in sorted(P["fc"]):
        for op, w in ((">", "rose"), ("<", "fell")):
            A.append(("F|%s%s0" % (f, op), "f:" + f, [f + "_change", op, 0], "%s %s on the signal day" % (f, w)))
    for dim, lo, hi in ZONE_RANGES:
        A.append(("Z|%s:%d:%d" % (dim, lo, hi), "z:" + dim, ["zone:" + dim, "in", [lo, hi]],
                  zone_text(((dim, lo, hi),)) + " at the signal close"))
    A += [("P|rank1", "rank", ["rank", "<=", 1], "the model's rank 1"),
          ("P|top3", "rank", ["rank", "<=", 3], "the model's ranks 1-3"),
          ("P|rank4_10", "rank", ["rank", ">=", 4], "the model's ranks 4-10"),
          ("P|agree", "agree", ["agree", ">=", 1], "the other engine picked it too (its ranks 1-10)"),
          ("P|agree3", "agree", ["agree3", ">=", 1], "both engines have it in their ranks 1-3"),
          ("P|alone", "agree", ["agree", "<=", 0], "only this engine picked it")]
    for w, nm in enumerate(WEEKDAYS):
        A.append(("W|%d" % w, "weekday", ["weekday_d1", "==", w], "D1 (the buy day) is a %s" % nm))
    for nm, col, op, v, grp, words in CTX_ATOMS:
        if col in P["snap"]:
            A.append(("C|" + nm, grp, ["snap:" + col, op, v], words))
    A += [("G|up0", "gap", ["gap_d1", ">=", 0], "D1 opens at or above the signal close (seen in the pre-open)"),
          ("G|up1", "gap", ["gap_d1", ">=", 1], "D1 opens 1% or more above the signal close (pre-open)"),
          ("G|dn0", "gap", ["gap_d1", "<", 0], "D1 opens below the signal close (pre-open)"),
          ("G|dn1", "gap", ["gap_d1", "<=", -1], "D1 opens 1% or more below the signal close (pre-open)")]
    return A


def atom_mask(cond, P):
    f, op, v = cond
    if f.startswith("zone:"):
        b = P["zb"][f[5:]]
        return (b >= v[0]) & (b <= v[1])
    if f.endswith("_change"):
        x = P["fc"].get(f[:-7])
    elif f.startswith("snap:"):
        x = P["snap"].get(f[5:])
    else:
        x = P.get(f)
    if x is None:
        return np.zeros(len(P["net"]), bool)
    x = np.asarray(x, float)
    ok = np.isfinite(x)
    r = np.zeros(len(x), bool)
    r[ok] = RUN_OPS[op](np.round(x[ok], 9), round(float(v), 9))
    return r


def run_cands(atoms, pairs_from=None):
    """Singles and every pair from different families (pairs_from None), or the given pairs with one more
    rank / agreement / weekday / context / gap condition."""
    grp = [a[1] for a in atoms]
    if pairs_from is None:
        n = len(atoms)
        return [(i,) for i in range(n)] + [(i, j) for i in range(n) for j in range(i + 1, n) if grp[i] != grp[j]]
    ctx = [i for i, a in enumerate(atoms) if a[1] in RUN_CTX_GROUPS]
    out = []
    for c in pairs_from:
        g = {grp[x] for x in c}
        out += [tuple(sorted(c + (k,))) for k in ctx if grp[k] not in g]
    return list(dict.fromkeys(out))


def _cmask(AM, c):
    m = AM[c[0]]
    for x in c[1:]:
        m = m & AM[x]
    return m


def _clb(di, x, nd):
    """Trades, mean and the quick 95% lower bound (standard error clustered by day)."""
    n = len(x)
    if n < 2:
        return n, (float(x.mean()) if n else np.nan), np.nan
    S = np.bincount(di, weights=x, minlength=nd)
    N = np.bincount(di, minlength=nd)
    m = S.sum() / n
    r = S - m * N
    g = int((N > 0).sum())
    se = math.sqrt(float((r * r).sum()) * g / max(g - 1, 1)) / n
    return n, m, m - RUN_Z * se


def _dlb(di_c, x_c, di_x, x_x, nd):
    """The quick 95% lower bound of mean(x_c) - mean(x_x), both groups clustered by day (delta method)."""
    nc, nx = len(x_c), len(x_x)
    if nc < 2 or nx < 2:
        return np.nan
    mc, mx = float(x_c.mean()), float(x_x.mean())
    r = np.bincount(di_c, weights=x_c - mc, minlength=nd) / nc - np.bincount(di_x, weights=x_x - mx, minlength=nd) / nx
    g = int(((np.bincount(di_c, minlength=nd) + np.bincount(di_x, minlength=nd)) > 0).sum())
    return (mc - mx) - RUN_Z * math.sqrt(float((r * r).sum()) * g / max(g - 1, 1))


def run_extras(AM, c):
    """For each condition of a rule: the trades its simpler version (that condition dropped) adds."""
    m = _cmask(AM, c)
    return m, ([_cmask(AM, c[:k] + c[k + 1:]) & ~m for k in range(len(c))] if len(c) > 1 else [])


def run_earn_quick(P, AM, c):
    """The smallest quick 95% lower bound, over the rule's conditions, of: its net per trade minus the net of the
    trades its simpler version adds (+inf for one condition; -inf when a simpler version adds no trades)."""
    if len(c) < 2:
        return np.inf
    m, extras = run_extras(AM, c)
    ic, nd, out = np.flatnonzero(m), len(P["days"]), np.inf
    for x in extras:
        ix = np.flatnonzero(x)
        v = _dlb(P["di"][ic], P["net"][ic], P["di"][ix], P["net"][ix], nd)
        if not np.isfinite(v) or v <= 0:
            return v if np.isfinite(v) else -np.inf
        out = min(out, v)
    return out


def run_screen(Ps, AMs, cands):
    """-> (candidates, engines, 4): trades, mean net, quick 95% lower bound of the net, of the lift."""
    R = np.full((len(cands), len(Ps), 4), np.nan)
    for e, (P, AM) in enumerate(zip(Ps, AMs)):
        di, net, lift, nd = P["di"], P["net"], P["lift"], len(P["days"])
        for i, c in enumerate(cands):
            idx = np.flatnonzero(_cmask(AM, c))
            R[i, e, 0] = len(idx)
            if len(idx) < 2:
                continue
            n, m, lb = _clb(di[idx], net[idx], nd)
            R[i, e, 1:3] = m, lb
            R[i, e, 3] = _clb(di[idx], lift[idx], nd)[2]
    return R


def run_eval(boot, P, m, extras=()):
    """One rule in one engine: trades, net per trade and its 95% interval, the lift and its interval, years, rates;
    earn_lo = the smallest 95% lower bound of (its net - the net of the trades a simpler version adds)."""
    nd = len(boot.days)
    di = np.searchsorted(boot.days, P["day"][m])
    net, lift = P["net"][m], P["lift"][m]
    n = int(m.sum())
    r = {"n": n, "per_year": n / P["years"], "net": float(net.mean()) if n else np.nan,
         "lift": float(lift.mean()) if n else np.nan, "lo": np.nan, "hi": np.nan, "lift_lo": np.nan,
         "lift_hi": np.nan, "years": 0, "bad_years": 0, "earn_lo": np.nan}
    if extras:
        los = []
        for x in extras:
            if n < 2 or x.sum() < 2:
                los.append(-np.inf)
                continue
            los.append(boot.ci_diff(di, net, np.searchsorted(boot.days, P["day"][x]), P["net"][x])[0])
        r["earn_lo"] = float(np.nanmin(los)) if np.isfinite(los).any() else -np.inf
    if n >= 2:
        X = boot.M @ np.column_stack([np.bincount(di, weights=net, minlength=nd), np.bincount(di, minlength=nd),
                                      np.bincount(di, weights=lift, minlength=nd)]).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            cnt = np.where(X[:, 1] > 0, X[:, 1], np.nan)
            mn, ml = X[:, 0] / cnt, X[:, 2] / cnt
        r["lo"], r["hi"] = float(np.nanpercentile(mn, 2.5)), float(np.nanpercentile(mn, 97.5))
        r["lift_lo"], r["lift_hi"] = float(np.nanpercentile(ml, 2.5)), float(np.nanpercentile(ml, 97.5))
    if n:
        yrs = P["year"][m]
        u = np.unique(yrs)
        r["years"] = int(len(u))
        r["bad_years"] = int(sum(net[yrs == y].mean() <= 0 for y in u))
        for k in ("dip", "runner", "rt5", "rt10", "dip_low"):
            r[k] = float(100 * P[k][m].mean())
        r["mae"] = float(P["mae"][m].mean())
    return r


def run_search(Ps, atoms, finalists=RUN_FINALISTS, log=lambda *a: None):
    """The declared search on engine tables Ps. -> (finalists table, atom masks per engine)."""
    AMs = [[atom_mask(a[2], P) for a in atoms] for P in Ps]
    mins = [RUN_MIN_PER_YEAR * P["years"] for P in Ps]
    base = run_cands(atoms)
    tested = [0]

    def scored(R):
        elig = np.all([R[:, e, 0] >= mins[e] for e in range(len(Ps))], axis=0)
        lb = np.where(np.isfinite(R[:, :, 2]), R[:, :, 2], -np.inf).min(1)
        return elig & np.isfinite(lb), lb

    def earning(cands, elig, score, k, size=None):
        """Down the ranking: the first k eligible rules whose every condition earns its place (quick, both engines)."""
        out = []
        for i in np.argsort(-np.where(elig, score, -np.inf), kind="stable"):
            if not elig[i] or len(out) == k:
                break
            if size and len(cands[i]) != size:
                continue
            tested[0] += 1
            if all(run_earn_quick(P, AM, cands[i]) > 0 for P, AM in zip(Ps, AMs)):
                out.append(int(i))
        return out
    R = run_screen(Ps, AMs, base)
    elig, score = scored(R)
    pairs = [base[i] for i in earning(base, elig, score, RUN_TRIPLE_PAIRS, size=2)]
    tri = run_cands(atoms, pairs)
    cands = base + tri
    if tri:
        R = np.concatenate([R, run_screen(Ps, AMs, tri)])
    elig, score = scored(R)
    order = earning(cands, elig, score, finalists)
    log("   screened %d rules (%d singles and pairs, %d triples); %d keep %d+ trades a year in both engines; %d "
        "tested for every condition earning its place" % (len(cands), len(base), len(tri), int(elig.sum()),
                                                          RUN_MIN_PER_YEAR, tested[0]))
    boots = [Boot(P["day"]) for P in Ps]
    rows = []
    for i in order:
        c = cands[i]
        ev = [run_eval(b, P, *run_extras(AM, c)) for b, P, AM in zip(boots, Ps, AMs)]
        qual = all(x["n"] >= mn and x["lo"] > 0 and x["lift_lo"] > 0 and x["bad_years"] <= RUN_MAX_BAD_YEARS and
                   (len(c) == 1 or x["earn_lo"] > 0) for x, mn in zip(ev, mins))
        row = {"cand": tuple(c), "rule": " & ".join(atoms[x][0] for x in c),
               "text": " & ".join(atoms[x][3] for x in c), "qualifies": bool(qual),
               "score": float(min(x["lo"] for x in ev)), "screen": float(score[i])}
        for P, x in zip(Ps, ev):
            row.update({"%s_%s" % (P["name"], k): v for k, v in x.items()})
        rows.append(row)
    T = pd.DataFrame(rows)
    if len(T):
        T = T.sort_values(["qualifies", "score"], ascending=[False, False], kind="stable").reset_index(drop=True)
    return T, AMs


def run_pick_top(T, AMs, k=RUN_TOP, only_qualified=True):
    """Walk down the ranking (only_qualified=False: by score alone); keep a rule unless it is a version of one kept
    (its conditions within the other's, or 70% of the same trades of the first engine)."""
    if not len(T):
        return []
    rows = T if only_qualified else T.sort_values("score", ascending=False, kind="stable")
    chosen = []
    for r in rows.itertuples(index=False):
        if only_qualified and not r.qualifies:
            continue
        c = tuple(r.cand)
        ids = set(np.flatnonzero(_cmask(AMs[0], c)).tolist())
        if not ids or any(set(c) <= set(c2) or set(c2) <= set(c) or overlap(ids, i2) >= RUN_OVERLAP
                          for c2, i2 in chosen):
            continue
        chosen.append((c, ids))
        if len(chosen) == k:
            break
    return [c for c, _ in chosen]


def _union(AM, cands, n):
    m = np.zeros(n, bool)
    for c in cands:
        m |= _cmask(AM, c)
    return m


def run_walk_forward(Ps, atoms, years=RUN_WF_YEARS, log=lambda *a: None):
    """The search replayed: each year, the candidates chosen with the picks whose D5 exit was before 1 January,
    their picks (each once) judged on that year. -> (rows, {engine: pooled out-of-sample lift and verdict})."""
    rows, pool = [], {P["name"]: [] for P in Ps}
    for Y in years:
        cut, nxt = np.datetime64("%d-01-01" % Y), np.datetime64("%d-01-01" % (Y + 1))
        train = [run_index(run_sub(P, P["d5"] < cut)) for P in Ps]
        test = [run_index(run_sub(P, (P["day"] >= cut) & (P["day"] < nxt))) for P in Ps]
        if any(len(t["net"]) < RUN_WF_MIN for t in train) or any(len(t["net"]) == 0 for t in test):
            rows.append({"year": Y, "chosen": 0, "rules": "", "text": "too few picks to choose with"})
            continue
        T, AMs = run_search(train, atoms)
        top = run_pick_top(T, AMs)
        row = {"year": Y, "chosen": len(top), "rules": "; ".join(" & ".join(atoms[x][0] for x in c) for c in top),
               "text": "; ".join(" & ".join(atoms[x][3] for x in c) for c in top) or
               "no rule qualified on the years before"}
        for t in test:
            e = t["name"]
            row["%s_n" % e] = len(t["net"])
            row["%s_net_all" % e] = float(t["net"].mean())
            row["%s_nodip_all" % e] = float(100 * (~t["dip"]).mean())
            if top:
                m = _union([atom_mask(a[2], t) for a in atoms], top, len(t["net"]))
                row["%s_n_in" % e] = int(m.sum())
                if m.any():
                    row["%s_net_in" % e] = float(t["net"][m].mean())
                    row["%s_lift_in" % e] = float(t["lift"][m].mean())
                    row["%s_nodip_in" % e] = float(100 * (~t["dip"][m]).mean())
                    pool[e].append((t["day"][m], t["lift"][m], t["net"][m]))
        rows.append(row)
        log("   replay %d: %s" % (Y, row["rules"] or row["text"]))
    res = {}
    for e, parts in pool.items():
        d = np.concatenate([x[0] for x in parts]) if parts else np.array([], "datetime64[D]")
        if len(d) < 2:
            res[e] = {"years": len(parts), "n": int(len(d)), "verdict": "NO RULE CHOSEN" if not parts else "NOT SHOWN"}
            continue
        lift, net = np.concatenate([x[1] for x in parts]), np.concatenate([x[2] for x in parts])
        boot = Boot(d)
        lo, hi = _bci(boot, d, lift)
        nlo, nhi = _bci(boot, d, net)
        res[e] = {"years": len(parts), "n": int(len(d)), "lift": float(lift.mean()), "lift_lo": lo, "lift_hi": hi,
                  "net": float(net.mean()), "net_lo": nlo, "net_hi": nhi,
                  "verdict": "HOLDS" if lo > 0 else ("WORSE" if hi < 0 else "NOT SHOWN")}
    return pd.DataFrame(rows), res


def run_events(P):
    """Every pick's entries, all sold at the D5 close: {event: (filled, net)}."""
    O, C, H, L = P["O"], P["C"], P["H"], P["L"]
    stop = H[:, 0] * (1 + RUN_STOP_BUF)
    f1 = H[:, 1] >= stop
    f2 = ~f1 & (H[:, 2] >= stop)
    px = np.where(f1, np.maximum(O[:, 1], stop), np.where(f2, np.maximum(O[:, 2], stop), np.nan))
    rng = H[:, 1] - L[:, 1]
    with np.errstate(invalid="ignore", divide="ignore"):
        strong = (C[:, 1] > O[:, 1]) & (rng > 0) & ((C[:, 1] - L[:, 1]) / np.where(rng > 0, rng, 1.0) >= RUN_STRONG)
        c5 = C[:, 5]
        return {"E0": (np.ones(len(c5), bool), P["net"]),
                "E1": (f1 | f2, (c5 / px - 1) * 100 - COST),
                "E2": (strong, (c5 / np.where(strong, O[:, 2], np.nan) - 1) * 100 - COST),
                "E3": (strong, (c5 / np.where(strong, C[:, 1], np.nan) - 1) * 100 - COST)}


def run_event_rows(P, m, source, boot):
    """The four entries on the picks of one rule (m): per trade, per pick (an unfilled pick = 0, cash) and against
    the D1 open on exactly the picks the event filled."""
    rows = []
    for ev, (f, net) in run_events(P).items():
        ff = m & f & np.isfinite(net)
        r = {"source": source, "engine": P["name"], "event": ev, "entry": EVENT_WORDS[ev], "picks": int(m.sum()),
             "filled": int(ff.sum()), "fill_pct": 100.0 * ff.sum() / max(1, m.sum())}
        if ff.sum() >= 2:
            lo, hi = _bci(boot, P["day"][ff], net[ff])
            slot = np.where(ff, net, 0.0)[m]
            slo, shi = _bci(boot, P["day"][m], slot)
            d = net[ff] - P["net"][ff]
            dlo, dhi = _bci(boot, P["day"][ff], d)
            r.update({"net": float(net[ff].mean()), "lo": lo, "hi": hi, "per_pick": float(slot.mean()),
                      "per_pick_lo": slo, "per_pick_hi": shi, "vs_open": float(d.mean()), "vs_open_lo": dlo,
                      "vs_open_hi": dhi, "nodip_pct": float(100 * (~P["dip"][ff]).mean()),
                      "runner_pct": float(100 * P["runner"][ff].mean()), "per_year": ff.sum() / P["years"]})
        rows.append(r)
    return rows


def wauc(x, y, W):
    """AUC of x for y (bool) with weights W (rows = resamples): ties count half."""
    o = np.argsort(x, kind="mergesort")
    return _wauc_sorted(x[o], y[o], W[:, o])


def _wauc_sorted(xs, ys, Ws, st=None):
    if st is None:
        st = np.flatnonzero(np.r_[True, xs[1:] != xs[:-1]])
    pos = np.add.reduceat(Ws * ys, st, axis=1)
    neg = np.add.reduceat(Ws, st, axis=1) - pos
    below = np.cumsum(neg, axis=1) - neg
    with np.errstate(invalid="ignore", divide="ignore"):
        return (pos * (below + 0.5 * neg)).sum(1) / (pos.sum(1) * neg.sum(1))


def run_anatomy(Ps, target="runner", word="runners", B=RUN_ANAT_B, seed=7):
    """What marks the target at the signal close (and the D1 open): every measure's AUC in each engine with a 95%
    interval (AUC +- 1.96 x its block-bootstrap standard deviation over signal days), Benjamini-Hochberg q within each
    engine. SHOWN = both engines' intervals off 0.5 the same way and q <= 0.10 in both."""
    def measures(P):
        M = {"rank": P["rank"], "other engine picked it": P["agree"], "gap at the D1 open %": P["gap_d1"],
             "s_atr14": P["atr"]}
        M.update({"%s (level)" % f: v for f, v in P["fv"].items()})
        M.update({"%s (change on the signal day)" % f: v for f, v in P["fc"].items()})
        M.update({"zone %s" % k: v for k, v in P["zv"].items()})
        M.update({"snapshot %s" % k: v for k, v in P["snap"].items()})
        return M
    per = []
    for P in Ps:
        boot = Boot(P["day"], B=B, seed=seed)
        Wfull = boot.M[:, np.searchsorted(boot.days, P["day"])]
        y = P[target].astype(bool)
        res = {}
        for k, x in measures(P).items():
            x = np.asarray(x, float)
            ok = np.isfinite(x)
            if ok.sum() < 50 or y[ok].all() or not y[ok].any() or np.std(x[ok]) == 0:
                continue
            xo, yo = x[ok], y[ok]
            o = np.argsort(xo, kind="mergesort")
            xs, ys, cols = xo[o], yo[o], np.flatnonzero(ok)[o]
            st = np.flatnonzero(np.r_[True, xs[1:] != xs[:-1]])
            a = float(_wauc_sorted(xs, ys, np.ones((1, len(xs))), st)[0])
            bs = np.concatenate([_wauc_sorted(xs, ys, Wfull[i:i + 100][:, cols], st) for i in range(0, B, 100)])
            sd = float(np.nanstd(bs))
            z = (a - 0.5) / sd if sd > 0 else np.nan
            med = np.median(xo)
            res[k] = {"auc": a, "lo": a - RUN_Z * sd if sd > 0 else np.nan, "hi": a + RUN_Z * sd if sd > 0 else np.nan,
                      "p": math.erfc(abs(z) / math.sqrt(2)) if np.isfinite(z) else np.nan,
                      "rate_hi": float(100 * yo[xo >= med].mean()),
                      "rate_lo": float(100 * yo[xo < med].mean()) if (xo < med).any() else np.nan}
        for (k, v), qq in zip(res.items(), bh_q([v["p"] for v in res.values()])):
            v["q"] = float(qq)
        per.append(res)
    rows = []
    for k in [k for k in per[0] if all(k in r for r in per)]:
        up = all(p[k]["lo"] > 0.5 for p in per)
        dn = all(p[k]["hi"] < 0.5 for p in per)
        r = {"measure": k, "shown": bool((up or dn) and all(p[k]["q"] <= 0.10 for p in per)),
             "direction": ("higher -> more " + word) if up else (("lower -> more " + word) if dn else ""),
             "strength": float(min(abs(p[k]["auc"] - 0.5) for p in per)) if (up or dn) else 0.0}
        for P, p in zip(Ps, per):
            r.update({"%s_%s" % (P["name"], kk): vv for kk, vv in p[k].items()})
        rows.append(r)
    A = pd.DataFrame(rows)
    if len(A):
        A = A.sort_values(["shown", "strength"], ascending=[False, False], kind="stable").reset_index(drop=True)
    return A


def run_sim(ent, ex, ret, prio, sym, t0, t1, cal, k, lev=1):
    """Closed-trade equity of a k-slot book (start 1.0) on calendar indices t0..t1: each trade gets 1/k of the equity
    at its entry open; all slots busy = skipped (the lower prio first on the same open); exits at the close, the slot
    free from the next open; MTF: lev x exposure, 0.04% a day on the borrowed part."""
    keep = (ent >= t0) & (ent <= t1)
    o = np.lexsort((sym[keep], prio[keep], ent[keep]))
    E, X, R = ent[keep][o], ex[keep][o], ret[keep][o]
    cash, pos, eq, j, n, skipped = 1.0, [], np.empty(t1 - t0 + 1), 0, 0, 0
    for t in range(t0, t1 + 1):
        while j < len(E) and E[j] == t:
            if len(pos) < k:
                size = (cash + sum(p[1] for p in pos)) / k
                if size > 0:
                    days = int((cal[X[j]] - cal[E[j]]) / np.timedelta64(1, "D"))
                    cash -= size
                    pos.append((X[j], size, size * (lev * R[j] / 100 - (lev - 1) * RUN_MTF_DAY * days)))
                    n += 1
            else:
                skipped += 1
            j += 1
        still = []
        for p in pos:
            if p[0] <= t:
                cash += p[1] + p[2]
            else:
                still.append(p)
        pos = still
        eq[t - t0] = cash + sum(p[1] for p in pos)
    return np.maximum(eq, 0.0), n, skipped


def run_book_stats(eq, n, skipped, years):
    end = float(eq[-1]) if len(eq) else np.nan
    dd = float(np.max(1 - eq / np.maximum(np.maximum.accumulate(eq), 1e-12))) * 100 if len(eq) else np.nan
    return {"end_rs": end * RUN_CAPITAL, "cagr": (end ** (1 / years) - 1) * 100 if end > 0 else -100.0,
            "worst_fall": dd, "trades": n, "per_week": n / (years * 365.25 / 7), "skipped": skipped}


def run_dedupe(T):
    """One position per pick: its earliest entry (the same open: the lower prio)."""
    return T.sort_values(["pick", "ent", "prio"], kind="stable").drop_duplicates("pick", keep="first")


def run_money(arms, cal):
    """arms: {name: DataFrame(pick, ent, ex, net, prio, sym)} on calendar indices. Every book on the same window
    (from RUN_MONEY_FROM to the last exit of any book). -> rows."""
    calD = np.asarray(cal).astype("datetime64[D]")
    t0 = int(np.searchsorted(calD, RUN_MONEY_FROM))
    arms = {k: run_dedupe(v) for k, v in arms.items() if len(v)}
    last = [int(v.loc[v["ent"] >= t0, "ex"].max()) for v in arms.values() if (v["ent"] >= t0).any()]
    if not last or t0 >= len(calD):
        return pd.DataFrame()
    t1 = min(len(calD) - 1, max(last))
    years = max(1e-9, float((calD[t1] - calD[t0]) / np.timedelta64(1, "D")) / 365.25)
    rows = []
    for name, T in arms.items():
        for k in RUN_SLOTS:
            for lev in (1, 2):
                eq, n, sk = run_sim(T["ent"].to_numpy(np.int64), T["ex"].to_numpy(np.int64), T["net"].to_numpy(float),
                                    T["prio"].to_numpy(float), T["sym"].astype(str).to_numpy(), t0, t1, calD, k, lev)
                rows.append({"book": name, "slots": k, "mtf": "2x" if lev == 2 else "none",
                             **run_book_stats(eq, n, sk, years), "from": str(calD[t0]), "to": str(calD[t1])})
    return pd.DataFrame(rows)


def run_dip_arm(out, cal):
    """The frozen setups' trades of the newest ZONES run (picks_zone_trades.parquet, hash-checked) with IN / OUT of
    each setup's picks zone, on the watchlist's calendar. -> (DataFrame or None, note)."""
    try:
        zrun, zdoc = load_zones(Path(out))
    except ValueError as e:
        return None, "not used: %s" % e
    if zrun is None or not (Path(zrun) / "picks_zone_trades.parquet").is_file():
        return None, "not used: no ZONES run with picks_zone_trades.parquet under %s" % (Path(out) / "ZONES")
    read_hashed_run(zrun, ["picks_zone_trades.parquet"])
    Z = pd.read_parquet(Path(zrun) / "picks_zone_trades.parquet")
    sid_ = Z["setup"].astype(str).to_numpy()
    inz = np.zeros(len(Z), bool)
    for sid in np.unique(sid_):
        key = (((zdoc.get("setups") or {}).get(sid) or {}).get("picks") or {}).get("zone", "")
        m = sid_ == sid
        if key:
            inz[m] = zone_mask(zone_parse(key), {d: Z.loc[m, d].to_numpy() for d in ZDIM})
    calD = np.asarray(cal).astype("datetime64[D]")
    e_ = pd.to_datetime(Z["day"]).to_numpy().astype("datetime64[D]")
    x_ = pd.to_datetime(Z["exit"]).to_numpy().astype("datetime64[D]")
    ent, ex = np.searchsorted(calD, e_), np.searchsorted(calD, x_)
    ok = (ent < len(calD)) & (ex < len(calD)) & np.isfinite(Z["net"].to_numpy(float))
    ok[ok] &= (calD[ent[ok]] == e_[ok]) & (calD[ex[ok]] == x_[ok])
    D = pd.DataFrame({"pick": Z["trade_id"].astype(str).to_numpy(), "engine": Z["engine"].astype(str).to_numpy(),
                      "setup": sid_, "ent": ent, "ex": ex, "net": Z["net"].to_numpy(float),
                      "rank": Z["rank"].to_numpy(float), "sym": Z["symbol"].astype(str).to_numpy(),
                      "zone_in": inz})[ok].reset_index(drop=True)
    return D, "%s: %d setup trades, %d of them IN their picks zone" % (Path(zrun).name, len(D), int(D["zone_in"].sum()))


def run_arms(P, masks, names, dip):
    """One engine's money books: the plan (ranks 1-3 at the D1 open), the no-dip arm (the candidates' picks at the D1
    open), the dip arm (S3 in its zone; all 7 setups) and both arms together."""
    base = pd.DataFrame({"pick": P["ids"], "ent": P["ent"], "ex": P["ex"], "net": P["net"], "rank": P["rank"],
                         "sym": P["symbols"]})
    plan = base[P["rank"] <= 3].copy()
    plan["prio"] = plan["rank"]
    arms = {"plan: ranks 1-3 at the D1 open": plan}
    N = None
    if masks:
        N = pd.concat([base[m].assign(src=nm) for m, nm in zip(masks, names)], ignore_index=True)
        N["prio"] = -N["src"].map(N.groupby("src")["net"].mean()) * 1000 + N["rank"]
        arms["no-dip arm: the candidates at the D1 open"] = N
    if dip is not None and len(dip):
        D = dip[dip["engine"] == P["name"]].copy()
        if len(D):
            good = D["zone_in"].to_numpy(bool)
            D["src"] = np.where(good, "IN:", "OUT:").astype(object) + D["setup"].to_numpy(object)
            D["prio"] = -D["src"].map(D.groupby("src")["net"].mean()) * 1000 + D["rank"]
            s3 = D[(D["setup"] == "S3").to_numpy() & good]
            if len(s3):
                arms["dip arm: S3 in its zone"] = s3
            arms["dip arm: all 7 setups (in-zone first)"] = D
            if N is not None:
                if len(s3):
                    arms["BOTH ARMS: no-dip + S3 in its zone"] = pd.concat([N, s3], ignore_index=True)
                arms["BOTH ARMS: no-dip + all 7 setups"] = pd.concat([N, D], ignore_index=True)
    return arms


def runners_hash(doc):
    return hashlib.sha256(_canon_json({k: v for k, v in doc.items() if k != "sha256"}).encode()).hexdigest()


def load_runners(base):
    """The newest runners run's RUNNER_CANDIDATES.json (hash-checked) -> (folder, doc) or (None, None)."""
    run = latest_run(base, "RUNNERS", [RUN_FILE])
    if run is None:
        return None, None
    doc = json.loads((run / RUN_FILE).read_text(encoding="utf-8"))
    if doc.get("sha256") != runners_hash(doc):
        raise ValueError("%s was changed after it was written - refusing" % (run / RUN_FILE))
    return run, doc


def _p(x, nd=2, sign=True):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return ""
    return ("%+.*f" % (nd, x) if sign else "%.*f" % (nd, x)) if np.isfinite(x) else ""


def _g(r, k):
    try:
        return float(r.get(k, np.nan))
    except (TypeError, ValueError):
        return np.nan


def cmd_runners(a, log=None, data=None):
    """The no-dip study: labels, what marks a runner, the rule search, entries, the year-by-year replay, the money
    view with the dip arm. Writes RUNNERS\\RUNNERS_<date>_<nnn>\\ under --out."""
    log = log or (lambda *x: print(time.strftime("%H:%M:%S ") + " ".join(str(y) for y in x), flush=True))
    t0 = time.time()
    cols_file = Path(a.columns_file) if getattr(a, "columns_file", "") else \
        Path(__file__).resolve().with_name("features_final.txt")
    if not cols_file.is_file():
        print("REFUSED: no feature list %s (give --columns-file)" % cols_file)
        return 3
    cols = read_columns_file(cols_file)
    log("%s runners: watchlist %s; panel %s; features %s (%d)" % (VERSION, a.data, a.features, cols_file.name,
                                                                  len(cols)))
    book = load(a.data, a.features, None, cols, None, log, getattr(a, "chunk", 8))
    if book.missing_features:
        log(" NOTE: %d feature columns are not in the panel: %s" % (len(book.missing_features),
                                                                    ", ".join(book.missing_features)))
    if data is None:
        data = LiveData(a.root, getattr(a, "stage_e_any", False), panel=None)
    M = market_dims(data.index_closes(dict(ZONE_INDEX)))
    log(" reading every pick's own bars (highs, lows, the zone values at the signal close)")
    bars = run_bars(book, data.ohlcv, data.forget, M)
    engines = [e for e in ("D", "ENS") if (book.engine_arr == e).any()]
    if not engines:
        print("REFUSED: no D or ENS picks in the watchlist")
        return 3
    sdD = np.asarray(book.signal_day).astype("datetime64[D]")
    ranks = {e: dict(zip(zip(sdD[book.engine_arr == e], book.symbols[book.engine_arr == e]),
                         book.rank[book.engine_arr == e].astype(float))) for e in engines}
    Ps = []
    for e in engines:
        m = book.engine_arr == e
        other = ranks[[x for x in engines if x != e][0]] if len(engines) > 1 else {}
        bsub = {"H": bars["H"][m], "L": bars["L"][m], "Cb": bars["Cb"][m], "Z": {k: v[m] for k, v in bars["Z"].items()}}
        P = runner_table(book.take(m, e), bsub, other, e)
        Ps.append(P)
        c = P["counts"]
        log(" %s: %d settled picks, %d with their bars, %d whose bars give the watchlist's D1-D5 closes (%d after a "
            "price adjustment), %d complete; %.1f years" % (e, c["settled"], c["with_bars"], c["aligned"],
                                                             c["rescaled"], c["complete"], P["years"]))
    align = "; ".join("%s: %d of %d settled picks complete (their bars give the watchlist's D1-D5 closes)%s" % (
        P["name"], P["counts"]["complete"], P["counts"]["settled"],
        " - WARNING: below 98%, send RUNNERS.md" if P["counts"]["complete"] < 0.98 * P["counts"]["settled"] else "")
        for P in Ps)
    del bars
    have = [{x[0] for x in run_atoms(P)} for P in Ps]
    atoms = [x for x in run_atoms(Ps[0]) if all(x[0] in h for h in have)]
    log(" %d single conditions (features %d, zones %d, rank / agreement / weekday / context / gap %d)" % (
        len(atoms), sum(x[0].startswith("F|") for x in atoms), sum(x[0].startswith("Z|") for x in atoms),
        sum(not x[0].startswith(("F|", "Z|")) for x in atoms)))
    base = []
    for P in Ps:
        net, top3 = P["net"], P["rank"] <= 3
        tot = float(net.sum())
        base.append({"engine": P["name"], "picks": int(len(net)), "no_dip_pct": float(100 * (~P["dip"]).mean()),
                     "dip_low_pct": float(100 * P["dip_low"].mean()), "dip_atr_pct": float(100 * P["dip_atr"].mean()),
                     "rt5_pct": float(100 * P["rt5"].mean()), "rt10_pct": float(100 * P["rt10"].mean()),
                     "runner_pct": float(100 * P["runner"].mean()), "net_all": float(net.mean()),
                     "net_runner": float(net[P["runner"]].mean()) if P["runner"].any() else np.nan,
                     "net_nodip": float(net[~P["dip"]].mean()) if (~P["dip"]).any() else np.nan,
                     "net_dip": float(net[P["dip"]].mean()) if P["dip"].any() else np.nan,
                     "runner_share_of_profit": float(100 * net[P["runner"]].sum() / tot) if tot > 0 else np.nan,
                     "top3_no_dip_pct": float(100 * (~P["dip"][top3]).mean()) if top3.any() else np.nan})
    log(" base: " + "; ".join("%s no dip %.1f%%, runners %.1f%% (net %s; all picks %s)" % (
        b["engine"], b["no_dip_pct"], b["runner_pct"], _p(b["net_runner"]), _p(b["net_all"])) for b in base))
    log(" what marks a runner / a dip (AUC of every measure, both engines)")
    AN = run_anatomy(Ps, "runner", "runners")
    AN2 = run_anatomy(Ps, "dip", "dips")
    log(" the rule search (both engines)")
    T, AMs = run_search(Ps, atoms, log=log)
    top = run_pick_top(T, AMs)
    top_any = run_pick_top(T, AMs, only_qualified=False)
    nm = lambda c: " & ".join(atoms[x][0] for x in c)
    log(" %d of %d finalists qualify; candidates: %s" % (int(T["qualifies"].sum()) if len(T) else 0, len(T),
                                                         "; ".join(nm(c) for c in top) or "none"))
    log(" the year-by-year replay")
    WF, wfres = run_walk_forward(Ps, atoms, log=log)
    log(" out of sample: " + "; ".join("%s %s" % (e, v["verdict"]) for e, v in wfres.items()))
    log(" entries on the candidates' picks")
    ev_rows = []
    for P, AM in zip(Ps, AMs):
        boot = Boot(P["day"])
        ev_rows += run_event_rows(P, np.ones(len(P["net"]), bool), "ALL picks", boot)
        if top:
            ev_rows += run_event_rows(P, _union(AM, top, len(P["net"])), "the no-dip arm (R1-R%d)" % len(top), boot)
        for c in dict.fromkeys(top + top_any):
            ev_rows += run_event_rows(P, _cmask(AM, c), nm(c), boot)
    EV = pd.DataFrame(ev_rows)
    log(" the money view")
    dip, dip_note = run_dip_arm(a.out, book.cal)
    money = []
    for P, AM in zip(Ps, AMs):
        Mo = run_money(run_arms(P, [_cmask(AM, c) for c in top], ["R%d" % (i + 1) for i in range(len(top))], dip),
                       book.cal)
        if len(Mo):
            Mo.insert(0, "engine", P["name"])
            money.append(Mo)
    MO = pd.concat(money, ignore_index=True) if money else pd.DataFrame()
    run = new_run_dir(Path(a.out) / "RUNNERS", "RUNNERS")
    cand_doc = []
    pos = {tuple(c): i for i, c in enumerate(T["cand"])} if len(T) else {}
    for kind, lst, tag in (("qualified", top, "R"), ("best by score", top_any, "B")):
        for i, c in enumerate(lst):
            r = T.iloc[pos[tuple(c)]]
            cand_doc.append({"list": kind, "id": "%s%d" % (tag, i + 1), "rule": r["rule"], "text": r["text"],
                             "qualifies": bool(r["qualifies"]), "conds": [atoms[x][2] for x in c],
                             "stats": {P["name"]: {k: r.get("%s_%s" % (P["name"], k)) for k in
                                                   ("n", "per_year", "net", "lo", "hi", "lift", "lift_lo", "lift_hi",
                                                    "dip", "runner", "rt5", "rt10", "mae", "bad_years", "years")}
                                       for P in Ps}})
    res = _clean({"file": RUN_FILE, "tool": VERSION, "made_at": _dt.datetime.now(IST).isoformat(timespec="seconds"),
                  "rule": RUN_RULE, "watchlist": str(a.data), "panel": str(a.features), "features": cols_file.name,
                  "alignment": align, "counts": {P["name"]: P["counts"] for P in Ps}, "base": base,
                  "candidates": cand_doc, "out_of_sample": wfres, "dip_arm": dip_note})
    res["sha256"] = runners_hash(res)
    (run / RUN_FILE).write_text(json.dumps(res, indent=1), encoding="utf-8")
    Tw = T.copy()
    if len(Tw):
        Tw["cand"] = Tw["cand"].apply(lambda c: "+".join(atoms[x][0] for x in c))
    Tw.to_csv(run / "runner_finalists.csv", index=False)
    WF.to_csv(run / "runner_walk_forward.csv", index=False)
    AN.to_csv(run / "runner_anatomy.csv", index=False)
    AN2.to_csv(run / "dip_anatomy.csv", index=False)
    EV.to_csv(run / "runner_events.csv", index=False)
    MO.to_csv(run / "runner_money.csv", index=False)
    pk = []
    for P, AM in zip(Ps, AMs):
        D = pd.DataFrame({"trade_id": P["ids"], "engine": P["name"], "symbol": P["symbols"], "signal_day": P["day"],
                          "rank": P["rank"], "net": P["net"], "lift": P["lift"], "dip": P["dip"],
                          "dip_low": P["dip_low"], "dip_atr": P["dip_atr"], "rt5": P["rt5"], "rt10": P["rt10"],
                          "runner": P["runner"], "mfe": P["mfe"], "mae": P["mae"], "gap_d1": P["gap_d1"],
                          "agree": P["agree"]})
        for i, c in enumerate(top):
            D["R%d" % (i + 1)] = _cmask(AM, c)
        pk.append(D)
    pd.concat(pk, ignore_index=True).to_parquet(run / "runner_picks.parquet", index=False)
    md = runner_report(res, base, AN, AN2, T, top, top_any, WF, wfres, EV, MO, [P["name"] for P in Ps])
    (run / "RUNNERS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    write_hashes(run, [RUN_FILE, "RUNNERS.md", "runner_finalists.csv", "runner_walk_forward.csv",
                       "runner_anatomy.csv", "dip_anatomy.csv", "runner_events.csv", "runner_money.csv",
                       "runner_picks.parquet"])
    log("RUNNERS WRITTEN -> %s (%.1f min)" % (run, (time.time() - t0) / 60))
    return 0


def runner_report(res, base, AN, AN2, T, top, top_any, WF, wfres, EV, MO, E):
    md = ["# Runners - the picks that do not dip (%s, %s)" % (time.strftime("%d %b %Y"), VERSION), "",
          "Watchlist %s; panel %s; features %s. %s." % (res["watchlist"], res["panel"], res["features"],
                                                        res["alignment"]), "",
          "**The rule (declared before any result):** " + RUN_RULE, "",
          "Rs a year = net % per trade x trades a year x Rs 1,000 (Rs 1 L a trade, before taxes).", "",
          "## Verdict: the no-dip candidates (bought at the D1 open, sold at the D5 close)", ""]
    hdr = "| | rule | " + " | ".join(("%s trades a year | %s net %% per trade [95%%] | %s lift over all picks [95%%] | "
                                      "%s no dip | %s runners | %s Rs a year") % ((e,) * 6) for e in E) + " |"
    sep = "|---|---|" + "---:|" * (6 * len(E))
    pos = {tuple(c): i for i, c in enumerate(T["cand"])} if len(T) else {}

    def line(tag, c):
        r = T.iloc[pos[tuple(c)]]
        cells = []
        for e in E:
            n_, py = _g(r, e + "_net"), _g(r, e + "_per_year")
            cells += ["%.0f" % py, "%s [%s, %s]" % (_p(n_), _p(_g(r, e + "_lo")), _p(_g(r, e + "_hi"))),
                      "%s [%s, %s]" % (_p(_g(r, e + "_lift")), _p(_g(r, e + "_lift_lo")), _p(_g(r, e + "_lift_hi"))),
                      "%.1f%%" % (100 - _g(r, e + "_dip")), "%.1f%%" % _g(r, e + "_runner"),
                      "{:,.0f}".format(n_ * py * 1000) if np.isfinite(n_ * py) else ""]
        return "| %s | %s%s | %s |" % (tag, r["text"], "" if r["qualifies"] else " (does NOT qualify)",
                                       " | ".join(cells))
    md += [hdr, sep] + [line("R%d" % (i + 1), c) for i, c in enumerate(top)]
    if not top:
        md.append("| | no rule qualifies in both engines |" + " |" * (6 * len(E)))
    md += ["", "**Out of sample (the whole search replayed year by year, the candidates' picks each once):** " +
           "; ".join("%s **%s** - lift over all picks %s [%s, %s], net %s [%s, %s] per trade on %d picks in %d years"
                     % (e, v["verdict"], _p(v.get("lift")), _p(v.get("lift_lo")), _p(v.get("lift_hi")),
                        _p(v.get("net")), _p(v.get("net_lo")), _p(v.get("net_hi")), v.get("n", 0), v.get("years", 0))
                     for e, v in wfres.items()), "",
           "The best 5 by score, qualified or not (the open list):", "", hdr, sep]
    md += [line("B%d" % (i + 1), c) for i, c in enumerate(top_any)]
    if len(MO):
        md += ["", "**Trades a week and money at a glance** (Rs 5 L, no MTF, from 2022; in-sample):", "",
               "| engine | book | slots | trades a week | Rs 5 L became | a year | worst fall |",
               "|---|---|---:|---:|---:|---:|---:|"]
        for r in MO[(MO["mtf"] == "none") & MO["slots"].isin([3, 5])].to_dict("records"):
            md.append("| %s | %s | %d | %.1f | Rs %s | %s%% | %.1f%% |" % (
                r["engine"], r["book"], r["slots"], r["per_week"], "{:,.0f}".format(r["end_rs"]), _p(r["cagr"], 1),
                r["worst_fall"]))
    md += ["", "## The year-by-year replay", "",
           "| year | candidates chosen with exits before 1 January | " + " | ".join(
               "%s picks that year | %s in the candidates | %s net in them | %s net all picks | %s no dip in them | "
               "%s no dip all" % ((e,) * 6) for e in E) + " |", "|---|---|" + "---:|" * (6 * len(E))]
    for r in WF.to_dict("records"):
        cells = []
        for e in E:
            cells += ["%.0f" % _g(r, e + "_n") if np.isfinite(_g(r, e + "_n")) else "",
                      "%.0f" % _g(r, e + "_n_in") if np.isfinite(_g(r, e + "_n_in")) else "",
                      _p(_g(r, e + "_net_in")), _p(_g(r, e + "_net_all")),
                      ("%.1f%%" % _g(r, e + "_nodip_in")) if np.isfinite(_g(r, e + "_nodip_in")) else "",
                      ("%.1f%%" % _g(r, e + "_nodip_all")) if np.isfinite(_g(r, e + "_nodip_all")) else ""]
        md.append("| %s | %s | %s |" % (r["year"], r.get("rules") or r.get("text", ""), " | ".join(cells)))
    md += ["", "## Base rates (every complete pick bought at the D1 open, sold at the D5 close)", "",
           "| engine | picks | no dip (a close 2% below) | dip by the intraday low 2% | dip by 1 ATR | D5 close +5% | "
           "+10% | runners | net all | net runners | net no dip | net dip | runners' share of the profit | ranks 1-3 "
           "no dip |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for b in base:
        md.append("| %s | %d | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %.1f%% | %s | %s | %s | %s | %s | %s |" % (
            b["engine"], b["picks"], b["no_dip_pct"], b["dip_low_pct"], b["dip_atr_pct"], b["rt5_pct"], b["rt10_pct"],
            b["runner_pct"], _p(b["net_all"]), _p(b["net_runner"]), _p(b["net_nodip"]), _p(b["net_dip"]),
            ("%.0f%%" % b["runner_share_of_profit"]) if np.isfinite(_g(b, "runner_share_of_profit")) else "",
            ("%.1f%%" % b["top3_no_dip_pct"]) if np.isfinite(_g(b, "top3_no_dip_pct")) else ""))
    for title, A, what in (("What marks a runner at the signal close (and the D1 open)", AN, "runners"),
                           ("What marks a pick that will dip (below 0.5 = less dipping)", AN2, "dips")):
        md += ["", "## " + title, "",
               "AUC = the chance a pick with the outcome scores higher on the measure than one without (0.5 = no "
               "information). SHOWN = both engines' 95%% intervals off 0.5 the same way and q <= 0.10 in both. Above / "
               "below = the share of %s among picks above / below the measure's median. The 30 strongest:" % what, "",
               "| measure | SHOWN | " + " | ".join("%s AUC [95%%] | %s above / below the median" % (e, e) for e in E)
               + " |", "|---|---|" + "---:|" * (2 * len(E))]
        for r in A.head(30).to_dict("records"):
            md.append("| %s | %s | %s |" % (r["measure"], ("yes, " + r["direction"]) if r["shown"] else "", " | ".join(
                "%.3f [%.3f, %.3f] | %.1f%% / %s" % (
                    r["%s_auc" % e], r["%s_lo" % e], r["%s_hi" % e], r["%s_rate_hi" % e],
                    ("%.1f%%" % r["%s_rate_lo" % e]) if np.isfinite(_g(r, "%s_rate_lo" % e)) else "") for e in E)))
    md += ["", "## Entries: the D1 open against the events, on the same picks", "",
           "Per trade = the filled trades only; per pick = an unfilled pick counts 0 (cash); against the D1 open = the "
           "event's trade minus the D1-open trade on exactly the picks the event filled. All sold at the D5 close.",
           "", "| picks of | engine | entry | filled | per trade [95%] | per pick [95%] | against the D1 open [95%] | "
           "no dip | runners | trades a year |", "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in EV.to_dict("records"):
        md.append("| %s | %s | %s | %d of %d (%.0f%%) | %s [%s, %s] | %s [%s, %s] | %s [%s, %s] | %s | %s | %s |" % (
            r["source"], r["engine"], r["entry"], r["filled"], r["picks"], r["fill_pct"], _p(_g(r, "net")),
            _p(_g(r, "lo")), _p(_g(r, "hi")), _p(_g(r, "per_pick")), _p(_g(r, "per_pick_lo")),
            _p(_g(r, "per_pick_hi")), _p(_g(r, "vs_open")), _p(_g(r, "vs_open_lo")), _p(_g(r, "vs_open_hi")),
            ("%.1f%%" % _g(r, "nodip_pct")) if np.isfinite(_g(r, "nodip_pct")) else "",
            ("%.1f%%" % _g(r, "runner_pct")) if np.isfinite(_g(r, "runner_pct")) else "",
            ("%.0f" % _g(r, "per_year")) if np.isfinite(_g(r, "per_year")) else ""))
    md += ["", "## Money: the arms alone and together (one position per pick, Rs 5 L, profits reinvested, from 2022)",
           "", "Dip arm: %s. Worst fall = the largest fall from a peak, counted when trades close (open positions' "
           "daily swings would show more). In-sample: the candidates and the zones were chosen on these years. One "
           "slot holds a 5-session trade, so a slot carries about one trade a week." % res["dip_arm"], "",
           "| engine | book | slots | MTF | Rs 5 L became | a year | worst fall | trades a week | skipped (slots full) |",
           "|---|---|---:|---|---:|---:|---:|---:|---:|"]
    for r in MO.to_dict("records"):
        md.append("| %s | %s | %d | %s | Rs %s | %s%% | %.1f%% | %.1f | %d |" % (
            r["engine"], r["book"], r["slots"], r["mtf"], "{:,.0f}".format(r["end_rs"]), _p(r["cagr"], 1),
            r["worst_fall"], r["per_week"], r["skipped"]))
    md += ["", "## Limits", "",
           "- Everything here is on the history the engines, the setups and the zones were studied on; the replay "
           "guards the search, not the list of conditions. Only the forward paper ledger is clean evidence.",
           "- The D1 open and the gap are the cache's; a pre-open (AMO) order fills at the open price. The breakout "
           "fills at the stop (or the open above it) with no slippage; the D1-close entry fills at the official close.",
           "- The money view ignores taxes and assumes every order fills; MTF needs the stock on the broker's list."]
    return md


# ======================================================================================== v1.0: the no-dip study, v2
ND_FILE = "NODIP_CANDIDATES.json"
ND_BEFORE = 3                 # own bars read before the signal day (the candles into the pick)
ND_LISTS = ("nodip", "runner", "money")
ND_V = {"nodip": "nodip", "runner": "runner_f", "money": "net"}
ND_TAG = {"nodip": "N", "runner": "U", "money": "M"}
ND_NAME = {"nodip": "no-dip", "runner": "runner", "money": "money"}
ND_WHAT = {"nodip": "no-dip share (never a close 2% below the D1 open on D1-D4)",
           "runner": "runner share (no dip and the D5 close 5% or more above the D1 open)",
           "money": "net % per trade at the D1 open"}
ND_FINALISTS = 60
ND_EARN_WALK = 5000           # per list, the best by the quick bound tested for every condition earning its place
ND_TRIPLE_PAIRS = 150
ND_TOP = 5
ND_OPEN = 10
ND_WF_MIN = 600               # pooled picks a training window needs
ND_LEVELS = (("L3", None, 0, "low third"), ("H3", 2, None, "high third"), ("LO", None, 1, "lower half"),
             ("HI", 1, None, "upper half"))       # cut index into the reference picks' (1/3, 1/2, 2/3) quantiles
ND_PATTERNS = (("upup", 1, 1, "rose on the session before the pick and on the signal day"),
               ("dndn", -1, -1, "fell on the session before the pick and on the signal day"),
               ("dnup", -1, 1, "turned up (fell the session before the pick, rose on the signal day)"),
               ("updn", 1, -1, "turned down (rose the session before the pick, fell on the signal day)"))
ND_PX = (("X|green", "px:candle", "body0", ">", 0, "the signal day closed above its open (green)"),
         ("X|red", "px:candle", "body0", "<", 0, "the signal day closed below its open (red)"),
         ("X|top3rd", "px:pos", "pos0", ">=", 2 / 3, "the signal day closed in the top third of its range"),
         ("X|bot3rd", "px:pos", "pos0", "<=", 1 / 3, "the signal day closed in the bottom third of its range"),
         ("X|gapup0", "px:gap0", "gap0", ">", 0, "the signal day opened above the previous close"),
         ("X|gapdn0", "px:gap0", "gap0", "<", 0, "the signal day opened below the previous close"),
         ("X|bigup", "px:ret1", "ret1", ">=", 2, "the signal day rose 2% or more"),
         ("X|bigdn", "px:ret1", "ret1", "<=", -2, "the signal day fell 2% or more"),
         ("X|up3", "px:ret3", "ret3", ">", 0, "up over the 3 sessions into the pick"),
         ("X|dn3", "px:ret3", "ret3", "<", 0, "down over the 3 sessions into the pick"),
         ("X|run_up", "px:run", "run", ">=", 2, "two higher closes in a row into the pick"),
         ("X|run_dn", "px:run", "run", "<=", -2, "two lower closes in a row into the pick"))
WHY_PAIRS = (("d_donch_pos_50_rmean50", "d_bb_bw_20"), ("d_vol_yz_50", "d_n_5pct_up_252"),
             ("d_ema20_angle_deg", "w_ret_13w"), ("d_ema20_angle_deg", "d_bb_bw_20"),
             ("d_ema20_angle_deg", "d_vol_yz_50"), ("d_vol_yz_50", "d_dist_from_52wl"),
             ("d_n_5pct_up_252", "d_bb_bw_20"), ("d_vol_yz_50", "w_ret_13w"), ("d_vol_yz_50", "d_wq_16"),
             ("d_ema20_angle_deg", "d_wq_29"), ("d_ema20_angle_deg", "d_dist_from_52wl"),
             ("d_donch_pos_50_rmean50", "d_dist_from_52wl"), ("d_dist_from_52wl", "d_wq_16"),
             ("d_ema20_angle_deg", "d_adx14"))
ND_RULE = (
    "nodip v2, declared 8 Nov 2026 before any result (Karan: test it as rigorously as the setups - which features and "
    "combinations help most and how they behaved in the sessions before the pick; be very open, we are exploring). "
    "PICKS: engines D and ENS, ranks 1-10, bought at the D1 open, sold at the D5 close, 0.35 pp costs, judged on the "
    "POOLED picks: a stock-day picked by both engines counts once (its best rank); each engine is also checked on its "
    "own. DIP = a close on D1-D4 at least 2% below the D1 open; RUNNER = no dip and the D5 close 5% or more above the "
    "D1 open. THREE LISTS from the same search: no-dip (target = the share of picks with no dip), runner (the runner "
    "share), money (net % per trade). CONDITIONS, all known at the signal close or the D1 open: for each of the 60 "
    "features - its level at the signal close (low third, high third, lower half, upper half; the cut-offs come from "
    "the picks of the window the rule is chosen on, never from later ones), its move on the signal day (rose / fell), "
    "its move on the session before the pick (rose / fell) and the two together (rose twice, fell twice, turned up, "
    "turned down); the stock's own candles into the pick (green / red signal day, a close in the top / bottom third "
    "of its range, a gap up / down, a 2% rise / fall, up / down over 3 sessions, two higher / lower closes in a row); "
    "the 12 zone measures; the model's rank, both engines picking it, D1's weekday, the market context and the "
    "stock's state at the pick, the gap at the D1 open. SEARCH: stage 1 every single condition; stage 2 every pair "
    "from different families (a feature's level may pair with its own moves); stage 3 the 150 best earning pairs of "
    "each list with one more rank / agreement / weekday / context / gap condition. Per list, the 5,000 best by a "
    "quick day-clustered lower bound of its target are tested for every condition earning its place (quick) and the "
    "first 60 that pass get the full block bootstrap. A rule QUALIFIES for its list when, on the pooled picks: 25 or "
    "more trades a year; its target's excess over all picks of the same days (resampled together) has a 95% interval "
    "above 0; net per trade at the D1 open 95% above 0; every condition earns its place on the target (the rule "
    "minus the trades its simpler version adds, 95% above 0); net <= 0 in at most 2 of its years; and in each engine "
    "on its own the target beats that engine's picks and the net is above 0. Score = the lower 95% bound of the "
    "target. CANDIDATES: per list the top 5 qualifiers that are not versions of each other (conditions within, or 70% "
    "of the same trades); the 10 best by score are listed too, qualified or not. Plain 95% per rule (be very open): "
    "the whole search is replayed year by year 2022-2026 (chosen with the picks whose D5 exit was before 1 January - "
    "the cut-offs too - and judged on that year); per list HOLDS when the chosen rules' target beats all picks out of "
    "sample (95%), WORSE when below, else NOT SHOWN. MONEY, apples to apples: Rs 5 L in 2 / 3 / 5 / 7 equal slots, "
    "profits reinvested, no MTF and MTF 2x, entries from 2022, one position per pick, the same open by the model's "
    "rank: the baseline (each engine's ranks 1-3 at the D1 open) against each list's arm OUT OF SAMPLE (each year the "
    "rules chosen from the years before), the arm in-sample (the candidates) and the out-of-sample arm with S3 in its "
    "zone (the newest ZONES run; in-sample). ENTRIES: the D1 open against the breakout, the D2 open after a strong D1 "
    "and the D1 close after a strong D1, on the same picks.")


def nd_index(P):
    """run_index plus the same-day lift of the no-dip and runner shares."""
    P = run_index(P)
    nd = len(P["days"])
    c = np.maximum(np.bincount(P["di"], minlength=nd), 1)
    for t in ("nodip", "runner"):
        v = P[ND_V[t]]
        P["lift_" + t] = v - (np.bincount(P["di"], weights=v, minlength=nd) / c)[P["di"]]
    P["lift_money"] = P["lift"]
    return P


def nd_engine(P):
    """An engine's runner table with the study's targets."""
    P["nodip"] = (~P["dip"]).astype(float)
    P["runner_f"] = P["runner"].astype(float)
    P["key"] = np.array([str(d) + "|" + str(s) for d, s in zip(P["day"], P["symbols"])], dtype=object)
    return nd_index(P)


def nd_pool(Ps):
    """Both engines' complete picks as one table: a stock-day picked by both counts once (its best rank)."""
    allk = np.concatenate([P["key"] for P in Ps])
    rk = np.concatenate([P["rank"] for P in Ps])
    o = np.lexsort((rk, allk))
    ks = allk[o]
    sel = o[np.r_[True, ks[1:] != ks[:-1]]]
    n0 = len(Ps[0]["net"])
    U = {}
    for key, v0 in Ps[0].items():
        if key in ("days", "di", "year", "years", "counts", "name") or key.startswith("lift"):
            continue
        if isinstance(v0, dict):
            U[key] = {kk: np.concatenate([P[key][kk] for P in Ps])[sel] for kk in v0 if all(kk in P[key] for P in Ps)}
        elif isinstance(v0, np.ndarray) and v0.ndim and len(v0) == n0:
            U[key] = np.concatenate([P[key] for P in Ps])[sel]
    for P in Ps:
        r = dict(zip(P["key"], P["rank"]))
        U["rank_" + P["name"]] = np.array([r.get(k, np.nan) for k in U["key"]], float)
    R = np.column_stack([U["rank_" + P["name"]] for P in Ps])
    have = np.isfinite(R)
    U["rank"] = np.where(have, R, np.inf).min(1)
    U["engines"] = np.array(["+".join(P["name"] for P, h in zip(Ps, row) if h) for row in have], dtype=object)
    both = have.all(1) if len(Ps) > 1 else np.zeros(len(U["key"]), bool)
    U["agree"] = both.astype(float)
    U["agree3"] = (both & (np.where(have, R, 99) <= 3).all(1)).astype(float)
    U["name"] = "pooled"
    return nd_index(U)


def nd_atoms(P):
    """Every single condition (level conditions carry quantile cuts; nd_resolve turns them into numbers)."""
    A = []
    for f in sorted(P["fv"]):
        for nm, lo, hi, w in ND_LEVELS:
            A.append(("V|%s:%s" % (f, nm), "fl:" + f, ["lvl", f, lo, hi], "%s in its %s at the signal close" % (f, w)))
    for f in sorted(P["fc"]):
        A.append(("B|%s:up0" % f, "fb:" + f, ["fc", f, ">"], "%s rose on the signal day" % f))
        A.append(("B|%s:dn0" % f, "fb:" + f, ["fc", f, "<"], "%s fell on the signal day" % f))
        if f in P.get("fcp", {}):
            A.append(("B|%s:up1" % f, "fb:" + f, ["fcp", f, ">"], "%s rose on the session before the pick" % f))
            A.append(("B|%s:dn1" % f, "fb:" + f, ["fcp", f, "<"], "%s fell on the session before the pick" % f))
            for nm, a, b, w in ND_PATTERNS:
                A.append(("B|%s:%s" % (f, nm), "fb:" + f, ["pat", f, a, b], "%s %s" % (f, w)))
    if P.get("px"):
        A += [(aid, grp, ["px", fld, op, v], w) for aid, grp, fld, op, v, w in ND_PX]
    A += [a for a in run_atoms(P) if not a[0].startswith("F|")]
    return A


def nd_resolve(atoms, Pref):
    """Level conditions get their cut-offs from the reference picks (the window the rules are chosen on)."""
    qs, out = {}, []
    for aid, grp, c, w in atoms:
        if c[0] != "lvl":
            out.append((aid, grp, c, w))
            continue
        f = c[1]
        if f not in qs:
            x = np.asarray(Pref["fv"].get(f, []), float)
            x = x[np.isfinite(x)]
            qs[f] = np.quantile(x, [1 / 3, 0.5, 2 / 3]) if len(x) >= 30 else None
        q = qs[f]
        if q is None:
            continue
        lo = -np.inf if c[2] is None else float(q[c[2]])
        hi = np.inf if c[3] is None else float(q[c[3]])
        rng = ("<= %.6g" % hi) if c[2] is None else ("> %.6g" % lo) if c[3] is None else "%.6g to %.6g" % (lo, hi)
        out.append((aid, grp, ["fv", f, lo, hi], "%s (%s)" % (w, rng)))
    return out


def nd_mask(cond, P):
    k, n = cond[0], len(P["net"])
    if k in ("fv", "fc", "fcp", "pat", "px"):
        src = {"fv": "fv", "fc": "fc", "fcp": "fcp", "px": "px"}.get(k)
        with np.errstate(invalid="ignore"):
            if k == "pat":
                a, b = P.get("fcp", {}).get(cond[1]), P.get("fc", {}).get(cond[1])
                if a is None or b is None:
                    return np.zeros(n, bool)
                return np.isfinite(a) & np.isfinite(b) & (np.sign(a) == cond[2]) & (np.sign(b) == cond[3])
            x = P.get(src, {}).get(cond[1])
            if x is None:
                return np.zeros(n, bool)
            x = np.asarray(x, float)
            if k == "fv":
                return np.isfinite(x) & (x > cond[2]) & (x <= cond[3])
            if k in ("fc", "fcp"):
                return np.isfinite(x) & ((x > 0) if cond[2] == ">" else (x < 0))
            ok = np.isfinite(x)
            r = np.zeros(n, bool)
            r[ok] = RUN_OPS[cond[2]](np.round(x[ok], 9), round(float(cond[3]), 9))
            return r
    return atom_mask(cond, P)


def nd_screen(P, AM, cands):
    """-> (candidates, 7): trades; mean and quick 95% lower bound (day-clustered) of the no-dip share, the runner share
    and the net per trade."""
    R = np.full((len(cands), 7), np.nan)
    di, nd = P["di"], len(P["days"])
    V = [P[ND_V[t]] for t in ND_LISTS]
    for i, c in enumerate(cands):
        idx = np.flatnonzero(_cmask(AM, c))
        n = len(idx)
        R[i, 0] = n
        if n < 2:
            continue
        d = di[idx]
        N = np.bincount(d, minlength=nd)
        g = int((N > 0).sum())
        f = g / max(g - 1, 1)
        for t, v in enumerate(V):
            S = np.bincount(d, weights=v[idx], minlength=nd)
            m = S.sum() / n
            r = S - m * N
            R[i, 1 + 2 * t] = m
            R[i, 2 + 2 * t] = m - RUN_Z * math.sqrt(float(r @ r) * f) / n
    return R


def nd_earn_quick(P, AM, c, v):
    """The smallest quick 95% lower bound, over the rule's conditions, of: its target minus the target of the trades
    its simpler version adds (+inf for one condition)."""
    if len(c) < 2:
        return np.inf
    m, extras = run_extras(AM, c)
    ic, nd, out = np.flatnonzero(m), len(P["days"]), np.inf
    for x in extras:
        ix = np.flatnonzero(x)
        val = _dlb(P["di"][ic], v[ic], P["di"][ix], v[ix], nd)
        if not np.isfinite(val) or val <= 0:
            return val if np.isfinite(val) else -np.inf
        out = min(out, val)
    return out


def nd_eval(boot, P, m, extras, t, allsum):
    """One rule on the pooled picks: trades; each target's mean and 95% interval and its excess over all picks of the
    same (resampled) days; the same-day lift of the list's target; earn_lo on it; years and bad years (net <= 0)."""
    nd = len(boot.days)
    di = np.searchsorted(boot.days, P["day"][m])
    n = int(m.sum())
    r = {"n": n, "per_year": n / P["years"], "earn_lo": np.nan, "years": 0, "bad_years": 0}
    cnt = np.bincount(di, minlength=nd).astype(float)
    MC = boot.M @ cnt
    with np.errstate(invalid="ignore", divide="ignore"):
        MCn = np.where(MC > 0, MC, np.nan)
        for tt in ND_LISTS:
            v = P[ND_V[tt]][m]
            r[tt] = float(v.mean()) if n else np.nan
            r[tt + "_ex"] = r[tt] - float(P[ND_V[tt]].mean())
            for k in ("_lo", "_hi", "_ex_lo", "_ex_hi"):
                r[tt + k] = np.nan
            if n >= 2:
                mb = (boot.M @ np.bincount(di, weights=v, minlength=nd)) / MCn
                Sa, Na = allsum[tt]
                ex = mb - Sa / Na
                r[tt + "_lo"], r[tt + "_hi"] = float(np.nanpercentile(mb, 2.5)), float(np.nanpercentile(mb, 97.5))
                r[tt + "_ex_lo"], r[tt + "_ex_hi"] = float(np.nanpercentile(ex, 2.5)), float(np.nanpercentile(ex, 97.5))
        lf = P["lift_" + t][m]
        r["lift"] = float(lf.mean()) if n else np.nan
        r["lift_lo"] = r["lift_hi"] = np.nan
        if n >= 2:
            ml = (boot.M @ np.bincount(di, weights=lf, minlength=nd)) / MCn
            r["lift_lo"], r["lift_hi"] = float(np.nanpercentile(ml, 2.5)), float(np.nanpercentile(ml, 97.5))
    v = P[ND_V[t]]
    if extras:
        los = []
        for x in extras:
            if n < 2 or x.sum() < 2:
                los.append(-np.inf)
                continue
            los.append(boot.ci_diff(di, v[m], np.searchsorted(boot.days, P["day"][x]), v[x])[0])
        r["earn_lo"] = float(np.nanmin(los)) if np.isfinite(los).any() else -np.inf
    if n:
        yrs, net = P["year"][m], P["net"][m]
        u = np.unique(yrs)
        r["years"] = int(len(u))
        r["bad_years"] = int(sum(net[yrs == y].mean() <= 0 for y in u))
        r["mae"] = float(P["mae"][m].mean())
    return r


def nd_search(P, atoms, engines=(), finalists=ND_FINALISTS, log=lambda *a: None):
    """The declared search on the pooled picks P (atoms resolved on P). engines: their tables, for the direction check.
    -> ({list: finalists table}, pooled atom masks, (candidates, screen))."""
    AM = [nd_mask(a[2], P) for a in atoms]
    AMe = [[nd_mask(a[2], E) for a in atoms] for E in engines]
    mins = RUN_MIN_PER_YEAR * P["years"]
    base = run_cands(atoms)
    R = nd_screen(P, AM, base)
    tested = [0]

    def walk(cands, R, t, k, size=None):
        ti = ND_LISTS.index(t)
        elig = (R[:, 0] >= mins) & np.isfinite(R[:, 2 + 2 * ti])
        out, walked = [], 0
        for i in np.argsort(-np.where(elig, R[:, 2 + 2 * ti], -np.inf), kind="stable"):
            if not elig[i] or len(out) == k or walked >= ND_EARN_WALK:
                break
            if size and len(cands[i]) != size:
                continue
            walked += 1
            tested[0] += 1
            if nd_earn_quick(P, AM, cands[i], P[ND_V[t]]) > 0:
                out.append(int(i))
        return out
    pairs = []
    for t in ND_LISTS:
        pairs += [base[i] for i in walk(base, R, t, ND_TRIPLE_PAIRS, size=2)]
    tri = run_cands(atoms, list(dict.fromkeys(pairs)))
    cands = base + tri
    if tri:
        R = np.concatenate([R, nd_screen(P, AM, tri)])
    boot = Boot(P["day"])
    nd = len(boot.days)
    Na = boot.M @ np.bincount(P["di"], minlength=nd).astype(float)
    allsum = {t: (boot.M @ np.bincount(P["di"], weights=P[ND_V[t]], minlength=nd), Na) for t in ND_LISTS}
    eall = [{t: float(E[ND_V[t]].mean()) for t in ND_LISTS} for E in engines]
    tables = {}
    for t in ND_LISTS:
        rows = []
        for i in walk(cands, R, t, finalists):
            c = cands[i]
            m, extras = run_extras(AM, c)
            r = nd_eval(boot, P, m, extras, t, allsum)
            cons = True
            for E, AMx, ea in zip(engines, AMe, eall):
                me = _cmask(AMx, c)
                ne = int(me.sum())
                tv = float(E[ND_V[t]][me].mean()) if ne else np.nan
                nv = float(E["net"][me].mean()) if ne else np.nan
                r.update({"%s_n" % E["name"]: ne, "%s_target" % E["name"]: tv, "%s_net" % E["name"]: nv,
                          "%s_all" % E["name"]: ea[t]})
                cons = cons and ne > 0 and tv > ea[t] and nv > 0
            q = (r["n"] >= mins and r[t + "_ex_lo"] > 0 and r["money_lo"] > 0 and (len(c) == 1 or r["earn_lo"] > 0)
                 and r["bad_years"] <= RUN_MAX_BAD_YEARS and cons)
            rows.append({"cand": tuple(c), "rule": " & ".join(atoms[x][0] for x in c),
                         "text": " & ".join(atoms[x][3] for x in c), "qualifies": bool(q), "engines_agree": bool(cons),
                         "score": r[t + "_lo"], "screen": float(R[i, 2 + 2 * ND_LISTS.index(t)]), **r})
        T = pd.DataFrame(rows)
        if len(T):
            T = T.sort_values(["qualifies", "score"], ascending=[False, False], kind="stable").reset_index(drop=True)
        tables[t] = T
    log("   %d rules screened (%d singles and pairs, %d triples), %d keep %d+ trades a year; %d tested for every "
        "condition earning its place; qualify: %s" % (len(cands), len(base), len(tri), int((R[:, 0] >= mins).sum()),
                                                      RUN_MIN_PER_YEAR, tested[0], ", ".join(
                                                          "%s %d" % (ND_NAME[t], int(tables[t]["qualifies"].sum())
                                                                     if len(tables[t]) else 0) for t in ND_LISTS)))
    return tables, AM, (cands, R)


def nd_walk_forward(U, Es, spec, years=RUN_WF_YEARS, log=lambda *a: None):
    """The search replayed: each year the cut-offs and the rules come from the picks whose D5 exit was before 1
    January; the rules' picks of that year are the out-of-sample selection. -> (rows, verdicts, {list: selection})."""
    rows, rrows, sel = [], [], {t: np.zeros(len(U["net"]), bool) for t in ND_LISTS}
    used = np.zeros(len(U["net"]), bool)
    for Y in years:
        cut, nxt = np.datetime64("%d-01-01" % Y), np.datetime64("%d-01-01" % (Y + 1))
        tm = (U["day"] >= cut) & (U["day"] < nxt)
        tr = nd_index(run_sub(U, U["d5"] < cut))
        if len(tr["net"]) < ND_WF_MIN or not tm.any():
            rows.append({"year": Y, "picks": int(tm.sum()), "note": "too few picks to choose with"})
            continue
        te = nd_index(run_sub(U, tm))
        trE = [nd_index(run_sub(E, E["d5"] < cut)) for E in Es]
        atoms = nd_resolve(spec, tr)
        tables, AM, _ = nd_search(tr, atoms, trE)
        AMt = [nd_mask(a[2], te) for a in atoms]
        used |= tm
        row = {"year": Y, "picks": int(tm.sum())}
        for tt in ND_LISTS:
            row["all_" + tt] = float(te[ND_V[tt]].mean())
        for t in ND_LISTS:
            top = run_pick_top(tables[t], [AM])
            m = _union(AMt, top, len(te["net"])) if top else np.zeros(len(te["net"]), bool)
            sel[t][np.flatnonzero(tm)[m]] = True
            row[t + "_rules"] = "; ".join(" & ".join(atoms[x][0] for x in c) for c in top) or "none qualified"
            row[t + "_conds"] = json.dumps([[atoms[x][2] for x in c] for c in top], default=float)
            row[t + "_n"] = int(m.sum())
            for tt in ND_LISTS:
                row["%s_%s" % (t, tt)] = float(te[ND_V[tt]][m].mean()) if m.any() else np.nan
            for c in top:                                     # each chosen rule on its own, that year
                mc = _cmask(AMt, c)
                rrows.append({"year": Y, "list": t, "rule": " & ".join(atoms[x][0] for x in c), "n": int(mc.sum()),
                              "target": float(te[ND_V[t]][mc].mean()) if mc.any() else np.nan,
                              "target_all": float(te[ND_V[t]].mean()),
                              "net": float(te["net"][mc].mean()) if mc.any() else np.nan,
                              "net_all": float(te["net"].mean())})
        rows.append(row)
        log("   replay %d: %s" % (Y, "; ".join("%s %d picks" % (ND_NAME[t], row[t + "_n"]) for t in ND_LISTS)))
    verdicts = {}
    if used.sum() >= 2:
        O = nd_index(run_sub(U, used))
        boot = Boot(O["day"])
        nd = len(boot.days)
        Na = boot.M @ np.bincount(O["di"], minlength=nd).astype(float)
        for t in ND_LISTS:
            m = sel[t][used]
            v = {"list": t, "picks": int(m.sum())}
            for tt in (t, "money"):
                x = O[ND_V[tt]]
                v[tt] = float(x[m].mean()) if m.any() else np.nan
                v[tt + "_all"] = float(x.mean())
                v[tt + "_ex_lo"] = v[tt + "_ex_hi"] = np.nan
                if m.sum() >= 2:
                    di = O["di"][m]
                    with np.errstate(invalid="ignore", divide="ignore"):
                        mb = (boot.M @ np.bincount(di, weights=x[m], minlength=nd)) / \
                            (boot.M @ np.bincount(di, minlength=nd).astype(float))
                        ex = mb - (boot.M @ np.bincount(O["di"], weights=x, minlength=nd)) / Na
                    v[tt + "_ex_lo"], v[tt + "_ex_hi"] = float(np.nanpercentile(ex, 2.5)), float(
                        np.nanpercentile(ex, 97.5))
            lo, hi = v[t + "_ex_lo"], v[t + "_ex_hi"]
            v["verdict"] = "NO RULE CHOSEN" if not m.any() else "HOLDS" if lo > 0 else "WORSE" if hi < 0 else \
                "NOT SHOWN"
            verdicts[t] = v
    return pd.DataFrame(rows), verdicts, sel, pd.DataFrame(rrows)


def nd_evidence(U, AM, c, t, RR, rule):
    """A candidate's track record: in how many years (10+ trades) it beat all picks on its target (in-sample), and
    each replay year in which the same rule was chosen from the years before, with its target there vs all picks."""
    m = _cmask(AM, c)
    v = U[ND_V[t]]
    good = tot = 0
    for y in np.unique(U["year"]):
        yr = U["year"] == y
        if (m & yr).sum() >= 10:
            tot += 1
            good += int(v[m & yr].mean() > v[yr].mean())
    rep_ = []
    if len(RR):
        for r in RR[(RR["list"] == t) & (RR["rule"] == rule)].to_dict("records"):
            rep_.append({"year": int(r["year"]), "n": int(r["n"]), "diff": r["target"] - r["target_all"],
                         "net": r["net"]})
    return {"years_better": good, "years": tot, "replay": rep_}


def nd_member(E, keys):
    return np.array([k in keys for k in E["key"]], bool)


def nd_books(E, tops_in, sel_oos, U, dip):
    """One engine's money books: the baseline (ranks 1-3 at the D1 open) and, per list, the arm out of sample, the arm
    in-sample and the out-of-sample arm with S3 in its zone. The same open: the model's rank (the no-dip side first)."""
    base = pd.DataFrame({"pick": E["ids"], "ent": E["ent"], "ex": E["ex"], "net": E["net"], "rank": E["rank"],
                         "sym": E["symbols"]})
    base["prio"] = base["rank"]
    books = {"baseline: ranks 1-3 at the D1 open": base[E["rank"] <= 3]}
    s3 = None
    if dip is not None and len(dip):
        s3 = dip[(dip["engine"] == E["name"]) & (dip["setup"] == "S3") & dip["zone_in"].astype(bool)].copy()
        s3["prio"] = s3["rank"] + 100
    for t in ND_LISTS:
        oos = base[nd_member(E, set(U["key"][sel_oos[t]]))]
        books["%s arm, out of sample" % ND_NAME[t]] = oos
        books["%s arm, in-sample (%s1-%s%d)" % (ND_NAME[t], ND_TAG[t], ND_TAG[t], max(1, len(tops_in[t][1])))] = \
            base[nd_member(E, set(U["key"][tops_in[t][0]]))]
        if s3 is not None and len(s3):
            books["%s arm, out of sample + S3 in its zone" % ND_NAME[t]] = pd.concat([oos, s3], ignore_index=True)
    return {k: v for k, v in books.items() if len(v)}


def nd_table(U, tops, sel_oos):
    """The pooled picks with every condition's input, the labels and the selections (float32 where numeric)."""
    cols = {"key": U["key"].astype(str), "day": U["day"], "symbol": U["symbols"].astype(str),
            "engines": U["engines"].astype(str)}
    for k in ("rank", "rank_D", "rank_ENS", "net", "nodip", "runner_f", "rt5", "rt10", "dip_low", "dip_atr", "mfe",
              "mae", "gap_d1", "weekday_d1", "agree", "agree3", "atr", "lift"):
        if k in U:
            cols[k] = np.asarray(U[k], float).astype(np.float32)
    for grp, pre in (("fv", "lvl:"), ("fc", "chg0:"), ("fvp", "lvl_prev:"), ("fcp", "chg_prev:"), ("zv", "zone:"),
                     ("px", "px:"), ("snap", "")):
        for k, v in U.get(grp, {}).items():
            cols[pre + k] = np.asarray(v, float).astype(np.float32)
    for t in ND_LISTS:
        for i, c in enumerate(tops[t][1]):
            cols["%s%d" % (ND_TAG[t], i + 1)] = tops[t][2][i]
        cols["oos_" + t] = sel_oos[t]
    return pd.DataFrame(cols)


def cmd_nodip(a, log=None, data=None):
    """The no-dip study v2 (declared ND_RULE). Writes NODIP\\NODIP_<date>_<nnn>\\ under --out."""
    log = log or (lambda *x: print(time.strftime("%H:%M:%S ") + " ".join(str(y) for y in x), flush=True))
    t0 = time.time()
    cols_file = Path(a.columns_file) if getattr(a, "columns_file", "") else \
        Path(__file__).resolve().with_name("features_final.txt")
    if not cols_file.is_file():
        print("REFUSED: no feature list %s (give --columns-file)" % cols_file)
        return 3
    cols = read_columns_file(cols_file)
    log("%s nodip: watchlist %s; panel %s; features %s (%d)" % (VERSION, a.data, a.features, cols_file.name, len(cols)))
    book = load(a.data, a.features, None, cols, None, log, getattr(a, "chunk", 8), prev=True)
    if book.missing_features:
        log(" NOTE: %d feature columns are not in the panel: %s" % (len(book.missing_features),
                                                                    ", ".join(book.missing_features)))
    if data is None:
        data = LiveData(a.root, getattr(a, "stage_e_any", False), panel=None)
    M = market_dims(data.index_closes(dict(ZONE_INDEX)))
    log(" reading every pick's own bars (3 sessions before the pick to D5, the zone values at the signal close)")
    bars = run_bars(book, data.ohlcv, data.forget, M, before=ND_BEFORE)
    engines = [e for e in ("D", "ENS") if (book.engine_arr == e).any()]
    if not engines:
        print("REFUSED: no D or ENS picks in the watchlist")
        return 3
    sdD = np.asarray(book.signal_day).astype("datetime64[D]")
    ranks = {e: dict(zip(zip(sdD[book.engine_arr == e], book.symbols[book.engine_arr == e]),
                         book.rank[book.engine_arr == e].astype(float))) for e in engines}
    Es = []
    for e in engines:
        m = book.engine_arr == e
        other = ranks[[x for x in engines if x != e][0]] if len(engines) > 1 else {}
        bsub = {"H": bars["H"][m], "L": bars["L"][m], "Cb": bars["Cb"][m], "Ob": bars["Ob"][m], "before": ND_BEFORE,
                "Z": {k: v[m] for k, v in bars["Z"].items()}}
        E = runner_table(book.take(m, e), bsub, other, e)
        E["name"] = e
        Es.append(nd_engine(E))
        c = Es[-1]["counts"]
        log(" %s: %d settled picks, %d complete (their bars give the watchlist's D1-D5 closes); %.1f years" % (
            e, c["settled"], c["complete"], Es[-1]["years"]))
    del bars
    U = nd_pool(Es)
    nboth = int((U["agree"] > 0).sum())
    log(" pooled: %d stock-days (%d picked by both engines, counted once)" % (len(U["net"]), nboth))
    align = "; ".join("%s: %d of %d settled picks complete%s" % (
        E["name"], E["counts"]["complete"], E["counts"]["settled"],
        " - WARNING: below 98%, send NODIP.md" if E["counts"]["complete"] < 0.98 * E["counts"]["settled"] else "")
        for E in Es) + "; pooled %d stock-days, %d of them picked by both engines (counted once)" % (len(U["net"]),
                                                                                                    nboth)
    spec = nd_atoms(U)
    atoms = nd_resolve(spec, U)
    log(" %d single conditions (feature levels %d, moves %d, candles %d, zones %d, rank / agreement / weekday / "
        "context / gap %d)" % (len(atoms), sum(x[0].startswith("V|") for x in atoms),
                               sum(x[0].startswith("B|") for x in atoms), sum(x[0].startswith("X|") for x in atoms),
                               sum(x[0].startswith("Z|") for x in atoms),
                               sum(x[0][:2] in ("P|", "W|", "C|", "G|") for x in atoms)))
    log(" the search (pooled picks; each engine checked for direction)")
    tables, AM, (cands, R) = nd_search(U, atoms, Es, log=log)
    tops = {}
    for t in ND_LISTS:
        top = run_pick_top(tables[t], [AM])
        opn = run_pick_top(tables[t], [AM], ND_OPEN, only_qualified=False)
        tops[t] = (_union(AM, top, len(U["net"])), top, [_cmask(AM, c) for c in top], opn)
        log(" %s list: %s" % (ND_NAME[t], "; ".join(" & ".join(atoms[x][0] for x in c) for c in top) or
                              "no rule qualifies"))
    log(" the year-by-year replay (cut-offs and rules from the years before each year)")
    WF, verdicts, sel, RR = nd_walk_forward(U, Es, spec, log=log)
    log(" out of sample: " + "; ".join("%s %s" % (ND_NAME[t], v["verdict"]) for t, v in verdicts.items()))
    log(" entries and money")
    dip, dip_note = run_dip_arm(a.out, book.cal)
    ev_rows, money = [], []
    AMe = [[nd_mask(x[2], E) for x in atoms] for E in Es]
    for E, AMx in zip(Es, AMe):
        boot = Boot(E["day"])
        ev_rows += run_event_rows(E, np.ones(len(E["net"]), bool), "ALL picks", boot)
        for t in ND_LISTS:
            mo = nd_member(E, set(U["key"][sel[t]]))
            if mo.any():
                ev_rows += run_event_rows(E, mo, "%s arm, out of sample" % ND_NAME[t], boot)
            for i, c in enumerate(tops[t][1]):
                ev_rows += run_event_rows(E, _cmask(AMx, c), "%s%d: %s" % (ND_TAG[t], i + 1, " & ".join(
                    atoms[x][0] for x in c)), boot)
        Mo = run_money(nd_books(E, tops, sel, U, dip), book.cal)
        if len(Mo):
            Mo.insert(0, "engine", E["name"])
            money.append(Mo)
    EV = pd.DataFrame(ev_rows)
    MO = pd.concat(money, ignore_index=True) if money else pd.DataFrame()
    # stage 1 (every single condition) and the model's own pairs
    single = [i for i, c in enumerate(cands) if len(c) == 1]
    S1 = pd.DataFrame({"condition": [atoms[cands[i][0]][0] for i in single],
                       "text": [atoms[cands[i][0]][3] for i in single], "n": R[single, 0],
                       "per_year": R[single, 0] / U["years"], "nodip": R[single, 1], "nodip_lo": R[single, 2],
                       "runner": R[single, 3], "runner_lo": R[single, 4], "net": R[single, 5],
                       "net_lo": R[single, 6]})
    for E, AMx in zip(Es, AMe):
        S1["%s_nodip" % E["name"]] = [float(E["nodip"][AMx[cands[i][0]]].mean()) if AMx[cands[i][0]].any() else np.nan
                                      for i in single]
        S1["%s_net" % E["name"]] = [float(E["net"][AMx[cands[i][0]]].mean()) if AMx[cands[i][0]].any() else np.nan
                                    for i in single]
    feat = [x[0].split("|", 1)[1].split(":", 1)[0] if x[0][:2] in ("V|", "B|") else None for x in atoms]
    mins = RUN_MIN_PER_YEAR * U["years"]
    wanted = {frozenset(p_) for p_ in WHY_PAIRS}
    bucket = {}
    for i, c in enumerate(cands):
        if len(c) == 2 and R[i, 0] >= mins and feat[c[0]] and feat[c[1]]:
            k = frozenset((feat[c[0]], feat[c[1]]))
            if k in wanted:
                bucket.setdefault(k, []).append(i)
    why = []
    for fa, fb in WHY_PAIRS:
        ix = bucket.get(frozenset((fa, fb)), [])
        if ix:
            b = max(ix, key=lambda i: R[i, 2] if np.isfinite(R[i, 2]) else -np.inf)
            why.append({"features": "%s x %s" % (fa, fb), "rule": " & ".join(atoms[x][0] for x in cands[b]),
                        "text": " & ".join(atoms[x][3] for x in cands[b]), "n": R[b, 0], "nodip": R[b, 1],
                        "nodip_lo": R[b, 2], "runner": R[b, 3], "net": R[b, 5], "net_lo": R[b, 6]})
    WHY = pd.DataFrame(why)
    base = []
    for P in Es + [U]:
        t3 = P["rank"] <= 3
        base.append({"table": P["name"], "picks": int(len(P["net"])), "nodip": float(100 * P["nodip"].mean()),
                     "runner": float(100 * P["runner_f"].mean()), "net": float(P["net"].mean()),
                     "top3_nodip": float(100 * P["nodip"][t3].mean()) if t3.any() else np.nan,
                     "top3_net": float(P["net"][t3].mean()) if t3.any() else np.nan})
    # write
    evid = {t: {tuple(c): nd_evidence(U, AM, c, t, RR, " & ".join(atoms[x][0] for x in c))
                for c in dict.fromkeys(tops[t][1] + tops[t][3])} for t in ND_LISTS}
    run = new_run_dir(Path(a.out) / "NODIP", "NODIP")
    lists = {}
    for t in ND_LISTS:
        T = tables[t]
        pos = {tuple(c): i for i, c in enumerate(T["cand"])} if len(T) else {}
        items = []
        for kind, lst, tag in (("qualified", tops[t][1], ND_TAG[t]), ("open list (best by score)", tops[t][3], "B")):
            for i, c in enumerate(lst):
                r = T.iloc[pos[tuple(c)]]
                items.append({"list": kind, "id": "%s%d" % (tag, i + 1), "rule": r["rule"], "text": r["text"],
                              "qualifies": bool(r["qualifies"]), "conds": [atoms[x][2] for x in c],
                              "evidence": evid[t][tuple(c)],
                              "stats": {k: r.get(k) for k in r.index if k not in ("cand", "rule", "text")}})
        lists[t] = {"target": ND_WHAT[t], "candidates": items, "out_of_sample": verdicts.get(t, {})}
    res = _clean({"file": ND_FILE, "tool": VERSION, "made_at": _dt.datetime.now(IST).isoformat(timespec="seconds"),
                  "rule": ND_RULE, "watchlist": str(a.data), "panel": str(a.features), "features": cols_file.name,
                  "alignment": align, "counts": {E["name"]: E["counts"] for E in Es}, "base": base,
                  "lists": lists, "dip_arm": dip_note})
    res["sha256"] = runners_hash(res)
    (run / ND_FILE).write_text(json.dumps(res, indent=1), encoding="utf-8")
    F = []
    for t in ND_LISTS:
        T = tables[t].copy()
        if len(T):
            T["cand"] = T["cand"].apply(lambda c: "+".join(atoms[x][0] for x in c))
            T.insert(0, "list", t)
            F.append(T)
    (pd.concat(F, ignore_index=True) if F else pd.DataFrame()).to_csv(run / "nodip_finalists.csv", index=False)
    S1.sort_values("nodip_lo", ascending=False).to_csv(run / "nodip_stage1.csv", index=False)
    WF.to_csv(run / "nodip_walk_forward.csv", index=False)
    RR.to_csv(run / "nodip_replay_rules.csv", index=False)
    WHY.to_csv(run / "nodip_why_pairs.csv", index=False)
    EV.to_csv(run / "nodip_events.csv", index=False)
    MO.to_csv(run / "nodip_money.csv", index=False)
    nd_table(U, tops, sel).to_parquet(run / "nodip_table.parquet", index=False)
    md = nodip_report(res, base, tables, tops, atoms, WF, verdicts, S1, WHY, EV, MO, mins, evid)
    (run / "NODIP.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    write_hashes(run, [ND_FILE, "NODIP.md", "nodip_finalists.csv", "nodip_stage1.csv", "nodip_walk_forward.csv",
                       "nodip_replay_rules.csv", "nodip_why_pairs.csv", "nodip_events.csv", "nodip_money.csv",
                       "nodip_table.parquet"])
    log("NODIP WRITTEN -> %s (%.1f min)" % (run, (time.time() - t0) / 60))
    return 0


def load_nodip(base):
    """The newest NODIP run's NODIP_CANDIDATES.json (hash-checked) -> (folder, doc) or (None, None)."""
    run = latest_run(base, "NODIP", [ND_FILE])
    if run is None:
        return None, None
    doc = json.loads((run / ND_FILE).read_text(encoding="utf-8"))
    if doc.get("sha256") != runners_hash(doc):
        raise ValueError("%s was changed after it was written - refusing" % (run / ND_FILE))
    return run, doc


def _pct(x, nd=1):
    x = _g({"x": x}, "x")
    return ("%.*f%%" % (nd, x)) if np.isfinite(x) else ""


def _tv(t, x):
    """A list's target as text: net % per trade, or a share in %."""
    return _p(x) if t == "money" else _pct(100 * _g({"x": x}, "x"))


def _td(t, x):
    """A difference of a list's target: net points, or share points."""
    return _p(x) if t == "money" else (_p(100 * _g({"x": x}, "x"), 1) + " pts" if np.isfinite(_g({"x": x}, "x")) else "")


def nodip_report(res, base, tables, tops, atoms, WF, verdicts, S1, WHY, EV, MO, mins, evid=None):
    md = ["# No-dip study v2 - which picks will not dip (%s, %s)" % (time.strftime("%d %b %Y"), VERSION), "",
          "Watchlist %s; panel %s; features %s. %s." % (res["watchlist"], res["panel"], res["features"],
                                                        res["alignment"]), "",
          "**The rule (declared before any result):** " + ND_RULE, "",
          "Shares are % of picks; net is % per trade after 0.35 pp costs. 'vs all' = the rule minus all picks of the "
          "same days. Rs a year = net x trades a year x Rs 1,000 (Rs 1 L a trade).", "",
          "**How to read the candidates (be very open, plain 95%):** with 360,000 rules some qualify by luck. Two "
          "columns separate them: 'years better than all picks' (in-sample consistency) and 'replay' - the years in "
          "which the replay chose the SAME rule from the years before, and how it did in that year against all picks "
          "(out of sample). A candidate with replay years that beat all picks has out-of-sample support; 'never "
          "chosen' = in-sample only.", "",
          "## At a glance: out of sample, apples to apples", ""]
    for t in ND_LISTS:
        v = verdicts.get(t)
        if not v:
            md.append("- **%s list:** the replay could not run (too few years)." % ND_NAME[t])
            continue
        md.append("- **%s list: %s.** Each year's rules chosen from the years before took %d picks in 2022-2026: %s "
                  "%s vs %s for all picks (difference [95%%]: %s to %s); net %s vs %s per trade (difference [95%%]: "
                  "%s to %s)." % (ND_NAME[t], v["verdict"], v["picks"], ND_WHAT[t].split(" (")[0], _tv(t, v.get(t)),
                                  _tv(t, v.get(t + "_all")), _td(t, v.get(t + "_ex_lo")), _td(t, v.get(t + "_ex_hi")),
                                  _p(v.get("money")), _p(v.get("money_all")), _p(v.get("money_ex_lo")),
                                  _p(v.get("money_ex_hi"))))
    if len(MO):
        md += ["", "Money, Rs 5 L from 2022, no MTF (out-of-sample arms: each year only rules chosen from the years "
               "before; the baseline needs no choosing; MTF 2x and 2 / 7 slots in the full table):", "",
               "| engine | book | 3 slots: a year | worst fall | trades a week | 5 slots: a year | worst fall | trades a "
               "week |", "|---|---|---:|---:|---:|---:|---:|---:|"]
        G = MO[(MO["mtf"] == "none") & ~MO["book"].str.contains("in-sample")]
        for (e, b), g in G.groupby(["engine", "book"], sort=False):
            cells = []
            for k in (3, 5):
                r = g[g["slots"] == k]
                cells += (["%s%%" % _p(r["cagr"].iloc[0], 1), "%.1f%%" % r["worst_fall"].iloc[0],
                           "%.1f" % r["per_week"].iloc[0]] if len(r) else ["", "", ""])
            md.append("| %s | %s | %s |" % (e, b, " | ".join(cells)))
    md += ["", "## Base rates (every complete pick at the D1 open, sold at the D5 close)", "",
           "| table | picks | no dip | runners | net per trade | ranks 1-3: no dip | ranks 1-3: net |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for b in base:
        md.append("| %s | %d | %.1f%% | %.1f%% | %s | %s | %s |" % (b["table"], b["picks"], b["nodip"], b["runner"],
                                                                   _p(b["net"]), _pct(b["top3_nodip"]),
                                                                   _p(b["top3_net"])))
    for t in ND_LISTS:
        T = tables[t]
        pos = {tuple(c): i for i, c in enumerate(T["cand"])} if len(T) else {}

        def line(tag, c):
            r = T.iloc[pos[tuple(c)]]
            ev = (evid or {}).get(t, {}).get(tuple(c), {})
            yb = "%d of %d" % (ev["years_better"], ev["years"]) if ev else ""
            rp = ", ".join("%d %s" % (x["year"], _td(t, x["diff"])) for x in ev.get("replay", [])) or "never chosen"
            eng = " / ".join("%s %s" % (e, _tv(t, r.get("%s_target" % e))) for e in ("D", "ENS")
                             if "%s_target" % e in r.index)
            return "| %s | %s%s | %.0f | %s [%s, %s] | %s [%s, %s] | %s | %s | %s [%s, %s] | %s | %s | %s | %s |" % (
                tag, r["text"], "" if r["qualifies"] else " (does NOT qualify)", r["per_year"],
                _tv(t, r[t]), _tv(t, r[t + "_lo"]), _tv(t, r[t + "_hi"]), _td(t, r[t + "_ex"]), _td(t, r[t + "_ex_lo"]),
                _td(t, r[t + "_ex_hi"]), _pct(100 * r["nodip"]), _pct(100 * r["runner"]), _p(r["money"]),
                _p(r["money_lo"]), _p(r["money_hi"]), eng,
                "{:,.0f}".format(r["money"] * r["per_year"] * 1000) if np.isfinite(r["money"]) else "", yb, rp)
        hdr = ("| | rule | trades a year | %s [95%%] | vs all picks [95%%] | no dip | runners | net [95%%] | D / ENS "
               "alone | Rs a year | years better than all picks | replay: chosen before the year (that year vs all) |"
               % ND_WHAT[t].split(" (")[0])
        md += ["", "## The %s list (in-sample: chosen on all the years) - target: %s" % (ND_NAME[t], ND_WHAT[t]), "",
               hdr, "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
        md += [line("%s%d" % (ND_TAG[t], i + 1), c) for i, c in enumerate(tops[t][1])] or \
            ["| | no rule qualifies |" + " |" * 10]
        md += ["", "Open list - the 10 best by score, qualified or not:", "", hdr,
               "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
        md += [line("B%d" % (i + 1), c) for i, c in enumerate(tops[t][3])]
    md += ["", "## The year-by-year replay (each year: cut-offs and rules from the years before)", "",
           "| year | list | rules chosen | picks in them | no dip in them / all | runners in them / all | net in them / "
           "all |", "|---|---|---|---:|---:|---:|---:|"]
    for r in WF.to_dict("records"):
        if "note" in r and isinstance(r.get("note"), str):
            md.append("| %s | | %s | | | | |" % (r["year"], r["note"]))
            continue
        for t in ND_LISTS:
            md.append("| %s | %s | %s | %d | %s / %s | %s / %s | %s / %s |" % (
                r["year"], ND_NAME[t], r.get(t + "_rules", ""), int(_g(r, t + "_n")) if np.isfinite(_g(r, t + "_n"))
                else 0,
                _pct(100 * _g(r, t + "_nodip")), _pct(100 * _g(r, "all_nodip")), _pct(100 * _g(r, t + "_runner")),
                _pct(100 * _g(r, "all_runner")), _p(_g(r, t + "_money")), _p(_g(r, "all_money"))))
    ok = S1[S1["n"] >= mins]
    for title, col in (("what separates the picks that do NOT dip (single conditions, by the lower bound of the "
                        "no-dip share)", "nodip_lo"), ("what marks the runners (single conditions, by the lower bound "
                                                      "of the runner share)", "runner_lo")):
        md += ["", "## Stage 1: " + title, "",
               "| condition | trades a year | no dip [lower bound] | runners [lower bound] | net [lower bound] | D no "
               "dip / net | ENS no dip / net |", "|---|---:|---:|---:|---:|---:|---:|"]
        for r in ok.sort_values(col, ascending=False).head(30).to_dict("records"):
            md.append("| %s | %.0f | %s [%s] | %s [%s] | %s [%s] | %s / %s | %s / %s |" % (
                r["text"], r["per_year"], _pct(100 * r["nodip"]), _pct(100 * r["nodip_lo"]), _pct(100 * r["runner"]),
                _pct(100 * r["runner_lo"]), _p(r["net"]), _p(r["net_lo"]), _pct(100 * _g(r, "D_nodip")),
                _p(_g(r, "D_net")), _pct(100 * _g(r, "ENS_nodip")), _p(_g(r, "ENS_net"))))
    if len(WHY):
        md += ["", "## The model's own pairs (the WHY study's interactions): the best pair of their conditions", "",
               "| features | best pair (by the no-dip lower bound) | trades | no dip [lower bound] | runners | net "
               "[lower bound] |", "|---|---|---:|---:|---:|---:|"]
        for r in WHY.to_dict("records"):
            md.append("| %s | %s | %.0f | %s [%s] | %s | %s [%s] |" % (
                r["features"], r["text"], r["n"], _pct(100 * r["nodip"]), _pct(100 * r["nodip_lo"]),
                _pct(100 * r["runner"]), _p(r["net"]), _p(r["net_lo"])))
    md += ["", "## Entries: the D1 open against the events, on the same picks", "",
           "| picks of | engine | entry | filled | per trade [95%] | against the D1 open [95%] | no dip | runners |",
           "|---|---|---|---:|---:|---:|---:|---:|"]
    for r in EV.to_dict("records"):
        md.append("| %s | %s | %s | %d of %d | %s [%s, %s] | %s [%s, %s] | %s | %s |" % (
            r["source"], r["engine"], r["entry"], r["filled"], r["picks"], _p(_g(r, "net")), _p(_g(r, "lo")),
            _p(_g(r, "hi")), _p(_g(r, "vs_open")), _p(_g(r, "vs_open_lo")), _p(_g(r, "vs_open_hi")),
            _pct(_g(r, "nodip_pct")), _pct(_g(r, "runner_pct"))))
    md += ["", "## Money in full (Rs 5 L from 2022; one position per pick; worst fall counted on closed trades)", "",
           "Dip arm: %s (S3 and its zone were chosen on these years: in-sample)." % res["dip_arm"], "",
           "| engine | book | slots | MTF | Rs 5 L became | a year | worst fall | trades a week | skipped |",
           "|---|---|---:|---|---:|---:|---:|---:|---:|"]
    for r in MO.to_dict("records"):
        md.append("| %s | %s | %d | %s | Rs %s | %s%% | %.1f%% | %.1f | %d |" % (
            r["engine"], r["book"], r["slots"], r["mtf"], "{:,.0f}".format(r["end_rs"]), _p(r["cagr"], 1),
            r["worst_fall"], r["per_week"], r["skipped"]))
    md += ["", "## Limits", "",
           "- Exploratory: thousands of rules on 2020-2026. The replay guards the search (out of sample year by year); "
           "the in-sample lists do not. Only the forward paper ledger is clean evidence.",
           "- The in-sample books use rules chosen on these years; the out-of-sample books use, each year, only rules "
           "chosen before it. The dip arm (S3 in its zone) is in-sample in every book.",
           "- Fills: the D1 open (AMO) at the open price; no taxes; MTF needs the stock on the broker's list."]
    return md


# ===================================================================================== v1.1: the entry tree
# TREE.json (shipped next to this file, never written by the tool): calm / jumpy lanes by the pick's ATR, then per
# engine - D: the best-ranked calm pick that opens at or above its signal close, everything else only through a frozen
# setup; ENS: every calm pick at the open, jumpy ones only through a frozen setup. 'tree' tags the history and compares
# each tree book with its baseline; the nightly scan names tomorrow's tree orders and keeps the forward books.
TREE_FILE = "TREE.json"
TREE_FROM = "2026-11-09"        # the evening the tree was declared: the first scan that may name tree orders
TREE_ORDER = ("S1", "S2", "S3", "C1", "C2", "C3", "N1")     # a tie between setups filling on the same open
TREE_ETF_RE = re.compile(r"(BEES|IETF|ETF)$")
TREE_SLOTS = 3
TREE_RERUNS = 200
TREE_TOL = 0.05                 # points: the history must give the declaration's numbers within this (rounding)
TREE_BOOKS = ("D baseline", "D tree", "ENS baseline", "ENS tree")
TREE_GROUPS = (("D baseline", (("D baseline", 1.0),)), ("D tree", (("D tree", 1.0),)),
               ("ENS baseline", (("ENS baseline", 1.0),)), ("ENS tree", (("ENS tree", 1.0),)),
               ("both baselines (Rs 2.5 L each)", (("D baseline", 0.5), ("ENS baseline", 0.5))),
               ("both trees (Rs 2.5 L each)", (("D tree", 0.5), ("ENS tree", 0.5))))
TREE_COLS = ["trade_id", "engine", "rank", "symbol", "sday", "i1", "o1", "sc", "c5", "lane", "etf",
             "su_id", "su_k", "su_ent", "su_ex", "su_net"]


def load_tree(path=None):
    """The tree file - shipped next to setuplab.py, never written by the tool. A changed file is refused."""
    p = Path(path) if path else Path(__file__).resolve().with_name(TREE_FILE)
    if not p.is_file():
        raise ValueError("no tree file at %s (it ships next to setuplab.py)" % p)
    doc = json.loads(p.read_text(encoding="utf-8"))
    if doc.get("sha256") != frozen_hash(doc):
        raise ValueError("%s was changed after the freeze (its sha256 does not match its content) - restore the "
                         "shipped file" % p)
    return p, doc


def etf_list(root):
    """NSE's ETF list (CACHE\\sectors\\eq_etfseclist.csv, a Symbol column) when present, else None."""
    if not root:
        return None
    p = Path(root) / "sectors" / "eq_etfseclist.csv"
    if not p.is_file():
        return None
    E = pd.read_csv(p, dtype=str)
    col = next((c for c in E.columns if str(c).strip().lower() == "symbol"), None)
    if col is None:
        raise ValueError("%s has no Symbol column - is it NSE's ETF list?" % p)
    return {str(s).strip().upper() for s in E[col].dropna() if str(s).strip()}


def tree_etf(symbols, tdoc, listed=None):
    names = {str(s).strip().upper() for s in tdoc["picks"]["etf_names"]}
    out = []
    for s in symbols:
        u = str(s).strip().upper()
        out.append(bool(TREE_ETF_RE.search(u)) or u in names or (listed is not None and u in listed))
    return np.array(out, dtype=bool)


def tree_complete(book):
    """The picks the cut-off and the history books use (as the research did): settled, every D1..D5 price, an ATR."""
    return (book.ok & np.isfinite(book.O[:, 1]) & np.isfinite(book.C[:, 1:6]).all(1) &
            np.isfinite(book.O[:, 2:6]).all(1) & np.isfinite(book.atr))


def tree_cutoff(atr, sday, complete, year, extra=None):
    """The 2/3 quantile of s_atr14 over the complete picks before 1 January of the year (+ extra ATRs, e.g. pick_meta's
    cards after the history file ends). -> (cut-off, picks used); nan when fewer than 100."""
    ref = complete & (np.asarray(sday).astype("datetime64[D]") < np.datetime64("%d-01-01" % int(year)))
    vals = np.asarray(atr, float)[ref]
    if extra is not None and len(extra):
        vals = np.concatenate([vals, np.asarray(extra, float)])
    vals = vals[np.isfinite(vals)]
    if len(vals) < 100:
        return np.nan, int(len(vals))
    return float(np.quantile(vals, 2 / 3)), int(len(vals))


def tree_cutoffs(tdoc, ledger=None):
    """year -> cut-off: the declared ones (TREE.json), then those recorded later with --cutoff-year (tree ledger)."""
    cuts = {int(k): float(v) for k, v in tdoc["lane"]["cutoffs"].items()}
    for r in (ledger_lines(ledger) if ledger else []):
        if r.get("event") == "cutoff" and int(r["year"]) not in cuts:
            cuts[int(r["year"])] = float(r["cutoff"])
    return cuts


def tree_lanes(atr, years, cuts):
    """CALM (ATR at or below the year's cut-off), JUMPY (above), NO ATR, or NO CUT-OFF (no cut-off for the year)."""
    atr, years = np.asarray(atr, float), np.asarray(years)
    lane = np.full(len(atr), "NO CUT-OFF", dtype=object)
    for y in np.unique(years):
        if int(y) in cuts:
            m = years == y
            a = atr[m]
            lane[m] = np.where(~np.isfinite(a), "NO ATR", np.where(a > cuts[int(y)], "JUMPY", "CALM"))
    return lane


def tree_first_setup(su, i1, primary):
    """su: {setup id: (filled bool, watch day k, net at the primary exit)} per pick arrays. -> the earliest fill per
    pick (a tie: TREE_ORDER): id, k, entry index (i1 + k - 1), exit index, net (nan = not settled)."""
    n = len(i1)
    sid = np.full(n, "", dtype=object)
    sk = np.zeros(n, dtype=np.int64)
    snet = np.full(n, np.nan)
    for s_ in TREE_ORDER:
        if s_ not in su:
            continue
        f, k, net = su[s_]
        k = np.asarray(k, float)
        f = np.asarray(f, bool) & np.isfinite(k)
        better = f & ((sk == 0) | (np.where(f, k, 1e9) < sk))
        sid[better], sk[better], snet[better] = s_, k[better].astype(np.int64), np.asarray(net, float)[better]
    has = sk > 0
    ent = np.where(has, np.asarray(i1) + sk - 1, -1)
    ex = np.full(n, -1, dtype=np.int64)
    for s_ in TREE_ORDER:
        m = has & (sid == s_)
        ex[m] = np.where(primary.get(s_) == "fresh", ent[m] + 4, np.asarray(i1)[m] + 4)
    return sid, sk, ent, ex, snet


def tree_plan(P, final=True):
    """The tree on the picks of ranks 1-3 (one row each; columns TREE_COLS; o1 / c5 nan = not known yet).
    -> (P with 'action' and 'how', trades: one row per traded pick, baseline: the same picks at the open)."""
    P = P.reset_index(drop=True).copy()
    n = len(P)
    o1, sc, c5 = (P[c].to_numpy(float) for c in ("o1", "sc", "c5"))
    lane, etf = P["lane"].to_numpy(dtype=object), P["etf"].to_numpy(bool)
    isD = (P["engine"] == "D").to_numpy()
    calm, nocut = lane == "CALM", lane == "NO CUT-OFF"
    known = np.isfinite(o1)
    up = known & np.isfinite(sc) & (o1 >= sc)
    act_ok = ~etf & ~nocut
    bought = np.zeros(n, dtype=bool)
    cand = isD & calm & act_ok & up
    if cand.any():                                  # D: the best-ranked calm pick that opened at or above its close
        bought[P[cand].groupby("sday")["rank"].idxmin().to_numpy()] = True
    bought |= ~isD & calm & act_ok & known          # ENS: every calm pick at the open
    elig = act_ok & ~bought & (isD | ~calm)         # through a frozen setup only
    has_su = elig & (P["su_ent"].to_numpy() >= 0)
    act = np.full(n, "", dtype=object)
    how = np.full(n, "", dtype=object)
    for i in range(n):
        if etf[i]:
            act[i] = "SKIP: ETF"
            continue
        if nocut[i]:
            act[i] = "NO CUT-OFF"
            continue
        if bought[i]:
            act[i] = "BUY AT OPEN (calm, opened up)" if isD[i] else "BUY AT OPEN (calm)"
            how[i] = "open"
            continue
        if isD[i] and calm[i]:
            if not known[i]:
                act[i] = "CALM: buy at the open if it opens at or above %.2f (the first in rank order)" % sc[i]
            elif up[i]:
                act[i] = "WAIT: calm, a better-ranked calm pick opened up"
            else:
                act[i] = "WAIT: calm, opened lower"
        elif not isD[i] and calm[i]:
            act[i] = "BUY AT OPEN (calm)"            # ENS calm, the open not known yet
            continue
        else:
            act[i] = "WAIT: no ATR" if lane[i] == "NO ATR" else "WAIT: jumpy"
        if has_su[i]:
            how[i] = "%s@D%d" % (P.at[i, "su_id"], int(P.at[i, "su_k"]))
            act[i] += " -> %s" % how[i]
        elif final or np.isfinite(c5[i]):
            act[i] += " -> no setup: skipped"
        else:
            act[i] += " (watching for a setup)"
    P["action"], P["how"] = act, how
    i1 = P["i1"].to_numpy(np.int64)
    rows = []
    op = np.flatnonzero(bought & known)
    if len(op):
        rows.append(pd.DataFrame({"row": op, "how": "open", "ent": i1[op], "ex": i1[op] + 4, "ek": 1,
                                  "net": (c5[op] / o1[op] - 1) * 100 - COST}))
    ss = np.flatnonzero(has_su)
    if len(ss):
        rows.append(pd.DataFrame({"row": ss, "how": how[ss], "ent": P["su_ent"].to_numpy(np.int64)[ss],
                                  "ex": P["su_ex"].to_numpy(np.int64)[ss], "ek": P["su_k"].to_numpy(np.int64)[ss],
                                  "net": P["su_net"].to_numpy(float)[ss]}))
    cols = ["row", "how", "ent", "ex", "ek", "net"]
    Tt = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=cols)
    bb = np.flatnonzero(~etf & known)
    Tb = pd.DataFrame({"row": bb, "how": "open", "ent": i1[bb], "ex": i1[bb] + 4, "ek": 1,
                       "net": (c5[bb] / o1[bb] - 1) * 100 - COST})
    for T_ in (Tt, Tb):
        for c in ("trade_id", "engine", "rank", "symbol"):
            T_[c] = P[c].to_numpy()[T_["row"].to_numpy(np.int64)] if len(T_) else []
    return P, Tt.sort_values(["ent", "rank"]).reset_index(drop=True), Tb.sort_values(["ent", "rank"]).reset_index(drop=True)


def tree_sim(T_, prow, O, C, i1, s0, t1, k=TREE_SLOTS):
    """A k-position book (value 1.0 at s0) on calendar indices s0..t1: each trade gets 1/k of the book's value
    (closed trades) at its entry open; all positions busy = skipped (the same open: lower rank first, then the
    symbol, then the trade id); the exit at the close frees the position from the next open.
    T_: trades (row = index into prow; ent, ex, ek, net, rank, symbol); prow: book row per trade row.
    -> (closed value, marked value: open positions at the session's close, taken trade indices)."""
    ent, ex = T_["ent"].to_numpy(np.int64), T_["ex"].to_numpy(np.int64)
    net, ek = T_["net"].to_numpy(float), T_["ek"].to_numpy(np.int64)
    rk, sy = T_["rank"].to_numpy(float), T_["symbol"].astype(str).to_numpy()
    tid = T_["trade_id"].astype(str).to_numpy() if len(T_) else np.zeros(0, dtype=object)
    br = np.asarray(prow, dtype=np.int64)[T_["row"].to_numpy(np.int64)] if len(T_) else np.zeros(0, np.int64)
    keep = np.flatnonzero((ent >= s0) & (ent <= t1))
    o = keep[np.lexsort((tid[keep], sy[keep], rk[keep], ent[keep]))]      # a full tie: the research's order (trade id)
    cash, pos, j, took = 1.0, [], 0, []
    eqc, eqm = np.empty(t1 - s0 + 1), np.empty(t1 - s0 + 1)
    for t in range(s0, t1 + 1):
        while j < len(o) and ent[o[j]] == t:
            x = o[j]
            if len(pos) < k:
                size = (cash + sum(p[1] for p in pos)) / k
                if size > 0:
                    cash -= size
                    pos.append((ex[x], size, size * net[x] / 100, br[x], O[br[x], ek[x]]))
                    took.append(x)
            j += 1
        still = []
        for p in pos:
            if p[0] <= t:
                cash += p[1] + p[2]
            else:
                still.append(p)
        pos = still
        eqc[t - s0] = cash + sum(p[1] for p in pos)
        mk = 0.0
        for p in pos:
            kk = t - i1[p[3]] + 1
            c_ = C[p[3], kk] if 1 <= kk <= PATH else np.nan
            mk += p[1] * (c_ / p[4]) if np.isfinite(c_) and np.isfinite(p[4]) and p[4] > 0 else p[1]
        eqm[t - s0] = cash + mk
    return np.maximum(eqc, 0.0), np.maximum(eqm, 0.0), np.array(took, dtype=np.int64)


def tree_stats(eqc, eqm, cal, s0, t1, tr=None, slots=TREE_SLOTS):
    """A year (closed value), worst fall and worst month (marked), the longest wait for a new high, losing months,
    year by year (marked, year ends); with tr (the taken trades): per week, win share, mean, the 1-in-20 loss,
    share of days invested, share bought through a setup."""
    yrs = float((cal[t1] - cal[s0]) / np.timedelta64(1, "D")) / 365.25
    idx = np.arange(s0, t1 + 1)
    pk = np.maximum.accumulate(eqm)
    run = best = 0
    for u in eqm < pk * (1 - 1e-9):
        run = run + 1 if u else 0
        best = max(best, run)
    dts = pd.DatetimeIndex(cal[idx])
    me = pd.Series(eqm).groupby(dts.to_period("M")).last().to_numpy()
    mr = me / np.r_[1.0, me[:-1]] - 1
    ys, prev = {}, 1.0
    for y in np.unique(dts.year):
        v = eqm[np.flatnonzero(dts.year == y)[-1]]
        ys[int(y)] = (v / prev - 1) * 100
        prev = v
    st = {"a_year": (eqc[-1] ** (1 / yrs) - 1) * 100 if eqc[-1] > 0 and yrs > 0 else np.nan, "end": float(eqc[-1]),
          "fall": float(100 * np.max(1 - eqm / pk)), "worst_month": float(100 * mr.min()),
          "wait_months": best / 21.0, "losing_months": float(100 * (mr < 0).mean()), "years": ys}
    if tr is not None and len(tr):
        cnt = np.zeros(t1 - s0 + 1)
        for a, b in zip(tr["ent"].to_numpy(), tr["ex"].to_numpy()):
            cnt[a - s0: min(b, t1) - s0 + 1] += 1
        st.update({"per_week": len(tr) / (yrs * 52.18), "win": float(100 * (tr["net"] > 0).mean()),
                   "mean": float(tr["net"].mean()), "p5": float(np.percentile(tr["net"], 5)),
                   "invested": float(100 * cnt.mean() / slots), "via_setups": float(100 * (tr["how"] != "open").mean())})
    return st


def newest_tags(out):
    """The newest TAGS run under OUT\\TAGS whose outputs.sha256 still matches -> its setup_tags.parquet frame."""
    runs = sorted((Path(out) / "TAGS").glob("TAGS_*"), reverse=True)
    for r in runs:
        hf = r / "outputs.sha256"
        if not hf.is_file() or not (r / "setup_tags.parquet").is_file():
            continue
        ok = True
        for ln in hf.read_text(encoding="utf-8").splitlines():
            h, _, nm = ln.partition("  ")
            if nm and hashlib.sha256((r / nm).read_bytes()).hexdigest() != h:
                ok = False
        if ok:
            return r, pd.read_parquet(r / "setup_tags.parquet")
    raise ValueError("no TAGS run with intact hashes under %s\\TAGS (run setuplab tag first)" % out)


def tree_history_picks(book, tags, fdoc, tdoc, cuts):
    """Every pick of the research watchlist with its lane, gap, dip / runner marks, its first frozen setup and the
    tree's inputs. -> DataFrame (one row per pick, the book's order)."""
    T = tags.set_index("trade_id")
    miss = [t for t in book.ids if t not in T.index]
    if miss:
        raise ValueError("%d picks of the watchlist are not in the TAGS run (e.g. %s) - tag this watchlist first" % (
            len(miss), miss[0]))
    T = T.loc[book.ids]
    primary = {s["id"]: s["primary_exit"] for s in fdoc["setups"]}
    su = {}
    for s_ in TREE_ORDER:
        if "su_%s_status" % s_ not in T.columns:
            continue
        f = (T["su_%s_status" % s_].astype(str) == "Filled").to_numpy()
        k = pd.to_numeric(T["su_%s_day" % s_], errors="coerce").to_numpy(float)
        net = pd.to_numeric(T["su_%s_net_%s" % (s_, "fresh" if primary.get(s_) == "fresh" else "d5")],
                            errors="coerce").to_numpy(float)
        su[s_] = (f, k, net)
    sid, sk, sent, sex, snet = tree_first_setup(su, book.i1, primary)
    comp = tree_complete(book)
    years = pd.DatetimeIndex(book.signal_day).year.to_numpy()
    lane = tree_lanes(book.atr, years, cuts)
    O1, C5 = book.O[:, 1], book.C[:, 5]
    hit = book.C[:, 1:5] <= O1[:, None] * 0.98
    dip = hit.any(axis=1)
    P = pd.DataFrame({"trade_id": book.ids, "engine": book.engine_arr, "rank": book.rank, "symbol": book.symbols,
                      "sday": book.signal_day, "i1": book.i1, "o1": O1, "sc": book.sc, "c5": C5,
                      "s_atr14": book.atr, "lane": lane, "etf": tree_etf(book.symbols, tdoc), "complete": comp,
                      "gap_pct": (O1 / book.sc - 1) * 100, "dip_2pct": dip,
                      "runner": ~dip & (C5 >= O1 * 1.05), "su_id": sid, "su_k": sk, "su_ent": sent, "su_ex": sex,
                      "su_net": np.where(sk > 0, snet, np.nan), "d1_net": (C5 / O1 - 1) * 100 - COST})
    P["opened_up"] = P["o1"] >= P["sc"]
    P["cutoff"] = [cuts.get(int(y), np.nan) for y in years]
    return P


def tree_run_books(P, book, s_):
    """The four history books on complete ranks 1-3 picks from s_: trades (settled nets only) and the plan."""
    out, plans = {}, []
    for e in ("D", "ENS"):
        m = (P["engine"] == e) & (P["rank"] <= 3) & P["complete"] & (P["sday"] >= book.cal[s_])
        Pe = P[m]
        pl, Tt, Tb = tree_plan(Pe[TREE_COLS])
        prow = Pe.index.to_numpy()                        # row in P (= the book's row)
        Tt = Tt[np.isfinite(Tt["net"].to_numpy(float))].reset_index(drop=True)
        Tb = Tb[np.isfinite(Tb["net"].to_numpy(float))].reset_index(drop=True)
        out[e + " tree"], out[e + " baseline"] = (Tt, prow), (Tb, prow)
        pl.index = Pe.index
        plans.append(pl)
    return out, pd.concat(plans)


def tree_history(book, P, books, s_, t1, reruns=TREE_RERUNS, seed=11, log=print):
    """Each book on the five start days and on the reruns; the groups (one book, or two half books)."""
    res = {g: [] for g, _ in TREE_GROUPS}
    taken_first = {}
    for p_ in range(5):
        s0 = s_ + p_
        SIM = {}
        for nm in TREE_BOOKS:
            T_, prow = books[nm]
            eqc, eqm, tk = tree_sim(T_, prow, book.O, book.C, book.i1, s0, t1)
            SIM[nm] = (eqc, eqm, T_.iloc[tk])
            if p_ == 0:
                taken_first[nm] = T_.iloc[tk]
        for g, parts in TREE_GROUPS:
            eqc = sum(w * SIM[k][0] for k, w in parts)
            eqm = sum(w * SIM[k][1] for k, w in parts)
            tr = pd.concat([SIM[k][2] for k, w in parts], ignore_index=True)
            res[g].append(tree_stats(eqc, eqm, book.cal, s0, t1, tr, slots=TREE_SLOTS * len(parts)))
    rng = np.random.default_rng(seed)
    pool = {e: book.ids[P.index[(P["engine"] == e) & (P["rank"] <= 3) & P["complete"] &
                                 (P["sday"] >= book.cal[s_])].to_numpy()] for e in ("D", "ENS")}
    rr = {g: [] for g, _ in TREE_GROUPS}
    for d in range(reruns):
        s0 = s_ + int(rng.integers(0, 5))
        drop = {e: set(rng.choice(pool[e], size=int(0.02 * len(pool[e])), replace=False)) for e in ("D", "ENS")}
        SIM = {}
        for nm in TREE_BOOKS:
            T_, prow = books[nm]
            T2 = T_[~T_["trade_id"].isin(drop[nm.split()[0]])]
            eqc, eqm, _ = tree_sim(T2, prow, book.O, book.C, book.i1, s0, t1)
            SIM[nm] = (eqc, eqm)
        yrs = float((book.cal[t1] - book.cal[s0]) / np.timedelta64(1, "D")) / 365.25
        for g, parts in TREE_GROUPS:
            eqc = sum(w * SIM[k][0] for k, w in parts)
            eqm = sum(w * SIM[k][1] for k, w in parts)
            rr[g].append(((eqc[-1] ** (1 / yrs) - 1) * 100, 100 * np.max(1 - eqm / np.maximum.accumulate(eqm))))
        if (d + 1) % 50 == 0:
            log(" reruns: %d of %d" % (d + 1, reruns))
    return res, rr, taken_first


def tree_bunch(P, plan):
    """For a pick bought through a setup: how many OTHER setup entries of the same engine's ranks 1-3 fell in the 3
    sessions before its entry or on the same open (the sell-off measure). nan otherwise."""
    out = pd.Series(np.nan, index=P.index)
    m = (P["rank"] <= 3) & (P["su_ent"] >= 0)
    for e in ("D", "ENS"):
        g = P[m & (P["engine"] == e)]
        E = np.sort(g["su_ent"].to_numpy(np.int64))
        for i, x in zip(g.index, g["su_ent"].to_numpy(np.int64)):
            out.at[i] = int(np.searchsorted(E, x, side="right") - np.searchsorted(E, x - 3, side="left")) - 1
    return out


def tree_md(tdoc, res, rr, ref_ok, cuts_data, cut_check, window, plan_counts):
    """TREE.md - the history comparison (the same tables as the chat of 9 Nov)."""
    a = {g: {k: np.mean([d[k] for d in L], 0) if k != "years" else None for k in L[0]} for g, L in res.items()}
    rng_ = {g: (min(d["a_year"] for d in L), max(d["a_year"] for d in L)) for g, L in res.items()}
    yrs = sorted(res["D tree"][0]["years"])
    yv = {g: {y: np.mean([d["years"][y] for d in L]) for y in yrs} for g, L in res.items()}
    G = [g for g, _ in TREE_GROUPS]
    md = ["# The entry tree - history (%s)" % VERSION, "",
          "TREE.json sha256 `%s` (frozen %s). Window %s .. %s, Rs 5 L per book, %d positions, no MTF, %.2f pp costs; "
          "each number is the average of the first five sessions as start days; worst fall = the book marked daily; "
          "both = two books of Rs 2.5 L." % (tdoc["sha256"][:16], tdoc["frozen_at"], window[0], window[1],
                                             TREE_SLOTS, COST), "",
          "**%s**" % ("RECONCILED: the same numbers as the declaration's history (within %.2f points)." % TREE_TOL
                      if ref_ok else "DIFFERS from the declaration's history - expected only with another watchlist "
                                     "or TAGS run (e.g. later dates); otherwise send this file."), "",
          "Cut-offs (jumpy = s_atr14 above): " + "; ".join("%d %.4f%%%s" % (y, 100 * v, "" if y not in cut_check else
                                                            " (declared %.4f%%: %s)" % (100 * cut_check[y][0], "same" if
                                                            cut_check[y][1] else "DIFFERS"))
                                                            for y, v in sorted(cuts_data.items())), "",
          "## Money", "", "| | " + " | ".join(G) + " |", "|---|" + "---:|" * len(G)]
    rows = [("A year", lambda g: "%+.1f%% (%+.0f..%+.0f)" % (a[g]["a_year"], rng_[g][0], rng_[g][1])),
            ("Rs 5 L became", lambda g: "Rs %.1f L" % (5 * a[g]["end"])),
            ("Worst fall (marked daily)", lambda g: "%.1f%%" % a[g]["fall"]),
            ("Worst month", lambda g: "%+.1f%%" % a[g]["worst_month"]),
            ("Longest wait for a new high", lambda g: "%.1f months" % a[g]["wait_months"]),
            ("Losing months", lambda g: "%.0f%%" % a[g]["losing_months"])]
    for lab, f in rows:
        md.append("| %s | " % lab + " | ".join(f(g) for g in G) + " |")
    md += ["", "## Year by year (marked, year ends)", "", "| | " + " | ".join(G) + " |", "|---|" + "---:|" * len(G)]
    for y in yrs:
        md.append("| %d | " % y + " | ".join("%+.0f%%" % yv[g][y] for g in G) + " |")
    md += ["", "## Trades", "", "| | " + " | ".join(G) + " |", "|---|" + "---:|" * len(G)]
    for lab, k, fmt in (("Trades a week", "per_week", "%.1f"), ("Trades that win", "win", "%.0f%%"),
                        ("Mean trade", "mean", "%+.2f%%"), ("1 trade in 20 loses at least", "p5", "%.1f%%"),
                        ("Days invested", "invested", "%.0f%%"), ("Bought through a setup", "via_setups", "%.0f%%")):
        md.append("| %s | " % lab + " | ".join(fmt % (-a[g][k] if k == "p5" else a[g][k]) for g in G) + " |")
    md += ["", "## %d reruns (a random start day of the five, the same random 2%% of each engine's picks dropped "
               "from every book)" % len(rr["D tree"]), "",
           "| | median a year | 1 run in 10 below | median worst fall | 1 run in 10 above | beats its baseline |",
           "|---|---:|---:|---:|---:|---:|"]
    base_of = {"D tree": "D baseline", "ENS tree": "ENS baseline",
               "both trees (Rs 2.5 L each)": "both baselines (Rs 2.5 L each)"}
    for g in G:
        c = np.array([x[0] for x in rr[g]])
        f = np.array([x[1] for x in rr[g]])
        b = base_of.get(g)
        md.append("| %s | %+.1f%% | %+.1f%% | %.1f%% | %.1f%% | %s |" % (
            g, np.median(c), np.percentile(c, 10), np.median(f), np.percentile(f, 90),
            "%.0f%%" % (100 * (c > np.array([x[0] for x in rr[b]])).mean()) if b else "-"))
    md += ["", "## The tree's actions on the complete ranks 1-3 picks in the window", "",
           "| engine | action | picks |", "|---|---|---:|"]
    for (e, k), v in plan_counts.items():
        md.append("| %s | %s | %d |" % (e, k, v))
    md += ["", "In-sample: the frozen setups and the tree were chosen on this history. Only the forward paper ledger "
               "is clean evidence (TREE.json, forward_rule). The rupee totals assume unlimited liquidity.", ""]
    return md


def tree_record_cutoff(a, tdoc, book, comp, log=print):
    """--cutoff-year YYYY: the year's cut-off from the history watchlist plus pick_meta's cards after it, recorded once
    in OUT\\scan\\tree_ledger.jsonl (hash-chained)."""
    y = int(a.cutoff_year)
    tl = Path(a.out) / "scan" / "tree_ledger.jsonl"
    tl.parent.mkdir(parents=True, exist_ok=True)
    have = tree_cutoffs(tdoc, tl)
    if y in have:
        print("REFUSED: %d already has a cut-off (%.6f) - it is never changed" % (y, have[y]))
        return 3
    last = pd.Timestamp(np.max(book.signal_day))
    extra = []
    if a.root:
        fw = Path(a.root) / "research2" / "pick_meta" / "forward"
        for p in sorted(fw.glob("PM_cards_*.csv")):
            d = pd.Timestamp(p.stem.split("_")[-1])
            if last < d < pd.Timestamp("%d-01-01" % y):
                df = pd.read_csv(p)
                low = {c.lower(): c for c in df.columns}
                if "s_atr14" in low and "rank" in low:
                    extra += [float(v) for v in pd.to_numeric(df[low["s_atr14"]], errors="coerce") if np.isfinite(v)]
    v, nused = tree_cutoff(book.atr, book.signal_day, comp, y, np.array(extra))
    if not np.isfinite(v):
        print("REFUSED: too few picks before %d to set a cut-off (%d)" % (y, nused))
        return 3
    rec = {"event": "cutoff", "year": y, "cutoff": v, "picks": nused, "history_to": str(last.date()),
           "cards_after_history": len(extra), "recorded_at": _dt.datetime.now(IST).isoformat(timespec="seconds"),
           "tool": VERSION, "tree_sha256": tdoc["sha256"]}
    ledger_append(tl, rec)
    log("%s: cut-off %d = %.6f (s_atr14; %d picks: history to %s + %d from pick_meta's cards) -> %s" % (
        VERSION, y, v, nused, last.date(), len(extra), tl))
    print("CUTOFF RECORDED %d %.6f" % (y, v))
    return 0


def cmd_tree(a, log=print):
    """History: every pick of the research watchlist tagged with its lane and the tree's action; the four books and
    their comparison (TREE.md). With --cutoff-year: record that year's cut-off for the nightly scan."""
    try:
        tp, tdoc = load_tree(a.tree or None)
        fp, fdoc = load_frozen(a.frozen or None)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    try:
        book = load(a.data, None, None)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    comp = tree_complete(book)
    if a.cutoff_year:
        return tree_record_cutoff(a, tdoc, book, comp, log)
    try:
        trun, tags = (Path(a.tags), pd.read_parquet(Path(a.tags) / "setup_tags.parquet")) if a.tags else \
            newest_tags(a.out)
    except (ValueError, OSError) as e:
        print("REFUSED: %s" % e)
        return 3
    years = pd.DatetimeIndex(book.signal_day).year.to_numpy()
    declared = {int(k): float(v) for k, v in tdoc["lane"]["cutoffs"].items()}
    cuts, cut_check = {}, {}
    for y in sorted(set(int(x) for x in years)):
        v, _ = tree_cutoff(book.atr, book.signal_day, comp, y)
        if np.isfinite(v):
            cuts[y] = v
            if y in declared:
                cut_check[y] = (declared[y], abs(declared[y] - v) < 1e-9)
        elif y in declared:
            cuts[y] = declared[y]                 # too little earlier history in this file: the declared cut-off
    try:
        P = tree_history_picks(book, tags, fdoc, tdoc, cuts)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    lane_years = sorted(y for y in cuts if (years == y).any())
    if not lane_years:
        print("REFUSED: no year of the watchlist has a cut-off")
        return 3
    s_ = int(np.searchsorted(book.cal, np.datetime64("%d-01-01" % lane_years[0])))
    books, plan = tree_run_books(P, book, s_)
    t1 = int(min(len(book.cal) - 1, max(int(b[0]["ex"].max()) for b in books.values() if len(b[0]))))
    run = new_run_dir(Path(a.out) / "TREE", "TREE")
    log("%s tree: TREE.json sha256 %s; freeze %s; watchlist %s (%d picks); tags %s; window %s .. %s -> %s" % (
        VERSION, tdoc["sha256"][:16], fdoc["sha256"][:16], a.data, book.n, trun.name, pd.Timestamp(book.cal[s_]).date(),
        pd.Timestamp(book.cal[t1]).date(), run))
    res, rr, taken = tree_history(book, P, books, s_, t1, reruns=a.reruns, log=log)
    window = [str(pd.Timestamp(book.cal[s_]).date()), str(pd.Timestamp(book.cal[t1]).date())]
    ref = tdoc.get("history_reference", {})
    ref_ok = window == ref.get("window") and all(
        abs(np.mean([d["a_year"] for d in res[g]]) - ref[g]["a_year_pct"]) <= TREE_TOL and
        abs(np.mean([d["fall"] for d in res[g]]) - ref[g]["worst_fall_pct"]) <= TREE_TOL
        for g, _ in TREE_GROUPS if g in ref)
    # tags: every pick, the tree's action on ranks 1-3 in the window, and the start-day-1 book's trades
    P["bunch"] = tree_bunch(P, plan)
    P["action"], P["how"] = "", ""
    P.loc[plan.index, "action"] = plan["action"]
    P.loc[plan.index, "how"] = plan["how"]
    P["in_book_start1"] = P["trade_id"].isin(set(taken["D tree"]["trade_id"]) | set(taken["ENS tree"]["trade_id"]))
    P["first_setup"] = np.where(P["su_k"] > 0, P["su_id"] + "@D" + P["su_k"].astype(str), "")
    P["signal_day"] = pd.DatetimeIndex(P["sday"]).strftime("%Y-%m-%d")
    out_cols = ["trade_id", "engine", "rank", "symbol", "signal_day", "s_atr14", "cutoff", "lane", "etf", "gap_pct",
                "opened_up", "dip_2pct", "runner", "first_setup", "su_net", "bunch", "d1_net", "action", "how",
                "in_book_start1", "complete"]
    Tg = P[out_cols].rename(columns={"su_net": "setup_net"})
    Tg.to_parquet(run / "tree_tags.parquet", index=False)
    Tg.to_csv(run / "tree_tags.csv", index=False)
    trades = []
    for nm, tk in taken.items():
        x = tk.copy()
        x["book"] = nm
        x["entry_date"] = _days(book, x["ent"].to_numpy())
        x["exit_date"] = _days(book, x["ex"].to_numpy())
        trades.append(x[["book", "trade_id", "engine", "rank", "symbol", "how", "entry_date", "exit_date", "net"]])
    pd.concat(trades, ignore_index=True).to_csv(run / "tree_trades.csv", index=False)
    counts = {}
    for (e, act), g in plan.groupby([plan["engine"], plan["action"].str.replace(r" -> [SCN][0-9]@D[0-9]", " -> a setup",
                                                                               regex=True)]):
        counts[(e, act)] = len(g)
    md = tree_md(tdoc, res, rr, ref_ok, cuts, cut_check, window, counts)
    (run / "TREE.md").write_text("\n".join(md), encoding="utf-8")
    meta = {"version": VERSION, "made": _dt.datetime.now(IST).isoformat(timespec="seconds"), "tree_file": str(tp),
            "tree_sha256": tdoc["sha256"], "frozen_sha256": fdoc["sha256"], "tags_run": str(trun),
            "watchlist": str(Path(a.data) / "watchlist.parquet"), "window": window, "reconciled": bool(ref_ok),
            "cutoffs": {str(k): v for k, v in cuts.items()},
            "books": {g: {"a_year_pct": float(np.mean([d["a_year"] for d in L])),
                          "worst_fall_pct": float(np.mean([d["fall"] for d in L])),
                          "rs_5l_became_lakh": float(5 * np.mean([d["end"] for d in L]))} for g, L in res.items()}}
    (run / "TREE_RUN.json").write_text(json.dumps(meta, indent=1, default=str), encoding="utf-8")
    write_hashes(run, ["tree_tags.parquet", "tree_tags.csv", "tree_trades.csv", "TREE.md", "TREE_RUN.json"])
    for g in ("D tree", "ENS tree", "both trees (Rs 2.5 L each)"):
        log(" %-28s %+.1f%% a year, worst fall %.1f%%" % (g, meta["books"][g]["a_year_pct"],
                                                          meta["books"][g]["worst_fall_pct"]))
    log(" wrote %s" % run)
    print("TREE %s" % ("RECONCILED" if ref_ok else "WRITTEN (differs from the declaration's history)"))
    return 0


# ---- the nightly part (called by the scan)
def tree_atr(data, picks, T):
    """s_atr14 for the evening's picks: pick_meta's card, else the simple ATR from the stock's bars."""
    card = pm_atr(data.root, T)
    atr = np.full(len(picks), np.nan)
    src = np.full(len(picks), "", dtype=object)
    for i, r in enumerate(picks.itertuples(index=False)):
        v = card.get((str(r.engine), int(r.rank), str(r.symbol)))
        if v is not None and np.isfinite(v):
            atr[i], src[i] = v, "pick_meta"
    need = np.flatnonzero(~np.isfinite(atr))
    if len(need) and hasattr(data, "ohlcv"):
        bars = data.ohlcv(sorted({str(picks.iloc[i]["symbol"]) for i in need}))
        Td = np.datetime64(pd.Timestamp(T).date(), "D")
        for i in need:
            b = bars.get(str(picks.iloc[i]["symbol"]))
            if b is None:
                continue
            dates = np.asarray(b[0]).astype("datetime64[D]")
            j = int(np.searchsorted(dates, Td))
            if j < len(dates) and dates[j] == Td:
                atr[i], src[i] = atr_simple(b[2], b[3], b[4])[j], "bars"
    return atr, src


def tree_inputs(Lp, data, T, F, fdoc, tdoc, cuts, listed):
    """The tree's inputs for paper picks (signal days up to T): a live book of their prices, lanes, ETF marks, the
    first frozen setup the setup scan named on time and the bars confirmed. -> (P with TREE_COLS, book)."""
    Lp = Lp.copy()
    Lp["trade_id"] = ["%s-%s-%d" % (e, pd.Timestamp(d).strftime("%Y%m%d"), r)
                      for e, d, r in zip(Lp["engine"], Lp["signal_day"], Lp["rank"])]
    bars = data.bars(sorted(Lp["symbol"].unique()))
    book, kstar, dropped = live_book(Lp[["trade_id", "engine", "rank", "symbol", "signal_day"]], bars, data.cal, T,
                                     data.root)
    if book is None:
        return None, None, dropped
    atr = np.full(book.n, np.nan)
    src = np.full(book.n, "", dtype=object)
    for d in np.unique(book.signal_day):
        m = np.flatnonzero(book.signal_day == d)
        sub = pd.DataFrame({"engine": book.engine_arr[m], "rank": book.rank[m], "symbol": book.symbols[m]})
        atr[m], src[m] = tree_atr(data, sub, d)
    primary = {s["id"]: s["primary_exit"] for s in fdoc["setups"]}
    su = {}
    if F is not None and len(F):
        E = F[F["entered"].astype(bool)]
        for s_ in TREE_ORDER:
            g = E[E["setup"] == s_].set_index("trade_id")
            f = np.array([t in g.index for t in book.ids])
            k = np.array([float(g.at[t, "named_watch_day"]) if t in g.index else np.nan for t in book.ids])
            net = np.array([float(g.at[t, "net_primary"]) if t in g.index else np.nan for t in book.ids])
            su[s_] = (f, k, net)
    sid, sk, sent, sex, snet = tree_first_setup(su, book.i1, primary)
    years = pd.DatetimeIndex(book.signal_day).year.to_numpy()
    P = pd.DataFrame({"trade_id": book.ids, "engine": book.engine_arr, "rank": book.rank, "symbol": book.symbols,
                      "sday": book.signal_day, "i1": book.i1, "o1": book.O[:, 1], "sc": book.PC[:, 1],
                      "c5": book.C[:, 5], "lane": tree_lanes(atr, years, cuts),
                      "etf": tree_etf(book.symbols, tdoc, listed), "su_id": sid, "su_k": sk, "su_ent": sent,
                      "su_ex": sex, "su_net": np.where(sk > 0, snet, np.nan), "s_atr14": atr, "atr_source": src})
    return P, book, dropped


def tree_evening(T, tdoc, fdoc, L, data, S, F, out, listed=None, now=None, log=print, since=TREE_FROM):
    """One evening: tonight's tree orders (recorded once in tree_ledger.jsonl, ON TIME before 09:00 IST of the next
    session), the forward books rebuilt from the on-time records, and the page section. -> (text, record)."""
    T = np.datetime64(pd.Timestamp(T).date(), "D")
    tl = Path(out) / "tree_ledger.jsonl"
    cuts = tree_cutoffs(tdoc, tl)
    y = int(pd.Timestamp(T).year)
    d = str(pd.Timestamp(T).date())
    if y not in cuts:
        return ("## Tree - NO ORDERS tonight\n\nNo cut-off for %d. Record it once, before the year's first session:\n"
                "`python setuplab.py tree --data C:\\QuantData\\setuplab\\WL_R1_10 --out C:\\QuantData\\setuplab "
                "--root %%CACHE_DAILY_ROOT%% --cutoff-year %d`\n" % (y, y)), None
    cal = data.cal
    iT = int(np.searchsorted(cal, T, side="right")) - 1
    first = cal[max(0, iT - SCAN_BACK)]
    Lr = L[(L["signal_day"] >= pd.Timestamp(first)) & (L["signal_day"] <= pd.Timestamp(T))]
    P, book, dropped = tree_inputs(Lr, data, T, F, fdoc, tdoc, cuts, listed)
    if P is None:
        return "## Tree\n\nNo paper picks in the last five sessions.\n", None
    tonight = P[P["sday"] == T]
    now = now or _dt.datetime.now(IST)
    dl = on_time_deadline(T, cal)
    r13 = tonight[tonight["rank"] <= 3]
    order_D = r13[(r13["engine"] == "D") & (r13["lane"] == "CALM") & ~r13["etf"]].sort_values("rank")
    buys_E = r13[(r13["engine"] == "ENS") & (r13["lane"] == "CALM") & ~r13["etf"]].sort_values("rank")
    # tonight's setup buys the tree takes: ranks 1-3, not an ETF, a lane; D: not bought at its open by the tree, ENS:
    # not calm; a pick already in (or past) a position through its first setup takes no second one
    plan_now = tree_plan(P[P["rank"] <= 3][TREE_COLS], final=False)[0] if len(P) else pd.DataFrame()
    bought_open = set(plan_now.loc[plan_now["how"] == "open", "trade_id"]) if len(plan_now) else set()
    iTb = int(np.searchsorted(book.cal, T, side="right")) - 1
    had_setup = set(P.loc[(P["su_k"] > 0) & (P["su_ent"] <= iTb), "trade_id"])
    lane_of = dict(zip(P["trade_id"], P["lane"]))
    act = pd.DataFrame()
    if S is not None and len(S):
        a_ = S[S["status"].isin(["FIRES", "ARMED"]) & (S["rank"].astype(int) <= 3)].copy()
        # masks as numpy arrays: an empty pandas mask of object dtype would select columns instead of rows
        tid = a_["trade_id"].astype(str).to_numpy()
        eng = a_["engine"].astype(str).to_numpy()
        ln = np.array([lane_of.get(t, "NO CUT-OFF") for t in tid], dtype=object)
        etfs = list(set(P.loc[P["etf"], "trade_id"]))
        keep = ((eng == "D") & ~np.isin(tid, list(bought_open))) | ((eng == "ENS") & ~np.isin(ln, ["CALM", "NO CUT-OFF"]))
        keep &= (ln != "NO CUT-OFF") & ~np.isin(tid, etfs) & ~np.isin(tid, list(had_setup))
        act = a_[np.asarray(keep, dtype=bool)]
        if len(act):
            # one buy per pick: its named setups in the freeze's order up to the first that FIRES (a sure fill); the
            # first of them that fills at the open is the pick's setup (and sets its exit)
            act = act.assign(_o=act["setup"].map({s_: i for i, s_ in enumerate(TREE_ORDER)}).to_numpy())
            act = act.sort_values(["engine", "rank", "symbol", "trade_id", "_o"]).reset_index(drop=True)
            f_ = (act["status"].to_numpy() == "FIRES").astype(int)
            before = pd.Series(f_).groupby(act["trade_id"].to_numpy()).cumsum().to_numpy() - f_
            act = act[before == 0].drop(columns="_o").reset_index(drop=True)
            # tonight's D calm picks: the setup only if the pick was not the calm buy at the same open
            act = act.assign(calm_first=act["trade_id"].isin(set(order_D["trade_id"])).to_numpy(dtype=bool))
    # the record (once per evening): tonight's picks with lane and close, and every order the page names
    rec = {"event": "tree", "scan_date": d, "recorded_at": now.isoformat(timespec="seconds"),
           "deadline": dl.isoformat(timespec="minutes"), "on_time": now < dl, "tool": VERSION,
           "tree_sha256": tdoc["sha256"], "frozen_sha256": fdoc["sha256"], "cutoff": cuts[y],
           "picks": [{"trade_id": r.trade_id, "engine": r.engine, "rank": int(r.rank), "symbol": r.symbol,
                      "s_atr14": None if not np.isfinite(r.s_atr14) else round(float(r.s_atr14), 6),
                      "lane": r.lane, "etf": bool(r.etf), "close": None if not np.isfinite(r.sc) else
                      round(float(r.sc), 4)} for r in tonight.sort_values(["engine", "rank"]).itertuples()],
           "orders": {"D_calm_in_rank_order": list(order_D["trade_id"]), "ENS_calm_at_open": list(buys_E["trade_id"]),
                      "setup_buys": [{"trade_id": r.trade_id, "engine": r.engine, "setup": r.setup,
                                      "status": r.status, "rule_at_open": str(r.rule_at_open),
                                      "unless_calm_buy": bool(r.calm_first)} for r in act.itertuples()]
                      if len(act) else []}}
    old = [r for r in ledger_lines(tl) if r.get("event") == "tree" and r.get("scan_date") == d]
    if not old:
        ledger_append(tl, rec)
    else:
        rec = old[0]
    # the forward books: picks of every on-time tree record up to tonight
    recs = [r for r in ledger_lines(tl) if r.get("event") == "tree" and r.get("on_time") and since <= r[
        "scan_date"] <= d]
    fw = tree_forward(recs, L, data, T, F, fdoc, tdoc, cuts, listed)
    # tonight's tags (ranks 1-10) and the CSV
    tags = tonight.sort_values(["engine", "rank"]).copy()
    pn = tree_plan(tags[tags["rank"] <= 3][TREE_COLS], final=False)[0]
    tags["tree"] = ""
    tags.loc[tags["rank"] <= 3, "tree"] = pn["action"].to_numpy()
    tags["tree"] = tags["tree"].where(tags["rank"] <= 3, "(rank 4-10: no tree action)")
    csv = Path(out) / ("tree_%s.csv" % pd.Timestamp(T).strftime("%Y%m%d"))
    tags[["trade_id", "engine", "rank", "symbol", "s_atr14", "atr_source", "lane", "etf", "sc", "tree"]].rename(
        columns={"sc": "close_tonight"}).to_csv(csv, index=False)
    if fw is not None and len(fw["trades"]):
        fw["trades"].to_csv(Path(out) / "tree_book.csv", index=False)
    sell = {e: int(((S["engine"] == e) & S["status"].isin(["FIRES", "ARMED"]) & (S["rank"].astype(int) <= 3)).sum())
            if S is not None and len(S) else 0 for e in ("D", "ENS")}
    text = tree_section(T, tdoc, rec, cuts[y], order_D, buys_E, act, tags, fw, sell)
    return text, rec


def tree_forward(recs, L, data, T, F, fdoc, tdoc, cuts, listed):
    """The forward books from the on-time tree records: the tree's trades on those evenings' ranks 1-3 picks (with
    the setup scan's on-time entries) and the baseline on the same picks, each a 3-position book from the first
    record's next session to T. -> dict or None."""
    if not recs:
        return None
    ids = {x["trade_id"] for r in recs for x in r["picks"] if int(x["rank"]) <= 3}
    Lp = L.copy()
    Lp["trade_id"] = ["%s-%s-%d" % (e, pd.Timestamp(d).strftime("%Y%m%d"), r)
                      for e, d, r in zip(Lp["engine"], Lp["signal_day"], Lp["rank"])]
    Lp = Lp[Lp["trade_id"].isin(ids)]
    P, book, _ = tree_inputs(Lp.drop(columns="trade_id"), data, T, F, fdoc, tdoc, cuts, listed)
    if P is None:
        return None
    lanes = {x["trade_id"]: x["lane"] for r in recs for x in r["picks"]}       # the lane the record named
    P["lane"] = [lanes.get(t, l) for t, l in zip(P["trade_id"], P["lane"])]
    Td = np.datetime64(pd.Timestamp(T).date(), "D")
    t1 = int(np.searchsorted(book.cal, Td, side="right")) - 1
    s0 = int(P["i1"].min())
    out = {"first": str(pd.Timestamp(np.min(P["sday"])).date()), "books": {}, "trades": []}
    plan, Tt, Tb = tree_plan(P[TREE_COLS], final=False)
    out["plan"], out["cand_tree"], out["cand_base"], out["book"], out["P"], out["t1"] = plan, Tt, Tb, book, P, t1
    for e in ("D", "ENS"):
        for nm, T_ in (("tree", Tt), ("baseline", Tb)):
            T2 = T_[T_["engine"] == e].reset_index(drop=True)
            T2 = T2[T2["ent"] <= t1].reset_index(drop=True)
            if s0 > t1 or not len(T2):
                out["books"]["%s %s" % (e, nm)] = {"value": 1.0, "marked": 1.0, "held": pd.DataFrame(), "closed": 0,
                                                   "mean": np.nan, "win": np.nan, "taken": pd.DataFrame()}
                continue
            eqc, eqm, tk = tree_sim(T2, P.index.to_numpy(), book.O, book.C, book.i1, s0, t1)
            X = T2.iloc[tk].copy()
            X["book"] = "%s %s" % (e, nm)
            X["entry_date"] = _days(book, X["ent"].to_numpy())
            X["exit_date"] = _days(book, X["ex"].to_numpy())
            X["entry"] = [float(book.O[P.index.to_numpy()[r], k]) for r, k in zip(X["row"], X["ek"])]
            X["status"] = np.where(X["ex"] <= t1, "closed", "held")
            mk = []
            for r, en in zip(X["row"], X["entry"]):
                br = P.index.to_numpy()[r]
                kk = t1 - book.i1[br] + 1
                c_ = book.C[br, kk] if 1 <= kk <= PATH else np.nan
                mk.append((c_ / en - 1) * 100 if np.isfinite(c_) else np.nan)
            X["now_pct"] = np.where(X["status"] == "held", mk, np.nan)
            X["net"] = np.where(X["status"] == "closed", X["net"], np.nan)
            cl = X[X["status"] == "closed"]
            out["books"]["%s %s" % (e, nm)] = {"value": float(eqc[-1]), "marked": float(eqm[-1]),
                                               "held": X[X["status"] == "held"], "closed": len(cl),
                                               "mean": float(cl["net"].mean()) if len(cl) else np.nan,
                                               "win": float(100 * (cl["net"] > 0).mean()) if len(cl) else np.nan,
                                               "taken": X, "next_exit": X[(X["status"] == "held") & (X["ex"] == t1 + 1)]}
            out["trades"].append(X[["book", "trade_id", "engine", "rank", "symbol", "how", "entry_date", "entry",
                                    "exit_date", "status", "net", "now_pct"]])
    out["trades"] = pd.concat(out["trades"], ignore_index=True) if out["trades"] else pd.DataFrame()
    return out


def tree_section(T, tdoc, rec, cut, order_D, buys_E, act, tags, fw, sell):
    """The page section: the next open's tree orders per book, what each book holds, tonight's tags, the scoreboard."""
    d = str(pd.Timestamp(T).date())
    L = ["## Tree - orders for the next open (tonight %s)" % d, "",
         "TREE.json sha256 `%s`; %d cut-off: jumpy = s_atr14 above %.2f%% of the close. Recorded %s - %s." % (
             tdoc["sha256"][:16], pd.Timestamp(T).year, 100 * cut, rec["recorded_at"],
             "ON TIME" if rec["on_time"] else "LATE: counts for nothing"), ""]
    for e in ("D", "ENS"):
        bk = (fw or {}).get("books", {}).get("%s tree" % e) if fw else None
        held = bk["held"] if bk is not None and len(bk.get("held", [])) else pd.DataFrame()
        free = TREE_SLOTS - len(held)
        L += ["### %s book - %d of %d positions held tonight; %d free at the next open" % (
            e, len(held), TREE_SLOTS, max(free, 0)), ""]
        if e == "D":
            L += ["**Buy at the open: the FIRST of these that opens at or above tonight's close** (compare the pre-open "
                  "price with the close, 09:00-09:07):", ""]
            if len(order_D):
                L += ["| try | stock | rank | lane (ATR) | tonight's close |", "|---:|---|---:|---|---:|"]
                for i, r in enumerate(order_D.itertuples(), 1):
                    L.append("| %d | %s | %d | CALM (%.2f%%) | %.2f |" % (i, r.symbol, r.rank, 100 * r.s_atr14, r.sc))
            else:
                L.append("No calm pick tonight - no open buy.")
        else:
            L += ["**Buy at the open (every calm pick):**", ""]
            if len(buys_E):
                L += ["| stock | rank | lane (ATR) | tonight's close |", "|---|---:|---|---:|"]
                for r in buys_E.itertuples():
                    L.append("| %s | %d | CALM (%.2f%%) | %.2f |" % (r.symbol, r.rank, 100 * r.s_atr14, r.sc))
            else:
                L.append("No calm pick tonight - no open buy.")
        L.append("")
        a = act[act["engine"] == e] if len(act) else act
        L += ["**Frozen-setup buys the tree takes** (%s):" % ("any top-3 pick not bought at its open" if e == "D" else
                                                              "jumpy top-3 picks only"), ""]
        if len(a):
            L += ["| setup | what to do | stock | rank | signal day | watch day | tonight's close |",
                  "|---|---|---|---:|---|---:|---:|"]
            for r in a.itertuples():
                what = "BUY at the open" if r.status == "FIRES" else "BUY at the open only if %s" % r.rule_at_open
                if getattr(r, "calm_first", False):
                    what += " - unless you bought it above as the calm buy"
                L.append("| %s | %s | %s | %d | %s | D%s | %.2f |" % (r.setup, what, r.symbol, int(r.rank),
                                                                      r.signal_day, r.next_watch_day, r.close_tonight))
            if a["trade_id"].duplicated().any():
                L += ["", "A stock listed more than once: buy it once - the first of its rows (in this order) that "
                          "fills is its setup and sets its exit day."]
        else:
            L.append("None tonight.")
        L.append("")
        if len(held):
            L += ["**Held** (sell at the exit day's close):", "",
                  "| stock | how | bought | price | exit day | now % |", "|---|---|---|---:|---|---:|"]
            for r in held.itertuples():
                L.append("| %s | %s | %s | %.2f | %s | %s |" % (r.symbol, r.how, r.entry_date, r.entry, r.exit_date,
                                                                "%+.2f" % r.now_pct if np.isfinite(r.now_pct) else "-"))
            nx = bk.get("next_exit", pd.DataFrame())
            if len(nx):
                L.append("")
                L.append("**Sell at the next close:** " + ", ".join(nx["symbol"]))
            L.append("")
    L += ["More buys than free positions in a book: take them by rank (1 first), then the stock name A-Z; skip the "
          "rest. Each buy = 1/3 of the book's closed-trade value. (The backtest did exactly this.)", ""]
    L += ["### Tonight's tags (ranks 1-10)", "", "| engine | rank | stock | ATR % | lane | tree |",
          "|---|---:|---|---:|---|---|"]
    for r in tags.itertuples():
        L.append("| %s | %d | %s | %s | %s%s | %s |" % (r.engine, r.rank, r.symbol,
                                                        "%.2f" % (100 * r.s_atr14) if np.isfinite(r.s_atr14) else "-",
                                                        r.lane, " (ETF)" if r.etf else "", r.tree))
    L += ["", "Sell-off meter: frozen-setup buys named for the next open among ranks 1-3 - D %d, ENS %d. (In 2020-26 "
              "a setup trade made more when several fired within a few days; in-sample, a reference only.)" % (
                  sell["D"], sell["ENS"]), ""]
    L += ["### Scoreboard since %s (paper, on-time evenings only; Rs 5 L per book)" % (fw["first"] if fw else d), ""]
    if fw:
        L += ["| book | value now (marked) | closed trades | mean net per closed trade | trades that win |",
              "|---|---:|---:|---:|---:|"]
        for nm in ("D tree", "D baseline", "ENS tree", "ENS baseline"):
            b = fw["books"].get(nm)
            if b is None:
                continue
            L.append("| %s | Rs %.2f L | %d | %s | %s |" % (nm, 5 * b["marked"], b["closed"],
                                                           "%+.2f%%" % b["mean"] if np.isfinite(b["mean"]) else "-",
                                                           "%.0f%%" % b["win"] if np.isfinite(b["win"]) else "-"))
    else:
        L.append("No on-time tree evening yet.")
    L += ["", "Rules: TREE.json (D: the best-ranked calm pick that opens up, the rest only through a frozen setup; "
              "ENS: calm picks at the open, jumpy ones only through a frozen setup; ETFs skipped; 3 positions per "
              "book; month 6 a first read, month 12 decides).", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="setuplab")
    ap.add_argument("command", nargs="?", choices=("run", "reproduce", "build", "tag", "scan", "frozen", "zones",
                                                       "runners", "nodip", "tree"))
    ap.add_argument("--ranks", default="", help="run: only these ranks (e.g. 1-3, 4-10); build: default 1-10")
    ap.add_argument("--root", help="build: the daily cache root (%%CACHE_DAILY_ROOT%%)")
    ap.add_argument("--export", help="build: tradelab's export folder (TLX_...)")
    ap.add_argument("--pm-run", default="PM_20261017_001")
    ap.add_argument("--engines", default="D,ENS")
    ap.add_argument("--to", default="")
    ap.add_argument("--stage-e-any", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--costs", default="stage_e", help=argparse.SUPPRESS)
    ap.add_argument("--check", default="", help="build: ChatGPT's watchlist.parquet - the ranks 1-3 must match")
    ap.add_argument("--data")
    ap.add_argument("--features")
    ap.add_argument("--ledgers")
    ap.add_argument("--out")
    ap.add_argument("--engine", default="D", help="D, ENS, or several: D,ENS (one run, a leaderboard across them)")
    ap.add_argument("--columns-file", default="", help="a file of feature names, one per line (# = comment)")
    ap.add_argument("--chunk", type=int, default=8, help=argparse.SUPPRESS)
    ap.add_argument("--columns", default="", help="comma list of feature columns to test (default: every column)")
    ap.add_argument("--why", default="", help="why_features.csv: test the engine's top --top features by its importance")
    ap.add_argument("--top", type=int, default=50)
    ap.add_argument("--confluence", action="store_true", help="also run the setups x logical confluences stage")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--frozen", default="", help="tag / scan: another freeze file (default: FROZEN_SETUPS.json beside "
                                                  "setuplab.py)")
    ap.add_argument("--date", default="", help="scan: the evening to scan (default: the cache's last session)")
    ap.add_argument("--all-missing", action="store_true", help="scan: every session since the freeze not scanned yet")
    ap.add_argument("--force", action="store_true", help="scan: rescan a scanned evening (its first record stays)")
    ap.add_argument("--panel", default="panel_live", help="scan: the panel folder under --root (default panel_live)")
    ap.add_argument("--picks-only", action="store_true", help="zones: skip the whole-market study")
    ap.add_argument("--tags", default="", help="tree: a TAGS run folder (default: the newest under --out\\TAGS)")
    ap.add_argument("--tree", default="", help="tree / scan: another tree file (default: TREE.json beside setuplab.py)")
    ap.add_argument("--cutoff-year", type=int, default=0, help="tree: record that year's cut-off for the nightly scan")
    ap.add_argument("--reruns", type=int, default=TREE_RERUNS, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if a.selftest:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
        import test_setuplab
        return test_setuplab.main()
    a.ranks_list = []
    if a.ranks:
        lo, _, hi = a.ranks.partition("-")
        a.ranks_list = list(range(int(lo), int(hi or lo) + 1))
    if a.command == "frozen":
        try:
            fp, doc = load_frozen(a.frozen or None)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
        print("%s - %s, frozen %s, sha256 %s" % (VERSION, fp, doc["frozen_at"], doc["sha256"]))
        for x in doc["setups"]:
            print("  %s  %-70s primary exit %-11s  %s" % (x["id"], x["name"][:70], x["primary_exit"],
                                                          " & ".join("%s %s %g" % tuple(c) for c in x["conds"])))
        print("FROZEN FILE OK")
        return 0
    if a.command == "tag":
        if not a.data or not a.features or not a.out:
            print("ERROR: tag needs --data <watchlist folder>, --features <panel.parquet> and --out (no defaults)")
            return 2
        a.frozen = a.frozen or None
        return cmd_tag(a)
    if a.command == "scan":
        if not a.root or not Path(a.root).is_dir() or not a.out:
            print("ERROR: scan needs --root <cache root> and --out <setuplab output folder> (no defaults)")
            return 2
        a.frozen = a.frozen or None
        return cmd_scan(a)
    if a.command == "tree":
        if not a.data or not a.out:
            print("ERROR: tree needs --data <watchlist folder> and --out <setuplab output folder holding the TAGS run> "
                  "(no defaults)")
            return 2
        a.frozen = a.frozen or None
        return cmd_tree(a)
    if a.command == "zones":
        if not a.root or not Path(a.root).is_dir() or not a.out or not a.features or not Path(a.features).is_file():
            print("ERROR: zones needs --root <cache root>, --features <panel.parquet> and --out <setuplab output "
                  "folder holding the TAGS run> (no defaults)")
            return 2
        try:
            return cmd_zones(a)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
    if a.command == "nodip":
        if not a.root or not Path(a.root).is_dir() or not a.out or not a.data or not a.features or \
                not Path(a.features).is_file():
            print("ERROR: nodip needs --root <cache root>, --data <watchlist folder>, --features <panel.parquet> "
                  "and --out <setuplab output folder> (no defaults)")
            return 2
        try:
            return cmd_nodip(a)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
    if a.command == "runners":
        if not a.root or not Path(a.root).is_dir() or not a.out or not a.data or not a.features or \
                not Path(a.features).is_file():
            print("ERROR: runners needs --root <cache root>, --data <watchlist folder>, --features <panel.parquet> "
                  "and --out <setuplab output folder> (no defaults)")
            return 2
        try:
            return cmd_runners(a)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
    if a.command == "build":
        if not a.root or not Path(a.root).is_dir() or not a.export or not a.out:
            print("ERROR: build needs --root <cache root>, --export <tradelab export folder> and --out (no defaults)")
            return 2
        return cmd_build(a)
    if not a.command or not a.data or not a.features:
        print("ERROR: give a command, --data and --features (no default paths)")
        return 2
    cols = [c.strip() for c in a.columns.split(",") if c.strip()] or None
    if a.columns_file:
        if not Path(a.columns_file).is_file():
            print("REFUSED: no file %s" % a.columns_file)
            return 3
        cols = list(dict.fromkeys((cols or []) + read_columns_file(a.columns_file)))
    if a.why:
        if not Path(a.why).is_file():
            print("REFUSED: no file %s" % a.why)
            return 3
        cols, skipped = pick_features(a.why, a.top, a.features, a.engine.split(",")[0])
        print("%s: the top %d features by the WHY importance (%d skipped before reaching them: %s)" % (
            VERSION, len(cols), len(skipped), ", ".join("%s (%s)" % x for x in skipped[:40])))
        print("  " + ", ".join(cols))
    engines = [e.strip() for e in a.engine.split(",") if e.strip()]
    if a.command == "reproduce":
        try:
            book = load(a.data, a.features, engines[0], cols, a.ranks_list or None)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
        if not a.ledgers:
            print("ERROR: --ledgers <folder of the delivered *.csv.gz>")
            return 2
        n, bad, worst = cmd_reproduce(book, a.ledgers)
        print("%s reproduce: %d ledgers compared, %d differ, largest ret difference %.2e pp" % (
            VERSION, n, len(bad), worst))
        for b in bad:
            print("  DIFFERS", *b)
        print("REPRODUCED" if not bad else "NOT REPRODUCED")
        return 0 if not bad else 1
    if not a.out:
        print("ERROR: --out <folder>")
        return 2
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    # the same command again resumes a stopped run; different settings in the same folder are refused
    st = lambda f: [str(Path(f).resolve()), Path(f).stat().st_size, int(Path(f).stat().st_mtime)] if f else None
    settings = {"version": VERSION, "engines": engines, "ranks": a.ranks_list, "columns": cols,
                "confluence": bool(a.confluence), "watchlist": st(Path(a.data) / "watchlist.parquet"),
                "features": st(a.features)}
    sf = out / "RUN_SETTINGS.json"
    if sf.is_file():
        old = json.loads(sf.read_text(encoding="utf-8"))
        if old != json.loads(json.dumps(settings)):
            print("REFUSED: %s holds a run with other settings (or another version / data) - use a new --out" % out)
            return 3
        print("resuming the run in %s (finished parts are kept)" % out)
    sf.write_text(json.dumps(settings, indent=1), encoding="utf-8")
    logf = open(out / "run.log", "a", encoding="utf-8")

    def log(*x):
        line = time.strftime("%H:%M:%S ") + " ".join(str(y) for y in x)
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()
    t0 = time.time()
    try:
        book = load(a.data, a.features, None if len(engines) > 1 else engines[0], cols, a.ranks_list or None, log,
                    a.chunk)
    except ValueError as e:
        print("REFUSED: %s" % e)
        return 3
    info = {"version": VERSION, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "args": vars(a),
            "features_attached": book.features, "features_missing": getattr(book, "missing_features", []),
            "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}
    if book.missing_features:
        log(" NOTE: %d feature columns are not in the panel and were skipped: %s" % (
            len(book.missing_features), ", ".join(book.missing_features)))
    if a.check:
        res = check_watchlists(book.wl, a.check)
        info["watchlist_check"] = res
        log(" " + res["text"])
    if cols:
        (out / "features_tested.txt").write_text("\n".join(book.features) + "\n", encoding="utf-8")
    if len(engines) == 1:
        cmd_run(book, out, log=log, with_confluence=a.confluence)
    else:
        books = {}
        for e in engines:
            mask = book.engine_arr == e
            if not mask.any():
                print("REFUSED: no picks of engine %s in the watchlist" % e)
                return 3
            books[e] = book.take(mask, e)
        info["picks"] = {e: b.n for e, b in books.items()}
        del book
        cmd_run_multi(books, out, log=log, with_confluence=a.confluence)
    info["minutes"] = round((time.time() - t0) / 60, 1)
    (out / "RUN.json").write_text(json.dumps(info, indent=1, default=str), encoding="utf-8")
    log(" DONE in %.1f minutes - %s" % (info["minutes"], out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
