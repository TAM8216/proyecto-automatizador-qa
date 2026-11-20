# TC-EXP-002 Rechazar expediente sin delito

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-002 |
| Prioridad | Alta |
| Tipo | partición de equivalencia inválida |
| Módulo | expedientes |
| Ambiente | Local QA |
| Requisito | RF-04 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Validar que delito sea obligatorio al crear un expediente.

## Precondiciones

- Abogado QA autenticado

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Delito | Ausente | prueba | Partición inválida |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar POST /casos sin delito | Datos QA del caso | HTTP 400 |
| 2 | Revisar el mensaje | Datos QA del caso | Indica campos requeridos |

## Resultado Esperado Final

HTTP 400 indicando campos requeridos.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
