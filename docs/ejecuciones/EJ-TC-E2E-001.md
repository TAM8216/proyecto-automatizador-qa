# EJ-TC-E2E-001 Ejecución de TC-E2E-001

| Campo | Valor |
|---|---|
| ID del TC | TC-E2E-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 6.834 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: El abogado inicia sesión y visualiza QA-EXP-0001 en Gestión de Casos.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Autenticar al abogado desde la interfaz | Se muestra el dashboard | PASS | Coincidió con la validación automatizada. |
| 2 | Abrir Casos desde el menú lateral | Se muestra Gestión de Casos | PASS | Coincidió con la validación automatizada. |
| 3 | Buscar el NUREJ QA-EXP-0001 en la tabla | Expediente visible con datos ficticios | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html; evidencias/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/TC-E2E-001/.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones
