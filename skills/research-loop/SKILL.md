---
name: research-loop
description: Routes a research task into the right project and runs the step-wise, QC'd analysis loop end to end. Use when starting or continuing a bioinformatics analysis, working on a project, or when the user wants to do an analysis or "run the loop". Enforces rigor with human checkpoints — not automation of judgment.
---

# Research loop — run the analysis rigorously

The L2 entry into doing an analysis. Route to the project, then run the loop. This is a
research-rigor helper: the human decides at every ★ checkpoint; you enforce the steps and push back.

**Read the record first.** Once the project is picked, read `.record/CONTEXT.md`, `docs/.record/brief.md`,
`docs/.record/decisions.md`, and `docs/adr/` before running any step — every step builds on logged decisions,
never silently re-derives or contradicts them.

## 1. Pick the project
- New question with new data/context → `new-project`
- Existing repo → `adopt-project` (if unscaffolded) or resume it
- Tiny question sharing an existing project's data → a fast-lane loop-run inside it

## 2. Run the loop (elastic — fast lane for tiny checks, full path for figures)
```
scope → literature → intake-qc ★ → design → build → output-qc ★ → bio-sense ★ → reviewing-analysis → narrate → reflect
```
Invoke the matching skill at each step. ★ = human checkpoint (get outputs in front of the user; they
decide) — logged as a dated, tagged section in `docs/checkpoints.html`. Fast lane: scope(one line) → build → output-qc(eyeball) → decide+commit.

## Rules
- **`docs/checkpoints.html` follows the HTML deliverable standard** (`~/hub/knowledge/html-deliverable-standard.md`):
  minimalist overview + expand-for-depth, self-explanatory (define Arm A/B and every label + abbreviation
  at first use), a Concepts & methods learning layer, professional grammar, self-contained + theme-aware.
- **Commit per approved checkpoint** via `decide` (record rides with the change).
- **Deterministic compute** — the analysis is code (scripts/containers); AI never in the compute path.
- **Never skip a ★ checkpoint** silently. If a checkpoint fails, loop back to design or build.
- **Flag engineering-driven parameter changes** at the Build handoff — a threshold/filter changed
  for memory or runtime (not science) is surfaced and `decide`-logged before any result is reported.
- **Scope-lock** — before diverging from a logged scope/plan decision, restate it and get explicit
  reconfirmation; never silently re-scope.
- **Park tooling tangents** — mid-analysis drift into tooling/naming/meta goes to `ideas.md`, then
  return to the work; protect the session's stated purpose.
- Read `~/hub/config.yml` for paths; `~/hub/design.md` for the full loop rationale.
