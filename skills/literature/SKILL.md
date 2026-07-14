---
name: literature
description: Bio-specialized literature deep-research — triage, discovery, full-text verification, and a tiered cited synthesis written to Obsidian and the sources registry. Use when researching the literature, grounding methods, checking what the literature says, or running the Ground step of an analysis. Wraps the deep-research harness and reads in sub-agents to keep context small.
---

# Literature — rigorous, cited, bio-specialized deep research

Wraps the `deep-research` harness (fan-out → fetch → adversarial verify → cited synthesis); do not
reimplement it. Add the biomedical layer, source-tiering, and full-text verification. Keys are shell
env vars in `~/.env`.

## Workflow
**First, classify the session — Grounding or Survey.** This decides which artefacts step 6 produces;
get it wrong and a survey masquerades as a decision record, or a real decision ships unchecked.
- **Grounding** — this literature feeds a specific pending decision (method choice, threshold,
  direction call) that will be logged via `decide` in `docs/.record/decisions.md` or an ADR. Produces all
  three artefacts in step 6, including the decision-record HTML (6c).
- **Survey** — pure understanding-building for a topic/field; no decision is pending. Produces only
  the Obsidian learning layer (6a) and the reading list (6b) — skip 6c, there is no decision to make
  checkable. If a readable pass is still wanted, render the MOC narrative as an Artifact, but do not
  save it into `docs/papers/` as a decision record — that would misrepresent a survey as grounding.
- When unsure which one this is, ask. The answer changes what gets *written*, not just how it reads.

1. **Check trusted anchors first** — read `~/hub/knowledge/sources.md`. Reuse gold-standard sources
   before fanning out.
2. **Triage** — `Consensus` and `Elicit` MCP connectors (evidence synthesis / structured extraction)
   to surface candidate papers and claims. Triage is a STARTING point, never the whole search.
3. **Discovery — query every source, don't stop at triage.** Run PubMed AND OpenAlex AND (for
   preprints) bioRxiv/medRxiv, not just Consensus. Pitfalls that silently drop sources:
   - **PubMed**: a long natural-language query gets over-ANDed and returns 0. Build focused queries
     (MeSH terms, few clauses); if a query returns 0, broaden and retry before concluding "nothing".
   - **bioRxiv/medRxiv**: NO keyword search (date+category only). Do topical preprint discovery via
     OpenAlex / Europe PMC / Consensus, then fetch specific preprints by DOI with `bioRxiv:get_preprint`.
   - **Coverage is mandatory and logged in a REQUIRED artifact.** Write a coverage log — a table of
     `source × query × hit-count × reachable?(y/n, reason if n)` — as the FIRST section of the
     human-readable review (`docs/papers/literature-review.html`, step 6c) and mirror it into the Obsidian MOC.
     If a source returned nothing or was unreachable (auth/VPN), say so explicitly in the table.
   - **HARD GATE — single-source = fail.** A synthesis is NOT allowed to ship on triage alone. The
     minimum bar is PubMed **and** OpenAlex **and** one preprint source (bioRxiv/medRxiv via
     OpenAlex/Europe PMC) actually queried — Consensus/Elicit are triage, they do not count toward
     it. If the bar can't be met (source down, off-VPN), STOP and say so in the coverage log; do not
     silently present a narrower search as "the literature".
4. **Full-text verify** (order = OA first, then subscribed):
   - OA/keyless: Springer OA API, Europe PMC, Unpaywall, bioRxiv
   - Subscribed publishers (from config `literature.full_text_on_vpn`, e.g. Elsevier ScienceDirect) —
     **preflight your institution's VPN** (macOS `scutil --nc status` or a
     test call); if off-VPN, fall back to OA and flag. Never bypass paywalls (no Sci-Hub); anything
     unreachable → list in the project's `docs/papers/sources/need-pdf.md` for a manual PDF drop.
   - **Repo holds text outputs only; PDFs live in EndNote** (`endnote_data` in `~/hub/config.yml`),
     the reference-manager PDF store — never loose in `docs/papers/`. If a PDF genuinely must sit in
     the repo for an analysis step, a **gitignored `docs/papers/pdf/`** subfolder, never the top level.
5. **Synthesize** — tier each source (T1 peer-reviewed/seminal, T2 standard, T3 preprint — always
   flag preprints), cite everything, and make the evidence basis VISIBLE, not just recorded:
   - Every source and every claim it supports carries a `basis: full-text | abstract` marker,
     shown in the synthesis (a badge in the HTML, a field in the Obsidian note) — the reader always
     sees whether a statement was verified against the actual paper or only its abstract.
   - **A basis tally is REQUIRED** in the review — `N full-text / M abstract` across cited sources —
     so an all-abstract synthesis (a run that read no full text) is glaringly visible and cannot pass
     unremarked. It also seeds the step-7 ask.
   - **Abstract-only = explicitly lower confidence.** Flag it: the claim may not reflect what the
     full text actually says (methods/caveats/numbers live in the body, not the abstract). Never let
     an abstract-derived claim read as if the paper was read. Anything method-defining that is still
     abstract-only is a candidate for the step-7 full-text ask.
   - A claim asserted with confidence must trace to a full-text source; if only an abstract backs it,
     hedge the language and say so.

**Folder homes (obey global CLAUDE.md folder-hygiene).** ONE human-readable file per project: `docs/papers/literature-review.html` — different topics are SECTIONS inside it, never separate per-topic HTML files. Machine/AI sources (`reading-list.md`, `need-pdf.md`, coverage tables, `.ris`) live in `docs/papers/sources/`. PDFs (only if one must sit in-repo) in a gitignored `docs/papers/pdf/`. The paths named below resolve to these homes.

6. **Output — three artefacts in Grounding mode, two in Survey mode** (see classification above).
   Markdown is for the vault/AI; a Grounding session's human also needs a readable, decision-clear
   version.
   a. **Obsidian — the LEARNING layer** (`paths.obsidian` in `~/hub/config.yml`, under `<project>/`).
      This is where understanding is kept, deliberately OUT of the repo so structure stays clean, and
      it is written to TEACH — as if you had read the papers, not to cite them:
      - **Per-paper reading notes** — each written as learning notes: the question the paper asked,
        what they did (method in plain terms), what they found, the one result that matters, and
        **why it matters for us**. Not a metadata stub.
      - **A "What we learned" narrative** in the project **Map (MOC)** note — ties the papers into an
        understanding of the subfield (what's settled, what's contested, where our work sits), linking
        the per-paper notes and `Concepts/` entries.
      - **An "Open questions" section in the MOC — this makes it a LIVING document.** Reading
        questions the user raises (in-session or later) get parked here with a date; each is resolved
        in place (answer + link to the note/source/decision it produced) or carried to the next
        `/literature` pass. On any re-run, read Open questions FIRST and address them. The Obsidian
        MOC is the living source of truth; the repo `docs/papers/literature-review.html` is a rendered snapshot
        of it at synthesis time (regenerate it when the MOC materially changes).
      - Reusable `Concepts/` notes for recurring domain terms. Save new gold-standard anchors to
        `~/hub/knowledge/sources.md` with `last_checked`.
      (Contrast: the repo `docs/papers/literature-review.html` (6c) is the DECISION record — checkable
      method→control→evidence. Obsidian is the DURABLE understanding. Two audiences, two homes.)
   b. **Recommended reading — the prioritized INDEX, not a duplicate of the depth.** The human's
      shortlist: must-read / recommended / background, each with a one-line WHY, its tier, and TWO
      resolvable links (linking rule in 6c) — one to the paper, one to its Obsidian learning note.
      It indexes INTO the learning layer, it does not re-teach it. Render it human-readably as a
      **"Reading list" section inside the HTML review (6c)** — the HTML is the single human entry
      point — with the plain-text `docs/papers/sources/reading-list.md` as the machine/quick-reference source.
      (Three artefacts in Grounding mode, three jobs: reading-list = what-to-read-first; HTML =
      checkable decisions; Obsidian = durable learning — two jobs in Survey mode, HTML dropped.
      Cross-linked, never duplicated.)
   c. **Human-readable review — Grounding sessions only, skip entirely for Survey.** Render an **Artifact** (load the `artifact-design` skill first) and
      ALSO save the HTML into the repo at `docs/papers/literature-review.html`, built to the HTML
      deliverable standard (`~/hub/knowledge/html-deliverable-standard.md`): self-explanatory standing
      alone (spell out every abbreviation at first use, define internal labels like Arm A/B in place),
      minimalist + expand-for-depth, neutral definitions, professional grammar. Structure it so EVERY
      methodological decision and control step is explicit and checkable (decision → control it
      enforces → backing evidence + tier), plus the coverage log from step 3. The reader must be able
      to approve or challenge each decision without reading raw markdown.
      - **Every cited source is a one-click link to the paper — the reader must be able to reach the
        literature from the review.** Do NOT embed full papers (copyright; blocked by Artifact CSP) —
        link out. Priority: (1) DOI `https://doi.org/…` (stable, preferred); (2) an **OA full-text**
        link (Europe PMC / PMC / bioRxiv) when one exists, badged "read free"; (3) PubMed / publisher
        page as fallback. Papers held in **EndNote** are noted as such (DOI + "in EndNote", since
        EndNote isn't web-linkable). Pair with the basis badge: `full-text` OA → "read it here";
        `abstract`-only → links to the abstract and stays hedged.
        - **Hide the URL — the citation text itself is the link.** Anchor the hyperlink on the
          paper title / citation marker (e.g. author-year) so it reads as clean prose; never print
          a raw `https://…` string. Links open in a new tab; being navigation not fetched content,
          they work in both the saved file and a published Artifact.
      - **Educational, layered — readable on the FIRST pass, not just to an expert.** Expert-terse
        framing is a failure mode: a novice hits a wall, however correct it is. So:
        (i) open with a jargon-free "Start here" overview — what the analysis asks and why it's hard;
        (ii) every decision/finding leads with a plain-language sentence, with the technical statement,
        control, and citations UNDERNEATH as a second layer;
        (iii) any term beyond the project glossary (`.record/CONTEXT.md`) gets a "Concepts, explained" entry
        (what it is + why it matters) in a glossary section; every first use in the body is a
        clickable in-page anchor (`<a href="#term-id">`) that jumps straight to that glossary
        paragraph, and each glossary entry has a "↩ back" anchor to return — self-contained, no
        external links;
        (iv) offer a plain-language-only reading mode so the same page serves first-time and expert.
        Mirror genuinely reusable terms into Obsidian `Concepts/`.
7. **CLOSE — ask the user for full text (batched, at the end). HARD GATE — a run does not complete
   silently.** Present one batched full-text request from `need-pdf.md` and the abstract-only tags,
   ranked and split:
   - **Should get** — anchor / T1 / method-defining papers grounded on abstract-only; the synthesis
     is weaker without them. For each: title, one-line why-it-matters, and where it stalled (paywall
     / off-VPN / no OA).
   - **Optional** — background / T3 where the abstract sufficed.
   The user drops PDFs into EndNote and says done → re-verify those, upgrade `basis: abstract` →
   `full-text`, and note the upgrade in the resolution log. Never present an abstract-only grounding of
   a method-defining paper as settled without having asked.
   - **`need-pdf.md` is a REQUIRED artifact** (same standing as the step-3 coverage log): the run is
     INCOMPLETE until it exists in `docs/papers/sources/` AND the ranked ask has been shown to the user. If
     every source reached full text, still write it saying so (empty request + the basis tally) —
     never omit the file, because a missing `need-pdf.md` is indistinguishable from "we forgot to
     ask", which is exactly the gap this closes. It carries a dated **resolution log** tracking each
     `abstract → full-text` upgrade across re-runs.
8. **Active recall — hard gate, applies to both modes.** Reading a synthesis once does not make it
   stick. Before closing, ask 2-3 questions back about the "What we learned" narrative (6a) and any
   new `Concepts/` notes — answered from memory, not by rereading what was just written (e.g. "what
   did paper X actually define, and why does it matter for us" rather than "does this look right").
   This is the retention step; a session nobody is quizzed on gets read once and forgotten. Skip only
   if the user explicitly asks for a fast pass with no quiz.

## Efficiency
- Do heavy reading in sub-agents (read-big-return-small) so the main context stays lean.
- Use fully-qualified MCP tool names (e.g. `PubMed:search_articles`, `Consensus:...`).

Full context: `~/hub/design.md` (literature skill; source tiering; full-text cascade; token economy).
