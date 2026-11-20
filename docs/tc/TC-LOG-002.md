# TC-LOG-002 Rechazo de contraseña incorrecta

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-002 |
| Prioridad | Alta |
| Tipo | funcional negativo |
| Módulo | autenticación |
| Ambiente | Local QA |
| Requisito | RF-01 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Comprobar el rechazo de una contraseña que no corresponde al usuario.

## Precondiciones

- API disponible
- Usuario abogado QA existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Contraseña | incorrecta-qa | prueba | Partición inválida |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar POST /auth/login con correo válido y contraseña incorrecta | Datos QA del caso | HTTP 401 |
| 2 | Revisar el mensaje de respuesta | Datos QA del caso | Password incorrecto |

## Resultado Esperado Final

HTTP 401 con mensaje Password incorrecto.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
