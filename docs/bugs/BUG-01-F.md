# BUG-01-F — Abogado puede listar todos los usuarios

- **Fecha de registro:** 17 de noviembre de 2026.
- **Reportado por:** Tamengo Sanchez Bustamante Calderon.
- **Estado:** Abierto, pendiente de corrección.
- **Responsable de seguimiento:** Tamengo Sanchez Bustamante Calderon.
- **Descripción:** el endpoint `GET /api/usuarios` exige JWT, pero no restringe el rol. Un usuario `abogado` obtiene el listado completo.
- **Referencia:** TC-ROL-001.
- **Pasos:** iniciar sesión como abogado QA; enviar `GET /api/usuarios` con su token.
- **Resultado actual:** HTTP 200 con listado de usuarios.
- **Resultado esperado:** HTTP 403 y mensaje de privilegios insuficientes.
- **Prioridad:** 1/5.
- **Severidad:** 2/5.
- **Ambiente:** Windows, IPAS local QA, Node.js 24, PostgreSQL 17.
- **Adjuntos:** reporte del run de la suite `controlled_fail`.
- **Comentarios:** posible exposición de datos personales. La corrección debe aplicar `authorize(['superadmin','admin'])` en backend; no basta ocultar la ruta en React.

