# Templates

`project/` — the canonical **analysis-project** structure (minimal, gold-standard: Wilson *Good
Enough Practices* 2017, Noble 2009, Marwick compendium 2018). Single source of truth for project
layout: `new-project` copies it; `adopt-project` fills missing pieces against it. Change the
structure HERE, once — both skills follow.

Analysis projects only. Pipelines reused across projects are separate versioned repos; a
project-specific pipeline lives in the project's agnostic `workflow/` subdir.
