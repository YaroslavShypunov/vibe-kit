#!/bin/bash
# Link skills/agents/loops from this repo into local tool paths.
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
targets=("$HOME/.agents/skills" "$HOME/.codex/skills")
mkdir -p "${targets[@]}"
for src in "$KIT"/skills/*/; do
  [ -d "$src" ] || continue
  name="$(basename "$src")"
  for t in "${targets[@]}"; do
    dest="$t/$name"
    if [ -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "skip $name -> $dest exists as a real directory (remove or replace manually)"
      continue
    fi
    ln -sfn "$src" "$dest"
    echo "linked $name -> $dest"
  done
done
echo "done. skills linked from $KIT/skills"
echo "agents/ and loops/ are plain markdown — copy or reference as needed."
