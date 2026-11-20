# TC-DOC-002 Rechazar extensión ejecutable

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-002 |
| Prioridad | Alta |
| Tipo | partición de equivalencia inválida |
| Módulo | documentos |
| Ambiente | Local QA |
| Requisito | RF-05 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Confirmar el rechazo de una extensión ejecutable.

## Precondiciones

- Abogado QA autenticado
- Expediente QA existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Archivo | malware.exe | generado en memoria | Contenido inerte |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar archivo .exe por multipart | Datos QA del caso | HTTP 400 |
| 2 | Revisar el mensaje | Datos QA del caso | Informa tipos permitidos |

## Resultado Esperado Final

HTTP 400 con mensaje de tipos permitidos.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
