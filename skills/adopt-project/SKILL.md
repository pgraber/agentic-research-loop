---
name: adopt-project
description: Adopts an existing repo or folder into the system by scaffolding only the missing compendium structure — never touching existing code or data. Use when applying the system to an existing project, for example the isoform analysis, or when the user says "adopt" or "apply the system to this project".
---

# Adopt project — bring an existing repo into the system

Additive only. Add what's missing; touch no existing code, data, or results.

Compare against the canonical template `~/research-system/templates/project/` (the structure's
single source of truth). Add what's MISSING; never move existing files (that's a separate step).

## Steps
1. Inspect the repo — note what already exists (scripts, data, results, git).
2. **Add ONLY the missing pieces** from the template (copy individual files/dirs that are absent):
   `.record/CONTEXT.md`, `docs/checkpoints.html`, `docs/.record/{brief,decisions}.md`,
   `docs/{adr/,papers/,notebooks/}`, `env/`, `figures/`, `scripts/validate.{R,py,sh}`, `.gitignore`
   entries, and a project `CLAUDE.md`. Do not overwrite anything that exists.
3. If raw data is edited-in-place anywhere, flag it — propose a read-only `data/raw/` copy
   (chmod a-w + `chflags uchg`) + `PROVENANCE.md`. Do not move data without the `archivist`.
4. **Structure report** — list what you scaffolded (missing → added) AND what's MISPLACED vs the
   template. Do NOT move misplaced files yourself; offer to rearrange via `librarian`/`archivist`
   (dry-run → confirm → move; reversible via git), only on the user's say-so.
5. Register the project with the hub (portfolio).

## Guardrails
- Never modify, move, or delete existing files — additive only. Rearranging is a separate,
  confirmed, git-reversible op (librarian/archivist), never automatic.
- Never run analyses here — that's `research-loop`.
- Show the exact list of files you'll create and wait for confirmation.

## Successor-ready output (standing standard — do not wait to be asked)
Every doc that REMAINS after adoption (`README`, `CLAUDE.md`, `.record/CONTEXT.md`, `docs/.record/brief.md`,
`docs/.record/decisions.md`, `PROVENANCE.md`) must read as a clean, standalone research compendium for
someone who INHERITS it after the author leaves the institute and must reproduce it. So in those docs:
- No process / migration meta-language ("clean-copy adoption", "original left untouched",
  "ported/migrated from…", "yardstick", "adoption scope").
- No transient local paths that won't exist after archival (e.g. the source folder that later gets
  deleted). State provenance in stable terms: dataset, accession, thesis chapter/section.
- No internal skill tags (`[office-hours]`, `[adopt-project]`, …) and no style-policing notes.
- References to the thesis/manuscript cite the REAL chapter/section number and title (confirm
  against the thesis — do not guess or reuse a folder's aim-number).
- `.record/CONTEXT.md` is a clean glossary: definitions only.
Migration mechanics belong in the git commit message, not in the artifact. Before declaring done,
grep the docs for the above and fix.

See `~/hub/design.md` (migration = additive overlay, never big-bang).
