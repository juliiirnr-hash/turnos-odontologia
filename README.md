# Turnos Odontología

SaaS multi-tenant de gestión odontológica (FastAPI + React). Ver `AGENTS.md` para instrucciones de agentes y `knowledge-base/` para el dominio.

## Prerrequisitos

- Python 3.12+ · Docker Desktop (daemon corriendo) · Node 22+ (solo frontend)
- Puerto **5433** libre para el Postgres de tests (el 5432 suele estar ocupado por un Postgres local)

## Backend: instalar

```powershell
cd backend
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

## Base de datos (tests y dev)

```powershell
docker run -d --name turnos-pg -e POSTGRES_USER=turnos -e POSTGRES_PASSWORD=turnos -e POSTGRES_DB=turnos -p 5433:5432 postgres:16
```

Variables (o `.env` en `backend/`):

```powershell
$env:DATABASE_URL="postgresql+psycopg://turnos:turnos@localhost:5433/turnos"
```

Aplicar migraciones:

```powershell
cd backend
.venv/Scripts/alembic upgrade head
```

## Correr los tests

```powershell
cd backend
$env:DATABASE_URL="postgresql+psycopg://turnos:turnos@localhost:5433/turnos"
.venv/Scripts/python -m pytest tests/ -m "not slow"
```

Notas:

- Los tests usan Postgres real (contenedor `turnos-pg`), sin servidor vivo (cliente ASGI).
- En Windows se requiere `WindowsSelectorEventLoopPolicy` (ya configurado en `app/main.py`, `alembic/env.py` y `tests/conftest.py`); con Python ≤3.13 y driver asyncpg puede no hacer falta.
- Si el driver `psycopg` falla con `ProactorEventLoop`, verificar que el policy esté activo.

## Correr la API (dev)

```powershell
cd backend
.venv/Scripts/uvicorn app.main:app --reload --port 8000
```

- Liveness: `GET http://localhost:8000/api/health`
- Docs: `http://localhost:8000/docs`
