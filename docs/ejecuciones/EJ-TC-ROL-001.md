# EJ-TC-ROL-001 Ejecución de TC-ROL-001

| Campo | Valor |
|---|---|
| ID del TC | TC-ROL-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:50:36 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `dd68354b-0cb1-4d65-8d8e-f23d4b83142c` |
| Estado | FAIL |
| Duración del caso | 0.466 segundos |

## Resultado Observado

El endpoint devolvió HTTP 200 y el listado de usuarios al rol abogado; se esperaba HTTP 403 sin datos.

## Comparación

No coincide: se obtuvo HTTP 200 en lugar de HTTP 403.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Autenticar al abogado QA | JWT válido | PASS | Coincidió con la validación automatizada. |
| 2 | Enviar GET /usuarios | HTTP 200 con listado de usuarios | FAIL | Se esperaba HTTP 403; se vinculó BUG-01-F. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/dd68354b-0cb1-4d65-8d8e-f23d4b83142c/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** El backend autenticó al abogado, pero no aplicó autorización por rol al listar usuarios.
- **Referencia del defecto:** BUG-01-F.

## Observaciones

AssertionError: BUG-01-F: un abogado autenticado pudo listar usuarios; respuesta HTTP observada=200 assert 200 == 403  +  where 200 = <Response [200 OK]>.status_code
