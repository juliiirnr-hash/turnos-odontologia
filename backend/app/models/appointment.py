"""Modelo Appointment con anti-solapamiento a nivel DB."""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Identity, Text, func
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

ESTADOS_VIGENTES = ("reservado", "confirmado", "atendido")


class Appointment(Base):
    """Turno. El rango [inicio, fin) es semiabierto: back-to-back es válido."""

    __tablename__ = "appointments"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('reservado','confirmado','atendido','cancelado','ausente')",
            name="ck_appointments_estado",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    professional_id: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False)
    chair_id: Mapped[int] = mapped_column(ForeignKey("chairs.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(Text, nullable=False, default="reservado", server_default="reservado")
    sobreturno: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)


Appointment.__table__.append_constraint(
    ExcludeConstraint(
        ("professional_id", "="),
        (func.tstzrange(Appointment.inicio, Appointment.fin, "[)"), "&&"),
        where=(Appointment.estado.in_(ESTADOS_VIGENTES) & (Appointment.sobreturno.is_(False))),
        name="ex_appointments_professional_rango",
    )
)
Appointment.__table__.append_constraint(
    ExcludeConstraint(
        ("chair_id", "="),
        (func.tstzrange(Appointment.inicio, Appointment.fin, "[)"), "&&"),
        where=(Appointment.estado.in_(ESTADOS_VIGENTES) & (Appointment.sobreturno.is_(False))),
        name="ex_appointments_chair_rango",
    )
)
