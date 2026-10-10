# Report and learning

## First answer: a decision, not a session report

Analyze the accessible history deeply, then return a small action brief.
Default to 120-180 words. The first answer must not exceed 200 words unless
the user explicitly requests detailed analysis. Count all visible words,
including headings, tables, evidence notes, and any next-step sentence.

Lead with the strongest recommendation. One to three recommendations can
be bullets, a small table, or short paragraphs. No mandatory section stack.

Each recommendation must answer:

- **Change:** What exactly should be reused, updated, created, or done
  differently? Name a relevant existing artifact or propose a specific one.
- **Why:** What short observation supports it? A compact source reference
  can help; a statistics dump cannot replace the recommendation.
- **Use:** When and how should the user apply it? Preserve the relevant
  quality check and distinguish an experiment from a proven improvement.

For example:

```markdown
**Best change: <specific recommendation>.**
<One brief reason grounded in this session.>

1. **<Concrete action>.** <When/how to use it; important guardrail.>
2. **<Second action only if valuable>.** <Brief reason and usable next step.>

<Only a material evidence gap or one compact evidence reference.>
```

A repeatable successful process is a candidate improvement, not just a
"keep doing" compliment. If turning it into a tool would be worthwhile,
offer that concrete option in the first answer; do not wait for the user
to ask whether a skill or loop could help.

Check plausible existing artifacts first. Recommend reuse before creating
a duplicate. Do not invent a named tool, force an integration for every
session, or present changes to an existing manual workflow as authorized.

One recommendation may address quality, time, and tokens together. Do not
repeat it under separate categories or force those labels into the answer.

Omit generic praise, incidental counts, unsupported model judgments, and
required AI-lesson/experiment sections. Explain a necessary unfamiliar
concept briefly rather than teaching all of AI coding.

Keep the detailed timeline, usage accounting, alternative explanations,
and implementation plan out of the first answer. Expand only on request
or when the user selects a recommendation that needs a scoped proposal.
Do not hide a material coverage gap to make the answer sound decisive.

Do not call a delivery claim verified. Necessary outcome limitations take
priority over extra recommendations. A clean task can have no improvement,
and insufficient evidence may prevent any responsible recommendation.

## Final usefulness check

Before sending, ask internally:

1. Does the first sentence say what I recommend, not what I investigated?
2. Can the user act on it without inventing the missing solution?
3. Did I offer an obvious reuse/integration opportunity myself?
4. Is each action supported, applicable, and worth its overhead?
5. Is the first answer within 200 words, without a wall of evidence?

Revise once if it fails. Do not spawn a reviewer or repeat the full history
read just to check the answer's wording.

## Calibration examples

These are illustrative, not claims about a newly reviewed session. Do not
copy recommendations without matching evidence and checking existing tools.

### Repair-heavy UI task

Assume the evidence supports repeated coordination, delayed real-screen
feedback, and a useful approved-mockup stage. Also assume `ui-delivery`
has been inspected and is a suitable existing skill.

```markdown
**Use the existing `ui-delivery` skill for the next similar UI task; do not create another workflow.**

It preserves the useful design-to-mockup process while making the first real screen an early checkpoint.

- **Keep one implementation session and one writer.** Create a child only when branch isolation or a separate phase needs it; nesting and subagents are different.
- **Compare the first complete screen with the approved mockup before expanding.** Keep final behavior, keyboard, and regression checks.
- **Batch cosmetic feedback.** Rerun affected checks after each batch, rather than restarting unaffected reviews.

The earlier report identified repeated handoffs and late visual corrections. This is a proposed improvement, not proven token savings.
```

The failure this prevents is waiting for "should we create a loop?" before
offering a concrete reusable route.

### Clean task

```markdown
**Keep the focused approach; no new skill or automation is justified here.**

The recorded change stayed within scope, and the final focused check followed the last relevant edit. For the next comparable task, reuse the short acceptance checklist and verify after the final edit.

This session does not show a recurring problem worth adding tooling for.
```

### Incomplete history

```markdown
**I cannot recommend a workflow change from this partial history.**

The available records omit implementation attempts and final check results. Please provide the missing implementation-session export before treating its delays as avoidable.

I have not verified the delivered result or measured its token usage. Another scout cannot recover records that are unavailable.
```

## Examples of precise recommendations

These illustrate form; use them only when the target evidence supports them.

- **Repeated speculative fixes:** "The same error returned after three edits.
  Before another edit, collect the relevant error trace and inspect the
  assumption behind the fix. Keep the regression check."
- **Repeated context setup:** "Two agents independently rediscovered the same
  package constraints. For a similar task, provide a short shared context
  packet; do not forward the whole transcript."
- **Missing final verification:** "The only recorded check preceded the last
  behavior change. Run the focused check after the last relevant edit in the
  next task; do not treat the earlier pass as current evidence."

Do not infer that every repeat, agent, or failed command was unnecessary.
Explain the plausible cause and any uncertainty.

These statements become useful recommendations only after identifying a
specific adoption step, not simply by reporting the pattern.

## Learning log

Location: `~/.copilot/learning-logs/vibe-coding-retrospective.md`.

Keep the log separate from the skill's instructions. Do not create it during
ordinary review or skill installation. Create it only with approval for the
first specific entry.

Before any write, show the exact proposed entries or changes and ask for
approval. Approval to implement a tool does not approve a log update, and
log approval does not approve implementation.

Do not attach a learning-log proposal or print the entry template in every
first answer. Expand it when the user chooses to retain a lesson; preserve
the approval requirement before writing.

Suggested entry:

```markdown
### <descriptive-lesson-id>
- Recorded: <date>.
- Source: <session ID/link and brief evidence reference>.
- Scope: <general or named project; task type and relevant environment>.
- Status: <hypothesis / trying / supported / retired>.
- Lesson: <one actionable sentence>.
- Use when: <conditions>.
- Avoid when: <limits or contradictory conditions>.
- Experiment and measure: <one change and practical evidence to compare>.
- Quality guardrail: <what must remain unchanged>.
- Observed follow-up: <source session and result, or not yet observed>.
```

Approval and evidence status are separate. A user-approved hypothesis remains
a hypothesis until observations support it. Comparable observations increase
confidence but do not establish a universal causal claim.

Search for relevant entries and read their full applicability/evidence before
using them. Do not load the whole growing log by default, duplicate a lesson,
or apply a project-specific workaround globally.

Log only actionable, reusable learning or an explicitly chosen experiment.
One-off narration, generic slogans, speculative model judgments, raw
transcripts, secrets, and numerical scores do not belong in the log.

When later evidence conflicts, propose a specific revision or retirement
rather than silently reinforcing an old rule. Preserve unrelated entries.
Deduplication, compaction, deletion, and status changes also require approval.

## Source foundations

These inform the skill, not a requirement to research on every review:

- [Anthropic: Claude Code best practices](https://code.claude.com/docs/en/best-practices):
  evidence, verification, and context management.
- [OpenAI: evaluations](https://developers.openai.com/api/docs/guides/evals):
  explicit criteria and evaluation-driven iteration.
- [Google SRE: postmortem culture](https://sre.google/sre-book/postmortem-culture/):
  contributing causes, actionable follow-up, and avoiding blame.
- [Anthropic: building effective agents](https://www.anthropic.com/engineering/building-effective-agents):
  simplicity before added orchestration.
- [METR: early-2025 developer study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/):
  perceived speed is not measured speed; do not transfer its percentages.
- [OWASP: prompt-injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html):
  untrusted content is not authorization; instructions alone are not enforcement.
- [Agent Skills specification](https://agentskills.io/specification):
  progressive loading of instructions and references.
