# Requisitos documentales cubiertos por las pruebas

Los siguientes identificadores se asignaron para la documentación del proyecto a partir de funcionalidades verificadas en el código y en las ejecuciones reales de IPAS. No representan requisitos nuevos ni amplían el alcance del sistema.

| ID | Tipo | Descripción verificable | Casos relacionados |
|---|---|---|---|
| RF-01 | Funcional | El sistema debe autenticar a usuarios internos mediante correo y contraseña y rechazar credenciales o campos obligatorios inválidos. | TC-LOG-001, TC-LOG-002, TC-LOG-003 |
| RF-02 | Funcional | El sistema debe verificar un token de sesión válido y devolver la identidad y el rol asociados. | TC-LOG-004 |
| RF-03 | Funcional | El sistema debe permitir el seguimiento público de un expediente únicamente cuando coincidan el NUREJ o CUD y el CI relacionado. | TC-PUB-001, TC-PUB-002 |
| RF-04 | Funcional | El sistema debe permitir crear y consultar expedientes jurídicos, validando sus campos obligatorios y la inexistencia de identificadores consultados. | TC-EXP-001, TC-EXP-002, TC-EXP-003 |
| RF-05 | Funcional | El sistema debe permitir cargar documentos de formatos autorizados y rechazar extensiones no permitidas o archivos superiores a 10 MB. | TC-DOC-001, TC-DOC-002, TC-DOC-003 |
| RF-06 | Funcional de seguridad | El sistema debe restringir las operaciones administrativas según el rol autenticado. | TC-ROL-001 |
| RF-07 | Funcional E2E | Un abogado autenticado debe poder acceder a Gestión de Casos y visualizar el expediente ficticio asignado en el ambiente QA. | TC-E2E-001 |
| RNF-01 | No funcional | La API local debe mantener un p95 menor a 2.000 ms y una tasa de errores menor a 1 % bajo el perfil propuesto de cinco usuarios, incremento de un usuario por segundo y 30 segundos. | TC-PERF-001 |

El caso TC-SMK-001 verifica condiciones de disponibilidad del ambiente y se utiliza como criterio técnico de entrada, no como requisito funcional del SUT.
