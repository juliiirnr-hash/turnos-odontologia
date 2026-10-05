# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| writing Python tests, setting up test suites, TDD | python-testing-patterns | C:\Users\Cara Palida\.agents\skills\python-testing-patterns\SKILL.md |
| designing a new service/component, refactoring a God class, layering responsibilities | python-design-patterns | C:\Users\Cara Palida\.agents\skills\python-design-patterns\SKILL.md |
| building async APIs, concurrent I/O, async/await | async-python-patterns | C:\Users\Cara Palida\.agents\skills\async-python-patterns\SKILL.md |
| writing new code, reviewing style, configuring linters, docstrings | python-code-style | C:\Users\Cara Palida\.agents\skills\python-code-style\SKILL.md |
| debugging slow Python code, optimizing bottlenecks | python-performance-optimization | C:\Users\Cara Palida\.agents\skills\python-performance-optimization\SKILL.md |
| validation logic, exception strategies, batch failures, robust APIs | python-error-handling | C:\Users\Cara Palida\.agents\skills\python-error-handling\SKILL.md |
| anything that lives in Postgres: schema, migrations, RLS, indexes, slow queries | supabase-postgres-best-practices | C:\Users\Cara Palida\.agents\skills\supabase-postgres-best-practices\SKILL.md |
| designing or reviewing a PostgreSQL-specific schema | postgresql-table-design | C:\Users\Cara Palida\.agents\skills\postgresql-table-design\SKILL.md |
| writing, reviewing, or refactoring React code for performance | vercel-react-best-practices | C:\Users\Cara Palida\.agents\skills\vercel-react-best-practices\SKILL.md |
| refactoring components with boolean props, component libraries, reusable APIs | vercel-composition-patterns | C:\Users\Cara Palida\.agents\skills\vercel-composition-patterns\SKILL.md |
| working with Vite projects, vite.config.ts, plugins, library/SSR builds | vite | C:\Users\Cara Palida\.agents\skills\vite\SKILL.md |
| creating component libraries, design systems, UI patterns with Tailwind | tailwind-design-system | C:\Users\Cara Palida\.agents\skills\tailwind-design-system\SKILL.md |
| complex type logic, reusable type utilities, compile-time type safety | typescript-advanced-types | C:\Users\Cara Palida\.agents\skills\typescript-advanced-types\SKILL.md |
| automating browser interactions, testing web pages, Playwright tests | playwright-cli | C:\Users\Cara Palida\.agents\skills\playwright-cli\SKILL.md |
| writing Playwright tests, fixing flaky tests, POM, CI/CD, mocking | playwright-best-practices | C:\Users\Cara Palida\.agents\skills\playwright-best-practices\SKILL.md |
| testing local webapps, debugging UI, screenshots, browser logs | webapp-testing | C:\Users\Cara Palida\.agents\skills\webapp-testing\SKILL.md |
| creating optimized multi-stage Dockerfiles | multi-stage-dockerfile | C:\Users\Cara Palida\.agents\skills\multi-stage-dockerfile\SKILL.md |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### python-testing-patterns
- Structure tests with AAA (Arrange/Act/Assert); one behavior per test, no shared state between tests
- Name tests `test_<unit>_<scenario>_<expected>` (e.g. `test_create_user_with_duplicate_email_raises_conflict`)
- Organize as `tests/conftest.py` (shared fixtures) + `test_unit/`, `test_integration/`, `test_e2e/`
- FastAPI: test endpoints with `httpx.AsyncClient` + `ASGITransport`, never a live server
- Mock external deps (WhatsApp/Mercado Pago/AFIP) with `unittest.mock`; use `freezegun.freeze_time` for time-dependent logic (turnos, recordatorios)
- Mark slow/integration tests (`@pytest.mark.slow`, `@pytest.mark.integration`); run `pytest -m "not slow"` by default
- Assert domain status codes: 409 solapamiento, 422 validación; test error paths, not just happy paths

### python-design-patterns
- KISS: simplest solution that works; complexity must be justified by concrete requirements
- One reason to change per unit (SRP); dependency direction is strictly API → Service → Repository, never upward
- Prefer composition over inheritance; keep composition shallow (2-3 levels)
- Rule of three: no abstraction before 3 instances — unless divergent copies already cause bugs
- Functions 20-50 lines, one purpose; constructor injection for testability (7+ params = split the class)
- Delete dead code before abstracting; explicit over clever

### async-python-patterns
- Stay fully sync or fully async within a call path — never mix; FastAPI endpoints + SQLAlchemy async engine
- Never block the loop: `await asyncio.sleep`, never `time.sleep`; CPU work goes to `asyncio.to_thread()`
- Concurrent independent I/O with `asyncio.gather(*tasks)`; use `return_exceptions=True` + filter for batch ops
- Always `await` coroutines; handle `CancelledError` with cleanup + re-raise
- Bound concurrency with `asyncio.Semaphore` for fan-out (recordatorios masivos, notificaciones)
- Test async code with `pytest-asyncio` (`@pytest.mark.asyncio`); timeout with `asyncio.wait_for`

### python-code-style
- `ruff check --fix .` + `ruff format .`; line-length 120; target py312; strict mypy (`disallow_untyped_defs = true`)
- snake_case functions/vars, PascalCase classes, SCREAMING_SNAKE_CASE constants; absolute imports only, grouped stdlib → third-party → local
- Type hints on all public APIs; Google-style docstrings on all public functions/classes (Args/Returns/Raises/Example)
- Never `except Exception: pass`; never relative imports (`from ..utils import x`)

### python-performance-optimization
- Profile before optimizing (`cProfile`, `py-spy` in prod); optimize hot paths (agenda queries, reportes) first
- Kill N+1 queries: SQLAlchemy `selectinload`/`joinedload`; use connection pooling; batch I/O
- Prefer built-ins (C-implemented), dict/set for lookups, generators for large datasets, `functools.lru_cache` for expensive pure computation
- Measure with `timeit`, not `time.time()`; never optimize rare code paths at clarity's expense

### python-error-handling
- Validate early at API boundaries (fail fast); report all validation errors at once when possible
- Use Pydantic models (`BaseModel`, `Field`, `field_validator`) for structured input validation in FastAPI
- Map failures to specific exceptions: `ValueError` bad input, `TypeError` wrong type, `KeyError` missing item — never bare `Exception("...")`
- Parse strings to domain Enums early (e.g. estado de turno); messages must say what failed, why, and valid options
- Chain with `raise ... from e`; batch ops track successes/failures separately, one item never aborts the batch
- Document failure modes in docstrings (Raises:); test error paths

### supabase-postgres-best-practices
- Load BEFORE any Postgres change, even one column or one query; rules prioritized: query perf > connections > RLS/security > schema
- Never `SELECT *`; index FK columns manually (Postgres does NOT auto-index them); prefer partial indexes for hot subsets (`WHERE estado = 'activo'`)
- Multi-tenant isolation via RLS policies + tests verifying cross-tenant invisibility; never trust app-layer filtering alone
- Diagnose slowness with `EXPLAIN (ANALYZE, BUFFERS)`; watch for sequential scans on large tables, connection exhaustion (use pooling)
- Details per rule in `references/` (e.g. `references/query-missing-indexes.md`)

### postgresql-table-design
- PK: `BIGINT GENERATED ALWAYS AS IDENTITY` (UUID only for distributed/opaque IDs); always `NOT NULL` where semantically required + `DEFAULT`s
- Types: `TIMESTAMPTZ` for time (never `timestamp`), `NUMERIC(p,s)` for money (never `money`/`float`), `TEXT` for strings (never `varchar(n)`), `BOOLEAN NOT NULL`, `JSONB` (never `JSON`) with GIN only for optional attrs
- Anti-solapamiento de turnos: `EXCLUDE USING gist (profesional_id WITH =, rango WITH &&)` — GiST, not app checks
- Enums (`CREATE TYPE ... AS ENUM`) only for small stable sets; evolving business values → `TEXT` + `CHECK` or lookup table
- snake_case unquoted identifiers; UNIQUE allows multiple NULLs — use `UNIQUE NULLS NOT DISTINCT` (PG15+) to forbid; sequences have gaps (normal, never "fix")
- Index real access paths: FKs, filters/sorts, join keys; composite = most selective first, leftmost-prefix applies; covering via `INCLUDE (...)`

### vercel-react-best-practices
- Kill waterfalls: `Promise.all()` for independent fetches; start promises early, await late; Suspense boundaries for streaming
- Never import from barrel files — import modules directly; `next/dynamic` (or `React.lazy`) for heavy components; defer analytics/logging until after hydration
- Memoize expensive subtrees only (`memo` + primitive deps); never define components inside components; derive state during render, not in effects
- Interaction logic in event handlers, not effects; `startTransition`/`useDeferredValue` to keep agenda inputs responsive
- `Set`/`Map` for O(1) lookups; cache localStorage reads; `content-visibility` for long lists (agenda semanal)

### vercel-composition-patterns
- Never add boolean props to customize behavior — compose instead (`<Card><Card.Header/>…</Card>`)
- Compound components share state via context provider; provider is the ONLY place that knows how state is managed
- Explicit variant components over boolean modes (`<PrimaryButton/>` not `<Button primary/>`); `children` over `renderX` props
- Lift shared state into provider so siblings access it without prop drilling
- React 19+: no `forwardRef` (ref is a regular prop); `use()` instead of `useContext()`

### vite
- `vite.config.ts` with `defineConfig`, ESM only (no CommonJS); alias `@` → `/src`; dev proxy `/api` → backend
- Dev `vite`, build `vite build`, preview `vite preview`; env vars via `import.meta.env` (must be prefixed `VITE_*`)
- Static assets: `import.meta.glob`, `?raw`/`?url` queries; HMR via `import.meta.hot`
- React plugin: `@vitejs/plugin-react`; lazy routes with `React.lazy` + dynamic `import()` for code splitting
- Vite 8 = Rolldown bundler + Oxc transformer; check `references/rolldown-migration.md` when touching build config

### tailwind-design-system
- Tailwind v4: CSS-first config — `@import "tailwindcss"` + `@theme { --color-*: … }` in CSS; NO `tailwind.config.ts`
- Tokens hierarchy brand → semantic → component; colors in OKLCH; dark mode via `@custom-variant dark (&:where(.dark, .dark *))` + `.dark` overrides
- Semantic utilities only (`bg-primary text-foreground`), never raw hex in markup; radius/animate tokens from `@theme`
- Component order: base → variants → sizes → states → overrides; responsive mobile-first (`md:`/`lg:` up); focus-visible rings required
- Entry animations: CSS `@keyframes` in `@theme` + `@starting-style`; no JS animation libs for simple transitions

### typescript-advanced-types
- `unknown` over `any` always; `strict: true` + strict null checks; `interface` for object shapes, `type` for unions/complex logic
- Domain modeling: discriminated unions for turno states (`programado | confirmado | cancelado | ...`) to get narrowing; `Pick`/`Omit` for DTOs (`Omit<Turno,'id'>` for create input)
- Let inference work; `as` casts forbidden — use type guards; `NonNullable<T>` at boundaries; `Record<K,T>` for keyed maps
- Keep conditional/mapped types shallow (perf); document complex helpers with JSDoc; test tricky types with `AssertEqual<T,U>` assertions

### playwright-cli
- Drive via refs from `snapshot`: `open <url>` → `snapshot` → `click e3` / `fill e5 "…" --submit`; `find "text"` to grep large snapshots
- Never screenshot for state — snapshot is the source of truth; `--raw` for piped output, `--filename=` when results are large
- Auth reuse: `state-save auth.json` / `state-load auth.json`; mock APIs with `route "<url>" --body='…'`; `console` + `requests` for debugging
- Mobile-first project: prefer `open --mobile` for cheaper snapshots; Windows PowerShell URLs with `&` need `--%`
- Multi-tab: `tab-new` / `tab-list` / `tab-select`; always `close` when done

### playwright-best-practices
- Locators: `getByRole`/`getByTestId` only — never CSS/XPath brittle selectors; auto-waiting assertions, never `wait_for_timeout`
- Page Object Model per page (agenda, reserva, login); fixtures for setup, `test-data` factories; storage state for auth, never UI login per test
- Tag critical flows `@smoke`/`@critical` (reserva/confirmación/cancelación); filter with `--grep`; repeat flaky suspects `--repeat-each=5`
- Isolate tests: unique data per test, no shared state, no parallel-order dependence; mock third parties (MP/WhatsApp) via network interception
- Debug loop: `npx playwright test --reporter=list` → trace on failure → fix locator/wait/assertion → re-run green before proceeding

### webapp-testing
- Python Playwright scripts with `sync_playwright()`, headless Chromium, `browser.close()` always
- Dynamic apps: `page.wait_for_load_state('networkidle')` BEFORE any DOM inspection — never inspect pre-hydration DOM
- Server lifecycle via black-box helper: `python scripts/with_server.py --help` first, then `--server "…" --port N -- python script.py`; never read helper source unless `--help` fails
- Reconnaissance-then-action: screenshot/DOM → identify selectors (`text=`/`role=`/IDs) → act; static HTML → `file://` URL directly

### multi-stage-dockerfile
- Stages ordered dependencies → build → test → runtime; named stages (`AS builder`); copy ONLY runtime artifacts into final stage
- Pinned minimal bases (`python:3.12-slim`, `node:22-alpine`), exact tags never `latest`; `NODE_ENV=production` in runtime
- Least-to-most-frequently-changing layer order for cache; combine `RUN … && …`; `.dockerignore` mandatory; `COPY --chown` for perms
- Never root in runtime: `USER appuser`; strip build tools/secrets from final image; `HEALTHCHECK` per service (api/web)

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| (none — CLAUDE.md/AGENTS.md deleted for interactive redo) | — | Conventions section intentionally empty |

No convention files found at project root (checked: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, copilot instructions). Re-run will pick them up once created.
