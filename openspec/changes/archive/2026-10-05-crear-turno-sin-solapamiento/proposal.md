# Proposal — crear-turno-sin-solapamiento

## Why

El doble turno (mismo profesional o sillón ocupado) es el error operativo que el sistema existe para eliminar (Discovery: coordinación por WhatsApp/papel). Este change implementa la primera funcionalidad del MVP con regla de negocio verificable.

## What Changes

- `POST /appointments`: crea un turno con fin auto-calculado por prestación, rechaza solapamientos con 409 y admite sobreturno explícito con motivo.
- Blindaje doble: chequeo en app + constraint EXCLUDE en DB (carrera concurrente).
- Modelos asumidos preexistentes; seed mínimo solo para tests de este change.

## Capabilities

### New Capabilities

- `agenda/crear-turno`: creación de turnos con anti-solapamiento por profesional y sillón (4 escenarios: feliz, conflicto 409, borde back-to-back, sobreturno explícito).

### Modified Capabilities

—

## Impact

- Crea `POST /appointments`, modelo `Appointment` mínimo operativo, constraint EXCLUDE, `openspec/specs/agenda/crear-turno` (al archivar).
- Base para reprogramación y cancelación (RN-TU-01/02) en changes futuros. Sin UI en este change.
