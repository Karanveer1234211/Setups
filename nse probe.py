r"""nse_probe.py - v1.0 (31 Oct 2026)

Probe for the Spec v2 Tier 2 collectors (T2-1 .. T2-5). Run it on your PC: it checks which NSE
sources answer from your connection and how far back each one goes, BEFORE any collector is built.

Sources checked
  delivery   nsearchives  /products/content/sec_bhavdata_full_DDMMYYYY.csv   (one file per date)
  announce   nseindia     /api/corporate-announcements                       (date window)
  boardmeet  nseindia     /api/corporate-board-meetings                      (date window)
  pit        nseindia     /api/corporates-pit                                (date window)
  bulk       nseindia     /api/historical/bulk-deals                         (date window)
  block      nseindia     /api/historical/block-deals                        (date window)

About 35 small requests, 2 seconds apart (roughly 1.5 minutes). Raw answers are saved under
<out>\probe\PROBE_YYYYMMDD_HHMMSS\raw\ and summarised in probe_report.md + probe.json.
Nothing else on your PC is read or changed.

Usage (cmd)
  python nse_probe.py --selftest
  python nse_probe.py --out C:\QuantData\nse_ext
  (or set NSE_EXT_ROOT=C:\QuantData\nse_ext and run without --out)

Guards: --out (or NSE_EXT_ROOT) is required - no default path. The output folder may not sit
inside %CACHE_DAILY_ROOT% or inside any folder named bigmove_deploy, pathlab or tradelab.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import platform
import re
import sys
import time
from pathlib import Path

VERSION = "nse_probe v1.0"
BASE = "https://www.nseindia.com"
ARCH = "https://nsearchives.nseindia.com"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}
DELIVERY_URL = ARCH + "/products/content/sec_bhavdata_full_{d}.csv"  # d = DDMMYYYY
WINDOW_SOURCES = {
    "announce": "/api/corporate-announcements?index=equities&from_date={f}&to_date={t}",
    "boardmeet": "/api/corporate-board-meetings?index=equities&from_date={f}&to_date={t}",
    "pit": "/api/corporates-pit?index=equities&from_date={f}&to_date={t}",
    "bulk": "/api/historical/bulk-deals?from={f}&to={t}",
    "block": "/api/historical/block-deals?from={f}&to={t}",
}
# Known trading days / weeks, newest first: how far back does each source go?
HIST_DATES = ["2025-06-02", "2023-06-01", "2021-06-01", "2020-06-01"]
HIST_WEEKS = [("2025-06-02", "2025-06-06"), ("2023-06-05", "2023-06-09"),
              ("2021-06-07", "2021-06-11"), ("2020-06-01", "2020-06-05")]
FORBIDDEN_DIR_NAMES = ("bigmove_deploy", "pathlab", "tradelab")
DATE_FORMATS = ("%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M", "%d-%b-%Y", "%d-%m-%Y %H:%M:%S",
                "%d-%m-%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d/%m/%Y")


class ProbeError(Exception):
    pass


# ----------------------------------------------------------------------------- transport
class Transport:
    """Real HTTP: one requests.Session, browser-like headers, a cookie warm-up on the home page."""

    def __init__(self, pause=2.0):
        import requests  # imported here so --selftest runs without requests installed
        self.requests_version = requests.__version__
        self.s = requests.Session()
        self.s.headers.update(HEADERS)
        self.pause = pause

    def warm(self):
        r = self.s.get(BASE + "/", timeout=20)
        return r.status_code

    def get(self, url):
        time.sleep(self.pause)
        r = self.s.get(url, timeout=25)
        return r.status_code, r.headers.get("Content-Type", ""), r.content


# ----------------------------------------------------------------------------- parsing
def parse_date(value):
    s = str(value).strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def summarise_csv(body):
    text = body.decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return {"ok": False, "error": "empty file", "rows": 0}
    header = [h.strip() for h in rows[0]]
    data = [r for r in rows[1:] if any(c.strip() for c in r)]
    up = [h.upper() for h in header]
    out = {"ok": True, "rows": len(data), "columns": header,
           "has_delivery": ("DELIV_QTY" in up and "DELIV_PER" in up)}
    if not out["has_delivery"]:
        out["warning"] = "no DELIV_QTY / DELIV_PER columns"
    if "DATE1" in up and data:
        i = up.index("DATE1")
        out["dates_in_file"] = sorted({r[i].strip() for r in data if len(r) > i})[:3]
    if not data:
        out["ok"] = False
        out["error"] = "header only, no rows"
    return out


def records_of(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for k in ("data", "Data", "rows"):
            if isinstance(obj.get(k), list):
                return obj[k]
    return None


def summarise_json(body):
    try:
        obj = json.loads(body.decode("utf-8-sig", errors="replace"))
    except ValueError:
        return {"ok": False, "error": "not valid JSON"}
    recs = records_of(obj)
    if recs is None:
        keys = list(obj)[:8] if isinstance(obj, dict) else type(obj).__name__
        return {"ok": False, "error": "JSON without a record list (%s)" % (keys,)}
    out = {"ok": True, "rows": len(recs), "date_fields": {}, "has_timestamp": False}
    if not recs:
        out["warning"] = "no records in this window"
        return out
    first = recs[0] if isinstance(recs[0], dict) else {}
    out["columns"] = list(first)[:40]
    for k in [k for k in first if re.search(r"(dt|date|time)", k, re.I)]:
        parsed = [parse_date(r.get(k)) for r in recs
                  if isinstance(r, dict) and r.get(k) not in (None, "", "-")]
        parsed = [p for p in parsed if p is not None]
        if parsed:
            out["date_fields"][k] = {
                "min": min(parsed).isoformat(sep=" "),
                "max": max(parsed).isoformat(sep=" "),
                "has_time": any(p.hour or p.minute or p.second for p in parsed),
            }
    out["has_timestamp"] = any(v["has_time"] for v in out["date_fields"].values())
    return out


# ----------------------------------------------------------------------------- probing
def probe_url(tp, url, kind):
    """kind = 'csv' or 'json'. Returns (record, raw bytes)."""
    rec = {"url": url, "kind": kind}
    try:
        status, ctype, body = tp.get(url)
        if status in (401, 403) and kind == "json":
            rec["rewarm_status"] = tp.warm()
            status, ctype, body = tp.get(url)
    except Exception as e:  # network trouble is a finding, not a crash
        rec.update(status=None, ok=False, error="%s: %s" % (type(e).__name__, e))
        return rec, b""
    rec.update(status=status, bytes=len(body), content_type=ctype)
    if status != 200:
        rec.update(ok=False, error="HTTP %s" % status)
        return rec, body
    head = body[:300].lstrip().lower()
    if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
        rec.update(ok=False, error="an HTML page came back instead of data (blocked or moved)")
        return rec, body
    rec.update(summarise_csv(body) if kind == "csv" else summarise_json(body))
    return rec, body


def last_weekdays(today, n):
    d, out = today - dt.timedelta(days=1), []
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d -= dt.timedelta(days=1)
    return out


def save_raw(folder, name, body):
    if body:
        (folder / name).write_bytes(body)


def run_probe(tp, today, outdir):
    raw = outdir / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    results = []
    try:
        w = tp.warm()
        results.append({"source": "warmup", "window": "-", "url": BASE + "/", "status": w,
                        "ok": w == 200, "error": None if w == 200 else "HTTP %s" % w})
    except Exception as e:
        results.append({"source": "warmup", "window": "-", "url": BASE + "/", "status": None,
                        "ok": False, "error": "%s: %s" % (type(e).__name__, e)})
    # delivery: the latest weekday that has a file (up to 5 tries; holidays have none), then history
    for d in last_weekdays(today, 5):
        rec, body = probe_url(tp, DELIVERY_URL.format(d=d.strftime("%d%m%Y")), "csv")
        rec.update(source="delivery", window=d.isoformat())
        results.append(rec)
        save_raw(raw, "delivery_%s.csv" % d.strftime("%Y%m%d"), body)
        if rec.get("ok"):
            break
    for s in HIST_DATES:
        d = dt.date.fromisoformat(s)
        rec, body = probe_url(tp, DELIVERY_URL.format(d=d.strftime("%d%m%Y")), "csv")
        rec.update(source="delivery", window=d.isoformat())
        results.append(rec)
        save_raw(raw, "delivery_%s.csv" % d.strftime("%Y%m%d"), body)
    # windowed JSON sources: the last 7 days, then one week in 2025, 2023, 2021, 2020
    windows = [(today - dt.timedelta(days=7), today - dt.timedelta(days=1))]
    windows += [(dt.date.fromisoformat(a), dt.date.fromisoformat(b)) for a, b in HIST_WEEKS]
    for name, path in WINDOW_SOURCES.items():
        for f, t in windows:
            url = BASE + path.format(f=f.strftime("%d-%m-%Y"), t=t.strftime("%d-%m-%Y"))
            rec, body = probe_url(tp, url, "json")
            rec.update(source=name, window="%s..%s" % (f.isoformat(), t.isoformat()))
            results.append(rec)
            save_raw(raw, "%s_%s.json" % (name, f.strftime("%Y%m%d")), body)
    return results


def verdicts(results):
    """One line per source: reachable, how far back rows came, timestamps."""
    out = {}
    for name in ["delivery"] + list(WINDOW_SOURCES):
        recs = [r for r in results if r.get("source") == name]
        oks = [r for r in recs if r.get("ok") and r.get("rows", 0) > 0]
        if not oks:
            errs = sorted({str(r.get("error") or r.get("warning")) for r in recs})
            out[name] = {"usable": False, "line": "NOT USABLE from this PC: " + "; ".join(errs)}
            continue
        earliest = min(r["window"] for r in oks)
        ts = any(r.get("has_timestamp") for r in oks)
        extra = ""
        if name == "delivery":
            extra = ("; delivery columns present" if all(r.get("has_delivery") for r in oks)
                     else "; delivery columns MISSING in some files")
        elif name in ("announce", "pit", "boardmeet"):
            extra = "; timestamps with time of day" if ts else "; dates only, no time of day"
        out[name] = {"usable": True, "earliest_window_with_rows": earliest, "has_timestamp": ts,
                     "line": "USABLE - earliest window with rows: %s (%d of %d probes ok)%s"
                             % (earliest, len(oks), len(recs), extra)}
    return out


def write_report(outdir, results, meta):
    v = verdicts(results)
    (outdir / "probe.json").write_text(json.dumps({"meta": meta, "verdicts": v, "results": results},
                                                  indent=2, default=str), encoding="utf-8")
    lines = ["# NSE probe - %s" % meta["run_at"], "", VERSION, "",
             "## Verdict per source", ""]
    for name, item in v.items():
        lines.append("- **%s**: %s" % (name, item["line"]))
    lines += ["", "## Every request", "", "| source | window | status | rows | note |",
              "| --- | --- | --- | --- | --- |"]
    for r in results:
        note = r.get("error") or r.get("warning") or ""
        if not note and r.get("source") == "delivery" and r.get("ok"):
            note = "delivery cols" if r.get("has_delivery") else "NO delivery cols"
        if not note and r.get("date_fields"):
            note = "timestamps" if r.get("has_timestamp") else "dates only"
        lines.append("| %s | %s | %s | %s | %s |" % (r.get("source"), r.get("window"),
                                                    r.get("status"), r.get("rows", ""), note))
    lines += ["", "Send this file (and probe.json) back to Claude."]
    (outdir / "probe_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return v


# ----------------------------------------------------------------------------- guards / main
def resolve_out(arg_out, env):
    out = arg_out or env.get("NSE_EXT_ROOT")
    if not out:
        raise ProbeError("give --out C:\\QuantData\\nse_ext (or set NSE_EXT_ROOT); there is no default")
    p = Path(out).resolve()
    cache = env.get("CACHE_DAILY_ROOT")
    if cache:
        c = Path(cache).resolve()
        if p == c or c in p.parents:
            raise ProbeError("refused: %s is inside CACHE_DAILY_ROOT (%s)" % (p, c))
    lowered = [part.lower() for part in p.parts]
    for bad in FORBIDDEN_DIR_NAMES:
        if bad in lowered:
            raise ProbeError("refused: %s is inside a %s folder" % (p, bad))
    return p


def main(argv=None, env=None, transport=None, today=None):
    env = os.environ if env is None else env
    ap = argparse.ArgumentParser(description=VERSION)
    ap.add_argument("--out", help="output root, e.g. C:\\QuantData\\nse_ext")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        root = resolve_out(args.out, env)
    except ProbeError as e:
        print("STOP:", e)
        return 2
    tp = transport or Transport()
    today = today or dt.date.today()
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = root / "probe" / ("PROBE_" + stamp)
    outdir.mkdir(parents=True, exist_ok=False)
    print("%s - writing to %s" % (VERSION, outdir))
    print("About 35 requests, 2 s apart: roughly 1.5 minutes.")
    results = run_probe(tp, today, outdir)
    meta = {"version": VERSION, "run_at": dt.datetime.now().isoformat(sep=" ", timespec="seconds"),
            "today": today.isoformat(), "python": platform.python_version(),
            "requests": getattr(tp, "requests_version", "n/a"), "out": str(outdir)}
    v = write_report(outdir, results, meta)
    print("")
    for name, item in v.items():
        print("%-9s %s" % (name, item["line"]))
    print("")
    print("Report: %s" % (outdir / "probe_report.md"))
    return 0


# ----------------------------------------------------------------------------- self-test
class FakeTransport:
    """Scripted answers keyed by URL substring; counts warm-ups; records every URL asked."""

    def __init__(self, script, default=(404, "text/html", b"not found"), warm_status=200):
        self.script, self.default, self.warm_status = script, default, warm_status
        self.warms, self.asked, self.requests_version = 0, [], "fake"

    def warm(self):
        self.warms += 1
        return self.warm_status

    def get(self, url):
        self.asked.append(url)
        for key, answer in self.script:
            if key in url:
                if callable(answer):
                    return answer(self)
                return answer
        return self.default


def _csv(deliv=True, date1="30-Oct-2026", rows=3):
    head = "SYMBOL, SERIES, DATE1, PREV_CLOSE, CLOSE_PRICE, TTL_TRD_QNTY"
    if deliv:
        head += ", DELIV_QTY, DELIV_PER"
    lines = [head]
    for i in range(rows):
        line = "SYM%d, EQ, %s, 100, 101, 5000" % (i, date1)
        if deliv:
            line += ", 2500, 50.00"
        lines.append(line)
    return ("\n".join(lines) + "\n").encode()


def _json(recs, wrap=False):
    return json.dumps({"data": recs} if wrap else recs).encode()


def selftest():
    import tempfile
    fails = []

    def check(name, cond, detail=""):
        print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  -> " + str(detail)))
        if not cond:
            fails.append(name)

    # t1 CSV: spaced NSE headers, delivery present (planted) and absent
    s = summarise_csv(_csv(True))
    check("t1a csv rows and delivery columns", s["ok"] and s["rows"] == 3 and s["has_delivery"], s)
    check("t1b csv date read", s.get("dates_in_file") == ["30-Oct-2026"], s)
    s = summarise_csv(_csv(False))
    check("t1c csv without delivery is flagged", s["ok"] and not s["has_delivery"] and "warning" in s, s)
    s = summarise_csv(b"SYMBOL, DELIV_QTY, DELIV_PER\n")
    check("t1d header-only csv is not ok", not s["ok"], s)

    # t2 JSON: timestamps planted vs absent; wrappers; empties; junk
    recs = [{"symbol": "AAA", "an_dt": "30-Oct-2026 18:45:12", "desc": "Outcome of Board Meeting"},
            {"symbol": "BBB", "an_dt": "29-Oct-2026 09:05:00", "desc": "Press Release"}]
    s = summarise_json(_json(recs))
    check("t2a json list rows + timestamp", s["ok"] and s["rows"] == 2 and s["has_timestamp"], s)
    check("t2b json min/max", s["date_fields"]["an_dt"]["min"].startswith("2026-10-29 09:05")
          and s["date_fields"]["an_dt"]["max"].startswith("2026-10-30 18:45"), s)
    s = summarise_json(_json([{"symbol": "AAA", "date": "30-10-2026"}], wrap=True))
    check("t2c json wrapped in data, dates only", s["ok"] and s["rows"] == 1 and not s["has_timestamp"], s)
    s = summarise_json(_json([{"symbol": "AAA", "an_dt": "30-Oct-2026 00:00:00"}]))
    check("t2d midnight-only stamps are not timestamps", not s["has_timestamp"], s)
    s = summarise_json(_json([]))
    check("t2e empty window flagged", s["ok"] and s["rows"] == 0 and "warning" in s, s)
    check("t2f junk is not json", not summarise_json(b"\x00\x01garbage")["ok"])
    check("t2g dict without list", not summarise_json(_json({"msg": "x"}).replace(b'"data"', b'"msg"'))["ok"])

    # t3 probe_url: HTML wall, 401 then 200 after re-warm, 404, network error
    tp = FakeTransport([("html", (200, "text/html", b"<!DOCTYPE html><html>blocked</html>"))])
    rec, _ = probe_url(tp, "https://x/html", "json")
    check("t3a html page is a block, not data", not rec["ok"] and "HTML" in rec["error"], rec)
    state = {"n": 0}

    def flaky(t):
        state["n"] += 1
        return (401, "application/json", b"{}") if state["n"] == 1 else (200, "application/json", _json(recs))
    tp = FakeTransport([("flaky", flaky)])
    rec, _ = probe_url(tp, "https://x/flaky", "json")
    check("t3b 401 -> re-warm -> ok", rec["ok"] and tp.warms == 1 and rec["rows"] == 2, rec)
    rec, _ = probe_url(FakeTransport([]), "https://x/none", "csv")
    check("t3c 404 recorded", not rec["ok"] and rec["error"] == "HTTP 404", rec)

    class Boom(FakeTransport):
        def get(self, url):
            raise ConnectionError("no route")
    rec, _ = probe_url(Boom([]), "https://x/any", "csv")
    check("t3d network error recorded, no crash", not rec["ok"] and "ConnectionError" in rec["error"], rec)

    # t4 end to end on a scripted world: delivery to 2023 only, announcements with stamps, bulk blocked
    today = dt.date(2026, 10, 31)  # a Saturday: the latest weekday is Fri 30 Oct
    script = [
        ("sec_bhavdata_full_30102026", (200, "text/csv", _csv(True))),
        ("sec_bhavdata_full_02062025", (200, "text/csv", _csv(True, "02-Jun-2025"))),
        ("sec_bhavdata_full_01062023", (200, "text/csv", _csv(True, "01-Jun-2023"))),
        ("corporate-announcements", (200, "application/json", _json(recs))),
        ("corporate-board-meetings", (200, "application/json", _json([{"bm_date": "05-Nov-2026"}]))),
        ("corporates-pit", (200, "application/json", _json([], wrap=True))),
        ("bulk-deals", (200, "text/html", b"<html>Access Denied</html>")),
    ]
    tmp = Path(tempfile.mkdtemp())
    rc = main(["--out", str(tmp)], env={}, transport=FakeTransport(script), today=today)
    folders = list((tmp / "probe").glob("PROBE_*"))
    check("t4a run ends 0 and writes one PROBE folder", rc == 0 and len(folders) == 1, (rc, folders))
    report = (folders[0] / "probe_report.md").read_text(encoding="utf-8")
    data = json.loads((folders[0] / "probe.json").read_text(encoding="utf-8"))
    v = data["verdicts"]
    check("t4b delivery usable back to 2023-06-01", v["delivery"]["usable"]
          and v["delivery"]["earliest_window_with_rows"] == "2023-06-01", v["delivery"])
    check("t4c announcements usable with timestamps", v["announce"]["usable"] and v["announce"]["has_timestamp"],
          v["announce"])
    check("t4d bulk blocked -> not usable, reason kept", (not v["bulk"]["usable"]) and "HTML" in v["bulk"]["line"],
          v["bulk"])
    check("t4e empty pit windows -> not usable", not v["pit"]["usable"], v["pit"])
    check("t4f block (unscripted 404) -> not usable", not v["block"]["usable"] and "404" in v["block"]["line"],
          v["block"])
    check("t4g report lists every request", report.count("\n| ") >= 1 + len(data["results"]), len(data["results"]))
    check("t4h raw samples saved", (folders[0] / "raw" / "delivery_20261030.csv").exists())
    asked_dates = [u for u in data["results"] if u.get("source") == "delivery"]
    check("t4i stops at the first good recent weekday", asked_dates[0]["window"] == "2026-10-30", asked_dates[0])

    # t5 guards: no out, inside the cache, inside a forbidden folder
    check("t5a no --out and no env -> STOP", main([], env={}, transport=FakeTransport([]), today=today) == 2)
    cache = Path(tempfile.mkdtemp())
    check("t5b out inside CACHE_DAILY_ROOT -> STOP",
          main(["--out", str(cache / "ext")], env={"CACHE_DAILY_ROOT": str(cache)},
               transport=FakeTransport([]), today=today) == 2)
    check("t5c out inside a pathlab folder -> STOP",
          main(["--out", str(tmp / "pathlab" / "x")], env={}, transport=FakeTransport([]), today=today) == 2)
    check("t5d NSE_EXT_ROOT accepted", resolve_out(None, {"NSE_EXT_ROOT": str(tmp / "ok")}) == (tmp / "ok").resolve())

    # t6 ascii-only source (project rule for shipped modules)
    src = Path(__file__).read_bytes()
    check("t6 module text is ASCII", all(b < 128 for b in src))

    print("")
    if fails:
        print("SELFTEST FAILED (%s): %s" % (VERSION, ", ".join(fails)))
        return 1
    print("VERIFIED (%s)" % VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
