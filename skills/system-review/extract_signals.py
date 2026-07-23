#!/usr/bin/env python3
"""Deterministically extract review signals from Claude Code session transcripts.

The firewall step of `system-review`: code computes the signals, the agents interpret them.
Reads ~/.claude/projects/**/*.jsonl (or a given root) and writes distilled digests + stats to
an output dir, so a review never hand-counts what a script can count.

Usage:  python3 extract_signals.py OUTDIR [PROJECTS_ROOT]
        OUTDIR         where to write digests (e.g. the session scratchpad)
        PROJECTS_ROOT  default ~/.claude/projects

Outputs in OUTDIR:
    00_SUMMARY.json      counts, skill-attribution tally, model/token split, tool tally,
                         context-exhaustion + interrupt counts, per-category output tokens
    01_FRICTION_REEL.txt every human message that looks like a correction/frustration, chronological
    02_META_REEL.txt     every human message that talks about the system itself
    digests/<cat>.txt    per-category: per-session first-intent, skills run, friction, all human msgs

Stdlib only. Categorises by project-dir; flags hook-fired automated sessions so they can be
excluded from "activity" (they inflate counts). No hardcoded project names.
"""
import json, glob, os, re, sys, datetime
from collections import Counter, defaultdict

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ROOT = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.claude/projects")
os.makedirs(os.path.join(OUT, "digests"), exist_ok=True)

FRICTION = re.compile(r"""(?ix)\b(no,|not\ what|that'?s\ not|isn'?t\ what|don'?t|didn'?t|shouldn'?t|
  wrong|mistake|actually|instead|revert|undo|stop|wait|why\ did\ you|you\ should|you\ didn'?t|
  i\ said|i\ asked|i\ told|redo|try\ again|start\ over|as\ i\ said|too\ much|too\ little|too\ many|
  over-?engineer|overkill|simplif|frustrat|annoying|confus|useless|didn'?t\ work|not\ working|
  doesn'?t\ work|broke|broken|skipped|you\ skipped|missed|forgot|again|still|come\ on)\b""")
META = re.compile(r"(?ix)\b(skill|office\ hour|research\ loop|research-loop|the\ loop|checkpoint|"
                  r"decide|reflect|the\ hub|grill|scope|design|narrate|bio-sense|output-qc|intake-qc|"
                  r"literature|new-project|adopt|status|librarian|archivist|workflow|track|dispatch)\b")
INTERRUPT = re.compile(r"\[Request interrupted by user\]")
CONT = re.compile(r"ran out of context|continued from a previous conversation", re.I)
# automated hook template (adjust the phrase if the hook prompt changes)
HOOK = re.compile(r"Review this change for security vulnerabilities", re.I)

def clean(s):
    if not isinstance(s, str): return ""
    for pat in (r"<local-command-[^>]*>.*?</local-command-[^>]*>", r"<command-[^>]*>.*?</command-[^>]*>",
                r"<system-reminder>.*?</system-reminder>"):
        s = re.sub(pat, " ", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def text_of(content):
    if isinstance(content, str): return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
    return ""

def is_tool_result(content):
    return isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content)

def category(proj):
    p = proj.lower()
    if "subagents" in p: return "subagent"
    if p.startswith("wf_"): return "workflow"
    return proj  # the cwd-encoded project dir; agents group semantically

files = glob.glob(os.path.join(ROOT, "**", "*.jsonl"), recursive=True)
sessions = []
skill_tally, tool_tally = Counter(), Counter()
model_tok = defaultdict(lambda: [0, 0, 0])   # msgs, output, cache_read
cat_out, cat_exh, cat_intr, cat_auto = Counter(), Counter(), Counter(), Counter()

for f in files:
    proj = os.path.basename(os.path.dirname(f)); cat = category(proj)
    try:
        lines = open(f, encoding="utf-8").readlines()
    except OSError:
        continue
    m = {"file": os.path.basename(f)[:12], "proj": proj, "cat": cat, "date": "",
         "nu": 0, "skills": set(), "first": "", "human": [], "friction": [], "meta": [], "auto": False}
    m["date"] = datetime.date.fromtimestamp(os.stat(f).st_mtime).isoformat()
    for ln in lines:
        try: o = json.loads(ln)
        except Exception: continue
        sk = o.get("attributionSkill")
        if sk: m["skills"].add(sk); skill_tally[sk] += 1
        msg = o.get("message", {}) if isinstance(o.get("message"), dict) else {}
        content, role = msg.get("content"), msg.get("role")
        if role == "user":
            if is_tool_result(content): continue
            raw = content if isinstance(content, str) else text_of(content)
            if not m["first"] and HOOK.search(raw or ""): m["auto"] = True
            if INTERRUPT.search(raw or ""): cat_intr[cat] += 1
            if CONT.search(raw or ""): cat_exh[cat] += 1
            t = clean(raw)
            if not t: continue
            m["nu"] += 1
            if not m["first"]: m["first"] = t[:600]
            snip = t[:1200]; m["human"].append(snip)
            if FRICTION.search(t): m["friction"].append(snip[:600])
            if META.search(t): m["meta"].append(snip[:600])
        elif role == "assistant":
            model = msg.get("model", "?"); u = msg.get("usage") or {}
            d = model_tok[model]; d[0] += 1; d[1] += u.get("output_tokens", 0); d[2] += u.get("cache_read_input_tokens", 0)
            cat_out[cat] += u.get("output_tokens", 0)
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        tool_tally[c.get("name", "?")] += 1
                        if c.get("name") == "Skill":
                            s2 = (c.get("input") or {}).get("skill")
                            if s2: m["skills"].add(s2); skill_tally[s2] += 1
    m["skills"] = sorted(m["skills"])
    if m["auto"]: cat_auto[cat] += 1
    sessions.append(m)

json.dump({
    "n_sessions": len(sessions),
    "automated_sessions_by_cat": dict(cat_auto),
    "skill_attribution_tally": skill_tally.most_common(),
    "tool_tally": tool_tally.most_common(40),
    "model_tokens": {k: {"msgs": v[0], "output": v[1], "cache_read": v[2]} for k, v in model_tok.items()},
    "output_tokens_by_cat": cat_out.most_common(),
    "context_exhaustion_by_cat": dict(cat_exh),
    "interrupts_by_cat": dict(cat_intr),
    "note": "Exclude automated_sessions (hook-fired) from activity judgements; they inflate counts.",
}, open(os.path.join(OUT, "00_SUMMARY.json"), "w"), indent=2)

def reel(field, path, header):
    n = 0
    with open(path, "w") as fh:
        for s in sorted(sessions, key=lambda x: x["date"]):
            if not s[field] or s["auto"]: continue
            fh.write(f"\n[{s['date']} · {s['cat'][:45]}] skills={s['skills']}\n")
            for msg in s[field]:
                fh.write(f"   • {msg}\n"); n += 1
        fh.write(f"\n\nTOTAL {header}: {n}\n")

reel("friction", os.path.join(OUT, "01_FRICTION_REEL.txt"), "friction markers")
reel("meta", os.path.join(OUT, "02_META_REEL.txt"), "meta markers")

by_cat = defaultdict(list)
for s in sessions: by_cat[s["cat"]].append(s)
for cat, ss in by_cat.items():
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", cat)[:60]
    with open(os.path.join(OUT, "digests", f"{safe}.txt"), "w") as fh:
        for s in sorted(ss, key=lambda x: x["date"]):
            if not s["human"]: continue
            tag = " [AUTOMATED HOOK]" if s["auto"] else ""
            fh.write(f"\n{'='*80}\n### {s['date']} | {s['file']}{tag} | users={s['nu']} | skills={s['skills']}\n")
            fh.write(f"FIRST: {s['first']}\n")
            for msg in s["human"]:
                fh.write(f"  • {msg}\n")

print(f"wrote signals for {len(sessions)} sessions to {OUT}")
print(f"  automated (hook) sessions: {sum(cat_auto.values())}")
print(f"  skills attributed: {len(skill_tally)}; tools seen: {len(tool_tally)}")
