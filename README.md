# vibe-kit

Personal toolkit for vibe coding: AI skills, agents, loops, prompts and snippets.

This repo contains portable copies of my GitHub Copilot CLI `/build` and
`/vibe-coding-retrospective` setup.
Keep the GitHub repository private if it contains private working instructions.

## Layout

- `skills/build/` - the active workflow, six references, and three helper scripts.
- `skills/vibe-coding-retrospective/` - session review guidance, four references, a history reader, and its tests.
- `agents/` - the six core build roles and the Sage, Browser QA, and UI Critic.
- `instructions/` - shared English, naming, testing, PR, Civil-iTwin Node, and code-mode rules.
- `settings/build-settings.json` - portable main-session and per-agent model settings.
- `settings/copilot-instructions.md` - manual-only workflow and model-dispatch rules.
- Other `skills/`, `loops/`, and `snippets/` - reusable toolkit material.

## Use on a new laptop

Requires Git, Bash, Python 3.9+, and GitHub Copilot CLI. Log in to Copilot
separately; this repo does not contain account credentials.

```bash
git clone git@github.com:YaroslavShypunov/vibe-kit.git ~/vibe-kit
cd ~/vibe-kit
./install.sh
```

The installer:

- Links skills into `~/.copilot/skills`, `~/.agents/skills`, and `~/.codex/skills`.
- Links `*.agent.md` profiles into `~/.copilot/agents` and shared instructions into `~/.copilot/instructions`.
- Merges the saved model settings into `~/.copilot/settings.json`, preserving unrelated settings and agent entries.
- Updates only the two marked policy blocks in `~/.copilot/copilot-instructions.md`, preserving other instructions.

Existing settings and policy files are backed up before changes. Conflicting
skills, agents, or instruction files stop installation before any changes.
To replace those files safely, run `./install.sh --replace`; their originals
are moved to `~/.copilot/backups/vibe-kit-<timestamp>/`, using paths relative
to your home folder. Configuration symlinks and malformed settings or policy
blocks require a manual merge.

Keep the clone in place: installed skills and agents are links to this repo.
No source files on the original laptop are removed by this export.

Restart Copilot CLI after installation. Check `/skills info build`, `/agent`,
and `/subagents`, then explicitly enter `/build <task>`. The workflow remains
manual-only; ordinary prompts do not start its contract and review process.

## Review a coding session

The same installer includes `/vibe-coding-retrospective`. After restarting
Copilot CLI, check `/skills info vibe-coding-retrospective`, then use:

```text
/vibe-coding-retrospective review session <session-id-or-link>
```

The skill reviews the named session and recommends concrete improvements.
Reviews are read-only by default; implementation and learning-log updates
need separate approval. It uses the current main model and, for large
histories, one evidence scout with `gpt-6-luna`. No additional model settings
are needed.

The bundled Python reader supports local Copilot session UUIDs. Session
history and `~/.copilot/learning-logs/vibe-coding-retrospective.md` stay local
and are not included in this repo or created by installation.

## Saved models

| Role | Model | Effort |
|---|---|---|
| Main session, coder, reviewer, diagnostician, security-reviewer | `gpt-6.1-sol` | `xhigh` |
| repo-scout, test-engineer | `gpt-6-luna` | `max` |

Sage, Browser QA, and UI Critic keep native host defaults, matching the source
setup. `/build` uses native `subagents.agents` dispatch and omits model overrides.
Model availability depends on the Copilot account and CLI version. If a saved
model is unavailable, the workflow reports `MODEL_UNAVAILABLE` rather than
intentionally substituting another model.

These main-session settings are global, not limited to `/build`.

## Environment-specific tools

The core workflow needs Git and `shasum` for review packets and frozen tests.
Configure `chrome-devtools` MCP separately for Browser QA.
Civil-iTwin instructions assume interactive Zsh with nvm and Node `20.19.3`.
OpenSite+ code-mode live checks also require the `bentley-osp` bridge and a
running OpenSite+ session; the workflow can use `execute_code` directly without
the optional, separately installed `code-mode-test-runner` skill.

Account data, permissions, trusted paths, MCP configuration, plugins, session
history, and credentials are deliberately not exported. Set those up on each
laptop as needed.

## Sync changes

Edit the repo, commit, and push. On the other laptop:

```bash
cd ~/vibe-kit
git pull
./install.sh
```

Linked skill, agent, and instruction changes are picked up from the clone.
Run the installer again after adding files or changing saved settings or policy
blocks, then restart Copilot CLI. Changing models in `/subagents` updates only
local settings; also update `settings/build-settings.json` to sync that change.

## Add a skill, agent, or loop

```bash
mkdir -p skills/my-skill
# Create skills/my-skill/SKILL.md, then:
./install.sh
```

Custom Copilot agents use `agents/<name>.agent.md`. Example agent files and
`loops/` are reference material and are not installed as Copilot profiles.
