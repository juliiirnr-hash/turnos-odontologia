"""Escenarios del spec agenda/crear-turno (AAA, un comportamiento por test)."""
import asyncio

import pytest

INICIO = "2026-10-06T10:00:00+00:00"


def _payload(seed, inicio=INICIO, **extra):
    return {
        "tenant_id": seed["tenant_id"],
        "patient_id": seed["patient_id"],
        "professional_id": seed["professional_id"],
        "chair_id": seed["chair_id"],
        "service_id": seed["service_id"],
        "inicio": inicio,
        **extra,
    }


@pytest.mark.integration
async def test_crear_turno_slot_libre_devuelve_201_con_fin_calculado(client, seed_minimo):
    resp = await client.post("/appointments", json=_payload(seed_minimo))
    assert resp.status_code == 201
    body = resp.json()
    assert body["estado"] == "reservado"
    assert body["fin"] == "2026-10-06T10:30:00Z"
    assert body["sobreturno"] is False


@pytest.mark.integration
async def test_crear_turno_solapado_devuelve_409_sin_crear(client, seed_minimo, session):
    primero = await client.post("/appointments", json=_payload(seed_minimo))
    assert primero.status_code == 201
    resp = await client.post("/appointments", json=_payload(seed_minimo, inicio="2026-10-06T10:15:00+00:00"))
    assert resp.status_code == 409
    from sqlalchemy import func, select

    from app.models.appointment import Appointment

    total = (await session.execute(select(func.count(Appointment.id)))).scalar()
    assert total == 1


@pytest.mark.integration
async def test_crear_turno_back_to_back_devuelve_201(client, seed_minimo):
    primero = await client.post("/appointments", json=_payload(seed_minimo))
    assert primero.status_code == 201
    resp = await client.post("/appointments", json=_payload(seed_minimo, inicio="2026-10-06T10:30:00+00:00"))
    assert resp.status_code == 201


@pytest.mark.integration
async def test_crear_sobreturno_con_motivo_devuelve_201_marcado(client, seed_minimo):
    primero = await client.post("/appointments", json=_payload(seed_minimo))
    assert primero.status_code == 201
    resp = await client.post(
        "/appointments",
        json=_payload(seed_minimo, inicio="2026-10-06T10:15:00+00:00", sobreturno=True, motivo="urgencia"),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["sobreturno"] is True


@pytest.mark.integration
async def test_crear_sobreturno_sin_motivo_devuelve_422(client, seed_minimo):
    resp = await client.post(
        "/appointments", json=_payload(seed_minimo, sobreturno=True)
    )
    assert resp.status_code == 422


@pytest.mark.integration
async def test_doble_insert_concurrente_solo_uno_persiste(client, seed_minimo, session):
    async def _crear():
        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            return await c.post("/appointments", json=_payload(seed_minimo))

    r1, r2 = await asyncio.gather(_crear(), _crear())
    oks = [r for r in (r1, r2) if r.status_code == 201]
    conflictos = [r for r in (r1, r2) if r.status_code == 409]
    assert len(oks) == 1 and len(conflictos) == 1

    from sqlalchemy import func, select

    from app.models.appointment import Appointment

    total = (await session.execute(select(func.count(Appointment.id)))).scalar()
    assert total == 1
