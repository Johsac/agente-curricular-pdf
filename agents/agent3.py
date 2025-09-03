# agents/agent3.py

from pathlib import Path
from llama_index.llms.openai import OpenAI
from prompts.prompts_library import PROMPTS_AGENTE_3
import re

# --- LISTA OFICIAL DE CAMPOS QUE EL AGENTE 3 PUEDE GENERAR ---
GENERATABLE_FIELDS = [
    "Resultado de aprendizaje del curso",
    "Resultado de aprendizaje de la unidad",
    "Indicadores de Evaluación(IE)",
    "Actividades didácticas y experiencias de aprendizaje",
    "Actividades evaluativas (formativas y/o sumativas)",
    "Recursos y materiales",
    "Tipo de evaluación",
    "Instrumento",
    "Ponderación (%)"
]

def parse_partial_plan(plan_content: str):
    """
    Extrae información clave y la estructura de unidades del plan parcial
    para usarla como contexto en los prompts del Agente 3.
    """
    print("    [Agente 3 - Paso 1/4] Analizando el plan parcial...")
    data = {}
    try:
        data['nombre_asignatura'] = re.search(r"- Nombre del curso/asignatura:\s*(.*)", plan_content).group(1).strip()
        
        unidades_texto = re.search(r"- Unidad:\s*(.*?)(?=- Indicadores de Evaluación\(IE\):)", plan_content, re.DOTALL).group(1).strip()
        contenidos_texto = re.search(r"- Contenidos de la Unidad:\s*(.*?)(?=- Actividades didácticas)", plan_content, re.DOTALL).group(1).strip()
        aprendizajes_texto = re.search(r"- Resultado de aprendizaje de la unidad:\s*(.*?)\n\n3\.", plan_content, re.DOTALL).group(1).strip()

        unidades_titulos = [u.strip().replace("- ", "") for u in unidades_texto.split('\n') if u.strip() and "UNIDAD" in u]
        
        contenidos_split_raw = re.split(r'UNIDAD [IVX]+:', contenidos_texto)
        contenidos_split = [c.strip() for c in contenidos_split_raw if c.strip()]
        
        aprendizajes_bloques_raw = re.split(r'-\s*AE\d+:', aprendizajes_texto)
        aprendizajes_bloques = [a.strip() for a in aprendizajes_bloques_raw if a.strip()]

        data['unidades'] = []
        for i, titulo in enumerate(unidades_titulos):
            unidad_data = {
                "nombre_unidad": titulo,
                "contenido_unidad": contenidos_split[i] if i < len(contenidos_split) else "Contenido no encontrado",
                "aprendizaje_esperado": aprendizajes_bloques[i] if i < len(aprendizajes_bloques) else "Aprendizaje esperado no encontrado"
            }
            data['unidades'].append(unidad_data)
        
        print(f"    [Agente 3 - Paso 1/4] Análisis completado. Se encontraron {len(data['unidades'])} unidades.")
        return data
        
    except (AttributeError, IndexError) as e:
        print(f"    [Agente 3 - ERROR] No se pudo analizar la estructura del archivo parcial: {e}")
        return None

def run_agent_3(planificacion_parcial_path: Path):
    print("\n--- Iniciando Agente 3: Verificación y Generación por Razonamiento ---")
    
    with open(planificacion_parcial_path, "r", encoding="utf-8") as f:
        contenido_parcial = f.read()

    context_data = parse_partial_plan(contenido_parcial)
    if not context_data:
        # Si el parseo falla, simplemente se copia el archivo sin cambios.
        output_path = Path("./resultados/")
        planificacion_final_path = output_path / "planificacion_final.txt"
        with open(planificacion_final_path, "w", encoding="utf-8") as f:
            f.write(contenido_parcial)
        return

    llm = OpenAI(model="gpt-4o-mini")
    contenido_final = contenido_parcial
    
    print(f"    [Agente 3 - Paso 2/4] Asignatura identificada: {context_data['nombre_asignatura']}.")
    print("    [Agente 3 - Paso 3/4] Verificando y generando contenido para campos autorizados...")

    # --- LÓGICA DE VERIFICACIÓN Y RELLENO ---
    for field_name in GENERATABLE_FIELDS:
        # Crear un patrón de búsqueda flexible para el campo
        field_pattern = re.compile(f"(- {re.escape(field_name)}:.*)", re.IGNORECASE)
        match = field_pattern.search(contenido_final)

        if not match:
            continue

        # Extraer la línea completa (ej: "- Tipo de evaluación: ") para ver si está vacía
        linea_actual = match.group(1)
        # Verificar si la línea está vacía, o contiene los marcadores
        if linea_actual.endswith(": ") or "No encontrado" in linea_actual or "PENDIENTE - AGENTE 3" in linea_actual:
            print(f"\n      >> Campo '{field_name}' requiere generación. Iniciando...")
            
            # Lógica de generación (unitaria o por cada unidad)
            if "unidad" in PROMPTS_AGENTE_3[field_name] or "logro" in PROMPTS_AGENTE_3[field_name]:
                # Generar contenido para cada unidad
                generated_blocks = []
                for unidad in context_data['unidades']:
                    prompt = PROMPTS_AGENTE_3[field_name].format(
                        nombre_asignatura=context_data['nombre_asignatura'],
                        n_indicadores=3,
                        nombre_unidad=unidad['nombre_unidad'],
                        aprendizaje_esperado=unidad['aprendizaje_esperado'],
                        contenido_unidad=unidad['contenido_unidad'],
                        indicadores_logro="[Indicadores generados previamente]" # Simplificado, se puede mejorar
                    )
                    print(f"        -> Enviando prompt para '{unidad['nombre_unidad']}'...")
                    response = str(llm.complete(prompt)).strip()
                    generated_blocks.append(f"Para {unidad['nombre_unidad']}:\n{response}")
                
                final_generated_text = "\n\n".join(generated_blocks)
            else:
                # Generar contenido a nivel de curso
                prompt = PROMPTS_AGENTE_3[field_name].format(nombre_asignatura=context_data['nombre_asignatura'])
                print(f"        -> Enviando prompt para '{field_name}'...")
                final_generated_text = str(llm.complete(prompt)).strip()

            # Reemplazar la línea vacía/marcador con el nuevo contenido
            contenido_final = contenido_final.replace(linea_actual, f"- {field_name}:\n{final_generated_text}")
            print("        <- Contenido generado y reemplazado.")

    # Guardar el archivo final
    output_path = Path("./resultados/")
    planificacion_final_path = output_path / "planificacion_final.txt"
    with open(planificacion_final_path, "w", encoding="utf-8") as f:
        f.write(contenido_final)
        
    print(f"\n    [Agente 3 - Paso 4/4] Archivo de planificación final guardado en: {planificacion_final_path}")
    print("--- Agente 3: Proceso completado ---")