#!/usr/bin/env bash
# Freeze and guard independent RED test files for /build.
#
# Usage:
#   red-tests.sh freeze   <repository-root> <session-folder> <path>...  first freeze of RED files
#   red-tests.sh refreeze <repository-root> <session-folder> [path...]  RED updated or added its own files
#   red-tests.sh extend   <repository-root> <session-folder> [path...]  HARDEN: additions only, plus new files
#   red-tests.sh check    <repository-root> <session-folder>
#   red-tests.sh restore  <repository-root> <session-folder>
#
# Paths are relative to the repository root. `refreeze` re-hashes every frozen
# file that still exists plus the given paths. `refreeze` and `extend` keep the
# previous snapshot in files/build/red.previous.
set -euo pipefail

usage() {
  sed -n '2,13p' "$0" >&2
  exit 2
}

[[ $# -ge 3 ]] || usage
action="$1"
repository_root="$2"
session_folder="$3"
shift 3

[[ -d "$repository_root" ]] || { echo "repository root not found: $repository_root" >&2; exit 2; }
[[ -d "$session_folder" ]] || { echo "session folder not found: $session_folder" >&2; exit 2; }

state_folder="$session_folder/files/build/red"
snapshot_folder="$state_folder/snapshot"
manifest="$state_folder/manifest.sha256"

validate_paths() {
  for test_path in "$@"; do
    if [[ "$test_path" == /* || "$test_path" == ../* || "$test_path" == */../* ]]; then
      echo "use a path relative to the repository root without '..': $test_path" >&2
      exit 2
    fi
    [[ -f "$repository_root/$test_path" ]] || { echo "not a file: $test_path" >&2; exit 2; }
  done
}

read_manifest_paths() {
  frozen_paths=()
  while IFS= read -r line; do
    frozen_paths+=("${line:66}")
  done < "$manifest"
}

write_snapshot() {
  [[ $# -ge 1 ]] || { echo "nothing to freeze" >&2; exit 2; }
  local staging_folder="$state_folder.staging.$$"
  rm -rf "$staging_folder"
  mkdir -p "$staging_folder/snapshot"
  for test_path in "$@"; do
    mkdir -p "$staging_folder/snapshot/$(dirname "$test_path")"
    cp -p "$repository_root/$test_path" "$staging_folder/snapshot/$test_path"
  done
  (cd "$repository_root" && shasum -a 256 -- "$@") > "$staging_folder/manifest.sha256"
  if [[ -d "$state_folder" ]]; then
    rm -rf "$state_folder.previous"
    mv "$state_folder" "$state_folder.previous"
  fi
  mv "$staging_folder" "$state_folder"
  echo "RED_TESTS_FROZEN ($# files) -> $manifest"
}

check_manifest() {
  [[ -f "$manifest" ]] || { echo "no frozen RED tests: run freeze first" >&2; exit 2; }
  if (cd "$repository_root" && shasum -a 256 -c --quiet "$manifest"); then
    echo "RED_TESTS_UNCHANGED ($(wc -l < "$manifest" | tr -d ' ') files)"
  else
    echo "RED_TESTS_CHANGED"
    return 1
  fi
}

case "$action" in
  freeze)
    [[ $# -ge 1 ]] || usage
    [[ ! -f "$manifest" ]] || { echo "already frozen: use refreeze for RED updates or extend for HARDEN" >&2; exit 2; }
    validate_paths "$@"
    write_snapshot "$@"
    ;;
  refreeze)
    [[ -f "$manifest" ]] || { echo "no frozen RED tests: run freeze first" >&2; exit 2; }
    validate_paths "$@"
    read_manifest_paths
    kept_paths=()
    for frozen_path in "${frozen_paths[@]}"; do
      if [[ -f "$repository_root/$frozen_path" ]]; then
        is_repeated=0
        for new_path in "$@"; do
          [[ "$new_path" != "$frozen_path" ]] || is_repeated=1
        done
        [[ "$is_repeated" == "1" ]] || kept_paths+=("$frozen_path")
      else
        echo "RED_FILE_DROPPED: $frozen_path"
      fi
    done
    write_snapshot ${kept_paths[@]+"${kept_paths[@]}"} "$@"
    ;;
  extend)
    [[ -f "$manifest" ]] || { echo "no frozen RED tests: run freeze first" >&2; exit 2; }
    validate_paths "$@"
    read_manifest_paths
    for new_path in "$@"; do
      for frozen_path in "${frozen_paths[@]}"; do
        [[ "$new_path" != "$frozen_path" ]] || { echo "already frozen: $new_path" >&2; exit 2; }
      done
    done
    changed_assertions=0
    for frozen_path in "${frozen_paths[@]}"; do
      if [[ ! -f "$repository_root/$frozen_path" ]]; then
        echo "RED_FILE_MISSING: $frozen_path"
        changed_assertions=1
        continue
      fi
      removed_lines=$(diff "$snapshot_folder/$frozen_path" "$repository_root/$frozen_path" | grep -c '^<' || true)
      if [[ "$removed_lines" != "0" ]]; then
        echo "RED_LINES_CHANGED: $frozen_path ($removed_lines lines removed or edited)"
        changed_assertions=1
      fi
    done
    [[ "$changed_assertions" == "0" ]] || { echo "RED_TESTS_CHANGED"; exit 1; }
    write_snapshot "${frozen_paths[@]}" "$@"
    ;;
  check)
    check_manifest
    ;;
  restore)
    [[ -d "$snapshot_folder" ]] || { echo "no snapshot: run freeze first" >&2; exit 2; }
    cp -Rp "$snapshot_folder/." "$repository_root/"
    check_manifest
    ;;
  *)
    usage
    ;;
esac
