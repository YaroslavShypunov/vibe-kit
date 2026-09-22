# Build Risk Profiles

Risk follows concrete affected behavior and boundaries, not file labels. Judgment
may raise but never lower genuine protected risks. Resolve or escalate boundary uncertainty.

Classify the planned change before approval:

- no production behavior change is required for `L0`;
- any observable production behavior change is at least `L1`;
- shared state, nontrivial cross-module/package data flow, or material ownership
  unknowns require `L2`; and
- actual changes to auth/trust, public/shared contracts, migration/persistence/
  serialization compatibility, process/command/filesystem/network permissions or
  access mechanisms, dependency/build/CI execution, concurrency, or numerical
  engineering units/precision require `L3`.

A config filename, bug fix, or passing previously validated data through an existing
API alone does not imply L3/L2. A deterministic setting value can be L1 with a
reliable seam and no higher trigger; config work has no blanket exemption.

Record the exact planned paths, change types, expected production file count,
expected line range, and the trigger that sets the floor in the approved
contract.

| Level | Typical surface | Required workflow |
|---|---|---|
| `L0` | Nonbehavioral documentation, metadata, or test-only correction. | Inline change and relevant mechanical check. |
| `L1` | Known bounded local fix or deterministic setting value; reliable seam, no higher trigger. | Discovery if uncertain, approved contract, one writer, maker checks, applicable hardening, rerun affected checks, fresh final review, traceability. |
| `L2` | Shared state, nontrivial cross-module/package flow, material ownership unknowns. | L1 plus pre-approval Scout, frozen pre-patch CHARTER, fresh HARDEN author context, and final review covering material test deltas. |
| `L3` | Actual protected changes listed above. | L2 plus applicable specialist and explicit human approval before completion; ask before changing protected/shared contracts. |

One fresh final reviewer may provide separately labeled production and material
test-delta verdicts after the latest production AND test edits. An inapplicable
hardening/specialist gate needs approved concrete N/A rationale and sufficient
alternative evidence, never a ceremonial empty-scope task.

Size assessment:

- more than three production files or roughly 150 changed production lines prompts
  explicit impact/scope assessment, not automatic escalation;
- more than eight production files or roughly 400 changed production lines
  requires splitting the task or explicit user approval; and
- unrelated cleanup or refactoring requires a separate contract.

Repository instructions may define stricter triggers. A small diff does not
lower API, security, data, process, or engineering risk.

Reclassify before crossing a new trigger. Stop before the next edit, raise the
floor, add the required gates, and reapprove the contract. Do not cross into
`L2`/`L3` implementation before freezing the Test Charter. If an unexpected
escalation is discovered after a patch exists, derive the charter from the
approved contract and pre-change baseline without exposing the patch, then
reapprove before further edits.
