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
- **Build every HTML deliverable to the standard** in `~/hub/knowledge/html-deliverable-standard.md`:
  minimalist overview by default with expand-for-depth (hover a term for a one-line meaning, open a
  "＋ Learn" unit for the concept/algorithm/tool with a worked example and its origin/etymology + memory
  aid, "⟨/⟩ Show code" to verify); self-explanatory standing alone (define Arm A/B and every internal
  label, spell out abbreviations at first use); neutral standard definitions; professional academic
  grammar (tables/bullets welcome, no em dashes); clean code/math typesetting; a workflow overview
  where it helps; self-contained, theme-aware, sticky TOC; single-source glossary from `CONTEXT.md`.
- **Numbers must match** — as a SEPARATE trace-check after the prose is drafted, not folded into
  writing it: go statistic by statistic and confirm every figure/number quoted equals the value in
  the `results/` file, reading the value fresh from the file rather than trusting what you just wrote.
  No number may come from an AI chat computation — only from a script output.
- Explain new concepts pedagogically (the user is learning); keep the firewall — show and explain
  the deterministic code, never recompute in prose.
- Render locally; sync only the final self-contained HTML/PDF to the cloud-docs tier (config `paths.onedrive_docs`; avoid many-small-files).
- The user edits and owns the narrative. → `reflect`.

Manuscript Methods = distilled from `docs/.record/brief.md` + ADRs + this report. See `~/hub/design.md`
(learning layer; two renders; numbers-match check).
