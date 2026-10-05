"""App FastAPI."""
import asyncio
import sys

if sys.platform == "win32":  # asyncpg/psycopg exigen selector loop en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI

from app.routers.appointments import router as appointments_router

app = FastAPI(title="Turnos Odontología")
app.include_router(appointments_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Liveness sin dependencias."""
    return {"status": "ok"}
