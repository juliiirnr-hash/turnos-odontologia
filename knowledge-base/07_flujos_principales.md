# Flujos Principales — Turnos Odontología

## Flujo 1: Reserva online del paciente
**Disparador**: paciente autenticado busca turno. **Actor**: paciente.
**Pasos**:
1. Frontend pide slots libres (prestación + profesional + rango).
2. API calcula slots: horario profesional − bloques − turnos vigentes (RN-AG-01/02/03).
3. Paciente elige y confirma → API crea turno `reservado` (RN-TU-03).
4. Sistema muestra confirmación con fecha, hora y consultorio.
**Casos de error**: slot tomado en concurrente → 409 con slots alternativos; fuera de antelación → 422.

## Flujo 2: Atención en consultorio
**Disparador**: paciente llega. **Actor**: recepcionista + odontólogo.
**Pasos**:
1. Recepcionista marca turno `confirmado` → `atendido` al iniciar.
2. Odontólogo abre ficha (US-020), actualiza odontograma (RN-CL-01) y adjunta Rx (RN-CL-03).
3. Si hay tratamiento: crea plan + presupuesto con cobertura OS (RN-CL-02); paciente aprueba.
4. Cada escritura clínica genera entrada de auditoría (RN-SEG-01).

## Flujo 3: Cobro y cierre de caja
**Disparador**: fin de la atención. **Actor**: recepcionista, dueña.
**Pasos**:
1. Recepcionista registra pago asociado a turno/presupuesto (RN-CA-03).
2. Al cierre del día, la dueña ejecuta cierre: totales por medio (RN-CA-01).
3. Periódicamente genera liquidaciones por profesional/OS y exporta PDF (RN-CA-02).
**Casos de error**: día ya cerrado → solo ajuste vía pago de corrección; liquidación cerrada → nota de ajuste nueva.

## Flujo 4: Cancelación y lista de espera
**Disparador**: paciente cancela. **Actor**: paciente, recepcionista.
**Pasos**:
1. API valida antelación mínima del tenant (RN-TU-01).
2. Turno pasa a `cancelado`; slot liberado.
3. Sistema ofrece el slot al primero de la lista de espera FIFO (RN-TU-02); recepcionista confirma reasignación.
**Casos de error**: bajo la antelación → solo staff puede cancelar (queda auditado).

## Flujo 5: Recordatorio manual (v1.0)
**Disparador**: recepcionista repasa agenda del día siguiente. **Actor**: recepcionista.
**Pasos**:
1. Agenda muestra turnos sin confirmar.
2. Botón "Recordar" abre `wa.me/<tel>?text=<mensaje>` con datos del turno (RN-TU-04).
3. Recepcionista envía y marca turno `confirmado`.
