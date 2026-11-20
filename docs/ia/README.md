# Registros auditables de IA

Cada análisis crea una carpeta UUID con entrada, prompts, análisis, aclaraciones, borrador y revisión humana.
La clave de Anthropic nunca se persiste aquí. Los borradores no ejecutan pruebas ni cambian resultados.

Los selectores sólo pueden provenir de `config/dom_selectors.json`, generado por
`scripts/inspect_dom_stage8.py` contra el DOM local renderizado. Un selector no verificado bloquea el código.

Los resúmenes de corridas se guardan en `run-summaries/<run_id>` y conservan una copia inmutable del
estado y de las métricas emitidas por el motor de pruebas.
