# EJ-TC-LOG-001 Ejecución de TC-LOG-001

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
