<!-- user-owned-workflows:start -->
# USER-OWNED Manual Workflow Policy

This manual-only policy applies only to `/build`, `/design`, `/analyze`,
`/review`, `/pr-ready`, `/threat-model`, `/wiki`, and `/orchestrator`
and their workflow-specific delegation.
Unrelated skills and agents retain normal host selection behavior.

Do not invoke, select, imitate, or delegate to these workflows or their
workflow-specific skills or agents merely
because a normal-language request resembles implementation, planning, review,
analysis, security work, PR preparation, or wiki work.

Use one of these workflows only after the user explicitly enters its slash command.

When a user explicitly invokes one of those commands, follow only that
workflow. `/orchestrator` is a manual router and may route the explicit request
to one other listed manual workflow when needed.

For ordinary prompts, use normal host behavior. Do not reproduce these
workflows' multi-role loops, Build Contracts, review gates, or repair policies
unless the user explicitly invoked that workflow.

Normal work never modifies `.wiki` unless the user explicitly invokes
`/wiki init` or `/wiki reinit`.

Invoke these workflows only with their explicit slash commands; use `/skills` for discovery and `/agent` for custom-agent selection.
<!-- user-owned-workflows:end -->

<!-- user-build-models:start -->
# /build role model dispatch

For `/build`, native `~/.copilot/settings.json` → `subagents.agents` is the sole
role model/effort mapping. Omit per-call model/effort arguments and let the host
use configured defaults unless the user explicitly requests an override.
If a required configured model is unavailable, return `MODEL_UNAVAILABLE`;
never intentionally substitute. Never ask the user for permission to use a
configured role model; the runtime applies it. Other roles keep their
configured defaults.
This prompt policy is not technical dispatch enforcement.
<!-- user-build-models:end -->
