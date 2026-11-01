r"""pb_core.py - the BigMove playbook v1.1: categories, ten long playbooks, the config code and a TradingView-faithful
mirror of the Pine strategy.

A pick's CATEGORY is tl_state's confirmed state and shown event at the pick's close T, the market regime, and the S05
overextension flag on the chart at T:
    state   S01 S02 S03 S06 S07 S08 S09 S12 UNK INS
    event   BO_NEW BO_CONF BO_STALL FBO BD_NEW BD_CONF BD_STALL FBD NONE
            (S04 breakout new / confirmed / stalled, S11 failed breakout, S10 breakdown new / confirmed / stalled,
             failed breakdown = bear trap, none)
    regime  BB broad bullish, NB narrow bullish, MX mixed, BR broad bearish, HS high stress, NA unknown
    S05     N none, OV overextended, EX extreme (tl_state's thresholds on the chart's own bars at T: (close - EMA20) /
            ATR >= 3, (close - EMA50) / ATR >= 6 or (close - close 10 sessions ago) / ATR >= 6 = OV; EMA20 gap >= 4.5 or
            EMA50 gap >= 9 ATR = EX)
The LONG POSITION MAP sends each category to one of ten PLAYBOOKS, first matching rule wins:
    STATE:EVENT[:REGIME[:S05]]=Pn; ...  ('*' = any; lists with commas), e.g. *:BD_NEW,BD_CONF,BD_STALL:*=P10
A PLAYBOOK = entry + invalidation + protective stop + target + exits (every field tweakable; the Pine script has the
same fields, defaults and order of events):
    E   entry   OPEN   market at T+1's open (G > 0: a limit at T's close x (1 + G%) for T+1 only)
                DELAY  market at the open of T+1+V
                STH    buy-stop at T's high + O x ATR(T), T+1 .. T+V                (stop-limit: + L x ATR; L = 0: plain)
                STPD   buy-stop at the previous session's high + O x ATR, re-set each evening, T+1 .. T+V
                STLV   buy-stop at the event level + O x ATR(T) (reclaim of a failed breakout / breakdown level)
                LMLV   limit at the event level + O x ATR(T) (retest of the breakout level)
                LMTC   limit at T's close - O x ATR(T) (pullback)
                LMEMA  limit at EMA20 + O x ATR, re-set each evening
                SWHI   buy-stop at the last confirmed swing high + O x ATR, re-set each evening (no order while that
                       trigger is at or below the close)
                STRNG  buy-stop at the N-session high + O x ATR, re-set each evening (range breakout)
                LMRNG  limit at the N-session low + O x ATR, re-set each evening (buy the range floor)
                SKIP   no trade
        Buy-stops follow the 'already through' rule: STH / STLV whose trigger is at or below the last close are not
        placed (or are cancelled); the re-set ones (STPD / SWHI / STRNG) skip that evening.
    F   if nothing filled in the window: NONE, or OPEN (market at the next open)
    IV  invalidation while the entry waits: NONE | TLOW (a close below T's low - IK x ATR(T)) | LVL (below the event
        level - IK x ATR(T)) | SWL (below the last confirmed swing low - IK x ATR) | EMA50 (below EMA50 - IK x ATR):
        the order is cancelled and the pick is INVALID (no fallback). Checked at every evening the entry waits, T
        included.
    S   stop    NONE | ATR (entry - SK x ATR at the entry close) | PCT (entry x (1 - SK%)) | TLOW (T's low - SK x ATR(T))
                | LVL (event level - SK x ATR(T)) | SWL (the last confirmed swing low at the entry close - SK x ATR;
                only while below that close) | RNG (the N-session low at the entry close - SK x ATR)
    T   target  NONE | R (entry + TK x (entry - stop)) | PCT (entry x (1 + TK%)) | SWH (the last confirmed swing high +
                TK x ATR) | RNGH (the N-session high + TK x ATR) | EMA50 (EMA50 + TK x ATR); SWH / RNGH / EMA50 only
                when above the entry, all at the entry close
    H   hold    sessions counted from the entry session; X = OPEN sells at the next open (H = 5 from a T+1 entry is
                OPEN6), X = CLOSE sells at that session's close (PLAN)
    TR  trail   1 = after a COMPLETED close above entry x (1 + TA%), the stop moves to entry + both commissions and then
                trails TM x ATR under the highest close; it never moves down; EX > 0 holds a trailed trade up to EX
                sessions instead of H
    TS  time stop  TS > 0: at the close of the TS-th session held, if that close is not above entry x (1 + TSP%),
                sell at the next open
    XC  close exit NONE | EMA20 | EMA50 | SWL: from the session after the entry, a close below that line - XK x ATR
                sells at the next open (trend rides: exit when the trend breaks)
    N   lookback of STRNG / LMRNG / RNG / RNGH (sessions, the current one included)
Swings (tl_state's rule): a swing high is higher than the 3 bars before it and not lower than the 3 after it, known 3
sessions later (lows mirrored). ATR = ta.atr(14), EMA = ta.ema.
Order of events (TradingView's broker emulator on daily bars): orders are placed at a session's close and act from the
next session; the stop / target of a trade are placed at its entry session's close (the entry session itself has no
stop); a stop or target gapped through fills at the open; a stop and a target inside one bar: open -> the nearer
extreme -> the other extreme -> close; a stop-limit gapped above its limit fills at the limit if the bar trades back
to it. At a close in a trade the exits are decided in this order: the hold (H) -> the time stop (TS) -> the close exit
(XC); each sells at the next open (H with X = CLOSE sells at that close).
Net return = (exit - entry - c x (entry + exit)) / entry, c = commission per side (TradingView's percent commission).
"""
from dataclasses import dataclass, field, asdict

import numpy as np

VERSION = "playbook v1.1"
CODE_TAG = "BMPB2"
STATES = ("S01", "S02", "S03", "S06", "S07", "S08", "S09", "S12", "UNK", "INS")
EVENTS = ("BO_NEW", "BO_CONF", "BO_STALL", "FBO", "BD_NEW", "BD_CONF", "BD_STALL", "FBD", "NONE")
REGIMES = ("BB", "NB", "MX", "BR", "HS", "NA")
S05S = ("N", "OV", "EX")
ENTRY = ("OPEN", "DELAY", "STH", "STPD", "STLV", "LMLV", "LMTC", "LMEMA", "SWHI", "STRNG", "LMRNG", "SKIP")
STOPS = ("NONE", "ATR", "PCT", "TLOW", "LVL", "SWL", "RNG")
TARGETS = ("NONE", "R", "PCT", "SWH", "RNGH", "EMA50")
EXIT_AT = ("OPEN", "CLOSE")
FALLBACK = ("NONE", "OPEN")
INVALID = ("NONE", "TLOW", "LVL", "SWL", "EMA50")
XCLOSE = ("NONE", "EMA20", "EMA50", "SWL")
FIELDS = ("E", "O", "V", "L", "G", "F", "N", "IV", "IK", "S", "SK", "T", "TK", "H", "X", "TR", "TA", "TM", "EX", "XC",
          "XK", "TS", "TSP")
NPB = 10
PB_NAMES = tuple("P%d" % k for k in range(1, NPB + 1))
COMMISSION = 0.175          # percent per side (35 bp round trip, the project's flat cost)
SWING_K = 3
S05_T = {"ext20": 3.0, "ext50": 6.0, "ext10": 6.0, "extreme20": 4.5, "extreme50": 9.0}

# tl_state / tl_context codes -> playbook tokens
STATE_TOKEN = {"S01": "S01", "S02": "S02", "S03": "S03", "S06": "S06", "S07": "S07", "S08": "S08", "S09": "S09",
               "S12": "S12", "UNKNOWN": "UNK", "INSUFFICIENT_DATA": "INS"}
STATE_CODE_TOKEN = {1: "S01", 2: "S02", 3: "S03", 6: "S06", 7: "S07", 8: "S08", 9: "S09", 12: "S12", 0: "UNK", -1: "INS"}
EVENT_CODE_TOKEN = {0: "NONE", 1: "BO_NEW", 2: "BO_CONF", 3: "BO_STALL", 4: "FBO", 5: "BD_NEW", 6: "BD_CONF",
                    7: "BD_STALL", 8: "FBD"}
REGIME_CODE_TOKEN = {0: "BB", 1: "NB", 2: "MX", 3: "BR", 4: "HS", -1: "NA"}


@dataclass
class Playbook:
    name: str
    E: str = "OPEN"
    O: float = 0.0
    V: int = 1
    L: float = 0.3
    G: float = 0.0
    F: str = "NONE"
    N: int = 20
    IV: str = "NONE"
    IK: float = 0.0
    S: str = "NONE"
    SK: float = 0.0
    T: str = "NONE"
    TK: float = 0.0
    H: int = 5
    X: str = "OPEN"
    TR: int = 0
    TA: float = 3.0
    TM: float = 2.0
    EX: int = 0
    XC: str = "NONE"
    XK: float = 0.0
    TS: int = 0
    TSP: float = 0.0
    title: str = ""

    def check(self):
        bad = []
        for f, allowed in (("E", ENTRY), ("S", STOPS), ("T", TARGETS), ("X", EXIT_AT), ("F", FALLBACK),
                           ("IV", INVALID), ("XC", XCLOSE)):
            if getattr(self, f) not in allowed:
                bad.append("%s=%s" % (f, getattr(self, f)))
        if int(self.V) < 1 or int(self.H) < 1 or int(self.N) < 2:
            bad.append("V and H must be >= 1, N >= 2")
        if int(self.TS) < 0:
            bad.append("TS must be >= 0")
        if bad:
            raise ValueError("playbook %s: %s" % (self.name, ", ".join(bad)))
        return self


# The starting hypotheses (v1.1, from how each state and event is expected to behave): each playbook is an entry, an
# invalidation and the structural stop / target / exit that fit it. Every field is a setting.
DEFAULT_PLAYBOOKS = {
    "P1": Playbook("P1", "OPEN", 0.0, 1, 0.3, 0.0, "NONE", title="Open T+1 (baseline)"),
    "P2": Playbook("P2", "LMLV", 0.25, 5, 0.3, 0.0, "NONE", IV="LVL", IK=0.25, S="LVL", SK=0.25,
                   title="Breakout retest: limit at the breakout level, out below it"),
    "P3": Playbook("P3", "STLV", 0.10, 10, 0.3, 0.0, "NONE", S="TLOW", SK=0.25,
                   title="Failed breakout: reclaim the level, stop under T's low"),
    "P4": Playbook("P4", "STLV", 0.25, 5, 0.3, 0.0, "NONE", S="TLOW", SK=0.25,
                   title="Bear trap: reclaim the breakdown level, stop under T's low"),
    "P5": Playbook("P5", "STH", 0.10, 10, 0.3, 0.0, "NONE", IV="TLOW", IK=0.5, S="TLOW", SK=0.25,
                   title="Confirmation: above T's high, void below T's low"),
    "P6": Playbook("P6", "LMTC", 1.0, 3, 0.3, 0.0, "NONE", title="Pullback: limit at T's close - 1 ATR"),
    "P7": Playbook("P7", "SWHI", 0.10, 10, 0.3, 0.0, "NONE", IV="SWL", IK=0.0, S="SWL", SK=0.25,
                   title="Structure: buy the break of the last swing high, stop under the swing low"),
    "P8": Playbook("P8", "LMEMA", 0.0, 5, 0.3, 0.0, "NONE", S="SWL", SK=0.25, H=20, TR=1, TA=3.0, TM=2.0,
                   XC="EMA20", XK=0.25, title="Trend: buy the EMA20 pullback, ride until a close under EMA20"),
    "P9": Playbook("P9", "LMRNG", 0.25, 10, 0.3, 0.0, "NONE", N=20, S="RNG", SK=0.25, T="RNGH", TK=0.0, H=10,
                   title="Range: buy near the 20-session low, target the range high"),
    "P10": Playbook("P10", "SKIP", title="No long: bearish state or a breakdown"),
}
# 1 Nov 2026: S08 / S09 and breakdowns -> P1 (the open), not P10: in 2020-22 S08 picks made +4.2% (D) / +5.2% (ENS)
# per pick under OPEN6 vs +1.6% / +2.0% for all picks, so 'no long' was contradicted. P10 stays available, unmapped.
DEFAULT_MAP = ("S08,S09:*:*=P1;*:BD_NEW,BD_CONF,BD_STALL:*=P1;*:FBD:*=P4;*:FBO:*=P3;S01,S02,S03:BO_NEW,BO_CONF:*=P2;"
               "*:BO_STALL:*=P5;S01:*:*:OV,EX=P8;S01:*:*=P1;S02,S03,S06:*:*=P7;S07:*:*=P9;S12:*:*=P5;*:*:*=P1")


# ============================================================================ mapping and the config code
@dataclass
class Rule:
    states: tuple      # () = any
    events: tuple
    regimes: tuple
    s05: tuple
    pb: str
    text: str = ""


def parse_map(text):
    rules = []
    for raw in text.replace("\r", "").replace("\n", ";").split(";"):
        r = raw.replace(" ", "")
        if not r:
            continue
        if "=" not in r:
            raise ValueError("mapping rule without '=': %r" % raw)
        left, pb = r.split("=", 1)
        parts = left.split(":")
        while len(parts) < 4:
            parts.append("*")
        if len(parts) > 4:
            raise ValueError("mapping rule needs STATE:EVENT[:REGIME[:S05]]=Pn: %r" % raw)

        def lst(s, allowed):
            if s == "*" or s == "":
                return ()
            vals = tuple(x for x in s.split(",") if x)
            for v in vals:
                if v not in allowed:
                    raise ValueError("unknown token %r in rule %r" % (v, raw))
            return vals
        if pb not in PB_NAMES:
            raise ValueError("rule %r must end in =P1 .. =P%d" % (raw, NPB))
        rules.append(Rule(lst(parts[0], STATES), lst(parts[1], EVENTS), lst(parts[2], REGIMES), lst(parts[3], S05S),
                          pb, r))
    if not rules:
        raise ValueError("empty mapping")
    return rules


def match(rules, state, event, regime, s05="N"):
    for r in rules:
        if (not r.states or state in r.states) and (not r.events or event in r.events) and \
                (not r.regimes or regime in r.regimes) and (not r.s05 or s05 in r.s05):
            return r.pb
    return "P1"


def _num(x):
    s = ("%.6f" % float(x)).rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def config_code(playbooks=None, mapping=DEFAULT_MAP, comm=COMMISSION):
    pbs = playbooks or DEFAULT_PLAYBOOKS
    parts = [CODE_TAG, "C=" + _num(comm), "M=" + mapping.replace("\n", ";").replace(" ", "")]
    for k in PB_NAMES:
        p = pbs[k]
        vals = []
        for f in FIELDS:
            v = getattr(p, f)
            vals.append("%s:%s" % (f, v if isinstance(v, str) else _num(v)))
        parts.append("%s=%s" % (k, ",".join(vals)))
    return "|".join(parts)


def parse_code(code):
    """The config code printed by the Pine script (or config_code()) -> (playbooks, rules, comm, mapping)."""
    code = code.strip()
    parts = code.split("|")
    if parts and parts[0] == "BMPB1":
        raise ValueError("a playbook v1.0 code (BMPB1): its short form is relative to v1.0's defaults. Copy the code "
                         "again from the v1.1 script (BMPB2), or run it with playbook v1.0")
    if not parts or parts[0] != CODE_TAG:
        raise ValueError("not a %s config code" % CODE_TAG)
    comm, mapping, pbs = COMMISSION, DEFAULT_MAP, {k: Playbook(**{**asdict(v)}) for k, v in DEFAULT_PLAYBOOKS.items()}
    for p in parts[1:]:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        if k == "C":
            comm = float(v)
        elif k == "M":
            mapping = v
        elif k in pbs:
            d = asdict(pbs[k])
            for kv in v.split(","):
                if ":" not in kv:
                    continue
                f, val = kv.split(":", 1)
                if f not in FIELDS:
                    raise ValueError("unknown playbook field %s" % f)
                cur = d[f]
                d[f] = val if isinstance(cur, str) else (int(round(float(val))) if isinstance(cur, int) else float(val))
            pbs[k] = Playbook(**d).check()
    return pbs, parse_map(mapping), comm, mapping


# ============================================================================ TradingView's indicators
def tv_atr(h, l, c, n=14):
    """ta.atr(14) = ta.rma(ta.tr(true), 14): the first true range is high - low; seeded with the mean of 14."""
    m = len(c)
    tr = np.empty(m)
    tr[0] = h[0] - l[0]
    if m > 1:
        pc = c[:-1]
        tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - pc), np.abs(l[1:] - pc)))
    out = np.full(m, np.nan)
    if m >= n:
        a = tr[:n].mean()
        out[n - 1] = a
        for i in range(n, m):
            a = (a * (n - 1) + tr[i]) / n
            out[i] = a
    return out


def tv_ema(c, n=20):
    """ta.ema: alpha = 2 / (n + 1), seeded with the first value (Pine's reference implementation)."""
    a = 2.0 / (n + 1)
    out = np.empty(len(c))
    e = c[0]
    for i in range(len(c)):
        e = c[i] if i == 0 else a * c[i] + (1 - a) * e
        out[i] = e
    return out


def tv_swings(h, l, k=SWING_K):
    """The Pine script's swings: at bar i, bar i - k is a swing high when its high is above the k highs before it and
    not below the k after it (lows mirrored); swh[i] / swl[i] = the last swing known at bar i (NaN before the first)."""
    n = len(h)
    swh, swl = np.full(n, np.nan), np.full(n, np.nan)
    sh = sl = np.nan
    for i in range(n):
        if i >= 2 * k:
            p = i - k
            if h[p] > max(h[p - k:p]) and h[p] >= max(h[p + 1:i + 1]):
                sh = h[p]
            if l[p] < min(l[p - k:p]) and l[p] <= min(l[p + 1:i + 1]):
                sl = l[p]
        swh[i], swl[i] = sh, sl
    return swh, swl


# ============================================================================ fills (TradingView's broker emulator)
def high_first(o, h, l):
    """The emulator's intrabar path: if the high is closer to the open than the low, open -> high -> low -> close."""
    return (h - o) < (o - l)


def fill_stop_limit(o, h, l, trig, lim):
    """A buy stop-limit for this bar (lim None: a plain buy-stop). Returns the fill price or None."""
    if o >= trig:                       # triggered at the open
        if lim is None or o <= lim:
            return o
        return lim if l <= lim else None
    if h >= trig:
        return trig                     # crossed intrabar; trig <= lim
    return None


def fill_limit_buy(o, h, l, lim):
    if o <= lim:
        return o
    return lim if l <= lim else None


def exit_in_bar(o, h, l, stop, tgt):
    """(price, reason) when a protective stop / target order fills in this bar, else None."""
    has_s = stop is not None and np.isfinite(stop)
    has_t = tgt is not None and np.isfinite(tgt)
    if has_s and o <= stop:
        return o, "STOP_GAP"
    if has_t and o >= tgt:
        return o, "TARGET_GAP"
    hit_s = has_s and l <= stop
    hit_t = has_t and h >= tgt
    if hit_s and hit_t:
        return (tgt, "TARGET") if high_first(o, h, l) else (stop, "STOP")
    if hit_s:
        return stop, "STOP"
    if hit_t:
        return tgt, "TARGET"
    return None


def net_of(entry, exitp, comm_pct):
    c = comm_pct / 100.0
    return (exitp - entry - c * (entry + exitp)) / entry


# ============================================================================ one pick
@dataclass
class Bars:
    """One stock's own bars (as its TradingView chart has them) and the indicators the playbooks use."""
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    atr: np.ndarray = field(default=None)
    ema: np.ndarray = field(default=None)
    ema50: np.ndarray = field(default=None)
    swh: np.ndarray = field(default=None)
    swl: np.ndarray = field(default=None)

    def __post_init__(self):
        if self.atr is None:
            self.atr = tv_atr(self.h, self.l, self.c)
        if self.ema is None:
            self.ema = tv_ema(self.c)
        if self.ema50 is None:
            self.ema50 = tv_ema(self.c, 50)
        if self.swh is None or self.swl is None:
            self.swh, self.swl = tv_swings(self.h, self.l)

    @property
    def n(self):
        return len(self.c)

    def rng_low(self, a, n):
        return float(np.min(self.l[max(0, a - int(n) + 1):a + 1]))

    def rng_high(self, a, n):
        return float(np.max(self.h[max(0, a - int(n) + 1):a + 1]))


def s05_at(b, t):
    """N / OV / EX: tl_state's S05 thresholds on the chart's bars at close t."""
    a = b.atr[t]
    if not np.isfinite(a) or a <= 0:
        return "N"
    d20 = (b.c[t] - b.ema[t]) / a
    d50 = (b.c[t] - b.ema50[t]) / a
    m10 = (b.c[t] - b.c[t - 10]) / a if t >= 10 else np.nan
    if d20 >= S05_T["extreme20"] or d50 >= S05_T["extreme50"]:
        return "EX"
    if d20 >= S05_T["ext20"] or d50 >= S05_T["ext50"] or (np.isfinite(m10) and m10 >= S05_T["ext10"]):
        return "OV"
    return "N"


def baseline(b, t, comm):
    """Buy T+1's open; OPEN6 = sell T+6's open, PLAN5 = sell T+5's close."""
    out = {"b_entry": np.nan, "open6_gross": np.nan, "open6_net": np.nan, "plan5_gross": np.nan, "plan5_net": np.nan}
    if t + 1 < b.n:
        e = b.o[t + 1]
        out["b_entry"] = e
        if t + 5 < b.n:
            out["plan5_gross"] = b.c[t + 5] / e - 1.0
            out["plan5_net"] = net_of(e, b.c[t + 5], comm)
        if t + 6 < b.n:
            out["open6_gross"] = b.o[t + 6] / e - 1.0
            out["open6_net"] = net_of(e, b.o[t + 6], comm)
    return out


def inval_line(b, t, a, pb, lvl):
    """The invalidation line at close a (NaN = not active)."""
    IV = pb.IV
    if IV == "TLOW":
        return b.l[t] - pb.IK * b.atr[t]
    if IV == "LVL":
        return lvl - pb.IK * b.atr[t]
    if IV == "SWL":
        return b.swl[a] - pb.IK * b.atr[a]
    if IV == "EMA50":
        return b.ema50[a] - pb.IK * b.atr[a]
    return np.nan


def is_invalid(b, t, a, pb, lvl):
    x = inval_line(b, t, a, pb, lvl)
    return bool(np.isfinite(x) and b.c[a] < x)


def stop_target(b, t, e, px0, pb, lvl):
    """Protective stop and target placed at the entry session's close e."""
    stop = np.nan
    atr_t, atr_e = b.atr[t], b.atr[e]
    if pb.S == "ATR" and np.isfinite(atr_e):
        stop = px0 - pb.SK * atr_e
    elif pb.S == "PCT":
        stop = px0 * (1 - pb.SK / 100.0)
    elif pb.S == "TLOW" and np.isfinite(atr_t):
        stop = b.l[t] - pb.SK * atr_t
    elif pb.S == "LVL" and np.isfinite(lvl) and np.isfinite(atr_t):
        stop = lvl - pb.SK * atr_t
    elif pb.S == "SWL" and np.isfinite(b.swl[e]) and np.isfinite(atr_e):
        s = b.swl[e] - pb.SK * atr_e
        stop = s if s < b.c[e] else np.nan
    elif pb.S == "RNG" and np.isfinite(atr_e):
        stop = b.rng_low(e, pb.N) - pb.SK * atr_e
    tgt = np.nan
    if pb.T == "R" and np.isfinite(stop) and px0 > stop:
        tgt = px0 + pb.TK * (px0 - stop)
    elif pb.T == "PCT":
        tgt = px0 * (1 + pb.TK / 100.0)
    elif pb.T in ("SWH", "RNGH", "EMA50") and np.isfinite(atr_e):
        base = b.swh[e] if pb.T == "SWH" else (b.rng_high(e, pb.N) if pb.T == "RNGH" else b.ema50[e])
        x = base + pb.TK * atr_e
        tgt = x if np.isfinite(x) and x > px0 else np.nan
    return stop, tgt


def xc_line(b, j, pb):
    if pb.XC == "EMA20":
        base = b.ema[j]
    elif pb.XC == "EMA50":
        base = b.ema50[j]
    elif pb.XC == "SWL":
        base = b.swl[j]
    else:
        return np.nan
    return base - pb.XK * b.atr[j]


def simulate_pick(b, t, pb, lvl, comm):
    """The playbook's trade for a pick whose signal close is bar t. lvl: the event level (price) or NaN.
    Returns a dict (status FILLED / NO_FILL / NO_ORDER / NO_LEVEL / NO_ATR / INVALID / SKIP / OPEN_AT_END, entry / exit
    bars and prices, reason, net)."""
    r = {"status": "", "entry_i": None, "entry_px": np.nan, "exit_i": None, "exit_px": np.nan, "reason": "",
         "net": np.nan, "gross": np.nan, "trig": np.nan, "stop": np.nan, "target": np.nan, "armed": False}
    n = b.n
    E = pb.E
    if E == "SKIP":
        r["status"] = "SKIP"
        return r
    if is_invalid(b, t, t, pb, lvl):
        r["status"] = "INVALID"
        return r
    atr_t = b.atr[t]
    entry_i = entry_px = None
    fb_i = None                      # the bar whose open a fallback market order takes (F = OPEN)
    V = int(pb.V)
    last = t
    if E == "OPEN":
        last = t + 1
        if t + 1 < n:
            if pb.G > 0:
                px = fill_limit_buy(b.o[t + 1], b.h[t + 1], b.l[t + 1], b.c[t] * (1 + pb.G / 100.0))
                if px is not None:
                    entry_i, entry_px = t + 1, px
                elif is_invalid(b, t, t + 1, pb, lvl):
                    r["status"] = "INVALID"
                    return r
                else:
                    fb_i = t + 2
            else:
                entry_i, entry_px = t + 1, b.o[t + 1]
    elif E == "DELAY":
        last = t + V + 1
        for a in range(t + 1, min(t + V, n - 1) + 1):          # every evening that waits, the placing one included
            if is_invalid(b, t, a, pb, lvl):
                r["status"] = "INVALID"
                return r
        if t + V + 1 < n:
            entry_i, entry_px = t + V + 1, b.o[t + V + 1]
    elif E in ("STLV", "LMLV") and not np.isfinite(lvl):
        r["status"] = "NO_LEVEL"
        fb_i = t + 1
    elif not np.isfinite(atr_t):
        r["status"] = "NO_ATR"
        fb_i = t + 1
    else:
        last = min(t + V, n - 1)
        fixed = None
        if E == "STH":
            fixed = b.h[t] + pb.O * atr_t
        elif E in ("STLV", "LMLV"):
            fixed = lvl + pb.O * atr_t
        elif E == "LMTC":
            fixed = b.c[t] - pb.O * atr_t
        r["trig"] = fixed if fixed is not None else np.nan
        for a in range(t, min(t + V - 1, n - 1) + 1):     # evenings that place an order for bar a + 1
            i = a + 1
            if a > t and is_invalid(b, t, a, pb, lvl):
                r["status"] = "INVALID"
                return r
            order = None                                  # (trigger, limit): trigger None = a limit buy
            if E in ("STH", "STLV"):
                if not (fixed > b.c[a]):                  # already through: not placed (a = T) / cancelled
                    if a == t:
                        r["status"] = "NO_ORDER"
                    fb_i = a + 1
                    break
                order = (fixed, fixed + pb.L * atr_t if pb.L > 0 else None)
            elif E in ("STPD", "SWHI", "STRNG"):
                if np.isfinite(b.atr[a]):
                    base = b.h[a] if E == "STPD" else (b.swh[a] if E == "SWHI" else b.rng_high(a, pb.N))
                    trig = base + pb.O * b.atr[a]
                    if np.isfinite(trig) and trig > b.c[a]:       # else: no order this evening
                        order = (trig, trig + pb.L * b.atr[a] if pb.L > 0 else None)
            elif E in ("LMLV", "LMTC"):
                order = (None, fixed)
            elif E in ("LMEMA", "LMRNG"):
                if np.isfinite(b.atr[a]):
                    base = b.ema[a] if E == "LMEMA" else b.rng_low(a, pb.N)
                    order = (None, base + pb.O * b.atr[a])
            else:
                raise ValueError(E)
            if i > n - 1:
                break                                     # the order is still working when the data end
            if order is None:
                continue
            if order[0] is None:
                px = fill_limit_buy(b.o[i], b.h[i], b.l[i], order[1])
            else:
                px = fill_stop_limit(b.o[i], b.h[i], b.l[i], order[0], order[1])
            if px is not None:
                entry_i, entry_px = i, px
                break
        if entry_i is None and fb_i is None and t + V <= n - 1:
            if is_invalid(b, t, t + V, pb, lvl):          # the closing evening checks before it gives up
                r["status"] = "INVALID"
                return r
            fb_i = last + 1                               # the window closed without a fill
    if entry_i is None and pb.F == "OPEN" and fb_i is not None:
        if fb_i >= n:                                     # the fallback's open is not in the data yet
            r["status"] = "OPEN_AT_END"
            return r
        entry_i, entry_px = fb_i, b.o[fb_i]
        r["entry_how"] = "FALLBACK"
    if entry_i is None:
        if not r["status"]:
            r["status"] = "NO_FILL" if (fb_i is not None or (E in ("OPEN", "DELAY") and last < n)) else "OPEN_AT_END"
        return r
    r.setdefault("entry_how", "ORDER")
    r.update(status="FILLED", entry_i=int(entry_i), entry_px=float(entry_px))
    e = entry_i
    px0 = entry_px
    stop, tgt = stop_target(b, t, e, px0, pb, lvl)
    r["stop"], r["target"] = stop, tgt
    hi_c = px0
    armed = False
    hold = int(pb.H)
    max_hold = int(pb.EX) if (pb.TR and int(pb.EX) > hold) else hold
    cpct = comm / 100.0

    def close_decisions(j):
        nonlocal hi_c, armed, stop
        hi_c = max(hi_c, b.c[j])
        if pb.TR:
            if not armed and b.c[j] > px0 * (1 + pb.TA / 100.0):
                armed = True
            if armed and np.isfinite(b.atr[j]):
                lvl_t = max(px0 * (1 + 2 * cpct), hi_c - pb.TM * b.atr[j])
                stop = lvl_t if not np.isfinite(stop) else max(stop, lvl_t)

    close_decisions(e)
    j = e
    while True:
        held = j - e + 1                                   # sessions held including bar j
        limit_hold = max_hold if armed else hold
        why = None
        if held >= limit_hold:
            why = "TIME"
        elif int(pb.TS) > 0 and held == int(pb.TS) and not (b.c[j] > px0 * (1 + pb.TSP / 100.0)):
            why = "TSTOP"
        elif pb.XC != "NONE" and j > e:
            x = xc_line(b, j, pb)
            if np.isfinite(x) and b.c[j] < x:
                why = "XCLOSE"
        if why is not None:
            if why == "TIME" and pb.X == "CLOSE":
                r.update(exit_i=j, exit_px=float(b.c[j]), reason="TIME")
                break
            if j + 1 >= n:
                r["status"] = "OPEN_AT_END"
                return r
            k = j + 1
            ex = exit_in_bar(b.o[k], b.h[k], b.l[k], stop, tgt)
            if ex is not None and ex[1].endswith("_GAP"):
                reason = ex[1]
                if armed and reason.startswith("STOP"):
                    reason = "TRAIL" + reason[4:]
                r.update(exit_i=k, exit_px=float(ex[0]), reason=reason)
            else:
                r.update(exit_i=k, exit_px=float(b.o[k]), reason=why)
            break
        j += 1
        if j >= n:
            r["status"] = "OPEN_AT_END"
            return r
        ex = exit_in_bar(b.o[j], b.h[j], b.l[j], stop, tgt)
        if ex is not None:
            reason = ex[1]
            if armed and reason.startswith("STOP"):
                reason = "TRAIL" + reason[4:]
            r.update(exit_i=j, exit_px=float(ex[0]), reason=reason)
            break
        close_decisions(j)
    r["armed"] = armed
    r["gross"] = r["exit_px"] / px0 - 1.0
    r["net"] = net_of(px0, r["exit_px"], comm)
    return r
