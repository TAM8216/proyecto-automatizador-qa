# Anexo B Ejecuciones Completas

Las fichas siguientes documentan una ejecución por cada ID único. TC-SMK-001 y TC-LOG-001 también fueron ejecutados en smoke, pero se usa la regresión como registro de cierre para evitar duplicar el resultado global.

| Suite | Run ID | Inicio | Duración | Total | PASS | FAIL | BLOCKED | NOT RUN |
|---|---|---|---:|---:|---:|---:|---:|---:|
| smoke | `4a5768c2-f856-4f88-ac8f-787dd0ad47d4` | 2026-11-17T00:33:39-04:00 | 21.218 s | 2 | 2 | 0 | 0 | 0 |
| carga_local | `537b1503-ed43-4b11-891f-379887f2733e` | 2026-11-17T12:24:22-04:00 | 33.66 s | 1 | 1 | 0 | 0 | 0 |
| regression | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` | 2026-11-17T12:49:53-04:00 | 29.139 s | 14 | 14 | 0 | 0 | 0 |
| controlled_fail | `dd68354b-0cb1-4d65-8d8e-f23d4b83142c` | 2026-11-17T12:50:36-04:00 | 4.579 s | 1 | 0 | 1 | 0 | 0 |

## EJ-TC-SMK-001 Ejecución de TC-SMK-001

| Campo | Valor |
|---|---|
| ID del TC | TC-SMK-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 2.61 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: Frontend HTTP 200, API accesible con HTTP 401 sin token y conexión a ius_puniendi_qa.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Consultar la URL del frontend | HTTP 200 | PASS | Coincidió con la validación automatizada. |
| 2 | Consultar auth verify sin token | HTTP 401 que confirma disponibilidad | PASS | Coincidió con la validación automatizada. |
| 3 | Abrir conexión PostgreSQL y consultar current_database | Nombre exacto ius_puniendi_qa | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-LOG-001 Ejecución de TC-LOG-001

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 6.65 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: El sistema autentica al abogado y muestra Mi panel de trabajo.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Abrir la página pública de IPAS | Se muestra Acceso equipo | PASS | Coincidió con la validación automatizada. |
| 2 | Abrir el diálogo de autenticación | Se muestran correo y contraseña | PASS | Coincidió con la validación automatizada. |
| 3 | Ingresar las credenciales QA y confirmar | Navegación a /abogado/dashboard | PASS | Coincidió con la validación automatizada. |
| 4 | Esperar el encabezado Mi panel de trabajo | Dashboard completamente cargado | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html; evidencias/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/TC-LOG-001/.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-LOG-002 Ejecución de TC-LOG-002

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-002 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.409 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 401 con mensaje Password incorrecto.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar POST /auth/login con correo válido y contraseña incorrecta | HTTP 401 | PASS | Coincidió con la validación automatizada. |
| 2 | Revisar el mensaje de respuesta | Password incorrecto | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-LOG-003 Ejecución de TC-LOG-003

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-003 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 4.093 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 400 indicando que email y password son obligatorios.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar POST /auth/login con email vacío | HTTP 400 | PASS | Coincidió con la validación automatizada. |
| 2 | Revisar el mensaje de validación | Indica campos obligatorios | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-LOG-004 Ejecución de TC-LOG-004

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-004 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.204 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 200 con rol abogado y correo ficticio.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Autenticar al abogado QA | Se obtiene JWT | PASS | Coincidió con la validación automatizada. |
| 2 | Enviar GET /auth/verify con Bearer token | HTTP 200 | PASS | Coincidió con la validación automatizada. |
| 3 | Comparar rol y correo | Coinciden con el usuario QA | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-PUB-001 Ejecución de TC-PUB-001

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.029 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 200 y datos públicos del expediente solicitado.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Consultar /seguimiento/publico/QA-EXP-0001 con el CI QA | HTTP 200 | PASS | Coincidió con la validación automatizada. |
| 2 | Validar success y NUREJ | success true y QA-EXP-0001 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-PUB-002 Ejecución de TC-PUB-002

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-002 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.005 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 404 sin información del expediente.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Consultar el NUREJ válido con CI incorrecto | HTTP 404 | PASS | Coincidió con la validación automatizada. |
| 2 | Revisar success | Valor false | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-EXP-001 Ejecución de TC-EXP-001

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.21 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: Creación HTTP 201, datos persistidos y limpieza HTTP 204.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar POST /casos con delito tipo y asunto | HTTP 201 | PASS | Coincidió con la validación automatizada. |
| 2 | Comparar el NUREJ devuelto | Coincide con el generado | PASS | Coincidió con la validación automatizada. |
| 3 | Eliminar el caso temporal como admin | HTTP 204 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-EXP-002 Ejecución de TC-EXP-002

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-002 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.003 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 400 indicando campos requeridos.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar POST /casos sin delito | HTTP 400 | PASS | Coincidió con la validación automatizada. |
| 2 | Revisar el mensaje | Indica campos requeridos | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-EXP-003 Ejecución de TC-EXP-003

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-003 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.002 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 404.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar GET /casos/999999999 | HTTP 404 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-DOC-001 Ejecución de TC-DOC-001

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.016 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: Carga HTTP 201 y eliminación HTTP 204.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar multipart PDF a /documentos/casos/{id} | HTTP 201 | PASS | Coincidió con la validación automatizada. |
| 2 | Recuperar el ID creado | ID de documento presente | PASS | Coincidió con la validación automatizada. |
| 3 | Eliminar el documento temporal | HTTP 204 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-DOC-002 Ejecución de TC-DOC-002

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-002 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.003 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 400 con mensaje de tipos permitidos.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Enviar archivo .exe por multipart | HTTP 400 | PASS | Coincidió con la validación automatizada. |
| 2 | Revisar el mensaje | Informa tipos permitidos | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-DOC-003 Ejecución de TC-DOC-003

| Campo | Valor |
|---|---|
| ID del TC | TC-DOC-003 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 0.041 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: HTTP 400 con error File too large.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Generar el PDF sintético de 10.485.770 bytes | El archivo supera el límite de 10 MB en 10 bytes | PASS | Coincidió con la validación automatizada. |
| 2 | Enviar el archivo por multipart | HTTP 400 | PASS | Coincidió con la validación automatizada. |
| 3 | Revisar el mensaje | File too large | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-ROL-001 Ejecución de TC-ROL-001

| Campo | Valor |
|---|---|
| ID del TC | TC-ROL-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:50:36 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `dd68354b-0cb1-4d65-8d8e-f23d4b83142c` |
| Estado | FAIL |
| Duración del caso | 0.466 segundos |

## Resultado Observado

El endpoint devolvió HTTP 200 y el listado de usuarios al rol abogado; se esperaba HTTP 403 sin datos.

## Comparación

No coincide: se obtuvo HTTP 200 en lugar de HTTP 403.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Autenticar al abogado QA | JWT válido | PASS | Coincidió con la validación automatizada. |
| 2 | Enviar GET /usuarios | HTTP 200 con listado de usuarios | FAIL | Se esperaba HTTP 403; se vinculó BUG-01-F. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/dd68354b-0cb1-4d65-8d8e-f23d4b83142c/result.json, junit.xml, pytest.log y pytest.html.

## Desviación y Defecto

- **Desviación encontrada:** El backend autenticó al abogado, pero no aplicó autorización por rol al listar usuarios.
- **Referencia del defecto:** BUG-01-F.

## Observaciones

AssertionError: BUG-01-F: un abogado autenticado pudo listar usuarios; respuesta HTTP observada=200 assert 200 == 403  +  where 200 = <Response [200 OK]>.status_code


---

## EJ-TC-E2E-001 Ejecución de TC-E2E-001

| Campo | Valor |
|---|---|
| ID del TC | TC-E2E-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:49:53 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `4a2c9ce1-0a85-4208-91bb-f9dd03db004b` |
| Estado | PASS |
| Duración del caso | 6.834 segundos |

## Resultado Observado

Las aserciones automatizadas confirmaron el comportamiento esperado: El abogado inicia sesión y visualiza QA-EXP-0001 en Gestión de Casos.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Autenticar al abogado desde la interfaz | Se muestra el dashboard | PASS | Coincidió con la validación automatizada. |
| 2 | Abrir Casos desde el menú lateral | Se muestra Gestión de Casos | PASS | Coincidió con la validación automatizada. |
| 3 | Buscar el NUREJ QA-EXP-0001 en la tabla | Expediente visible con datos ficticios | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/result.json, junit.xml, pytest.log y pytest.html; evidencias/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/TC-E2E-001/.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

Sin observaciones


---

## EJ-TC-PERF-001 Ejecución de TC-PERF-001

| Campo | Valor |
|---|---|
| ID del TC | TC-PERF-001 |
| Ejecutado por | Tamengo Sanchez Bustamante Calderon |
| Fecha | 17/11/2026 |
| Hora de inicio de la corrida | 12:24:22 UTC-4 |
| Ambiente | Windows local QA, IPAS y PostgreSQL 17 |
| Versión | Backend IPAS 1.0.0; frontend IPAS 0.1.0 |
| Run ID | `537b1503-ed43-4b11-891f-379887f2733e` |
| Estado | PASS |
| Duración del caso | 33.66 segundos |

## Resultado Observado

191 solicitudes, 0 fallos, p95 de 18 ms, tasa de errores de 0,00 % y throughput de 6,809 solicitudes/s.

## Comparación

Coincide con lo esperado.

## Registro por Paso

| Nro. | Paso ejecutado | Resultado observado | Estado | Observación |
|---:|---|---|---|---|
| 1 | Ejecutar el health-check del ambiente | Frontend, API y base QA disponibles | PASS | Coincidió con la validación automatizada. |
| 2 | Iniciar Locust con cinco usuarios y rampa de un usuario por segundo | La carga alcanza cinco usuarios | PASS | Coincidió con la validación automatizada. |
| 3 | Autenticar a cada usuario ficticio | Login HTTP 200 y token disponible en memoria | PASS | Coincidió con la validación automatizada. |
| 4 | Ejecutar consultas ponderadas de casos y documentos | Solicitudes procesadas sin datos reales | PASS | Coincidió con la validación automatizada. |
| 5 | Recolectar CSV, log y métricas agregadas | p95 y tasa de errores comparables con RNF-01 | PASS | Coincidió con la validación automatizada. |

## Evidencia

- **Tipo:** resultado estructurado, log y reporte técnico.
- **Referencia:** reports/537b1503-ed43-4b11-891f-379887f2733e/result.json, locust_stats.csv, locust_stats_history.csv, locust.log, DOCX y HTML.

## Desviación y Defecto

- **Desviación encontrada:** Ninguna.
- **Referencia del defecto:** N/A.

## Observaciones

p95=18.0 ms; errores=0.00%; throughput=6.809 req/s
