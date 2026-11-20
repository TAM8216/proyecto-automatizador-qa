# TC-SMK-001 Disponibilidad integral de IPAS QA

| Campo | Valor |
|---|---|
| ID del TC | TC-SMK-001 |
| Prioridad | Alta |
| Tipo | funcional |
| Módulo | infraestructura local |
| Ambiente | Local QA |
| Requisito | Criterio técnico de entrada |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Confirmar que frontend, API y base QA están disponibles antes de ejecutar pruebas.

## Precondiciones

- PostgreSQL 17 iniciado
- IPAS levantado con ius_puniendi_qa
- puertos locales libres y configurados

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Ambiente | local-qa | configuración | Sin datos reales |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Consultar la URL del frontend | Datos QA del caso | HTTP 200 |
| 2 | Consultar auth verify sin token | Datos QA del caso | HTTP 401 que confirma disponibilidad |
| 3 | Abrir conexión PostgreSQL y consultar current_database | Datos QA del caso | Nombre exacto ius_puniendi_qa |

## Resultado Esperado Final

Frontend HTTP 200, API accesible con HTTP 401 sin token y conexión a ius_puniendi_qa.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
