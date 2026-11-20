# Checklist Final del Capítulo 6

**Proyecto:** IPAS IUS PUNIENDI  
**Responsable de la revisión:** Tamengo Sanchez Bustamante Calderon  
**Fecha:** 17 de noviembre de 2026

La versión v2 de la guía contiene 22 casillas visibles bajo “Checklist antes de entregar”, aunque la instrucción inicial menciona 21 puntos. Para evitar omisiones se verificaron las 22 casillas oficiales.

| Nro. | Verificación oficial | Estado | Evidencia concreta |
|---:|---|---|---|
| 1 | El Plan de Pruebas explica el alcance, estrategia y condiciones de trabajo | Cumple | Sección 6.1.3 a 6.1.13 |
| 2 | Las funcionalidades y requisitos están identificados | Cumple | Secciones 6.2.1 y 6.2.2; `requisitos_documentales.md` |
| 3 | Los casos de prueba están completos y pueden ser reproducidos | Cumple | Anexo A y 16 archivos en `docs/tc/` |
| 4 | Los datos de prueba están definidos | Cumple | Secciones 6.1.10, 6.2.6 y datos de cada TC del Anexo A |
| 5 | Las ejecuciones tienen estado, resultado y evidencia | Cumple | Sección 6.5.2 y 16 fichas del Anexo B |
| 6 | Los defectos están documentados y relacionados con los casos | Cumple | BUG-01-F relacionado con TC-ROL-001 en 6.5.3 y Anexo C |
| 7 | Retesting y Regression están correctamente diferenciados | Cumple | Secciones 6.5.4 y 6.5.5 |
| 8 | La automatización explica qué se automatizó y por qué | Cumple | Secciones 6.3.1 y 6.3.2 |
| 9 | Se identifica la herramienta o framework principal y se justifica su elección | Cumple | Sección 6.3.3, pytest como motor principal |
| 10 | Se explica la arquitectura y el flujo de ejecución de la solución | Cumple | Sección 6.3.4 y Figura 1 |
| 11 | Los scripts están relacionados con casos identificados | Cumple | Sección 6.3.8, relación de los 15 TC funcionales con sus scripts |
| 12 | Se documentan comandos e instrucciones para reproducir la ejecución | Cumple | Sección 6.3.10 y `README.md` |
| 13 | Las evidencias corresponden a ejecuciones reales | Cumple | Secciones 6.3.11, 6.4.7, 6.5.7 y Anexo D |
| 14 | Se diferencia lo implementado de lo propuesto como trabajo futuro | Cumple | Secciones 6.3.14, 6.3.15 y 6.8 |
| 15 | Si se utilizó IA, se documentan herramienta, entrada, prompt, resultado y revisión humana | Cumple | Sección 6.3.16 y Anexo F |
| 16 | No se exponen credenciales, tokens ni datos sensibles | Cumple | Secciones 6.1.10, 6.3.9 y 6.3.17; anexos sin secretos |
| 17 | La estructura y ejecución de la automatización están documentadas | Cumple | Secciones 6.3.4, 6.3.5 y 6.3.10 |
| 18 | La cobertura de automatización tiene una base clara | Cumple | Sección 6.3.12: 15/15 funcional y sección 6.6.4: 16/16 global |
| 19 | Los resultados corresponden a ejecuciones reales | Cumple | Secciones 6.3.13, 6.4.5 y 6.6; `result.json` citados por run ID |
| 20 | Las conclusiones se basan en los resultados | Cumple | Sección 6.7, derivada de 15 PASS, 1 FAIL y métricas Locust |
| 21 | Las recomendaciones son concretas | Cumple | Sección 6.8, acciones priorizadas y criterios de verificación |
| 22 | Los apartados que no aplican están justificados | Cumple | Manual, retesting, CI/CD, estrés, soak, CPU y memoria declarados como no realizados |

## Resultado de la Revisión

- **Puntos verificados:** 22.
- **Puntos que cumplen:** 22.
- **Puntos que no cumplen:** 0.
- **Marcadores pendientes en el Capítulo 6 y anexos:** 0.

El cumplimiento del checklist indica que la documentación contiene los elementos solicitados. No modifica el estado abierto de BUG-01-F ni convierte en realizadas las actividades registradas como trabajo futuro.
