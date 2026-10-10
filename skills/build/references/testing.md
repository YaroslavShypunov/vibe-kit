# Test Oracle Guidance

Derive expectations from the approved contract, external contract, domain
invariants, or independently observed baseline behavior. Never adapt expected
values, fixtures, snapshots, or assertions merely to match the patch.

## Baseline

Before approval, while discovery runs, start the focused existing tests and a
no-emit type check (or IDE diagnostics) for the owning packages on untouched
code in an async shell. Inspect the script first. Allowed: test runs without
coverage, update, or watch flags, and no-emit type checks; they may write only
ignored caches or build-info files. No builds, fixers, installs, snapshot
updates, or external writes before approval. Record each failure as
`PRE_EXISTING` with a normalized signature: test or file, assertion or
diagnostic code, and location, so a new failure inside an already failing
test is still visible. If the baseline cannot run
(for example, dependencies are not built), record `BASELINE_BLOCKED` with the
reason and put the needed command in the contract. If a `PRE_EXISTING` failure
blocks an `AC-*` evidence plan, resolve it in the contract. `PRE_EXISTING`
failures are not repair cycles. Later gates compare against this list: a
failure that is not on it is new and must be fixed or explained. Finish the
baseline before any test file is written, so new tests never look
pre-existing.

## Maker tests

When RED tests exist, the production writer adds maker tests only for assigned
criteria that RED does not cover, in files that are not frozen. Otherwise it
adds the smallest regression or behavior proof needed for the assigned
criteria. When a reliable bug seam exists, record why the initial failure
proves the requested behavior is missing. A compile error, broken fixture, or
wrong import is not valid red evidence.

## Independent RED tests (`L2`/`L3`)

After approval and before the production patch exists, the Test Engineer in
`RED` mode receives the approved contract, baseline result, allowed test paths,
and baseline interfaces, but no maker reasoning or patch. It writes failing
tests for its assigned criteria in the approved test paths, formats only its
own test files, runs them, and returns:

```markdown
# RED Report — contract revision N
## Tests written (path :: test name -> AC-*)
## Red evidence per test (command and failing assertion, or missing new symbol)
## Oracle provenance per AC
## Plausible near-correct failures covered / not covered
## Lowest reliable test level and why
## Properties or metamorphic relations used
## ACs without automated tests: live or manual evidence steps
## ALREADY_GREEN tests and limitations
```

Valid red is a wrong result, missing behavior, or a missing symbol that the
contract names as new. A typo import, broken fixture, or environment error is
not valid red; RED fixes its own test before reporting. A test that passes on
the baseline is `ALREADY_GREEN`: the behavior may already exist or the test is
too weak. RED strengthens it or reports it, and the main session asks the user
(the criterion may already be met); never resolve it as an addendum.

The main session freezes every file RED created or changed (tests, fixtures,
helpers) with `red-tests.sh freeze` and runs `red-tests.sh check` after each
coder turn and at the final gate. The coder never edits frozen files, test
fixtures, test utilities, or test configuration. A coder that believes a
frozen test is wrong returns `TEST_DISPUTE` with the test name, the contract
text, and the reason in contract terms. The main session sends that to the
same `RED` agent without the patch. RED decides from the contract and baseline
only: it fixes its own test (then `red-tests.sh refreeze`) or upholds it with
a reason. Allow one dispute per test; a second dispute on the same test, or
any change to what a test asserts, goes to the user as a contract question.

RED follow-ups go through `write_agent` and never include a patch, diff, or
changed production file:

- for an addendum that affects RED tests, send only that change; RED updates
  only the affected tests;
- for a reapproved revision that keeps the objective and allowed paths, send
  the complete revised contract; RED updates its tests and report; and
- when the objective or allowed paths change, launch a new `RED` agent with the
  complete revised contract.

After a patch exists, RED reads production code only from the baseline
(`git show HEAD:<path>`) and does not run tests; the main session runs them.
When RED first runs after a patch already exists (unexpected escalation), red
cannot be observed; the final reviewer confirms from the diff that each such
test would fail without the patch.

## Hardening

`HARDEN` is required for `L3`, optional for `L2` (see the Build skill, step
8), and used for `L1` when meaningful near-correct failures remain plausible.
A fresh Test Engineer in `HARDEN` mode receives the RED Report, approved
contract, authorized test scope, supplied interface slices, review packet, and
command evidence. It may inspect only that packet plus authorized tests,
fixtures, and test utilities. It adds cases as new lines in RED files or in
new files, and never edits or deletes an existing RED line; when a case needs
such an edit, it uses a new file. If the packet is insufficient, it returns
`CONTRACT_GAP` instead of browsing unrelated production code or maker
reasoning. Afterwards run `red-tests.sh extend` with its new files; it rejects
any edited RED line. Send defects in `HARDEN` tests to the same `HARDEN`
agent.

## Select applicable adversarial cases

- empty, missing, invalid, extreme, and exact-boundary input;
- off-by-one behavior and repeated invocation;
- errors, cancellation, partial failure, retries, and stale state;
- ordering, concurrency, caller compatibility, and serialization;
- permissions and trust boundaries;
- realistic identifiers, connections, units, coordinates, precision, and
  tolerance; and
- behavior a plausible near-correct implementation would get wrong.

Use property or metamorphic tests only when the domain offers a real invariant,
such as round-trip stability, idempotence, monotonicity, conservation, bounds,
ordering invariance, equivalent unit/coordinate transformations, or
parse/format stability. Do not introduce a new testing dependency without
approval.

Rerun agreed validation after writer work and after test hardening. For
`L2`/`L3`, every Test Engineer change to tests, fixtures, utilities, or
test-only configuration is material. For `L1`, changed expected values,
snapshots, fixtures, mocks, timing/concurrency, or assertion logic is material.
After the latest material test edit, an independent read-only Reviewer that did
not author the tests must review the full material test delta. A reviewer that
saw earlier bytes may do this in `VERIFY` mode only under the Build skill's
**Agent reuse** rules. Rerun affected checks before independent final review
after latest production AND test edits. One independent reviewer context/report
may return separately labeled production and material test-delta verdicts; no
mandatory earlier production review.
Optional early risk review does not count as final. Inapplicable hardening needs
approved concrete N/A rationale and sufficient alternative evidence, not an empty task.
