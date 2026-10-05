"""Lógica de creación de turnos con anti-solapamiento."""
from datetime import timedelta

from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import ESTADOS_VIGENTES, Appointment
from app.models.reference import Service
from app.schemas.appointments import AppointmentCreate


class OverlapError(Exception):
    """El rango solicitado se solapa con un turno vigente."""


async def _hay_solapamiento(
    session: AsyncSession, tenant_id: int, professional_id: int, chair_id: int, inicio, fin
) -> bool:
    """Devuelve True si existe un turno vigente solapado (rango semiabierto).

    Args:
        session: sesión async.
        tenant_id: tenant del turno.
        professional_id: profesional solicitado.
        chair_id: sillón solicitado.
        inicio: inicio solicitado (aware UTC).
        fin: fin calculado (aware UTC).

    Returns:
        True si hay solapamiento vigente.
    """
    stmt = (
        select(Appointment.id)
        .where(
            Appointment.tenant_id == tenant_id,
            Appointment.estado.in_(ESTADOS_VIGENTES),
            or_(
                Appointment.professional_id == professional_id,
                Appointment.chair_id == chair_id,
            ),
            Appointment.inicio < fin,
            Appointment.fin > inicio,
        )
        .limit(1)
    )
    return (await session.execute(stmt)).first() is not None


async def crear_turno(session: AsyncSession, data: AppointmentCreate) -> Appointment:
    """Crea un turno calculando el fin y validando solapamientos.

    Args:
        session: sesión async.
        data: payload validado.

    Returns:
        El turno persistido.

    Raises:
        OverlapError: si hay solapamiento y no es sobreturno explícito con motivo.
        ValueError: si la prestación no existe o sobreturno sin motivo.
    """
    service = await session.get(Service, data.service_id)
    if service is None or service.tenant_id != data.tenant_id:
        raise ValueError("prestación inexistente para el tenant")
    if data.sobreturno and not data.motivo:
        raise ValueError("el sobreturno exige motivo (RN-AG-04)")

    fin = data.inicio + timedelta(minutes=service.duracion_min)
    if not data.sobreturno and await _hay_solapamiento(
        session, data.tenant_id, data.professional_id, data.chair_id, data.inicio, fin
    ):
        raise OverlapError("rango solapado con un turno vigente")

    turno = Appointment(
        tenant_id=data.tenant_id,
        patient_id=data.patient_id,
        professional_id=data.professional_id,
        chair_id=data.chair_id,
        service_id=data.service_id,
        inicio=data.inicio,
        fin=fin,
        estado="reservado",
        sobreturno=data.sobreturno,
        motivo=data.motivo,
    )
    session.add(turno)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise OverlapError("rango solapado (constraint)") from e
    await session.refresh(turno)
    return turno
