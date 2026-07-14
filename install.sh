#!/usr/bin/env bash
# Symlink each skill into ~/.claude/skills so Claude Code loads it.
# Idempotent: safe to re-run. Skips real dirs that aren't ours (won't clobber).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude/skills"
mkdir -p "$DEST"
for skill in "$DIR"/skills/*/; do
  name="$(basename "$skill")"
  target="$DEST/$name"
  if [[ -e "$target" && ! -L "$target" ]]; then
    echo "skip $name (a real dir already exists at $target)"
    continue
  fi
  ln -sfn "$skill" "$target"
  echo "linked $name"
done
echo "done. Claude Code will load these from ~/.claude/skills."
