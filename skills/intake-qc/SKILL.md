---
name: intake-qc
description: Checks whether input data is sound before analysis — file integrity, expected sample and read counts, metadata completeness, sample-ID consistency, failed lanes, and contamination. Use right after data lands in a project and before designing or running the analysis. A human checkpoint; distinct from the output-QC checkpoint (run inline in research-loop) which checks results.
---

# Intake-QC — is the DATA sound? (before analysis)

Garbage-in-garbage-out: catch a swapped sample or a failed lane at intake, not after weeks of
analysis. A human ★ checkpoint — you surface findings; the user decides.

## Checks (compute deterministically, then interpret)
- File integrity — not truncated; checksums match `data/raw/PROVENANCE.md`.
- Expected counts — number of samples, reads/cells per sample within expected range.
- Metadata completeness — required fields present; correct genome build.
- **Sample-ID consistency** — IDs match across files/sheets (the classic silent error).
- Anomalies — failed lanes, contamination flags, obvious outliers.

## Do
1. Run a metric script over `data/raw/` (deterministic); AI interprets the output.
2. Compare against expectations from `docs/.record/question.md`.
3. Add a dated, tagged ("Intake QC") section to `docs/checkpoints.html` (create it, with a
   sticky-sidebar TOC + loop-status strip, if this is the project's first checkpoint): sample table + QC
   plots (reads/cells per sample, distributions, the sample-ID consistency check) inlined so the section
   is self-contained (toggleable via the plain/technical mode button). Link only to raw source
   (`data/raw/PROVENANCE.md`, the raw metrics), never to a separate polished write-up.
4. Log the outcome via `decide` (e.g. "sample GRA15 excluded — 3% of expected reads").
5. Fail → fix/re-acquire data before proceeding. Never analyse data that failed intake.

Reads from `data/` only; never writes to raw. See `~/hub/design.md` (intake vs output QC).
