"""Schemas de creación y respuesta de turnos."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    """Payload de creación. El fin lo calcula el servidor (RN-AG-02)."""

    model_config = ConfigDict(extra="forbid")

    tenant_id: int
    patient_id: int
    professional_id: int
    chair_id: int
    service_id: int
    inicio: datetime
    sobreturno: bool = False
    motivo: str | None = Field(default=None, max_length=500)


class AppointmentOut(BaseModel):
    """Turno creado. Nunca expone internos (regla dura 1)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    patient_id: int
    professional_id: int
    chair_id: int
    service_id: int
    inicio: datetime
    fin: datetime
    estado: str
    sobreturno: bool
    motivo: str | None
