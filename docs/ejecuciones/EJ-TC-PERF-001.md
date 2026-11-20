# EJ-TC-PERF-001 Ejecución de TC-PERF-001

| Campo | Valor |
|---|---|
| ID del TC | TC-PERF-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:24:22 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `537b1503-ed43-4b11-891f-379887f2733e` |
| Estado | PASS |
| Duración del caso | 33.66 segundos |

## Resultado Observado

191 solicitudes, 0 fallos, p95 de 18 ms, tasa de errores de 0,00 % y throughput de 6,809 solicitudes/s.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Ejecutar el health-check del ambiente | Frontend, API y base QA disponibles | PASS | Coincidió con la validación automatizada. |
| 2 | Iniciar Locust con cinco usuarios y rampa de un usuario por segundo | La carga alcanza cinco usuarios | PASS | Coincidió con la validación automatizada. |
| 3 | Autenticar a cada usuario ficticio | Login HTTP 200 y token disponible en memoria | PASS | Coincidió con la validación automatizada. |
| 4 | Ejecutar consultas ponderadas de casos y documentos | Solicitudes procesadas sin datos reales | PASS | Coincidió con la validación automatizada. |
| 5 | Recolectar CSV, log y métricas agregadas | p95 y tasa de errores comparables con RNF-01 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/537b1503-ed43-4b11-891f-379887f2733e/result.json, locust_stats.csv, locust_stats_history.csv, locust.log, DOCX y HTML.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

p95=18.0 ms; errores=0.00%; throughput=6.809 req/s
