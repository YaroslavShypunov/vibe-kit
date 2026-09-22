# Verification Guidance

For every command, record:

- exact command and working directory;
- exit status and relevant output;
- `AC-*` criteria covered;
- current files or behavior it proves;
- limitations and any manual evidence still required.

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
  traceability.
- Classify actual affected behavior using `profiles.md`; a configuration filename
  alone does not raise risk to `L3`. Never lower genuine protected risks.

After the last relevant edit, rerun the smallest complete gate set and perform
any required re-review. Final completion requires a current traceability row for
every acceptance criterion. User testing is useful external evidence but does
not replace a repository check that can run now.

Order: maker checks -> applicable independent hardening -> rerun affected checks
-> fresh final review after latest production AND test edits. One independent
reviewer context/report may supply separately labeled production and material
test-delta verdicts. Early risk review is not final; later edits invalidate
affected evidence/review. Feature PASS requires actual integrated journey evidence
on the current integrated revision. Report ticket and pending feature separately.
