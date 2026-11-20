# QA Platform para IPAS

Plataforma independiente de automatización para **IPAS – IUS PUNIENDI**. Esta
versión cubre las etapas 1 a 5: protección del ambiente QA, catálogo y runner,
automatización real, reportes ejecutivos, API y entrega por correo.

## Requisitos de la etapa 1

- Windows y PowerShell.
- Python 3.11 de 64 bits.
- PostgreSQL 17 con una base llamada exactamente `ius_puniendi_qa`.
- IPAS local: frontend `3000`, API `4000` y, cuando aplique, IA `8001`.
- Microsoft Edge o Google Chrome.

## Preparación

```powershell
cd C:\Users\tamri\OneDrive\Escritorio\IUS-PUNIENDI\qa-platform
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Completa `.env` localmente. Nunca lo adjuntes a evidencias ni lo subas al
repositorio. La plataforma aborta si `QA_DB_NAME` no es exactamente
`ius_puniendi_qa`.

## Flujo seguro

1. Crear `ius_puniendi_qa` vacía.
2. Restaurar **solo el esquema** compatible de IPAS en esa base.
3. Ejecutar el seed ficticio:

```powershell
python -m data.seed.seed_qa
```

4. Levantar IPAS apuntando exclusivamente a `ius_puniendi_qa`.
5. Ejecutar el preflight:

```powershell
python -m backend.runner.health
```

6. Ejecutar el primer caso real:

```powershell
pytest tests\functional\test_login_smoke.py -v -s
```

Las capturas se guardan bajo `evidencias/<run_id>/TC-LOG-001/`.

## Catálogo y runner — etapa 2

El catálogo `config/test_catalog.yaml` contiene 15 casos reales y suites para
smoke, autenticación, consulta pública, expedientes, documentos, roles, E2E,
regresión y FAIL controlado.

La interfaz organiza el catálogo en tres niveles: **tipo de prueba**, **flujo
funcional** y **suite**. Los flujos disponibles son acceso y sesión, gestión
jurídica, seguridad y permisos, flujo integral/regresión y rendimiento.

Ejecutar una suite:

```powershell
python -m backend.runner.run --suite regression
```

Ejecutar casos concretos:

```powershell
python -m backend.runner.run --case TC-LOG-002 --case TC-DOC-003
```

Ejecutar todo, incluido el defecto controlado:

```powershell
python -m backend.runner.run --all
```

Cada corrida genera `reports/<run_id>/result.json`, `junit.xml`, `pytest.html`
y `pytest.log`. Si falla el preflight, la corrida queda `FALLIDA` por
infraestructura y los casos quedan `NOT RUN`; nunca se convierten en falsos
FAIL funcionales.

La suite `regression` excluye deliberadamente `TC-ROL-001`. La suite
`controlled_fail` demuestra `BUG-01-F`: un abogado puede listar usuarios por
API y recibe HTTP 200 en lugar de 403.

## Reportes ejecutivos — etapa 3

Generar el DOCX detallado y el HTML autocontenido a partir de una corrida:

```powershell
python -m backend.reports.generator --result reports\<run_id>\result.json
```

También puede registrarse un correo de referencia sin enviar mensajes:

```powershell
python -m backend.reports.generator --result reports\<run_id>\result.json --email qa@ejemplo.test
```

Los archivos se guardan junto al `result.json` como
`informe_detallado.docx` y `reporte_autocontenido.html`. El HTML no requiere
servidor ni conexión: incorpora estilos y capturas en base64. El DOCX incluye
resumen, detalle por caso, pasos, datos ficticios y evidencias visuales.

## API del orquestador — etapa 4

Levantar la API local:

```powershell
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8080
```

La documentación interactiva queda en `http://127.0.0.1:8080/docs`. Endpoints:

- `GET /suites`: catálogo real de suites y casos.
- `POST /runs`: valida correo y selección; responde `202` con un `run_id`.
- `GET /runs/{run_id}`: devuelve `PENDIENTE`, `EN CURSO`, `FINALIZADA` o
  `FALLIDA`, además del resultado de cada caso.

Ejemplo para lanzar la suite smoke:

```powershell
$body = @{
  email = "qa@example.com"
  type = "funcional"
  suite = "smoke"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8080/runs `
  -ContentType application/json -Body $body
```

La ejecución usa un worker local y no bloquea la respuesta HTTP. El estado se
persiste desde el inicio en `reports/<run_id>/result.json`, por lo que puede
consultarse aunque la interfaz se recargue.

## Correo SMTP — etapa 5

Configura `SMTP_HOST`, `SMTP_PORT`, `SMTP_FROM` y, si el proveedor lo exige,
`SMTP_USER` y `SMTP_PASSWORD` en `.env`. Usa una contraseña de aplicación; no
guardes la clave real en el repositorio. `SMTP_USE_STARTTLS=true` es el valor
recomendado para el puerto 587.

`SMTP_USER` y `SMTP_PASSWORD` deben contener únicamente caracteres ASCII para
la autenticación SMTP estándar. Si contienen tildes, `ñ` u otros caracteres
Unicode, la plataforma bloquea el envío antes de conectarse y muestra una
explicación accionable. Después de modificar `.env`, reinicia la API.

Para `smtp.gmail.com`, `SMTP_PASSWORD` debe ser la contraseña de aplicación de
16 caracteres generada por Google con verificación en dos pasos; no corresponde
a la contraseña normal de la cuenta. La plataforma acepta que el código se
pegue con espacios y los elimina únicamente al autenticar.

Al terminar las pruebas, el worker genera primero `informe_detallado.docx` y
`reporte_autocontenido.html`. Solo cuando existen ambos construye el mensaje con
el asunto `Reporte de automatización – <Suite> – <fecha y hora>` y los adjunta.
El resultado de entrega queda en `email_delivery` dentro de `result.json`.

Si SMTP no está configurado o rechaza el mensaje, la corrida queda `FALLIDA`
con `failure_type=infraestructura`; los reportes no se eliminan y permanecen en
`reports/<run_id>/` para descarga o reenvío manual.

## Frontend React — etapa 6

Instalar y levantar la interfaz:

```powershell
cd frontend
npm install
npm run dev
```

Abre `http://127.0.0.1:5173` con la API activa en el puerto `8080`. La interfaz
carga el catálogo real, valida el correo, permite ejecutar una suite completa o
casos específicos, consulta el `run_id` cada 1.5 segundos y muestra resultados,
entrega SMTP y descargas de los dos reportes. Para usar otra API define
`VITE_API_URL` antes de iniciar Vite.

## Rendimiento con Locust — etapa 7

La suite `carga_local` ejecuta autenticación y consultas de expedientes y
documentos ficticios sobre `SUT_API_URL`. No invoca búsqueda semántica,
embeddings, LLM ni servicios externos. Perfil predeterminado:

- 5 usuarios concurrentes.
- Incremento de 1 usuario por segundo.
- 30 segundos de duración.
- Criterio: p95 menor a 2000 ms y errores menores a 1%.

Desde la interfaz selecciona **No funcionales** para ajustar estos tres
parámetros dentro de límites seguros. Desde consola:

```powershell
python -m locust -f tests\non_functional\locustfile.py --headless `
  --host http://127.0.0.1:4000/api --users 5 --spawn-rate 1 --run-time 30s
```

La ejecución por API guarda CSV y log de Locust, incorpora solicitudes,
throughput, promedio, mediana, p95, mínimo, máximo y tasa de errores en
`result.json`, DOCX y HTML.

## Asistente IA con revisión humana — etapa 8

Configura `AI_PROVIDER=groq` y `GROQ_API_KEY` únicamente en `.env`. El modelo
predeterminado es el mismo configurado en IPAS (`openai/gpt-oss-120b`). También
se conserva `AI_PROVIDER=anthropic` como alternativa compatible con el alcance
inicial. Sin la clave del proveedor elegido, los endpoints responden `503` y no
simulan una respuesta real.

Flujo disponible en la pestaña **Asistente IA**:

1. `POST /ai/analyses` detecta ambigüedades, datos faltantes y preguntas.
2. `POST /ai/drafts` genera Gherkin en español, propuesta de pasos, Page Object
   y pytest sólo después de recibir la información necesaria.
3. `POST /ai/analyses/{analysis_id}/review` registra aprobación o correcciones;
   nunca inicia una corrida automáticamente.
4. `POST /ai/runs/{run_id}/summary` explica fallos observados sin modificar el
   estado ni las métricas emitidas por pytest/Locust.

La interfaz presenta el Gherkin completo en un bloque copiable con
`Característica`, `Escenario` y pasos `Dado/Cuando/Entonces/Y`. El backend
normaliza esos encabezados y elimina cercos Markdown del código Python antes de
validarlo.

Cada interacción se audita bajo `docs/ia/<analysis_id>/`. Los locators están
limitados al registro `config/dom_selectors.json`, verificado contra el DOM
renderizado mediante:

```powershell
python scripts\inspect_dom_stage8.py --env-file .env `
  --driver .drivers\msedgedriver.exe --output config\dom_selectors.json
```

Si la IA propone un selector ausente del registro, el borrador queda
`REQUIERE_CONFIRMACION_SELECTOR`, se suprime el código inseguro y se bloquea la
aprobación hasta realizar una nueva inspección real del DOM.

## Decisiones defendibles

- El orquestador está separado del SUT para evitar acoplamiento y cambios
  accidentales en IPAS.
- El nombre de base se valida dos veces: al cargar configuración y justo antes
  del seed.
- El health-check considera `401` en `/api/auth/verify` como API disponible:
  ese endpoint requiere token y el backend aún no ofrece un health-check global.
- Los selectores del primer POM derivan de etiquetas y botones observados en el
  DOM React de IPAS; el registro de etapa 8 confirma siete locators con Selenium
  y no depende de clases CSS generadas por MUI.
- Las evidencias usan datos sintéticos y nunca leen documentos existentes del
  repositorio del SUT.

