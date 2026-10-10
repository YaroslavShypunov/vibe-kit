# Failure Routing and Repair

Route by evidence:

| Failure | Owner |
|---|---|
| Ambiguous behavior, changed scope, or unsupported assumption | User through contract revision |
| Wrong package, caller, architecture layer, reuse choice, or test seam | Repository Scout |
| Production behavior defect | Production Coder |
| Invalid oracle, weak assertion, fixture, or test-only defect | Test Engineer that wrote the test (`RED` or `HARDEN`) |
| `TEST_DISPUTE` from the coder | Same `RED` agent, from the contract only; the user if still disputed |
| Changed frozen RED test | Restore with `red-tests.sh restore`; repair to the coder |
| `red-tests.sh extend` rejects an edited RED line | Same `HARDEN` agent: undo that edit and put the case in a new file |
| `PRE_EXISTING` baseline failure | Not a repair; record it, and resolve it in the contract if it blocks an `AC-*` |
| Missing or stale command evidence | Missing verification step |
| Security, API, process, data, numerical, unit, or domain concern | Applicable specialist and human owner |
| Environment, tooling, or ambiguous repeated failure | Diagnostician |

Do not treat model majority as stronger than current bytes, command output, or a
human-owned product decision.

Only a failing gate or a reviewer `BLOCKER` starts a repair. `NOTE` findings are
reported to the user and never repaired automatically. Send each repair as a
delta (finding, evidence, allowed paths, checks to rerun) to the owner agent
that made the change with `write_agent`, when the Build skill's **Agent reuse**
rules allow it.

`PRE_EXISTING` failures and `TEST_DISPUTE` decisions are not failed cycles.
Allow one normal focused repair. If the same normalized failure remains after
that repair, invoke the read-only Diagnostician before another edit. Permit at
most two completed failed repair cycles for one task. Count a failed cycle only
after a finding is repaired and its next applicable gate still fails.

Keep a repair ledger in the active Task Capsule with normalized signature,
repair owner, repair result, next gate, and failed-cycle count. After the
second failed cycle, stop all edits and repair delegation and ask the user for
direction. Do not start a third repair.

A contract gap is not repaired as code. The coder must not weaken an
independent test. Non-blocking suggestions do not trigger automatic cleanup.
An impossible objective/allowed-path mismatch returns `CONTRACT_GAP`; never
force an edit into a known-wrong approved path. Material expansion needs reapproval.
When reviewers disagree and no executable discriminator exists, ask the human
owner instead of adding reviewers until a majority appears.
