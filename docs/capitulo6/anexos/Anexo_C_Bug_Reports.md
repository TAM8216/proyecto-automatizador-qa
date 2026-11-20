# Anexo C Bug Reports

## BUG-01-F Abogado puede listar todos los usuarios

| Campo | Registro |
|---|---|
| Fecha | 17 de noviembre de 2026 |
| Reportado por | Tamengo Sanchez Bustamante Calderon |
| Estado | Abierto, pendiente de corrección |
| Responsable de seguimiento | Tamengo Sanchez Bustamante Calderon |
| Caso relacionado | TC-ROL-001 |
| Requisito | RF-06 |
| Descripción | `GET /api/usuarios` exige JWT, pero no restringe el rol; un abogado obtiene el listado completo. |
| Pasos | Autenticar al abogado QA y enviar `GET /api/usuarios` con su token. |
| Resultado actual | HTTP 200 con listado de usuarios. |
| Resultado esperado | HTTP 403 sin datos de usuarios. |
| Prioridad | 1/5 |
| Severidad | 2/5 |
| Ambiente | Windows local QA, Node.js 24, PostgreSQL 17 |
| Evidencia | Run `dd68354b-0cb1-4d65-8d8e-f23d4b83142c`, `result.json`, JUnit, log y pytest HTML |
| Comentario técnico | La corrección debe aplicar autorización para `superadmin` y `admin` en backend; ocultar una ruta en React no impide el acceso directo. |
