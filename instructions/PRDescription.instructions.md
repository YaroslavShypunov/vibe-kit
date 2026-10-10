---
description: When I ask you to write a PR description, follow these guidelines to generate a concise, well-structured pull request description for Azure DevOps.
---

# PR Description Writing Guidelines

## Output Format
- Return the PR description in **Markdown format** compatible with Azure DevOps.
- The result must be ready to copy-paste into Azure DevOps PR description field with all font styles preserved.
- Use Azure DevOps-compatible Markdown: headings (`##`, `###`), bullet lists (`-`), bold (`**`), inline code (`` ` ``), and code blocks (` ``` `).

## Length Constraints
- **Hard limit: 4000 characters maximum.**
- Target **1500–2500 characters** for UI changes (to leave room for screenshots).
- Target **2500–3500 characters** for logic-heavy or backend changes with no screenshots.
- Always count characters before returning. If over 4000, trim lower-priority sections first (e.g., reduce detail in "Changes" bullets, shorten "Context").

## Structure
Use this template:

```
## Context
<1–3 sentences explaining WHY this change is needed. Reference the work item/bug number if available.>

## Changes
<Bulleted list of WHAT was changed. Group by area if touching multiple files/features.>

## How to Test
<Steps a reviewer can follow to verify the change works.>

## Screenshots
<Placeholder: "See screenshots below" or "N/A" for non-UI changes.>
```

### Section Rules
- **Context**: Extract from the branch name, commit messages, and any user-provided context. Link the work item number (e.g., `#2011675`) when identifiable.
- **Changes**: Be specific but concise. Each bullet = one logical change. Use file or component names when helpful. Do NOT list every single file — group related changes.
- **How to Test**: Provide actionable steps, not vague directions. Include specific inputs or scenarios when relevant.
- **Screenshots**: For UI changes, leave a clear placeholder where the user will paste before/after screenshots. For non-UI changes, write "N/A".

## Deriving Changes
- **Always compare the current branch against `master`** to identify what changed using `git diff` or `git log`.
- Summarize the diff into meaningful, reviewer-friendly bullets — do not dump raw file lists.
- When the user provides additional context about the changes, incorporate it to improve clarity and accuracy.

## Tone & Style
- Professional but not formal. Write for a technical reviewer.
- Use active voice: "Fixed…", "Added…", "Refactored…", "Updated…".
- Avoid filler words and generic statements like "Various improvements were made."
- Do not include PR title in the body — Azure DevOps has a separate title field.
