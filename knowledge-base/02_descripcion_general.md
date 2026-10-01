# Descripción General — Turnos Odontología

## Stack tecnológico

| Capa | Tecnología | Versión mínima |
|---|---|---|
| Frontend | React + TypeScript + Vite (SPA) | React 18, TS 5, Vite 5 |
| Backend | Python + FastAPI | Python 3.12, FastAPI 0.110+ |
| Auth | JWT (access corto + refresh) | PyJWT / python-jose |
| ORM / migraciones | SQLAlchemy 2.0 + Alembic | 2.0 / 1.13+ |
| Base de datos | PostgreSQL (driver asyncpg) | 16 |
| Async / worker | Redis + Celery (fase 2; v1.0 sin worker) | Redis 7 |
| Almacenamiento | Disco local / S3-compatible (imágenes/Rx) | — |
| PDF / Excel | reportlab o weasyprint + openpyxl (lado servidor) | — |
| Tests | pytest + httpx (backend); Vitest + Playwright (frontend) | — |
| Entornos | Docker + Docker Compose | — |

Stack decidido de arriba por el equipo (ver DD-01 en `09_decisiones_y_supuestos.md`).

## Arquitectura general

Backend API modular + frontend SPA separados, orquestados con Docker Compose (`api`, `web`, `db`, `redis`). Multi-tenant lógico: `tenant_id` en todas las tablas de dominio + dependencias FastAPI que filtran por tenant. Módulos backend: identidad, agenda, clínica, caja, auditoría. En v1.0 no hay worker (recordatorio manual vía `wa.me`); Redis queda reservado para fase 2 (recordatorios automáticos, colas). Prioridad de calidad: **mantenibilidad** (capas explícitas, testing por módulo).

```
Paciente/Staff → React (Vite) → FastAPI (routers → servicios) → PostgreSQL
                                      ↘ dependencia auditoría → audit_logs
Fase 2: Celery worker ↔ Redis (recordatorios, tareas async)
```

## Integraciones externas

| Servicio | Propósito | Tipo | Fase |
|---|---|---|---|
| WhatsApp (manual) | Recordatorio con mensaje redactado (deep link `wa.me`) | Link | v1.0 |
| Redis | Colas y tareas asincrónicas (recordatorios, jobs) | RESP / redis-py | Fase 2 |
| WhatsApp Business API | Recordatorios/confirmaciones automáticas | REST | Fase 2 |
| Mercado Pago | Seña y cobro online, conciliación | SDK/REST + webhook | Fase 2 |
| AFIP/ARCA | Factura electrónica con CAE | WS SOAP (wsfev1) | Fase 2 |
| Google Calendar | Sincronización por profesional | REST/OAuth | Fase 2 |

## API REST (resumen por recurso)

- `/auth` — registro, login JWT, refresh, recuperación (paciente y staff).
- `/tenants`, `/users` — consultorio, usuarios y roles.
- `/professionals`, `/chairs`, `/services` — recursos de agenda.
- `/appointments`, `/blocks`, `/waitlist` — turnos, bloqueos, lista de espera.
- `/patients`, `/clinical-records`, `/odontogram`, `/treatment-plans`, `/budgets` — clínica.
- `/payments`, `/cash-closings`, `/settlements`, `/reports` — caja.
- `/audit-logs` — consulta de auditoría (solo lectura, rol dueño).
