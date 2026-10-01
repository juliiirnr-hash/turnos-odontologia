# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| React components, Next.js pages, data fetching, bundle optimization, performance improvements | vercel-react-best-practices | C:\Users\Cara Palida\.agents\skills\vercel-react-best-practices\SKILL.md |
| Compound components, render props, context providers, component architecture, boolean prop proliferation | vercel-composition-patterns | C:\Users\Cara Palida\.agents\skills\vercel-composition-patterns\SKILL.md |
| TypeScript repo module boundaries (user-invoked setup) | setup-ts-deep-modules | C:\Users\Cara Palida\.agents\skills\setup-ts-deep-modules\SKILL.md |
| Complex type logic, reusable type utilities, compile-time type safety | typescript-advanced-types | C:\Users\Cara Palida\.agents\skills\typescript-advanced-types\SKILL.md |
| TypeScript, Node.js, Next.js App Router, React, Shadcn UI, Radix UI, Tailwind | nextjs-react-typescript | C:\Users\Cara Palida\.agents\skills\nextjs-react-typescript\SKILL.md |
| NestJS modules, controllers, services, DI, security, performance | nestjs-best-practices | C:\Users\Cara Palida\.agents\skills\nestjs-best-practices\SKILL.md |
| NestJS backend — modules, providers, DTO validation, guards, interceptors | nestjs-patterns | C:\Users\Cara Palida\.agents\skills\nestjs-patterns\SKILL.md |
| Node.js servers, REST APIs, GraphQL backends, microservices | nodejs-backend-patterns | C:\Users\Cara Palida\.agents\skills\nodejs-backend-patterns\SKILL.md |
| Prisma setup (deprecated stub — use prisma-orm-setup) | prisma-database-setup | C:\Users\Cara Palida\.agents\skills\prisma-database-setup\SKILL.md |
| Prisma + Postgres (deprecated stub — use prisma-postgres-setup) | prisma-postgres | C:\Users\Cara Palida\.agents\skills\prisma-postgres\SKILL.md |
| Postgres schema, migrations, RLS, indexes, slow queries, connection issues | supabase-postgres-best-practices | C:\Users\Cara Palida\.agents\skills\supabase-postgres-best-practices\SKILL.md |
| PostgreSQL-specific schema design/review: types, keys, constraints, indexes | postgresql-table-design | C:\Users\Cara Palida\.agents\skills\postgresql-table-design\SKILL.md |
| Better Auth, betterauth, auth.ts, email/password, OAuth, plugins | better-auth-best-practices | C:\Users\Cara Palida\.agents\skills\better-auth-best-practices\SKILL.md |
| Browser automation, web page interaction, Playwright tests | playwright-cli | C:\Users\Cara Palida\.agents\skills\playwright-cli\SKILL.md |
| Playwright tests, flaky tests, POM, CI/CD, auth, a11y, mobile, security testing | playwright-best-practices | C:\Users\Cara Palida\.agents\skills\playwright-best-practices\SKILL.md |
| Testing local web apps with Playwright, debugging UI, screenshots, browser logs | webapp-testing | C:\Users\Cara Palida\.agents\skills\webapp-testing\SKILL.md |
| Component libraries, design systems, design tokens, UI patterns (Tailwind v4) | tailwind-design-system | C:\Users\Cara Palida\.agents\skills\tailwind-design-system\SKILL.md |
| Deploy app, push live, preview deployment (Vercel) | deploy-to-vercel | C:\Users\Cara Palida\.agents\skills\deploy-to-vercel\SKILL.md |

> Stack note: project backend is Python/FastAPI/SQLAlchemy (not NestJS/Prisma/Node). The nestjs-*, nodejs-*, and prisma-* skills apply as **transferable patterns** (module boundaries, DTO validation, error shape, migration discipline) adapted to FastAPI — never import NestJS/Prisma code.

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### vercel-react-best-practices
- Eliminate waterfalls: parallelize independent fetches with `Promise.all()`, start promises early / await late, use Suspense boundaries for streaming
- Never import barrel files — import components/modules directly; use `next/dynamic` for heavy components, load third-party/analytics only after hydration
- Server: use `React.cache()` for per-request dedup, minimize data serialized to client components, never keep mutable request state at module level
- Client: use SWR (request dedup), passive listeners for scroll, versioned/minimal localStorage payloads
- Re-renders: derive state during render (not in effects), primitive effect deps, `startTransition`/`useDeferredValue` for non-urgent updates, never define components inside components
- Prefer ternary over `&&` for conditionals; hoist static JSX; use `content-visibility` for long lists

### vercel-composition-patterns
- Never add boolean props to customize behavior — use composition (compound components + shared context)
- Create explicit variant components instead of boolean mode props (e.g. `PrimaryButton`, not `<Button primary>`)
- Provider is the only place that knows how state is managed; define generic `{ state, actions, meta }` context interface for injection
- Lift shared state into provider components for sibling access; prefer `children` over `renderX` props
- React 19+: no `forwardRef` (ref is a regular prop); use `use()` instead of `useContext()`

### setup-ts-deep-modules
- Each package is a deep module: public surface = root entry-point files only (`index.ts`, `client.ts`…); everything in subfolders (`lib/`, `tests/`) is private
- Outside code (app or other packages) may import only a package's root entry points, never subfolder internals
- Tests under `<pkg>/tests/` import only entry points (own or others') plus own fixtures — never deep internals
- No dependency cycles; barrels re-exporting whole subtrees are discouraged — keep entry points small
- Enforce with dependency-cruiser + `lint:boundaries` script wired into the same check command as typecheck (user-invoked setup, not automatic)

### typescript-advanced-types
- Prefer generics with constraints (`<T extends HasLength>`) for reusable type-safe utilities; infer where possible instead of explicit type args
- Use conditional types (`T extends U ? A : B`), mapped types, and template literal types for derived/domain types (turnos, planes, liquidaciones)
- Prefer `interface` over `type` for object shapes; avoid enums — use maps or string-literal unions
- Model domain states as discriminated unions so impossible states are unrepresentable at compile time
- Never use `any` — use `unknown` + narrowing; keep reusable utilities in a shared types module, not duplicated per file

### nextjs-react-typescript
- Functional/declarative patterns only — no classes; `function` keyword for pure functions; named exports for components
- File order: exported component, subcomponents, helpers, static content, types; lowercase-with-dashes directories
- Interfaces over types; no enums (use maps); descriptive boolean names (`isLoading`, `hasError`)
- Minimize `'use client'`, `useEffect`, `useState` — prefer Server Components; wrap client components in Suspense with fallback; dynamic-load non-critical components
- Shadcn UI + Radix + Tailwind mobile-first; `nuqs` for URL search-param state; optimize images (WebP, sizes, lazy); watch Web Vitals (LCP, CLS, FID)

### nestjs-best-practices
- Organize by feature module, not technical layer; avoid circular module deps; one focused service per responsibility (no god services)
- Constructor injection only (no service-locator); depend on interface tokens (ISP/LSP); respect singleton/request/transient scopes
- Centralize errors with exception filters; throw NestJS HTTP exceptions; always handle async errors
- Validate ALL input with class-validator; guard authN/authZ; sanitize output (XSS); rate-limit public endpoints
- Use transactions, avoid N+1, migrate schema via migrations; version APIs; serialize responses via DTOs/interceptors; structured logging + graceful shutdown

### nestjs-patterns
- Thin controllers: parse HTTP input → call provider → return response DTO; business logic lives in injectable services
- One global `ValidationPipe` with `whitelist: true, forbidNonWhitelisted: true, transform: true` — never repeat per route
- Every request DTO validated with class-validator; never return ORM entities — dedicated response DTOs/serializers, strip secrets (hashes, tokens, audit cols)
- Coarse access in guards (`JwtAuthGuard`, `RolesGuard`), resource-specific checks in services; keep guards module-local unless truly shared
- Global exception filter → uniform error shape; cross-cutting filters/guards/interceptors in `common/`; DTOs next to owning module

### nodejs-backend-patterns
- TypeScript everywhere; validate input with Zod/Joi; custom error classes + centralized error middleware
- Secrets only via env vars; structured logging (Pino/Winston); rate limiting; CORS never `*` in production; HTTPS in production
- Connection pooling for DB; health-check endpoint; graceful shutdown (drain connections); compression; APM monitoring
- DI for testability; unit + integration + E2E tests; background jobs via queues, never blocking request handlers
- Detailed patterns live in the skill's `references/details.md` — read it when the summary above is insufficient

### prisma-database-setup
- DEPRECATED stub: contains no recipes — load `prisma-orm-setup` instead (prisma/skills: `prisma-orm-setup`), covering Prisma 6/7/8 setup and connection repair
- If `prisma-orm-setup` is not installed, install it before continuing; keep this entry until consumers migrate

### prisma-postgres
- DEPRECATED stub: contains no recipes — load `prisma-postgres-setup` instead (prisma/skills: `prisma-postgres-setup`)
- If `prisma-postgres-setup` is not installed, install it before continuing; keep this entry until consumers migrate

### supabase-postgres-best-practices
- Load BEFORE any Postgres schema/query/migration/RLS change — even one column or one query
- Query perf is priority 1: index actual access paths (FK columns manually — PG does not auto-index them), prefer partial/expression/covering indexes, check EXPLAIN plans
- Connection management is priority 2: pool connections (PgBouncer/pooler), never open unbounded per-request connections
- RLS: every tenant/health-data table gets policies + tests proving cross-tenant invisibility; never rely on app-layer filtering alone
- Schema: normalize first, explicit `ON DELETE/UPDATE` on FKs, `TIMESTAMPTZ` for time, `NUMERIC` for money; migrations declarative + reversible
- Read the specific `references/*.md` rule file for the task at hand (query, conn, security, schema, lock, data, monitor, advanced)

### postgresql-table-design
- PK: `BIGINT GENERATED ALWAYS AS IDENTITY` (ref tables); `UUID` (uuidv7) only for distributed/opaque IDs; never `serial`
- Types: `TIMESTAMPTZ` (never bare `timestamp`), `NUMERIC` for money (never `money`), `TEXT` + `CHECK (length<=n)` (never `varchar(n)`/`char(n)`), `BOOLEAN NOT NULL`, small stable enums as PG ENUM else `TEXT`+`CHECK`/lookup table, `JSONB`+GIN only for optional semi-structured attrs
- `NOT NULL` everywhere semantically required; `UNIQUE NULLS NOT DISTINCT` (PG15+) when a single NULL must be unique
- Prevent double-booking with `EXCLUDE USING gist (resource WITH =, period WITH &&)` — directly applicable to turnos anti-solapamiento
- Indexing: composite leftmost-prefix, partial for hot subsets (`WHERE estado='activo'`), expression must match query text, GIN for JSONB/arrays/FTS, BRIN for ordered time-series
- Conventions: `snake_case` unquoted identifiers; identity gaps and MVCC dead tuples are normal — don't "fix"

### better-auth-best-practices
- Pin docs to the installed `better-auth` version (lockfile → version → matching docs); separate current-version from target-version guidance on upgrades
- Setup: `BETTER_AUTH_SECRET` (≥32 chars) + `BETTER_AUTH_URL` env; `auth.ts` in `./ lib/ utils/ src/`; route handler; migrate (`npx auth@latest migrate`, or `generate` + drizzle-kit/prisma migrate); verify `GET /api/auth/ok`
- Re-run generate/migrate after adding/changing plugins; adapter `modelName` = ORM model name, NOT table name
- Sessions: `secondaryStorage` (Redis/KV) takes over storage; `cookieCache` compact/jwt/jwe; tune `expiresIn`/`updateAge`; bump `cookieCache.version` to invalidate all
- AuthZ for roles (paciente/odontólogo/recepcionista/dueño): `user.additionalFields` + endpoint/database hooks; never disable CSRF/origin checks; rate-limit auth endpoints

### playwright-cli
- `open [url]` → `snapshot` (read refs) → `click/fill/select/check e<N>` → `snapshot` to verify; `close` when done
- Find elements with `find "text"` / `find --regex "/pattern/i"` (save to file with `--filename` on many matches); read hidden attrs via `eval "el => el.getAttribute(...)" e<N>`
- Forms: `fill eN "value" --submit` presses Enter; `upload`/`drop` for files; `press Enter`; `hover`; `drag eA eB`
- Dialogs: `dialog-accept ["text"]` / `dialog-dismiss`; navigation: `go-back/go-forward/reload`; `resize W H` for viewports
- Debug via `snapshot` + `eval "document.title"` / element expressions — screenshots only when snapshot is insufficient

### playwright-best-practices
- Locators: role/label/placeholder/testid first — never CSS-class or XPath; auto-waiting assertions (`expect(locator).toBeVisible()`), never `sleep`/`waitForTimeout`
- Structure: Page Object Model per page/flow; fixtures + hooks for setup/teardown; isolated test data per test (no shared mutable state → no flakes)
- Auth: authenticate once in global setup, reuse storage state across tests; mock third-party (payments, email, WhatsApp) — never hit real services
- Booking flows: mock clock for recordatorios/antelación tests; test mobile viewports + touch for the mobile-first reserva UI; cover multi-tab (pagos) explicitly
- CI: shard + retry only genuinely flaky infra failures, quarantine with `fixme` + ticket; tag `@smoke/@critical` and filter with `--grep`; fail on console errors

### webapp-testing
- Test dynamic apps with native Python Playwright scripts (sync API, headless Chromium), never by reading source HTML alone
- Server lifecycle via `scripts/with_server.py` (supports multiple servers: backend + frontend); always run scripts with `--help` first; treat helpers as black boxes — don't read their source unless customization is proven necessary
- Pattern: `goto` → `wait_for_load_state('networkidle')` → screenshot/DOM recon → identify selectors → act (never inspect DOM before networkidle)
- Static HTML: read file directly for selectors; dynamic: recon-then-action loop above

### tailwind-design-system
- Tailwind v4 is CSS-first: `@import "tailwindcss"` + `@theme { --color-*: … }` — no `tailwind.config.ts`, no `@tailwind base/components/utilities`
- Semantic tokens (`--color-primary/foreground`, `--color-muted…`, `--radius-*`, `--animate-*` with `@keyframes` inside `@theme`); OKLCH colors; dark mode via `@custom-variant dark (&:where(.dark, .dark *))`
- Build variant-driven components (explicit variants, not boolean props); responsive + accessible by default; entry animations via `@starting-style`
- v3→v4: `theme.extend.colors` → `@theme`, `darkMode:"class"` → custom variant, `tailwindcss-animate` → CSS keyframes

### deploy-to-vercel
- Default to **preview** deployments — production only on explicit user request
- First gather state (all four): git remote, `.vercel/project.json` or `repo.json` (linked?), `vercel whoami` (authed?), `vercel teams list`
- Linked + git remote → ask before pushing, then commit+push (Vercel builds automatically); unlinked → link/deploy flow toward permanent git integration
- Multi-team: ask which team slug, pass `--scope <slug>` on all CLI commands; existing link's `orgId` decides — don't re-ask
- Never run `vercel project inspect`/`ls`/`link` to probe an unlinked dir (side-effect linking) — only `whoami` is safe; get preview URL from `vercel ls --format json` (`deployments[].url`) or dashboard

## Project Conventions

No project convention files found (first foundation pass — CLAUDE.md/AGENTS.md do not exist yet). This section is intentionally empty.

| File | Path | Notes |
|------|------|-------|
| (none) | — | No AGENTS.md, CLAUDE.md, .cursorrules, GEMINI.md, or copilot-instructions.md at project root |
