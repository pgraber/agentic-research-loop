---
name: narrate
description: Produces the learning notebook and the clean report from one literate source, and verifies every reported number traces to a results file. Use when writing up an analysis, making a figure's narrative, or explaining what was done and why. The manuscript Methods is a downstream distillation of these.
---

# Narrate — explain it (to learn) and prove it (to share)

One literate source (.qmd / notebook), two renders — no drift, and the clean render is genuine
proof because both run the same code.

**Read the record first.** Before writing the narrative, read `.record/CONTEXT.md`, `docs/.record/brief.md`, and
`docs/.record/decisions.md` — the write-up must match the question and the decisions actually made, and use
the glossary's terms.

## Two renders (Quarto profiles / conditional content)
- **learning** — code echoed, "concept boxes" explaining new ideas (sourced from the papers
  screened in `literature`), the WHY of each step, inline QC + figures. For the user to *understand*.
- **report** — code folded/hidden, terse, styled, with a **provenance footer**: commit SHA,
  environment (container digest / lockfile), date. Shareable / lab-notebook / proof of analysis.

## Rules
- **Numbers must match** — verify every figure/statistic quoted in the prose equals the value in
  the `results/` file. No number may come from an AI chat computation — only from a script output.
- Explain new concepts pedagogically (the user is learning); keep the firewall — show and explain
  the deterministic code, never recompute in prose.
- Render locally; sync only the final self-contained HTML/PDF to the cloud-docs tier (config `paths.onedrive_docs`; avoid many-small-files).
- The user edits and owns the narrative. → `reflect`.

Manuscript Methods = distilled from `docs/.record/brief.md` + ADRs + this report. See `~/hub/design.md`
(learning layer; two renders; numbers-match check).
