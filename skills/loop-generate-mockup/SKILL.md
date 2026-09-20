---
name: loop-generate-mockup
description: Create or revise interactive HTML design mockups from requirements and project design context, with an independent rendered UI/UX review and bounded refinement. Produces a temporary mockup and concise implementation brief. Use for design exploration and pre-implementation mockups, not production implementation or audits of an existing application.
---

# Generate Mockup Loop

Create a coherent, task-appropriate design that another session can implement.
The main session coordinates one builder and one independent reviewer. Keep the
workflow portable: discover project instructions, platforms, paths, and design
conventions rather than assuming a particular repository or mobile-only layout.

## 1. Establish the brief

Read applicable repository instructions, the active requirements, and the
project's authoritative design documents. Honour required task preparation;
this workflow does not bypass project decision gates or authorize production
implementation. Inspect existing tokens/components and a few representative
rendered screens when available. Preserve unrelated work.

Agree the bounded journey or screen set. Reuse the current conversation's
decisions. Ask only about missing choices that materially affect the result;
resolve ordinary design details yourself. Do not silently invent product rules,
business outcomes, evidence, or backend capabilities.

Prepare a compact brief with:

- user goal, audience, numbered requirements, primary action and content hierarchy;
- platform, target viewports, relevant input methods, required states and journeys;
- authoritative project paths and representative visual references;
- existing tokens/components to reuse, or a small proposed visual foundation for
  a new project; label new conventions provisional until accepted;
- relevant UI/UX guidance selected through [references/guidance.md](references/guidance.md);
- resolved skill paths and versions/hashes using [references/skills.md](references/skills.md):
  frontend-design for the builder, web-design-guidelines for the reviewer, and
  ui-ux-pro-max only for a named unresolved design question;
- exact output directory, allowed writes, browser evidence directory and server plan;
- review scope and budget: one initial review and at most two repair/review rounds.

Choose task-local disposable storage consistent with the repository, otherwise
`output/mockups/<task-slug>/`. Do not overwrite an unrelated existing directory.
Default output is `index.html`, `design-brief.md`, and local assets only as needed.
Keep browser evidence under that task's output directory. Cover a connected
journey together when transitions are important; split large work into explicitly
bounded batches instead of enforcing one page regardless of the task.

## 2. Dispatch two agents

Use two named roles with canonical, harness-independent Markdown instructions:

- `loop-generate-mockup-builder`: [agents/builder.md](agents/builder.md).
- `loop-generate-mockup-reviewer`: [agents/reviewer.md](agents/reviewer.md).

Read
[references/assignments.md](references/assignments.md) and
[references/review.md](references/review.md), then perform the harness-specific
preflight in [references/harnesses.md](references/harnesses.md). Default both roles
to OpenAI GPT-5.6 Terra with high reasoning through the harness's actual supported
model identifiers. Explicit user model choices override these defaults through
declared bindings, never accidental inheritance or silent fallback. Missing roles,
unsupported settings or unavailable delegation mean BLOCKED. The main session
retains its current model and coordinates only; it does not build the mockup or
replace the reviewer. Use separate agent contexts with explicit assignment packets.

Run the builder then reviewer sequentially. Reuse both agent threads for repairs
where supported; follow assignments.md when the harness requires a replacement.
Do not spawn an agent for each stage or allow agents to spawn successors. Escalate
to a stronger model only when the user requests it or authorizes a proposed
escalation after a concrete unresolved problem; do not silently increase cost.
Record actual dispatch IDs and completed returns; a profile file alone is not
evidence that an agent ran.

## 3. Build and self-check

Give the builder its concrete packet from `assignments.md`. It owns the mockup,
assets and draft brief, not application code or canonical project documents.
The same builder establishes direction, builds, and refines. Use one deliberate
direction by default; alternatives are optional when requested or when a material
choice warrants them.

Require a running, interactive mockup, realistic synthetic content and reachable
required states. The builder renders and inspects it, checks its primary journey,
and returns the actual files, URL, evidence and limitations. Do not route a
known-broken initial build to review to save a basic self-check.

## 4. Review and repair

The reviewer is read-only for the mockup and design documents. It receives the
same brief, relevant source paths, artifact paths and known simulation limits.
Builder claims are unverified. It inspects rendered screenshots and exercises
interactions using fresh browser state; source inspection alone cannot pass.
Use the verdicts and evidence requirements in `review.md`.

- `ACCEPT`: all in-scope requirements checked, no required finding or material
  unknown remains. Optional suggestions may remain.
- `REVISE`: pass consolidated, evidence-backed findings to the same builder;
  then rerun affected journeys and check regressions with the same reviewer.
- `BLOCKED`: a required prerequisite or product decision is missing. Report the
  exact gap and request only what is needed; do not invent acceptance.

The initial build/review is round 0. Repairs are rounds 1 and 2. If round 2 still
fails, stop with `NEEDS_DECISION`, remaining findings and attempted fixes. Do not
reset the budget by spawning new agents. Avoid scoring aesthetics numerically
or blocking on a reviewer's unsupported stylistic preference. An edit after
acceptance invalidates the affected review evidence.

## 5. Handoff and disposable-artifact lifecycle

The builder maintains `design-brief.md` using
[references/handoff.md](references/handoff.md). The coordinator finalizes the
review status without changing the accepted mockup. Deliver a clickable entry
file, brief, acceptance status, evidence summary and any limitations. Include a
working preview command/URL; retain the mockup for implementation and subsequent
UI review. Do not launch development or change `develop-loop` as part of this skill.

Before completion, enforce the two-context completion checks in assignments.md.
Distinguish configured model settings from runtime-verified metadata.

Mockups are disposable after task implementation and any review that needs them.
Do not delete them automatically. Durable decisions must not have a temporary
HTML file as their only source. In the handoff, name the project-owned destination
for decisions worth retaining, such as its design system or task record. Promote
accepted decisions there when authorized and required by project instructions;
otherwise provide a concise carry-forward section for the implementation session.
Do not turn provisional styling into an approved project-wide design system.

## Cost discipline

Load only relevant guidance and source excerpts; do not pass full conversation
history or an entire wiki to every agent. Keep initial viewports representative
of the actual platform and breakpoints, then test additional ones when a failure
or requirement justifies it. Consolidate review findings; recheck affected states
plus a short main-journey regression after repairs. Avoid repeated broad web
research, competing designs, generated imagery, large frameworks and extra
reports unless they materially serve the brief. Never skip required checks to
claim a cheaper pass. Report known usage if available; do not invent costs.
