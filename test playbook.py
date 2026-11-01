r"""test_playbook.py - the playbook bundle's self-test (python playbook.py --selftest).

p01 fill helpers by hand            p07 mapping (S05 included) and the config code (round trip, short codes,
p02 every entry rule by hand            refusals, a v1.0 code refused)
p03 every exit by hand              p08 a planted category effect is found; an absent one is not; null worlds
p04 statuses, invalidation and          flag about 2.5% of the time
    the data's end                  p09 the exporter and sim on a fake production cache (pathlab's test world)
p05 P1 = OPEN6 and PLAN5 exactly    p10 the Pine strategy's contract: defaults, tokens, code = pb_core's; lint
p06 the Pine twin = simulate_pick   p11 the block bootstrap's coverage
    on random paths and playbooks   p12 swings, ranges and S05 by hand; on real NSE bars when given
"""
import csv
import io
import os
import sys
import tempfile
import time
from contextlib import redirect_stdout
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p_ in (str(ROOT), str(HERE)):
    if p_ not in sys.path:
        sys.path.insert(0, p_)
import pb_core as P  # noqa: E402
import pine_twin as TW  # noqa: E402

RESULTS = []
NAN = float("nan")


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("  %s  %s%s" % ("ok  " if ok else "FAIL", name, "" if ok else "   <- %s" % (detail,)))


def close(a, b, tol=1e-9):
    if a is None or b is None:
        return a is None and b is None
    a, b = float(a), float(b)
    if np.isnan(a) or np.isnan(b):
        return np.isnan(a) and np.isnan(b)
    return abs(a - b) <= tol


def mk(rows, atr=2.0, ema=None, ema50=None, swh=None, swl=None):
    a = np.asarray(rows, dtype=float)
    n = len(a)
    A = np.full(n, float(atr)) if np.isscalar(atr) else np.asarray(atr, dtype=float)
    Em = np.full(n, 100.0) if ema is None else (np.full(n, float(ema)) if np.isscalar(ema) else
                                                np.asarray(ema, dtype=float))
    E5 = np.full(n, 100.0) if ema50 is None else (np.full(n, float(ema50)) if np.isscalar(ema50) else
                                                  np.asarray(ema50, dtype=float))
    full = lambda x: None if x is None else (np.full(n, float(x)) if np.isscalar(x) else np.asarray(x, dtype=float))  # noqa: E731
    sh, sl = full(swh), full(swl)
    if sh is None or sl is None:
        h0, l0 = P.tv_swings(a[:, 1], a[:, 2])
        sh = h0 if sh is None else sh
        sl = l0 if sl is None else sl
    return P.Bars(a[:, 0].copy(), a[:, 1].copy(), a[:, 2].copy(), a[:, 3].copy(), atr=A, ema=Em, ema50=E5, swh=sh,
                  swl=sl)


def pb(**kw):
    return P.Playbook("PX", **kw).check()


F_ = (100.0, 100.5, 99.5, 100.0)          # a quiet filler bar


def trade(r):
    return (r["status"], r["entry_i"], None if r["entry_i"] is None else round(r["entry_px"], 6), r.get("entry_how"))


# ============================================================================ p01
def p01_fills():
    fs, fl, ex = P.fill_stop_limit, P.fill_limit_buy, P.exit_in_bar
    check("p01a buy stop-limit: crossed inside the bar fills at the trigger", fs(101, 103, 100, 102, 102.6) == 102)
    check("p01b ... opened between trigger and limit: at the open", fs(102.4, 103, 102, 102, 102.6) == 102.4)
    check("p01c ... gapped above the limit, never back down: no fill", fs(104, 105, 103, 102, 102.6) is None)
    check("p01d ... gapped above the limit, back down to it: at the limit", fs(104, 105, 102.5, 102, 102.6) == 102.6)
    check("p01e a plain buy stop (limit None) gapped above: at the open", fs(104, 105, 103, 102, None) == 104)
    check("p01f ... high below the trigger: no fill", fs(101, 101.9, 100, 102, 102.6) is None)
    check("p01g buy limit: open below it fills at the open, touched at the limit, missed = none",
          fl(99, 101, 98, 100) == 99 and fl(101, 102, 99.5, 100) == 100 and fl(101, 102, 100.5, 100) is None)
    check("p01h exits: stop gapped / touched, target touched / gapped",
          ex(97, 98, 96, 98, NAN) == (97, "STOP_GAP") and ex(99, 100, 97.5, 98, NAN) == (98, "STOP") and
          ex(101, 104.5, 100.5, 98, 104) == (104, "TARGET") and ex(105, 106, 104.5, 98, 104) == (105, "TARGET_GAP"))
    check("p01i stop and target in one bar: the extreme nearer the open comes first (TradingView's path)",
          ex(101, 104.2, 97.9, 98, 104) == (98, "STOP") and ex(101, 104.1, 97.5, 98, 104) == (104, "TARGET"))
    check("p01j net = (exit - entry - c x (entry + exit)) / entry", close(P.net_of(100, 110, 0.175), 0.096325, 1e-12))


# ============================================================================ p02
def p02_entries():
    c = 0.175
    b = mk([(100, 101, 99, 100), (101, 102, 100, 101.5)] + [F_] * 4 + [(106, 107, 105, 106.5)] + [F_] * 5)
    r = P.simulate_pick(b, 0, pb(), NAN, c)
    base = P.baseline(b, 0, c)
    check("p02a OPEN: T+1's open in, T+6's open out (= OPEN6)",
          trade(r) == ("FILLED", 1, 101.0, "ORDER") and r["exit_i"] == 6 and r["exit_px"] == 106 and
          r["reason"] == "TIME" and close(r["net"], base["open6_net"]))
    r = P.simulate_pick(b, 0, pb(X="CLOSE"), NAN, c)
    check("p02b OPEN, sell at the close: T+5's close (= PLAN5)", r["exit_i"] == 5 and close(r["net"], base["plan5_net"]))
    rows = [(100, 101, 99, 100), (103, 104, 102, 103.5)] + [F_] * 10
    check("p02c OPEN with G = 1%: a gap above the cap is not chased (NO_FILL) / F = OPEN buys T+2's open",
          trade(P.simulate_pick(mk(rows), 0, pb(G=1.0), NAN, c)) == ("NO_FILL", None, None, None) and
          trade(P.simulate_pick(mk(rows), 0, pb(G=1.0, F="OPEN"), NAN, c)) == ("FILLED", 2, 100.0, "FALLBACK"))
    rows2 = [(100, 101, 99, 100), (103, 104, 100.5, 103)] + [F_] * 10
    rows3 = [(100, 101, 99, 100), (100.5, 101, 100, 100.8)] + [F_] * 10
    check("p02d ... the bar trades back to the cap: at the cap; opens below it: at the open",
          trade(P.simulate_pick(mk(rows2), 0, pb(G=1.0), NAN, c))[:3] == ("FILLED", 1, 101.0) and
          trade(P.simulate_pick(mk(rows3), 0, pb(G=1.0), NAN, c))[:3] == ("FILLED", 1, 100.5))
    rows = [(100, 101, 99, 100)] + [(100 + k, 101 + k, 99 + k, 100 + k) for k in range(1, 12)]
    check("p02e DELAY V = 2: the open of T+3", trade(P.simulate_pick(mk(rows), 0, pb(E="DELAY", V=2), NAN, c)) ==
          ("FILLED", 3, 103.0, "ORDER"))
    T = (100, 101, 99, 100.5)               # STH O 0.5 x ATR 2: trigger 102, limit 102.6
    sth = dict(E="STH", O=0.5, V=5, L=0.3)
    cases = [
        ("p02f STH crossed in T+2: at the trigger", [T, (101, 101.5, 100, 101), (101.5, 103, 101, 102.5)], {},
         ("FILLED", 2, 102.0, "ORDER")),
        ("p02g STH opened inside trigger .. limit: at the open", [T, (102.4, 103, 102, 102.8)], {},
         ("FILLED", 1, 102.4, "ORDER")),
        ("p02h STH gapped over the limit, closed above the trigger: cancelled (already through)",
         [T, (104, 105, 103, 104.5)], {}, ("NO_FILL", None, None, None)),
        ("p02i ... with F = OPEN: the next open", [T, (104, 105, 103, 104.5)], {"F": "OPEN"},
         ("FILLED", 2, 100.0, "FALLBACK")),
        ("p02j STH gapped over the limit and back to it: at the limit", [T, (104, 105, 102.5, 104)], {},
         ("FILLED", 1, 102.6, "ORDER")),
        ("p02k STH with L = 0 (plain stop) gapped: at the open", [T, (104, 105, 103, 104.5)], {"L": 0.0},
         ("FILLED", 1, 104.0, "ORDER")),
        ("p02l STH whose trigger is at T's close: not placed (NO_ORDER)", [(100, 101, 99, 101)], {"O": 0.0},
         ("NO_ORDER", None, None, None)),
        ("p02m ... with F = OPEN: T+1's open", [(100, 101, 99, 101)], {"O": 0.0, "F": "OPEN"},
         ("FILLED", 1, 100.0, "FALLBACK")),
        ("p02n STH V = 2 never reached: NO_FILL after T+2", [T, (100, 101.5, 99, 100), (100, 101.8, 99, 100)],
         {"V": 2}, ("NO_FILL", None, None, None)),
        ("p02o ... with F = OPEN: T+3's open", [T, (100, 101.5, 99, 100), (100, 101.8, 99, 100)],
         {"V": 2, "F": "OPEN"}, ("FILLED", 3, 100.0, "FALLBACK")),
    ]
    for name, rows, kw, want in cases:
        got = trade(P.simulate_pick(mk(rows + [F_] * 10), 0, pb(**{**sth, **kw}), NAN, c))
        check(name, got == want, got)
    rows = [(100, 101, 99, 100), (100.5, 100.8, 99, 99.5), (99.6, 100.9, 99.5, 100.5)] + [F_] * 10
    check("p02p STPD follows the previous session's high (T+2 at 100.8); STH at T's high does not fill there",
          trade(P.simulate_pick(mk(rows), 0, pb(E="STPD", O=0.0, V=5), NAN, c)) == ("FILLED", 2, 100.8, "ORDER") and
          P.simulate_pick(mk(rows), 0, pb(E="STH", O=0.0, V=5), NAN, c)["entry_i"] != 2)
    rows = [(100, 101, 99, 100), (100, 100.5, 99, 100.5), (100.6, 101, 100.4, 100.8), (100.9, 101.2, 100.5, 101)]
    check("p02q STPD: no order the evening the close is at the high; next evening's order fills at 101",
          trade(P.simulate_pick(mk(rows + [F_] * 10), 0, pb(E="STPD", O=0.0, V=5), NAN, c)) ==
          ("FILLED", 3, 101.0, "ORDER"))
    rows = [(103, 104, 102, 103), (103, 104, 102, 103.5), (104, 105.5, 103.8, 105.4)] + [F_] * 10
    check("p02r STLV: reclaim of the level 105 + 0.1 ATR at 105.2",
          trade(P.simulate_pick(mk(rows), 0, pb(E="STLV", O=0.1, V=10), 105.0, c)) == ("FILLED", 2, 105.2, "ORDER"))
    check("p02s STLV / LMLV without a level: NO_LEVEL; F = OPEN: T+1's open",
          trade(P.simulate_pick(mk(rows), 0, pb(E="STLV", O=0.1, V=10), NAN, c))[0] == "NO_LEVEL" and
          P.simulate_pick(mk(rows), 0, pb(E="LMLV", O=0.1, V=10), NAN, c)["status"] == "NO_LEVEL" and
          trade(P.simulate_pick(mk(rows), 0, pb(E="STLV", O=0.1, V=10, F="OPEN"), NAN, c)) ==
          ("FILLED", 1, 103.0, "FALLBACK"))
    rows = [(102, 103.5, 101.5, 103), (103, 104, 101, 102), (102, 102.5, 100.2, 101)] + [F_] * 10
    rows2 = [(102, 103.5, 101.5, 103), (100, 101, 99.5, 100.5)] + [F_] * 10
    check("p02t LMLV: limit at level 100 + 0.25 ATR = 100.5 (T+2); an open below it fills at the open",
          trade(P.simulate_pick(mk(rows), 0, pb(E="LMLV", O=0.25, V=5), 100.0, c)) == ("FILLED", 2, 100.5, "ORDER") and
          trade(P.simulate_pick(mk(rows2), 0, pb(E="LMLV", O=0.25, V=5), 100.0, c)) == ("FILLED", 1, 100.0, "ORDER"))
    rows = [(100, 101, 99, 100), (99.5, 100, 98.5, 99), (99, 100, 99, 99.5), (99.5, 100, 98.6, 99)] + [F_] * 10
    check("p02u LMTC at T's close - 1 ATR = 98 for 3 sessions: missed -> NO_FILL; F = OPEN: T+4's open",
          trade(P.simulate_pick(mk(rows), 0, pb(E="LMTC", O=1.0, V=3), NAN, c)) == ("NO_FILL", None, None, None) and
          trade(P.simulate_pick(mk(rows), 0, pb(E="LMTC", O=1.0, V=3, F="OPEN"), NAN, c)) ==
          ("FILLED", 4, 100.0, "FALLBACK"))
    rows = [(100, 101, 99.5, 100), (100, 101, 99.5, 100), (99, 99.5, 98.4, 99)] + [F_] * 10
    ema = [99.0, 98.5] + [98.0] * 11
    check("p02v LMEMA re-set each evening: T+2 fills at the evening's EMA 98.5",
          trade(P.simulate_pick(mk(rows, ema=ema), 0, pb(E="LMEMA", O=0.0, V=5), NAN, c)) ==
          ("FILLED", 2, 98.5, "ORDER"))
    check("p02w SKIP: no trade", P.simulate_pick(mk(rows), 0, pb(E="SKIP"), NAN, c)["status"] == "SKIP")
    T0 = (100, 101, 99, 100)
    rows = [T0, (100.5, 101, 100, 100.5), (101, 102.5, 100.8, 102.3)] + [F_] * 10
    rows_lo = [T0] + [F_] * 12
    check("p02x SWHI: buy-stop at the swing high 102 + 0.1 ATR = 102.2, crossed in T+2; a swing high under the close "
          "places nothing (NO_FILL after V; F = OPEN: the open after the window)",
          trade(P.simulate_pick(mk(rows, swh=102.0), 0, pb(E="SWHI", O=0.1, V=5, L=0.0), NAN, c)) ==
          ("FILLED", 2, 102.2, "ORDER") and
          trade(P.simulate_pick(mk(rows_lo, swh=99.0), 0, pb(E="SWHI", O=0.1, V=3), NAN, c)) ==
          ("NO_FILL", None, None, None) and
          trade(P.simulate_pick(mk(rows_lo, swh=99.0), 0, pb(E="SWHI", O=0.1, V=3, F="OPEN"), NAN, c)) ==
          ("FILLED", 4, 100.0, "FALLBACK"))
    rows = [(100, 103, 99, 100), (100.5, 102, 100, 101), (102, 103.4, 101.8, 103.2)] + [F_] * 10
    check("p02y STRNG N = 3: buy-stop at the 3-session high (103, re-set each evening) -> T+2 at 103",
          trade(P.simulate_pick(mk(rows), 0, pb(E="STRNG", O=0.0, V=5, N=3, L=0.0), NAN, c)) ==
          ("FILLED", 2, 103.0, "ORDER"))
    rows = [T0, (100.5, 101, 99.8, 100.5), (100, 100.4, 99.3, 99.6)] + [F_] * 10
    check("p02z LMRNG N = 3: limit at the 3-session low 99 + 0.25 ATR = 99.5 -> T+2 at 99.5",
          trade(P.simulate_pick(mk(rows), 0, pb(E="LMRNG", O=0.25, V=5, N=3), NAN, c)) ==
          ("FILLED", 2, 99.5, "ORDER"))


# ============================================================================ p03
def p03_exits():
    c = 0.175
    T, E1 = (100, 100.5, 99.5, 100), (100, 101, 97, 100.5)      # entry at T+1's open 100; its low 97 is below 98

    def run(rows, atr=2.0, lvl=NAN, **kw):
        return P.simulate_pick(mk([T, E1] + rows + [F_] * 14, atr=atr), 0, pb(**kw), lvl, c)

    r = run([(99, 100, 97.5, 98)], S="ATR", SK=1.0)
    check("p03a ATR stop 98 placed at the entry close: the entry bar's low 97 does not stop it; T+2 does at 98",
          (r["exit_i"], r["exit_px"], r["reason"]) == (2, 98.0, "STOP") and close(r["net"], P.net_of(100, 98, c)))
    r = run([(97, 98, 96, 97)], S="ATR", SK=1.0)
    check("p03b a gap through the stop fills at the open", (r["exit_i"], r["exit_px"], r["reason"]) == (2, 97, "STOP_GAP"))
    r = run([(101, 104.5, 100.5, 104)], S="ATR", SK=1.0, T="R", TK=2.0)
    check("p03c 2R target 104", (r["exit_px"], r["reason"], r["target"]) == (104, "TARGET", 104))
    r1 = run([(101, 104.2, 97.9, 100)], S="ATR", SK=1.0, T="R", TK=2.0)
    r2 = run([(101, 104.1, 97.5, 100)], S="ATR", SK=1.0, T="R", TK=2.0)
    check("p03d both in one bar: the low nearer the open -> STOP; the high nearer -> TARGET",
          (r1["exit_px"], r1["reason"]) == (98, "STOP") and (r2["exit_px"], r2["reason"]) == (104, "TARGET"))
    r = run([(105, 106, 104.5, 105)], S="ATR", SK=1.0, T="R", TK=2.0)
    check("p03e a gap over the target fills at the open", (r["exit_px"], r["reason"]) == (105, "TARGET_GAP"))
    r = run([], S="PCT", SK=5.0, T="PCT", TK=10.0)
    check("p03f PCT stop / target: 95 / 110", close(r["stop"], 95.0) and close(r["target"], 110.0))
    r = run([], S="TLOW", SK=0.5)
    r2 = run([], S="LVL", SK=0.5, lvl=99.0)
    check("p03g TLOW = T's low - 0.5 ATR(T) = 98.5; LVL = level - 0.5 ATR(T) = 98",
          close(r["stop"], 98.5) and close(r2["stop"], 98.0))
    atr = [2.0] * 4 + [1.0] * 20
    rows = [(100, 101, 99.5, 101), (101, 104.5, 100.8, 104), (104, 110.5, 103.5, 110), (109.5, 110, 108.6, 109),
            (109.3, 109.6, 108.8, 109)]
    r = P.simulate_pick(mk([T] + rows + [F_] * 14, atr=atr), 0, pb(TR=1, TA=3.0, TM=1.0, H=10), NAN, c)
    check("p03h trail: armed by the close 104 (> 103), stop 102 -> 108 -> 109 (highest close 110 - 1 ATR); TRAIL at 109",
          (r["exit_i"], r["exit_px"], r["reason"], r["armed"]) == (5, 109.0, "TRAIL", True), r)
    rows = [(100, 101, 99.5, 101), (101, 104.5, 100.8, 104)] + [(104, 105, 103.5, 104.5)] * 14
    r1 = P.simulate_pick(mk([T] + rows), 0, pb(TR=1, TA=3.0, TM=5.0, H=3, EX=10), NAN, c)
    r2 = P.simulate_pick(mk([T] + rows), 0, pb(TR=1, TA=50.0, TM=5.0, H=3, EX=10), NAN, c)
    check("p03i EX: an armed trade holds to the open of entry + 10; an unarmed one exits at entry + 3",
          (r1["exit_i"], r1["reason"], r1["armed"]) == (11, "TIME", True) and (r2["exit_i"], r2["armed"]) == (4, False))
    r = run([], H=1, X="CLOSE")
    check("p03j H = 1, sell at the close: the entry session's own close", (r["exit_i"], r["exit_px"]) == (1, 100.5))
    r = P.simulate_pick(mk([T, E1, F_, F_]), 0, pb(), NAN, c)
    check("p03k a hold the data cannot finish: OPEN_AT_END (entry kept)", (r["status"], r["entry_i"]) ==
          ("OPEN_AT_END", 1))
    r = P.simulate_pick(mk([T, E1, (100, 101, 99, 100), (96, 97, 95, 96)] + [F_] * 5), 0, pb(S="ATR", SK=1.0, H=2),
                        NAN, c)
    check("p03l the time exit's open gaps through the stop: STOP_GAP at that open",
          (r["exit_i"], r["exit_px"], r["reason"]) == (3, 96.0, "STOP_GAP"))

    def run2(rows, lvl=NAN, **kw):
        bk = {k_: kw.pop(k_) for k_ in ("ema", "ema50", "swh", "swl") if k_ in kw}
        return P.simulate_pick(mk([T, E1] + rows + [F_] * 14, **bk), 0, pb(**kw), lvl, c)

    r = run2([(99, 100, 97.5, 98)], S="SWL", SK=0.25, swl=98.5)
    r2 = run2([], S="SWL", SK=0.25, swl=101.0)
    r3 = run2([], S="RNG", SK=0.25, N=3)
    check("p03m SWL stop = swing low 98.5 - 0.25 ATR = 98 (STOP at 98); not placed when at or above the entry close; "
          "RNG N = 3: the 3-session low 97 - 0.5 = 96.5",
          (r["exit_px"], r["reason"]) == (98.0, "STOP") and np.isnan(r2["stop"]) and close(r3["stop"], 96.5),
          (r["exit_px"], r["reason"], r2["stop"], r3["stop"]))
    r = run2([(101, 104.5, 100.5, 104)], T="SWH", TK=0.0, swh=104.0)
    r2 = run2([], T="RNGH", TK=0.5, N=3)
    r3 = run2([], T="EMA50", TK=0.0, ema50=103.0)
    r4 = run2([], T="EMA50", TK=0.0, ema50=99.0)
    check("p03n targets: SWH 104 (TARGET), RNGH N = 3 = 101 + 0.5 ATR = 102, EMA50 103; none when not above the entry",
          (r["exit_px"], r["reason"]) == (104.0, "TARGET") and close(r2["target"], 102.0) and
          close(r3["target"], 103.0) and np.isnan(r4["target"]))
    ema = [99.0] * 30
    r = run2([(100, 100.5, 97.8, 98.0), (98.2, 99, 97.5, 98.5)], XC="EMA20", XK=0.25, H=10, ema=ema)
    r2 = run2([(100, 100.5, 98.6, 98.9), (99, 99.5, 98.5, 99.2)] + [(99.5, 100, 99, 99.6)] * 12, XC="EMA20", XK=0.25,
              H=4, ema=ema)
    check("p03o close exit EMA20 - 0.25 ATR = 98.5: the close 98 sells at the next open 98.2 (XCLOSE); a close at 98.9 "
          "does not (TIME at H)", (r["exit_i"], r["exit_px"], r["reason"]) == (3, 98.2, "XCLOSE") and
          (r2["reason"], r2["exit_i"]) == ("TIME", 5), (r["exit_i"], r["exit_px"], r["reason"], r2["reason"]))
    r = run2([(100.5, 101, 100, 100.8), (100.6, 101, 100, 100.7)], TS=2, TSP=1.0, H=10)
    r2 = run2([(100.5, 102, 100, 101.5), (101.6, 102, 101, 101.8)], TS=2, TSP=1.0, H=4)
    check("p03p time stop TS = 2, TSP = 1%: the 2nd held close 100.8 is not above 101 -> out at the next open (TSTOP); "
          "101.5 is -> held to H", (r["exit_i"], r["reason"]) == (3, "TSTOP") and r2["reason"] == "TIME",
          (r["exit_i"], r["reason"], r2["reason"]))


# ============================================================================ p04
def p04_ends():
    c = 0.175
    T = (100, 101, 99, 100.5)
    r = P.simulate_pick(mk([T, (100, 101.5, 99, 100), (100, 101.8, 99, 100)]), 0, pb(E="STH", O=0.5, V=5), NAN, c)
    check("p04a a window cut by the data's end, order still working: OPEN_AT_END", r["status"] == "OPEN_AT_END")
    r = P.simulate_pick(mk([T, (100, 101.5, 99, 100), (104, 105, 103, 104.5)]), 0, pb(E="STH", O=0.5, V=5, L=0.3),
                        NAN, c)
    check("p04b already through at the data's last close: NO_FILL (the chart cancels it at that close)",
          r["status"] == "NO_FILL", r["status"])
    r = P.simulate_pick(mk([T, (100, 101.5, 99, 100), (100, 101.8, 99, 100)]), 0,
                        pb(E="STH", O=0.5, V=2, F="OPEN"), NAN, c)
    check("p04c the fallback's open is after the data's end: OPEN_AT_END", r["status"] == "OPEN_AT_END")
    b = mk([T] + [F_] * 10, atr=[NAN] + [2.0] * 10)
    check("p04d no ATR at T: NO_ATR; F = OPEN: T+1's open",
          P.simulate_pick(b, 0, pb(E="STH", O=0.5), NAN, c)["status"] == "NO_ATR" and
          trade(P.simulate_pick(b, 0, pb(E="STH", O=0.5, F="OPEN"), NAN, c)) == ("FILLED", 1, 100.0, "FALLBACK"))
    rows = [(100, 101, 99, 100.5), (100, 100.5, 98.5, 98.8)] + [F_] * 10
    st1 = P.simulate_pick(mk(rows), 0, pb(E="STH", O=0.5, V=5, IV="TLOW", IK=0.0, F="OPEN"), NAN, c)["status"]
    st2 = P.simulate_pick(mk(rows, ema50=101.0), 0, pb(E="STH", O=0.5, V=5, IV="EMA50"), NAN, c)["status"]
    st3 = P.simulate_pick(mk(rows, swl=99.0), 0, pb(E="SWHI", O=0.1, V=5, IV="SWL", IK=0.0), NAN, c)["status"]
    st4 = P.simulate_pick(mk(rows), 0, pb(E="DELAY", V=2, IV="TLOW"), NAN, c)["status"]
    st5 = P.simulate_pick(mk(rows), 0, pb(E="STH", O=0.5, V=5, IV="TLOW", IK=0.5), NAN, c)["status"]
    check("p04e invalidation: a close under T's low cancels a waiting STH (INVALID, no fallback even with F = OPEN); "
          "T under EMA50: INVALID at T; under the swing low (SWHI); a DELAY; a deeper line (IK 0.5) does not trigger",
          (st1, st2, st3, st4) == ("INVALID",) * 4 and st5 != "INVALID", (st1, st2, st3, st4, st5))


# ============================================================================ random paths
def rand_bars(rng, n):
    o, h, l, c = (np.empty(n) for _ in range(4))
    prev = 100.0
    for i in range(n):
        g = rng.normal(0, 0.01) + (rng.choice([0, 0, 0, 0, 0.04, -0.04, 0.08, -0.06]) if rng.random() < 0.15 else 0)
        op = prev * np.exp(g)
        cl = op * np.exp(rng.normal(0.001, 0.02))
        o[i], c[i] = op, cl
        h[i] = max(op, cl) * (1 + abs(rng.normal(0, 0.01)) * (rng.random() > 0.1))
        l[i] = min(op, cl) * (1 - abs(rng.normal(0, 0.01)) * (rng.random() > 0.1))
        prev = cl
    return P.Bars(o, h, l, c)


def rand_pb(rng):
    return P.Playbook("PX", E=str(rng.choice(P.ENTRY)), O=float(rng.choice([0, 0.1, 0.25, 0.5, 1, -0.5])),
                      V=int(rng.choice([1, 2, 3, 5, 10])), L=float(rng.choice([0, 0.3, 1])),
                      G=float(rng.choice([0, 0, 0.5, 2])), F=str(rng.choice(P.FALLBACK)),
                      N=int(rng.choice([3, 5, 20])), IV=str(rng.choice(P.INVALID + ("NONE", "NONE"))),
                      IK=float(rng.choice([0, 0.25, 0.5, -0.25])), S=str(rng.choice(P.STOPS)),
                      SK=float(rng.choice([0.25, 0.5, 1, 2, 3])), T=str(rng.choice(P.TARGETS)),
                      TK=float(rng.choice([0, 1, 2, 5])), H=int(rng.choice([1, 2, 5, 10])), X=str(rng.choice(P.EXIT_AT)),
                      TR=int(rng.choice([0, 1])), TA=float(rng.choice([1, 3, 5])), TM=float(rng.choice([1, 2, 3])),
                      EX=int(rng.choice([0, 10, 20])), XC=str(rng.choice(P.XCLOSE + ("NONE",))),
                      XK=float(rng.choice([0, 0.25, 0.5])), TS=int(rng.choice([0, 0, 2, 3])),
                      TSP=float(rng.choice([0, 1, 2])))


def p05_baseline():
    rng = np.random.default_rng(5)
    ok6 = ok5 = 0
    for _ in range(300):
        b = rand_bars(rng, 40)
        t = int(rng.integers(14, 30))
        base = P.baseline(b, t, 0.175)
        ok6 += close(P.simulate_pick(b, t, P.DEFAULT_PLAYBOOKS["P1"], NAN, 0.175)["net"], base["open6_net"], 1e-12)
        ok5 += close(P.simulate_pick(b, t, pb(X="CLOSE"), NAN, 0.175)["net"], base["plan5_net"], 1e-12)
    check("p05a the shipped P1 is OPEN6 exactly (300 random paths)", ok6 == 300, ok6)
    check("p05b P1 selling at the close is PLAN5 exactly", ok5 == 300, ok5)


def p06_twin(n_cases=24000):
    rng = np.random.default_rng(6)
    keys = ("status", "entry_i", "entry_px", "exit_i", "exit_px", "reason")
    bad, first = 0, None
    seen = set()
    for it in range(n_cases):
        n = int(rng.integers(20, 70))
        b = rand_bars(rng, n)
        t = int(rng.integers(14, n - 1)) if rng.random() < 0.95 else int(rng.integers(0, n - 1))
        lvl = NAN if rng.random() < 0.2 else float(b.c[t] * (1 + rng.normal(0, 0.04)))
        q = rand_pb(rng)
        a, z = P.simulate_pick(b, t, q, lvl, 0.175), TW.run_twin(b, t, q, lvl, 0.175)
        seen.add((q.E, a["status"]))
        seen.add(("R", a["reason"]))
        diff = [k for k in keys if not (a[k] == z[k] if not isinstance(a[k], float) and not isinstance(z[k], float)
                                        else close(a[k], z[k]))]
        if a["status"] == "FILLED" and a.get("entry_how") != z.get("entry_how"):
            diff.append("entry_how")
        if diff:
            bad += 1
            first = first or (it, q, diff, a, z)
    reasons = {r for k, r in seen if k == "R"} - {""}
    check("p06a the Pine twin (bar by bar, TradingView's broker) = simulate_pick on %d random paths x playbooks"
          % n_cases, bad == 0, first)
    check("p06b ... covering every entry rule, every status and every exit reason",
          {e for e, s in seen if s == "FILLED"} >= set(P.ENTRY) - {"SKIP"} and
          {s for e, s in seen} >= {"FILLED", "NO_FILL", "NO_ORDER", "NO_LEVEL", "NO_ATR", "SKIP", "OPEN_AT_END",
                                   "INVALID"} and
          reasons >= {"TIME", "STOP", "STOP_GAP", "TARGET", "TARGET_GAP", "TRAIL", "TRAIL_GAP", "TSTOP", "XCLOSE"},
          reasons)


# ============================================================================ p07
def p07_codes():
    rules = P.parse_map(P.DEFAULT_MAP)
    m = lambda s_, e, r="BB", x="N": P.match(rules, s_, e, r, x)  # noqa: E731
    want = [(("S01", "BO_NEW"), "P2"), (("S03", "BO_CONF"), "P2"), (("S07", "FBO"), "P3"), (("S01", "FBO"), "P3"),
            (("S02", "BD_NEW"), "P1"), (("S01", "FBD"), "P4"), (("S08", "FBD"), "P1"), (("S08", "NONE", "HS"), "P1"), (("S01", "NONE"), "P1"),
            (("S01", "NONE", "BB", "OV"), "P8"), (("S01", "NONE", "NB", "EX"), "P8"), (("S06", "BO_NEW"), "P7"),
            (("S02", "NONE"), "P7"), (("S03", "BO_STALL"), "P5"), (("S07", "NONE"), "P9"), (("S12", "NONE"), "P5"),
            (("UNK", "NONE"), "P1"), (("S09", "BO_NEW"), "P1")]
    got = [(a, m(*a)) for a, w in want]
    check("p07a the shipped long-position map: 12 rules, first match wins (S08 / S09 and breakdowns -> the open; S01 overextended -> the EMA20 pullback)", len(rules) == 12 and all(g == w for (a, g), (_, w) in
                                                                                     zip(got, want)),
          [(a, g, w) for (a, g), (_, w) in zip(got, want) if g != w])
    r2 = P.parse_map("*:*:BR,HS=P5\n S01 : BO_NEW = P2 ;*:*:*:EX=P8;*:*:*=P1")
    check("p07b regimes, S05, new lines and spaces in the mapping",
          P.match(r2, "S01", "BO_NEW", "BR") == "P5" and P.match(r2, "S01", "BO_NEW", "BB") == "P2" and
          P.match(r2, "S07", "NONE", "MX") == "P1" and P.match(r2, "S07", "NONE", "MX", "EX") == "P8")
    bad = 0
    for txt in ("S04:BO_NEW=P2", "S01:BO_NEW", "S01:BO_NEW=P11", "S01:BO_NEW:BB:N:X=P2", "S01:BREAKOUT=P2", "", ";;",
                "S01:*:*:ZZ=P2"):
        try:
            P.parse_map(txt)
        except ValueError:
            bad += 1
    check("p07c refused: unknown state / event / S05, no '=', P11, five parts, empty", bad == 8, bad)
    pbs = {k: P.Playbook(**asdict(v)) for k, v in P.DEFAULT_PLAYBOOKS.items()}
    pbs["P2"] = P.Playbook("P2", E="STH", O=0.5, V=7, L=0.0, G=1.25, F="OPEN", N=15, IV="SWL", IK=0.5, S="ATR", SK=1.5,
                           T="R", TK=2.0, H=8, X="CLOSE", TR=1, TA=4.0, TM=2.5, EX=12, XC="EMA50", XK=0.25, TS=3,
                           TSP=1.5)
    pbs["P10"] = P.Playbook("P10", E="LMRNG", O=0.25, V=4, N=30, S="RNG", SK=0.5, T="RNGH", TK=0.5)
    mapping = "S01:BO_NEW:BB,NB:OV=P2;*:*:*=P1"
    code = P.config_code(pbs, mapping, 0.2)
    got, rules3, comm, mp = P.parse_code(code)
    strip = lambda d: {k: v for k, v in asdict(d).items() if k != "title"}  # noqa: E731
    check("p07d config code round trip (every field of all ten playbooks, the mapping, the commission)",
          all(strip(got[k]) == strip(pbs[k]) for k in pbs) and mp == mapping and comm == 0.2 and
          P.match(rules3, "S01", "BO_NEW", "NB", "OV") == "P2" and P.match(rules3, "S01", "BO_NEW", "NB") == "P1")
    d, _, cm, mp = P.parse_code("BMPB2")
    d2, _, _, _ = P.parse_code("BMPB2|P2=O:0.5|P9=N:30")
    check("p07e short codes: 'BMPB2' = the defaults; 'BMPB2|P2=O:0.5|P9=N:30' changes those fields only",
          all(strip(d[k]) == strip(P.DEFAULT_PLAYBOOKS[k]) for k in d) and cm == P.COMMISSION and mp == P.DEFAULT_MAP
          and d2["P2"].O == 0.5 and d2["P9"].N == 30 and strip(d2["P3"]) == strip(P.DEFAULT_PLAYBOOKS["P3"]) and
          d2["P2"].E == "LMLV" and d2["P2"].IV == "LVL")
    bad = 0
    for txt in ("XYZ|P2=O:1", "BMPB2|P2=Q:1", "BMPB2|P2=E:FOO", "BMPB2|P2=H:0", "BMPB2|M=S99:*=P2", "BMPB1",
                "BMPB2|P3=IV:FOO", "BMPB2|P4=XC:BAR"):
        try:
            P.parse_code(txt)
        except ValueError:
            bad += 1
    check("p07f refused codes: another tag, unknown field / entry / invalidation / close exit, H = 0, a bad mapping, a "
          "v1.0 code (BMPB1: its short form is relative to v1.0's defaults)", bad == 8, bad)


# ============================================================================ p08
def world(rng, n_picks, planted, dip_share=0.85, cat="S01:BO_NEW"):
    """Each pick on its own bars. Planted: after T the price dips to the breakout level (97, T close 100) on T+1
    in dip_share of the picks, then rallies ~+5% by T+6. Absent: the same rally without the dip."""
    picks, own = [], {}
    st, ev = cat.split(":")
    for k in range(n_picks):
        rows = []
        px = 100.0
        for _ in range(20):
            rows.append((px, px + 1.0, px - 1.0, px))
        rows[-1] = (99.5, 100.5, 99.0, 100.0)                        # T
        dip = planted and rng.random() < dip_share
        o1 = 100.0 + rng.normal(0, 0.2)
        rows.append((o1, o1 + 0.5, 97.2 if dip else 99.0, 98.5 if dip else 100.5))
        drift = abs(rng.normal(0.05, 0.03))
        for j in range(2, 12):
            lvl = 100.0 * (1 + drift * min(j, 6) / 6.0)
            rows.append((lvl, lvl + 1.0, lvl - 1.0, lvl))
        b = mk(rows)
        sym = "W%04d" % k
        own[sym] = (np.arange(len(rows)), b)
        day = np.datetime64("2020-01-01") + np.timedelta64(k, "D")
        picks.append(SimpleNamespace(symbol=sym, t_own=19, lvl=97.0, state=st, event=ev, regime="BB", T=str(day),
                                     cat=cat, id=sym))
    return picks, own


def null_world(rng, n_picks):
    picks, own = [], {}
    for k in range(n_picks):
        b = rand_bars(rng, 45)
        sym = "N%04d" % k
        own[sym] = (np.arange(45), b)
        day = np.datetime64("2020-01-01") + np.timedelta64(k // 2, "D")
        picks.append(SimpleNamespace(symbol=sym, t_own=25, lvl=float(b.c[25] * 0.98), state="S07", event="NONE",
                                     regime="MX", T=str(day), cat="S07:NONE", id=sym))
    return picks, own


def p08_worlds():
    import playbook as PB
    pbs, rules, comm, _ = P.parse_code(P.config_code())
    rng = np.random.default_rng(8)
    pk, own = world(rng, 240, planted=True)
    s = PB.summarize(PB.run_sim(pk, own, pbs, rules, comm))[0]
    pk2, own2 = world(rng, 240, planted=False)
    s2 = PB.summarize(PB.run_sim(pk2, own2, pbs, rules, comm))[0]
    check("p08a planted (dip to the breakout level, then the rally): P2 beats OPEN6, interval above 0",
          s["group"] == ("S01:BO_NEW", "P2") and s["diff"][1] > 0, s["diff"])
    check("p08b absent (the rally without the dip): P2 never fills, interval below 0 (no false lift)",
          s2["filled"] == 0 and s2["diff"][2] < 0, s2["diff"])
    flags = 0
    for seed in range(40):
        pk3, own3 = null_world(np.random.default_rng(100 + seed), 160)
        s3 = PB.summarize(PB.run_sim(pk3, own3, pbs, rules, comm, force_pb="P5"))[0]
        flags += int(s3["diff"][1] > 0)
    check("p08c null worlds (random walks): 'better than OPEN6' at 95% in <= 4 of 40 (expected about 1)", flags <= 4,
          flags)


# ============================================================================ p09
def _find(name, env, marker):
    cands = [os.environ.get(env, ""), str(ROOT.parent / name), str(ROOT.parent / "work" / name)]
    for c in cands:
        if c and (Path(c) / marker).exists():
            return Path(c)
    return None


def p09_exporter():
    pdir = _find("pathlab", "PATHLAB_DIR", "pathlab.py")
    tdir = _find("tradelab", "TRADELAB_DIR", "tl_common.py")
    vdir = _find("v2engine", "V2_DIR", "v2_data.py")
    if pdir is None or tdir is None or vdir is None:
        check("p09 the exporter test needs pathlab, tradelab and v2engine (PATHLAB_DIR / TRADELAB_DIR / V2_DIR)",
              False, (pdir, tdir, vdir))
        return
    os.environ["TRADELAB_DIR"] = str(tdir)
    for p_ in (str(pdir / "tests"), str(pdir), str(tdir / "tests"), str(tdir), str(vdir)):
        if p_ not in sys.path:
            sys.path.insert(0, p_)
    saved = {k: os.environ.pop(k, None) for k in ("TRADELAB_OUT", "PATHLAB_OUT", "V2_OUT")}
    import pl_world as W
    import tl_world as TWL
    import playbook as PB
    tmp = Path(tempfile.mkdtemp(prefix="pbt09_"))
    try:
        w = W.make_cache_world(tmp / "w1", n_regular=14, n_3m=3)
        TWL.use_mods(w["root"])
        os.environ["V2_OUT"] = str(tmp / "v2out")              # v2_data keeps its breadth copy there
        out = tmp / "out"
        common = ["--root", str(w["root"]), "--out", str(out), "--pm-run", "PM_TEST_001", "--stage-e-any",
                  "--costs", "replica"]
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = PB.main(["export"] + common)
        picks, own, data = PB.load(w["root"], "PM_TEST_001", ["D", "ENS"], [1, 2, 3], "2020-01-01", "2022-12-31",
                                   log=lambda *a: None, stage_e_any=True, costs="replica")
        files = sorted((out / "pine").glob("*.txt"))
        lines, heads, ids = [], [], []
        for f in files:
            tx = f.read_text(encoding="ascii").splitlines()
            heads.append(tx[0])
            lines += tx[1:]
        ids = [ln.split(",")[0] for ln in lines]
        check("p09a export: one Pine file per symbol, a #%s header naming it, one line per pick, ids unique" % P.CODE_TAG,
              rc == 0 and len(files) == len({p.symbol for p in picks}) and len(lines) == len(picks) and
              len(set(ids)) == len(ids) and all(h.startswith("#%s|%s|%s|" % (P.CODE_TAG, f.stem, P.VERSION))
                                                for h, f in zip(heads, files)), (rc, len(files), len(lines), len(picks)))
        ok = True
        by = {p.id: p for p in picks}
        for ln in lines:
            f_ = ln.split(",")
            eng, ymd, rk = f_[0].split("-")
            p = by[f_[0]]
            ok &= len(f_) == 10 and eng in ("D", "ENS") and len(ymd) == 8 and p.state == f_[1] and p.event == f_[2]
            ok &= f_[9] == PB.tv_name(p.symbol)
            ok &= f_[1] in P.STATES and f_[2] in P.EVENTS and f_[4] in P.REGIMES
            if np.isfinite(p.lvl):
                ok &= abs(float(f_[5]) * float(f_[6]) - p.lvl) <= 1e-4 * p.lvl + 0.01
            else:
                ok &= f_[5] == ""
        n_lvl = sum(np.isfinite(p.lvl) for p in picks)
        check("p09b each line parses the way the Pine reads it; level / close x close = the event level (%d levels)"
              % n_lvl, ok and n_lvl > 0)
        cl, cok = [], True
        for f in sorted((out / "pine_by_category").glob("*.txt")):
            tx = f.read_text(encoding="ascii").splitlines()
            cok &= tx[0].startswith("#%s|*|%s|" % (P.CODE_TAG, P.VERSION)) and len(f.read_text()) <= PB.PINE_MAX
            for ln in tx[1:]:
                cl.append(ln)
                cok &= by[ln.split(",")[0]].cat.replace(":", "_") == f.stem.split("_20")[0]
        check("p09h category files: every pick exactly once, in its own category's file, header #BMPB2|*|, each "
              "under the paste limit", cok and sorted(cl) == sorted(lines), (len(cl), len(lines)))
        rows = list(csv.DictReader((out / "review_picks.csv").open(encoding="utf-8")))
        check("p09c review sheet: every pick once, with empty columns for the findings",
              len(rows) == len(picks) and {"verdict", "notes", "pine_net"} <= set(rows[0]) and
              all(r["verdict"] == "" for r in rows) and (out / "categories.csv").exists() and (out / "EXPORT.md").exists())
        with redirect_stdout(buf):
            rc1 = PB.main(["sim"] + common + ["--code", "BMPB2|M=*:*:*=P1"])
            rc2 = PB.main(["sim"] + common)
            rc3 = PB.main(["matrix"] + common)
        sims = sorted(out.glob("sim_*"))
        d1 = [d for d in sims if (d / "config_code.txt").read_text().strip() == "BMPB2|M=*:*:*=P1"][0]
        tr = list(csv.DictReader((d1 / "trades.csv").open(encoding="utf-8")))
        diffs = [float(r["diff_vs_open6"]) for r in tr if r["diff_vs_open6"] != ""]
        check("p09d sim with everything mapped to P1 reproduces OPEN6 on every pick (difference 0)",
              rc1 == 0 and len(tr) == len(picks) and len(diffs) > 0 and max(abs(x) for x in diffs) < 1e-12, len(diffs))
        d2 = [d for d in sims if d != d1][0]
        tr2 = list(csv.DictReader((d2 / "trades.csv").open(encoding="utf-8")))
        rep = (d2 / "REPORT.md").read_text(encoding="utf-8")
        check("p09e default sim: every pick, a playbook per category, the report and the summary",
              rc2 == 0 and len(tr2) == len(picks) and "| category | playbook |" in rep and
              {r["playbook"] for r in tr2} <= set(P.PB_NAMES) and (d2 / "summary.csv").exists() and
              all(r["s05"] in P.S05S for r in tr2))
        mx = sorted(out.glob("matrix_*"))
        mrep = (mx[0] / "REPORT.md").read_text(encoding="utf-8") if mx else ""
        check("p09f matrix: all ten playbooks on every category", rc3 == 0 and len(mx) == 1 and
              "P6 LMTC" in mrep and "P9 LMRNG" in mrep and "P10 SKIP" in mrep)
        with redirect_stdout(buf):
            rc4 = PB.main(["export"] + common + ["--to", "2023-06-30"])
            rc5 = PB.main(["export", "--out", str(out)])
            rc6 = PB.main(["sim"] + common + ["--code", "BMPB2|P2=E:NOPE"])
        led = (out / "playbook_ledger.jsonl").read_text(encoding="utf-8").splitlines()
        check("p09g refused: the holdout without --spend-holdout (3), no --root (2), a bad code (3); ledger written",
              (rc4, rc5, rc6) == (3, 2, 3) and len(led) == 4, (rc4, rc5, rc6, len(led)))
    finally:
        os.environ.pop("V2_OUT", None)
        for k_, v_ in saved.items():
            if v_ is not None:
                os.environ[k_] = v_


# ============================================================================ p10
def _pine():
    return (ROOT / "BigMove_Playbook.pine").read_text(encoding="utf-8")


def _lit(src, name):
    import re
    m = re.search(r'^%s = "([^"]*)"' % re.escape(name), src, re.M)
    return m.group(1) if m else None


def p10_pine(lint=True):
    import re
    src = _pine()
    check("p10a Pine v5, version and tag = pb_core's", src.startswith("//@version=5") and
          _lit(src, "VERSION") == P.VERSION and _lit(src, "TAG") == P.CODE_TAG)
    check("p10b the Pine's DEFAULT_CODE = pb_core.config_code() (the shipped defaults, character for character)",
          _lit(src, "DEFAULT_CODE") == P.config_code(), (_lit(src, "DEFAULT_CODE"), P.config_code()))
    m = re.search(r'^iMap = input\.text_area\("([^"]*)"', src, re.M)
    c1 = re.search(r'^iComm = input\.float\(([0-9.]+)', src, re.M)
    c2 = re.search(r'commission_value=([0-9.]+)', src)
    check("p10c the Pine's default mapping and commission (input and Properties) = pb_core's",
          m and m.group(1) == P.DEFAULT_MAP and c1 and float(c1.group(1)) == P.COMMISSION and c2 and
          float(c2.group(1)) == P.COMMISSION)
    got = {}
    for k, suf, kind, val in re.findall(r'^p(\d+)([A-Za-z]+) = input\.(\w+)\(("[^"]*"|[^,]+),', src, re.M):
        f = {"Title": "title", "NB": "N"}.get(suf, suf)
        got[("P" + k, f)] = (kind, val.strip())
    bad = []
    for k, d in P.DEFAULT_PLAYBOOKS.items():
        for f in P.FIELDS + ("title",):
            want = getattr(d, f)
            kind, val = got.get((k, f), (None, None))
            if kind is None:
                bad.append((k, f, "missing"))
                continue
            if kind == "string" or kind == "text_area":
                ok = val == '"%s"' % want
            elif kind == "bool":
                ok = val == ("true" if want else "false")
            else:
                ok = float(val) == float(want) and (kind != "int" or "." not in val)
            if not ok:
                bad.append((k, f, val, want))
    n_in = P.NPB * (len(P.FIELDS) + 1)
    check("p10d every playbook input's default = DEFAULT_PLAYBOOKS (%d playbooks x %d fields + titles = %d inputs)" % (
        P.NPB, len(P.FIELDS), n_in), not bad and len(got) == n_in, (bad[:5], len(got)))
    opts = re.findall(r'^p\d+(E|S|T|X|F|IV|XC) = input\.string\("[^"]*", "[^"]*", options=\[([^\]]*)\]', src, re.M)
    want = {"E": P.ENTRY, "S": P.STOPS, "T": P.TARGETS, "X": P.EXIT_AT, "F": P.FALLBACK, "IV": P.INVALID,
            "XC": P.XCLOSE}
    okopt = len(opts) == 7 * P.NPB and all(tuple(x.strip().strip('"') for x in o.split(",")) == want[f]
                                           for f, o in opts)
    fil = {n: tuple(x.strip().strip('"') for x in o.split(",")) for n, o in
           re.findall(r'^(iSt|iEv|iRg|iSx) = input\.string\("ALL", "[^"]*", options=\[([^\]]*)\]', src, re.M)}
    okfil = fil.get("iSt") == ("ALL",) + P.STATES and fil.get("iEv") == ("ALL",) + P.EVENTS and \
        fil.get("iRg") == ("ALL",) + P.REGIMES and fil.get("iSx") == ("ALL",) + P.S05S
    oktok = _lit(src, "STATES") == "," + ",".join(P.STATES) + "," and \
        _lit(src, "EVENTS") == "," + ",".join(P.EVENTS) + "," and \
        _lit(src, "REGIMES") == "," + ",".join(P.REGIMES) + "," and _lit(src, "S05S") == "," + ",".join(P.S05S) + ","
    fo = re.search(r'^iForce = input\.string\("Mapping", "[^"]*", options=\[([^\]]*)\]', src, re.M)
    okf = fo and tuple(x.strip().strip('"') for x in fo.group(1).split(",")) == ("Mapping",) + P.PB_NAMES
    check("p10e the Pine's option lists and tokens = pb_core's (entries, invalidations, stops, targets, exits, close "
          "exits, fallbacks, filters incl. S05, P1 .. P10)", okopt and okfil and oktok and okf,
          (len(opts), okopt, okfil, oktok, okf))
    import playbook as PB
    check("p10g the Pine reads the export's line as playbook.py writes it (10 fields, ticker last, category files)",
          len(PB.PINE_FIELDS) == 10 and PB.PINE_FIELDS[-1] == "tv_symbol" and "f.get(9) != (iTk != \"\" ? iTk : syminfo.ticker)" in src and
          'hdrSym == "*"' in src and "f.get(8))" in src)
    if not lint:
        return
    try:
        import pynescript  # noqa: F401
    except ImportError:
        print("  skip  p10f pynescript is not installed here: the Pine's syntax and names were checked where the "
              "bundle was built")
        return
    import pine_lint as PL
    t0 = time.time()
    errs = PL.lint(src)
    check("p10f the Pine parses (pynescript) and lints clean: names, keyword arguments, declarations, Pick fields "
          "(%.0f s)" % (time.time() - t0), not errs, errs[:8])


# ============================================================================ p11
def p11_bootstrap():
    import playbook as PB
    rng = np.random.default_rng(11)
    cover = 0
    reps = 200
    for _ in range(reps):
        days = np.repeat(np.arange(250), 2)
        vals = rng.normal(0.001, 0.02, len(days))
        m, lo, hi, n = PB.block_ci(days, vals, B=600, seed=int(rng.integers(1 << 30)))
        cover += int(lo <= 0.001 <= hi)
    check("p11a the block bootstrap's 95%% interval covers the true mean %d / %d times (90-99%% expected)" %
          (cover, reps), 0.90 * reps <= cover <= 0.99 * reps)
    m, lo, hi, n = PB.block_ci(["d"] * 5, [0.1] * 5)
    check("p11b fewer than 20 signal days: the mean without an interval", n == 5 and np.isnan(lo) and close(m, 0.1))


# ============================================================================ p12
def p12_structure():
    h = np.array([10, 11, 12, 15, 13, 12, 11, 12, 14, 13, 12, 11, 10], float)
    swh, swl = P.tv_swings(h, h - 1.0)
    same = lambda u, v: np.array_equal(np.isnan(u), np.isnan(v)) and np.allclose(np.nan_to_num(u), np.nan_to_num(v))  # noqa: E731
    e_h = np.r_[np.full(6, np.nan), np.full(5, 15.0), np.full(2, 14.0)]
    e_l = np.r_[np.full(9, np.nan), np.full(4, 10.0)]
    h2 = np.array([10, 11, 12, 15, 15, 12, 11, 10, 9, 9], float)      # a tie: the first 15 is the swing
    swh2, _ = P.tv_swings(h2, h2 - 1.0)
    ties = same(swh2, np.r_[np.full(6, np.nan), np.full(4, 15.0)])
    rows = [(100, 101, 99, 100)] * 3 + [(100, 104, 96, 100)] + [(100, 101, 99, 100)] * 3
    b = mk(rows)
    rr = (b.rng_low(3, 3), b.rng_high(3, 3), b.rng_low(6, 3), b.rng_high(1, 5))
    c = np.r_[np.full(15, 100.0), [106.5, 110.0, 100.0]]
    bars = [(x, x + 0.5, x - 0.5, x) for x in c]
    bs = mk(bars, atr=2.0, ema=100.0, ema50=100.0)
    sx = [P.s05_at(bs, t) for t in (14, 15, 16)]
    check("p12a structure by hand: swings (tl_state's rule, known 3 sessions later), N-session low / high (current "
          "session included), S05 at T (EMA20 gap 3.25 ATR = OV, 5 ATR = EX)",
          same(swh, e_h) and same(swl, e_l) and ties and rr == (96.0, 104.0, 99.0, 101.0) and sx == ["N", "OV", "EX"],
          (swh.tolist(), swl.tolist(), swh2.tolist(), rr, sx))
    import json
    data = sorted((HERE / "data").glob("NSE_*_1D.json"))
    if not data:
        print("  skip  p12b no real NSE bars in tests\\data")
        return
    bad, n, first, stats = 0, 0, None, {}
    keys = ("status", "entry_i", "entry_px", "exit_i", "exit_px", "reason")
    for f in data:
        d = json.loads(f.read_text(encoding="utf-8"))
        rb = P.Bars(*(np.asarray(d[k], dtype=float) for k in ("o", "h", "l", "c")))
        for t in range(20, rb.n - 2):
            lvl = float(rb.c[t] * 0.97) if t % 3 else np.nan
            for k_, q in P.DEFAULT_PLAYBOOKS.items():
                a, z = P.simulate_pick(rb, t, q, lvl, P.COMMISSION), TW.run_twin(rb, t, q, lvl, P.COMMISSION)
                n += 1
                stats.setdefault(k_, {}).setdefault(a["status"], 0)
                stats[k_][a["status"]] += 1
                diff = [x for x in keys if not (a[x] == z[x] if not isinstance(a[x], float) and
                                                not isinstance(z[x], float) else close(a[x], z[x]))]
                if diff:
                    bad += 1
                    first = first or (f.name, t, k_, diff, a, z)
        sx = {x: sum(P.s05_at(rb, t) == x for t in range(20, rb.n)) for x in P.S05S}
        stats["S05 " + f.stem] = sx
    check("p12b on real NSE bars (%s, TradingView): the Pine twin = simulate_pick for all ten shipped playbooks at "
          "every session as T (%d cases); S05 on the chart %s" % (", ".join(x.stem for x in data), n,
                                                                  {k: v for k, v in stats.items() if k.startswith("S05")}),
          bad == 0 and n > 1000, first)


def main(argv=None):
    argv = argv or []
    quick = "quick" in argv
    t0 = time.time()
    print("%s self-test%s" % (P.VERSION, " (quick)" if quick else ""))
    for f in (p01_fills, p02_entries, p03_exits, p04_ends, p05_baseline):
        f()
    p06_twin(6000 if quick else 24000)
    p07_codes()
    p08_worlds()
    p09_exporter()
    p10_pine(lint=not quick)
    p11_bootstrap()
    p12_structure()
    bad = [r for r in RESULTS if not r[1]]
    print("%d checks, %d failed (%.0f s)" % (len(RESULTS), len(bad), time.time() - t0))
    if bad:
        print("NOT VERIFIED")
        return 1
    print("VERIFIED (%s)" % P.VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
