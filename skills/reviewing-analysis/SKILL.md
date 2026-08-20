---
name: reviewing-analysis
description: Reviews an analysis for correctness and reproducibility before a result is finalized — runs code review, verification, tests, and a clean-room reproducibility check in the pinned container. Use before tagging a figure or finalizing a result. Distinct from the generic pull-request review skill.
---

# Reviewing analysis — correctness + reproducibility check

The last check before a result becomes final. Combines existing review tools with the science-
specific reproducibility check.

## Do
1. **Code review** — run `/code-review` on the analysis changes as an INDEPENDENT pass: it reviews
   the diff cold, blind to the reasoning that produced it, rather than the build agent signing off on
   its own work. Address correctness findings.
2. **Validation record** — `results/checks.tsv` must exist, contain no `FAIL`, and cover every
   script in the run (each script's `step` present). Spot-check three checks against their stated
   sources: an expected value that turns out to be derived from the same code that produced the
   observed value is not a check, and the analysis goes back to `build`. Any `WARN` must have been
   explained at output-QC. Contract: `~/hub/knowledge/validation.md`.
3. **Verify + tests** — run `/verify`; ensure unit/edge tests pass (`tdd`). Per the user's
   CLAUDE.md, a result isn't done if tests are missing or failing.
4. **Reproducibility check** — clean-room re-run *from scratch in the pinned container*
   (`nextflow run -profile singularity`, or `targets::tar_make()`, from a clean state) → same
   output. Verify the container `@sha256` digest matches the one
   `design` pinned (a moved `:tag` is not a clean re-run). This is the ultimate science QC. Emit the **architecture visual** from this run —
   `nextflow -with-dag -with-report` or `targets::tar_visnetwork()` — as the pipeline overview.
5. Only when all pass: **tag the figure/result** (`git tag`) so the manuscript can cite an exact
   SHA. Log via `decide`, and add ONE status line to `docs/checkpoints.html` ("✓ reviewed &
   reproducible, commit `<sha>`") — a fact, not a log entry. No separate code-review file or
   history of every review pass: ad hoc `/code-review`/`/review` during `build` is git's job (the
   commit is already the trail); this is the only persistent record this step needs.

Fail → back to `build`. → `narrate`. See `~/hub/design.md` (review; reproducibility; git discipline).
