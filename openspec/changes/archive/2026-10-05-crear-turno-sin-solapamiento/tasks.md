# Tasks — crear-turno-sin-solapamiento

## 1. Modelo y constraint

- [x] 1.1 Crear modelo `Appointment` mínimo operativo (tenant, patient, professional, chair, service, inicio, fin, estado, sobreturno, motivo) + seed mínimo para tests y verificar `alembic upgrade head` limpio
- [x] 1.2 Agregar constraints EXCLUDE (profesional+rango, sillón+rango, rango semiabierto) con btree_gist y verificar que un insert solapado directo en DB falla

## 2. Endpoint

- [x] 2.1 Implementar `POST /appointments` (fin auto-calculado, chequeo de solapamiento → 409, sobreturno con motivo → 201 marcado) con schemas Pydantic de respuesta y verificar escenario feliz (201 reservado) con httpx
- [x] 2.2 Verificar escenario de conflicto (409 sin crear turno) y escenario borde back-to-back (201) con tests
- [x] 2.3 Verificar escenario de sobreturno (201 marcado) y carrera concurrente (doble insert simultáneo → uno 201, otro 409) con tests
