#!/usr/bin/env bash
# Writes one review packet: repository facts, status, full diff against HEAD,
# and new untracked files. Read-only for the repository.
# Usage: review-packet.sh <repository-root> <output-file> [paths relative to the root...]
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: review-packet.sh <repository-root> <output-file> [paths...]" >&2
  exit 64
fi

repository_input="$1"
output_file="$2"
shift 2

maximum_untracked_bytes=204800
warning_packet_bytes=409600

repository_root="$(git -C "$repository_input" rev-parse --show-toplevel)"
branch_name="$(git -C "$repository_root" branch --show-current)"
head_revision="$(git -C "$repository_root" rev-parse HEAD)"
branch_name="${branch_name:-DETACHED}"

# Disable repository-configured helpers so building the packet runs no repository code.
safe_git() {
  git -C "$repository_root" -c core.fsmonitor=false "$@"
}

path_arguments=(--)
if [ "$#" -gt 0 ]; then
  path_arguments+=("$@")
fi

mkdir -p "$(dirname "$output_file")"
# Keep scratch files outside the repository so they never appear in the packet.
temporary_file="$(mktemp "${TMPDIR:-/tmp}/review-packet.XXXXXX")"
untracked_list_file="$(mktemp "${TMPDIR:-/tmp}/review-packet-untracked.XXXXXX")"
trap 'rm -f "$temporary_file" "$untracked_list_file"' EXIT
safe_git ls-files --others --exclude-standard -z "${path_arguments[@]}" > "$untracked_list_file"

untracked_count=0
skipped_count=0
error_count=0
{
  echo "# Review packet"
  echo "Repository root: $repository_root"
  echo "Branch: $branch_name"
  echo "HEAD: $head_revision"
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if [ "$#" -gt 0 ]; then
    echo "Path filter: $*"
  else
    echo "Path filter: NONE (whole worktree)"
  fi
  echo "Rule: use only absolute paths under the repository root; never guess other locations."
  echo
  echo "## git status --short"
  safe_git status --short "${path_arguments[@]}"
  echo
  echo "## git diff --stat HEAD"
  safe_git diff --no-ext-diff --no-textconv --stat HEAD "${path_arguments[@]}"
  echo
  echo "## git diff HEAD"
  safe_git diff --no-ext-diff --no-textconv HEAD "${path_arguments[@]}"
  echo
  echo "## New untracked files"
} > "$temporary_file"

while IFS= read -r -d '' relative_path; do
  absolute_path="$repository_root/$relative_path"
  if [ ! -f "$absolute_path" ]; then
    continue
  fi
  file_bytes="$(wc -c < "$absolute_path" | tr -d ' ')"
  if [ "$file_bytes" -gt "$maximum_untracked_bytes" ]; then
    echo "SKIPPED (size ${file_bytes} bytes): $absolute_path" >> "$temporary_file"
    skipped_count=$((skipped_count + 1))
    continue
  fi
  # --no-index exits 1 when files differ; only a higher status is an error.
  set +e
  (cd "$repository_root" && git -c core.fsmonitor=false diff --no-ext-diff --no-textconv --no-index -- /dev/null "$relative_path") >> "$temporary_file"
  no_index_status=$?
  set -e
  if [ "$no_index_status" -gt 1 ]; then
    echo "ERROR (git status ${no_index_status}) reading: $absolute_path" >> "$temporary_file"
    error_count=$((error_count + 1))
    continue
  fi
  untracked_count=$((untracked_count + 1))
done < "$untracked_list_file"

if [ "$untracked_count" -eq 0 ] && [ "$skipped_count" -eq 0 ] && [ "$error_count" -eq 0 ]; then
  echo "NONE" >> "$temporary_file"
fi

mv "$temporary_file" "$output_file"
rm -f "$untracked_list_file"
trap - EXIT

packet_bytes="$(wc -c < "$output_file" | tr -d ' ')"
echo "Review packet: $output_file"
echo "Repository root: $repository_root | Branch: $branch_name | HEAD: $head_revision"
echo "Size: ${packet_bytes} bytes | New files: ${untracked_count} | Skipped large files: ${skipped_count} | Errors: ${error_count}"
if [ "$packet_bytes" -gt "$warning_packet_bytes" ]; then
  echo "WARNING: packet is large; pass the approved paths to narrow it." >&2
fi
if [ "$error_count" -gt 0 ]; then
  echo "ERROR: ${error_count} new file(s) could not be added; see the packet." >&2
  exit 1
fi
