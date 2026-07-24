---
name: system-review
description: Runs a periodic, evidence-based review of the hub and skills themselves and proposes a ranked refinement plan, building on prior reviews so nothing is re-derived. Deterministically extracts signals from session transcripts, fans out read-only analysis agents, grades findings against the north-star, and produces a decision-brief for sign-off. Use to review or tune the system, when the user asks to analyse how the setup is working, or on /system-review. Changes nothing without approval.
---

# System-review — review and tune the system itself

The "system" track: turn how the setup is actually working into a ranked, evidence-based refinement
plan. This exists because the review kept being run ad hoc from a blank chat (three times before this
skill existed). It is read-only and diagnostic until the user signs off; strategic and architectural
calls are the user's.

## Method

**1 · Read the record first.** `~/hub/design.md`, `~/hub/decisions.md`, `~/hub/north-star.md`, the
prior reviews in `~/hub/reviews/`, and the current skill set (`~/research-system/skills/*/SKILL.md`).
Build ON the last review — confirm or refute its open items with new evidence; never re-derive what
it already found. Read `~/hub/config.yml` for paths.

**2 · Extract signals deterministically (firewall: code computes, you interpret).** Run the bundled
`extract_signals.py` over the Claude Code transcripts (`~/.claude/projects/**/*.jsonl`). It writes,
to a scratch dir: per-category digests of the user's own messages, a friction reel (human corrections),
a meta reel (the user talking about the system), a usage-stats summary (skill-attribution tally,
model/token split, tool-call counts, context-exhaustion continuations, interrupts), all categorised by
work-type. Never hand-count what the script can count. **Correct for automation:** hook-fired sessions
(automated `security-review` commits, one machine turn each) inflate counts — exclude them from
"activity" and say so; flag any headline number that is an artifact.

**3 · Fan out read-only analysis agents (cheap/mid tier, never Opus for pure read).** One agent per
angle over the distilled digests (not the raw transcripts): e.g. non-research usage weight, loop
behaviour vs the prior baseline, the user's own words on the themes the user raised. Give each the
prior-review baseline so it reports what is NEW or CHANGED. Require verbatim quotes + session ids.

**4 · Synthesise and be the skeptic.** Rank pitfalls by leverage; separate what genuinely works
(keep it) from what to change. Grade every proposed change against the north-star goals AND non-goals
(no infra I can't maintain, don't over-engineer, no results I can't explain). Run the adversarial pass
as a SEPARATE step, not folded into synthesis: challenge each surviving item against the non-goals on
its own, so findings are graded blind rather than waved through in the same breath that generates them.
Own any overstatement from a prior pass.

**5 · Produce the decision brief** as `~/hub/reviews/<YYYY-MM-DD>-system-review.html` (date from the
system clock via `date`), to the HTML deliverable standard (`~/hub/knowledge/html-deliverable-standard.md`):
self-explanatory, minimalist-with-expand, professional grammar, theme-aware, sticky TOC. Each proposed
change carries a decision tag, a recommendation, and its trade-off. It changes nothing by itself.

**6 · Sign-off, then enact.** Present the forks; do NOT infer approval (a "continue" is not a yes). Use
a batched question for the strategic forks. Implement only what the user picks; show every edit; log
the decision via `decide`; commit locally per change (NO push — cloud is opt-in). Hold commits until
the user nods. Fold the review's own learnings via `reflect`.

## Guardrails
- **Read-only until sign-off.** Extraction and analysis never edit anything; never touch project data.
- **The conversation is never the record** — the brief + a `decide` entry are the durable output.
- **Skeptic, not relay** — surface the honest effect size, name what a critical reviewer would attack,
  and offer a real alternative before agreeing. The user decides; you support.
- **Don't over-build the review itself** — reuse the bundled script and existing agents; add machinery
  only when a mechanical step has genuinely repeated.

Bundled: `extract_signals.py` (deterministic transcript → digests + stats). See `~/hub/design.md`
(the system self-review; the firewall; north-star) and the prior briefs in `~/hub/reviews/`.
