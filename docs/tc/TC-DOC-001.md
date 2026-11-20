# TC-DOC-001 Cargar documento PDF válido

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-001 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | documentos |
| Ambiente | Local QA |
| Requisito | RF-05 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Comprobar la carga y limpieza de un PDF sintético permitido.

## Precondiciones

- Abogado QA autenticado
- Expediente QA-EXP-0001 existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Archivo | evidencia_qa.pdf | generado en memoria | Sin información jurídica real |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar multipart PDF a /documentos/casos/{id} | Datos QA del caso | HTTP 201 |
| 2 | Recuperar el ID creado | Datos QA del caso | ID de documento presente |
| 3 | Eliminar el documento temporal | Datos QA del caso | HTTP 204 |

## Resultado Esperado Final

Carga HTTP 201 y eliminación HTTP 204.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
