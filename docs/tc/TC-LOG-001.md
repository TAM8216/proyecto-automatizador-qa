# TC-LOG-001 Login válido de abogado desde la interfaz

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
