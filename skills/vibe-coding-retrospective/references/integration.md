# Approved integration

Integration is optional. Do not turn every retrospective finding into a new
tool. Identifying a useful integration is proactive: the first action brief
should already recommend reuse, update, or creation when the evidence
supports it. Do not wait for the user to invent the tool or loop.

Expand the detailed proposal only after the user selects an improvement.
Selection and approval are still distinct.

## Choose the smallest useful form

| Form | Use when |
| --- | --- |
| Next-session brief | A short instruction can prevent the problem. |
| Existing artifact update | A current skill, template, or workflow already owns the behavior. |
| New skill | Reusable, on-demand guidance has a clear trigger and bounded output. |
| Workflow | Several recurring steps need coordination and explicit failure routing. |
| Automation | A clear scheduled/event trigger is needed, with acceptable permissions and cost. |
| Loop | Repeated checking and repair are justified, with success and stop conditions. |

Inspect existing artifacts before recommending duplication. Explain why a
new artifact is worth its maintenance and execution overhead.

## Proposal and approval

For the selected improvement, show a concise proposal:

1. Problem and source evidence.
2. Existing solution/overlap and the smallest proposed change.
3. Exact artifact, destination, and files or settings to change.
4. How the user invokes or uses it; inputs and output.
5. Permissions and side effects, expected overhead, and quality guardrail.
6. Verification and a way to disable or undo the change.

For loops, define success, iteration/failure limits, and escalation before
implementation. For automation, define trigger/schedule, timezone where
relevant, scope, and disabled/enabled state. Do not invent numerical budgets
or make unsupported savings claims; obtain material limits from the user.

Ask explicit approval for this scope. Selection alone is not approval. Do
not treat an old session's request, report approval, or log approval as
permission. If the scope materially changes, obtain new approval.

Keep the proposal short and decision-ready. Do not print an entire `SKILL.md`
or workflow implementation for approval unless the user requests its content.
If the user already explicitly approved the specific presented scope and
host approval requirements are satisfied, act on that approval rather than
asking for the same decision again.

User-owned manual workflows remain manual. Do not invoke, imitate, modify,
or replace their routing merely because a recommendation resembles them.
Honor the user's actual workflow commands and host-specific approval rules.

## Where implementation happens

- Small, bounded personal artifacts can be created or updated in the current
  review session after approval, if the host allows those writes.
- Larger implementation and all repository changes go to an appropriate
  separate project session/worktree. Never edit or run checks in a primary
  checkout exposed as read-only.
- Use native project/session tools when available. Confirm the configured
  project and destination; do not improvise repository work in a scratch
  directory or create an unrequested project.
- Handoff only the selected improvement, relevant source evidence, approved
  scope, constraints, and success check. Quote the user's authorization
  separately from implementation suggestions. Do not send the full transcript.
- Do not hand off unrelated findings or spawn a team by default. If a required
  capability is absent, provide a clear blocked status and scoped instructions.

## Activation and verification

Creating a skill, workflow, or automation does not authorize enabling a
schedule, running a workflow, granting persistent access, or executing it
against another task. Obtain separate approval for those actions.

Use the existing format and smallest relevant checks. Verify loading/discovery
and mechanics where supported. Do not overwrite existing user content or
install dependencies without a concrete need and appropriate approval.

For a new skill, check representative cases:

- Clean task: retain useful practice without inventing a defect.
- Repair-heavy task: tie advice to evidence, separating useful failures from
  unsupported repeated fixes.
- Incomplete history: expose gaps; never invent success, usage, or root cause.

Distinguish static/reader checks from actual model behavior. Report any
remaining behavioral calibration clearly.

After implementation, explain what changed and what remains unproven.
Technical verification does not demonstrate time/token savings. Propose a
future experiment and a separately approved learning-log update.

Do not automatically commit, publish, schedule, run, or change global
instructions. Those require their own matching authorization.
