PROMPTS_AGENTE_1 = {
    "I. IDENTIFICACIÓN": (
        "Del documento, extrae el contenido completo de la sección 'I. IDENTIFICACIÓN'. Asegúrate de que la parte de 'Requisito para cursar', 'Requisitos previos' y 'Co - Requisitos' se presenten en líneas separadas y únicas, así: 'Requisito para cursar: No tiene'."
        #"Si tus políticas de seguridad te impiden extraer textualmente, genera un resumen detallado y comienza tu respuesta con 'AVISO: El siguiente texto es un resumen generado por IA debido a políticas internas de seguridad o directrices de uso:'"
    ),
    "II. CARGA ACADÉMICA": (
        """Tu rol es ser un asistente de extracción de datos. A partir del texto proporcionado, localiza la sección "II. CARGA ACADÉMICA". Tu única tarea es encontrar los valores numéricos para las siguientes categorías  y devolverlos en una lista.

Las SCT (horas cronológicas) se dividen en dos: Directas o Personal.
Para el "Tipo de Actividad", haya el valor numérico de:
Presenta el resultado colocando como titulo "Tipo de Actividad - SCT (horas cronológicas)":
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
Para las últimas dos categorías de "Tipo de Actividad", se coloca un valor único de SCT.
- Total horas dedicación semanal: [valor]
- Créditos SCT: [valor]

**Instrucciones importantes:**
1. Si una celda está vacía o no tiene un número, déjalo con un espacio vacío: ` `.
2. No incluyas ningún texto introductorio o conclusión."""
    ),
    "III. DESCRIPCIÓN": (
        "Extrae el texto completo y sin modificar de 'III. DESCRIPCIÓN'. "
        #"Si tus políticas de seguridad te impiden extraer textualmente, genera un resumen detallado y comienza tu respuesta con 'AVISO: El siguiente texto es un resumen generado por IA debido a políticas internas de seguridad o directrices de uso:'"
    ),
    "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS": (
        "Realiza la siguiente tarea compleja: 1. Busca en todo el documento los títulos de 'UNIDAD' (ej. 'UNIDAD I: ...') y el texto de sus correspondientes 'Aprendizaje Esperado' (AE). "
        "2. El contenido de cada UNIDAD (usualmente una lista de puntos) puede estar en una página diferente a su título. Debes encontrarlo. "
        "3. Formatea la salida para cada par así, asegurándote de incluir el contenido completo de la unidad:\n"
        "UNIDAD I: [Título y todo el contenido en lista de la UNIDAD I]\n\nAE1: [Texto completo de AE1]\n\n---"
    ),
    "VI. HABILIDADES TRANSVERSALES": (
        "Extrae el texto completo y sin modificar de 'VI. HABILIDADES TRANSVERSALES'. "
        #"Si tus políticas de seguridad te impiden extraer textualmente, genera un resumen detallado y comienza tu respuesta con 'AVISO: El siguiente texto es un resumen generado por IA debido a políticas internas de seguridad o directrices de uso:'"
    ),
    "VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN": (
        "Extrae el texto completo y sin modificar de 'VII. ESTRATEGIAS DIDÁCTICAS Y PROCEDIMIENTOS DE EVALUACIÓN'. "
        #"Si tus políticas de seguridad te impiden extraer textualmente, genera un resumen detallado y comienza tu respuesta con 'AVISO: El siguiente texto es un resumen generado por IA debido a políticas internas de seguridad o directrices de uso:'"
    ),
    "VIII. CONDICIONES DE APROBACIÓN": (
        "Extrae el texto completo y sin modificar de 'VIII. CONDICIONES DE APROBACIÓN'. "
        #"Si tus políticas de seguridad te impiden extraer textualmente, genera un resumen detallado y comienza tu respuesta con 'AVISO: El siguiente texto es un resumen generado por IA debido a políticas internas de seguridad o directrices de uso:'"
    ),
    "IX. BIBLIOGRAFÍA": (
        "Extrae el texto completo y sin modificar de 'IX. BIBLIOGRAFÍA'. , donde esta sección está dividida generalmente en subsecciones como 'Obligatoria' y 'Complementaria'. "

    ),
    "X. CORRESPONDENCIA CRÉDITOS UNAB": (
        """Del texto de la sección 'X. CORRESPONDENCIA CRÉDITOS UNAB', extrae dos cosas:
1. Una lista de todos los números que aparecen en la tabla, en el orden exacto en que aparecen.
2. El texto completo del párrafo que comienza con "Nota importante:".
3. Al mostrar los resultados COMIENZA CON UN ENCABEZADO que diga: 'Horas pedagógicas:'

Formatea tu respuesta exactamente así:
COMIENZA CON UN ENCABEZADO OBLIGATORIO: 'Horas pedagógicas:'
NUMEROS: [lista de números separados por comas]
TEXTO: [texto de la nota]"""  
    )
}


PROMPT_AGENTE_2_TEMPLATE = """
Tu tarea es actuar como un planificador curricular experto. Debes rellenar la "PLANTILLA A RELLENAR" basándote en dos fuentes de información: el "SOPORTE TEÓRICO" que define cada categoría y el "CONTEXTO" que contiene el texto extraído de un programa de asignatura.

---
# SOPORTE TEÓRICO PARA LA EXTRACCIÓN

**Resultado de aprendizaje del curso:** Es una declaración clara, específica y medible que describe lo que un estudiante será capaz de conocer, comprender, aplicar o demostrar al finalizar un curso. Se centra en el estudiante, es observable y se formula con verbos de acción.

**Resultado de aprendizaje de la unidad:** Es una declaración específica y observable que expresa lo que el estudiante debe demostrar al finalizar una unidad. Se deriva del resultado de aprendizaje del curso y representa una meta intermedia.

**Unidad:** Es un segmento estructurado de contenido en torno a un tema, problema o competencia. Constituye un bloque de enseñanza-aprendizaje.

**Indicadores de Evaluación(IE):** Es un descriptor observable y medible que permite verificar el grado en que un estudiante ha alcanzado un resultado de aprendizaje. Se expresa en conductas o productos observables.

**Contenidos de la Unidad:** Es el conjunto de saberes (conceptos, procedimientos) seleccionados para que el estudiante alcance los Resultados de Aprendizaje de la Unidad.

**Actividades didácticas y experiencias de aprendizaje:** Son las estrategias planificadas por el docente que sitúan al estudiante en un proceso activo para alcanzar los Resultados de Aprendizaje.

**Actividades evaluativas (formativas y/o sumativas):** Son las tareas diseñadas para que el estudiante demuestre el logro de los Resultados de Aprendizaje. La formativa retroalimenta el proceso; la sumativa certifica el resultado.

**Recursos y materiales:** Son todos los apoyos didácticos, tecnológicos y bibliográficos que se ponen a disposición del estudiante.

**Tipo de evaluación:** Se refiere a la función y momento de la evaluación (Formativa: durante el proceso para retroalimentar; Sumativa: al cierre para certificar el logro).

**Instrumento:** Es la herramienta concreta con la que se recoge evidencia del aprendizaje (ej. Ensayo con rúbrica, Estudio de caso, Proyecto, Presentación oral, etc.).

**Ponderación (%):** Es el peso porcentual de cada actividad evaluativa en la calificación final (ej. 20%, 30%).
---

**CONTEXTO:**
{contenido_observaciones_txt}

---
**PLANTILLA A RELLENAR:**

# MATRIZ DE PLANIFICACIÓN CURRICULAR UNIFICADA

1. Identificación general del curso
- Nombre del curso/asignatura: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Nombre"]
- Código: [Busca en "I. IDENTIFICACIÓN" el campo "Código"]
- Programa/Plan de estudios: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Carrera"]
- Modalidad: [Busca en la sección "I" o "VIII" o "X" el campo "Modalidad" o similar, si la modalidad es alguna de estas 3 opciones: Online o Presencial o Semipresencial. Si no lo encuentras, coloca "Presencial"]
- Nivel académico: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Periodo" o "Semestre"]
- Duración: [Busca en la sección "I. IDENTIFICACIÓN" el campo "Régimen" o "Periodo"]
- Créditos SCT: [Busca en la sección "II. CARGA ACADÉMICA" el campo "Créditos SCT"]
- Docente/ Diseñador instruccional(s) del curso: 
- Fecha de elaboración: 

2. Objetivos formativos
- Resultado de aprendizaje del curso: [Extrae el texto del "Resultado de Aprendizaje (RA)" de la sección "III. DESCRIPCIÓN"]
- Resultado de aprendizaje de la unidad: [Extrae y lista todos los "Aprendizajes Esperados (AE)" de la sección "IV. APRENDIZAJES ESPERADOS y V. CONTENIDOS"]

3. Estructura por unidad
- Unidad: [De la sección "IV", extrae y lista todos los títulos de las Unidades (ej. "UNIDAD I: FUNDAMENTOS...", "UNIDAD II: ...").]
- Indicadores de Evaluación(IE): [coloca textualmente esta frase: "PENDIENTE - AGENTE 3"]
- Contenidos de la Unidad: [De la sección "IV", extrae y lista los contenidos asociados a cada una de las unidades que encontraste.]
- Actividades didácticas y experiencias de aprendizaje: [coloca textualmente esta frase: "PENDIENTE - AGENTE 3"]
- Actividades evaluativas (formativas y/o sumativas): [coloca textualmente esta frase: "PENDIENTE - AGENTE 3"]
- Recursos y materiales: [coloca textualmente esta frase: "PENDIENTE - AGENTE 3"]

4. Evaluación
- Tipo de evaluación: [Basándote en la definición del SOPORTE TEÓRICO, busca en las secciones VII y VIII y extrae textualmente palabras clave como 'diagnóstica', 'formativa', 'sumativa', 'avances', 'solemnes', 'examen final'.]
- Instrumento: [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VII y extrae textualmente herramientas como 'rúbricas', 'lista de cotejo', 'proyecto', 'estudio de casos', 'exposición oral'.]
- Indicadores asociados: 
- Ponderación (%): [Basándote en la definición del SOPORTE TEÓRICO, busca en la sección VIII y extrae textualmente cualquier peso porcentual explícito (ej. '70%', '30%').]

**Instrucciones:**
- Rellena cada campo [ ] con la información exacta que encuentres en el CONTEXTO.
- Si un campo no tiene una instrucción de búsqueda específica (como 'Indicadores de Evaluación(IE)'), déjalo en blanco.
- No incluyas ningún texto introductorio ni conclusión, solo la plantilla rellenada.
"""

PROMPTS_AGENTE_3 = {
    "Resultado de aprendizaje del curso": "Actúa como un experto metodológico y redacta un resultado de aprendizaje claro, medible y coherente para la asignatura {nombre_asignatura}. El resultado debe describir lo que el estudiante será capaz de hacer al finalizar el curso, utilizando verbos de acción de la Taxonomía de Bloom (versión revisada). Incluye un solo resultado, expresado en tiempo futuro, que combine conocimiento, habilidades y actitudes relevantes para la asignatura. Evita formulaciones vagas y asegúrate de que sea observable y evaluable.",
    "Resultado de aprendizaje de la unidad": "Actúa como un experto metodológico y redacta un resultado de aprendizaje claro, medible y coherente para la asignatura {nombre_asignatura} y de la unidad {nombre_unidad}. El resultado debe describir lo que el estudiante será capaz de hacer al finalizar la unidad, utilizando verbos de acción de la Taxonomía de Bloom (versión revisada). Incluye un solo resultado, expresado en tiempo futuro, que combine conocimiento, habilidades y actitudes relevantes para la asignatura. Evita formulaciones vagas y asegúrate de que sea observable y evaluable.",
    #"Indicadores de Evaluación(IE)": "Actúa como un docente experto metodológico y de la asignatura {nombre_asignatura} y redacta {n_indicadores} indicadores de logro para cada unidad de aprendizaje que sea coherente con el aprendizaje esperado de la unidad: Unidad N°: {nombre_unidad}. Cada indicador de logro debe ser redactado con un solo verbo (taxonomía de Bloom) + contenido de la unidad + contexto (donde o para qué se realiza la acción). Además, deben estar graduados en función de la taxonomía de Bloom y no superar taxonómicamente al aprendizaje esperado. Considera la siguiente información de la asignatura: Aprendizaje esperado para la unidad N°: {aprendizaje_esperado} Contenido de la unidad N°: {contenido_unidad}",
    "Indicadores de Evaluación(IE)": "Actúa como un docente experto metodológico para la asignatura {nombre_asignatura} y redacta {n_indicadores} indicadores de logro para la unidad '{nombre_unidad}'. Cada indicador debe ser coherente con el siguiente aprendizaje esperado: '{aprendizaje_esperado}'. Redacta cada indicador con un verbo (taxonomía de Bloom) + contenido + contexto. La respuesta debe ser una lista de puntos. Sé directo y no uses frases introductorias. No excedas las 150 palabras.",
    #"Actividades didácticas y experiencias de aprendizaje": "Actúa como un docente experto metodológico y de la asignatura {nombre_asignatura} y redacta una experiencia de aprendizaje donde se describa qué actividad formativa y de evaluación se puede proponer para la unidad {nombre_unidad} y que tributen a los siguientes indicadores de logro {indicadores_logro}.",
    "Actividades didácticas y experiencias de aprendizaje": "Actúa como un docente experto para la asignatura {nombre_asignatura} y redacta una experiencia de aprendizaje para la unidad '{nombre_unidad}' que tribute a los siguientes indicadores de logro: {indicadores_logro}. La respuesta debe ser concisa y no exceder las 300 palabras. No uses introducciones.",
    #"Actividades evaluativas (formativas y/o sumativas)": "Actúa como un docente experto en evaluación y de la asignatura {nombre_asignatura} y redacta actividades formativas y/o sumativas que se pueden proponer para la unidad {nombre_unidad} y que tributen a los siguientes indicadores de logro {indicadores_logro}.",
    "Actividades evaluativas (formativas y/o sumativas)": "Actúa como un docente experto en evaluación para la asignatura {nombre_asignatura} y redacta actividades formativas y/o sumativas para la unidad '{nombre_unidad}' que tributen a los siguientes indicadores de logro: {indicadores_logro}. La respuesta debe ser una lista de puntos y no exceder las 300 palabras. Sé directo.",
    #"Recursos y materiales": "Actúa como un docente experto de la asignatura {nombre_asignatura} y redacta propuesta de recursos y materiales que se pueden proponer para la unidad {nombre_unidad} y que tributen a los siguientes indicadores de logro.",
    "Recursos y materiales": "Actúa como un docente experto para la asignatura {nombre_asignatura} y redacta una propuesta de recursos y materiales para la unidad '{nombre_unidad}' que tributen a los siguientes indicadores de logro: {indicadores_logro}. La respuesta debe ser una lista concisa y no exceder las 300 palabras.",
    "Tipo de evaluación": "Aquí deberás indicar las actividades formativas y sumativas propuestas anteriormente para esta unidad.",
    "Instrumento": "Actúa como un experto en evaluación y realiza una propuesta de instrumento evaluativo para las actividades sumativas.",
    "Ponderación (%)": "Actúa como un experto en evaluación y redacta una propuesta de ponderación para las actividades sumativas declaradas para la unidad de aprendizaje y que tributen a los siguientes indicadores de logro {indicadores_logro}."
}

