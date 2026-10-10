---
description: "Use when running Node, Rush, or npm commands in Civil-iTwin. Run them through the user's interactive login Zsh, where nvm use 20.19.3 is already available."
---
# Node Version Setup for Civil-iTwin

The Copilot command runner does not load the user's interactive shell configuration. Run every Node-related command through the user's configured interactive login Zsh:

```bash
zsh -lic 'nvm use 20.19.3 && <command>'
```

## Rules

- Run every `rush`, `npm`, or `npx` command as `zsh -lic 'nvm use 20.19.3 && <command>'`.
- Keep `nvm use 20.19.3` as the first command inside the Zsh command string.
- Put any required `cd` inside the Zsh command string before `nvm use 20.19.3`.
- Do **not** source `$HOME/.nvm/nvm.sh`, inspect `NVM_DIR`, test for NVM files, use `command -v nvm`, wrap the command in `if`/`else`, or create an NVM bootstrap script.
- If the Zsh command fails, report its error. Do not try alternate NVM setup commands.

## Example

```bash
zsh -lic 'nvm use 20.19.3 && rush install'
zsh -lic 'nvm use 20.19.3 && rush build'
zsh -lic 'cd typescript/core/civil-frontend && nvm use 20.19.3 && npm run test'
```
