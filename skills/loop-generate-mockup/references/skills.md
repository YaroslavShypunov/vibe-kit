# Skill routing and conflict policy

These are the user's selected capabilities for this loop. Resolve their actual
SKILL.md paths through the active harness's skill catalog or declared installation
roots. Do not hardcode a machine-specific home directory or assume a subagent
inherits the main session's loaded skills. Pass exact paths and require each agent
to read the skill it uses and any applicable supporting references.

| Skill | Owner | Use |
| --- | --- | --- |
| frontend-design | Builder | Default visual-design guidance within the project brief. |
| web-design-guidelines | Reviewer | Source-level web UI checks alongside rendered and interaction review. |
| ui-ux-pro-max | Builder, conditionally | A focused lookup for a concrete unresolved pattern, typography, colour or UX question. |

The first two are required dependencies for ordinary HTML mockup runs. Check they
are readable before dispatch. ui-ux-pro-max is required only when a lookup is
selected. If a required dependency is unavailable, report the exact gap; do not
pretend to use it or silently waive it. Installation or an explicitly approved
alternative resolves the gap. No additional research agent is needed.

## Stable, economical inputs

Record each selected skill's path, declared version when present and content hash
(or clean repository revision). Pin selected supporting files when relevant. Load
only the assigned skills and relevant topic references, not every installed design
skill or all of a large database. Reuse query results within the same run when the
question and source version have not changed.

web-design-guidelines requires a fresh source fetch before each review. Preserve
the fetched rules, URL, date and hash in task evidence. Compare with the prior
review's hash; when rules change, the coordinator assesses applicability and
explicitly rebaselines affected criteria before acceptance. Do not silently move
the goalposts or treat an offline cache as a fresh fetch. Failed fetch means the
required guideline check remains unverified; complete other checks but report
BLOCKED until access or an explicit offline alternative is supplied.

## Apply within the task

The coordinator states whether the task extends an existing visual system or
explores a new direction. Existing branding, components, domain wording and copy
conventions constrain creative choices. A skill's aesthetic preference is not a
universal usability rule. Applicable accessibility requirements still need to be
checked; a project conflict must be surfaced rather than silently excused.

Examples: a distinctive signature is not mandatory for a routine settings form;
Vercel's title-case preference does not override a project's sentence-case policy;
web URL-state guidance does not establish requirements for native navigation.
Consider all review rules, marking inapplicable ones when material, and classify
actual violations separately from preferences. Preserve the loop's full review
report and final verdict while including useful file:line findings.

## UI/UX Pro Max lookups

State the unresolved question first. Use one focused --domain query, or --stack
when implementation guidance is relevant and the stack is known. A design-system
query is reserved for an explicitly scoped new product-wide visual direction,
not every new screen in an existing product. Follow the skill's bounded retry
and result-relevance checks. Do not auto-persist generated MASTER.md files, change
canonical project documents, add frameworks, or enable GSAP just because a search
suggests them. Skill output remains advice until adopted in the brief.

Resolve scripts/search.py relative to the actual installed skill root and invoke
it with an available Python executable; do not rely on CLAUDE_PLUGIN_ROOT outside
its plugin environment. Verify scripts, references and data are present when
copying the skill to another harness. Passing only SKILL.md breaks its searches.

For native-target HTML mockups, use relevant platform guidance for design intent
and web guidance for the HTML representation. Neither constitutes native-runtime
or full accessibility conformance verification.
