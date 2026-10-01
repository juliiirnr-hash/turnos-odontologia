# Preguntas Abiertas — Turnos Odontología

## Inconsistencias detectadas

### IN-01 — Login obligatorio vs fricción de reserva
**Discovery dice**: el paciente debe poder reservar con mínima fricción (WhatsApp-like).
**KB dice**: RN-TU-03 exige login (decisión DD-03 del usuario).
**Impacto**: posible caída de conversión en reserva online.
**Resolución propuesta**: mantener login pero con registro de 3 campos + sesión persistente; medir abandono y re-evaluar token anónimo en fase 2.

### IN-02 — Seña sin cobro online
**Discovery dice**: seña posible para reservar (regla de negocio).
**KB dice**: MP en fase 2, caja v1.0 solo presencial.
**Impacto**: la seña v1.0 solo puede registrarse como compromiso, no cobrarse.
**Resolución propuesta**: v1.0 registra "seña acordada" como nota del turno; cobro digital en fase 2.

## Preguntas abiertas (priorizadas)

| Prioridad | Pregunta | Bloquea | Decisor |
|---|---|---|---|
| Alta | ¿Multisillón obligatorio día 1 o `chair_id` opcional alcanza? | Sprint 1 (modelo) | Product Owner |
| Alta | ¿Access JWT en memoria + refresh httpOnly, o todo en httpOnly? | Sprint 1 (auth) | Tech Lead |
| Alta | ¿Worker Celery o ARQ para las tareas Redis de fase 2? | Fase 2 | Tech Lead |
| Alta | ¿Proveedor de hosting + Postgres con respaldo diario? | Sprint 1 (infra) | Dueño |
| Media | ¿AFIP/ARCA en fase 2 inmediata o fase 3? | Roadmap | Product Owner |
| Media | ¿Costo de WA Business API lo absorbe el plan o se traslada? | Pricing | Dueño |
| Media | ¿Validación de DNI/obra social contra padrón en algún momento? | Fase 2 | Product Owner |
| Baja | ¿Nombre comercial y slug del producto? | Branding | Dueño |
| Baja | ¿Migración asistida desde papel/Excel en onboarding? | Lanzamiento | Equipo |
