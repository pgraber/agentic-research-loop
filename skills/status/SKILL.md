---
name: status
description: Shows where an analysis stands and what to do next — reads the project filesystem, infers the loop position, and prints it with a "you are here" marker plus the next step; also gives a portfolio view across all projects. Use when the user asks "where am I", "what's next", "status", or "portfolio".
model: sonnet
---

# Status — where am I, what's next

No stored state — infer everything from the filesystem, so it's always accurate.

## Single project
1. Detect the loop position from which artifacts exist:
   `docs/.record/question.md`? → scoped · `.record/brief.md`? → grounded · intake report? · `results/` populated? ·
   QC report? · tagged figure? · `notebooks/*.qmd`? → narrated.
2. Print the loop with a "▶ YOU ARE HERE" marker and note which lane (fast/full).
3. Name the **next command** (e.g. "results present, not QC'd → resume `research-loop` at the output-QC checkpoint").

## Portfolio (across projects)
Scan the project directories (`~/hub/config.yml` → `paths.workspace`) and summarise each project's
state and what needs the user ("scRNAseq at output-QC waiting on you; glioma needs Fig 4"). Include
a disk/space note if useful (regenerable `work/`/caches worth sweeping).

Read-only. Print a legible map, not raw data. See `~/hub/design.md` (discoverability; portfolio).
