# EJ-TC-EXP-001 Ejecución de TC-EXP-001

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.21 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: Creación HTTP 201, datos persistidos y limpieza HTTP 204.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar POST /casos con delito tipo y asunto | HTTP 201 | PASS | Coincidió con la validación automatizada. |
| 2 | Comparar el NUREJ devuelto | Coincide con el generado | PASS | Coincidió con la validación automatizada. |
| 3 | Eliminar el caso temporal como admin | HTTP 204 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones
