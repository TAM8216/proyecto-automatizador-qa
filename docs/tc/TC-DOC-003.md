# TC-DOC-003 Rechazar archivo mayor a 10 MB

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-003 |
| Prioridad | Alta |
| Tipo | valor límite |
| Módulo | documentos |
| Ambiente | Local QA |
| Requisito | RF-05 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Validar el límite superior de 10 MB para documentos.

## Precondiciones

- Abogado QA autenticado
- Expediente QA existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Tamaño | 10.485.770 bytes: 10 MB más 10 bytes | generado en memoria | PDF sintético con cabecera de 9 bytes y 10 MB más 1 byte de relleno |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Generar el PDF sintético de 10.485.770 bytes | Datos QA del caso | El archivo supera el límite de 10 MB en 10 bytes |
| 2 | Enviar el archivo por multipart | Datos QA del caso | HTTP 400 |
| 3 | Revisar el mensaje | Datos QA del caso | File too large |

## Resultado Esperado Final

HTTP 400 con error File too large.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
