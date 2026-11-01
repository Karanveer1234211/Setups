r"""playbook.py - BigMove state + event playbook v1.1: export for the Pine strategy, and the same rules on every
pick (ten long playbooks, the long-position map by state, event, regime and S05).

    python playbook.py export --root %CACHE_DAILY_ROOT% --out %PB_OUT%
    python playbook.py sim    --root %CACHE_DAILY_ROOT% --out %PB_OUT% [--code "<config code from the chart>"]
    python playbook.py matrix --root %CACHE_DAILY_ROOT% --out %PB_OUT%
    python playbook.py --selftest

export   reads production READ ONLY (pick_meta's run, the cache, tl_state, tl_context - through v2engine's adapter) and
         writes, for every pick (engines D and ENS, ranks 1-3 by default):
           pine\<SYMBOL>.txt          the text to paste into the Pine strategy's 'Picks' box on that symbol's chart
           review_picks.csv           one row per pick: category, context, the open-entry baselines, and empty
                                      columns for your findings (playbook, Pine result, verdict, notes)
           by_category\<CAT>.csv      the same rows, one file per state + event category, oldest first
           categories.csv             per engine and category: picks, open-entry (OPEN6 / PLAN5) results with 95%
                                      block-bootstrap intervals over signal days
           EXPORT.md                  what was exported and how to use it
sim      runs a config code (printed by the Pine strategy's table and its log; default = the shipped defaults) on
         every exported pick and compares each pick with buying at T+1's open (OPEN6), per category, paired:
           sim_<hash>\trades.csv, summary.csv, REPORT.md
matrix   every one of the ten playbooks on every category (the mapping ignored): which playbook works where.
Periods: the discovery years by default (signal days 2020-01-01 .. 2022-12-31; bars read to 45 days after the last
signal day so every window completes). 2023 onward is the holdout: --to later than 2022-12-31 needs --spend-holdout.
Writes only under --out. No default cache path: --root is required.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pb_core as P  # noqa: E402

DISCOVERY_FROM, DISCOVERY_TO = "2020-01-01", "2022-12-31"
TAIL_DAYS = 45
PINE_FIELDS = ("trade_id", "state", "event", "event_age", "regime", "level_over_T_close", "T_close", "open6_gross",
               "plan5_gross", "tv_symbol")   # one line per pick (the Pine strategy reads them in this order)
PINE_MAX = 4000                              # characters per paste file (--max-chars); TradingView refuses long pastes


# ============================================================================ the picks
class Pick:
    __slots__ = ("id", "symbol", "engine", "rank", "T", "ymd", "state", "event", "age", "regime", "lvl", "tc", "th",
                 "tl", "atrp", "t_cal", "t_own", "base", "base_flat", "cat", "s05")


def load(root, pm_run, engines, ranks, d_from, d_to, log=print, stage_e_any=False, tradelab_any=False, data=None,
         costs="stage_e"):
    """Picks with their context, the stock's own bars, and the open-entry baselines. data: a preloaded v2_data.Data
    (tests); else read through v2engine's adapter (tradelab, stage E's costs; costs='replica' only for the fake cache
    of the tests, whose stand-in stage E has no cost code)."""
    import v2_core as C
    import v2_money as M
    if data is None:
        import v2_data as VD
        seal = str(np.datetime64(d_to, "D") + np.timedelta64(TAIL_DAYS, "D"))
        data = VD.load_real(root, pm_run, tuple(engines), tuple(range(1, max(ranks) + 1)), d_from, d_to,
                            seal_end=seal, stage_e_any=stage_e_any, tradelab_any=tradelab_any, log=log,
                            with_home=False, costs=costs)
    M.install(data.cm)
    cal = data.cal
    lo, hi = np.datetime64(d_from, "D"), np.datetime64(d_to, "D")
    own = {}
    picks = []
    for s in data.registry.active():
        if s.engine not in engines or s.rank not in ranks:
            continue
        d = np.datetime64(s.T, "D")
        if d < lo or d > hi:
            continue
        b = data.bars[s.symbol]
        if s.symbol not in own:
            ok = ~np.isnan(b["close"]) & ~np.isnan(b["open"])
            idx = np.flatnonzero(ok)
            own[s.symbol] = (idx, P.Bars(b["open"][idx], b["high"][idx], b["low"][idx], b["close"][idx]))
        idx, ob = own[s.symbol]
        j = int(np.searchsorted(idx, s.t_idx))
        if j >= len(idx) or idx[j] != s.t_idx:
            continue                                            # no bar on T
        sn = s.snap()
        p = Pick()
        p.id = "%s-%s-%d" % (s.engine, s.T.replace("-", ""), s.rank)
        p.symbol, p.engine, p.rank, p.T = s.symbol, s.engine, s.rank, s.T
        p.ymd = s.T.replace("-", "")
        p.state = P.STATE_CODE_TOKEN.get(int(sn.get("state", -1)), "UNK")
        p.event = P.EVENT_CODE_TOKEN.get(int(sn.get("event", 0)), "NONE")
        p.age = int(sn.get("age", -1))
        p.regime = P.REGIME_CODE_TOKEN.get(int(sn.get("regime", -1)), "NA")
        ev = data.events.get(s.symbol, {})
        lv = np.nan
        if p.event in ("BO_NEW", "BO_CONF", "BO_STALL", "FBO") and "s04_level" in ev:
            lv = float(ev["s04_level"][s.t_idx])
        elif p.event in ("BD_NEW", "BD_CONF", "BD_STALL", "FBD") and "s10_level" in ev:
            lv = float(ev["s10_level"][s.t_idx])
        p.lvl = lv
        p.tc, p.th, p.tl = float(b["close"][s.t_idx]), float(b["high"][s.t_idx]), float(b["low"][s.t_idx])
        p.atrp = float(ob.atr[j] / ob.c[j]) if np.isfinite(ob.atr[j]) else np.nan
        p.t_cal, p.t_own = s.t_idx, j
        d6 = C.plan_detail(b, cal, s.t_idx, "OPEN6")
        d5 = C.plan_detail(b, cal, s.t_idx, "CLOSE5")
        p.base = {"open6_gross": d6["gross"], "open6_net_stageE": d6["net"], "plan5_gross": d5["gross"],
                  "plan5_net_stageE": d5["net"]}
        p.base_flat = P.baseline(ob, j, P.COMMISSION)
        p.cat = "%s:%s" % (p.state, p.event)
        p.s05 = P.s05_at(ob, j)
        picks.append(p)
    picks.sort(key=lambda p: (p.T, p.engine, p.rank))
    return picks, own, data


def _f(x, nd=5):
    return "" if x is None or not np.isfinite(x) else ("%.*f" % (nd, x))


def pine_line(p):
    """PINE_FIELDS. The level goes as a ratio to T's close: the chart multiplies it by its own close at T, so a split
    adjusted differently on TradingView does not move the level."""
    lvl_ratio = p.lvl / p.tc if np.isfinite(p.lvl) and p.tc > 0 else np.nan
    vals = [p.id, p.state, p.event, str(p.age), p.regime, _f(lvl_ratio, 6), _f(p.tc, 2),
            _f(p.base_flat["open6_gross"], 5), _f(p.base_flat["plan5_gross"], 5),   # plain, as the chart counts them
            tv_name(p.symbol)]
    return ",".join(vals)


def tv_name(sym):
    """TradingView's NSE ticker: '&' and '-' become '_' (M&M -> M_M, BAJAJ-AUTO -> BAJAJ_AUTO)."""
    return "".join(ch if ch.isalnum() else "_" for ch in sym.upper())


# ============================================================================ statistics
def block_ci(days, vals, B=2000, block=10, seed=7):
    """Mean per pick and its 95% circular block bootstrap interval over signal days."""
    vals = np.asarray(vals, dtype=float)
    days = np.asarray(days)
    ok = np.isfinite(vals)
    vals, days = vals[ok], days[ok]
    if len(vals) == 0:
        return np.nan, np.nan, np.nan, 0
    ud, inv = np.unique(days, return_inverse=True)
    sums = np.bincount(inv, weights=vals, minlength=len(ud))
    cnts = np.bincount(inv, minlength=len(ud)).astype(float)
    n = len(ud)
    mean = sums.sum() / cnts.sum()
    if n < 20:
        return float(mean), np.nan, np.nan, int(len(vals))
    rng = np.random.default_rng(seed)
    k = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(B, k))
    idx = ((starts[:, :, None] + np.arange(block)[None, None, :]) % n).reshape(B, -1)[:, :n]
    bs = sums[idx].sum(axis=1) / np.maximum(cnts[idx].sum(axis=1), 1e-12)
    return float(mean), float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)), int(len(vals))


def fmt_ci(m, lo, hi, scale=100.0, unit="%"):
    if not np.isfinite(m):
        return "-"
    if not np.isfinite(lo):
        return "%+.2f%s (n < 20 days)" % (m * scale, unit)
    return "%+.2f%s [%+.2f, %+.2f]" % (m * scale, unit, lo * scale, hi * scale)


# ============================================================================ commands
def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


REVIEW_HEADER = ["trade_id", "symbol", "tv_symbol", "engine", "rank", "signal_day", "category", "state", "event",
                 "event_age", "regime", "s05", "event_level", "t_close", "t_high", "t_low", "atr_pct",
                 "open6_gross", "open6_net_flat", "open6_net_stageE", "plan5_gross", "plan5_net_flat",
                 "plan5_net_stageE", "playbook_used", "pine_status", "pine_net", "verdict", "notes"]


def review_row(p):
    bf = p.base_flat
    return [p.id, p.symbol, "NSE:" + tv_name(p.symbol), p.engine, p.rank, p.T, p.cat, p.state, p.event, p.age,
            p.regime, p.s05, _f(p.lvl, 4), _f(p.tc, 2), _f(p.th, 2), _f(p.tl, 2), _f(p.atrp, 5),
            _f(bf["open6_gross"]), _f(bf["open6_net"]), _f(p.base["open6_net_stageE"]),
            _f(bf["plan5_gross"]), _f(bf["plan5_net"]), _f(p.base["plan5_net_stageE"]), "", "", "", "", ""]


def cmd_export(a, picks, own, data, out, log):
    pdir = out / "pine"
    pdir.mkdir(parents=True, exist_ok=True)
    by_sym = {}
    for p in picks:
        by_sym.setdefault(p.symbol, []).append(p)
    run = data.info.get("picks", {}).get("sha256", "")[:16]
    long_ = []
    for sym, lst in by_sym.items():
        chunks, chunk, size = [], [], 0
        for p in lst:
            ln = len(pine_line(p)) + 1
            if chunk and size + ln > PINE_MAX - 200:
                chunks.append(chunk)
                chunk, size = [], 0
            chunk.append(p)
            size += ln
        chunks.append(chunk)
        for k, ch in enumerate(chunks, 1):
            head = "#%s|%s|%s|%s..%s|%d picks|picks sha %s" % (P.CODE_TAG, tv_name(sym), P.VERSION, ch[0].T, ch[-1].T,
                                                              len(ch), run)
            txt = "\n".join([head] + [pine_line(p) for p in ch]) + "\n"
            fn = "%s.txt" % tv_name(sym) if k == 1 else "%s_part%d.txt" % (tv_name(sym), k)
            (pdir / fn).write_text(txt, encoding="ascii", newline="\n")
        if len(chunks) > 1:
            long_.append((sym, len(chunks)))
    write_csv(out / "review_picks.csv", REVIEW_HEADER, [review_row(p) for p in picks])
    cats = {}
    for p in picks:
        cats.setdefault(p.cat, []).append(p)
    # one Pine file per category, every symbol in it: paste once, then flip through the symbols on the chart
    cdir = out / "pine_by_category"
    cdir.mkdir(parents=True, exist_ok=True)
    cat_files = {}
    for cat, lst in cats.items():
        lst = sorted(lst, key=lambda p: (p.T, p.engine, p.rank))
        parts = [("", lst)]
        if sum(len(pine_line(p)) + 1 for p in lst) > PINE_MAX - 200:
            years = sorted({p.T[:4] for p in lst})
            parts = []
            for y in years:
                ly = [p for p in lst if p.T[:4] == y]
                chunk, size, k = [], 0, 1
                for p in ly:
                    ln = len(pine_line(p)) + 1
                    if chunk and size + ln > PINE_MAX - 200:
                        parts.append(("_%s_%d" % (y, k), chunk))
                        chunk, size, k = [], 0, k + 1
                    chunk.append(p)
                    size += ln
                parts.append((("_%s_%d" % (y, k)) if k > 1 else ("_%s" % y), chunk))
        names = []
        for suf, chunk in parts:
            nsym = len({p.symbol for p in chunk})
            head = "#%s|*|%s|%s..%s|%d picks|%d symbols|category %s%s|picks sha %s" % (
                P.CODE_TAG, P.VERSION, chunk[0].T, chunk[-1].T, len(chunk), nsym, cat, suf, run)
            fn = "%s%s.txt" % (cat.replace(":", "_"), suf)
            (cdir / fn).write_text("\n".join([head] + [pine_line(p) for p in chunk]) + "\n", encoding="ascii",
                                   newline="\n")
            names.append(fn)
        cat_files[cat] = names
    for cat, lst in cats.items():
        write_csv(out / "by_category" / ("%s.csv" % cat.replace(":", "_")), REVIEW_HEADER, [review_row(p) for p in lst])
    rows = []
    for eng in sorted({p.engine for p in picks}) + ["ALL"]:
        for cat in sorted(cats):
            lst = [p for p in cats[cat] if eng == "ALL" or p.engine == eng]
            if not lst:
                continue
            days = [p.T for p in lst]
            o6 = [p.base_flat["open6_net"] for p in lst]
            p5 = [p.base_flat["plan5_net"] for p in lst]
            m6 = block_ci(days, o6)
            m5 = block_ci(days, p5)
            v = np.array([x for x in o6 if np.isfinite(x)])
            rows.append([eng, cat, len(lst), fmt_ci(*m6[:3]), fmt_ci(*m5[:3]),
                         "%.1f%%" % (100 * np.mean(v > 0)) if len(v) else "-",
                         "%.1f%%" % (100 * np.mean(v <= -0.04)) if len(v) else "-",
                         "%+.2f%%" % (100 * np.sort(v)[:max(1, int(np.ceil(0.05 * len(v))))].mean()) if len(v) else "-"])
    write_csv(out / "categories.csv", ["engine", "category", "picks", "open6_net_mean_ci", "plan5_net_mean_ci",
                                       "open6_win_rate", "open6_bad_rate_le_-4pct", "open6_cvar5"], rows)
    L = ["# Playbook export (%s)" % P.VERSION, "",
         "- picks: %d (engines %s, ranks %s, signal days %s .. %s), %d symbols" % (
             len(picks), ",".join(a.engines), ",".join(map(str, a.ranks)), a.d_from, a.d_to, len(by_sym)),
         "- pick_meta file sha256 %s; calendar %s; costs %s" % (run, data.info.get("calendar"), data.info.get("costs")),
         "- baselines: OPEN6 = buy T+1's open, sell T+6's open; PLAN5 = sell T+5's close. *_flat = the Pine "
         "strategy's commission (%.3f%% a side); *_stageE = stage E's fully net costs" % P.COMMISSION, "",
         "## Use", "",
         "1. TradingView: open NSE:<SYMBOL> on the daily chart, add the strategy BigMove_Playbook.pine.",
         "2. Paste pine\\<SYMBOL>.txt (one stock, every category) or pine_by_category\\<STATE>_<EVENT>.txt (one "
         "category, every stock: paste once, then change the chart's symbol; the strategy keeps the chart's own "
         "picks) into its 'Picks' box. The audit table must say OK. The symbols of a category are in "
         "by_category\\<STATE>_<EVENT>.csv (column tv_symbol).",
         "3. Step through: 'Focus pick #' (1, 2, 3 ...), the pick list, or the Strategy Tester's List of Trades (each "
         "trade's signal = its trade id). Record a verdict per trade in the strategy's Findings box (id|BETTER|note) "
         "or in review_picks.csv / by_category\\<CAT>.csv (playbook_used, pine_status, pine_net, verdict, notes).",
         "4. The chart's config code (table, and the first line of the Pine Logs) reproduces the same rules on every "
         "pick: python playbook.py sim --code \"<code>\" ...", "",
         "## Categories, all engines: buying at the open (OPEN6) per pick, flat commission, 95% interval", ""]
    for cat in sorted(cats, key=lambda c: -len(cats[c])):
        lst = cats[cat]
        m6 = block_ci([p.T for p in lst], [p.base_flat["open6_net"] for p in lst])
        L.append("- %s: %d picks on %d symbols, OPEN6 %s; Pine file%s %s" % (
            cat, len(lst), len({p.symbol for p in lst}), fmt_ci(*m6[:3]), "s" if len(cat_files[cat]) > 1 else "",
            ", ".join(cat_files[cat])))
    if long_:
        L += ["", "Symbols split into several paste files (SYMBOL.txt, SYMBOL_part2.txt, ...; %d characters each at most): "
              % PINE_MAX + ", ".join("%s (%d files)" % x for x in long_)]
    (out / "EXPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    log(" export: %d picks, %d symbols, %d categories -> %s" % (len(picks), len(by_sym), len(cats), out))
    return out


def run_sim(picks, own, pbs, rules, comm, force_pb=None):
    """Every pick under its playbook (the mapping's, or force_pb for all) and its OPEN6 baseline on the same bars."""
    res = []
    for p in picks:
        idx, ob = own[p.symbol]
        x = getattr(p, "s05", None) or P.s05_at(ob, p.t_own)
        pbn = force_pb or P.match(rules, p.state, p.event, p.regime, x)
        r = P.simulate_pick(ob, p.t_own, pbs[pbn], p.lvl, comm)
        base = P.baseline(ob, p.t_own, comm)
        res.append((p, pbn, r, base))
    return res


def summarize(res, key=lambda p, pbn: (p.cat, pbn)):
    groups = {}
    for p, pbn, r, base in res:
        groups.setdefault(key(p, pbn), []).append((p, r, base))
    out = []
    for g, lst in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        settled = [(p, r, b) for p, r, b in lst if r["status"] != "OPEN_AT_END" and np.isfinite(b["open6_net"])]
        if not settled:
            continue
        days = [p.T for p, r, b in settled]
        app = [r["net"] if r["status"] == "FILLED" and np.isfinite(r["net"]) else 0.0 for p, r, b in settled]
        bas = [b["open6_net"] for p, r, b in settled]
        dif = [x - y for x, y in zip(app, bas)]
        fills = [r for p, r, b in settled if r["status"] == "FILLED" and np.isfinite(r["net"])]
        fb = [b["open6_net"] for p, r, b in settled if r["status"] == "FILLED" and np.isfinite(r["net"])]
        out.append({"group": g, "picks": len(settled), "filled": len(fills),
                    "approach": block_ci(days, app), "open6": block_ci(days, bas), "diff": block_ci(days, dif),
                    "approach_win": float(np.mean([x > 0 for x in app])) if app else np.nan,
                    "open6_win": float(np.mean([x > 0 for x in bas])) if bas else np.nan,
                    "per_fill": float(np.mean([r["net"] for r in fills])) if fills else np.nan,
                    "open6_same_fills": float(np.mean(fb)) if fb else np.nan})
    return out


def cmd_sim(a, picks, own, out, log, matrix=False):
    if a.code:
        pbs, rules, comm, mapping = P.parse_code(a.code)
        code = a.code.strip()
    else:
        pbs, rules, comm, mapping = P.parse_code(P.config_code())
        code = P.config_code()
    h = hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]
    sdir = out / (("matrix_" if matrix else "sim_") + h)
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / "config_code.txt").write_text(code + "\n", encoding="ascii")
    L = ["# Playbook %s (%s) - config %s" % ("matrix" if matrix else "simulation", P.VERSION, h), "",
         "- %d picks; signal days %s .. %s; engines %s; ranks %s; commission %.3f%% a side" % (
             len(picks), a.d_from, a.d_to, ",".join(a.engines), ",".join(map(str, a.ranks)), comm),
         "- per pick: the playbook's trade (an unfilled pick counts 0) minus buying T+1's open and selling T+6's open "
         "(OPEN6); 95% circular block bootstrap over signal days (10-day blocks, 2,000 draws)", "",
         "config code: `%s`%s" % (code, ("  (--force %s: that playbook on every pick)" % a.force) if a.force and
                                   not matrix else ""), ""]
    srows = []
    if matrix:
        allres = {}
        for k in P.PB_NAMES:
            allres[k] = run_sim(picks, own, pbs, rules, comm, force_pb=k)
        L += ["| category | picks | OPEN6 net / pick | " + " | ".join("%s %s" % (k, pbs[k].E) for k in allres) + " |",
              "|---|---|---|" + "---|" * len(allres)]
        cats = {}
        for k, res in allres.items():
            for s in summarize(res, key=lambda p, pbn: p.cat):
                cats.setdefault(s["group"], {})[k] = s
        for cat in sorted(cats, key=lambda c: -max(v["picks"] for v in cats[c].values())):
            row = cats[cat]
            any_ = next(iter(row.values()))
            cells = []
            for k in allres:
                s = row.get(k)
                cells.append(fmt_ci(*s["diff"][:3]) if s else "-")
                if s:
                    srows.append([cat, k, s["picks"], s["filled"], _f(s["approach"][0]), _f(s["open6"][0]),
                                  _f(s["diff"][0]), _f(s["diff"][1]), _f(s["diff"][2])])
            L.append("| %s | %d | %s | %s |" % (cat, any_["picks"], fmt_ci(*any_["open6"][:3]), " | ".join(cells)))
        L += ["", "Cells: playbook minus OPEN6 per pick (fully at the flat commission). In-sample exploration: a cell "
              "that looks good here is a hypothesis for the holdout, not a finding."]
    else:
        res = run_sim(picks, own, pbs, rules, comm, force_pb=a.force or None)
        rows = []
        for p, pbn, r, base in res:
            rows.append([p.id, p.symbol, p.engine, p.rank, p.T, p.cat, p.regime,
                         getattr(p, "s05", None) or P.s05_at(own[p.symbol][1], p.t_own), pbn, pbs[pbn].E, r["status"],
                         r.get("entry_how", ""), r["entry_i"] - p.t_own if r["entry_i"] is not None else "",
                         _f(r["entry_px"], 4), r["exit_i"] - p.t_own if r["exit_i"] is not None else "",
                         _f(r["exit_px"], 4), r["reason"], _f(r["net"]), _f(base["open6_net"]),
                         _f((r["net"] if r["status"] == "FILLED" else 0.0) - base["open6_net"])
                         if np.isfinite(base["open6_net"]) and r["status"] != "OPEN_AT_END" else "", "", ""])
        write_csv(sdir / "trades.csv", ["trade_id", "symbol", "engine", "rank", "signal_day", "category", "regime",
                                        "s05", "playbook", "entry_rule", "status", "entry_how", "entry_session",
                                        "entry_px", "exit_session", "exit_px", "exit_reason", "net",
                                        "open6_net", "diff_vs_open6", "verdict", "notes"], rows)
        L += ["| category | playbook | picks | filled | playbook net / pick | OPEN6 net / pick | difference | "
              "win (playbook / OPEN6) | per fill: playbook / OPEN6 same picks |", "|---|---|---|---|---|---|---|---|---|"]
        for s in summarize(res):
            cat, k = s["group"]
            L.append("| %s | %s %s | %d | %d | %s | %s | %s | %.0f%% / %.0f%% | %s / %s |" % (
                cat, k, pbs[k].E, s["picks"], s["filled"], fmt_ci(*s["approach"][:3]), fmt_ci(*s["open6"][:3]),
                fmt_ci(*s["diff"][:3]), 100 * s["approach_win"], 100 * s["open6_win"],
                ("%+.2f%%" % (100 * s["per_fill"])) if np.isfinite(s["per_fill"]) else "-",
                ("%+.2f%%" % (100 * s["open6_same_fills"])) if np.isfinite(s["open6_same_fills"]) else "-"))
            srows.append([cat, k, s["picks"], s["filled"], _f(s["approach"][0]), _f(s["open6"][0]), _f(s["diff"][0]),
                          _f(s["diff"][1]), _f(s["diff"][2])])
        tot = summarize(res, key=lambda p, pbn: "ALL")
        if tot:
            s = tot[0]
            L += ["", "**All picks:** playbook %s vs OPEN6 %s per pick; difference %s (%d picks, %d filled)." % (
                fmt_ci(*s["approach"][:3]), fmt_ci(*s["open6"][:3]), fmt_ci(*s["diff"][:3]), s["picks"], s["filled"])]
    write_csv(sdir / "summary.csv", ["category", "playbook", "picks", "filled", "playbook_net", "open6_net", "diff",
                                     "diff_lo", "diff_hi"], srows)
    (sdir / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    log(" %s written to %s" % ("matrix" if matrix else "simulation", sdir))
    return sdir


def ledger(out, rec):
    p = Path(out) / "playbook_ledger.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, sort_keys=True, default=str) + "\n")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(P.VERSION)
        print(__doc__)
        return 2
    if argv[0] == "--version":
        print(P.VERSION)
        return 0
    if argv[0] == "--selftest":
        sys.path.insert(0, str(HERE / "tests"))
        import test_playbook
        return test_playbook.main(argv[1:])
    ap = argparse.ArgumentParser(prog="playbook.py")
    ap.add_argument("command", choices=("export", "sim", "matrix", "journal"))
    ap.add_argument("--root", help="the daily cache root (%%CACHE_DAILY_ROOT%%) - required")
    ap.add_argument("--out", required=True, help="output folder (%%PB_OUT%%)")
    ap.add_argument("--pm-run", default="PM_20261017_001")
    ap.add_argument("--engines", nargs="+", default=["D", "ENS"])
    ap.add_argument("--ranks", default="1-3", help="e.g. 1-3 or 1-10")
    ap.add_argument("--from", dest="d_from", default=DISCOVERY_FROM)
    ap.add_argument("--to", dest="d_to", default=DISCOVERY_TO)
    ap.add_argument("--spend-holdout", action="store_true", help="allow signal days after 2022-12-31")
    ap.add_argument("--export", default="", help="journal: tradelab's export folder (or its name under %%TRADELAB_OUT%%\\export)")
    ap.add_argument("--all-years", action="store_true", help="every year 2015 .. 2026 (needs --spend-holdout)")
    ap.add_argument("--max-chars", type=int, default=4000, help="export: characters per paste file (default 4000)")
    ap.add_argument("--code", default="", help="sim: the config code from the chart")
    ap.add_argument("--force", default="", choices=("",) + P.PB_NAMES,
                    help="sim: one playbook on every pick (the chart's 'Playbook' = Pn)")
    ap.add_argument("--costs", default="stage_e", choices=("stage_e", "replica"), help=argparse.SUPPRESS)
    ap.add_argument("--stage-e-any", action="store_true")
    ap.add_argument("--tradelab-any", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return int(e.code or 2)
    global PINE_MAX
    PINE_MAX = max(1000, a.max_chars)
    if a.all_years:
        a.d_from, a.d_to = "2015-01-01", "2026-12-31"
    if a.command == "journal" and not a.export:
        print("ERROR: journal needs --export <tradelab export folder>")
        return 2
    if not a.root or not Path(a.root).is_dir():
        print("ERROR: --root <cache root> is required (there is no default cache path)")
        return 2
    if a.d_to > DISCOVERY_TO and not a.spend_holdout:
        print("REFUSED: --to %s reaches into 2023-25, the holdout for the frozen tests. Add --spend-holdout to do it "
              "knowingly (it is recorded in playbook_ledger.jsonl)." % a.d_to)
        return 3
    lo, hi = (a.ranks.split("-") + [a.ranks])[:2] if "-" in a.ranks else (a.ranks, a.ranks)
    a.ranks = list(range(int(lo), int(hi) + 1))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print("%s  %s  signal days %s .. %s  engines %s  ranks %s" % (P.VERSION, a.command, a.d_from, a.d_to,
                                                                 ",".join(a.engines), ",".join(map(str, a.ranks))))
    try:
        picks, own, data = load(a.root, a.pm_run, a.engines, a.ranks, a.d_from, a.d_to, stage_e_any=a.stage_e_any,
                                tradelab_any=a.tradelab_any, costs=a.costs)
    except Exception as e:
        if type(e).__name__ in ("V2Error", "TLError", "PLError"):
            print("REFUSED (%s): %s" % (type(e).__name__, e))
            return 3
        raise
    if a.command == "export":
        where = cmd_export(a, picks, own, data, out, print)
    elif a.command == "journal":
        import pb_journal as PJ
        if a.code:
            try:
                P.parse_code(a.code)
            except ValueError as e:
                print("REFUSED: the config code does not parse (%s)" % e)
                return 3
        try:
            where = PJ.cmd_journal(a, picks, own, data, out, print, block_ci)
        except ValueError as e:
            print("REFUSED: %s" % e)
            return 3
    else:
        if a.code:
            try:
                P.parse_code(a.code)
            except ValueError as e:
                print("REFUSED: the config code does not parse (%s)" % e)
                return 3
        where = cmd_sim(a, picks, own, out, print, matrix=(a.command == "matrix"))
    ledger(out, {"at": dt.datetime.now().isoformat(timespec="seconds"), "version": P.VERSION, "command": a.command,
                 "from": a.d_from, "to": a.d_to, "spend_holdout": a.spend_holdout, "engines": a.engines,
                 "ranks": a.ranks, "picks": len(picks), "code": a.code or "default", "force": a.force,
                 "written": str(where),
                 "seconds": round(time.time() - t0, 1)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
