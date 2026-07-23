---
name: reflect
description: Captures learnings at the end of an analysis — new concepts into the project glossary and Obsidian, decisions into ADRs, and durable facts into memory. Use at the end of a loop, after a figure is finished, or when something non-obvious was learned. Makes learning compound across analyses.
---

# Reflect — capture what was learned

The loop's closing step. Turns each analysis into durable, reusable knowledge so nothing has to be
re-learned.

**This is the capture that actually works — route "update the md" / "remember this" through here.**
In practice durable learning lands not by invoking this skill by name but by the user saying "add that
to the md" or "remember this"; treat those as this step. Capture channels by kind: behavioural
rules/preferences → the relevant `CLAUDE.md` (global or project, the auto-loaded layer); reusable
concepts → Obsidian + `.record/CONTEXT.md`; hard-to-reverse decisions → an ADR; durable cross-session
facts → a memory file. Keep it light; the point is that capture happens, not ceremony.

**Read the record first.** Before capturing, read the existing `.record/CONTEXT.md`, `docs/.record/decisions.md`,
and `docs/adr/` so you extend the record rather than duplicating entries already there.

## Do
1. **New concepts** — anything the user learned that was new → add a short explanation to
   `.record/CONTEXT.md` (project glossary) and, if cross-project, to the Obsidian vault
   (`paths.obsidian`). Explained once, linked thereafter.
   - **Active recall before writing, not after.** For a concept sourced from literature, don't
     transcribe the source text straight into the note — ask the user to state it back in their own
     words (or answer 1-2 questions about it) first, then write the note from that. A note written
     without that check is a document to reread, not something retained; `literature` already runs
     this same check at its own close (step 8) — don't skip it here just because the session wasn't
     a `/literature` run.
   - Literature-derived concepts get a backlink to the Obsidian reading note they came from (per
     `literature`'s Grounding/Survey split) — a concept with no traceable source is hard to trust
     later when it's out of context.
2. **Decisions** — heavyweight/hard-to-reverse calls → an ADR in `docs/adr/`; smaller ones are
   already in `docs/.record/decisions.md` via `decide`. Only applies when the session was Grounding a decision
   (see `literature`'s classification) — a pure Survey session has nothing to log here.
3. **Durable facts** — anything worth carrying to future sessions → a memory file.
4. **Automate only if it repeated** — if a mechanical step genuinely recurred, note it as a
   candidate to crystallize into a script/skill. Don't automate speculatively.

Keep it brief — a few lines of real learning beats a long summary. See `~/hub/design.md`
(reflect; learning compounds; knowledge reuse).
