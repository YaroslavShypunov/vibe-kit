# Concise design brief

Create design-brief.md alongside the mockup. Aim for roughly 400–800 words for
an ordinary task, expanding only when the journey requires it. Prefer compact
tables for state coverage. Explain intent and behaviour the HTML alone cannot
convey; do not narrate code or duplicate the requirements document.

Include:

1. **Scope and sources:** user goal, requirement IDs and authoritative paths;
   platform, viewports, design references and pinned UI/UX library revision;
   selected skills with versions/hashes, any focused lookup and its outcome,
   fetched review-guideline hash/date and material applicability exceptions.
2. **Design decisions:** reused tokens/components, important hierarchy and
   interaction choices, accepted versus provisional additions and exceptions.
3. **Behaviour and states:** journey, triggers, transitions, recovery and content
   extremes; identify anything intentionally outside the agreed scope.
4. **Preview and implementation:** entry file, reproducible local preview command,
   assets, simulation limits, component mappings when known, and distinctions
   between this HTML representation and a native target. Do not invent production
   architecture to explain a mockup.
5. **Review:** final verdict, reviewed revision, rounds used, checked coverage,
   evidence links, harness/version, actual builder/reviewer session IDs, configured
   model/effort, profile-check result and runtime verification status. Include known
   limitations. A blocked or budget-exhausted mockup must
   be clearly labelled; it is not an accepted reference.
6. **Carry forward before cleanup:** concise decisions that should survive in the
   project's task record/design system, with destination paths or clearly labelled
   proposed destinations. Name existing durable sources when nothing new needs
   preservation. Project-wide changes require acceptance; provisional choices
   must stay provisional. No lasting requirement may depend only on temporary
   screenshots or HTML.

The mockup, brief, assets and review evidence are task artifacts. Keep them until
implementation and any downstream comparison that needs them are finished; the
user can then remove them. Do not create dependencies from application code to
these files, automatically delete them, or copy all mockup assets into a permanent
wiki. A later implementation session should transfer accepted durable decisions
to canonical project docs before deletion, following that project's instructions.
