# Adopting and extending agentic-research-loop

This is mainly a personal research system, published so others can read the design, borrow ideas, and
adopt the workflow. It is a rigor scaffold, not a turnkey product. See the "What you need to bring"
section of the [README](README.md).

## The three layers (public versus private)

| Layer | What | Where | Public? |
|---|---|---|---|
| **Infrastructure** | skills, templates, loop logic, this design | *this repo* | yes |
| **Local config** | paths, entitlements, credential locations | your `config.yml` plus a git-ignored `.env` | no |
| **Personal record** | goals, ideas, decisions, accumulated knowledge | a *separate private* repo | no |

Nothing environment-specific is baked into the infrastructure. Skills read paths and entitlements
from `config.yml` and never hardcode a location or an institution. That is what lets the same skills
work unchanged across machines and institutions.

## Adopt it for yourself

```bash
git clone https://github.com/pgraber/agentic-research-loop.git ~/research-system
cd ~/research-system && ./install.sh          # symlinks skills into ~/.claude/skills/
cp config.example.yml ~/hub/config.yml        # edit paths for your environment
```

Then keep your own private hub (direction, decisions, knowledge) in a separate repo, and keep your
analyses in their own project repos scaffolded from `templates/`.

## Extend or add a skill

Each skill is a directory under `skills/<name>/` with a `SKILL.md` that has front-matter (`name` and
`description`) followed by the instructions. To keep the set coherent:

- **One skill, one rigor step.** If a skill starts doing two jobs, split it.
- **Read config, do not hardcode.** Any path, institution, or entitlement comes from `config.yml`.
- **Pushback over compliance.** A skill should challenge a bad plan, not just execute it.
- **The human keeps the scientific checkpoints.** Do not automate away intake-QC, output-QC, or
  bio-sense. Surface the evidence and let the person decide.
- **The conversation is never the record.** A skill that produces a decision ends by writing it to a
  human-owned file and committing.

After editing, run `./install.sh` (idempotent) and `bin/check-structure` (the compendium linter).

## Contributions

Issues and pull requests that sharpen the design or generalize a skill further are welcome. Because
this tracks one person's real workflow, large feature additions may be declined if they pull against
the non-goals in [`docs/DESIGN.md`](docs/DESIGN.md): no automation of judgment, no method development
for its own sake, and no infrastructure too complex to maintain single-handedly.
