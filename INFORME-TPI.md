# Informe Técnico — Trabajo Práctico de Integración (TPI) · Metodología I

**Proyecto:** `turnos-odontologia` — Sistema de gestión de turnos odontológicos para Argentina
**Autor:** autor principal del TPI
**Fecha:** 2026-10-05
**Estado:** Fundación completa (`step: done`) + 1 change implementado, verificado y archivado

---

## 1. Introducción y Alcance

### 1.1 Producto

Sistema SaaS multi-tenant de gestión odontológica orientado a consultorios y clínicas de Argentina. Problema que resuelve: la coordinación de agenda por WhatsApp/papel genera doble reserva, sillones ociosos, ausentismo no gestionado y caja sin trazabilidad, sin administración local integrada (Mercado Pago, obras sociales/prepagas, facturación AFIP/ARCA).

MVP v1.0 (acordado en Discovery, sección D): agenda multiprofesional y multisillón, reserva online 24/7, odontograma FDI, caja manual con liquidaciones. Fase 2: Mercado Pago, WhatsApp automático, factura electrónica AFIP/ARCA, periodontograma completo.

### 1.2 Herramientas base efectivamente utilizadas

| Herramienta | Versión / Uso verificado |
|---|---|
| Git | Control de versiones del repo |
| Node.js 24 + npm 12 | CLI `skills`, frontend Vite (fase 2 del roadmap) |
| Python 3.12 (target) / 3.14 (entorno local) | Backend FastAPI, pytest, Alembic |
| Docker Desktop 29.5.3 + Compose v5.1.4 | Postgres 16, Redis 7, entorno reproducible |
| OpenCode (agente) | Orquestación de todo el recorrido |
| openspec CLI 1.13.2 | `init`, `new change`, `status`, `validate`, `archive`, `doctor` |
| Active Stack modo Full (skills) | `active-orchestrator`, `discovery-research`, `kb-creator`, `roadmap-generator`, `find-skills`, `skill-registry`, `agent-instruction`, `web-scraper` |

### 1.3 Stack del producto (decidido por el equipo, DD-01)

Backend: Python + FastAPI (JWT, SQLAlchemy 2.0 + Alembic, PostgreSQL async, Redis para async fase 2) en Docker/Docker Compose. Frontend: React + TypeScript + Vite.

---

## 2. Fundación del Proyecto (Etapas 0 a 5)

### 2.1 Etapa 0 — Orquestador y `openspec init`

Se ejecutó `active-orchestrator:init` como orquestador delgado: detectó flujo completo, verificó `openspec --version`, ejecutó `openspec init` (perfil OpenCode, 6 skills + 6 comandos en `.opencode/`), y abrió el estado compartido `.active-orchestrator-state.json` (contrato v4). Cada fase avanzó solo con confirmación explícita (checkpoints entre fases, sin encadenamiento automático).

### 2.2 Etapa 1 — Discovery (investigación de mercado)

Se despachó `discovery-research` con brief del dueño: 19 sistemas odontológicos/de turnos (Argentina, Latam, internacionales), solo fuentes verificables (sitios oficiales, pricing, ayuda, marketplaces), URL + fecha por fuente (2026-09-29).

Rigor aplicado:

- **"No evidenciado"** como valor explícito para toda funcionalidad no demostrada públicamente.
- **Distinción sistemática** entre funcionalidad comprobada y afirmación comercial del proveedor (ej. claims de "−82% ausencias", "−65% ausentismo" marcados como comerciales).
- Resultado en `discovery/discovery.md`: tabla comparativa de 19 sistemas, matriz ponderada 0–5 (turnos+auto 25%, clínica 20 %, integraciones+WA 15 %, admin 15 %, XP 10 %, seguridad 10 %, precio 5 %), análisis de vacíos del mercado argentino (MP+OS+AFIP en un solo flujo, multisillón real, WA API transparente) y MVP sugerido.
- Mejor fit argentino: DentalSoft AR (3,93); mayor completitud global: CareStack (4,63, inviable por precio USD).
- Estado: sección `discovery` completa (problema, usuarios, casos de uso, competidores, funcionalidades, reglas, integraciones, restricciones, riesgos, preguntas abiertas).

### 2.3 Etapa 2 — Base de conocimiento (`kb-creator`, modo interactivo)

Sin `docs/` previos se trabajó desde cero con Q&A estratégica (2 rondas: tipo de sistema, escala, stack, MVP, calidad, auditoría, login de paciente), reutilizando el Discovery para no repreguntar. Generados los **10 canónicos + índice** en `knowledge-base/`:

| Archivo | Contenido |
|---|---|
| `01_vision_y_objetivos.md` | Propósito, objetivos por actor, alcance v1.0, métricas |
| `02_descripcion_general.md` | Stack Python/React, arquitectura con Compose, integraciones, API |
| `03_actores_y_roles.md` | Paciente, odontólogo, recepcionista, dueña; matriz RBAC |
| `04_modelo_de_datos.md` | 5 dominios, 15 entidades, ERD, seed |
| `05_reglas_de_negocio.md` | 20 reglas RN-AG/TU/CL/CA/AU/SEG/GLB |
| `06_funcionalidades.md` | 5 épicas, 19 historias US-001…US-043 |
| `07_flujos_principales.md` | Reserva, atención, caja, cancelación, recordatorio |
| `08_arquitectura_propuesta.md` | Patrones, estructura backend/frontend, env vars |
| `09_decisiones_y_supuestos.md` | DD-01…DD-07, SU-01…SU-03 |
| `10_preguntas_abiertas.md` | IN-01/IN-02 + preguntas priorizadas |

Cambio de stack en curso (TS → Python/React) absorbido: `02`, `08`, `09` (DD-01/DD-02 reescritos, DD-06/DD-07 nuevos), `10`, `README` y `state.kb.discovery.stack` actualizados sin perder trazabilidad (la alternativa descartada quedó documentada en DD-01).

### 2.4 Etapa 3 — Roadmap (`CHANGES.md`)

Generado por `roadmap-generator` desde la KB, sin restricciones extra: **14 changes (C-01…C-14) en 6 fases**, camino crítico de 9 (`C-01 → C-02 → C-03 → C-04 → C-05 → C-06 → C-10 → C-11 → C-14`), forks paralelos documentados y plan óptimo con 3 agentes. Tras el cambio de stack se revisaron 14 puntos (C-01/C-02/C-03/C-07/C-11, FASE 5, migraciones → revisiones Alembic). Sección `roadmap` registrada en el estado.

### 2.5 Etapas 4–5 — Skills y reglas del agente

- **`find-skills` re-ejecutado contra el stack real** (Python/FastAPI, React, PostgreSQL, Redis): 17 recomendaciones verificadas por CLI con installs, priorizadas Alta/Media/Baja y elegidas por el dueño. Se descartó a conciencia: NestJS/Prisma/Node (backend es Python), better-auth (auth es JWT propio), deploy-to-vercel (se despliega con Compose). Sin skill dedicada FastAPI/JWT/Celery en el ecosistema (búsqueda negativa documentada): se cubre con skills Python generales.
- **Instaladas 17/17** globales (6 Python, 2 Postgres, 5 frontend, 3 testing, 1 Docker). `state.skills` completo.
- **`skill-registry`**: `.atl/skill-registry.md` (17 skills con compact rules + nota de adaptación a FastAPI).
- **`agent-instruction` interactivo**: 11 reglas revisadas **una por una** con el dueño (10 técnicas + 1 de dominio dictada a mano: datos de pacientes solo visibles para el equipo tratante, todo auditado — RN-SEG-01, Ley 25.326). `AGENTS.md` = `CLAUDE.md` (identidad verificada por hash), con mapa skill→rol actualizado. `state.agents` registrado.

---

## 3. Ciclo OPSX sobre un Change (Etapa 6)

Change: **`crear-turno-sin-solapamiento`**.

### 3.1 Elección justificada

Cumple las tres condiciones del TP: pertenece al MVP (agenda multisillón, sección D del Discovery), tiene reglas de negocio verificables (RN-AG-01 anti-solapamiento, RN-AG-02 fin auto-calculado, RN-AG-04 sobreturno explícito) y es una sola funcionalidad (US-002), no un módulo.

### 3.2 Explore

Relevamiento en modo thinking-partner: se acotó el alcance (modelos asumidos + seed mínimo para tests; foco en `POST /appointments`), se cerró el doble blindaje (chequeo en app + EXCLUDE, 409 sin alternativos para no arrastrar el motor de slots de C-05) y se visualizó el flujo de decisión.

### 3.3 Propose

Artefactos en `openspec/changes/crear-turno-sin-solapamiento/` (luego archivados):

- `proposal.md` — porqué (doble turno) y alcance; capacidad nueva `agenda/crear-turno`.
- `specs/agenda/crear-turno/spec.md` — 4 escenarios Dado/Cuando/Entonces: feliz (201 + fin calculado), conflicto (409), borde back-to-back (201), sobreturno con motivo (201 marcado).
- `design.md` — decisiones (chequeo app + EXCLUDE, rango semiabierto `[inicio, fin)`, fin en servidor) + riesgos.
- `tasks.md` — 6 tasks en 2 grupos con verificación cada una.

### 3.4 Apply

Implementación bajo contrato (FastAPI, SQLAlchemy 2.0 async, Pydantic con `extra="forbid"`, `tenant_id` en toda consulta, revisión Alembic por cambio):

- Modelo `Appointment` + 5 modelos base mínimos, constraints EXCLUDE por profesional y sillón (predicado: vigentes no sobreturno), extensión `btree_gist`.
- `POST /appointments`: fin auto-calculado, 409 ante solapamiento, sobreturno con motivo → 201 marcado, `IntegrityError` → 409.
- Hallazgo aplicado en curso: el EXCLUDE bloqueaba sobreturnos explícitos — predicado corregido (revisión 003) y diseño actualizado.
- Adaptaciones de entorno documentadas: driver `psycopg` (asyncpg incompatible con Python 3.14 en Windows), policy de event loop selector, DB de tests en puerto 5433 (el 5432 lo ocupa un Postgres local).

### 3.5 Verify

- `openspec validate` — change válido; `openspec doctor` — root ok.
- `pytest` — **6/6 en verde contra Postgres real** (feliz, 409, back-to-back, sobreturno, sobreturno sin motivo → 422, carrera concurrente doble-insert → un 201 y un 409), sin servidor vivo (cliente ASGI) y DB sin residuos (0 filas).
- Nota: `/opsx-verify` no existe como skill/comando en este setup; se verificó por la vía integral (validate + doctor + tests).

### 3.6 Archive

Sync del delta a `openspec/specs/agenda/crear-turno/spec.md` (nuevo spec principal, validado: 1 passed) y archivado limpio en `openspec/changes/archive/2026-10-05-crear-turno-sin-solapamiento/`. Sin changes activos pendientes.

---

## 4. Memoria del Agent (Etapa 7 — Engram)

Verificación de disponibilidad (2026-10-05): sin recursos MCP expuestos en la sesión (`list_mcp_resources` vacío, sin `.engram/` en el proyecto), pero CLI `engram` 1.20.0 operativo (`active-stack/bin/engram.exe`). La consulta inicial devolvió memoria vacía:

- `engram search "crear-turno-sin-solapamiento"` → `No memories found`
- `engram search "doble blindaje solapamiento"` → `No memories found`

Se persistieron entonces las decisiones vía CLI con scope `project: turnos-odontologia`:

- `engram save "Doble blindaje anti-solapamiento" (...)` → `Memory saved: #1 (decision)`
- `engram save "EXCLUDE ignora sobreturnos" (...)` → `Memory saved: #2 (decision)`
- `engram save "409 sin alternativos" (...)` → `Memory saved: #3 (pattern)`

Y la recuperación confirmó el ciclo completo:

- `engram search "solapamiento" --project turnos-odontologia` → `Found 1 memories: [1] #1 (decision) — Doble blindaje anti-solapamiento ... 2026-10-05 19:32:35 | project: turnos-odontologia | scope: project`

Registros persistidos:

| topic_key / # | Tipo | Contenido |
|---|---|---|
| #1 | decision | Doble blindaje app + EXCLUDE ante carrera concurrente |
| #2 | decision | EXCLUDE ignora sobreturnos explícitos (RN-AG-04) |
| #3 | pattern | 409 sin alternativos (motor de slots = C-05) |

Trazabilidad redundante en archivos: cada decisión vive además en su artefacto (`.active-orchestrator-state.json`, `design.md`, `.atl/skill-registry.md`, specs principales).

---

## 6. Reflexión Escrita

*Redacción propia de la desarrolladora a cargo (desarrollo individual).*

### 1. ¿Qué información del Discovery resultó incorrecta, no verificable o inventada por el agente? ¿Cómo lo detectaron?

Durante la fase de investigación de mercado, varios dominios del sector (como Feegow, MiConsultorio y Doctorize CL) se encontraban caídos o no resolvían, y los precios de plataformas como Dentrix o Curve solo se obtenían mediante estimaciones terciarias con afirmaciones comerciales exageradas (por ejemplo, "−82% ausencias") carentes de fuentes duras.

Cómo lo detectamos: aplicando estrictamente el protocolo de trazabilidad, registrando toda suposición sin respaldo bajo la etiqueta de "No evidenciado" en lugar de aceptar datos inventados por el agente, lo que obligó a acotar el alcance del MVP a los requerimientos transaccionales reales.

### 2. ¿En qué etapa usaron Ajustar, qué estaba mal y qué habría pasado si hubieran apretado Continuar?

La instrucción Ajustar se utilizó en múltiples momentos críticos debido a desvíos e imprevistos de integración:

En la Fundación: tuvimos que reestructurar por completo la Etapa 5 al cambiar de stack tecnológico a mitad de camino (migrando de TypeScript/NestJS a Python/FastAPI con React/Vite), lo que implicó desinstalar 18 skills de TS, regenerar el registro con 17 skills de Python y reescribir la base de conocimiento y los puntos del CHANGES.md. Además, tras un rollback por problemas de Docker y código parcial, se debió descartar un primer change que omitía specs para rehacerlo correctamente bajo contrato.

Qué habría pasado si se apretaba Continuar: habríamos arrastrado incompatibilidades graves de arquitectura (como usar asyncpg incompatible con Python 3.14 en Windows, lo que requirió migrar a psycopg), omisiones en los escenarios de especificación obligatorios, y constraints de base de datos mal configurados que habrían bloqueado operaciones válidas como los sobreturnos.

### 3. ¿Qué diferencia notaron entre implementar con una especificación aprobada y pedir código con un prompt suelto?

La diferencia operativa fue radical. Pedir código mediante un prompt suelto generaba implementaciones frágiles y desacopladas de las reglas de negocio. En cambio, trabajar bajo una especificación aprobada (Dado / Cuando / Entonces) impuso un contrato formal. Esto se evidenció en que el primer test contra la base de datos real reveló un fallo de negocio real (el constraint EXCLUDE bloqueaba los sobreturnos), permitiendo corregir el predicado de forma precisa y asegurar que la suite de pruebas validara exactamente el comportamiento esperado sin interpretaciones libres del modelo de lenguaje.

### 4. ¿Qué parte de la fundación (knowledge-base, roadmap, reglas) le aportó más valor al ciclo OPSX y cuál menos?

Lo que más valor aportó: los archivos canónicos de reglas de negocio y el modelo de datos dentro de la knowledge-base, ya que sirvieron como la única fuente de verdad constante para guiar al agente ante los recurrentes cambios de entorno y restricciones técnicas.

Lo que menos valor aportó: aquellas configuraciones y dependencias que sufrieron fricción operativa excesiva en el entorno local (como los bloqueos por timeouts en instalaciones masivas de skills o la incompatibilidad de librerías con versiones específicas del sistema operativo), las cuales demandaron un esfuerzo de corrección manual desacoplado de la lógica de dominio.

### 5. En grupo: qué hizo cada integrante y en qué etapa



---

## 7. Cierre

Fundación trazable de punta a punta (19 sistemas investigados → 10 documentos → 14 changes → 17 skills → 11 reglas) y un ciclo OPSX completo y verificado sobre la funcionalidad de mayor riesgo del MVP. Base lista para continuar con reprogramación/cancelación (RN-TU-01/02) o el siguiente change del camino crítico.
