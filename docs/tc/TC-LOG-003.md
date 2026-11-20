# TC-LOG-003 Correo obligatorio vacío

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-003 |
| Prioridad | Alta |
| Tipo | valor límite |
| Módulo | autenticación |
| Ambiente | Local QA |
| Requisito | RF-01 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Validar el límite inferior del campo correo obligatorio.

## Precondiciones

- API disponible

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Email | Cadena vacía | prueba | Valor límite |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar POST /auth/login con email vacío | Datos QA del caso | HTTP 400 |
| 2 | Revisar el mensaje de validación | Datos QA del caso | Indica campos obligatorios |

## Resultado Esperado Final

HTTP 400 indicando que email y password son obligatorios.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
