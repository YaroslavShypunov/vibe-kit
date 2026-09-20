# Rendered review contract

Acceptance applies only to this mockup, scope and revision. It is not evidence
that the production application works or that accessibility conformance is complete.

## Required lenses

1. **Requirements and task completion:** every required journey and state is
   reachable; primary actions, navigation, selections, validation, cancellation
   and recovery work as specified. Identify missing requirements explicitly.
2. **UX clarity:** hierarchy supports the user's goal; labels and feedback are
   understandable; preserve entered work where appropriate; uncertainty and
   simulated capabilities are truthful. Do not invent product rules.
3. **Visual craft and consistency:** compare actual rendered screens with approved
   references and components. Check typographic roles, rhythm, alignment, grouping,
   density, imagery, visual emphasis and coherent styling across states. Explain
   how a weakness affects comprehension or violates the chosen direction.
4. **Adaptation and resilience:** inspect agreed viewports, content extremes and
   relevant zoom/reflow. Check clipping, overlap, unintended overflow, sticky
   controls, safe areas and interaction with available space. Desktop-only
   products do not automatically require a mobile redesign.
5. **Accessibility:** inspect semantics/names, labels, keyboard operation, focus
   visibility/order, dialog focus handling, non-colour cues, applicable contrast
   and target-size rules, feedback announcements and reduced motion. Measure
   objective properties where possible; appearance alone cannot establish contrast
   compliance. State the platform/standard and any untested assistive technology.
6. **Runtime:** check browser errors and missing assets. Distinguish mockup defects
   from agreed backend/native simulations. Do not pass an unreachable required
   journey merely because its buttons look correct.

Use actual browser tools and inspect representative screenshots yourself. When
tools or the environment prevent a required check, mark it unverified and return
BLOCKED. Automated scans supplement rendered and interaction checks; they do not
replace them. Never request that the user perform routine screenshots for you.

## Report

Keep reports compact, with:

- revision identity (commit when meaningful, otherwise artifact content hashes);
- coverage: requirement IDs, exercised journeys/states, viewport dimensions,
  input modes, checks and actual observations, screenshot/evidence paths;
- required findings, each with stable ID, severity, exact state/viewport,
  evidence, supporting requirement/rule, user impact and observable fix condition;
- optional suggestions in a separate non-blocking list;
- explicit limitations and unchecked scope;
- final line: `DECISION: ACCEPT`, `DECISION: REVISE`, or `DECISION: BLOCKED`.

Severity indicates repair priority, not whether the reviewer personally likes
the design. Blocking findings prevent completing a core task; major findings
materially impair usability, accessibility, consistency or required behaviour;
minor required findings are smaller but concrete contract violations. All required
findings prevent ACCEPT. Preferences without a requirement or demonstrated impact
are optional. Missing environments or unresolved product decisions mean BLOCKED.

During re-review, observe repaired behaviour in the browser, mark resolved IDs,
check affected adjacent states and the main journey for regressions. Do not accept
from code diffs or a builder's claim alone. Do not reopen settled style choices
without new evidence. The coordinator enforces the two-repair-round limit.
