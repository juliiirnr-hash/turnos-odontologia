# Funcionalidades — Turnos Odontología

## Épica 1: Agenda del consultorio

### US-001 — Ver agenda diaria/semanal
**Como** recepcionista **Quiero** ver la agenda por día/semana, profesional y sillón **Para** operar el consultorio sin choques.
**Criterios**: - [ ] Vista día/semana con turnos, bloqueos y sobreturnos diferenciados - [ ] Filtro por profesional y sillón
**Reglas**: RN-AG-01, RN-AG-03, RN-AG-04

### US-002 — Crear turno desde recepción
**Como** recepcionista **Quiero** crear un turno eligiendo paciente, prestación, profesional y sillón **Para** agendar llamadas y presenciales.
**Criterios**: - [ ] Fin auto-calculado por prestación - [ ] Rechazo ante solapamiento con mensaje claro
**Reglas**: RN-AG-01, RN-AG-02

### US-003 — Gestionar bloqueos
**Como** dueña **Quiero** bloquear rangos (feriados, vacaciones) **Para** que no se reserve en esos horarios.
**Criterios**: - [ ] Bloqueo por profesional, sillón o todo el consultorio - [ ] Reserva en rango bloqueado rechazada
**Reglas**: RN-AG-03

### US-004 — Sobreturno explícito
**Como** recepcionista **Quiero** crear un sobreturno con motivo **Para** atender urgencias.
**Criterios**: - [ ] Requiere motivo y queda marcado visualmente
**Reglas**: RN-AG-01, RN-AG-04

### US-005 — Lista de espera
**Como** paciente **Quiero** anotarme en lista de espera **Para** que me ofrezcan el turno si se libera.
**Criterios**: - [ ] Orden FIFO visible para staff - [ ] Al cancelar, oferta automática al primero
**Reglas**: RN-TU-02

## Épica 2: Reserva del paciente

### US-010 — Registro y login
**Como** paciente **Quiero** crear cuenta e iniciar sesión **Para** reservar y ver mis turnos.
**Criterios**: - [ ] Registro con email + DNI + teléfono - [ ] Login, logout y recuperación
**Reglas**: RN-AU-01, RN-TU-03

### US-011 — Reservar online
**Como** paciente **Quiero** elegir prestación, profesional y horario libre **Para** reservar sin llamar.
**Criterios**: - [ ] Solo slots reales (descuenta bloqueos y ocupados) - [ ] Confirmación inmediata en pantalla
**Reglas**: RN-TU-03, RN-AG-01, RN-AG-02

### US-012 — Cancelar / reprogramar
**Como** paciente **Quiero** cancelar o cambiar mi turno **Para** liberar el horario.
**Criterios**: - [ ] Respeta antelación mínima del consultorio - [ ] Reprogramar = cancelar + crear (trazable)
**Reglas**: RN-TU-01, RN-TU-02

### US-013 — Mis turnos
**Como** paciente **Quiero** ver mis turnos pasados y futuros **Para** llevar control.
**Criterios**: - [ ] Historial con estado de cada turno

## Épica 3: Clínica

### US-020 — Ficha del paciente
**Como** odontólogo **Quiero** ver y editar ficha (anamnesis, alergias) **Para** atender informado.
**Criterios**: - [ ] Edición con auditoría de cambios
**Reglas**: RN-SEG-01

### US-021 — Odontograma
**Como** odontólogo **Quiero** marcar estados por pieza FDI con nota **Para** registrar el estado bucal.
**Criterios**: - [ ] 18 estados cerrados + historial por pieza (quién/cuándo)
**Reglas**: RN-CL-01

### US-022 — Imágenes y Rx
**Como** odontólogo **Quiero** adjuntar fotos y radiografías **Para** documentar el caso.
**Criterios**: - [ ] Límite de cuota por consultorio con aviso
**Reglas**: RN-CL-03

### US-023 — Plan y presupuesto
**Como** odontólogo **Quiero** armar plan con prioridades y presupuesto con cobertura OS **Para** acordar el tratamiento.
**Criterios**: - [ ] Total, cobertura OS y monto a cargo discriminados - [ ] Estados: borrador/aprobado/rechazado
**Reglas**: RN-CL-02

## Épica 4: Caja y finanzas

### US-030 — Cobrar
**Como** recepcionista **Quiero** registrar un cobro (efectivo/tarjeta/transferencia) **Para** asentar el ingreso.
**Criterios**: - [ ] Asociado a turno o presupuesto - [ ] Anulación con motivo (sin borrado)
**Reglas**: RN-CA-01, RN-CA-03

### US-031 — Cierre diario
**Como** dueña **Quiero** cerrar la caja del día **Para** conciliar ingresos por medio.
**Criterios**: - [ ] Totales por medio de pago - [ ] Día cerrado no admite nuevos movimientos (ajuste vía corrección)
**Reglas**: RN-CA-01

### US-032 — Liquidaciones
**Como** dueña **Quiero** liquidar a profesionales y OS por período **Para** pagar comisiones y convenios.
**Criterios**: - [ ] Por % o por tratamiento, exportable a PDF - [ ] Liquidación cerrada inmutable
**Reglas**: RN-CA-02

### US-033 — Reportes
**Como** dueña **Quiero** ver ocupación, facturación y ausentismo **Para** decidir.
**Criterios**: - [ ] Por rango de fechas, exportable a Excel
**Reglas**: RN-GLB-01

## Épica 5: Administración y confianza

### US-040 — Usuarios y roles
**Como** dueña **Quiero** invitar staff y asignar roles **Para** operar con permisos correctos.
**Criterios**: - [ ] Alta, baja (soft) y cambio de rol
**Reglas**: RN-AU-01, RN-AU-02, RN-SEG-02

### US-041 — Recursos del consultorio
**Como** dueña **Quiero** gestionar profesionales, sillones y prestaciones **Para** configurar la agenda.
**Criterios**: - [ ] Horarios por profesional, duración y precio por prestación

### US-042 — Recordatorio manual
**Como** recepcionista **Quiero** enviar recordatorio por WhatsApp con un clic **Para** reducir ausencias sin automatizar.
**Criterios**: - [ ] Abre `wa.me` con mensaje pre-redactado (paciente, fecha, hora)
**Reglas**: RN-TU-04

### US-043 — Auditoría
**Como** dueña **Quiero** ver quién cambió HC y caja **Para** cumplir trazabilidad.
**Criterios**: - [ ] Listado filtrable por entidad, actor y fecha, solo lectura
**Reglas**: RN-SEG-01
