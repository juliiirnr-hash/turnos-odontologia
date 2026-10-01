# Modelo de Datos — Turnos Odontología

## Dominios

- **Identidad**: tenants, usuarios, roles.
- **Agenda**: profesionales, sillones, prestaciones, turnos, bloqueos, lista de espera.
- **Clínica**: pacientes, fichas, odontograma, imágenes, planes, presupuestos.
- **Administración**: pagos, cierres de caja, liquidaciones.
- **Auditoría**: bitácora append-only.

## ERD (textual)

```
Tenant 1──* User (*──1 Role por asignación)
Tenant 1──* Professional 1──* Appointment *──1 Patient
Tenant 1──* Chair 1──* Appointment
Service *──* Appointment (prestación del turno, define duración)
Appointment 1──* Payment | 1──0..1 WaitlistOffer
Patient 1──1 ClinicalRecord 1──* OdontogramEntry | * Image
TreatmentPlan *──1 Patient; Budget *──1 TreatmentPlan
CashClosing 1──* Payment; Settlement *──* Payment
AuditLog *──1 Tenant; *──0..1 User (actor)
```

Toda tabla de dominio lleva `tenant_id` (RN-AU-02) y `deleted_at` nullable (RN-SEG-02).

## Entidades

### Tenant (consultorio)
- Atributos: id (uuid), nombre, slug único, email, teléfono, configuración JSON (antelación mínima, horarios), created_at.
- Relaciones: 1──* casi todo. Índices: slug único.

### User
- Atributos: id, tenant_id, email único por tenant, password_hash, nombre, teléfono, rol (paciente|odontologo|recepcionista|dueño), active.
- Relaciones: odontólogo *──1 Professional (opcional); paciente *──1 Patient (opcional).

### Patient
- Atributos: id, tenant_id, user_id (único), dni, fecha_nacimiento, obra_social (texto v1), observaciones.

### Professional / Chair / Service
- Professional: id, tenant_id, user_id, especialidades[], horario JSON.
- Chair (sillón/box): id, tenant_id, nombre, activo.
- Service (prestación): id, tenant_id, nombre, duracion_min, precio_base, requiere_sillon.

### Appointment
- Atributos: id, tenant_id, patient_id, professional_id, chair_id (nullable), service_id, inicio, fin (calculado), estado (reservado|confirmado|atendido|cancelado|ausente), origen (online|recepcion), sobreturno bool, notas.
- Constraints: RN-AG-01 (sin solapamiento por profesional/sillón salvo sobreturno explícito). Índices: (tenant_id, professional_id, inicio), (tenant_id, chair_id, inicio), (tenant_id, estado).

### Block / Waitlist
- Block: id, tenant_id, professional_id/chair_id, desde, hasta, motivo (feriado/bloqueo).
- Waitlist: id, tenant_id, patient_id, service_id, professional_id (opcional), creada_en, estado; orden FIFO por creada_en.

### ClinicalRecord / OdontogramEntry / Image
- ClinicalRecord: id, tenant_id, patient_id, anamnesis_texto, alergias, updated_by.
- OdontogramEntry: id, tenant_id, record_id, pieza_fdi (11–48), estado (enum 18 valores v. DentalSoft), nota, fecha, professional_id.
- Image: id, tenant_id, record_id, tipo (foto|rx), storage_key, tamaño_bytes.

### TreatmentPlan / Budget
- TreatmentPlan: id, tenant_id, patient_id, professional_id, prioridad, items JSON, estado.
- Budget: id, tenant_id, plan_id, total, cobertura_os, a_cargo_paciente, estado (borrador|aprobado|rechazado), aprobado_en.

### Payment / CashClosing / Settlement
- Payment: id, tenant_id, appointment_id/budget_id, monto, medio (efectivo|tarjeta|transferencia), recibido_por, anulado bool, created_at.
- CashClosing: id, tenant_id, fecha, totales JSON por medio, cerrado_por, cerrado_en. Reapertura prohibida (nuevo ajuste vía pago de corrección).
- Settlement: id, tenant_id, beneficiario (professional_id u OS texto), período, líneas JSON, total, estado.

### AuditLog
- Atributos: id, tenant_id, actor_id, acción, entidad, entidad_id, diff JSON, created_at. Sin updates ni deletes (RN-SEG-01).

## Seed data inicial

- Roles (4), un Tenant demo, un Dueño, una Recepcionista, un Odontólogo con horario, dos sillones, 5 prestaciones (limpieza 30′, consulta 20′, conducto 60′, extracción 40′, ortodoncia control 30′), feriados AR año en curso.
