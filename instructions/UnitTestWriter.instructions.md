
 ---
description: When I ask you to create unit tests, you need to follow these guidelines to ensure consistency and quality in the tests you generate.
---

# Unit Test Writing Guidelines

## Framework
- Use **vitest** as the test runner and assertion library.
- Use **@testing-library/react** for rendering and interacting with React components.
- Import test utilities from `vitest`: `describe`, `it`, `expect`, `beforeEach`, `afterEach`, `beforeAll`, `afterAll`, `vi`.

## Mocking — General Principle
**Avoid unnecessary mocks.** Prefer real implementations whenever they are lightweight and side-effect free.

- **DO NOT** mock utility/helper functions that simply transform data (e.g., `getLocalized`, `DisplayUnitFormatter`, `usePendoId` formatting helpers). Use the real implementation.
- **DO** mock only things that have external side effects: network calls, RPC interfaces, browser APIs, iModel connections, third-party services.

## Mocking — Tools to Use
- Use `vi.spyOn(object, 'methodName')` as the primary mocking mechanism. It keeps the real reference and allows `vi.restoreAllMocks()` to clean up properly.
- Use `vi.fn()` for standalone function mocks or callback spies.
- Use `vi.mock('module')` only when `vi.spyOn` is not feasible (e.g., default exports, module-level side effects). When using `vi.mock`, always spread the actual module to avoid mocking more than necessary:
  ```ts
  vi.mock('@bentley/civil-frontend', async () => {
    const actual = await vi.importActual('@bentley/civil-frontend');
    return { ...actual, someFunction: vi.fn() };
  });
  ```
- Call `vi.restoreAllMocks()` in `afterEach` or `afterAll` to reset all spies and avoid test pollution.

## Mocking iModels
- Use `BlankConnectionHelper.createBlankConnection()` from `@bentley/civil-frontend` to create a lightweight iModel connection for tests. Do **not** mock the entire iModel object manually when this is available.
- Use `BlankConnectionHelper.createBlankViewState(iModel)` when a view state is required.
- Example:
  ```ts
  import { BlankConnectionHelper } from '@bentley/civil-frontend';
  const iModel = BlankConnectionHelper.createBlankConnection();
  ```

## Test Structure
- Group related tests inside `describe` blocks.
- Use `beforeEach`/`afterEach` for per-test setup and teardown.
- Use `beforeAll`/`afterAll` only for expensive one-time setup (e.g., `IModelApp` startup).
- Keep each `it` block focused on a single behaviour.
- Prefer `await vi.waitFor(() => { ... })` over manual delays when waiting for async updates in React components.

## Assertions
- Prefer `expect(value).toBe(...)`, `expect(value).toEqual(...)`, and `expect(fn).toHaveBeenCalledWith(...)`.
- Use `expect(element).to.exist` when checking DOM element presence with @testing-library.
- Use `screen.getByTestId`, `screen.queryAllByTestId`, `screen.getByText` to query the rendered DOM.

## RPC / Service Mocking
- Mock RPC clients via `vi.spyOn(SomeRpcInterface, 'getClient').mockReturnValue({ method: vi.fn() } as any)`.
- Assign mock return values close to where they are used (in `beforeEach` or inline) so intent is clear.

## What Not to Do
- Do not mock `getLocalized` or similar pure i18n/formatting helpers — let them run for real.
- Do not create manual plain-object iModel mocks when `BlankConnectionHelper` is available.
- Do not leave unused mocks or stubs in the file.
- Do not use `jest` APIs — this project uses `vitest` exclusively.
