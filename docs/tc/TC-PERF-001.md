# TC-PERF-001 Carga moderada de consultas jurídicas

| Campo | Valor |
|---|---|
| ID del TC | TC-PERF-001 |
| Prioridad | Alta |
| Tipo | rendimiento |
| Módulo | autenticación, expedientes y documentos |
| Ambiente | Local QA |
| Requisito | RNF-01 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Evaluar tiempos de respuesta y errores de la API local bajo una carga moderada y controlada.

## Precondiciones

- Frontend, API y PostgreSQL disponibles
- IPAS conectado exclusivamente a ius_puniendi_qa
- Usuario abogado y expediente QA-EXP-0001 creados por el seed
- Locust 2.32.6 instalado

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Usuarios | 5 | configuración QA | Concurrentes |
| Incremento | 1 usuario/s | configuración QA | Rampa gradual |
| Duración | 30 segundos | configuración QA | Carga moderada |
| Criterio p95 | Menor a 2.000 ms | RNF-01 | Criterio propuesto |
| Criterio de errores | Menor a 1 % | RNF-01 | Criterio propuesto |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Ejecutar el health-check del ambiente | Datos QA del caso | Frontend, API y base QA disponibles |
| 2 | Iniciar Locust con cinco usuarios y rampa de un usuario por segundo | Datos QA del caso | La carga alcanza cinco usuarios |
| 3 | Autenticar a cada usuario ficticio | Datos QA del caso | Login HTTP 200 y token disponible en memoria |
| 4 | Ejecutar consultas ponderadas de casos y documentos | Datos QA del caso | Solicitudes procesadas sin datos reales |
| 5 | Recolectar CSV, log y métricas agregadas | Datos QA del caso | p95 y tasa de errores comparables con RNF-01 |

## Resultado Esperado Final

p95 menor a 2.000 ms y tasa de errores menor a 1 % durante el perfil configurado.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
