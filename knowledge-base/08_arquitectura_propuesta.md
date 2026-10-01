# Arquitectura Propuesta — Turnos Odontología

## Patrones aplicados

| Patrón | Dónde | Por qué |
|---|---|---|
| API modular por routers | Backend FastAPI (identidad, agenda, clínica, caja, auditoría) | Mantenibilidad prioritaria; equipo chico |
| Multi-tenant por discriminador | `tenant_id` en dominio + dependencias FastAPI (`get_current_tenant`) | Un SaaS, datos aislados, costo bajo |
| Dependencia de auditoría | Escrituras en HC y caja | RN-SEG-01 sin ensuciar servicios |
| Soft delete | Todas las entidades de dominio | RN-SEG-02, trazabilidad |
| Esquemas Pydantic v2 | Validación de input/output en el borde API | Contratos explícitos entre React y FastAPI |
| Cálculo en servidor | Slots, fines de turno, totales | Reglas (RN-AG-01/02) no dependen del cliente |
| Migraciones versionadas | Alembic (una revisión por change) | Trazabilidad de esquema con el roadmap |

## Estructura de directorios

```
turnos-odontologia/
├── backend/               # Python + FastAPI
│   ├── app/
│   │   ├── routers/       # identidad, agenda, clinica, caja, auditoria
│   │   ├── services/      # lógica de dominio (slots, liquidaciones, presupuestos)
│   │   ├── models/        # modelos SQLAlchemy 2.0
│   │   ├── schemas/       # esquemas Pydantic v2
│   │   ├── core/          # settings, security (JWT), deps (tenant, roles), logging
│   │   └── workers/       # tareas Celery (fase 2; vacío en v1.0)
│   ├── alembic/           # revisiones de migración
│   └── tests/             # pytest + httpx
├── frontend/              # React + TypeScript + Vite
│   └── src/
│       ├── features/      # agenda, reserva, clinica, caja, admin
│       ├── shared/        # componentes UI, api client, hooks
│       └── pages/         # rutas staff + paciente
├── docker-compose.yml     # api, web, db (Postgres 16), redis
├── .env.example
└── knowledge-base/
```

## Seguridad

- Autenticación: JWT (access de corta vida + refresh rotativo); refresh en cookie httpOnly (secure, samesite=lax), access en memoria del frontend. Hash bcrypt (passlib). Recuperación por email con token expirable.
- Autorización: dependencias FastAPI de rol (matriz RBAC) + dependencia de tenant en cada endpoint de dominio (RN-AU-02).
- Validación de input: esquemas Pydantic v2 estrictos; rate-limit en `/auth` (slowapi); CORS restringido al origen del frontend.
- Secrets: `.env` local + gestor del hosting en producción; nunca en repo. Imágenes servidas con URLs firmadas de corta duración.
- Datos de salud: acceso por rol, audit trail, respaldo diario de Postgres (obligatorio desde v1.0).

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|---|---|---|---|
| `DATABASE_URL` | Conexión Postgres (asyncpg) | `postgresql+asyncpg://user:pass@db:5432/turnos` | Y |
| `JWT_SECRET` | Firma de tokens | aleatorio 32B | Y |
| `JWT_EXPIRE_MIN` / `REFRESH_EXPIRE_DAYS` | Vidas de access/refresh | `15` / `7` | N |
| `REDIS_URL` | Colas y tareas (fase 2) | `redis://redis:6379/0` | Parcial |
| `APP_URL` | URL pública | `https://turnos.ejemplo.com` | N |
| `TZ_DEFAULT` | Zona por defecto | `America/Argentina/Cordoba` | N |
| `STORAGE_DIR` / `S3_*` | Destino de imágenes | `./data/imagenes` | Parcial |
| `MP_ACCESS_TOKEN` | Mercado Pago (fase 2) | `APP-...` | Y |
| `WA_API_TOKEN` | WhatsApp API (fase 2) | `...` | Y |
| `AFIP_CERT` / `AFIP_KEY` | Certificado fiscal (fase 2) | rutas | Y |
