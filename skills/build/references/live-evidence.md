# Live Evidence

Use live evidence when an `AC-*` depends on behavior that unit tests cannot
show. Name the tool, URL or prompt, steps, and expected results in the
contract's live evidence plan. Live evidence runs on the final candidate bytes
in parallel with the final review.

## Viewer and other UI flows: `browser-qa` with `chrome-devtools`

- The main session builds what the flow needs, checks whether the app already
  runs, and starts the documented start command in an async shell if not. In
  Civil-iTwin: `npm run start:servers` in
  `typescript/apps/civil-itwin-viewer-web` (Vite on port 3000; the backend runs
  from built output, so build the changed packages and the app first).
- Launch `browser-qa` in background mode, so screenshots and page snapshots
  stay out of the main context. Pass the URL (with any iTwin or iModel IDs from
  the contract), exact steps, expected results, `AC-*` IDs, and the evidence
  folder `<session-folder>/files/build/evidence/`.
- Launch `browser-qa` only after the builds it needs finish, and do not run a
  build that rewrites the served output while it runs.
- The Chrome profile keeps logins between runs. If `browser-qa` reports
  `LOGIN_REQUIRED`, ask the user once to log in in that browser window, then
  send the same agent a retry with `write_agent`.
- `ENVIRONMENT_FAILURE` is an evidence gap, not a production defect; fix the
  environment and retry once before asking the user.

## Code-mode functions: `bentley-osp`

- Use the `bentley-osp` tools only for changes to code-mode functions.
- The user must rebuild and start OpenSite+ first. Ask once, when the final
  review starts, with the exact build of the changed packages to pick up.
- Check `ospBridgeStatus`, then run the contract's prompts with the
  `code-mode-test-runner` skill or `execute_code`.
- Repeat only when a repair touches code-mode files.

## Manual user test

Use it only when no tool can prove the behavior. Give exact steps and expected
results, and record the user's answer as evidence.

A later edit invalidates live evidence only when it touches the exercised flow.
