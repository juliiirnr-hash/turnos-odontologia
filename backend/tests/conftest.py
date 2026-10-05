"""Fixtures compartidas: DB real + cliente ASGI (sin servidor vivo)."""
import asyncio
import os
import sys

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if sys.platform == "win32":  # drivers async exigen selector loop en Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://turnos:turnos@localhost:5433/turnos"
)

from app.core import db as db_module  # noqa: E402
from app.main import app  # noqa: E402
from app.models.appointment import Appointment  # noqa: E402,F401
from app.models.base import Base  # noqa: E402
from app.models.reference import Chair, Patient, Professional, Service, Tenant  # noqa: E402,F401

TEST_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(TEST_URL, pool_pre_ping=True)
TestSession = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session():
    """Sesión con tablas limpias por test (transacción + truncate)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSession() as s:
        yield s
        for table in reversed(Base.metadata.sorted_tables):
            await s.execute(table.delete())
        await s.commit()


@pytest_asyncio.fixture
async def seed_minimo(session):
    """Tenant + paciente + profesional + sillón + prestación (30 min)."""
    tenant = Tenant(slug="t1", nombre="T1")
    session.add(tenant)
    await session.flush()
    patient = Patient(tenant_id=tenant.id, dni="1")
    professional = Professional(tenant_id=tenant.id)
    chair = Chair(tenant_id=tenant.id, nombre="S1")
    service = Service(tenant_id=tenant.id, nombre="Limpieza", duracion_min=30, precio_base=0)
    session.add_all([patient, professional, chair, service])
    await session.commit()
    return {
        "tenant_id": tenant.id,
        "patient_id": patient.id,
        "professional_id": professional.id,
        "chair_id": chair.id,
        "service_id": service.id,
    }


@pytest_asyncio.fixture
async def client(session):
    """Cliente ASGI con sesión nueva por request (sin servidor vivo).

    La sesión del test solo siembra datos y verifica; cada request abre
    la suya, igual que en producción (esto permite probar concurrencia).
    """

    async def _override():
        async with TestSession() as s:
            yield s

    app.dependency_overrides[db_module.get_session] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
