# agentic-research-loop

**A rigor-first research assistant for computational biology, built as [Claude Code](https://docs.claude.com/en/docs/claude-code) skills.**

This is a set of narrow, single-purpose skills that turn an AI coding agent into a disciplined
research assistant. It enforces a step-wise, quality-controlled analysis loop with a human at every
scientific checkpoint, and a recorded decision trail you could hand to a reviewer.

It is deliberately **not** an automation pipeline and **not** an app that makes scientific decisions
for you. The design principle is one line: **automate the mechanics, never automate away the
judgment.**

> **Read [`docs/DESIGN.md`](docs/DESIGN.md) for the thinking behind it** — the reproducibility
> firewall, the loop, the record, and the portability model. That document is the point of this repo;
> the code just implements it.

---

## The loop it enforces

```
 SCOPE → GROUND → INTAKE-QC ★ → DESIGN → BUILD → OUTPUT-QC ★ → BIO-SENSE ★ → REVIEW → NARRATE → REFLECT
   the      the      is the       method +   parameterised   do results   biologically   clean-room   literate   learning
 question  literature  data       pinned      script +        make sense   plausible?     reproduce    write-up   compounds
           grounding   sound?      tools +     tests           vs design?
                                   thresholds
```

`★` = a human checkpoint the agent cannot pass for you. It is a **loop, not a pipeline** — QC and
bio-sense fail backward to design or build. It is **elastic**: a throwaway experiment takes a fast
lane (scope one line → build → eyeball → commit); a figure-worthy result takes the full path.

## What's in here

```
skills/      the research-rigor skills — one skill per loop step (source of truth)
templates/   the research-compendium project layout a new analysis is scaffolded into
install.sh   symlinks each skill into ~/.claude/skills/ so Claude Code loads it
bin/         sync (commit + push) and check-structure (compendium linter)
docs/        DESIGN.md — the architecture and the reasoning
config.example.yml   the single per-environment config; copy it, fill in your paths
examples/    a worked walkthrough of the loop on a public dataset (10x PBMC 3k)
```

## Quick start

```bash
git clone https://github.com/pgraber/agentic-research-loop.git ~/research-system   # dir the skills reference
cd ~/research-system
./install.sh                              # symlinks skills into ~/.claude/skills/
cp config.example.yml ~/hub/config.yml    # then edit paths for your environment
```

Open Claude Code and the skills are available (e.g. `/office-hours`, `/scope`, `/design`,
`/output-qc`, `/narrate`). Each skill ends by naming the next one, so you never have to remember the
sequence. See [`examples/pbmc3k/`](examples/pbmc3k/) for the loop run end to end on a public dataset.

## Honest expectation

Cloned on its own, this is a rigor **scaffold** — the workflow and the skills, not a running research
program. You bring three things it does not ship:

- **your `config.yml`** — every environment-specific path and entitlement (institution-agnostic by
  design; nothing about my setup is baked into the skills);
- **your projects** — the actual analyses, in their own repos;
- **your direction and record** — goals, decisions, accumulated knowledge (private, never public).

The value is the thinking-partner, the rigor, and the record — not a pre-filled cockpit.

## Design lineage

The compendium structure follows the research-compendium convention (Marwick et al. 2018; `rrtools`),
and the reproducibility and workflow practices draw on the field's canon — Wilson et al. *Good Enough
Practices in Scientific Computing* (2017), Noble (2009), Sandve et al. *Ten Simple Rules for
Reproducible Computational Research* (2013), The Turing Way, and the FAIR principles.

## License

[MIT](LICENSE) — see [`CONTRIBUTING.md`](CONTRIBUTING.md) to adopt or extend it.
