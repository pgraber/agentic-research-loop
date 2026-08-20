---
name: scope
description: Locks the scientific point of an analysis before any code is written — the biological question, the expected answer shape, and (for anything manuscript-bound) what the finding is, whether it is novel, and where it fits the paper. Pre-registers QC thresholds and method intent. Use at the start of an analysis, when the question is fuzzy, or before building. Prevents post-hoc threshold gaming and the "built it then found it doesn't belong" waste.
---

# Scope — lock the point before touching data

Step 0 of the loop. No build until the question AND its scientific point are sharp. This is where
rigor starts, and it is the step whose absence has cost the most: analyses have been built, given an
ADR, and quality-checked, then cut from the paper because the "is there a finding, is it novel, does
it fit the story" question was only asked afterwards. Ask it here, first.

**Read the record first.** Before scoping, read `.record/CONTEXT.md`, `docs/.record/brief.md`,
`docs/.record/decisions.md`, and `docs/adr/` — a question may already be partly framed; build on
logged decisions, never silently re-derive or contradict them.

## Do
1. **Grill for the real question:** what biological question, on what data, what result is *expected*,
   and what would *surprise* you.
2. **Lock the scientific point (before any build).** For anything manuscript- or thesis-bound, get in
   writing: what is the finding, why is it novel, and where does it fit the paper/story. If this
   cannot be stated now, that is the signal to stop and settle it — not to build and hope a finding
   appears. This is the front-of-loop check that prevents the most expensive waste pattern.
3. **Offer a grill when the point is load-bearing or fuzzy.** `grill-me`/`grill-with-docs` cannot
   self-invoke, so name it: recommend the user run `/grill-with-docs` to stress-test the framing
   branch-by-branch before code. Don't run that relentless interrogation inline here.
4. **Pre-register** the QC thresholds and the intended method NOW, before any results exist. Choosing
   thresholds after seeing results is p-hacking, even unintentionally. If the user asks to defer a
   threshold "until we see the results", hold the line: name the pre-registration reason and log the
   yardstick now; deferring it is the exact pattern this step exists to prevent.
5. **Pre-register the expected shapes too, not just the thresholds.** For each step whose size is
   knowable in advance, write down the number and where it comes from: feature count from the
   annotation, sample count from the sample sheet, expected n after a stated filter, sums and ranges
   that must hold. These become the continuous-validation checks the build asserts line by line, and
   the yardstick must come from outside the code that will produce the object. Contract:
   `~/hub/knowledge/validation.md`.
6. **Write `docs/.record/question.md`:** the question, the data, expected/surprising outcomes, the
   finding + novelty + paper-fit, the pre-registered thresholds and method intent, and the expected
   shapes with their sources.
7. **Human approves the question and its point before proceeding** — do not infer approval from a
   "continue"; the framing call is the user's.

## Then
→ `literature` (ground it) if the method or the novelty claim needs evidence, or → `design` if it's
well understood.

Keep the human deciding what the question *is* and what the finding *means* — you sharpen it, you
don't invent it. See `~/hub/design.md` (the loop; pre-registered thresholds; front-of-loop lock).
