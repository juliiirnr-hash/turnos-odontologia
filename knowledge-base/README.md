# Turnos Odontología — Base de Conocimiento

SaaS multi-tenant (Python + FastAPI + PostgreSQL, frontend React + TypeScript + Vite) para gestión odontológica en Argentina: agenda multisillón, reserva online, odontograma, caja y liquidaciones. MVP v1.0 = agenda + clínica + caja; MP, WhatsApp automático y AFIP en fase 2.

## Índice de Archivos

| Archivo | Contenido |
|---------|-----------|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, objetivos por actor, alcance v1.0, métricas |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack, arquitectura con Compose, integraciones, API |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Paciente, odontólogo, recepcionista, dueña; RBAC |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | 5 dominios, 15 entidades, ERD, seed |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | 20 reglas RN-AG/TU/CL/CA/AU/SEG/GLB |
| [06_funcionalidades.md](06_funcionalidades.md) | 5 épicas, 19 historias US-001…US-043 |
| [07_flujos_principales.md](07_flujos_principales.md) | Reserva, atención, caja, cancelación, recordatorio |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, directorios, seguridad, env vars |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | DD-01…DD-05, SU-01…SU-03 |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | IN-01/IN-02 + 8 preguntas priorizadas |

## Quick Start para Desarrolladores

1. Entender el dominio → [01](01_vision_y_objetivos.md), [03](03_actores_y_roles.md)
2. Entender los datos → [04](04_modelo_de_datos.md)
3. Entender las reglas → [05](05_reglas_de_negocio.md)
4. Entender la arquitectura → [02](02_descripcion_general.md), [08](08_arquitectura_propuesta.md)
5. Implementar → [07](07_flujos_principales.md), [06](06_funcionalidades.md)
6. Antes de codificar → [10](10_preguntas_abiertas.md)

## Resumen Ejecutivo

Agenda multisillón con anti-solapamiento, reserva con login, odontograma FDI y caja con liquidaciones, todo multi-tenant y auditado. Se lanza sin pagos online para llegar rápido; MP, WhatsApp automático y factura electrónica vienen en fase 2.
