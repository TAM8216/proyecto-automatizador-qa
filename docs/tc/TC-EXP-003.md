# TC-EXP-003 Consultar expediente inexistente

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-003 |
| Prioridad | Media |
| Tipo | funcional negativo |
| Módulo | expedientes |
| Ambiente | Local QA |
| Requisito | RF-04 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar la respuesta ante un identificador de expediente inexistente.

## Precondiciones

- Abogado QA autenticado

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| ID | 999999999 | prueba | Fuera del conjunto existente |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar GET /casos/999999999 | Datos QA del caso | HTTP 404 |

## Resultado Esperado Final

HTTP 404.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
