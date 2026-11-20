# Inventario de fuentes para el Capítulo 6

## Resultado del inventario

Existe evidencia suficiente para redactar el plan de pruebas, las pruebas funcionales y automatizadas, la prueba de carga, la ejecución, los resultados, las conclusiones y las recomendaciones. El catálogo contiene 15 casos funcionales —14 estables y un FAIL controlado— y un caso no funcional. La regresión real del 17 de noviembre de 2026 finalizó con 14 PASS de 14 casos, mientras que la ejecución separada del caso de permisos confirmó el defecto BUG-01-F. La prueba de carga produjo 191 solicitudes sin errores.

Las principales brechas son documentales: no existen todavía casos completos en `docs/tc`, no existen registros completos en `docs/ejecuciones`, no se documentó una ejecución manual ni un retesting y no se implementó CI/CD. Los IDs documentales fueron autorizados y se definieron a partir de funcionalidades realmente verificadas.

## Matriz de disponibilidad por sección

| Sección | Datos reales disponibles | Fuentes verificadas | Datos faltantes o tratamiento |
|---|---|---|---|
| 6.1 Plan de Pruebas | Propósito de IPAS; módulos cubiertos; estrategia funcional, API, UI, E2E y rendimiento; ambiente local QA; datos ficticios; herramientas; health-check; gestión de defectos; riesgos de datos sensibles, IA y OneDrive. | `dashboard-legal/README.md`, `dashboard-legal/DEMO.md`, `qa-platform/README.md`, `config/test_catalog.yaml`, `config/test_details.yaml`, `.env.example`, `requirements.txt`, `data/seed/seed_qa.py`, `backend/runner/health.py`. | El autor, ejecutor y responsable es Tamengo Sanchez Bustamante Calderon. El cronograma autorizado abarca del 1 de julio al 17 de noviembre de 2026. No existe una versión integral única de IPAS; se usarán las versiones de componentes. La RAM del equipo no se registró. |
| 6.2 Pruebas Funcionales | Autenticación, seguimiento público, expedientes, documentos, roles, health-check y flujo E2E; técnicas de partición de equivalencia y valores límite; objetivos, precondiciones, datos, pasos y resultados esperados de los 15 TC. | `config/test_catalog.yaml`, `config/test_details.yaml`, `tests/api/`, `tests/functional/`, `pages/`, `data/seed/seed_qa.py`, `docs/capitulo6/requisitos_documentales.md`. | Se definieron RF-01 a RF-07 y RNF-01 como IDs documentales, sin ampliar el alcance funcional. Faltan los TC completos en `docs/tc`. |
| 6.3 Pruebas Automatizadas | Arquitectura FastAPI, pytest, Selenium POM, httpx, catálogo YAML, worker, evidencias, reportes, SMTP y frontend React; 14 casos estables automatizados; registro DOM de 7 locators; módulo IA con Groq; prueba real de análisis IA. | `backend/`, `frontend/`, `tests/`, `pages/`, `config/dom_selectors.json`, `scripts/inspect_dom_stage8.py`, `docs/ia/feeaf1ec-4d07-4e3b-901e-89e582f58d20/`. | CI/CD: **No implementado**, registrado como mejora futura. La cobertura final se calculó sobre los 15 casos funcionales seleccionados y los 16 casos globales al incluir rendimiento. La generación IA no continuó porque el análisis real solicitó seis aclaraciones. |
| 6.4 Pruebas No Funcionales | Locust 2.32.6; 5 usuarios; incremento de 1 usuario/s; 30 s; 191 solicitudes; 6,809 req/s; promedio 11,393 ms; mediana 5 ms; p95 18 ms; mínimo 2,407 ms; máximo 283,49 ms; 0 % de errores. Criterio propuesto: p95 menor a 2.000 ms y errores menores a 1 %. | `tests/non_functional/locustfile.py`, `reports/537b1503-ed43-4b11-891f-379887f2733e/result.json`, CSV y log de la misma corrida, DOCX y HTML generados. | CPU, memoria, red y base de datos: **No medidos**. Estrés y soak: **No realizados**; se justificarán como trabajo futuro. Los endpoints de IA fueron excluidos deliberadamente de la carga. |
| 6.5 Ejecución de Pruebas | Regresión automatizada real; ejecución aislada del FAIL controlado; ejecución de carga; logs, JUnit, HTML, capturas y resultados JSON; relación TC-ROL-001 → BUG-01-F. | `reports/4a2c9ce1-0a85-4208-91bb-f9dd03db004b/`, `reports/dd68354b-0cb1-4d65-8d8e-f23d4b83142c/`, `reports/537b1503-ed43-4b11-891f-379887f2733e/`, `evidencias/`, `docs/bugs/BUG-01-F.md`. | Ejecución manual: **No documentada**. Retesting: **No realizado**, porque BUG-01-F no fue corregido. Faltan registros completos en `docs/ejecuciones`. |
| 6.6 Resultados | Regresión: 14 diseñados y ejecutados, 14 PASS, 0 FAIL, 0 SKIPPED/BLOCKED y 0 NOT RUN. Caso controlado: 1 FAIL funcional. Carga: 1 PASS y métricas reales. Un defecto registrado. | Los tres `result.json` indicados en 6.5, `docs/bugs/BUG-01-F.md`, reportes HTML y DOCX. | El resumen global deberá separar la suite estable del caso controlado para no presentar 14 PASS y 1 FAIL como una sola ejecución. No se calcularán ahorros de tiempo porque no existe medición manual comparable. |
| 6.7 Conclusiones | Se puede concluir sobre los módulos realmente evaluados, la estabilidad de la regresión, el defecto de autorización, el aporte de automatización y las limitaciones del escenario de carga. | Evidencias de 6.2 a 6.6. | Se redactará después de aprobar los resultados de las secciones anteriores. No se afirmará capacidad máxima ni ausencia total de defectos. |
| 6.8 Recomendaciones | Corregir RBAC en `/api/usuarios`; ejecutar retesting y regresión; ampliar pruebas de roles; incorporar CI/CD; ejecutar estrés y soak; monitorear recursos; mantener datos ficticios y revisar selectores. | `docs/bugs/BUG-01-F.md`, resultados y limitaciones registradas. | Las recomendaciones se presentarán como acciones futuras, no como funciones implementadas. |
| Anexo A Casos de prueba | La plantilla del curso define identificación, objetivo, precondiciones, datos, pasos, resultado esperado y criterio de éxito. Los datos fuente de 15 TC están completos en YAML. | ZIP `proyecto_integrador.zip`, `Plantilla_TC_y_Ejecucion_TQA (2).docx`, `config/test_details.yaml`. | Crear archivos completos en `docs/tc` sin copiar ejemplos ajenos. |
| Anexo B Ejecuciones | La plantilla define tester, fecha, hora, ambiente, versión, estado, observado, comparación, pasos, evidencia, desviación y defecto. Los resultados técnicos existen. | Plantilla del ZIP, `reports/`, `evidencias/`. | Crear registros completos en `docs/ejecuciones`. El ejecutor es Tamengo Sanchez Bustamante Calderon; se consignarán versiones de componentes porque IPAS no tiene una versión integral única. |
| Anexo C Bug Reports | BUG-01-F contiene descripción, pasos, resultado actual y esperado, prioridad, severidad, ambiente y relación con TC-ROL-001. | `docs/bugs/BUG-01-F.md`, corrida `dd68354b-0cb1-4d65-8d8e-f23d4b83142c`. | Estado: Abierto, pendiente de corrección. Responsable de seguimiento: Tamengo Sanchez Bustamante Calderon. |
| Anexo D Evidencias | 39 capturas PNG, JUnit, logs, HTML de pytest, CSV de Locust y resultados JSON. | `evidencias/`, `reports/`. | Asignar códigos EV-xx y EV-NF-xx sin duplicar ni usar capturas de código como evidencia de ejecución. |
| Anexo E Reportes | Cinco DOCX y reportes HTML autocontenidos de ejecuciones reales; el run de carga contiene ambos formatos. | `reports/`, especialmente `537b1503-ed43-4b11-891f-379887f2733e/`. | Seleccionar reportes representativos y evitar incluir artefactos de corridas fallidas por infraestructura como resultado principal. |
| Anexo F Prompts de IA | Entrada ficticia, prompt, salida, proveedor, modelo, uso y estado de revisión guardados. | `docs/ia/feeaf1ec-4d07-4e3b-901e-89e582f58d20/`. | Faltan aclaraciones humanas, generación de Gherkin/POM/pytest y aprobación; se documentará la ejecución parcial real, sin simular las fases no realizadas. |

## Ambiente verificado

| Elemento | Valor observado | Fuente |
|---|---|---|
| Sistema operativo | Microsoft Windows 10.0.26300, arquitectura x64 | Runtime del equipo de prueba |
| Equipo | ASUS TUF Gaming F16 FX607JV | Registro local del sistema |
| Navegador | Microsoft Edge 157.0.4341.60 | Binario utilizado por Selenium |
| SUT backend | 1.0.0 | `dashboard-legal/Backend/package.json` |
| SUT cliente | 0.1.0, React 19.2.0 | `dashboard-legal/client/package.json` |
| Plataforma QA frontend | 0.6.0, React 18.3.1, MUI 6.4.0, Vite 6.0.7 | `qa-platform/frontend/package.json` |
| Automatización | Python 3.11.9, pytest 8.3.4, Selenium 4.27.1, Locust 2.32.6 | Entorno virtual y `requirements.txt` |
| Base de datos | PostgreSQL 17, `ius_puniendi_qa` | health-check y configuración QA |
| IA de valor agregado | Groq, `openai/gpt-oss-120b` | análisis real `feeaf1ec-4d07-4e3b-901e-89e582f58d20` |

## Riesgos detectados durante el inventario

1. El SUT contiene una clave de un servicio de jurisprudencia escrita directamente en un archivo de rutas. El valor no se reproduce en este inventario. Debe migrarse a una variable de entorno, previa aprobación para modificar `dashboard-legal`.
2. La llave Groq está en el `.env` del backend del SUT. Para la prueba del módulo IA se inyectó solamente en memoria; no se copió a reportes, prompts ni archivos versionables.
3. La carpeta está sincronizada con OneDrive, por lo que `node_modules`, `.venv`, `evidencias` y `reports` pueden causar bloqueos o sincronización innecesaria si no se excluyen.
4. Los documentos jurídicos reales quedan fuera de las pruebas; los datos y archivos usados son ficticios o generados en memoria.

## Decisiones confirmadas para la redacción

- Autor, ejecutor y responsable: Tamengo Sanchez Bustamante Calderon.
- Periodo del proyecto documentado: 1 de julio al 17 de noviembre de 2026.
- IDs documentales autorizados: RF-01 a RF-07 y RNF-01.
- BUG-01-F: Abierto, pendiente de corrección; responsable de seguimiento Tamengo Sanchez Bustamante Calderon.
