# crear-turno Specification

## Purpose

Permite crear turnos garantizando que ningún profesional ni sillón quede doblemente reservado en el mismo rango horario.

## Requirements

### Requirement: Crear turno en slot libre

El sistema SHALL crear un turno con fin calculado como inicio más la duración de la prestación, respondiendo 201 y estado reservado cuando el rango no se solapa con ningún turno vigente del mismo profesional ni del mismo sillón.

#### Scenario: Creación en slot libre

- **Dado** un profesional y un sillón sin turnos en el rango solicitado
- **Cuando** se crea un turno indicando paciente, prestación, profesional, sillón e inicio
- **Entonces** responde 201 con estado reservado y fin igual a inicio más la duración de la prestación

### Requirement: Rechazar solapamiento con 409

El sistema SHALL responder 409 sin crear el turno cuando el rango solicitado se solapa con un turno vigente del mismo profesional o del mismo sillón, salvo sobreturno explícito.

#### Scenario: Conflicto por solapamiento

- **Dado** un turno vigente para el mismo profesional o sillón cuyo rango se cruza con el solicitado
- **Cuando** se intenta crear el turno sin flag de sobreturno
- **Entonces** responde 409 por conflicto y no se crea ningún turno

### Requirement: Turnos contiguos son válidos

El sistema SHALL considerar válido un turno que empieza exactamente en el instante en que termina otro turno del mismo profesional y sillón.

#### Scenario: Borde back-to-back

- **Dado** un turno vigente que termina a las 10:00 para el mismo profesional y sillón
- **Cuando** se crea un turno que empieza exactamente a las 10:00
- **Entonces** responde 201 con estado reservado

### Requirement: Sobreturno explícito

El sistema SHALL crear el turno aunque exista solapamiento cuando se indica sobreturno explícito con motivo, marcándolo como sobreturno.

#### Scenario: Sobreturno con motivo

- **Dado** un rango solapado con un turno vigente
- **Cuando** se crea el turno con sobreturno verdadero y motivo de urgencia
- **Entonces** responde 201 con el turno marcado como sobreturno
