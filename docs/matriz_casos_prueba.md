**Matriz de Casos de Prueba**

| ID | Regla | Tipo | Datos de entrada | Resultado esperado |
|---|---|---|---|---|
| CP-01 | RN-01 | Positiva | `"  Juan Perez  "` | Nombre normalizado a `"Juan Perez"` sin espacios extra. |
| CP-02 | RN-01 | Negativa | `" Jo "` (2 caracteres tras trim) | Lanza `InvalidCustomerNameError`. |
| CP-03 | RN-01 | Frontera | `"Ana"` (exactamente 3 caracteres) | Válido, retorna `"Ana"`. |
| CP-04 | RN-02 | Positiva | `"ASESORIA"` / `"soporte"` | Normaliza a minúsculas y valida servicio. |
| CP-05 | RN-02 | Negativa | `"mantenimiento"` | Lanza `InvalidServiceError`. |
| CP-06 | RN-03 | Positiva | 30 y 60 minutos | Duración permitida. |
| CP-07 | RN-03 | Negativa / Frontera | 29, 31, 45, 0 minutos | Lanza `InvalidDurationError`. |
| CP-08 | RN-04 | Negativa | Fecha: 2026-04-19, Actual: 2026-04-20 | Lanza `InvalidReservationDateError` (fecha pasada). |
| CP-09 | RN-04 | Frontera / Positiva | Fecha: 2026-04-20, Actual: 2026-04-20 | Válido (mismo día). |
| CP-10 | RN-05 | Negativa | Sábado (2026-04-25) o Domingo (2026-04-26) | Lanza `InvalidReservationDateError` (fin de semana). |
| CP-11 | RN-06 | Frontera / Positiva | Hora inicio: 08:00 | Válido (hora de apertura). |
| CP-12 | RN-06 | Negativa | Hora inicio: 07:59 | Lanza `InvalidReservationTimeError` (antes de apertura). |
| CP-13 | RN-07 | Frontera / Positiva | Hora inicio: 16:30, Duración: 30 min | Válido (finaliza a las 17:00 exactas). |
| CP-14 | RN-07 | Negativa | Hora inicio: 16:31, Duración: 30 min | Lanza `InvalidReservationTimeError` (termina > 17:00). |
| CP-15 | RN-08 | Negativa | Misma fecha (2026-04-20) y hora (10:00) | Lanza `DuplicateReservationError`. |
| CP-16 | RN-09 & RN-10 | Positiva | Datos válidos completos | Reserva creada con estado `"confirmed"` y código generado inyectado. |