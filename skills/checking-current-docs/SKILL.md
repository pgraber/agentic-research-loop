---
name: checking-current-docs
description: Fetches and verifies current official documentation for a tool, package, or coding practice before syntax is written — official sources over blogs, matched to the installed version, and cited. Use before writing Quarto, Nextflow, R, Python, or other tool syntax, when unsure of an API, or when the user asks for current best practice. Runs in a sub-agent to keep context small and caches findings.
---

# Checking current docs — verify before writing syntax

Standing rule (from global CLAUDE.md): never trust training-data syntax for external tools; fetch
and verify current official docs first. This skill does that consistently and cheaply.

## Workflow
1. **Check the cache first** — read `~/hub/knowledge/tools.md`. **Reuse (skip the fetch) only if
   BOTH hold:** (a) `last_checked` is within **90 days** of today, AND (b) the pinned version still
   matches the project lockfile/container. Otherwise RE-VERIFY (steps 2–5) and update the entry.
   This is the token-saver AND the freshness guarantee — a cached pin is trusted for 90 days or until
   the installed version moves, whichever comes first; never indefinitely.
   - **Mandatory trigger points** (so it always runs at least once per tool per project): the `design`
     tool-screening step, and `build` before writing any syntax for a tool not already fresh in cache.
     A version bump in the lockfile invalidates that tool's entry immediately.
2. **Fetch official docs** — WebSearch for the official source (docs site, package docs, or the
   Microsoft Learn MCP for Microsoft/Azure); WebFetch it. Prefer official docs over blogs/forums.
3. **Match the version** — verify the doc matches the installed/pinned version (check the lockfile
   or container). Syntax differs across versions.
4. **Return the minimal answer + citation** — the exact snippet needed, with the source URL.
5. **Cache it** — save to `~/hub/knowledge/tools.md`: tool · version · one-line usage · docs URL ·
   `last_checked` date (from the system clock).

## Efficiency
- Do the heavy reading in a **sub-agent** (read-big-return-small): the sub-agent fetches and reads;
  it returns only the verified snippet, keeping the main context lean.
- For MCP tools, use fully-qualified names (e.g. `Microsoft_Learn:microsoft_docs_search`).

Never guess or construct URLs — navigate from a known official root and verify.
