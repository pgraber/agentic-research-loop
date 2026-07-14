# agentic-research-loop

**A rigor-first research assistant for computational biology, built as [Claude Code](https://docs.claude.com/en/docs/claude-code) skills.**

A set of small, single-purpose skills that make an AI coding agent work like a careful research
assistant. Analysis runs as a step-by-step, quality-controlled loop, a human signs off at every
scientific checkpoint, and the whole thing leaves a decision trail you could hand to a reviewer.

It is not an automation pipeline, and not an app that makes the scientific calls for you. The idea in
one line: automate the mechanics, keep the judgment human.

> **Start with [`docs/DESIGN.md`](docs/DESIGN.md).** It explains the reasoning behind the system: the
> line between AI and reproducible code, the loop, the record, and how everything stays portable. The
> code just implements what that document describes.

---

## The loop it enforces

```
 SCOPE → GROUND → INTAKE-QC ★ → DESIGN → BUILD → OUTPUT-QC ★ → BIO-SENSE ★ → REVIEW → NARRATE → REFLECT
   the      the      is the       method +   parameterised   do results   biologically   clean-room   literate   learning
 question  literature  data       pinned      script +        make sense   plausible?     reproduce    write-up   compounds
           grounding   sound?      tools +     tests           vs design?
                                   thresholds
```

`★` marks a checkpoint the agent cannot pass for you. It is a loop, not a pipeline, so QC and
bio-sense can send the work back to design or build. It is also elastic. A quick experiment takes the
fast lane: scope in a line, build, eyeball the result, commit. A figure headed for a paper takes the
full path.

## What's in here

```
skills/      the research-rigor skills, one per loop step (source of truth)
templates/   the research-compendium layout a new analysis is scaffolded into
install.sh   symlinks each skill into ~/.claude/skills/ so Claude Code loads it
bin/         sync (commit + push) and check-structure (compendium linter)
docs/        DESIGN.md, the architecture and the reasoning
config.example.yml   the one per-environment config file. Copy it and fill in your paths.
examples/    a worked walkthrough of the loop on a public dataset (10x PBMC 3k)
```

## Quick start

```bash
git clone https://github.com/pgraber/agentic-research-loop.git ~/research-system   # dir the skills reference
cd ~/research-system
./install.sh                              # symlinks skills into ~/.claude/skills/
cp config.example.yml ~/hub/config.yml    # then edit paths for your environment
```

Open Claude Code and the skills are available (for example `/office-hours`, `/scope`, `/design`,
`/output-qc`, `/narrate`). Each skill ends by naming the next one, so you do not have to remember the
sequence. See [`examples/pbmc3k/`](examples/pbmc3k/) for the loop run end to end on a public dataset.

## What you need to bring

On its own this is a scaffold: the workflow and the skills, not a running research program. Three
things stay yours and are not included here.

- **A `config.yml`** with your paths and entitlements. Nothing about my own setup is baked into the
  skills, so you fill this in for your environment.
- **Your projects.** The actual analyses live in their own repos.
- **Your direction and record.** Goals, decisions, and the knowledge you build up over time. These
  stay private.

What you get is the discipline and the record, not a finished cockpit.

## Design lineage

The project layout follows the research-compendium convention (Marwick et al. 2018, `rrtools`). The
reproducibility and workflow practices draw on the field's standard references: Wilson et al. *Good
Enough Practices in Scientific Computing* (2017), Noble (2009), Sandve et al. *Ten Simple Rules for
Reproducible Computational Research* (2013), The Turing Way, and the FAIR principles.

## License

[MIT](LICENSE). See [`CONTRIBUTING.md`](CONTRIBUTING.md) to adopt or extend it.
