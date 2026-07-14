# Design: a research-rigor system built on Claude Code

This document explains why the system is shaped the way it is. The code (skills, templates, install
script) is the easy part to read. This is the thinking behind it.

The system is a set of small, single-purpose skills for [Claude Code](https://docs.claude.com/en/docs/claude-code)
that make an AI coding agent work like a disciplined research assistant for computational biology. It
is not an automation pipeline, and not an app that makes scientific decisions. Its job is to make sure
an analysis is done properly: step by step, quality-controlled at every stage, grounded in the
literature, and recorded in a trail you could hand to a reviewer.

---

## The one stance everything follows from

**Automate the mechanics. Keep the judgment human.**

An AI is good at the ambiguous, one-off, first-time work: understanding a codebase, drafting an
approach, interpreting a QC plot, explaining a method. It is a liability inside the reproducible
compute path, because a result you cannot regenerate identically is not a result.

So the system draws a hard line, the **reproducibility firewall**:

```
 NON-DETERMINISTIC (AI skills)          DETERMINISTIC (programs)
 ambiguous · judgment · one-off         unambiguous · repeatable · cached · forever
 • understand code / data               • the ANALYSIS itself (script / targets / Nextflow)
 • scope · ground · design (decide)     • git commit at each checkpoint (hook, not AI typing git)
 • QC interpretation, bio-sense         • environment capture (lockfile / container digest)
 • draft the narrative, review          • QC metric computation (script → AI interprets output)
                                        • render / deploy (Quarto / Makefile)
      │  crystallize a recurring decision  ▼  (one-way promotion)
      └─ AI writes the script ONCE, it runs deterministically forever, AI never re-does it.
```

Rule of thumb: use the AI for the first time and the ambiguous times, and use code for every time
after. If you would ask the AI to do the same thing twice, it should be a program. The division of
labor is simple. The AI decides and understands, code computes and repeats, and git records. A skill
often ends by turning a settled decision into a deterministic script, so the next run needs no AI at
all.

---

## The research loop (elastic)

Research is a loop, not a pipeline. It fails backward constantly, and the QC and bio-sense
checkpoints send the work back to design or build. The loop is elastic. A throwaway experiment takes
the fast lane, and a figure headed for a paper takes the full path.

```
 0 SCOPE       the biological question + expected answer shape           👤 approve
 1 GROUND      literature triage → deep-read → brief (methods, params w/ citations)
 2 INTAKE-QC ★ is the DATA sound? integrity, sample IDs, metadata, contamination  👤 look
 3 DESIGN      approach + tool/version screening (fetch CURRENT docs) + pre-register
               QC thresholds + fixtures + ADR if there is a real trade-off        👤 approve
 4 BUILD       parameterised script → results/  +  tests (not done until they pass)
 5 OUTPUT-QC ★ do the RESULTS make sense vs the thresholds set at design time?     👤 look
 6 BIO-SENSE ★ result vs brief + literature: is it biologically plausible?         👤 the call
 7 REVIEW      code review + clean-room reproduce (re-run → identical output) + tests
 8 NARRATE     literate notebook: echo code, explain each step and why, inline QC   👤 edit 🏷 tag
 9 REFLECT     memory + ADR + new concepts → glossary / notes (learning compounds)
```

There are two kinds of human checkpoint, both marked 👤. The first is approve-the-plan, before any
work happens: scope and design. Fixing a wrong approach on paper is free. The second is
review-the-output, after the work: intake-QC, output-QC, bio-sense, and narrate. Here you look at
real results and make the scientific call. No agent passes these for you, which is what the ★ marks.

The loop flexes by weight. The fast lane for a tiny experiment is scope in one line, build, eyeball
the QC, and commit. It is still recorded, with one log line and one commit, but there is no ceremony.
You opt up to the full path only for results worth keeping.

The main thing this prevents is jumping straight to code. The agent is told to refuse to build before
the question is scoped and the approach is designed and approved.

---

## Pre-registration, not post-hoc

QC thresholds and validation fixtures are set at the design checkpoint, before the analysis runs.
This is the same anti-gaming logic as pre-registering a study. You decide the yardstick before you
see the result, so a disappointing number cannot quietly move the cutoff. There are three tiers of
check:

1. **Unit tests** on the pure, deterministic transforms, the functions that decide the numbers.
2. **Reference or published-data validation**, meaning acceptance tests with a tolerance against a
   committed fixture. For example, reproduce a published table within some percent, or correlate with
   an orthogonal assay.
3. **Biological controls**, such as stable housekeeping genes and expected markers being present.
   These stay a human bio-sense checkpoint and are not automated away.

Deviating from a pre-registered threshold requires an ADR (architecture decision record), a dated
note explaining the trade-off. The record makes you justify the change rather than drift silently.

---

## The record: the conversation is never the record

> Nothing is decided until it is written to a human-owned file and committed.

This is the rule the whole system exists to enforce. A chat is ephemeral. The scientific product is
the trail. So decisions are logged to markdown and committed, and the record rides in the same commit
as the code it explains, so provenance cannot drift.

Documentation is one layered tree read at three altitudes, not two separate trees:

```
 PRIMING     project instructions (CLAUDE.md), a domain glossary, the direction.
             Read by the agent every session.
 WORKING     brief (why these methods), decisions log, ADRs (why these parameters).
             Both the agent's working memory and the scientific record.
 DELIVERABLE literate notebooks, then the manuscript Methods section, then the paper.
```

Every human checkpoint lands as a dated, tagged section in one visual, self-contained
`checkpoints.html` per project, with a sticky-sidebar table of contents, a plain-language and
technical toggle, and code and tables inlined. There is never a new file per decision. The payoff is
that if the loop faithfully writes the brief, the ADRs, and the environment lockfile, the manuscript
Methods section largely assembles itself. The record is a side effect of running the process
honestly, not a separate end-task.

Git discipline here is stricter than in typical software work, because this is science. There is one
commit per decision, not per feature, so every threshold and filter has its own SHA.
Manuscript-relevant states are tagged (for example `git tag figure-3-v1`) so the paper cites an exact
commit. The commit timestamp is authoritative, and a date typed by the agent is never trusted.

---

## The multi-level stack

This is the Unix philosophy applied to a research working life: small sharp tools with pushback at
every seam, rather than one all-knowing agent.

```
 L0  OFFICE HOURS   strategic partner. "What should I work on? Where can this go?"
                    Reads your goals and non-goals, and pushes back when something drifts.
 L1  LIBRARIAN / ARCHIVIST   place and organize files (low stakes), versus move across
                    storage tiers, back up, and delete (high stakes: dry-run, copy then
                    verify then delete, never a blind rm).
 L2  ROUTERS        research versus admin, which project, new seed or adopt existing.
 L3  PROJECT        one shared data and environment context, the reproducibility unit.
 L4  THE LOOP       the elastic scope-to-reflect loop above.
 L5  SKILLS         each does one rigor step: scope, ground, design, qc, bio-sense,
                    narrate, decide, reflect, status.
```

Five principles hold the stack together:
1. **Single responsibility.** Each skill does one thing well.
2. **Context flows down.** Each level reads the level above as context.
3. **Pushback at every seam.** No level is a yes-man. Each challenges the one above and below, for
   example "this drifts from your non-goal" or "this result does not make biological sense".
4. **Safety scales with destructiveness.** The more irreversible the action, the more confirmation
   and dry-running it demands.
5. **You are at every checkpoint.** The system supports, you decide.
6. **The system teaches, it does not black-box.** You must be able to follow and explain every step.
   Results you cannot understand are an anti-goal. Learning is a first-class output.

Why skills (sub-agents) rather than one big prompt? Three reasons. Context economy, because each runs
in its own small context and keeps the main conversation lean, with heavy reads happening in a
sub-agent that returns a distilled page. Single responsibility, because one tool does one rigor step
well. And parallelism, because independent skills can fan out, running QC on three datasets at once
or several literature searches side by side.

---

## Portability: three layers

The system is meant to be reused anywhere, so it separates strictly on portability:

1. **Infrastructure (portable, public-safe, this repo).** Skills, templates, loop logic, the
   documentation conventions, and this design spec. Institution-agnostic. It is code, not data.
2. **Local config (per-environment, never shared).** One `config.yml` holds every
   environment-specific path, credential location, and entitlement. It is the single place that
   changes when you move machines or institutions. It ships here as `config.example.yml`.
3. **Personal record (portable with you, private).** Your direction, ideas, decisions, and
   accumulated knowledge. This lives in a private repo and never goes public.

Reusing the system elsewhere means cloning the infrastructure, writing a fresh `config.yml`, and
bringing your personal record. Nothing environment-bound is baked into the portable layer. Skills
read paths and entitlements from config and never hardcode a location or an institution.

> **Honest expectation for adopters.** On its own this is a scaffold: the workflow and the skills. It
> is not a running research program. You bring your own goals, your own projects, and your own
> `config.yml`. What it gives you is the discipline and the record, not a finished cockpit.

---

## Files and git are the database

For the record, portfolio, decisions, and provenance there is no database. A database would be a
second source of truth that drifts, plus a separate backup burden. Git is already a versioned,
timestamped, distributed store. Decisions are markdown plus commits, and the query engine is
`ripgrep` for full text and `jq` for structured data. Plain text is future-proof, diffable, and
human-readable.

For data specifically, the format is the store. Tabular data goes to Parquet or CSV. Single-cell and
other large objects go to HDF5, `.h5ad`, or `.rds`, which are already on-disk databases. Cross-dataset
SQL runs through DuckDB over the files in place, with no server. A server database is avoided because
it is mutable, hard to version and archive and cite, and fights the file-based reproducible ethos.
The data behind a figure is a file, archived and cited by path and commit, not a row in a server.

---

## Environment reproducibility

The environment specification lives in git, as a container recipe and a lockfile. The built image
lives in a registry, or as a Singularity or Apptainer `.sif` for HPC. Each step runs inside its
pinned environment. Pin by digest, not by tag, because tags are mutable and can silently move (for
example `tool:1.1` becoming `tool@sha256:9f2c...`). The reproducibility check has teeth. A clean
re-run giving identical output means re-running inside the pinned container from scratch before a
figure is tagged. The provenance footer records the container digest and the lockfile hash, which
makes the proof complete and re-runnable.

The container is the single reproducible artifact and the way work reaches a cluster. You build on a
workstation with internet, convert to a `.sif`, and run on compute nodes that have no internet. Data
is never baked into an image. Images are tools only.

---

## Learning is an output, not a side effect

Because comprehension is a goal and black-box results are an anti-goal, each analysis produces one
literate source rendered two ways, both from the same executed code so they cannot drift:

- a **learning** render, with the code echoed, concept boxes explaining new ideas grounded in the
  screened papers and tool docs, a verbose account of why each step is taken, and inline QC and
  figures.
- a **report** render, with the code folded, terse text, and a provenance footer (commit,
  environment, date), shareable as proof of the analysis.

New concepts are explained once and linked thereafter, accumulating in a glossary and a personal
notes vault so learning compounds across projects. The explainer shows and explains the deterministic
code and its real outputs. It never recomputes a number in prose.

---

## Safety, secrets, and governance

- **Default-deny cloud.** Nothing goes to a cloud remote unless that repository is explicitly
  cleared. Sensitive or patient-derived data must never touch a cloud service. The default backup
  remote is a bare git repo on institution-controlled storage.
- **Secrets** live as shell environment variables in a single git-ignored file (`chmod 600`), read
  the same way by R, Python, and shell. They are never committed, and a secret-scan guards the push
  path.
- **Raw data is immutable.** Analysis works on a read-only copy that is filesystem-locked. It reads
  from `data/` and writes only to `results/`. A step that "modifies" data writes a new derived file,
  and the input stays untouched. Provenance records the source path, checksum, and date.
- **Destructive operations dry-run first.** They show the plan and confirm, then copy, then verify by
  checksum, then delete, as separate confirmed steps. There is never a blind `rm -rf`. A git guardrail
  hook blocks the agent from `push`, `reset --hard`, `clean -f`, and branch deletion.

---

## The system maintains itself (one meta-level, no more)

The system evolves through its own machinery, because it is itself a project. This design doc is its
brief, its architecture choices are logged as decisions and ADRs, and the repo git-tracks its own
design. "Review the architecture" is office-hours pointed at the system. There is a firm ceiling.
Stop at one meta-level. No meta-agent managing the meta-agent. That way lies the biggest hidden
time-sink, polishing the tooling instead of doing the science.

---

## What it is not (non-goals)

- Not automation that makes scientific decisions for you.
- Not method development for its own sake.
- Not infrastructure too complex to maintain single-handedly.
- Not a producer of results you cannot understand and explain.

These non-goals are load-bearing. They let the agent prune whole branches of work without asking.
