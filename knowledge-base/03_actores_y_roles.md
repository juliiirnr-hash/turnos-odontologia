# Actores y Roles — Turnos Odontología

## Actores del sistema

| Actor | Descripción | Cómo interactúa |
|---|---|---|
| Paciente | Persona con cuenta (email + DNI + teléfono) que reserva turnos | Web autenticada: reserva, cancela, ve sus turnos |
| Odontólogo | Profesional que atiende y registra clínica | Web staff: agenda propia, ficha, odontograma |
| Recepcionista | Opera agenda, confirma y cobra | Web staff: agenda completa, caja, pacientes |
| Dueño / administrador | Gestiona consultorio, usuarios y finanzas | Web staff: todo + reportes, liquidaciones, auditoría |
| Sistema (actor técnico) | Procesos automáticos (fase 2: recordatorios, conciliación) | Jobs internos |

## RBAC — Matriz de permisos

| Recurso | Paciente | Odontólogo | Recepcionista | Dueño |
|---|---|---|---|---|
| Mis turnos | CRUD propio | — | CRUD | CRUD |
| Agenda (todos) | R (slots libres) | R + W propios | CRUD | CRUD |
| Pacientes | R propio | R + W clínico | CRUD admin. | CRUD |
| Odontograma / HC | — | CRUD | R | R |
| Planes / presupuestos | R propios | CRUD | R | CRUD |
| Cobros / caja | — | — | CR (cobrar) | CRUD + cierre |
| Liquidaciones | — | R propias | — | CRUD |
| Usuarios / roles | — | — | — | CRUD |
| Auditoría | — | — | — | R |
| Configuración tenant | — | — | — | CRUD |

## Rutas públicas (sin autenticación)

- `/` landing, `/precios`, `/legal/*`
- `/login`, `/register`, `/recuperar`
- Slots libres solo como dato agregado dentro del flujo de reserva autenticado (RN-TU-03: reservar exige login).
