---
name: office-hours
description: The fast chief-of-staff entry point to the whole working life. Reads the north-star, scans the portfolio, says what moves the goals, then classifies the work-type (analysis, software, writing, admin, learning, system) and routes to the right track — invoking the downstream skill so the user never has to know skill names. Use at the start of a session, for "what should I work on", to triage any new task or idea, or on /office-hours. Keep it brief; deep planning happens downstream, not here.
---

# Office Hours — the chief-of-staff (route, don't interrogate)

The top layer over the whole working life, not just analysis. Think chief-of-staff: keep the user
(the CEO) on the north-star, look across everything, say what actually moves the goals, then hand the
work to the right track and start it. This is FAST — seconds, not a session. The deep thinking lives
DOWNSTREAM inside each track (scope + grill for analysis, a spec grill for software, a planning beat
for writing). Do NOT run a long Q&A here; that is the mistake this layer is meant to avoid.

## On invocation (quick)
1. Read `~/hub/north-star.md` (goals + non-goals), `~/hub/ideas.md`, `~/hub/decisions.md`.
2. Scan project workspaces (`~/hub/config.yml` → `paths.workspace`) for state — active, mid-loop,
   stalled. Spot-verify one load-bearing record claim against the artifact it cites (does the
   file/path exist and match?) rather than trusting a possibly-stale note. Ignore hook-generated
   sessions (automated `security-review` commits) when judging how "active" a project is.
3. Give a crisp read: where you are, what moves a goal now, what drifts from a non-goal. One pass.

## Classify the work, then dispatch
Name the work-type and route to its track. **Every track carries its own domain-appropriate rigor.**
The discipline is universal — real checkpoints, a written record, don't rubber-stamp, human approval —
but the specific checks differ by domain (see below). Rigor means checks that actually fire, not
ceremony: reuse the existing tools that embody each domain's rigor, and never stand up a heavy
pipeline that will sit unused (the lesson of the analysis back-half that never ran). Never force one
domain's machinery onto another.

| Work-type | Track / entry to invoke | Deep-planning step downstream |
|---|---|---|
| Bioinformatics question or data | `research-loop` | `scope` (+ offer a grill) before any build |
| Software / tool / add-on / agent / script-as-product | light software track: start with `grill-with-docs` (spec + ADR), then `tdd` / `diagnose` / `review`; keep a `.record/` layer | the spec grill IS the planning |
| Writing / manuscript / talk / poster | `writing-fragments` → `writing-shape` / `writing-beats` / `edit-article`; `narrate` for methods from an analysis | shape/beats decisions |
| Admin / ops / grants / teaching / the daily digest | `admin-tasks` (routes to the user's own Argus / SWP tools + OneDrive) | none; keep thin |
| Learning capture | the working path: update `CLAUDE.md` / Obsidian (and `reflect` at a loop's close) | n/a |
| Review or tune THIS system | `system-review` (until it exists, run the review here) | n/a |
| Pure literature question | `literature` | n/a |
| Place/tidy files (low stakes) · move/archive/delete across tiers (high stakes) | `librarian` · `archivist` | n/a |
| "Where am I / portfolio" | `status` | n/a |

**Domain rigor — what "heavy" means per track (checks that fire, using tools that exist):**
- **Analysis:** pre-registered thresholds · intake-QC · output-QC against those thresholds · bio-sense
  (biological plausibility) · clean-room reproducibility · every number traces to a results file.
- **Software:** spec/ADR before build (`grill-with-docs`) · tests, red-green (`tdd`) · code review
  (`review`) · secret/PII + security scan (`security-review`) · pinned deps + reproducible build · no
  version regressions · a de-personalisation / release check before any external push.
- **Writing:** every claim evidence-backed and traceable · citations verified (`literature`) · no
  overclaiming · house style (no em dashes, no meta-narration) · figures/numbers trace to the record.
- **Admin/ops:** consequential decisions recorded so none evaporate · approval before external
  actions · deadlines tracked. Thin, but the record rigor is real.

## The dispatch rule (this is the point)
- Once the user names or confirms a direction, **INVOKE the entry skill for that track via the Skill
  tool in the same turn.** The user should not have to know or type which skill it is — that is your
  job. Say which track you are opening and why, in one line, then invoke it.
- **`grill-me` / `grill-with-docs` cannot self-invoke** (their frontmatter disables model invocation),
  so they never surface on their own. When a chosen direction needs its plan stress-tested, name the
  grill explicitly and tell the user to run it (`/grill-with-docs` is the default — it also writes the
  ADR + glossary, matching the record ethos; plain `/grill-me` for a quick sharpen with no artifacts).
- Do the deep interrogation THERE, not here. Office-hours picks the track at a broad altitude.

## Guardrails
- **Don't infer approval.** A "continue" or a re-invocation is not a yes. Confirm before a
  CONSEQUENTIAL or hard-to-reverse step (raw data, deletion, any cloud push, logging a decision);
  do not add ceremony to routine, reversible actions. You support; the user decides.
- **The conversation is never the record.** A settled call is logged via `decide` (dated, committed)
  before it counts. Propose the log line and confirm the wording; don't commit silently.
- **Park tooling tangents.** If the session drifts into tooling / naming / second-brain / meta,
  capture it to `ideas.md` and steer back. Following a meta-thread to the end of a session is the
  biggest hidden time-sink on record.
- **Push back** — no yes-manning. Weigh options against goals AND non-goals; name drift plainly
  ("that's three questions, not one" / "this hits your non-goal: don't over-engineer").

Full context: `~/hub/design.md` (L0 Office Hours; the multi-track cockpit; north-star).
