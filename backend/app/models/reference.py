"""Modelos base mínimos asumidos (Tenant, Patient, Professional, Chair, Service).

Solo lo indispensable para que Appointment tenga integridad referencial.
Su modelado completo vive en C-02/C-04.
"""
from sqlalchemy import BigInteger, Boolean, ForeignKey, Identity, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Tenant(Base):
    """Consultorio (tenant)."""

    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)


class Patient(Base):
    """Paciente."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    dni: Mapped[str] = mapped_column(Text, nullable=False)


class Professional(Base):
    """Odontólogo."""

    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)


class Chair(Base):
    """Sillón/box."""

    __tablename__ = "chairs"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")


class Service(Base):
    """Prestación (define duración y precio)."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    duracion_min: Mapped[int] = mapped_column(nullable=False)
    precio_base: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
