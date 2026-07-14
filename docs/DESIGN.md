# Design — a research-rigor system built on Claude Code

This document explains *why* the system is shaped the way it is. The code (skills, templates,
install script) is the easy part to read; this is the thinking behind it.

The system is a set of narrow, single-purpose **skills** for [Claude Code](https://docs.claude.com/en/docs/claude-code)
that turn an AI coding agent into a disciplined research assistant for computational biology. It is
deliberately **not** an automation pipeline and **not** an app that makes scientific decisions. Its
job is to make sure an analysis is done *right* — step by step, quality-controlled at every stage,
grounded in the literature, and recorded in a trail you could hand to a reviewer.

---

## The one stance everything follows from

**Automate the mechanics; never automate away the judgment.**

An AI is excellent at the ambiguous, one-off, first-time work (understanding a codebase, drafting an
approach, interpreting a QC plot, explaining a method). It is a liability sitting inside the
*reproducible compute path*, because a result you cannot regenerate identically is not a result.

So the system draws a hard line — the **reproducibility firewall**:

```
 NON-DETERMINISTIC (AI skills)          DETERMINISTIC (programs)
 ambiguous · judgment · one-off         unambiguous · repeatable · cached · forever
 • understand code / data               • the ANALYSIS itself (script / targets / Nextflow)
 • scope · ground · design (decide)     • git commit at each checkpoint (hook, not AI typing git)
 • QC interpretation, bio-sense         • environment capture (lockfile / container digest)
 • draft the narrative, review          • QC metric computation (script → AI interprets output)
                                        • render / deploy (Quarto / Makefile)
      │  crystallize a recurring decision  ▼  (one-way promotion)
      └─ AI writes the script ONCE → it runs deterministically forever; AI never re-does it.
```

Rule of thumb: **AI for the first time and the ambiguous times; code for every time after.** If
you would ask the AI to do the same thing twice, it should be a program. The division of labor:
**AI decides and understands; code computes and repeats; git records.** A skill often *ends* by
promoting a settled decision into a deterministic script, so the next run needs no AI at all.

---

## The research loop (elastic)

Research is a **loop, not a pipeline** — it fails backward constantly. QC and bio-sense checkpoints
send you back to design or build. The loop is elastic: a throwaway experiment takes the fast lane; a
figure-worthy result takes the full path.

```
 0 SCOPE       the biological question + expected answer shape           👤 approve
 1 GROUND      literature triage → deep-read → brief (methods, params w/ citations)
 2 INTAKE-QC ★ is the DATA sound? integrity, sample IDs, metadata, contamination  👤 look
 3 DESIGN      approach + tool/version screening (fetch CURRENT docs) + pre-register
               QC thresholds + fixtures + ADR if there is a real trade-off        👤 approve
 4 BUILD       parameterised script → results/  +  tests (not done until they pass)
 5 OUTPUT-QC ★ do the RESULTS make sense vs the thresholds set at design time?     👤 look
 6 BIO-SENSE ★ result vs brief + literature — is it biologically plausible?        👤 the call
 7 REVIEW      code review + clean-room reproduce (re-run → identical output) + tests
 8 NARRATE     literate notebook: echo code, explain each step + why, inline QC    👤 edit 🏷 tag
 9 REFLECT     memory + ADR + new concepts → glossary / notes (learning compounds)
```

**Two kinds of human checkpoint**, both marked 👤:
- **Approve-the-plan, before work** (scope, design). Fixing a wrong approach on paper is free.
- **Review-the-output, after work** (intake-QC, output-QC, bio-sense, narrate). You look at real
  results and make the scientific call. No agent passes these for you (★).

**Elastic by weight:** the fast lane (a tiny experiment) is `scope one line → build → eyeball QC →
commit`, still recorded but with no ceremony. You *opt up* to the full path only for keepers.

The key anti-pattern this prevents: **jumping straight to code.** The agent is instructed to refuse
to build before the question is scoped and the approach is designed and approved.

---

## Pre-registration, not post-hoc

QC thresholds and validation fixtures are set at the **design** checkpoint, *before* the analysis
runs — the same anti-gaming logic as pre-registering a study. You decide the yardstick before you
see the result, so a disappointing number cannot quietly move the cutoff. Three tiers of check:

1. **Unit tests** on the pure, deterministic transforms (the functions that decide the numbers).
2. **Reference / published-data validation** — acceptance tests with a tolerance against a committed
   fixture (e.g. "reproduce the published table within X%", "correlate with the orthogonal assay").
3. **Biological controls** — housekeeping stable, expected markers present. These stay a *human*
   bio-sense checkpoint; they are not automated away.

A deviation from a pre-registered threshold requires an ADR (architecture decision record) — a dated
note explaining the trade-off. The record challenges you; it does not let you drift silently.

---

## The record — the conversation is never the record

> Nothing is decided until it is written to a human-owned file and committed.

This is the rule the whole system exists to enforce. A chat is ephemeral; the scientific product is
the trail. So decisions are logged to markdown and committed, with the record riding *in the same
commit* as the code it explains — provenance that cannot drift.

Documentation is one layered tree read at three altitudes, not two separate trees:

```
 PRIMING     project instructions (CLAUDE.md), a domain glossary, the direction —
             read by the agent every session
 WORKING     brief (why these methods), decisions log, ADRs (why these parameters) —
             BOTH the agent's working memory AND the scientific record
 DELIVERABLE literate notebooks → the manuscript Methods section → the paper
```

Every human checkpoint lands as a dated, tagged section in one visual, self-contained
`checkpoints.html` per project (a sticky-sidebar table of contents, a plain-language / technical
toggle, code and tables inlined) — never a new file per decision. The **payoff**: if the loop
faithfully writes the brief, the ADRs, and the environment lockfile, **the manuscript Methods
section assembles itself.** The record is a side effect of running the process honestly, not a
separate end-task.

**Git discipline (harder than typical software practice, because science):** one commit per
*decision*, not per feature — every threshold and filter has its own SHA. Manuscript-relevant states
are tagged (`git tag figure-3-v1`) so the paper cites an exact commit. The commit timestamp is
authoritative; a date typed by the agent is never trusted.

---

## The multi-level stack

Unix philosophy applied to a research working life: small sharp tools with pushback at every seam,
not one god-agent.

```
 L0  OFFICE HOURS  — strategic partner. "What should I work on? Where can this go?"
                     Reads your goals + non-goals; pushes back when something drifts.
 L1  LIBRARIAN / ARCHIVIST — place & organize files (low stakes) vs move across storage
                     tiers, back up, delete (HIGH stakes: dry-run, copy→verify→delete, never blind rm).
 L2  ROUTERS       — research vs admin; which project; new seed or adopt existing.
 L3  PROJECT       — one shared data + environment context (the reproducibility unit).
 L4  THE LOOP      — the elastic scope→…→reflect loop above.
 L5  SKILLS        — each does ONE rigor step: scope · ground · design · qc · bio-sense ·
                     narrate · decide · reflect · status.
```

Five principles hold the stack together:
1. **Single responsibility** — each skill does one thing well.
2. **Context flows down** — each level reads the level above as context.
3. **Pushback at every seam** — no level is a yes-man; each challenges the one above and below
   ("this drifts from your non-goal", "this result doesn't make biological sense").
4. **Safety scales with destructiveness** — the more irreversible the action, the more confirmation
   and dry-running it demands.
5. **You are at every checkpoint** — the system supports; you decide.
6. **The system teaches, it doesn't black-box** — you must be able to follow and explain every step.
   Results you can't understand are an anti-goal. Learning is a first-class output.

**Why skills (sub-agents) rather than one big prompt?** Three reasons: *context economy* (each runs
in its own small context, keeping the main conversation lean — heavy reads happen in a sub-agent that
returns a distilled page); *single responsibility* (one tool, one rigor step, done excellently); and
*parallelism* (independent skills fan out — QC three datasets at once, run several literature
searches in parallel).

---

## Portability — three layers

The system is designed to be reused anywhere, by separating strictly on portability:

1. **Infrastructure (portable, public-safe — this repo).** Skills, templates, loop logic, the
   documentation conventions, this design spec. Institution-agnostic. It is code, not data.
2. **Local config (per-environment, never shared).** One `config.yml` holds every
   environment-specific path, credential location, and entitlement. It is the *single* place that
   changes when you move machines or institutions. Ships here as `config.example.yml`.
3. **Personal record (portable with you, private).** Your direction, ideas, decisions, and
   accumulated knowledge. A private repo — never public.

Reuse elsewhere = clone the infrastructure, write a fresh `config.yml`, bring your personal record.
Nothing environment-bound is baked into the portable layer. Skills read paths and entitlements *from
config*; they never hardcode a location or an institution.

> **Honest expectation for adopters:** cloned on its own, this is a rigor *scaffold* — the workflow
> and the skills. It is not a running research program. You bring your own goals, your own projects,
> and your own `config.yml`. The value is the thinking-partner, the rigor, and the record, not a
> pre-filled cockpit.

---

## Files + git are the database

For the record, portfolio, decisions, and provenance there is **no database** — that would be a
second source of truth that drifts, plus a separate backup burden. Git is already a versioned,
timestamped, distributed store; decisions are markdown plus commits; the query engine is `ripgrep`
(full-text) and `jq` (structured). Plain text is future-proof, diffable, and human-readable.

For *data* specifically, the format is the store: tabular → Parquet/CSV; single-cell/large objects →
HDF5/`.h5ad`/`.rds` (already an on-disk database); cross-dataset SQL → DuckDB over files in place
(no server). A server database is avoided — it is mutable, hard to version/archive/cite, and fights
the file-based reproducible ethos. Data behind a figure is a *file*, archived and cited by
path + commit, not a server row.

---

## Environment reproducibility

The environment **specification** lives in git (a container recipe and a lockfile); the built
**image** lives in a registry or as a Singularity/Apptainer `.sif` for HPC; each step runs inside its
pinned environment. Pin by **digest, not tag** — tags are mutable and can silently move
(`tool:1.1` → `tool@sha256:9f2c…`). The reproducibility check has teeth: "clean re-run → identical
output" means re-running *inside the pinned container from scratch* before a figure is tagged. The
provenance footer records the container digest and the lockfile hash — a complete, re-runnable proof.

The container is the single reproducible artifact and the delivery path to a cluster: build on a
workstation with internet, convert to `.sif`, run on compute nodes that have no internet. Never bake
data into an image — images are tools only.

---

## Learning is an output, not a side effect

Because comprehension is a goal and black-box results are an anti-goal, each analysis produces **one
literate source rendered two ways** (from the *same* executed code, so they cannot drift):
- a **learning** render — code echoed, concept boxes explaining new ideas (grounded in the screened
  papers and tool docs), verbose *why*, inline QC and figures;
- a **report** render — code folded, terse, with a provenance footer (commit, environment, date),
  shareable as proof of the analysis.

New concepts are explained once and linked thereafter, accumulating in a glossary and a personal
notes vault so learning compounds across projects. The explainer *shows and explains* the
deterministic code and its real outputs; it never recomputes a number in prose.

---

## Safety, secrets, and governance

- **Default-deny cloud.** Nothing goes to a cloud remote unless that repository is explicitly
  cleared. Sensitive or patient-derived data must never touch a cloud service. The default backup
  remote is a bare git repo on institution-controlled storage.
- **Secrets** live as shell environment variables in a single git-ignored file (`chmod 600`), read
  identically by R, Python, and shell. Never committed; a secret-scan guards the push path.
- **Raw data is immutable.** Analysis works on a read-only copy (filesystem-locked), reads from
  `data/`, and writes only to `results/`. A step that "modifies" data writes a new derived file; the
  input stays pristine. Provenance records the source path, checksum, and date.
- **Destructive operations dry-run first**, show the plan, and confirm — copy, verify (checksum),
  then delete as separate confirmed steps. Never a blind `rm -rf`. A git guardrail hook blocks the
  agent from `push`, `reset --hard`, `clean -f`, and branch deletion.

---

## The system maintains itself (one meta-level, no more)

The system evolves through its own machinery — it is itself a project: this design doc is its brief,
its architecture choices are logged as decisions and ADRs, and the repo git-tracks its own design.
"Review the architecture" is office-hours pointed at the system. The firm ceiling: **stop at one
meta-level.** No meta-agent managing the meta-agent. That way lies the biggest hidden time-sink —
polishing the tooling instead of doing the science.

---

## What it is not (non-goals)

- Not automation that makes scientific decisions for you.
- Not method development for its own sake.
- Not infrastructure too complex to maintain single-handedly.
- Not a producer of results you can't understand and explain.

These non-goals are load-bearing: they let the agent prune whole branches of work without asking.
