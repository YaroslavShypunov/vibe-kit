# History access

## Resolve identity before reading

Use the host's session metadata tools when available, such as
`get_session` and `list_sessions_and_chats`. A project/app session ID, local
Copilot history ID, cloud history ID, and subagent ID can be different
identifiers. Confirm a mapping through metadata; do not assume equality.

Use only tools actually exposed by the host. Discover deferred tool schemas
before calling them. If access fails, surface the failure and use another
authorized source or ask for an export; never bypass permissions.

If several tasks share a session, cover the whole accessible history but
separate their evidence. Ask which task to emphasize only if that choice
materially affects the review. Do not blame later requirement changes on an
earlier implementation.

## Local Copilot history

Verified local sources include:

- `~/.copilot/session-state/<local-session-id>/workspace.yaml`: identity and
  working-directory metadata.
- `~/.copilot/session-state/<local-session-id>/events.jsonl`: event history.

After confirming the local ID, use the bundled read-only Python reader:

```bash
python3 "<skill-directory>/scripts/read_session_history.py" "<local-session-id>" --mode index
python3 "<skill-directory>/scripts/read_session_history.py" "<local-session-id>" --mode page --start-line 1
python3 "<skill-directory>/scripts/read_session_history.py" "<local-session-id>" --mode event --event-line 42 --detail-offset 0
```

Replace placeholders with confirmed values. Do not run a placeholder command.
No dependencies beyond Python 3 are needed.

- `index` scans the file and reports event counts, actor counts, timestamps,
  duplicate IDs, and event types not exposed for analysis.
- `page` returns previews with source line numbers. Follow `next_start_line`
  until it is null. A preview is not a complete detail read.
- `event` pages the projected details of one source line. Follow
  `next_detail_offset` until it is null when complete details are needed.
- `--maximum-events` changes page size; `--maximum-characters` changes preview
  or detail size. Both must be positive.

Expand truncated substantive user/assistant messages before considering them
reviewed. For long tool output, inspect the task-relevant diagnostics and
artifacts; do not infer a complete result from a clipped preview.

The reader omits system/developer messages, hidden reasoning fields,
encrypted content, hook input, and full skill instructions. It is not a
secret detector: ordinary messages, commands, and tool results can still
contain private information. Do not quote or persist sensitive content.

Nested agent events may already be in the parent file under `agentId`.
Attribute them correctly instead of reading and counting the same work twice.
Check linked child histories only where their evidence is missing or needed.
The reader's event/actor counts are not token or cost measurements.

Unrecognized event types are listed in the index, not silently treated as
reviewed. Investigate a task-relevant unknown type safely through supported
tools without printing protected fields. A malformed record is an explicit
error. If history is still being written, use a stable authorized export or
record the review cutoff rather than claiming task completion.

## Native history tools

When `session_store_sql` is available, prefer exact session predicates.
Read ordered pages with explicit selected columns and `LIMIT`; do not issue
unbounded searches or load unrelated sessions. Read the exposed schema before
using it. Example for a confirmed history ID:

```sql
SELECT turn_index, user_message, assistant_response, timestamp
FROM turns
WHERE session_id = '<confirmed-history-id>'
  AND turn_index > <last-reviewed-turn-index>
ORDER BY turn_index
LIMIT 20
```

Use the appropriate local or cloud source. Conversation turns may omit tool
arguments/results, approvals, or child messages; they are not automatically
equivalent to complete event history. Checkpoints help navigation but do not
replace accessible substantive history.

Cloud views may expose `session_usage`, `tool_executions`, `session_files`,
and `session_refs`. Tool request/result data may require separately supported
sources. Local stores have a different schema and may not expose the same
usage or execution tables. Do not guess local usage columns or circumvent a
rejected query. Mark unavailable measurements explicitly.

Whole-session usage rows can be cumulative. Identify the included agents and
models, preserve reported units, and avoid counting parent/child totals twice.
Recorded billing multipliers or premium requests are not dollar amounts.

## Code and validation evidence

Use the task's recorded edits, commits, pull request, or worktree to identify
the relevant diff. Respect the actual base and repo conventions.

Read only task-related changes and recorded checks. Do not assume today's
working tree equals the delivered snapshot or attribute all dirty files to
the target session. When a worktree has been removed or changed afterward,
state the limitation.

Do not run tests, builds, installs, generators, or formatters during review.
Distinguish recorded passing checks, missing checks, outdated checks, and
actual user acceptance. A check before the final relevant edit is not fresh
evidence for that edit.

The tool execution `success` flag is not proof that a test or build passed.
Inspect the recorded exit code and result; a tool can successfully return
output describing a failed check.

For inaccessible cloud/remote sessions, ask for an authorized history export
and relevant diff/check results when needed. Review the available subset
honestly; never report missing records as successful work.
