---
name: scope
description: Defines the biological question, the expected answer shape, and pre-registers QC thresholds and method intent before any analysis begins. Use at the start of an analysis, when the research question is fuzzy, or when the user wants to plan an analysis. Prevents post-hoc threshold gaming.
---

# Scope — nail the question before touching data

Step 0 of the loop. No analysis until the question is sharp. This is where rigor starts: a fuzzy
question makes every later QC criterion meaningless.

**Read the record first.** Before scoping, read `.record/CONTEXT.md`, `docs/.record/brief.md`, `docs/.record/decisions.md`,
and `docs/adr/` — a question may already be partly framed; build on logged decisions, never silently
re-derive or contradict them.

## Do
1. Grill for the real question: what biological question, on what data, what result is *expected*,
   and what would *surprise* you.
2. **Pre-register** — write down the QC thresholds and the intended method NOW, before any results
   exist. (Choosing thresholds after seeing results is p-hacking, even unintentionally.)
3. Write `docs/.record/question.md`: the question, the data, expected/surprising outcomes, pre-registered
   thresholds and method intent.
4. Human approves the question before proceeding.

## Then
→ `literature` (ground it) if the method needs evidence, or → `design` if it's well understood.

Keep the human deciding what the question *is* — you sharpen it, you don't invent it. See
`~/hub/design.md` (the loop; pre-registered thresholds).
