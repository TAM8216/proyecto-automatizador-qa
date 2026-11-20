# TC-EXP-001 Crear expediente con campos obligatorios

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-001 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | expedientes |
| Ambiente | Local QA |
| Requisito | RF-04 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Crear y eliminar un expediente sintético con los campos obligatorios.

## Precondiciones

- Abogado QA autenticado
- Base ius_puniendi_qa

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| NUREJ | QA-AUTO-<uuid> | generado | Único por ejecución |
| Materia | Derecho Civil | prueba | Ficticia |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar POST /casos con delito tipo y asunto | Datos QA del caso | HTTP 201 |
| 2 | Comparar el NUREJ devuelto | Datos QA del caso | Coincide con el generado |
| 3 | Eliminar el caso temporal como admin | Datos QA del caso | HTTP 204 |

## Resultado Esperado Final

Creación HTTP 201, datos persistidos y limpieza HTTP 204.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
