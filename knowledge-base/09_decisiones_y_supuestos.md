# Decisiones y Supuestos — Turnos Odontología

## Decisiones documentadas

### DD-01 — Stack Python + React (decidido por el equipo)
**Decisión**: backend Python + FastAPI (JWT, SQLAlchemy 2.0 + Alembic, PostgreSQL, Redis para async) en Docker; frontend React + TypeScript + Vite.
**Contexto**: stack impuesto por el equipo; reemplaza la preferencia inicial TypeScript-fullstack (P4). Es restricción dada, no propuesta.
**Alternativas**: TypeScript fullstack (Next.js + NestJS + Prisma) — descartada por decisión externa.
**Justificación**: se acata la restricción; FastAPI + SQLAlchemy cubren API multi-tenant, JWT y migraciones sin fricción.
**Trade-offs**: dos lenguajes (tipos no compartidos; contrato vía OpenAPI/Pydantic ↔ TS); las skills TS instaladas aplican al frontend, el backend requiere criterio FastAPI/SQLAlchemy.

### DD-02 — Backend y frontend separados + Docker Compose
**Decisión**: `backend/` (FastAPI) y `frontend/` (React+Vite) separados, un `docker compose up` levanta api, web, db y redis.
**Contexto**: prioridad mantenibilidad, equipo chico, escala multi-tenant moderada; dos lenguajes impiden monorepo de código compartido.
**Alternativas**: despliegues manuales por pieza; PaaS separadas desde día 1.
**Justificación**: entorno reproducible, transacciones ACID simples en el backend (caja), testing integrado por pieza.
**Trade-offs**: Compose es para dev/piloto; producción seria pide hosting gestionado (DB con respaldo, Redis administrado).

### DD-03 — Paciente con login obligatorio para reservar
**Decisión**: RN-TU-03 (email + DNI + teléfono).
**Contexto**: pregunta abierta del Discovery resuelta por el usuario (ronda 2).
**Alternativas**: reserva anónima con token por SMS/WA.
**Justificación**: trazabilidad, historial y lista de espera confiable; menos no-shows fantasma.
**Trade-offs**: fricción de registro; mitigar con registro en 3 campos y login persistente.

### DD-04 — MVP sin pagos online ni AFIP
**Decisión**: v1.0 = agenda + clínica + caja manual; MP, WA auto y FE AFIP en fase 2.
**Contexto**: P2 eligió "Agenda + clínica + caja".
**Alternativas**: MVP con MP desde día 1.
**Justificación**: reduce riesgo regulatorio y de integraciones; el wedge es agenda + odontograma + caja trazable.
**Trade-offs**: cobro online y facturación quedan como deuda planificada (ver `10_preguntas_abiertas.md`).

### DD-05 — Audit trail append-only desde v1.0
**Decisión**: RN-SEG-01 + RN-SEG-02 en HC y caja.
**Contexto**: datos de salud (Ley 25.326/26.529) y dinero exigen trazabilidad.
**Alternativas**: auditoría en fase 2.
**Justificación**: costo bajo ahora, costo altísimo después; habilita disputas y control.
**Trade-offs**: tabla de auditoría crece; plan de retención/archivado en fase 2.

### DD-06 — Redis + Celery para async (fase 2)
**Decisión**: Redis como broker y Celery como worker para recordatorios automáticos y tareas programadas; en v1.0 Redis corre en Compose sin worker activo.
**Contexto**: el stack incluye Redis "para las funcionalidades asincrónicas que correspondan"; el MVP no tiene ninguna (recordatorio manual).
**Alternativas**: ARQ (nativo asyncio, más liviano); pg-boss sobre Postgres.
**Justificación**: Celery es el estándar documentado del ecosistema; ARQ queda como alternativa si el equipo prefiere asyncio puro.
**Trade-offs**: Celery suma una pieza a operar; si fase 2 tarda, Redis ocioso en piloto.

### DD-07 — Docker Compose como entorno base
**Decisión**: `docker-compose.yml` con `api`, `web`, `db` (Postgres 16) y `redis` desde C-01; `.env.example` único.
**Contexto**: parte del stack impuesto.
**Alternativas**: instalación local por lenguaje.
**Justificación**: onboarding en minutos, paridad dev/piloto.
**Trade-offs**: no es estrategia de producción (ver DD-02).

## Supuestos inferidos

### SU-01 — Multisillón desde día 1
**Supuesto**: la agenda modela sillones como recurso de primera clase.
**Origen**: Discovery (pregunta abierta) + MVP "agenda" sin recorte explícito.
**Riesgo si es falso**: modelo más simple posible; el campo `chair_id` nullable lo absorbe.
**Cómo validar**: primer piloto con consultorio de 1 sillón.

### SU-02 — Un tenant = un consultorio (multisucursal fase 2)
**Supuesto**: sin jerarquía de sucursales en v1.0.
**Origen**: fuera de alcance declarado.
**Riesgo si es falso**: re-modelar tenant con hijas.
**Cómo validar**: preguntar en piloto si hay redes de consultorios.

### SU-03 — Español rioplatense, moneda ARS, zona America/Argentina_Cordoba
**Supuesto**: localización AR por defecto configurable por tenant.
**Origen**: Discovery (restricciones).
**Riesgo si es falso**: bajo; parametrizado desde el inicio (RN-GLB-02).
