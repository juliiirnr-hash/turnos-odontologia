# Reglas de Negocio — Turnos Odontología

## Dominio: Agenda (RN-AG)

- **RN-AG-01**: Un profesional o un sillón no puede tener dos turnos superpuestos. El sistema rechaza la creación salvo sobreturno explícito.
- **RN-AG-02**: La duración del turno la define la prestación (duracion_min); el fin se calcula, no se ingresa.
- **RN-AG-03**: Los bloqueos (feriados, vacaciones, congresos) impiden reservar en el rango afectado.
- **RN-AG-04**: El sobreturno requiere flag explícito + motivo, y queda visible en la agenda.

## Dominio: Turnos (RN-TU)

- **RN-TU-01**: Cancelar/reprogramar exige la antelación mínima configurable del tenant (default 2 h); debajo del mínimo solo puede hacerlo el staff.
- **RN-TU-02**: Al cancelar un turno se libera el slot y se ofrece al primero de la lista de espera (FIFO por creada_en).
- **RN-TU-03**: Reservar online exige paciente autenticado (email + DNI + teléfono verificable).
- **RN-TU-04**: En v1.0 el recordatorio es manual: botón que abre WhatsApp con mensaje pre-redactado (paciente, fecha, hora, consultorio).

## Dominio: Clínica (RN-CL)

- **RN-CL-01**: Odontograma FDI (piezas 11–48) con estados cerrados (18 valores) + nota e historial por pieza (quién/cuándo).
- **RN-CL-02**: Todo plan de tratamiento con costo genera presupuesto con cobertura OS discriminada y monto a cargo del paciente; sin presupuesto aprobado no hay cobro asociado al plan.
- **RN-CL-03**: Imágenes/Rx con límite de tamaño total por tenant (cuota configurable, default 5 GB).

## Dominio: Caja (RN-CA)

- **RN-CA-01**: Cierre de caja diario obligatorio si hubo movimiento; anulaciones trazables (flag + motivo), nunca borrado físico.
- **RN-CA-02**: Liquidaciones por porcentaje o por tratamiento, exportables a PDF; una liquidación cerrada no se edita (se emite nota de ajuste).
- **RN-CA-03**: Medios v1.0: efectivo, tarjeta, transferencia. Mercado Pago y factura electrónica: fase 2.

## Dominio: Autenticación (RN-AU)

- **RN-AU-01**: Staff con email + contraseña (bcrypt cost 12); paciente con email + DNI + teléfono; recuperación por email.
- **RN-AU-02**: Aislamiento por tenant: toda consulta de dominio filtra por `tenant_id` del usuario; prohibido el acceso cruzado.

## Dominio: Seguridad y datos (RN-SEG)

- **RN-SEG-01**: Audit trail append-only en historia clínica y caja (quién, qué, cuándo, diff). Sin updates ni deletes en `audit_logs`.
- **RN-SEG-02**: Soft delete global (`deleted_at`); los listados excluyen eliminados salvo auditoría.

## Excepciones globales (RN-GLB)

- **RN-GLB-01**: Toda exportación (PDF/Excel) respeta los permisos del rol que la pide.
- **RN-GLB-02**: Los horarios se guardan en UTC y se muestran en America/Argentina_Cordoba (configurable por tenant).
