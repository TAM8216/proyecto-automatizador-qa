# TC-LOG-004 Verificación de token válido

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-004 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | autenticación |
| Ambiente | Local QA |
| Requisito | RF-02 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Confirmar que un JWT válido permite recuperar la identidad del abogado.

## Precondiciones

- Usuario abogado QA autenticable

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Token | Generado durante la prueba | POST /auth/login | No se guarda en reportes |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Autenticar al abogado QA | Datos QA del caso | Se obtiene JWT |
| 2 | Enviar GET /auth/verify con Bearer token | Datos QA del caso | HTTP 200 |
| 3 | Comparar rol y correo | Datos QA del caso | Coinciden con el usuario QA |

## Resultado Esperado Final

HTTP 200 con rol abogado y correo ficticio.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
