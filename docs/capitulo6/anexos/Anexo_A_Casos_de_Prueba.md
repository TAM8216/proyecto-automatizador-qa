# Anexo A Casos de Prueba Completos

Este anexo contiene los 16 casos diseñados a partir del catálogo real de IPAS. Los datos son ficticios y las credenciales permanecen fuera del documento.

## TC-SMK-001 Disponibilidad integral de IPAS QA

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


---

## TC-LOG-001 Login válido de abogado desde la interfaz

| Campo | Valor |
|---|---|
| ID del TC | TC-LOG-001 |
| Prioridad | Alta |
| Tipo | funcional |
| Módulo | autenticación |
| Ambiente | Local QA |
| Requisito | RF-01 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar el acceso de un abogado QA mediante la interfaz web.

## Precondiciones

- Frontend y API disponibles
- Usuario abogado ficticio activo
- Navegador Edge compatible

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Correo | qa.abogado@ipas.test | seed QA | Cuenta ficticia |
| Contraseña | Protegida en .env | configuración local | No se incluye en evidencias |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Abrir la página pública de IPAS | Datos QA del caso | Se muestra Acceso equipo |
| 2 | Abrir el diálogo de autenticación | Datos QA del caso | Se muestran correo y contraseña |
| 3 | Ingresar las credenciales QA y confirmar | Datos QA del caso | Navegación a /abogado/dashboard |
| 4 | Esperar el encabezado Mi panel de trabajo | Datos QA del caso | Dashboard completamente cargado |

## Resultado Esperado Final

El sistema autentica al abogado y muestra Mi panel de trabajo.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-LOG-002 Rechazo de contraseña incorrecta

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


---

## TC-LOG-003 Correo obligatorio vacío

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


---

## TC-LOG-004 Verificación de token válido

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


---

## TC-PUB-001 Consulta pública con NUREJ y CI válidos

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-001 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | seguimiento público |
| Ambiente | Local QA |
| Requisito | RF-03 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar la consulta pública protegida de un expediente ficticio.

## Precondiciones

- Seed QA aplicado
- Expediente QA-EXP-0001 relacionado con cliente ficticio

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| NUREJ | QA-EXP-0001 | seed QA | Ficticio |
| CI | QA-CI-0001 | seed QA | Ficticio |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Consultar /seguimiento/publico/QA-EXP-0001 con el CI QA | Datos QA del caso | HTTP 200 |
| 2 | Validar success y NUREJ | Datos QA del caso | success true y QA-EXP-0001 |

## Resultado Esperado Final

HTTP 200 y datos públicos del expediente solicitado.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-PUB-002 Consulta pública rechaza CI incorrecto

| Campo | Valor |
|---|---|
| ID del TC | TC-PUB-002 |
| Prioridad | Alta |
| Tipo | partición de equivalencia inválida |
| Módulo | seguimiento público |
| Ambiente | Local QA |
| Requisito | RF-03 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Impedir que un CI ajeno consulte el seguimiento público.

## Precondiciones

- Expediente QA-EXP-0001 existente

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| CI | CI-NO-VALIDO | prueba | Partición inválida |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Consultar el NUREJ válido con CI incorrecto | Datos QA del caso | HTTP 404 |
| 2 | Revisar success | Datos QA del caso | Valor false |

## Resultado Esperado Final

HTTP 404 sin información del expediente.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-EXP-001 Crear expediente con campos obligatorios

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-001 |
| Prioridad | Alta |
| Tipo | funcional positivo |
| Módulo | expedientes |
| Ambiente | Local QA |
| Requisito | RF-04 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Crear y eliminar un expediente sintético con los campos obligatorios.

## Precondiciones

- Abogado QA autenticado
- Base ius_puniendi_qa

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| NUREJ | QA-AUTO-<uuid> | generado | Único por ejecución |
| Materia | Derecho Civil | prueba | Ficticia |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar POST /casos con delito tipo y asunto | Datos QA del caso | HTTP 201 |
| 2 | Comparar el NUREJ devuelto | Datos QA del caso | Coincide con el generado |
| 3 | Eliminar el caso temporal como admin | Datos QA del caso | HTTP 204 |

## Resultado Esperado Final

Creación HTTP 201, datos persistidos y limpieza HTTP 204.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-EXP-002 Rechazar expediente sin delito

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


---

## TC-EXP-003 Consultar expediente inexistente

| Campo | Valor |
|---|---|
| ID del TC | TC-EXP-003 |
| Prioridad | Media |
| Tipo | funcional negativo |
| Módulo | expedientes |
| Ambiente | Local QA |
| Requisito | RF-04 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar la respuesta ante un identificador de expediente inexistente.

## Precondiciones

- Abogado QA autenticado

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| ID | 999999999 | prueba | Fuera del conjunto existente |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Enviar GET /casos/999999999 | Datos QA del caso | HTTP 404 |

## Resultado Esperado Final

HTTP 404.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-DOC-001 Cargar documento PDF válido

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


---

## TC-DOC-002 Rechazar extensión ejecutable

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


---

## TC-DOC-003 Rechazar archivo mayor a 10 MB

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


---

## TC-ROL-001 Abogado no puede listar usuarios

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


---

## TC-E2E-001 Login y consulta del expediente ficticio

| Campo | Valor |
|---|---|
| ID del TC | TC-E2E-001 |
| Prioridad | Alta |
| Tipo | E2E |
| Módulo | autenticación y expedientes |
| Ambiente | Local QA |
| Requisito | RF-07 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Verificar el recorrido completo desde login hasta el expediente QA visible.

## Precondiciones

- Frontend y API disponibles
- Abogado y expediente ficticios creados

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Expediente | QA-EXP-0001 | seed QA | Sintético |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Autenticar al abogado desde la interfaz | Datos QA del caso | Se muestra el dashboard |
| 2 | Abrir Casos desde el menú lateral | Datos QA del caso | Se muestra Gestión de Casos |
| 3 | Buscar el NUREJ QA-EXP-0001 en la tabla | Datos QA del caso | Expediente visible con datos ficticios |

## Resultado Esperado Final

El abogado inicia sesión y visualiza QA-EXP-0001 en Gestión de Casos.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.


---

## TC-PERF-001 Carga moderada de consultas jurídicas

| Campo | Valor |
|---|---|
| ID del TC | TC-PERF-001 |
| Prioridad | Alta |
| Tipo | rendimiento |
| Módulo | autenticación, expedientes y documentos |
| Ambiente | Local QA |
| Requisito | RNF-01 |
| Diseñado por | Tamengo Sanchez Bustamante Calderon |

## Objetivo

Evaluar tiempos de respuesta y errores de la API local bajo una carga moderada y controlada.

## Precondiciones

- Frontend, API y PostgreSQL disponibles
- IPAS conectado exclusivamente a ius_puniendi_qa
- Usuario abogado y expediente QA-EXP-0001 creados por el seed
- Locust 2.32.6 instalado

## Datos de Prueba

| Dato | Valor | Origen | Observación |
|---|---|---|---|
| Usuarios | 5 | configuración QA | Concurrentes |
| Incremento | 1 usuario/s | configuración QA | Rampa gradual |
| Duración | 30 segundos | configuración QA | Carga moderada |
| Criterio p95 | Menor a 2.000 ms | RNF-01 | Criterio propuesto |
| Criterio de errores | Menor a 1 % | RNF-01 | Criterio propuesto |

## Pasos y Resultados Esperados

| Nro. | Paso o acción | Dato utilizado | Resultado esperado |
|---:|---|---|---|
| 1 | Ejecutar el health-check del ambiente | Datos QA del caso | Frontend, API y base QA disponibles |
| 2 | Iniciar Locust con cinco usuarios y rampa de un usuario por segundo | Datos QA del caso | La carga alcanza cinco usuarios |
| 3 | Autenticar a cada usuario ficticio | Datos QA del caso | Login HTTP 200 y token disponible en memoria |
| 4 | Ejecutar consultas ponderadas de casos y documentos | Datos QA del caso | Solicitudes procesadas sin datos reales |
| 5 | Recolectar CSV, log y métricas agregadas | Datos QA del caso | p95 y tasa de errores comparables con RNF-01 |

## Resultado Esperado Final

p95 menor a 2.000 ms y tasa de errores menor a 1 % durante el perfil configurado.

## Criterio de Éxito

El caso se considera PASS cuando todos los pasos y aserciones coinciden con el resultado esperado final. Cualquier diferencia verificable se registra como FAIL; un impedimento externo se registra como BLOCKED.
