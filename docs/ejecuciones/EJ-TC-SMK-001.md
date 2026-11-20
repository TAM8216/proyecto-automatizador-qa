# EJ-TC-SMK-001 Ejecución de TC-SMK-001

| Campo | Valor |
|---|---|
| ID del TC | TC-SMK-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 2.61 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: Frontend HTTP 200, API accesible con HTTP 401 sin token y conexión a ius_puniendi_qa.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Consultar la URL del frontend | HTTP 200 | PASS | Coincidió con la validación automatizada. |
| 2 | Consultar auth verify sin token | HTTP 401 que confirma disponibilidad | PASS | Coincidió con la validación automatizada. |
| 3 | Abrir conexión PostgreSQL y consultar current_database | Nombre exacto ius_puniendi_qa | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones
