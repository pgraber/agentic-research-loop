---
name: output-qc
description: Checks whether analysis results make sense against the thresholds set at design time — distributions, marker genes, effect sizes, counts, and sample sizes. Use after a script produces results and before interpreting them. A human checkpoint; distinct from intake-qc which checks inputs.
---

# Output-QC — do the RESULTS make sense? (after build)

Catch garbage-out before it becomes a conclusion. A human ★ checkpoint: you produce a legible report;
the user looks and decides.

## Do
1. Run a metric script over `results/` (deterministic): distributions, marker genes, cluster/DE
   counts, effect sizes, n.
2. **Compare against the thresholds pre-registered in `design`** — not thresholds invented now.
   - **Fast lane (design was skipped):** there is no pre-registered baseline, so say that
     explicitly and eyeball-only — do NOT invent a threshold now to pass against (that is the
     p-hacking this guards). If a number genuinely must be checked, have `scope` pre-register it first.
3. Add a dated, tagged ("Output QC") section to `docs/checkpoints.html` (create it, with a
   sticky-sidebar TOC + loop-status strip, if this is the project's first checkpoint) — plots + numbers
   vs the pre-set thresholds inlined so the section is self-contained (toggleable via the plain/technical
   mode button), for the user to eyeball at a glance. Link only to the raw results files, never to a
   separate polished QC write-up.
4. Any deviation from the pre-registered thresholds requires an ADR justifying it (guards against
   post-hoc threshold gaming).
   - **Flag engineering-driven changes:** any parameter/filter/threshold changed during build for
     engineering reasons (memory, runtime) not science must be surfaced and `decide`-logged HERE
     before results are reported — a silent perf workaround (e.g. a gene-count cap to dodge an OOM)
     can masquerade as a biological result.
5. Log the outcome via `decide`. Pass → `bio-sense`. Fail → loop back to `design` or `build`.

Reads `results/`; writes only a QC report (never edits results in place). This is a numbers-sanity
check — biological plausibility is the separate `bio-sense` checkpoint. See `~/hub/design.md`.
