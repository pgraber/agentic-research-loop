---
name: decide
description: Logs a settled decision to the correct decisions log — the hub for strategic or cross-project calls, the project for analysis calls — dated from the system clock and committed. Use whenever a non-obvious decision is made: a threshold, a dropped sample, a change of direction, or a priority. The conversation is never the record.
---

# Decide — write it down so it doesn't evaporate

A decision isn't real until it's written to a human-owned file and committed. This makes that one
step. Human-triggered — the user decides what counts as a decision.

## Do
1. **Pick the tier**
   - Strategic / cross-project / portfolio → `~/hub/decisions.md`
   - Analysis decision → the project's `docs/.record/decisions.md`
2. **Append a dated one-liner** under the date header. Get the date from the system clock
   (`date`) — NEVER hand-type it (a wrong date is worse than none).
   Example: `- FDR 0.05 not 0.1 — matched brief refs [<commit>]`
   - **In-flux vs settled:** while a decision is still changing within a session, AMEND the
     existing dated entry (mark it) rather than appending a fresh 'settled' line each pass. Append a
     new superseding entry only for a genuine reversal — keep real history, never rewrite it away.
3. **Commit** — the record rides with the code change it explains (same commit). For a pure
   decision with no code, commit the log-line change itself. Use `[phase] decision` message style.
4. **Heavyweight** (hard-to-reverse, real trade-off) → also write an ADR and link it from the log.

Git owns the authoritative timestamp; the date header is human-readable convenience. See
`~/hub/design.md` (decision discipline; timestamps).
