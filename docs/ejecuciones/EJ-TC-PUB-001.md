# EJ-TC-PUB-001 Ejecución de TC-PUB-001

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.029 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 200 y datos públicos del expediente solicitado.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Consultar /seguimiento/publico/QA-EXP-0001 con el CI QA | HTTP 200 | PASS | Coincidió con la validación automatizada. |
| 2 | Validar success y NUREJ | success true y QA-EXP-0001 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones
