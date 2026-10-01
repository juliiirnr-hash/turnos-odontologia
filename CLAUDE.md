# Turnos Odontología — Instrucciones para Agentes

> Este archivo (y su copia `CLAUDE.md`) es lo PRIMERO que todo agente lee al entrar al repo.
> Generado a partir de `knowledge-base/` y `CHANGES.md`. No editar a mano sin re-sincronizar ambos archivos.

---

## Stack Tecnológico

| Capa | Tecnología | Versión mínima |
|---|---|---|
| Frontend | React + TypeScript + Vite (SPA) | React 18, TS 5, Vite 5 |
| Backend | Python + FastAPI | Python 3.12, FastAPI 0.110+ |
| Auth | JWT (access corto + refresh) | PyJWT / python-jose |
| ORM / migraciones | SQLAlchemy 2.0 + Alembic | 2.0 / 1.13+ |
| Base de datos | PostgreSQL (driver asyncpg) | 16 |
| Async / worker | Redis + Celery (fase 2; v1.0 sin worker) | Redis 7 |
| Almacenamiento | Disco local / S3-compatible | — |
| PDF / Excel | reportlab o weasyprint + openpyxl | — |
| Tests | pytest + httpx (backend); Vitest + Playwright (frontend) | — |
| Entornos | Docker + Docker Compose | — |

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md)

---

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. **Leé el archivo relevante ANTES de implementar.**

| Archivo | Cuándo leerlo |
|---------|---------------|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Entender propósito y alcance (MVP v1.0 = agenda + clínica + caja) |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Auth, RBAC, permisos |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Entidades, ERD, migraciones |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas codificadas (RN-AG/TU/CL/CA/AU/SEG/GLB) |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario por épica (US-001…US-043) |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos E2E (reserva, atención, caja, cancelación, recordatorio) |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, estructura backend/frontend, env vars |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | ⚠️ Inconsistencias a resolver ANTES de codear |

> ⚠️ Resolver las preguntas de prioridad **Alta** de `10_preguntas_abiertas.md` (JWT storage, worker Celery/ARQ, multisillón día 1, hosting) antes de arrancar el primer change.

---

## Skills Disponibles

| Agente | Rol | Skills que carga |
|--------|-----|------------------|
| **Backend Core** | FastAPI, SQLAlchemy, Alembic, Postgres | `postgresql-table-design`, `supabase-postgres-best-practices`, `nodejs-backend-patterns` (patrones transferibles), `nestjs-best-practices` (patrones transferibles) |
| **Backend Aux** | Auth JWT, testing API | `better-auth-best-practices` (roles y sesiones, adaptar a JWT propio), `webapp-testing` |
| **Frontend** | React + TS + Vite + Tailwind | `vercel-react-best-practices`, `vercel-composition-patterns`, `typescript-advanced-types`, `nextjs-react-typescript` (patrones React, no App Router), `tailwind-design-system`, `setup-ts-deep-modules` |
| **E2E / Calidad** | Flujos de reserva, caja | `playwright-cli`, `playwright-best-practices` |
| **Deploy** | Frontend como SaaS | `deploy-to-vercel` |
| **Orquestación** | SDD / OPSX / docs | `kb-creator`, `roadmap-generator`, `agents-md-generator` |

> Los compact rules de cada skill los resuelve el orquestador desde `.atl/skill-registry.md` (generado por `skill-registry`; no versionado — no está en el repo). Esta tabla solo mapea skill→rol. Nota: las skills NestJS/Prisma/Node aplican como patrones transferibles al backend FastAPI — nunca importar su código.

---

## Roadmap de Changes

El plan de implementación completo está en [CHANGES.md](CHANGES.md). Resumen:

- **Total**: 14 changes en 6 fases (C-01…C-14).
- **Camino crítico** (9): `C-01 → C-02 → C-03 → C-04 → C-05 → C-06 → C-10 → C-11 → C-14`.
- **Primer change**: `C-01` (foundation-setup: backend FastAPI + frontend Vite + Compose).

**Antes de cualquier `/opsx:propose`**: leé [CHANGES.md](CHANGES.md), identificá las dependencias del change y los archivos de "Leer antes".

---

## Reglas Duras

> Reglas globales ya definidas en `~/.claude/CLAUDE.md` (orquestador, governance, TDD, engram): el proyecto las hereda. Acá viven solo las reglas **específicas de este proyecto** + las universales que el global no cubre.

1. NUNCA exponer modelos SQLAlchemy en responses → schemas Pydantic de respuesta (sin password_hash, tokens ni columnas de auditoría).
2. NUNCA endpoint de dominio sin dependencia de tenant → toda consulta filtra por `tenant_id` (RN-AU-02).
3. NUNCA schema sin migración → cambios de modelo van con revisión Alembic versionada por change.
4. NUNCA JWT inseguro → access token en memoria del frontend, refresh rotativo en cookie httpOnly (secure, samesite=lax).
5. NUNCA cerrar un change con tests en rojo → pytest + httpx en verde para el módulo tocado.
6. NUNCA `any` en TypeScript → tipado estricto; componentes en PascalCase.
7. NUNCA llamadas al API por fuera del api client central → baseURL, header auth y manejo 401/409/422 en un solo lugar.
8. NUNCA UI solo-desktop → mobile-first, español rioplatense, zona America/Argentina/Cordoba.
9. NUNCA buildear, commitear ni pushear sin pedido explícito del usuario.
10. Commits en conventional commits, sin co-autoría de IA en el mensaje.

---

## Flujo de Trabajo

```
1. Leer la KB relevante (knowledge-base/)        → entender el dominio
2. Identificar el change en CHANGES.md           → respetar dependencias
3. /opsx:propose C-NN-nombre                     → proposal + design + specs + tasks
4. Implementar las tasks (cargando skills)       → respetando las reglas duras
5. /opsx:archive C-NN-nombre + marcar [x]        → cerrar el change
```

Aplicar TODAS las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, las reglas duras prevalecen.
