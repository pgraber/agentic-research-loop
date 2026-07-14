# <NAME>

<One-line description: the biological question this project answers.>

## What / why / how
- **Question:** see `docs/.record/brief.md`
- **Data:** raw is read-only in `data/` (provenance in `data/raw/PROVENANCE.md`); master on the
  institute volume.
- **Run:** analysis is containerised (`env/`) and reproducible — see `docs/notebooks/` for the
  narrative, `docs/checkpoints.html` for every human checkpoint, and `docs/.record/decisions.md`
  for the decision log.

## Layout
`data/` raw (read-only) · `results/` generated (gitignored) · `figures/` · `scripts/` code ·
`env/` container recipe + lockfile · `workflow/` optional pipeline · `docs/checkpoints.html`
every human checkpoint (TOC'd) · `docs/adr/` ADRs (visible) · `docs/.record/` hidden brief +
decisions · `docs/{papers,notebooks}/` · `.record/CONTEXT.md` hidden glossary.

Part of the research system — see `~/hub/` (spec, skills, config).
