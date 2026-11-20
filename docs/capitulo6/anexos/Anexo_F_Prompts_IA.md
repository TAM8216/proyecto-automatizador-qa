# Anexo F Prompts de Inteligencia Artificial

## Registro del Análisis

| Campo | Valor |
|---|---|
| Analysis ID | `feeaf1ec-4d07-4e3b-901e-89e582f58d20` |
| Fecha | 17/11/2026 16:57 UTC |
| Proveedor | groq |
| Modelo | `openai/gpt-oss-120b` |
| Estado | REQUIERE_ACLARACIONES |
| Revisión humana | Se mantuvo el bloqueo; no se generó borrador ni se registraron correcciones |

## Entrada

Como abogado ficticio quiero consultar el expediente QA-EXP-0001 por NUREJ para revisar su estado, usando únicamente datos sembrados en la base de pruebas.

## Prompt Utilizado

```text
Analiza el siguiente requisito. Detecta ambigüedades y datos faltantes antes de generar pruebas.
Devuelve exactamente: {"summary": str, "ambiguities": [str], "missing_data": [str],
"questions": [str], "ready_for_generation": bool}.

ENTRADA DEL USUARIO:
Como abogado ficticio quiero consultar el expediente QA-EXP-0001 por NUREJ para revisar su estado, usando únicamente datos sembrados en la base de pruebas.
```

## Resultado

- Resumen: El abogado ficticio necesita consultar el expediente QA-EXP-0001 mediante NUREJ para verificar su estado, limitándose a datos pre-cargados en la base de pruebas.
- Ambigüedades detectadas: 3.
- Datos faltantes: 6.
- Preguntas generadas: 6.
- Listo para generación: No.
- Uso total: 817 tokens.

### Preguntas Generadas

1. ¿Cuál es la URL completa o el path del endpoint para consultar expedientes por NUREJ?
2. ¿Qué método HTTP debe emplearse para la consulta?
3. ¿Cuál es el formato exacto del NUREJ (ejemplo de valor válido)?
4. ¿Qué mecanismo de autenticación se requiere (Bearer token, API key, etc.)?
5. ¿Qué campos debe incluir la respuesta (estado, fecha, etc.)?
6. ¿Cómo se identifica que los datos son los sembrados en la base de pruebas (marcador, entorno específico)?

La clave del proveedor no se incorporó a la entrada, al prompt ni a la evidencia. La IA no ejecutó pruebas ni modificó estados.
