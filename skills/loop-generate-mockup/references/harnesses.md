# Harness adapters

The workflow and agents/builder.md + agents/reviewer.md are harness-independent.
Distribute the whole skill directory; do not distribute a lone role without its
review/handoff references. Native wrappers embed the canonical role body and pin
model configuration. Re-export after editing a role, and check for drift.

Use Python 3.11+ and `scripts/export_agents.py` from the installed skill directory.
It writes only the two named profiles, refuses unmanaged overwrites and supports
`--check` to compare profiles without changing them. It does not install the skill
into another harness, verify model availability, launch agents, configure browser
tools, or prove runtime model identity. Check these in the target harness before
a real run. Keep the exported profile's skill reference path accessible there.

## Codex

Personal agents are standalone TOML under the actual CODEX_HOME/agents directory
(normally ~/.codex/agents). Export with `--harness codex --model gpt-5.6-terra
--effort high --output <agents-directory>`. Use `--write` during setup or `--check`
during preflight. Spawn the exact custom agent types with fork_turns="none" and
omit model/effort overrides. Start a fresh session if roles have not been loaded.

The configuration pins `model` and `model_reasoning_effort`; instructions are
embedded as developer_instructions. Workspace-write supports browser artifacts;
reviewer source ownership remains an instruction, not a filesystem guarantee.

Source: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## GitHub Copilot CLI

Profiles use .agent.md files with YAML frontmatter in ~/.copilot/agents or a
project's .github/agents. Export with `--harness copilot --model <catalog-id>
--effort high --output <agents-directory>`. Select an identifier actually available
in that Copilot installation. The wrapper sets `model`, `reasoningEffort` and
`modelPolicy: required` to reject unauthored model substitutions in supporting CLI
versions. Verify the installed version supports that policy; do not silently drop it.

Check effective per-call/user settings and reasoning effort before dispatch. The
CLI documents special model inheritance under Auto session selection; use a fixed
session model or verify that the required policy is honoured before proceeding.
Restart/reload as required. Explicitly delegate to
the named agent; selecting it as the main interactive agent is not the independent
two-context workflow. Browser tools must be available to the reviewer.

Sources: [CLI custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli),
[CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).

## OpenCode

Check the installed major version. Classic and V2 schemas differ; the exporter
requires either `--harness opencode` or `--harness opencode-v2` explicitly.
Use `--model <provider/model>` from the actual catalog and `--effort high`.

Classic: Markdown profiles under ~/.config/opencode/agents or .opencode/agents
set `mode: subagent`, model and provider-specific `reasoningEffort`. This exporter
assumes an OpenAI-compatible reasoningEffort option; use it only when the chosen
provider documents support.

V2: Markdown profiles set `mode: subagent` and `model: provider/model#high`.
Verify that a high variant is defined for the selected model. Do not assume that
V2 accepts classic provider-option fields. Choose the profile directory documented
by the installed version. Use native task delegation, not a primary-agent switch.

Sources: [Classic agents](https://opencode.ai/docs/agents/),
[V2 agents](https://opencode.ai/v2/docs/agents).

## Other harnesses

Map the same role bodies, fixed role names and user-approved model/effort bindings
to that harness's documented profile format. Verify separate contexts, browser
access and completed return IDs. There is no universal agent-profile format or
universal delegation tool name. If the mapping cannot preserve the contract,
report the specific unsupported capability instead of guessing syntax or silently
weakening the loop. Do not auto-install profiles into unrelated applications.
