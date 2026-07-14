---
name: new-project
description: Seeds a new research project workspace from a question plus its data, using the research-compendium structure. Use when starting an analysis whose data and context are not an existing project. Creates the folder layout, project instructions, and git repo — seeded from the question, not a presumed paper.
---

# New project — seed a research workspace

Create a self-contained compendium for one question + its data context. Seed from the QUESTION
(what you know day one), not "Paper X" — manuscript identity is attached later, no restructure.

## Steps
1. **Copy the canonical template** — the single source of truth for structure — into the workspace:
   `cp -R ~/research-system/templates/project <paths.workspace>/<name>` (get `paths.workspace` from
   `~/hub/config.yml`; never hardcode). Do NOT re-describe the structure here — the template IS it.
2. **Fill the placeholders** — replace `<NAME>` in CLAUDE.md/README/brief/decisions/CONTEXT; write
   the question into `docs/.record/brief.md`; set `phase:` in `.record/CONTEXT.md`. Seed from the QUESTION, not "Paper X".
3. **Set up data** — copy the read-only working subset into `data/raw/` (chmod a-w, then `chflags uchg` — chmod alone does not stop `rm`) and record it in
   `data/raw/PROVENANCE.md` (source volume path + sha256). Huge raw stays on the volume, referenced.
4. `git init` (the template ships a `.gitignore`). Register the project with the hub (portfolio).

If a project-specific pipeline is needed, it lives in the (agnostic) `workflow/` subdir. One repo =
one shared data+environment context; pipelines REUSED across projects are separate repos. See
`~/hub/design.md` (granularity & emergence).
