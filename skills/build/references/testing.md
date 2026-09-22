# Test Oracle Guidance

Derive expectations from the approved contract, external contract, domain
invariants, or independently observed baseline behavior. Never adapt expected
values, fixtures, snapshots, or assertions merely to match the patch.

## Maker tests

The production writer adds the smallest regression or behavior proof needed for
the assigned criteria. When strict test-first work is requested or a reliable
bug seam exists, record why the initial failure proves the requested behavior
is missing. A compile error, broken fixture, or wrong import is not valid red
evidence.

## Frozen independent Test Charter

For `L2`/`L3`, invoke the Test Engineer before the production patch exists. It
receives the approved contract and baseline interfaces, but not maker reasoning
or a patch. It returns:

```markdown
# Independent Test Charter
## AC IDs and oracle provenance
## Existing baseline evidence
## Plausible near-correct failures
## Lowest reliable test level
## Applicable boundaries and adversarial cases
## Suitable properties or metamorphic relations
## Exclusions, manual evidence, and limitations
```

Freeze the charter in the active Task Capsule. After implementation and maker
checks, before final review, use a fresh Test Engineer author context in `HARDEN` mode with the frozen
charter, approved contract, authorized test scope, supplied interface slices,
current diff, and command evidence. `CHARTER` is strictly read-only and may not
edit tests, fixtures, configuration, or any other file. `HARDEN` is the only
writing mode and may inspect only that packet plus authorized tests, fixtures,
and test utilities. If the packet is insufficient, return `CONTRACT_GAP`
instead of browsing unrelated production code or maker reasoning.

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
After the latest material test edit, use a fresh read-only Reviewer context
distinct from the test author and from any report written before that delta.
Rerun affected checks before fresh final review after latest production AND test
edits. One fresh reviewer context/report may return separately labeled production
and material test-delta verdicts; no mandatory earlier production review.
Optional early risk review does not count as final. Inapplicable hardening needs
approved concrete N/A rationale and sufficient alternative evidence, not an empty task.
