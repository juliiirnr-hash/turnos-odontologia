"""Engine async, sesiones y chequeo de readiness."""
from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provee una sesión por request (dependencia FastAPI)."""
    async with SessionLocal() as session:
        yield session


async def check_db(timeout_s: float = 2.0) -> bool:
    """Devuelve True si Postgres responde SELECT 1 dentro del timeout.

    Args:
        timeout_s: segundos máximos de espera.

    Returns:
        True si la base responde a tiempo, False en caso contrario.
    """
    import asyncio

    try:
        async with engine.connect() as conn:
            await asyncio.wait_for(conn.execute(text("SELECT 1")), timeout_s)
        return True
    except Exception:
        return False
