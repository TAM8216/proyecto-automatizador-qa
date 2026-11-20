# TC-PUB-001 Consulta pública con NUREJ y CI válidos

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-001 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | seguimiento público |
| Ambiente | Local QA |
| Requisito | RF-03 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar la consulta pública protegida de un expediente ficticio.

## Precondiciones

- Seed QA aplicado
- Expediente QA-EXP-0001 relacionado con cliente ficticio

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| NUREJ | QA-EXP-0001 | seed QA | Ficticio |
| CI | QA-CI-0001 | seed QA | Ficticio |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Consultar /seguimiento/publico/QA-EXP-0001 con el CI QA | Datos QA del caso | HTTP 200 |
| 2 | Validar success y NUREJ | Datos QA del caso | success true y QA-EXP-0001 |

## Resultado Esperado Final

HTTP 200 y datos públicos del expediente solicitado.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
