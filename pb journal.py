"""
pb_journal.py - playbook v1.1's journal command (add-on): every BigMove pick in tradelab's export, the long-position map's
playbook on it, all ten playbooks, OPEN6 and BigMove's own trade side by side, in one Excel file.

    python playbook.py journal --root %CACHE_DAILY_ROOT% --out %PB_OUT% --export <TLX folder or name>
        [--all-years --spend-holdout]   every year of the export instead of 2020-22 (2023-25 is then spent)
        [--code "BMPB2|..."]            a map / playbooks changed on the chart (the PBCFG line)

Reads tradelab's export READ ONLY (trades.parquet, checked against outputs.sha256 when that file is there). Writes
%PB_OUT%\\journal\\PLAYBOOK_JOURNAL.xlsx and playbook_journal.csv. TRADE_JOURNAL.xlsx is never opened or changed.
Your columns (My verdict, Tags, Note) are carried over by trade id every time you run it again.
"""
from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

import pb_core as P

JOURNAL_NAME = "PLAYBOOK_JOURNAL.xlsx"
USER_COLS = ["My verdict", "Tags", "Note"]
STATE_NUM = {1: "S01", 2: "S02", 3: "S03", 6: "S06", 7: "S07", 8: "S08", 9: "S09", 12: "S12", 0: "UNK", -1: "INS"}
EVENT_NUM = {0: "NONE", 1: "BO_NEW", 2: "BO_CONF", 3: "BO_STALL", 4: "FBO", 5: "BD_NEW", 6: "BD_CONF", 7: "BD_STALL",
             8: "FBD"}
J_COLS = ["trade_id", "engine", "rank", "symbol", "signal_day", "traded", "status", "entry_day", "entry", "exit_day",
          "exit_price", "exit_kind", "sessions_held", "net_bp", "open6_net_bp", "open6_status", "mfe", "mae",
          "excess_bp", "pre_state_num", "pre_state_event_num", "pre_state_confidence", "pre_state_phase",
          "pre_environment", "score"]
OPEN6_TOL = 0.002          # 0.2% gross: the cache's OPEN6 vs the export's


def resolve_export(arg):
    p = Path(arg)
    if not p.is_dir():
        base = os.environ.get("TRADELAB_OUT", "")
        if not base:
            raise ValueError("--export %s is not a folder and TRADELAB_OUT is not set: give the full path" % arg)
        p = Path(base) / "export" / arg
    if not (p / "trades.parquet").is_file():
        raise ValueError("no trades.parquet in %s" % p)
    sha = p / "outputs.sha256"
    if sha.is_file():
        h = hashlib.sha256((p / "trades.parquet").read_bytes()).hexdigest()
        if h not in sha.read_text(encoding="utf-8", errors="replace"):
            raise ValueError("trades.parquet does not match the export's outputs.sha256 (changed after export)")
    return p


def read_export(ex):
    import pyarrow.parquet as pq
    have = set(pq.read_schema(ex / "trades.parquet").names)
    J = pd.read_parquet(ex / "trades.parquet", columns=[c for c in J_COLS if c in have])
    if "traded" in J.columns:
        J = J[J["traded"].fillna(False).astype(bool)]
    return J.drop_duplicates("trade_id").set_index("trade_id")


def _num(x):
    try:
        v = float(x)
        return v if np.isfinite(v) else np.nan
    except (TypeError, ValueError):
        return np.nan


def integrity(p, j, base6_gross):
    """JOURNAL MATCHED / MISSING RECORD / SYMBOL MISMATCH / STATE DIFFERS / EVENT DIFFERS / DATA MISMATCH."""
    if j is None:
        return "MISSING RECORD", ""
    if str(j.get("symbol", p.symbol)) != p.symbol:
        return "SYMBOL MISMATCH", "export %s" % j.get("symbol")
    sn = _num(j.get("pre_state_num"))
    if np.isfinite(sn) and STATE_NUM.get(int(sn), "?") != p.state:
        return "STATE DIFFERS", "export %s" % STATE_NUM.get(int(sn), sn)
    en = _num(j.get("pre_state_event_num"))
    if np.isfinite(en) and EVENT_NUM.get(int(en), "?") != p.event:
        return "EVENT DIFFERS", "export %s" % EVENT_NUM.get(int(en), en)
    o6 = _num(j.get("open6_net_bp"))
    if np.isfinite(o6) and np.isfinite(base6_gross) and abs((o6 + 35.0) / 1e4 - base6_gross) > OPEN6_TOL:
        return "DATA MISMATCH", "OPEN6 gross export %.2f%% vs cache %.2f%%" % ((o6 + 35) / 100, base6_gross * 100)
    if p.event in ("BO_NEW", "BO_CONF", "BO_STALL", "FBO", "BD_NEW", "BD_CONF", "BD_STALL", "FBD") and \
            not np.isfinite(p.lvl):
        return "EVENT LEVEL UNVERIFIED", "no level for %s" % p.event
    return "JOURNAL MATCHED", ""


def _sel(r):
    """Selection view: a pick that never filled counts 0."""
    if r["status"] == "FILLED" and np.isfinite(r["net"]):
        return float(r["net"])
    return np.nan if r["status"] == "OPEN_AT_END" else 0.0


def build(picks, own, data, J, pbs, rules, comm, block_ci):
    days = np.asarray(data.cal.days)
    rows = []
    for p in picks:
        idx, ob = own[p.symbol]
        x = getattr(p, "s05", None) or P.s05_at(ob, p.t_own)
        pbn = P.match(rules, p.state, p.event, p.regime, x)
        base = P.baseline(ob, p.t_own, comm)
        b6 = float(base["open6_net"]) if np.isfinite(base["open6_net"]) else np.nan
        allr = {k: P.simulate_pick(ob, p.t_own, pbs[k], p.lvl, comm) for k in P.PB_NAMES}
        r = allr[pbn]
        j = J.loc[p.id].to_dict() if p.id in J.index else None
        integ, why = integrity(p, j, _num(p.base.get("open6_gross")))
        d = lambda i: str(days[idx[i]]) if i is not None else ""
        mfe = mae = np.nan
        if r["entry_i"] is not None:
            e, xi = r["entry_i"], (r["exit_i"] if r["exit_i"] is not None else ob.n - 1)
            mfe = float(np.max(ob.h[e:xi + 1]) / r["entry_px"] - 1)
            mae = float(np.min(ob.l[e:xi + 1]) / r["entry_px"] - 1)
        sel = _sel(r)
        alls = {k: _sel(v) for k, v in allr.items()}
        fin = {k: v for k, v in alls.items() if np.isfinite(v)}
        best = max(fin, key=fin.get) if fin and np.isfinite(b6) else ""
        jj = j or {}
        row = {
            "trade_id": p.id, "engine": p.engine, "rank": p.rank, "symbol": p.symbol, "signal_day": p.T,
            "year": int(p.T[:4]), "integrity": integ, "integrity_detail": why,
            "state": p.state, "event": p.event, "event_age": p.age, "regime": p.regime, "S05": x,
            "category": p.cat, "event_level": p.lvl if np.isfinite(p.lvl) else np.nan,
            "BigMove net % (export)": _num(jj.get("net_bp")) / 100, "BigMove exit (export)": jj.get("exit_kind", ""),
            "BigMove held (export)": _num(jj.get("sessions_held")),
            "OPEN6 net % (export, 35bp)": _num(jj.get("open6_net_bp")) / 100,
            "State confidence (export)": jj.get("pre_state_confidence", ""),
            "State phase (export)": jj.get("pre_state_phase", ""),
            "Environment (export)": jj.get("pre_environment", ""),
            "Playbook": pbn, "Playbook name": getattr(pbs[pbn], "title", ""),
            "Fill status": r["status"], "Entry day": d(r["entry_i"]),
            "Entry T+": (r["entry_i"] - p.t_own) if r["entry_i"] is not None else np.nan,
            "Entry price": r["entry_px"], "Order price": r["trig"],
            "Stop": r["stop"], "Target": r["target"],
            "Exit day": d(r["exit_i"]), "Exit price": r["exit_px"], "Exit reason": r["reason"],
            "Held": (r["exit_i"] - r["entry_i"]) if r["exit_i"] is not None and r["entry_i"] is not None else np.nan,
            "Playbook net %": r["net"] * 100 if np.isfinite(r["net"]) else np.nan,
            "OPEN6 net %": b6 * 100,
            "Selection net - OPEN6 bp": (sel - b6) * 1e4 if np.isfinite(sel) and np.isfinite(b6) else np.nan,
            "Per fill - OPEN6 bp": (r["net"] - b6) * 1e4 if r["status"] == "FILLED" and np.isfinite(b6) else np.nan,
            "MFE %": mfe * 100, "MAE %": mae * 100,
            "Capture %": (r["net"] / mfe * 100) if np.isfinite(r["net"]) and np.isfinite(mfe) and mfe > 0 else np.nan,
            "Major winner (OPEN6 > 10%)": bool(np.isfinite(b6) and b6 > 0.10),
        }
        for k in P.PB_NAMES:
            row["%s sel - OPEN6 bp" % k] = (alls[k] - b6) * 1e4 if np.isfinite(alls[k]) and np.isfinite(b6) else np.nan
        row["Best playbook (hindsight)"] = best
        rows.append(row)
    T = pd.DataFrame(rows)
    return T


def summaries(T, block_ci):
    def ci(g, col):
        g = g[np.isfinite(g[col])]
        if len(g) < 2:
            return np.nan, np.nan, np.nan
        m, lo, hi = block_ci(list(g["signal_day"]), list(g[col] / 1e4))[:3]
        return m * 1e4, lo * 1e4, hi * 1e4

    out = {}
    rows = []
    for (cat, pbn), g in T.groupby(["category", "Playbook"]):
        m, lo, hi = ci(g, "Selection net - OPEN6 bp")
        rows.append({"category": cat, "Playbook": pbn, "picks": len(g),
                     "fill %": 100 * (g["Fill status"] == "FILLED").mean(),
                     "sel - OPEN6 bp": m, "95% lo": lo, "95% hi": hi,
                     "per fill - OPEN6 bp": g["Per fill - OPEN6 bp"].mean(),
                     "playbook win %": 100 * (g["Playbook net %"] > 0).mean(),
                     "OPEN6 win %": 100 * (g["OPEN6 net %"] > 0).mean(),
                     "majors kept": int(((g["Major winner (OPEN6 > 10%)"]) & (g["Fill status"] == "FILLED")).sum()),
                     "majors": int(g["Major winner (OPEN6 > 10%)"].sum()),
                     "avg MFE %": g["MFE %"].mean(), "avg MAE %": g["MAE %"].mean(),
                     "avg capture %": g["Capture %"].mean(),
                     "avg entry T+": g["Entry T+"].mean(), "avg held": g["Held"].mean(),
                     "top exit": g["Exit reason"].replace("", np.nan).mode().iloc[0]
                     if g["Exit reason"].replace("", np.nan).notna().any() else ""})
    out["By category"] = pd.DataFrame(rows).sort_values("picks", ascending=False)
    mcols = ["%s sel - OPEN6 bp" % k for k in P.PB_NAMES]
    M = T.groupby("category")[mcols].mean()
    M.insert(0, "picks", T.groupby("category").size())
    M["mapped"] = T.groupby("category")["Playbook"].agg(lambda s: s.mode().iloc[0])
    out["Matrix"] = M.sort_values("picks", ascending=False).reset_index()
    rows = []
    for (y, e), g in T.groupby(["year", "engine"]):
        m, lo, hi = ci(g, "Selection net - OPEN6 bp")
        rows.append({"year": y, "engine": e, "picks": len(g), "sel - OPEN6 bp": m, "95% lo": lo, "95% hi": hi,
                     "playbook net % / pick": g["Playbook net %"].fillna(0).mean(),
                     "OPEN6 net % / pick": g["OPEN6 net %"].mean(),
                     "BigMove net % / pick (export)": g["BigMove net % (export)"].mean()})
    out["By year"] = pd.DataFrame(rows)
    I = T.groupby("integrity").size().rename("picks").reset_index()
    out["Integrity"] = I
    return out


def carry_notes(T, old):
    if not old.is_file():
        return T, 0
    try:
        O = pd.read_excel(old, sheet_name="Trades", usecols=lambda c: c in ["trade_id"] + USER_COLS, dtype=str)
    except Exception:
        return T, 0
    O = O.dropna(subset=["trade_id"]).drop_duplicates("trade_id").set_index("trade_id")
    for c in USER_COLS:
        T[c] = T["trade_id"].map(O[c]) if c in O.columns else ""
    T[USER_COLS] = T[USER_COLS].fillna("")
    return T, int((T[USER_COLS] != "").any(axis=1).sum())


README = [
    ("What", "Every BigMove pick (D and ENS, ranks 1-3) from tradelab's export, with the long-position map's playbook "
             "traded on the cache's daily bars by the chart's exact rules, OPEN6 on the same bars, all ten playbooks, "
             "and BigMove's own trade from the export."),
    ("Selection net - OPEN6 bp", "every pick counts; a pick whose order never filled counts 0 (missed or avoided)"),
    ("Per fill - OPEN6 bp", "filled trades only, each against its own OPEN6 (trade quality)"),
    ("Costs", "playbook and OPEN6 columns: 0.175% a side (the chart's). Export columns: tradelab's 35 bp round trip."),
    ("integrity", "JOURNAL MATCHED; MISSING RECORD (no row in the export); SYMBOL MISMATCH; STATE DIFFERS / EVENT "
                  "DIFFERS (the export's tl_state vs the cache's now); DATA MISMATCH (OPEN6 gross off by > 0.2%); EVENT "
                  "LEVEL UNVERIFIED (an event with no level)"),
    ("P1..P10 sel - OPEN6 bp", "each playbook forced on the pick. In-sample: a hypothesis, not a finding"),
    ("Best playbook (hindsight)", "the best of the ten after the fact. Never a rule: it is chosen with the future"),
    ("MFE / MAE / Capture", "best high / worst low between entry and exit vs entry; capture = net / MFE"),
    ("Major winner", "OPEN6 net above 10%: majors kept = how many the playbook still owned"),
    ("Your columns", "My verdict, Tags (e.g. FALSE_BREAK, EARLY_ENTRY, LATE_ENTRY, MISSED_WINNER, GOOD_EXIT, BAD_EXIT), "
                     "Note. Type in this file; the next run carries them over by trade id (the old file is kept as "
                     "PLAYBOOK_JOURNAL_prev.xlsx)."),
    ("Intervals", "95% circular block bootstrap over signal days (10-day blocks). Many groups at once: one interval "
                  "clear of 0 is not proof."),
]


def write_xlsx(path, T, S, info):
    from openpyxl.styles import Font, PatternFill
    tmp = path.with_name("." + path.name + ".partial.xlsx")
    with pd.ExcelWriter(tmp, engine="openpyxl") as xw:
        T.to_excel(xw, sheet_name="Trades", index=False)
        for k, v in S.items():
            v.to_excel(xw, sheet_name=k, index=False)
        pd.DataFrame([{"item": "run", "meaning": info}] + [{"item": a, "meaning": b} for a, b in README]).to_excel(
            xw, sheet_name="Read me", index=False)
        good, bad = PatternFill("solid", fgColor="C6EFCE"), PatternFill("solid", fgColor="FFC7CE")
        for name, ws in xw.sheets.items():
            ws.freeze_panes = "B2" if name != "Trades" else "F2"
            ws.auto_filter.ref = ws.dimensions
            for c in ws[1]:
                c.font = Font(bold=True)
            hdr = [c.value for c in ws[1]]
            for col in ("Selection net - OPEN6 bp", "sel - OPEN6 bp"):
                if col in hdr:
                    k = hdr.index(col) + 1
                    for row in ws.iter_rows(min_row=2, min_col=k, max_col=k):
                        v = row[0].value
                        if isinstance(v, (int, float)) and v == v and v != 0:
                            row[0].fill = good if v > 0 else bad
            for i, h in enumerate(hdr, 1):
                ws.column_dimensions[ws.cell(1, i).column_letter].width = max(9, min(28, len(str(h)) + 2))
    os.replace(tmp, path)


def cmd_journal(a, picks, own, data, out, log, block_ci):
    ex = resolve_export(a.export)
    J = read_export(ex)
    if a.code:
        pbs, rules, comm, _ = P.parse_code(a.code)
    else:
        pbs, rules, comm, _ = P.parse_code(P.config_code())
    T = build(picks, own, data, J, pbs, rules, comm, block_ci)
    seen = set(T["trade_id"])
    lo, hi = a.d_from, a.d_to
    sd = J["signal_day"].astype(str).str[:10] if "signal_day" in J.columns else pd.Series(dtype=str)
    eng = J["engine"] if "engine" in J.columns else pd.Series("", index=J.index)
    rk = pd.to_numeric(J["rank"], errors="coerce") if "rank" in J.columns else pd.Series(1, index=J.index)
    want = J.index[(sd >= lo) & (sd <= hi) & eng.isin(a.engines) & rk.isin(a.ranks)]
    miss = [t for t in want if t not in seen]
    log(" journal: export %d traded rows, %d in range, %d of them not on the cache" % (len(J), len(want), len(miss)))
    if miss:
        M = J.loc[miss].reset_index()
        T = pd.concat([T, pd.DataFrame({"trade_id": M["trade_id"], "engine": M.get("engine"),
                                        "rank": M.get("rank"), "symbol": M.get("symbol"),
                                        "signal_day": M["signal_day"].astype(str).str[:10] if "signal_day" in M else "",
                                        "integrity": "NOT ON THE CACHE",
                                        "integrity_detail": "in the export, no pick / no bar on T in the cache"})],
                      ignore_index=True)
    jdir = out / "journal"
    jdir.mkdir(parents=True, exist_ok=True)
    path = jdir / JOURNAL_NAME
    T, kept = carry_notes(T, path)
    for c in USER_COLS:
        if c not in T.columns:
            T[c] = ""
    T = T.sort_values(["signal_day", "engine", "rank"], ascending=[False, True, True])
    ok = T[T["integrity"].isin(["JOURNAL MATCHED", "EVENT LEVEL UNVERIFIED"]) & T["Fill status"].notna()]
    S = summaries(ok, block_ci)
    S["Integrity"] = T.groupby("integrity").size().rename("picks").reset_index()
    if path.is_file():
        shutil.copy2(path, jdir / "PLAYBOOK_JOURNAL_prev.xlsx")
    code = (a.code or P.config_code()).strip()
    info = "%s | export %s | signal days %s .. %s | config %s" % (P.VERSION, ex.name, lo, hi, code)
    try:
        write_xlsx(path, T, S, info)
    except PermissionError:
        raise ValueError("cannot write %s: it is open in Excel (close it)" % path)
    T.to_csv(jdir / "playbook_journal.csv", index=False)
    vc = T["integrity"].value_counts().to_dict()
    log(" journal: %d picks (%s); notes carried over on %d; summaries on %d matched picks -> %s" % (
        len(T), ", ".join("%s %d" % kv for kv in vc.items()), kept, len(ok), path))
    return path
