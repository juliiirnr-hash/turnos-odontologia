"""POST /appointments."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.appointments import AppointmentCreate, AppointmentOut
from app.services.appointments import OverlapError, crear_turno

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentOut, status_code=201)
async def post_appointment(data: AppointmentCreate, session: AsyncSession = Depends(get_session)) -> AppointmentOut:
    """Crea un turno con anti-solapamiento.

    Args:
        data: payload validado.
        session: sesión por request.

    Returns:
        El turno creado.

    Raises:
        HTTPException: 409 si hay solapamiento, 422 si el payload es inválido.
    """
    try:
        turno = await crear_turno(session, data)
    except OverlapError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return AppointmentOut.model_validate(turno)
