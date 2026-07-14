---
name: bio-sense
description: Judges whether an analysis result makes biological sense against the brief and the literature. Use after output-QC passes and before writing a result up. The human scientific checkpoint — flags results that conflict with known biology or the grounding literature, or that look like artefacts.
---

# Bio-sense — does it make BIOLOGICAL sense?

The scientific ★ checkpoint, separate from numerical QC. A result can be statistically clean and still be
biological nonsense (or an artefact). You surface the comparison; the user makes the scientific call.

## Do
1. Compare the result against `docs/.record/brief.md` and the literature priors (Obsidian syntheses /
   `~/hub/knowledge/sources.md`).
2. Ask: does it agree with known biology? Where does it conflict? Is a surprising result a real
   finding or an artefact (batch effect, contamination, mislabel)?
3. Flag conflicts and plausible artefacts explicitly — do not smooth them over.
4. The user decides: accept, investigate, or reject.
5. Add a dated, tagged ("Bio-sense") section to `docs/checkpoints.html`, inlined and self-contained
   (not a link to a separate write-up), then log the call via `decide`. Conflict/artefact → loop back to `design` or `build`. Genuine
   surprise the user accepts → proceed to `reviewing-analysis`.

Push back rather than agreeing — a wrong-but-plausible result passed here becomes a wrong paper.
See `~/hub/design.md` (bio-sense checkpoint).
