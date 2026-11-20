# TC-ROL-001 Abogado no puede listar usuarios

| Campo | Valor |
|---|---|
| ID del TC | TC-ROL-001 |
| Prioridad | Alta |
| Tipo | seguridad negativo |
| Módulo | roles y permisos |
| Ambiente | Local QA |
| Requisito | RF-06 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Impedir que un abogado obtenga el listado administrativo de usuarios.

## Precondiciones

- Abogado QA autenticado
- Endpoint /usuarios disponible

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Rol | abogado | seed QA | Privilegios insuficientes esperados |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Autenticar al abogado QA | Datos QA del caso | JWT válido |
| 2 | Enviar GET /usuarios | Datos QA del caso | HTTP 403 |

## Resultado Esperado Final

HTTP 403 sin listado de usuarios.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
