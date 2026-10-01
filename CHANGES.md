# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **Turnos Odontología** (SaaS multi-tenant de agenda, clínica y caja para consultorios odontológicos de Argentina).
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> Alcance: **MVP v1.0 = agenda + clínica + caja manual**. Mercado Pago, WhatsApp automático y facturación AFIP/ARCA son **fase 2** (ver DD-04) y NO tienen change en este índice.

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose <nombre-del-change>`.
4. Al terminar el change, archivarlo con `/opsx:archive <nombre-del-change>`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```
C-01 foundation-setup
  └── C-02 core-models-identity              ← Tenant, User, Patient, AuditLog; desbloquea todo
        └── C-03 auth-session                ← sesión + RBAC + tenant guard; desbloquea TODO lo demás
              │
              ├── C-04 practice-resources    ← professionals, chairs, services (US-041)
              │     └── C-05 agenda-backend  ← turnos, slots, bloques, sobreturnos (US-001–004, Flujo 1)
              │           ├── C-06 reserva-lista-espera   ← cancela/reprograma, waitlist FIFO, mis turnos (US-005, US-012/013)
              │           │     │
              │           │     ├── C-12 agenda-staff-web     ← UI agenda staff + wa.me manual (US-042)
              │           │     └── C-13 reserva-paciente-web ← UI pública + reserva + mis turnos (US-010/011/013)
              │           │
              │           └── C-10 caja-backend  ← pagos + cierres (US-030/031) [+ C-09 por budget_id]
              │                 └── C-11 liquidaciones-reportes ← settlements + reportes + PDF/Excel (US-032/033)
              │
              └── C-07 clinical-records      ← pacientes CRUD + ficha + interceptor auditoría (US-020) [paralelo con C-04]
                    ├── C-08 odontograma     ← entries FDI 18 estados + historial (US-021)
                    └── C-09 imagenes-planes ← imágenes/Rx con cuota + planes + presupuestos OS (US-022/023)
                          │
                          └── C-10 caja-backend (segunda dependencia)
                                └── C-14 clinica-caja-admin-web ← UI clínica + caja + admin + auditoría (US-040/041/043)
                                      ← + C-08 + C-11
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 (solo)

GATE 1: C-01 ✓
  → C-02 (solo)

GATE 2: C-02 ✓
  → C-03 (solo)

GATE 3: C-03 ✓                        ← PRIMER FORK (2 ramas backend)
  → C-04 practice-resources            [Agente A — Backend Agenda]
  → C-07 clinical-records              [Agente B — Backend Clínica]

GATE 4: C-04 ✓
  → C-05 agenda-backend                [Agente A]

GATE 5: C-05 ✓ + C-07 ✓               ← SEGUNDO FORK (3 paralelos)
  → C-06 reserva-lista-espera          [Agente A — si C-05 ✓]
  → C-08 odontograma                   [Agente B — si C-07 ✓]
  → C-09 imagenes-planes               [Agente C — si C-07 ✓]

GATE 6: C-05 + C-06 ✓                 ← FORK FRONTEND (2 paralelos) + caja
  → C-10 caja-backend                  [Agente A — si C-09 ✓]
  → C-12 agenda-staff-web              [Agente C]
  → C-13 reserva-paciente-web          [Agente B — si C-03 ✓ + C-05 + C-06 ✓]

GATE 7: C-10 ✓
  → C-11 liquidaciones-reportes        [Agente A]

GATE 8: C-08 + C-09 + C-11 ✓
  → C-14 clinica-caja-admin-web        [Agente B/C]
```

### Camino crítico (9 changes — mínimo irreducible)

```
C-01 → C-02 → C-03 → C-04 → C-05 → C-06 → C-10 → C-11 → C-14
```

(rama agenda; la rama clínica C-07 → C-09 converge en C-10 y es un change más corta)

### Plan óptimo con 3 agentes

```
Paso │ Agente A (Backend Agenda+Caja) │ Agente B (Backend Clínica+Paciente) │ Agente C (Frontend+Clínica aux)
─────┼────────────────────────────────┼─────────────────────────────────────┼────────────────────────────────
  1  │ C-01 foundation-setup          │                  —                  │               —
  2  │ C-02 core-models-identity      │                  —                  │               —
  3  │ C-03 auth-session              │                  —                  │               —
  4  │ C-04 practice-resources        │ C-07 clinical-records               │               —
  5  │ C-05 agenda-backend            │                  —                  │ C-09 imagenes-planes (si C-07 ✓)
  6  │ C-06 reserva-lista-espera      │ C-08 odontograma                    │               —
  7  │ C-10 caja-backend              │ C-13 reserva-paciente-web           │ C-12 agenda-staff-web
  8  │ C-11 liquidaciones-reportes    │                  —                  │               —
  9  │               —                │ C-14 clinica-caja-admin-web         │               —
```

---

## FASE 0 — Cimientos

### [C-01] `foundation-setup`
- **Estado**: `[ ]` pendiente
- **Scope**: Scaffolding completo + infraestructura base con Docker Compose
  - Estructura: `backend/` (Python + FastAPI, SQLAlchemy 2.0 + Alembic, pytest + httpx), `frontend/` (React + TypeScript + Vite), `docker-compose.yml` (`api`, `web`, `db` Postgres 16, `redis`), `knowledge-base/`
  - `backend/`: FastAPI mínima con `GET /api/health`, SQLAlchemy 2.0 contra PostgreSQL 16 (asyncpg), Alembic inicializado, `core/` (settings, logger, exception handlers, paginación)
  - `frontend/`: scaffolding React + TS + Vite, estilos base mobile-first, páginas vacías `/login`, `/register`, `/agenda`, `/mis-turnos`
  - `.env.example`: `DATABASE_URL` (asyncpg), `JWT_SECRET`, `JWT_EXPIRE_MIN`, `REDIS_URL`, `APP_URL`, `TZ_DEFAULT=America/Argentina/Cordoba`, `STORAGE_DIR`, placeholders fase 2 (`MP_ACCESS_TOKEN`, `WA_API_TOKEN`, `AFIP_CERT`) comentados
  - GitHub Actions CI: jobs paralelos backend (ruff + mypy + pytest) y frontend (lint + typecheck + test)
  - Seed de feriados AR del año en curso (script o JSON importable por C-04)
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` (alcance v1.0 y fuera de alcance)
  - `knowledge-base/02_descripcion_general.md` §Stack
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01, §DD-02

---

### [C-02] `core-models-identity`
- **Estado**: `[ ]` pendiente
- **Scope**: Modelos base multi-tenant + migraciones iniciales + seed mínimo
  - Modelos SQLAlchemy: `Tenant` (slug único, configuración JSON: antelación mínima, horarios), `User` (email único por tenant, password_hash, rol enum paciente|odontologo|recepcionista|dueño), `Patient` (user_id único, dni, fecha_nacimiento, obra_social texto v1), `AuditLog` (append-only: actor, acción, entidad, entidad_id, diff JSON)
  - Convenciones globales: `tenant_id` en todo dominio (RN-AU-02), `deleted_at` nullable + soft delete (RN-SEG-02), timestamps UTC (RN-GLB-02)
  - Revisión Alembic 001: tablas core + índices (`users(tenant_id,email)`, `patients(tenant_id,dni)`)
  - Seed mínimo: 1 tenant demo, 1 dueño, 1 recepcionista, 1 odontólogo, 1 paciente, 4 roles
  - Tests: aislamiento por tenant (acceso cruzado prohibido), soft delete excluido de listados
- **Dependencias**: C-01
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Tenant, §User, §Patient, §AuditLog, §Seed data inicial
  - `knowledge-base/05_reglas_de_negocio.md` §RN-AU-02, §RN-SEG-01, §RN-SEG-02, §RN-GLB-02
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05, §SU-02

---

## FASE 1 — Identidad y acceso

### [C-03] `auth-session`
- **Estado**: `[ ]` pendiente
- **Scope**: Autenticación JWT + RBAC + tenant guard (US-010, US-040 parcial)
  - `POST /auth/register` — paciente (email + DNI + teléfono, RN-AU-01/RN-TU-03); `POST /auth/login` — staff y paciente, bcrypt (passlib), access JWT corto + refresh rotativo en cookie httpOnly (secure, samesite=lax); `POST /auth/refresh`; `POST /auth/logout`; `POST /auth/recuperar` + reset con token expirable por email
  - Rate limiting en `/auth/*` (slowapi, 5 intentos/60s por IP+email)
  - Dependencias FastAPI de rol según matriz RBAC + dependencia de tenant (toda consulta de dominio filtra por `tenant_id`) + `GET /auth/me`
  - `POST /users` (invitar staff, solo dueño), `PATCH /users/:id/rol`, baja soft (US-040: alta, baja, cambio de rol)
  - Revisión Alembic 002: ajustes auth (índices, tokens de recuperación)
  - Tests: login correcto, token inválido/expirado, refresh rotativo, rate limit, RBAC denegado, recuperación completa
- **Dependencias**: C-02
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` (matriz RBAC completa, rutas públicas)
  - `knowledge-base/05_reglas_de_negocio.md` §RN-AU-01, §RN-AU-02, §RN-TU-03
  - `knowledge-base/06_funcionalidades.md` §US-010, §US-040
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad

---

## FASE 2 — Agenda

> C-04 y C-07 pueden proponerse en paralelo (ramas independientes tras C-03).

### [C-04] `practice-resources`
- **Estado**: `[ ]` pendiente
- **Scope**: Recursos configurables del consultorio (US-041)
  - Modelos: `Professional` (user_id, especialidades[], horario JSON), `Chair` (nombre, activo), `Service` (nombre, duracion_min, precio_base, requiere_sillon)
  - CRUD `/professionals`, `/chairs`, `/services` (solo dueño; recepcionista R) con validación (duración > 0, horario bien formado)
  - Revisión Alembic 003: tablas de recursos
  - Seed: 2 sillones + 5 prestaciones (limpieza 30′, consulta 20′, conducto 60′, extracción 40′, ortodoncia control 30′) + feriados AR (de C-01)
  - Tests: CRUD por rol, `chair_id` nullable absorbe consultorio de 1 sillón (SU-01)
- **Dependencias**: C-03
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Professional / Chair / Service, §Seed data inicial
  - `knowledge-base/06_funcionalidades.md` §US-041
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-01
  - `knowledge-base/10_preguntas_abiertas.md` (pregunta multisillón)

---

### [C-05] `agenda-backend`
- **Estado**: `[ ]` pendiente
- **Scope**: Núcleo de turnos + motor de slots + bloqueos + sobreturnos (US-001–004, Flujo 1)
  - Modelos: `Appointment` (patient/professional/chair/service, inicio, fin calculado por `duracion_min` RN-AG-02, estado reservado|confirmado|atendido|cancelado|ausente, origen online|recepcion, sobreturno bool + motivo), `Block` (por profesional, sillón o consultorio, motivo)
  - `POST /appointments` (recepción, US-002) — rechazo 409 ante solapamiento por profesional/sillón salvo sobreturno explícito (RN-AG-01, RN-AG-04); `GET /appointments?dia|semana&professional&chair` (US-001, índices por professional/chair/estado); `PATCH /appointments/:id/estado` (confirmado→atendido→ausente); `POST /blocks`, `DELETE /blocks/:id` (US-003, reserva en rango bloqueado rechazada RN-AG-03)
  - `GET /slots?service&professional&desde&hasta` — cálculo en servidor: horario profesional − bloques − turnos vigentes; 409 con slots alternativos si el slot se tomó en concurrente; 422 fuera de antelación
  - Revisión Alembic 004: tablas appointment, block + índices `(tenant_id, professional_id, inicio)`, `(tenant_id, chair_id, inicio)`
  - Tests: solapamiento rechazado, sobreturno con motivo, fin auto-calculado, bloqueos, concurrencia (doble reserva → 409), zona horaria America/Argentina_Cordoba
- **Dependencias**: C-04
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Appointment, §Block / Waitlist
  - `knowledge-base/05_reglas_de_negocio.md` §RN-AG-01–04, §RN-GLB-02
  - `knowledge-base/06_funcionalidades.md` §US-001, §US-002, §US-003, §US-004
  - `knowledge-base/07_flujos_principales.md` §Flujo 1

---

### [C-06] `reserva-lista-espera`
- **Estado**: `[ ]` pendiente
- **Scope**: Reserva online + cancelación/reprogramación + lista de espera + mis turnos (US-005, US-011–013, Flujo 4)
  - `POST /appointments/online` — paciente autenticado elige slot real (RN-TU-03), crea turno `reservado` + confirmación (Flujo 1 pasos 3–4)
  - `POST /appointments/:id/cancelar` — valida antelación mínima del tenant (default 2 h, RN-TU-01); bajo el mínimo solo staff (auditado); reprogramar = cancelar + crear trazable
  - `GET /patients/mis-turnos` — historial con estados (US-013)
  - Modelo `Waitlist` (patient, service, professional opcional, orden FIFO por creada_en) + `POST /waitlist`, `GET /waitlist` (staff); al cancelar, oferta automática al primero FIFO (RN-TU-02) con confirmación de recepcionista
  - Revisión Alembic 005: tabla waitlist (+ `waitlist_offers` si se modela la oferta)
  - Tests: antelación mínima, FIFO, reasignación al cancelar, reprogramación trazable, reserva exige login
- **Dependencias**: C-05
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §RN-TU-01, §RN-TU-02, §RN-TU-03
  - `knowledge-base/06_funcionalidades.md` §US-005, §US-011, §US-012, §US-013
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/10_preguntas_abiertas.md` §IN-01, §IN-02

---

## FASE 3 — Clínica

> C-08 y C-09 pueden proponerse en paralelo (ambos solo dependen de C-07).

### [C-07] `clinical-records`
- **Estado**: `[ ]` pendiente
- **Scope**: Pacientes admin + ficha clínica + interceptor de auditoría (US-020, Flujo 2 paso 4)
  - `CRUD /patients` — recepcionista CRUD administrativo, odontólogo R + W clínico, paciente R propio (matriz RBAC); búsqueda por DNI/nombre
  - Modelo `ClinicalRecord` (patient 1–1, anamnesis, alergias, updated_by) + `GET/PATCH /clinical-records/:patientId` con auditoría de cada edición (RN-SEG-01)
  - Dependencia/evento de auditoría FastAPI: toda escritura en HC y caja genera `AuditLog` (quién, qué, cuándo, diff) sin ensuciar servicios
  - Revisión Alembic 006: tabla clinical_records
  - Tests: permisos por rol sobre ficha, diff de auditoría correcto, soft delete de paciente
- **Dependencias**: C-03
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` (filas Pacientes, Odontograma/HC)
  - `knowledge-base/04_modelo_de_datos.md` §ClinicalRecord / OdontogramEntry / Image
  - `knowledge-base/05_reglas_de_negocio.md` §RN-SEG-01
  - `knowledge-base/06_funcionalidades.md` §US-020

---

### [C-08] `odontograma`
- **Estado**: `[ ]` pendiente
- **Scope**: Odontograma FDI con historial por pieza (US-021)
  - Modelo `OdontogramEntry` (record_id, pieza_fdi 11–48, estado enum 18 valores cerrados v. DentalSoft, nota, fecha, professional_id)
  - `GET /clinical-records/:id/odontogram` (mapa completo por pieza con último estado), `POST /odontogram-entries` (marca estado + nota), historial por pieza (quién/cuándo)
  - Validación: pieza en rango FDI, estado dentro del enum (RN-CL-01)
  - Revisión Alembic 007: tabla odontogram_entries + índice `(record_id, pieza_fdi, fecha)`
  - Tests: enum cerrado, historial ordenado, permisos (odontólogo CRUD, recep/dueño R)
- **Dependencias**: C-07
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §ClinicalRecord / OdontogramEntry / Image
  - `knowledge-base/05_reglas_de_negocio.md` §RN-CL-01
  - `knowledge-base/06_funcionalidades.md` §US-021
  - `knowledge-base/07_flujos_principales.md` §Flujo 2

---

### [C-09] `imagenes-planes`
- **Estado**: `[ ]` pendiente
- **Scope**: Imágenes/Rx con cuota + planes de tratamiento y presupuestos con cobertura OS (US-022, US-023, Flujo 2 paso 3)
  - Modelo `Image` (record_id, tipo foto|rx, storage_key, tamaño_bytes) + `POST /clinical-records/:id/images` (multipart, disco local/S3-compatible), `GET` con URLs firmadas de corta duración; cuota por tenant default 5 GB con aviso al superar el 80% (RN-CL-03)
  - Modelos `TreatmentPlan` (patient, professional, prioridad, items JSON, estado) + `Budget` (plan_id, total, cobertura_os, a_cargo_paciente, estado borrador|aprobado|rechazado, aprobado_en) — `CRUD /treatment-plans`, `CRUD /budgets`, `POST /budgets/:id/aprobar|rechazar`
  - Regla: sin presupuesto aprobado no hay cobro asociado al plan (RN-CL-02)
  - Revisión Alembic 008: tablas images, treatment_plans, budgets
  - Tests: cuota y aviso, URL firmada expira, presupuesto con cobertura discriminada, cobro bloqueado sin aprobación
- **Dependencias**: C-07
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §TreatmentPlan / Budget, §ClinicalRecord / OdontogramEntry / Image
  - `knowledge-base/05_reglas_de_negocio.md` §RN-CL-02, §RN-CL-03
  - `knowledge-base/06_funcionalidades.md` §US-022, §US-023
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad (imágenes), §Variables de entorno (`STORAGE_DIR`/`S3_*`)

---

## FASE 4 — Caja y finanzas

### [C-10] `caja-backend`
- **Estado**: `[ ]` pendiente
- **Scope**: Cobros + cierre diario (US-030, US-031, Flujo 3 pasos 1–2)
  - Modelo `Payment` (appointment_id/budget_id, monto, medio efectivo|tarjeta|transferencia — RN-CA-03, recibido_por, anulado bool + motivo; anulación con motivo, nunca borrado RN-CA-01)
  - `POST /payments` (asociado a turno o presupuesto aprobado), `POST /payments/:id/anular` (motivo obligatorio, genera auditoría)
  - Modelo `CashClosing` (fecha, totales JSON por medio, cerrado_por, cerrado_en) + `POST /cash-closings` (totales por medio) y `GET /cash-closings?fecha`; día cerrado no admite movimientos (ajuste vía pago de corrección); reapertura prohibida
  - Revisión Alembic 009: tablas payments, cash_closings
  - Tests: cobro asociado a turno/plan, anulación trazable, cierre con totales, día cerrado rechaza movimientos, liquidación de medios en ARS
- **Dependencias**: C-05, C-09
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Payment / CashClosing / Settlement
  - `knowledge-base/05_reglas_de_negocio.md` §RN-CA-01, §RN-CA-03
  - `knowledge-base/06_funcionalidades.md` §US-030, §US-031
  - `knowledge-base/07_flujos_principales.md` §Flujo 3

---

### [C-11] `liquidaciones-reportes`
- **Estado**: `[ ]` pendiente
- **Scope**: Liquidaciones + reportes + exportación PDF/Excel (US-032, US-033)
  - Modelo `Settlement` (beneficiario professional_id u OS texto, período, líneas JSON, total, estado borrador|cerrada) + `POST /settlements` (por % o por tratamiento), `POST /settlements/:id/cerrar` (inmutable; ajuste posterior = nota nueva RN-CA-02), exportación PDF (reportlab o weasyprint, lado servidor)
  - `GET /reports?desde&hasta&tipo=ocupacion|facturacion|ausentismo` (agregados por rango, exportable Excel vía openpyxl); toda exportación respeta permisos del rol (RN-GLB-01)
  - Revisión Alembic 010: tabla settlements
  - Tests: liquidación por % y por tratamiento, cerrada inmutable, reportes por rango, exportación respeta rol
- **Dependencias**: C-10
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §Stack (PDF/Excel)
  - `knowledge-base/04_modelo_de_datos.md` §Payment / CashClosing / Settlement
  - `knowledge-base/05_reglas_de_negocio.md` §RN-CA-02, §RN-GLB-01
  - `knowledge-base/06_funcionalidades.md` §US-032, §US-033

---

## FASE 5 — Web (frontend React + Vite)

> C-12 y C-13 pueden proponerse en paralelo (dependen del backend ya archivado, no entre sí).

### [C-12] `agenda-staff-web`
- **Estado**: `[ ]` pendiente
- **Scope**: Web staff de agenda + recordatorio manual WhatsApp (US-001–005 lado UI, US-042, Flujo 5)
  - Rutas staff (guarda por rol recepcionista+): `/agenda` vista día/semana con turnos, bloqueos y sobreturnos diferenciados + filtros por profesional/sillón; modal crear turno (fin auto, error claro ante 409); gestión de bloqueos; sobreturno con motivo; lista de espera FIFO visible + reasignación
  - Botón "Recordar" por turno sin confirmar: abre `wa.me/<tel>?text=<mensaje>` pre-redactado (paciente, fecha, hora, consultorio RN-TU-04) y permite marcar `confirmado` (Flujo 5)
  - Manejo de errores API: 409 con slots alternativos, 422 fuera de antelación
  - Mobile-first, español rioplatense, horarios America/Argentina_Cordoba
- **Dependencias**: C-05, C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-001–005, §US-042
  - `knowledge-base/07_flujos_principales.md` §Flujo 5
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios (`frontend/`)
  - `knowledge-base/01_vision_y_objetivos.md` §Métricas de éxito (ausentismo, ocupación)

---

### [C-13] `reserva-paciente-web`
- **Estado**: `[ ]` pendiente
- **Scope**: Web pública + cuenta paciente + flujo de reserva (US-010–013 lado UI, Flujo 1 lado UI)
  - Rutas públicas: `/` landing, `/precios`, `/legal/*`, `/login`, `/register` (3 campos: email + DNI + teléfono, DD-03), `/recuperar`
  - Flujo autenticado: elegir prestación → profesional → slots libres reales → confirmación inmediata en pantalla; `/mis-turnos` (historial con estados); cancelar/reprogramar con aviso de antelación mínima
  - Sesión persistente (mitigar fricción de login, IN-01); "seña acordada" solo como nota del turno, sin cobro (IN-02)
  - Mobile-first: el paciente reserva desde el teléfono
- **Dependencias**: C-03, C-05, C-06
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/06_funcionalidades.md` §US-010, §US-011, §US-012, §US-013
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-03
  - `knowledge-base/10_preguntas_abiertas.md` §IN-01, §IN-02

---

### [C-14] `clinica-caja-admin-web`
- **Estado**: `[ ]` pendiente
- **Scope**: Web de clínica + caja + administración y auditoría (US-020–023, US-030–033, US-040/041/043 lado UI, Flujo 2–3 lado UI)
  - Clínica (odontólogo): `/pacientes/:id` ficha (anamnesis, alergias), odontograma interactivo FDI (18 estados + nota + historial por pieza), adjuntar fotos/Rx (con aviso de cuota), planes con prioridades + presupuestos (total/cobertura/a cargo, aprobar/rechazar)
  - Caja (recepcionista/dueña): registrar cobro, anular con motivo, cierre diario con totales por medio, liquidaciones por profesional/OS con export PDF, reportes (ocupación, facturación, ausentismo) con export Excel
  - Admin (dueña): `/admin/recursos` (profesionales, sillones, prestaciones), `/admin/usuarios` (invitar, roles, baja soft), `/admin/auditoria` (listado filtrable por entidad/actor/fecha, solo lectura) + `GET /audit-logs` backend si aún no existe
  - Permisos UI según matriz RBAC; exportaciones solo con permiso del rol
- **Dependencias**: C-08, C-09, C-11
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` (matriz RBAC)
  - `knowledge-base/05_reglas_de_negocio.md` §RN-CL-01–03, §RN-CA-01–03, §RN-SEG-01, §RN-GLB-01
  - `knowledge-base/06_funcionalidades.md` §US-020–023, §US-030–033, §US-040, §US-041, §US-043
  - `knowledge-base/07_flujos_principales.md` §Flujo 2, §Flujo 3
