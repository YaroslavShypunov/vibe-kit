---
name: "Bentley Copilot API TSDoc"
description: "Use when the user asks to add tsdocs, TSDoc, JSDoc, code-mode functions, workflow/query/action APIs, or SKILL.md guidance for exported TypeScript APIs intended for Bentley Copilot, MCP code-mode, agent tools, or downstream consumer apps. Generate concise code-mode-ready docs and keep examples in runtime skills, not inline in TypeScript."
---

# Bentley Copilot API TSDoc

- Assume exported Copilot APIs may live in reusable civil/Bentley packages and later be imported, re-exported, or scraped by a host app.
- When the user asks for TSDoc on a Copilot-facing function, generate concise code-mode-ready docs instead of generic JSDoc.
- Keep docs simple by default. Avoid tutorial-style explanations, long workflows, and broad behavioral essays.
- If an exported function is part of the Copilot-facing API surface, add `@code-mode <Namespace(s)>` unless a repository-specific generation workflow owns the annotation.
- For OpenSite+ MCP/Bentley Copilot code-mode integrations, prefer `@code-mode MCPCodeModeDev MCPCodeModeProd` on the same line unless nearby code or the user explicitly requires another namespace. Bentley Copilot splits extraction into separate dev and prod namespaces, so use both tags together for these manually authored APIs.
- Use `@code-mode ModelingAgent` only when that is the active extraction or consumer namespace in the local project or nearby code-mode APIs clearly use it.
- Use `@code-mode Supervisor` only for non-model application state or when nearby code-mode APIs clearly use Supervisor for the same responsibility.
- If the namespace is still ambiguous and the choice matters, ask once.
- Prefer exported function declarations (`export async function name(...)`) over exported arrow functions unless the local extractor supports arrow exports.
- For package-owned features before package scraping is available, use a thin app-level wrapper: import the package API with an alias, re-export a tagged function from the app, and call the package function directly.

## Civil-iTwin static namespace exception

This exception applies only to static namespace integrations in:

```text
typescript/core/civil-ai-frontend
```

Recognize this workflow from an authored metadata marker such as:

```ts
/** @civil-ai-generate OpenProfileSectionWorkflowOperations */
```

For this workflow:

- The shared implementation belongs in `src/features/<Feature>/operations/`.
- The shared namespace function is **not** a direct Code Mode API. Do **not** add `@code-mode` to it.
- Metadata in `src/features/<Feature>/metadata/` owns the operation ID, Zod input schema, targets, descriptions, example, and optional guidance.
- `scripts/generate.mjs` owns generated adapters in `new-code-mode/` and `new-tools/`.
- The generated Code Mode wrapper is the only extracted API. It uses exactly:

  ```ts
  @code-mode MCPCodeMode
  ```

- Do not replace that generated tag with `MCPCodeModeDev MCPCodeModeProd`.
- Do not manually edit files with an `@civil-ai-generated` header. Update metadata or generator input, then run:

  ```sh
  npm run generate
  npm run check
  ```

- Generated focused references, such as `open-profile-section.md`, are generator-owned. They log the complete returned value with `console.log(result)`.
- The feature parent `SKILL.md`, Tool Agent Provider, `CivilToolAgentCatalog` entry, and `civil-ai-frontend.ts` barrel export remain authored files.
- Parent Civil-iTwin skills and generated focused references omit `namespaces` frontmatter.
- A feature provider owns one stable host-facing agent identity. Generated tool prompt references must use:

  ```text
  <provider-schema-name>__<snake_case_tool_name>
  ```

  Tool definitions and executor keys remain unprefixed.

Use `typescript/core/civil-ai-frontend/docs/namespace-integrations.md` as the current source of truth for this workflow.

## Code-mode API layering

- Prefer a small workflow/query/action split when a direct user request needs domain lookup before a UI or model action.
- Workflow functions are the default route for standard natural-language requests. They accept user values such as names or labels, compose query/action functions, and return a concise user-facing status.
- Query functions find, inspect, resolve, or disambiguate domain objects. Return small Copilot-friendly DTOs instead of raw application objects.
- Action functions perform low-level work only after stable inputs are resolved, such as an element ID or selected object. They are not the first choice when the user supplied a name.
- Keep dependencies one-directional: workflows may import query and action functions; query and action functions must not import workflows.
- Do not create skills for architectural layers such as `workflow`, `query`, `action`, or `code-mode`. Skills describe the feature or domain users ask about.
- Example: `openProfile(alignmentName)` handles “Open Driveway-2 in Profile”; `queryAlignmentsByName` and `resolveAlignmentByName` support discovery; `openProfileWithAlignmentId` is only for a stable resolved ID.

## Preferred TSDoc shape

1. One short summary sentence describing the action.
2. One extra sentence only when it helps tool selection.
3. Optional `@note` with at most two realistic valid use cases and one invalid use case.
4. Optional `@param` only when the parameter is easy to confuse, such as a name versus an ID.
5. Optional `@returns` only when the return contract is not obvious from the signature.
6. `@code-mode ...` last.

For Civil-iTwin static namespace integrations, apply this TSDoc shape to the **generated wrapper only**. Keep the shared namespace implementation concise and untagged.

## Direct-action routing guidance

- Make the summary and first detail sentence describe performing the action, not teaching the UI.
- Include one invalid `@note` use case for how-to/tutorial wording when the function should only execute direct requests.
- Include one invalid `@note` use case for a nearby but wrong domain action when useful, such as Cross Section versus Profile.
- For synonymous product terms, state equivalence explicitly. For example, `Profile`, `Civil Profile`, and `Profile View` can trigger the same function.

## Example guidance

- Do not add inline `@example` blocks or `@code-mode-example` helper functions to TypeScript operation files.
- For manually authored APIs, keep snippets tiny: assign user-provided values to named variables, call the function, and place the example in the runtime `SKILL.md`.
- For Civil-iTwin generated focused references, do not edit the example directly. The generator intentionally emits `console.log(result)` to preserve the complete return shape.
- Do not add `@code-mode` to internal helpers or exported functions not intended for Bentley Copilot use.
- Preserve local house style when nearby manually authored code-mode APIs already exist.
- If the repository has a code-mode extraction, generation, or validation workflow, preserve it and mention the applicable regeneration step after editing. In OpenSite+, run:

  ```sh
  pnpm --filter opensiteplus extract-code-mode-api
  ```

  after changing manually authored code-mode APIs or docs.

## Skill guidance for MCP code-mode APIs

- Create or update a colocated `SKILL.md` when natural-language routing needs help finding the function.
- Name skills after the feature or domain in lowercase kebab-case, not after the implementation folder or code-mode layer. Prefer names like `profile`, `road-rail-alignment`, `corridor`, or `cross-section`.
- The frontmatter `description` is the primary routing signal. Lead with verbs and nouns users say.
- Never list function names in the description; users do not type function names in their prompts.
- Include relevant synonyms and variant phrasing, such as `XS view`, `section cut`, `profile view`, or `civil profile`.
- Keep the description under approximately 50 words.
- Keep the top-level heading aligned with the skill name unless the local project has a different established convention.
- For standard manually authored OpenSite+ skills, include a `namespaces` list matching the TypeScript tags.
- For the Civil-iTwin static namespace exception, omit `namespaces` from both the authored parent `SKILL.md` and generated focused references.
- When a feature has several independent operation families, keep one discoverable parent `SKILL.md` and route to flat focused references with `read_skills(["feature/reference"])`.
- Civil-iTwin parent skills are authored. Generated focused references are not.
- Keep skill files scalable: concise function instructions, a functions-covered list, and representative examples by functional group.
- Do not add a full tutorial or a separate long example for every function.
- Direct requests should call the applicable workflow; how-to questions should use documentation/tutorial flows.
- Standard requests use workflows, discovery/disambiguation uses queries, and resolved-ID scenarios may use actions.

## Manually authored OpenSite+ example

```ts
/**
 * Opens the Profile view for a named alignment.
 * Use this for direct requests to open, show, display, or view an alignment profile; it resolves the alignment by name and does not require the user to select it first.
 * The terms "Profile", "Civil Profile", and "Profile View" are equivalent triggers.
 * @note
 * - Valid use case: "Open Driveway-2 alignment in Profile".
 * - Valid use case: "Open TestTest in Profile".
 * - Invalid use case: "How do I open a profile?" because the user is asking for instructions, not asking you to perform the action.
 * - Invalid use case: "Open a cross section for Driveway-2" because this function only opens profile views.
 * @param alignmentName Exact alignment name or label provided by the user, for example `"Driveway-2"`.
 * @returns A short status message describing the result.
 * @code-mode MCPCodeModeDev MCPCodeModeProd
 */
export async function openProfile(alignmentName: string): Promise<string> {
  // ...
}
```

For manually authored runtime skills:

```ts
const alignmentName = "Driveway-2";
const result = await openProfile(alignmentName);
console.log(result.message);
```
