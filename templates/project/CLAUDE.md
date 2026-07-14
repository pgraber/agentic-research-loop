# Project: <NAME>

A research project in the research system. This is a RESEARCH-RIGOR workflow — follow the loop,
don't jump to code. System spec: `~/hub/design.md` · skills map: `~/hub/skills.html` ·
paths: `~/hub/config.yml` (never hardcode paths — read them from there).

## The loop (run `/research-loop`; it drives these — ★ = pause for you)
```
scope → literature → intake-qc ★ → design ★ → build → output-qc ★ → bio-sense ★ → reviewing-analysis → narrate ★ → reflect
```
★ = human checkpoint: approve a plan (scope, design) or review an output (QC, bio-sense). Every
checkpoint is a dated, tagged section in one running `docs/checkpoints.html` — visual + drillable,
never a new file per decision. Fast lane for a tiny check: scope → build → output-qc → `/decide`.

## Rules (non-negotiable)
- **Raw data is immutable.** `data/` is read-only (`chmod -R a-w` **+ `chflags uchg`** + `PROVENANCE.md`; chmod alone does not
  stop `rm`, and on SMB/network volumes read-only bits may not stick — treat volume immutability as
  enforced by the institute mount). Scripts READ
  `data/`, WRITE only `results/`. A step that "modifies" data writes a new file — never edit raw.
- **Reproducible compute.** Run in a container (Docker local / Singularity on HPC), digest-pinned;
  recipe + lockfile in `env/`. The AI is never in the compute path.
- **Pre-register QC thresholds** at `design`, before results exist. Deviations require an ADR.
- **Commit per approved checkpoint** (`/decide`) — the record rides with the code; tag figures.
- **Fetch current official docs** before writing tool syntax (`/checking-current-docs`).
- **Numbers in prose must trace to a results file** — never an AI chat computation.

## Structure
`data/` (raw, read-only) · `results/` (gitignored) · `figures/` · `scripts/` · `env/` (container) ·
`workflow/` (optional, project-specific pipeline — any manager) ·
`docs/checkpoints.html` (every human checkpoint, TOC'd, one file) ·
`docs/{adr/,papers/,notebooks/}` (adr/ visible — a standard artifact, not working log) ·
`docs/.record/{brief,decisions}.md` (hidden — AI-facing working record) ·
`.record/CONTEXT.md` (hidden — glossary) · `_quarto.yml`. Final results archived to the volume (`/archivist`).
