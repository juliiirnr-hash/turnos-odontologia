# Design — crear-turno-sin-solapamiento

## Context

Ver `proposal.md` — Why. Restricciones: DD-01 (FastAPI + SQLAlchemy async), reglas duras 1 (Pydantic), 2 (tenant), 3 (Alembic), 11 (datos de pacientes). Modelos base asumidos; seed mínimo para tests.

## Goals / Non-Goals

**Goals:** `POST /appointments` cumple los 4 escenarios del spec con doble blindaje (app + EXCLUDE).

**Non-Goals:** motor de slots y alternativos (C-05), reprogramación/cancelación, UI, facturación.

## Decisions

- **Chequeo app primero**: query de solapamiento `(inicio < fin_existente) AND (fin > inicio_existente)` por profesional o sillón; 409 rápido sin tocar la DB de escritura. Alternativa: solo EXCLUDE — descartada, el error de constraint es menos expresivo para el 409.
- **EXCLUDE USING gist como red**: constraint en (profesional, rango) y (sillón, rango) solo para turnos vigentes NO sobreturno; el sobreturno explícito lo permite la app (RN-AG-04) y la DB no lo bloquea. La carrera doble-clic (no sobreturno) falla en DB aunque pase el chequeo app.
- **Rango semiabierto `[inicio, fin)`**: el borde back-to-back (fin == inicio) es válido por construcción tanto en la query como en EXCLUDE con `&&`.
- **Fin calculado en servidor** (RN-AG-02): el cliente nunca envía `fin`; evita inconsistencias con la duración de la prestación.
- **Sobreturno con motivo obligatorio**: flag + motivo en el mismo request; queda marcado y visible (RN-AG-04).

## Risks / Trade-offs

- [EXCLUDE exige extensión btree_gist] → Mitigación: revisión Alembic que la crea; documentado para el hosting.
- [Seed mínimo diverge de C-02/C-04] → Mitigación: seed solo en tests de este change, marcado como temporal.
- [Zona horaria] → Mitigación: horarios en UTC, comparación en UTC (RN-GLB-02).
