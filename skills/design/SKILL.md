---
name: design
description: Designs the analysis approach, screens and version-pins the tool or method (fetching current official docs first), and pre-registers QC thresholds and validation fixtures (unit-test targets, reference/published-data checks, biological controls) before any code is written. Use after scoping and grounding, before building the analysis. Writes an architecture decision record when there is a real trade-off.
---

# Design — decide the approach before building

Step where the method is chosen and committed to. Rigor here prevents wasted builds and defensible-
result problems later.

**Read the record first.** Before choosing a method, read `docs/.record/brief.md` (question + literature
grounding), `docs/.record/decisions.md`, and `docs/adr/` — don't re-pick a tool already pinned or reopen a
settled trade-off without saying why.

## Do
**0 · Check reality first — before designing off literature or assumptions.** Grep/inspect the
user's OWN prior implementation of this analysis (thesis code, previous repos), and confirm the
project record's claims (`.record/brief.md`, `.record/CONTEXT.md`, memory) match the code/data they cite — the
cited file/path exists and says what the record says. Stale-record or literature-only design
caused the two biggest rework episodes on record. THEN:

1. **Choose the method/tool** for the question and data. Avoid offering many options — pick a
   sensible default with a clear reason.
2. **Screen the tool** — invoke `checking-current-docs` to fetch current official docs and pin the
   version. Never write syntax from training-data memory.
3. **Pre-register QC thresholds** now (FDR, min genes/cell, fold-change, etc.), before results
   exist. These are what the output-QC checkpoint (run inline in `research-loop`) checks against.
4. **Pre-register the validation fixtures + tolerances** now, same anti-gaming logic — decide the
   yardstick BEFORE seeing the result. Testing is three tiers; name what applies:
   - **Unit** — the deterministic pure functions this analysis introduces (transforms, metrics,
     resampling). These get `/tdd` red-green during `build`; list them here so they aren't skipped.
   - **Reference / published-data** — a committed reference fixture + tolerance the result must
     reproduce (e.g. a published label set, a prior table, a long-vs-short concordance). Acceptance
     test, not unit — record the source, the metric, and the pass/fail tolerance.
   - **Biological controls** — housekeeping stability, expected markers; these stay the human
     output-QC / bio-sense checkpoints (run inline in `research-loop`), not automated. Note which controls apply.
   (Generic SDD skills like `to-prd`/`to-issues` are NOT the spec here — `brief.md` + ADRs are.)
5. **ADR if warranted** — for a hard-to-reverse choice or a real trade-off, write an ADR in
   `docs/adr/` (per the project's convention). Small calls just get a `decide` log line.
6. **HUMAN CHECKPOINT — present the plan VISUALLY and wait.** Add a dated, tagged ("Design") section
   to `docs/checkpoints.html` (create it, with a sticky-sidebar TOC + loop-status strip, if this is the
   project's first checkpoint): the question → method → steps → inputs/outputs → pre-registered
   thresholds + validation fixtures, inlined so the section is self-contained (code/tables toggleable via
   the plain/technical mode button, not a link to a separate write-up) — link only to raw source (brief,
   scripts, cited docs), never to another polished document. They approve or adjust BEFORE any code is
   written — the cheapest place to catch a wrong approach. → `build` only after approval.

## Output
`docs/.record/brief.md` gains the chosen method + rationale + cited docs; QC thresholds AND validation
fixtures (unit targets, reference fixture + tolerance, biological controls) recorded. This later
composes into the manuscript Methods.

The build output must be deterministic code in a container (Docker/Singularity), not conda/pixi.
Pin the image by `@sha256` digest (not a mutable `:tag`) and record the digest — it is verified at
the repro check.
See `~/hub/design.md` (design step; firewall; environment).
