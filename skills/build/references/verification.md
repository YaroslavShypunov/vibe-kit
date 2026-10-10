# Verification Guidance

For every command, record:

- exact command and working directory;
- exit status and relevant output;
- `AC-*` criteria covered;
- current files or behavior it proves;
- limitations and any manual evidence still required.

Run the fastest check that can fail first: IDE diagnostics, a single-package
no-emit type check, single test files, and per-file lint in check mode. Run
full builds and broad suites once, in parallel with the final review. Keep
command output to failures and summary lines; save long logs to files. Compare
every gate with the baseline: only recorded `PRE_EXISTING` failures may remain.

A summary claim is not proof. Use commands from the approved Build Contract or
the repository's documented workflow. Do not infer broad, destructive, fix, or
installation commands from package files. Repository scripts execute local
code, so inspect them and use normal host approval.

## Invalidation

- A contract change invalidates affected discovery, tests, implementation,
  review, and final verification.
- A production edit invalidates affected command evidence, review, independent
  tests that depend on old behavior, and final traceability.
- A test edit invalidates affected test evidence, test review, and final
  traceability. A change to a frozen RED test outside `RED` or `HARDEN` is a
  `BLOCKER`; restore it with `red-tests.sh restore`.
- A production edit invalidates live evidence only when it touches the
  exercised flow.
- Classify actual affected behavior using `profiles.md`; a configuration filename
  alone does not raise risk to `L3`. Never lower genuine protected risks.

After the last relevant edit, rerun the smallest complete gate set and perform
any required re-review. Final completion requires a current traceability row for
every acceptance criterion. User testing is useful external evidence but does
not replace a repository check that can run now.

Order: baseline -> RED tests for `L2`/`L3` -> maker checks -> applicable
independent hardening -> rerun affected checks -> independent final review on
current bytes after latest production AND test edits, in parallel with
specialists, live evidence, and full gates. One independent
reviewer context/report may supply separately labeled production and material
test-delta verdicts. Early risk review is not final; later edits invalidate
affected evidence/review. Feature PASS requires actual integrated journey evidence
on the current integrated revision. Report ticket and pending feature separately.
