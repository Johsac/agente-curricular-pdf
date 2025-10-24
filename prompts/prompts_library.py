# prompts/prompts_library.py

# PROMPTS_AGENTE_1 = {
#     "I. IDENTIFICACIÓN": "Del documento, extrae el contenido completo de la sección 'I. IDENTIFICACIÓN'. Asegúrate de que la parte de 'Requisito para cursar', 'Requisitos previos' y 'Co - Requisitos' se presenten en líneas separadas y únicas, así: 'Requisito para cursar: No tiene'.",
#     "II. CARGA ACADÉMICA": """Tu rol es ser un asistente de extracción de datos. A partir del texto proporcionado, localiza la sección "II. CARGA ACADÉMICA". Tu única tarea es encontrar los valores numéricos para las siguientes categorías y devolverlos en una lista.

# Las SCT (horas cronológicas) se dividen en dos: Directas o Personal.
# Para el "Tipo de Actividad", haya el valor numérico de:
# Presenta el resultado colocando como titulo "Tipo de Actividad - SCT (horas cronológicas)":
# - Teórico - Directas: [valor]
# - Teórico - Personal: [valor]
# - Ayudantía - Directas: [valor]
# - Ayudantía - Personal: [valor]
# - Laboratorio - Directas: [valor]
# - Laboratorio - Personal: [valor]
# - Taller - Directas: [valor]
# - Taller - Personal: [valor]
# - Terreno - Directas: [valor]
# - Terreno - Personal: [valor]
# - Clínico - Directas: [valor]
# - Clínico - Personal: [valor]
# ----
# Para las últimas dos categorías de "Tipo de Actividad", se coloca un valor único de SCT.
# - Total horas dedicación semanal: [valor]
# - Créditos SCT: [valor]

# **Instrucciones importantes:**
# 1. Si una celda está vacía o no tiene un número, déjalo con un espacio vacío: ` `.
# 2. No incluyas ningún texto introductorio o conclusión.""",
#     "III. DESCRIPCIÓN": "Del documento, extrae únicamente las frases que comiencen con 'RA1:', 'RA2:', 'RA3:', etc., bajo la sección 'III. DESCRIPCIÓN'. Si no encuentras ninguna, extrae el primer párrafo de la sección.",
#     "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS": "Realiza la siguiente tarea compleja: 1. Busca en todo el documento los títulos de 'UNIDAD' (ej. 'UNIDAD I: ...') y el texto de sus correspondientes 'Aprendizaje Esperado' (AE). 2. El contenido de cada UNIDAD (usualmente una lista de puntos) puede estar en una página diferente a su título. Debes encontrarlo. 3. Formatea la salida para cada par así, asegurándote de incluir el contenido completo de la unidad:\nUNIDAD I: [Título y todo el contenido en lista de la UNIDAD I]\n\nAE1: [Texto completo de AE1]\n\n---",
#     "VI. HABILIDADES TRANSVERSALES": "Extrae el texto completo y sin modificar de 'VI. HABILIDADES TRANSVERSALES'.",
#     "VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN": "Extrae el texto completo y sin modificar de 'VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN'.",
#     "VIII. CONDICIONES DE APROBACIÓN": "Extrae el texto completo y sin modificar de 'VIII. CONDICIONES DE APROBACIÓN'.",
#     "IX. BIBLIOGRAFÍA": "Extrae el texto completo y sin modificar de 'IX. BIBLIOGRAFÍA', donde esta sección está dividida generalmente en subsecciones como 'Obligatoria' y 'Complementaria'.",
# #     "X. CORRESPONDENCIA CRÉDITOS UNAB": """Del texto de la sección 'X. CORRESPONDENCIA CRÉDITOS UNAB', extrae dos cosas:
# # 1. Una lista de todos los números que aparecen en la tabla, en el orden exacto en que aparecen.
# # 2. El texto completo del párrafo que comienza con "Nota importante:".
# # 3. Antes de mostrar la lista de todos los números, COMIENZA CON UN ENCABEZADO que diga: 'Horas pedagógicas:'.

# # Formatea tu respuesta exactamente así:
# # NUMEROS: [lista de números separados por comas]
# # TEXTO: [texto de la nota]"""
#     "X. CORRESPONDENCIA CRÉDITOS UNAB": """A partir del texto crudo de la sección 'X. CORRESPONDENCIA CRÉDITOS UNAB', interpreta la tabla y la 'Nota importante'. Usa la pista de que la actividad presencial activa es '{pista_actividad_activa}'.
# Formato de Salida Requerido:
# - Presencial - Teórico: [valor]
# - Presencial - Ayudantía: [valor]
# - Presencial - Laboratorio: [valor]
# - Presencial - Taller: [valor]
# - Presencial - Terreno: [valor]
# - Presencial - Clínico: [valor]
# - Personal: [valor]
# - Créditos UNAB: [valor]
# -----
# Texto adicional:
# [texto de la nota importante]"""
# }


PROMPTS_AGENTE_1 = {
    "I. IDENTIFICACIÓN": "Del documento, extrae el contenido completo de la sección 'I. IDENTIFICACIÓN'. Asegúrate de que la parte de 'Requisito para cursar', 'Requisitos previos' y 'Co - Requisitos' se presenten en líneas separadas y únicas, así: 'Requisito para cursar: No tiene'.",
    
    # --- PROMPT MEJORADO ---
    # Ahora le pedimos al LLM que identifique las categorías activas y las liste
    # en un formato fácil de parsear al final de su respuesta.
    "II. CARGA ACADÉMICA": """Tu rol es ser un asistente experto en extracción de datos. A partir del texto proporcionado, localiza la sección "II. CARGA ACADÉMICA".
Tu tarea tiene dos partes:

1.  Encuentra los valores numéricos para las siguientes categorías y preséntalos como una lista. Si una celda está vacía o no tiene un número, déjalo con un espacio vacío: ` `.
    - Teórico - Directas: [valor]
    - Teórico - Personal: [valor]
    - Ayudantía - Directas: [valor]
    - Ayudantía - Personal: [valor]
    - Laboratorio - Directas: [valor]
    - Laboratorio - Personal: [valor]
    - Taller - Directas: [valor]
    - Taller - Personal: [valor]
    - Terreno - Directas: [valor]
    - Terreno - Personal: [valor]
    - Clínico - Directas: [valor]
    - Clínico - Personal: [valor]
    ----
    - Total horas dedicación semanal: [valor]
    - Créditos SCT: [valor]

2.  Después de la lista, identifica todas las categorías de actividad presencial (Teórico, Ayudantía, Laboratorio, Taller, Terreno, Clínico) que tengan un valor numérico mayor que cero en la columna "Directas". Agrega al final una línea con el siguiente formato EXACTO:
    ACTIVIDADES_ACTIVAS: [Categoría1, Categoría2, Categoría3]

**Ejemplo de salida final:**
- Teórico - Directas: 3
- Teórico - Personal: 2
- Ayudantía - Directas:
- Ayudantía - Personal:
- Laboratorio - Directas: 2
- Laboratorio - Personal: 1
...
----
- Total horas dedicación semanal: 8
- Créditos SCT: 4
ACTIVIDADES_ACTIVAS: [Teórico, Laboratorio]
""",
    "III. DESCRIPCIÓN": "Del documento, extrae únicamente las frases que comiencen con 'RA1:', 'RA2:', 'RA3:', etc., bajo la sección 'III. DESCRIPCIÓN'. Si no encuentras ninguna, extrae el primer párrafo de la sección.",
    "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS": "Realiza la siguiente tarea compleja: 1. Busca en todo el documento los títulos de 'UNIDAD' (ej. 'UNIDAD I: ...') y el texto de sus correspondientes 'Aprendizaje Esperado' (AE). 2. El contenido de cada UNIDAD (usualmente una lista de puntos) puede estar en una página diferente a su título. Debes encontrarlo. 3. Formatea la salida para cada par así, asegurándote de incluir el contenido completo de la unidad:\nUNIDAD I: [Título y todo el contenido en lista de la UNIDAD I]\n\nAE1: [Texto completo de AE1]\n\n---",
    "VI. HABILIDADES TRANSVERSALES": "Extrae el texto completo y sin modificar de 'VI. HABILIDADES TRANSVERSALES'.",
    "VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN": "Extrae el texto completo y sin modificar de 'VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN'.",
    "VIII. CONDICIONES DE APROBACIÓN": "Extrae el texto completo y sin modificar de 'VIII. CONDICIONES DE APROBACIÓN'.",
    "IX. BIBLIOGRAFÍA": "Extrae el texto completo y sin modificar de 'IX. BIBLIOGRAFÍA', donde esta sección está dividida generalmente en subsecciones como 'Obligatoria' y 'Complementaria'.",
    "X. CORRESPONDENCIA CRÉDITOS UNAB": """A partir del texto crudo proporcionado de la sección 'X. CORRESPONDENCIA CRÉDITOS UNAB', interpreta la tabla y la 'Nota importante'.
Usa la siguiente pista crucial para asignar correctamente los números: Las actividades presenciales activas para este curso son **{pista_actividad_activa}**.

Tu tarea es rellenar la siguiente estructura con los valores numéricos correspondientes.

Formato de Salida Requerido:
- Presencial - Teórico: [valor]
- Presencial - Ayudantía: [valor]
- Presencial - Laboratorio: [valor]
- Presencial - Taller: [valor]
- Presencial - Terreno: [valor]
- Presencial - Clínico: [valor]
- Personal: [valor]
- Créditos UNAB: [valor]
-----
Texto adicional:
[texto de la nota importante]
"""
}

# PROMPT_AGENTE_2_TEMPLATE = """
# Tu tarea es actuar como un planificador curricular experto. Debes rellenar la "PLANTILLA A RELLENAR" basándote en el "CONTEXTO" que contiene el texto extraído de un programa de asignatura.

# **REGLAS ESTRICTAS:**
# 1.  Para cada campo, busca la información correspondiente en el CONTEXTO y transcríbela.
# 2.  Si un campo en la plantilla tiene la instrucción "[PENDIENTE - AGENTE 3]", DEBES escribir textualmente "PENDIENTE - AGENTE 3".
# 3.  Si no encuentras información para un campo de extracción, déjalo en blanco.
# 4.  No incluyas corchetes `[]` en tus respuestas. Tu respuesta debe ser únicamente la plantilla rellenada.

# **CONTEXTO:**
# {contenido_observaciones_txt}

# ---
# **PLANTILLA A RELLENAR:**

# # MATRIZ DE PLANIFICACIÓN CURRICULAR UNIFICADA

# 1. Identificación general del curso
# - Nombre del curso/asignatura: [Busca en "I. IDENTIFICACIÓN"]
# - Código: [Busca en "I. IDENTIFICACIÓN"]
# - Programa/Plan de estudios: [Busca en "I. IDENTIFICACIÓN"]
# - Modalidad: [Busca en el documento, si no encuentras, déjalo en blanco]
# - Nivel académico: [Busca en "I. IDENTIFICACIÓN"]
# - Duración: [Busca en "I. IDENTIFICACIÓN"]
# - Créditos SCT: [Busca en "II. CARGA ACADÉMICA"]
# - Docente/ Diseñador instruccional(s) del curso:
# - Fecha de elaboración:

# 2. Objetivos formativos
# - Resultado de aprendizaje del curso: [Extrae y lista todos los "RA" de la sección "III. DESCRIPCIÓN". Si no hay coloca "PENDIENTE - AGENTE 3"]
# - Resultado de aprendizaje de la unidad: [Extrae y lista todos los "AE" de la sección "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS". Si no hay coloca "PENDIENTE - AGENTE 3"]


# 3. Estructura por unidad
# - Unidad: [De la sección "IV", extrae y lista todos los títulos de las Unidades. IMPORTANTE: Cada unidad debe estar en una línea nueva y empezar con un guion (-).  Si no hay coloca "PENDIENTE - AGENTE 3"]
# - Indicadores de Evaluación(IE): [Extrae y lista todos los "AE" de la sección "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS". IMPORTANTE: Cada unidad debe estar en una línea nueva y empezar con un guion (-). Si no hay coloca "PENDIENTE - AGENTE 3"]
# - Contenidos de la Unidad: [De la sección "IV", extrae y lista los contenidos de cada unidad]
# - Actividades didácticas y experiencias de aprendizaje: [PENDIENTE - AGENTE 3]
# - Actividades evaluativas (formativas y/o sumativas): [PENDIENTE - AGENTE 3]
# - Recursos y materiales: [PENDIENTE - AGENTE 3]


# 4. Evaluación
# - Tipo de evaluación: [Busca en las secciones VII y VIII. Si no encuentras, deja en blanco]
# - Instrumento: [Busca en la sección VII y lista las herramientas. Si no encuentras, deja en blanco]
# - Indicadores asociados:
# - Ponderación (%): [Busca en la sección VIII cualquier peso porcentual explícito]
# """

# PROMPTS_AGENTE_3 = {
#     "Resultado de aprendizaje del curso": "Redacta un único resultado de aprendizaje global para la asignatura '{nombre_asignatura}'. Debe ser claro, medible y describir lo que el estudiante será capaz de hacer al finalizar. Usa verbos de acción de Bloom. Sé directo y presenta solo el texto del resultado.",
#     "Resultado de aprendizaje de la unidad": "Para la asignatura '{nombre_asignatura}' y la unidad '{nombre_unidad}', cuyo aprendizaje esperado original es '{aprendizaje_esperado}', reformúlalo en una sola frase concisa que comience con 'Al finalizar la unidad, el estudiante será capaz de...'. Tu respuesta debe ser solo esa frase.",
#     "Indicadores de Evaluación(IE)": "Redacta {n_indicadores} indicadores de logro para la unidad '{nombre_unidad}', coherentes con el aprendizaje esperado: '{aprendizaje_esperado}'. Cada indicador debe seguir la estructura: [Verbo de acción] + [Contenido] + [Contexto]. La respuesta debe ser únicamente una lista numerada.",
#     "Actividades didácticas y experiencias de aprendizaje": "Diseña una experiencia de aprendizaje breve para la unidad '{nombre_unidad}' que tribute a los indicadores: {indicadores_logro}. Describe una actividad para cada fase de la secuencia didáctica (Inicio, Desarrollo, Cierre). Sé conciso y práctico. No uses introducciones.",
#     "Actividades evaluativas (formativas y/o sumativas)": "Propón una actividad formativa y una sumativa para la unidad '{nombre_unidad}', alineadas con los indicadores: {indicadores_logro}. Describe cada actividad brevemente. Tu respuesta debe ser directa, sin preámbulos, en formato de lista.",
#     "Recursos y materiales": "Sugiere una lista de recursos y materiales (bibliográficos, digitales, etc.) para la unidad '{nombre_unidad}', que apoyen los indicadores: {indicadores_logro}. Sé específico y conciso. La respuesta debe ser solo la lista.",
#     "Tipo de evaluación": "Determina y nombra el tipo de evaluación principal (Formativa, Sumativa o Mixta) para la unidad {nombre_unidad}, justificando brevemente tu elección. Sé directo.",
#     "Instrumento": "Propón un instrumento de evaluación concreto (ej. rúbrica simple, lista de cotejo) para la actividad sumativa de la unidad {nombre_unidad}. Sé directo y presenta solo el instrumento.",
#     "Ponderación (%)": "Redacta una propuesta de ponderación para las actividades sumativas de la unidad, considerando los indicadores: {indicadores_logro}. Sé directo y presenta solo la propuesta."
# }

PROMPT_AGENTE_2_TEMPLATE = """
Tu tarea es actuar como un planificador curricular experto. Debes rellenar la "PLANTILLA A RELLENAR" basándote en dos fuentes de información: el "SOPORTE TEÓRICO" que define cada categoría y el "CONTEXTO" que contiene el texto extraído de un programa de asignatura.

---
# SOPORTE TEÓRICO PARA LA EXTRACCIÓN

**Resultado de aprendizaje del curso:** Es una declaración clara, específica y medible que describe lo que un estudiante será capaz de conocer, comprender, aplicar o demostrar al finalizar un curso. Se centra en el estudiante, es observable y se formula con verbos de acción.

**Resultado de aprendizaje de la unidad:** Es una declaración específica y observable que expresa lo que el estudiante debe demostrar al finalizar una unidad. Se deriva del resultado de aprendizaje del curso y representa una meta intermedia.

**Unidad:** Es un segmento estructurado de contenido en torno a un tema, problema o competencia. Constituye un bloque de enseñanza-aprendizaje.

**Indicadores de Evaluación (IE):** Es un descriptor observable y medible que permite verificar el grado en que un estudiante ha alcanzado un resultado de aprendizaje. Se expresa en conductas o productos observables.

**Contenidos de la Unidad:** Es el conjunto de saberes (conceptos, procedimientos) seleccionados para que el estudiante alcance los Resultados de Aprendizaje de la Unidad.

**Actividades didácticas y experiencias de aprendizaje:** Son las estrategias planificadas por el docente que sitúan al estudiante en un proceso activo para alcanzar los Resultados de Aprendizaje.

**Actividades evaluativas (formativas y/o sumativas):** Son las tareas diseñadas para que el estudiante demuestre el logro de los Resultados de Aprendizaje. La formativa retroalimenta el proceso; la sumativa certifica el resultado.

**Recursos y materiales:** Son todos los apoyos didácticos, tecnológicos y bibliográficos que se ponen a disposición del estudiante.

**Tipo de evaluación:** Se refiere a la función y momento de la evaluación (Formativa: durante el proceso para retroalimentar; Sumativa: al cierre para certificar el logro; También puedes usar diagnóstica, al inicio, para conocer saberes previos).

**Instrumento:** Es la herramienta concreta con la que se recoge evidencia del aprendizaje (ej. Prueba objetiva (múltiple opción, V/F, matching), Ensayo con rúbrica, Estudio de caso, Proyecto, Presentación oral, etc.).

**Ponderación (%):** Es el peso porcentual de cada actividad evaluativa en la calificación final (ej. 70% la nota de presentación y 30% la nota de examen).
---

**REGLAS ESTRICTAS:**
1.  Para cada campo que sigue a los dos puntos (:), busca la información correspondiente en el CONTEXTO y transcríbela.
2.  Si un campo en la plantilla tiene la instrucción "[PENDIENTE - AGENTE 3]", DEBES escribir textualmente "PENDIENTE - AGENTE 3" y NO intentar rellenarlo.
3.  Si no encuentras información para un campo de extracción, déjalo en blanco.
4.  No incluyas corchetes `[]` en tus respuestas.
5.  No incluyas ningún texto introductorio ni conclusión. Tu respuesta debe ser únicamente la plantilla rellenada.


**CONTEXTO:**
{contenido_observaciones_txt}

---
**PLANTILLA A RELLENAR:**

# MATRIZ DE PLANIFICACIÓN CURRICULAR UNIFICADA

1. Identificación general del curso
- Nombre del curso/asignatura: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Nombre"]
- Código: [Busca en "I. IDENTIFICACIÓN" el campo "Código"]
- Programa/Plan de estudios: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Carrera"]
- Modalidad: [Busca en la sección "I" o "VIII" o "X" el campo "Modalidad" o similar, si la modalidad es alguna de estas 3 opciones: Online o Presencial o Semipresencial. Si no lo encuentras, coloca "Online"]
- Nivel académico: [Busca en "I. IDENTIFICACIÓN" el campo "Periodo" o "Semestre"]
- Duración: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Régimen" o "Periodo", por ej. "trimestre", "semestral" o "anual"]
- Créditos SCT: [Busca en la sección "II. CARGA ACADÉMICA" el campo "Créditos SCT"]
- Docente/ Diseñador instruccional(s) del curso: 
- Fecha de elaboración: 

2. Objetivos formativos
## Resultado de aprendizaje del curso 
- [Extrae y lista todos los "Resultados de Aprendizaje (RA)" de la sección "III. DESCRIPCIÓN". Presentalo en una lista en viñetas ("RA1: ...", "RA2: ...",...)]
## Resultado de aprendizaje de la unidad 
- [Extrae y lista todos los "Aprendizajes Esperados (AE)" de la sección "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS". Presentalo en una lista en viñetas ("AE1: ...", "AE2: ...",...)]



3. Estructura por unidad
## Unidad
- [De la sección "IV", extrae y lista todos los títulos de las Unidades (ej. "UNIDAD I: FUNDAMENTOS...", "UNIDAD II: ...") deben ser colocado en una lista de viñetas. IMPORTANTE: Cada unidad debe estar en una línea nueva y empezar con un guion (-)]

## Indicadores de Evaluación (IE)
- [PENDIENTE - AGENTE 3]

## Contenidos de la Unidad
- [De la sección "IV", extrae y lista los contenidos asociados a cada una de las unidades que encontraste separados por su UNIDAD y su contenido.]

## Actividades didácticas y experiencias de aprendizaje
- [PENDIENTE - AGENTE 3]

## Actividades evaluativas (formativas y/o sumativas)
- [PENDIENTE - AGENTE 3]

## Recursos y materiales
- [PENDIENTE - AGENTE 3]


4. Evaluación
## Tipo de evaluación
- [Basándote en la definición del SOPORTE TEÓRICO, busca en las secciones VII y VIII. Se elige entre las opciones: "Formativa", "Sumativa", "Diagnóstica", podria ser seleccionada mas de una opcion caso sea necesario. Has una breve explicacion del porque esa opcion.  Caso no haya en el texto coloca [PENDIENTE - AGENTE 3]]

## Instrumento
- [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VII y extrae una lista con todas las posibles herramientas (por ej.: múltiple opción, V/F, matching, Ensayo con rúbrica, Estudio de caso, Proyecto, Presentación oral).  Caso no haya en el texto coloca [PENDIENTE - AGENTE 3]]

## Indicadores asociados
- [Este indicador se deja en blanco]

## Ponderación (%)
- [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VIII y extrae textualmente cualquier peso porcentual explícito con su respectivo campo (ej. '70% la nota de presentación', '30% la nota de examen').]

"""
# 2. Objetivos formativos
# - Resultado de aprendizaje del curso: [Extrae y lista todos los "Resultados de Aprendizaje (RA)" de la sección "III. DESCRIPCIÓN". Presentalo en una lista en viñetas ("RA1: ...", "RA2: ...",...)]
# - Resultado de aprendizaje de la unidad: [Extrae y lista todos los "Aprendizajes Esperados (AE)" de la sección "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS". Presentalo en una lista en viñetas ("AE1: ...", "AE2: ...",...)]



# 3. Estructura por unidad
# - Unidad: [De la sección "IV", extrae y lista todos los títulos de las Unidades (ej. "UNIDAD I: FUNDAMENTOS...", "UNIDAD II: ...") deben ser colocado en una lista de viñetas.]
# - Indicadores de Evaluación(IE): [PENDIENTE - AGENTE 3]
# - Contenidos de la Unidad: [De la sección "IV", extrae y lista los contenidos asociados a cada una de las unidades que encontraste.]
# - Actividades didácticas y experiencias de aprendizaje: [PENDIENTE - AGENTE 3]
# - Actividades evaluativas (formativas y/o sumativas): [PENDIENTE - AGENTE 3]
# - Recursos y materiales: [PENDIENTE - AGENTE 3]


# 4. Evaluación
# - Tipo de evaluación: [Basándote en la definición del SOPORTE TEÓRICO, busca en las secciones VII y VIII. Se elige entre las opciones: "Formativa", "Sumativa", "Diagnóstica", podria ser seleccionada mas de una opcion caso sea necesario. Has una breve explicacion del porque esa opcion.  Caso no haya en el texto coloca [PENDIENTE - AGENTE 3]]
# - Instrumento: [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VII y extrae una lista con todas las posibles herramientas (por ej.: múltiple opción, V/F, matching, Ensayo con rúbrica, Estudio de caso, Proyecto, Presentación oral).  Caso no haya en el texto coloca [PENDIENTE - AGENTE 3]]
# - Indicadores asociados: [Este indicador se deja en blanco]
# - Ponderación (%): [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VIII y extrae textualmente cualquier peso porcentual explícito con su respectivo campo (ej. '70% la nota de presentación', '30% la nota de examen').]


PROMPTS_AGENTE_3 = {
    "Resultado de aprendizaje del curso": "Actúa como un experto metodológico y redacta un resultado de aprendizaje claro, medible y coherente para la asignatura {nombre_asignatura}. El resultado debe describir lo que el estudiante será capaz de hacer al finalizar el curso, utilizando verbos de acción de la Taxonomía de Bloom (versión revisada). Incluye un solo resultado, expresado en tiempo futuro, que combine conocimiento, habilidades y actitudes relevantes para la asignatura. Evita formulaciones vagas y asegúrate de que sea observable y evaluable. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc).",
    "Resultado de aprendizaje de la unidad": """Actúa como un experto metodológico. Para la asignatura {nombre_asignatura} y la unidad '{nombre_unidad}', cuyo aprendizaje esperado es '{aprendizaje_esperado}', reformula este aprendizaje esperado en una sola frase que comience con 'Al finalizar la unidad, el estudiante será capaz de...'. La respuesta debe ser directa y concisa. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc).""",
    "Indicadores de Evaluación(IE)": """
    Si este campo ya fue respondido no es necesario que generes nada. Caso contrario actúa como un docente experto metodológico para la asignatura {nombre_asignatura}.
    SOPORTE TEÓRICO: Un indicador de evaluación debe tener la estructura: [Verbo de acción evaluable de Bloom] + [Objeto de conocimiento o contenido] + [Condición o contexto de aplicación].
    
    Basado en este soporte, redacta {n_indicadores} indicadores de logro para la unidad '{nombre_unidad}' que sean coherentes con el siguiente aprendizaje esperado: '{aprendizaje_esperado}'.
    
    Asegúrate de seguir la estructura indicada. La respuesta debe ser una lista numerada. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). Sé directo y no excedas las 200 palabras.""",

    "Actividades didácticas y experiencias de aprendizaje": """
    Si este campo ya fue respondido no es necesario que generes nada. Caso contrario actúa como un docente experto para la asignatura {nombre_asignatura}.
    SOPORTE TEÓRICO: Una experiencia de aprendizaje sigue la secuencia didáctica: Activación de conocimientos previos -> Aplicación guiada / Integración -> Evaluación formativa + Retroalimentación -> Cierre reflexivo / Metacognición.

    Basado en este soporte, diseña una experiencia de aprendizaje para la unidad '{nombre_unidad}' que tribute a los siguientes indicadores de logro: {indicadores_logro}.
    
    Describe brevemente una actividad para cada fase de la secuencia. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). La respuesta debe ser concisa y no exceder las 200 palabras.""",

    "Actividades evaluativas (formativas y/o sumativas)": """
    Actúa como un experto en evaluación para la asignatura {nombre_asignatura}.
    SOPORTE TEÓRICO: Las actividades evaluativas deben estar alineadas con los indicadores de evaluación. La evaluación formativa retroalimenta el proceso; la sumativa certifica el logro.

    Basado en este soporte, propón al menos una actividad formativa y una actividad sumativa para la unidad '{nombre_unidad}', asegurándote de que midan los verbos de desempeño de los siguientes indicadores de logro: {indicadores_logro}.
    
    Describe brevemente cada actividad. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). La respuesta debe ser una lista y no exceder las 200 palabras.""",

    "Recursos y materiales": """
    Actúa como un docente experto para la asignatura {nombre_asignatura}.
    SOPORTE TEÓRICO: Los recursos pueden ser Bibliográficos (textos, artículos), Digitales (plataformas, simuladores), Audiovisuales (videos, podcasts) o Instrumentales (guías, software).

    Basado en este soporte, sugiere una lista de recursos y materiales pertinentes para la unidad '{nombre_unidad}', que apoyen los siguientes indicadores de logro: {indicadores_logro}.
    
    Incluye al menos un ejemplo de cada tipo de recurso. Puedes tambien usar el material bibliogarfico de la seccion "8. IX. BIBLIOGRAFÍA" para que no necesites inventarte la bibliografia. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). La respuesta debe ser una lista de puntos concisa y no exceder las 150 palabras.""",
    
    "Tipo de evaluación": "Actúa como un experto en evaluación. Basándote en las actividades evaluativas propuestas para la unidad {nombre_unidad}, determina y nombra el tipo de evaluación principal (Formativa, Sumativa o Mixta). Justifica brevemente tu respuesta. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). No excedas las 100 palabras.",
    "Instrumento": "Actúa como un experto en evaluación y realiza una propuesta de instrumento evaluativo detallado (ej. una rúbrica simple o una lista de cotejo) para la actividad sumativa principal de la unidad {nombre_unidad}. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc). No excedas las 200 palabras.",
    "Ponderación (%)": "Actúa como un experto en evaluación y redacta una propuesta de ponderación para las actividades sumativas declaradas para la unidad de aprendizaje y que tributen a los siguientes indicadores de logro {indicadores_logro}. La respuesta debe ser sin introducciones ni explicaciones, ni formato extra (títulos, negritas, etc)."
    
}