---
name: office-hours
description: Answers "what should I work on" when the user genuinely does not know. Weighs the current portfolio state against the north-star, spot-verifies the record against the artifacts it cites, names the one thing that moves a goal, and opens that track. NOT the default session opener where a SessionStart hook already injects portfolio state: when the user names the work, do that work instead of invoking this. Use on /office-hours, or when the user asks where to start or what matters most.
---

# Office Hours — answer "what should I work on", then start it

**Scope, narrowed 2026-08-12.** Where the setup injects portfolio state at session start (this one
does, through a `SessionStart` hook feeding from the cockpit generator), every stream's position, the
queue, the goals and the priority rule are already in context before the user types. The original job
of reporting where things stand is therefore done, and invoking this skill to repeat it wastes a turn
and reads as interrogation.

**When the user names the work, do the work.** Do not open this skill to confirm a choice already
made, and never ask a routing question whose answer is in the message that triggered it. The failure
mode is real and was observed twice in a single session: the skill fired, asked which track to open,
and the user ignored the question and stated the task directly.

What remains is the case an injected status block cannot serve: the user does not know where to
start, or wants the portfolio weighed rather than listed. That is a real need and this is where it is
met.

## On invocation (fast, one pass)
1. Use the injected state if the setup provides one. Do NOT re-read each repository or re-derive
   stream status. Read the north-star and the decisions log for the goals, non-goals and settled
   calls that a status block does not carry.
2. **Spot-verify one load-bearing record claim against the artifact it cites.** Does the file exist,
   and is it newer or older than the note claims? This is the highest-value step here and the one
   nothing else does. In practice it catches a "resume exactly here" pointer that later sessions have
   silently overtaken. Ignore hook-generated commits when judging how active something is.
3. Say, in a few lines: where things stand, the one thing that most moves a goal now, and anything
   drifting into a non-goal. Then open that track. One pass, no interrogation.

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
| **Scientific paper** — journal manuscript, a Results/Discussion section, abstract, figure caption, reviewer response | `manuscript` | the per-section loop IS the planning (read record → read figure → list issues → discuss → edit → check → merge to Word) |
| Other writing — article, essay, talk, poster | `writing-fragments` → `writing-shape` / `writing-beats` / `edit-article`; `narrate` for methods from an analysis | shape/beats decisions |
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
- **Scientific paper (`manuscript`):** the writing checks above, plus ones that fire mechanically —
  topic-sentence test (read only each paragraph's first sentence; the story must be there) · sentences
  under 30 words · paragraphs under 500 · Results carry interpretation of the data in hand but never
  against outside knowledge · numbers reported ICMJE-style (absolute value and spread before the
  standardized statistic, never a bare Cohen's d) · every number traced to a named results file and
  none from a superseded analysis · every cited supplementary item exists · venue conventions looked
  up, never assumed · the Word merge closes each section, field codes and comments intact.
  Full contract: `~/hub/knowledge/scientific-writing.md`.
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
