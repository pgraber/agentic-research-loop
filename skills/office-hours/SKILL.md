---
name: office-hours
description: Strategic Q&A / planning session — the entry point to the research system. Reads the north-star and scans projects, then helps decide what to work on, where a project can go, and whether a new idea fits. Use at the start of a session, when the user asks "what should I work on", wants to plan or think strategically, floats a new idea or project, or types /office-hours.
---

# Office Hours — strategic entry point

The "sit down and think together" session. This is NOT automation and NOT doing the analysis —
it's deciding *what* to do, rigorously, aligned to what you actually want. Human stays in
charge; you push back.

## On invocation
1. Read `~/hub/north-star.md` (goals + non-goals), `~/hub/ideas.md`, `~/hub/decisions.md`.
2. Scan project workspaces (see `~/hub/config.yml` → `paths.workspace`) for state — what's active,
   what's mid-loop, what's stalled. Spot-verify a load-bearing record claim against the artifact it
   cites (does the file/path exist and match?) rather than trusting a possibly-stale note.
3. Q&A with the user: what should I work on? where can this project go? does this idea fit?

## How to help (rigor at the strategic altitude)
- **Align to the north-star.** Weigh options against goals AND non-goals. Say plainly when
  something drifts ("this hits your non-goal: don't over-engineer" / "this doesn't move any goal").
- **Push back** — no yes-manning. Challenge scope creep ("that's three questions, not one").
- **Route, don't do.** Once a direction is chosen: hand off to `research-loop` for an analysis,
  or note admin work as admin (separate track). Don't start analysis here.
- **Escalate to `grill-me`** when a chosen direction needs its plan stress-tested branch-by-branch —
  office-hours picks the direction at a broad altitude; grill-me hardens one plan. Don't do that
  relentless interrogation here.
- **Park vs decide.** New half-thoughts → `ideas.md`. Settled calls → log via `decide` skill
  (dated, committed) so they don't evaporate.

## Guardrails
- The conversation is never the record — anything decided gets written (`decide`) before it counts.
- You support; the user decides. Keep them at every checkpoint.
- **Park tooling tangents.** If the session drifts from the chosen work into tooling / naming /
  second-brain / meta, capture it to `ideas.md` and steer back — don't follow a meta-thread to the
  end of a session (it is the biggest hidden time-sink on record).

Full context: `~/hub/design.md` (L0 Office Hours; the hub; north-star).
