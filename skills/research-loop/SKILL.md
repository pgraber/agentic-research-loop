---
name: research-loop
description: Routes a research task into the right project and runs the step-wise, QC'd analysis loop end to end, including the output-QC and bio-sense human checkpoints inline. Use when starting or continuing a bioinformatics analysis, working on a project, or when the user wants to do an analysis or "run the loop". Enforces rigor with human checkpoints — not automation of judgment.
---

# Research loop — run the analysis rigorously

The L2 entry into doing an analysis. Route to the project, then run the loop. This is a
research-rigor helper: the human decides at every ★ checkpoint; you enforce the steps and push back.
This conductor runs two checkpoints INLINE (output-QC and bio-sense); the other steps are their own
skills, invoked in turn.

**Read the record first — but lean, on resume.** Once the project is picked, read `.record/CONTEXT.md`,
`docs/.record/brief.md`, `docs/.record/decisions.md`, and `docs/adr/` before running any step. On a
plain resume, do NOT re-read everything heavily every time: read `docs/checkpoints.html`'s loop-status
strip + the last decision, state "you are here" in one pass, and go. Every step builds on logged
decisions, never silently re-derives or contradicts them.

## 1. Pick the project
- New question with new data/context → `new-project`
- Existing repo → `adopt-project` (if unscaffolded) or resume it
- Tiny question sharing an existing project's data → a fast-lane loop-run inside it

## 2. Run the loop (elastic — fast lane for tiny checks, full path for figures)
```
scope → literature → intake-qc ★ → design → build → [output-QC ★] → [bio-sense ★] → reviewing-analysis → narrate → reflect
```
Steps in `[brackets]` are run INLINE by this conductor (specs below); the rest invoke their matching
skill. ★ = human checkpoint (get outputs in front of the user; they decide) — logged as a dated,
tagged section in `docs/checkpoints.html`. Fast lane: scope(one line) → build → output-QC(eyeball) →
decide+commit.

### ▸ OUTPUT-QC checkpoint ★ — do the RESULTS make sense? (after build)
Catch garbage-out before it becomes a conclusion. Produce a legible report; the user looks and decides.
0. **Read `results/checks.tsv` FIRST and render it as the validation table at the top of the
   checkpoint section** (check, expected, observed, status, source), taken from the file rather than
   retyped. A `FAIL` fails the checkpoint outright. A `WARN` must be explained here. An empty or
   missing `checks.tsv` also fails it: the build did not validate anything, so no number below it is
   trustworthy. Contract: `~/hub/knowledge/validation.md`.
1. Run a metric script over `results/` (deterministic firewall: script computes, you interpret):
   distributions, marker genes, cluster/DE counts, effect sizes, n.
2. **Compare against the thresholds pre-registered in `design`** — never thresholds invented now.
   - **Fast lane (design was skipped):** there is no pre-registered baseline, so say that explicitly
     and eyeball-only. Do NOT invent a threshold now to pass against (that is the p-hacking this
     guards). If a number genuinely must be checked, have `scope` pre-register it first.
3. Add a dated, tagged ("Output QC") section to `docs/checkpoints.html` (create it, with a
   sticky-sidebar TOC + loop-status strip, if this is the project's first checkpoint): plots + numbers
   vs the pre-set thresholds, inlined and self-contained (toggleable via the plain/technical mode
   button), for the user to eyeball at a glance. Link only to raw results files, never to a separate
   polished QC write-up.
4. Any deviation from the pre-registered thresholds requires an ADR justifying it (anti-gaming). And
   flag engineering-driven changes: any parameter/filter/threshold changed during build for
   engineering reasons (memory, runtime) not science must be surfaced and `decide`-logged HERE before
   results are reported — a silent perf workaround (e.g. a gene-count cap to dodge an OOM) can
   masquerade as a biological result.
5. Log the outcome via `decide`. Pass → bio-sense checkpoint. Fail → loop back to `design` or `build`.

### ▸ BIO-SENSE checkpoint ★ — does it make BIOLOGICAL sense?
The scientific checkpoint, separate from numerical QC. A result can be statistically clean and still be
biological nonsense (or an artefact). Surface the comparison; the user makes the scientific call.
1. Compare the result against `docs/.record/brief.md` and the literature priors (Obsidian syntheses /
   `~/hub/knowledge/sources.md`).
2. Ask: does it agree with known biology? Where does it conflict? Is a surprising result a real
   finding or an artefact (batch effect, contamination, mislabel)?
3. Flag conflicts and plausible artefacts explicitly — do not smooth them over. Push back rather than
   agree: a wrong-but-plausible result passed here becomes a wrong paper.
4. Add a dated, tagged ("Bio-sense") section to `docs/checkpoints.html`, inlined and self-contained,
   then log the call via `decide`. Conflict/artefact → loop back to `design` or `build`. Genuine
   surprise the user accepts → proceed to `reviewing-analysis`.

## Rules
- **`docs/checkpoints.html` follows the HTML deliverable standard** (`~/hub/knowledge/html-deliverable-standard.md`):
  minimalist overview + expand-for-depth, self-explanatory (define Arm A/B and every label + abbreviation
  at first use), a Concepts & methods learning layer, professional grammar, self-contained + theme-aware.
- **Commit per approved checkpoint** via `decide` (record rides with the change).
- **Deterministic compute** — the analysis is code (scripts/containers); AI never in the compute path.
- **Every build script validates as it runs** — it initialises a log (`scripts/validate.{R,py,sh}`,
  or the same `checks.log`/`checks.tsv` format from any other language) and asserts each shape
  pre-registered at `scope`/`design` immediately after the step that produces it. A `FAIL` stops the
  run rather than warning. An analysis with no checks does not reach output-QC.
- **Never skip a ★ checkpoint** silently. If a checkpoint fails, loop back to design or build.
- **Flag engineering-driven parameter changes** at the Build handoff — a threshold/filter changed
  for memory or runtime (not science) is surfaced and `decide`-logged before any result is reported.
- **Scope-lock** — before diverging from a logged scope/plan decision, restate it and get explicit
  reconfirmation; never silently re-scope.
- **Don't infer approval** — a "continue" or a re-invocation of this skill is not a yes at a ★
  checkpoint; the call is the user's. Confirm before consequential/irreversible steps.
- **Proactive handoff** — on a long or multi-hour session, prompt a `handoff` / next-session write
  BEFORE the context compacts, not after it is lost. Turns handoff from a rescue into a habit.
- **Park tooling tangents** — mid-analysis drift into tooling/naming/meta goes to `ideas.md`, then
  return to the work; protect the session's stated purpose.
- Read `~/hub/config.yml` for paths; `~/hub/design.md` for the full loop rationale.
