---
description: Always use full, descriptive names for variables, functions, parameters, classes, and other identifiers across all code. Never abbreviate, truncate, or use short forms.
applyTo: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.py,**/*.cs,**/*.java,**/*.go,**/*.rs,**/*.rb,**/*.php,**/*.swift,**/*.kt,**/*.cpp,**/*.c,**/*.h,**/*.hpp,**/*.scala,**/*.sql"
---

# Descriptive Naming Only

Every identifier you introduce or suggest — variables, function/method names, parameters,
class/interface/type names, properties, file names — must use full, descriptive words. Never
abbreviate, truncate, or drop vowels to save characters.

## Rules

- Spell out full words instead of shortening them:

  | Avoid | Use |
  |---|---|
  | `idx`, `j`, `k` (as loop counters beyond a single simple loop) | `index`, `rowIndex`, `columnIndex` |
  | `btn` | `button` |
  | `cfg`, `conf` | `configuration` |
  | `req`, `res` | `request`, `response` |
  | `err` | `error` |
  | `msg` | `message` |
  | `param`, `arg` | `parameter`, `argument` |
  | `ctx` | `context` |
  | `el`, `elem` | `element` |
  | `comp` | `component` |
  | `mgr` | `manager` |
  | `svc` | `service` |
  | `impl` | `implementation` |
  | `util`, `utils` | `utility`, `utilities` |
  | `tmp`, `temp` | `temporary` |
  | `num`, `cnt` | `number`, `count` |
  | `str` | `string` (or the actual meaning it holds, e.g. `userName`) |
  | `obj` | `object` (or the actual meaning it holds, e.g. `userProfile`) |
  | `arr` | `array` (or the actual meaning it holds, e.g. `selectedItems`) |

- Avoid single-letter identifiers, including lambda parameters — write `item`, `accumulator`,
  `columnIndex`, not `a`, `acc`, `j`. The only single-letter exceptions are `i`, `x`, `y`
  (see Exceptions below).
- Function and method names must describe the full action and subject: `calculateTotalPrice`,
  not `calcTotPrice` or `calcPrice`.
- Boolean names should read as a complete predicate: `isVisible`, `hasPermission`,
  `shouldRetry` — not `vis`, `perm`, `retry`.
- Prefer clarity over brevity even when it makes a name longer. Do not shorten a name just
  because a shorter alternative exists.

## Exceptions — do not rewrite these

- Single-letter `i`, `x`, `y` — allowed for a simple loop counter or coordinate/position value.
  Nothing else (no `j`, `k`, `z`, `n`, `t`, etc.) — those still need a full name, e.g.
  `rowIndex`/`columnIndex` for nested loops. Keep this list to just these three for now.
- Identifiers required by an external API, framework, or library you don't control (e.g., a
  destructured field from a third-party response, a parameter name mandated by a framework
  lifecycle hook).
- Terms that are already the full, standard word for the concept, not an abbreviation of a
  longer one: `id`, `url`, `api`, `html`, `css`, `sql`, `ui`, `io`.
- Pre-existing code outside the scope of the current change — don't perform drive-by renames
  unrelated to the task at hand.

## Applying This

Before writing any variable, function, parameter, or type name, mentally expand it to its full
form. If tempted to abbreviate for brevity, don't — use the longer, descriptive name every time.
