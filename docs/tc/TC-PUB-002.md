# TC-PUB-002 Consulta pública rechaza CI incorrecto

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-002 |
| Prioridad | Alta |
| Tipo | partición de equivalencia inválida |
| Módulo | seguimiento público |
| Ambiente | Local QA |
| Requisito | RF-03 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Impedir que un CI ajeno consulte el seguimiento público.

## Precondiciones

- Expediente QA-EXP-0001 existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| CI | CI-NO-VALIDO | prueba | Partición inválida |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Consultar el NUREJ válido con CI incorrecto | Datos QA del caso | HTTP 404 |
| 2 | Revisar success | Datos QA del caso | Valor false |

## Resultado Esperado Final

HTTP 404 sin información del expediente.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
