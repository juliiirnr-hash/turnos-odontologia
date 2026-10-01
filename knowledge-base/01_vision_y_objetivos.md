# Visión y Objetivos — Turnos Odontología

## Propósito del sistema

SaaS multi-tenant que permite a consultorios y clínicas odontológicas de Argentina gestionar agenda, historia clínica y caja en un solo lugar, eliminando la coordinación por WhatsApp/papel, el ausentismo no gestionado y la caja sin trazabilidad.

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|---|---|---|
| Paciente | Reservar y gestionar sus turnos sin llamar | Ver historial de turnos, recibir confirmaciones |
| Odontólogo | Atender con ficha y odontograma a mano | Registrar planes y presupuestos |
| Recepcionista | Operar la agenda multisillón sin solapamientos | Cobrar, confirmar turnos, exportar listados |
| Dueño / administrador | Ver ocupación, facturación y liquidaciones | Gestionar usuarios, roles y auditoría |

## Alcance v1.0 (MVP)

- Agenda diaria/semanal multiprofesional y multisillón, duración variable por prestación, bloqueos/feriados, sobreturnos explícitos, anti-solapamiento.
- Reserva online con paciente autenticado, confirmación/cancelación/reprogramación, lista de espera.
- Recordatorio manual (botón que abre WhatsApp con mensaje redactado).
- Ficha clínica, odontograma FDI, imágenes/Rx adjuntas, planes de tratamiento y presupuestos con cobertura OS.
- Caja diaria (efectivo/tarjeta/transferencia), cierre diario, liquidaciones por profesional y por OS, reportes básicos.
- Roles y permisos, audit trail en HC y caja, exportación PDF/Excel.

## Fuera de alcance (fase 2+)

- Cobro online / Mercado Pago / seña digital, recordatorios automáticos, facturación electrónica AFIP/ARCA.
- Periodontograma completo, ortodoncia avanzada, recetas digitales, consentimientos con firma avanzada.
- Multisucursal, API pública/webhooks, app nativa, BI avanzado, campañas de marketing.

## Métricas de éxito

- Ausentismo < 10% en consultorios activos a 90 días (vía confirmación + lista de espera).
- Ocupación de sillón > 70% en agenda publicada.
- Cierre de caja diario en el 100% de los días con movimiento.
- Tiempo de onboarding (registro → primer turno creado) < 30 minutos.
