# Portable dispatch and completion contract

Read [builder.md](../agents/builder.md), [reviewer.md](../agents/reviewer.md) and
[review.md](review.md) before dispatch. These Markdown roles are canonical across
harnesses. Native agent profiles are generated adapters, not separate role designs.

## Preflight

Resolve required skill dependencies using [skills.md](skills.md). Supply exact
paths instead of assuming another agent or harness inherits the skill catalog.

Identify the current harness and version. Read [harnesses.md](harnesses.md) for its
adapter and verify the two installed profiles match the Markdown, role names,
descriptions and user-selected model/effort binding. Check effective configuration
precedence, including project profiles, settings and per-call overrides. Do not
assume a file on disk proves that the harness loaded it.

Confirm that the available delegation mechanism can launch both named roles in
separate contexts. Missing roles, unsupported required model settings or unavailable
delegation mean BLOCKED. Never substitute generic agents, inherited models or main
thread implementation without an explicit user-requested workflow change. The main
session coordinates and maintains the brief/status; it does not write mockup code
or perform the independent review. Role/config updates are setup operations, not
implicit repairs during a mockup run.

## Assignment packets

Select `loop-generate-mockup-builder`, then `loop-generate-mockup-reviewer` using
the harness's native delegation mechanism. Use fresh contexts with explicit input
packets (Codex: `fork_turns="none"`); do not inherit the whole conversation.
The agreed default profile is OpenAI GPT-5.6 Terra with high reasoning. Translate
that into the actual provider/model identifier supported by the harness, after
checking its catalog. Do not invent model IDs or assume a provider supports that
effort. If unavailable, request an explicit alternative; no silent substitution.

Each packet supplies:

- the complete compact brief, numbered requirements and authoritative paths;
- allowed writes, evidence directory, live workspace state and unrelated changes;
- selected guidance files with pinned revision/hashes;
- assigned skill paths with versions/hashes, lookup questions if any, and the
  references/skills.md conflict policy;
- platform, viewports, journeys/states and known simulation boundaries;
- exact role Markdown and review.md/handoff.md paths;
- the task and expected return, without replacing or contradicting role rules.

The reviewer also needs the actual URL, artifact paths, revision identity and
simulation limits. Builder claims remain unverified. Run roles sequentially.
Reuse their contexts for repairs where supported; otherwise create a replacement
of the same named role with the prior findings and state, record the replacement,
and retain the same repair counter. Never reset budgets by replacing an agent.

## Evidence of delegation

Retain actual tool/process-returned agent or session IDs and completed returns.
Before acceptance, require distinct builder and reviewer contexts plus a reviewer
return for the final mockup revision with actual browser evidence. The coordinator
must not impersonate a return or fill a missing review itself.

Record a compact execution summary in design-brief.md: harness/version, role,
agent/session ID, configured model/effort, profile-check result, review revision,
verdict and round. Compare exposed runtime metadata with configured settings and
stop on mismatches. If runtime identity is not exposed, mark it unverified; an
agent's self-report does not verify its model. Do not invent IDs or claim a model
pin is runtime verification. Missing/failed dispatch or review means BLOCKED.

Markdown guides the model and native profiles constrain its configuration, but
neither guarantees that the coordinator executes every step. A host-enforced
guarantee requires an external deterministic runner that launches stages and
validates trusted events. This skill does not implement such a runner, and its
execution record is not an immutable audit trail.
