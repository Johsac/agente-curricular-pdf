# agents/agent3.py

from pathlib import Path
import re
import time
import json
from prompts.prompts_library import PROMPTS_AGENTE_3

# --- FUNCIONES AUXILIARES (DEBEN ESTAR EN EL ARCHIVO) ---

def add_visual_separators(content: str) -> str:
    content_with_spaces = re.sub(r'(?m)^(\d+\.\s.*)', r'\n\1', content)
    return content_with_spaces.strip()

def parse_partial_plan(plan_content: str):
    print("    [Agente 3 - Paso 1/4] Analizando el plan parcial (versión robusta)...")
    data = {}
    try:
        def safe_extract(pattern, text, flags=re.IGNORECASE):
            match = re.search(pattern, text, flags)
            return match.group(1).strip() if match else ""

        data['nombre_asignatura'] = safe_extract(r"-\s*Nombre del curso/asignatura:\s*(.*)", plan_content)
        if not data['nombre_asignatura']:
            raise ValueError("No se pudo extraer el nombre de la asignatura.")

        # Extraer los bloques principales de texto de forma segura
        unidades_bloque = safe_extract(r"##\s*Unidad\s*([\s\S]*?)(?=##|$)", plan_content, re.DOTALL)
        contenidos_bloque = safe_extract(r"##\s*Contenidos de la Unidad\s*([\s\S]*?)(?=##|$)", plan_content, re.DOTALL)
        aprendizajes_bloque = safe_extract(r"##\s*Resultado de aprendizaje de la unidad\s*([\s\S]*?)(?=##|$)", plan_content, re.DOTALL)
        
        unidades_titulos = re.findall(r'^\s*-\s*(UNIDAD\s+[IVX\d]+[:\s-].*)', unidades_bloque, re.MULTILINE | re.IGNORECASE)
        if not unidades_titulos:
            raise ValueError("No se encontraron títulos de UNIDAD en el formato esperado.")

        data['unidades'] = []
        for i, titulo in enumerate(unidades_titulos):
            # --- CORRECCIÓN DEFINITIVA DEL LECTOR "AMBICIOSO" ---
            # Busca el contenido desde el título actual hasta el siguiente título de unidad, o hasta el final del bloque.
            start_pos = contenidos_bloque.find(titulo)
            end_pos = len(contenidos_bloque)
            if i + 1 < len(unidades_titulos):
                next_start_pos = contenidos_bloque.find(unidades_titulos[i+1])
                if next_start_pos != -1:
                    end_pos = next_start_pos
            
            contenido_unidad_raw = contenidos_bloque[start_pos:end_pos]
            contenido_unidad = contenido_unidad_raw.replace(titulo, "", 1).strip()
            
            ae_num = i + 1
            aprendizaje_esperado = safe_extract(rf"-\s*AE{ae_num}:\s*(.*)", aprendizajes_bloque)

            data['unidades'].append({
                "nombre_unidad": titulo.strip(),
                "contenido_unidad": contenido_unidad or "Contenido no encontrado",
                "aprendizaje_esperado": aprendizaje_esperado or "[AE no encontrado en el archivo parcial]"
            })
        
        print(f"    [Agente 3 - Paso 1/4] Análisis completado. Se encontraron {len(data['unidades'])} unidades.")
        return data
        
    except (AttributeError, IndexError, ValueError) as e:
        print(f"    [Agente 3 - ERROR] No se pudo analizar la estructura del archivo parcial: {e}")
        return None

# --- FUNCIÓN PRINCIPAL DEL AGENTE ---

def run_agent_3(planificacion_parcial_path: Path, llm):
    print("\n--- Iniciando Agente 3: Verificación y Generación por Razonamiento ---")
    
    with open(planificacion_parcial_path, "r", encoding="utf-8") as f:
        contenido_parcial = f.read()

    context_data = parse_partial_plan(contenido_parcial)
    if not context_data:
        # Manejo de error si el parseo inicial falla
        output_path = Path("./resultados/")
        planificacion_final_path = output_path / "planificacion_final.txt"
        with open(planificacion_final_path, "w", encoding="utf-8") as f: f.write("ERROR: El Agente 3 no pudo analizar el archivo del Agente 2.\n\n" + contenido_parcial)
        print("    [Agente 3 - ERROR] Se guardó el contenido parcial para revisión.")
        return

    print("\n    [Agente 3 - DEBUG] CONTEXTO EXTRAÍDO DEL PLAN PARCIAL:")
    print(json.dumps(context_data, indent=2, ensure_ascii=False))
    print("    --------------------------------------------------\n")

    contenido_final = contenido_parcial
    print(f"    [Agente 3 - Paso 2/4] Asignatura identificada: {context_data['nombre_asignatura']}.")
    print("    [Agente 3 - Paso 3/4] Buscando y ejecutando tareas 'PENDIENTE'...")
    
    unidad_ies_generados = {}

    while "PENDIENTE - AGENTE 3" in contenido_final:
        tarea_match = re.search(r"(##\s*.*?)\n\s*-\s*PENDIENTE - AGENTE 3", contenido_final, re.IGNORECASE)
        if not tarea_match: break

        header_line = tarea_match.group(1).strip()
        
        def get_prompt_key(header):
            norm = re.sub(r'[\s\(\)/]', '', header).lower()
            for key in PROMPTS_AGENTE_3:
                if re.sub(r'[\s\(\)/]', '', key).lower() in norm: return key
            return None
        
        field_name_key = get_prompt_key(header_line)
        if not field_name_key:
            print(f"       >> ADVERTENCIA: Se encontró PENDIENTE para '{header_line}' pero no hay prompt. Saltando.")
            contenido_final = contenido_final.replace("- PENDIENTE - AGENTE 3", "[Error: Prompt no encontrado]", 1)
            continue

        print(f"\n       >> Tarea encontrada: '{field_name_key}'. Iniciando generación...")
        prompt_template = PROMPTS_AGENTE_3[field_name_key]
        
        if "{nombre_unidad}" in prompt_template:
            generated_blocks = []
            for unidad in context_data['unidades']:
                prompt = prompt_template.format(
                    nombre_asignatura=context_data['nombre_asignatura'], n_indicadores=3,
                    nombre_unidad=unidad['nombre_unidad'], aprendizaje_esperado=unidad['aprendizaje_esperado'],
                    contenido_unidad=unidad['contenido_unidad'],
                    indicadores_logro=unidad_ies_generados.get(unidad['nombre_unidad'], "[Indicadores no generados previamente]")
                )
                
                print(f"\n    [Agente 3 - DEBUG] PROMPT PARA '{unidad['nombre_unidad']}':\n    ----------------\n    {prompt}\n    ----------------")
                response = str(llm.complete(prompt)).strip()
                print(f"         <- Respuesta de IA recibida para '{unidad['nombre_unidad']}'.")
                time.sleep(2)
                
                if "Indicadores de Evaluación" in field_name_key:
                    unidad_ies_generados[unidad['nombre_unidad']] = response
                nombre_unidad_limpio = unidad['nombre_unidad'].replace("-", "").strip()
                generated_blocks.append(f"### **{nombre_unidad_limpio}**\n{response}")
            final_generated_text = "\n\n".join(generated_blocks)
        else:
            prompt = prompt_template.format(nombre_asignatura=context_data['nombre_asignatura'])
            print(f"\n    [Agente 3 - DEBUG] PROMPT PARA CAMPO GLOBAL:\n    ----------------\n    {prompt}\n    ----------------")
            final_generated_text = str(llm.complete(prompt)).strip()
            print("         <- Respuesta de IA recibida.")
            time.sleep(2)
        
        bloque_de_tarea_a_reemplazar = tarea_match.group(0)
        nuevo_bloque_completo = f"{header_line}\n{final_generated_text}\n\n"
        contenido_final = contenido_final.replace(bloque_de_tarea_a_reemplazar, nuevo_bloque_completo, 1)
        print(f"       >> Tarea '{field_name_key}' completada.")

    contenido_final_formateado = add_visual_separators(contenido_final)
    output_path = Path("./resultados/")
    planificacion_final_path = output_path / "planificacion_final.txt"
    with open(planificacion_final_path, "w", encoding="utf-8") as f: f.write(contenido_final_formateado)
    print(f"\n    [Agente 3 - Paso 4/4] Archivo de planificación final guardado en: {planificacion_final_path}")
    print("--- Agente 3: Proceso completado ---")

##############################################################################################################

# # agents/agent3.py

# from pathlib import Path
# import re
# import time
# from prompts.prompts_library import PROMPTS_AGENTE_3

# # Lista de campos canónicos. El código los buscará de forma flexible.
# GENERATABLE_FIELDS = [
#     "Resultado de aprendizaje del curso",
#     "Resultado de aprendizaje de la unidad",
#     "Indicadores de Evaluación (IE)",
#     "Actividades didácticas y experiencias de aprendizaje",
#     "Actividades evaluativas (formativas y/o sumativas)",
#     "Recursos y materiales",
#     "Tipo de evaluación",
#     "Instrumento",
#     "Indicadores asociados",
#     "Ponderación (%)"
# ]

# def add_visual_separators(content: str) -> str:
#     content_with_spaces = re.sub(r'(?m)^(\d+\.\s.*)', r'\n\1', content)
#     return content_with_spaces.strip()

# def parse_partial_plan(plan_content: str):
#     print("    [Agente 3 - Paso 1/4] Analizando el plan parcial (versión robusta)...")
#     data = {}
#     try:
#         def safe_extract(pattern, text, flags=re.IGNORECASE):
#             match = re.search(pattern, text, flags)
#             return match.group(1).strip() if match else ""

#         data['nombre_asignatura'] = safe_extract(r"-\s*Nombre del curso/asignatura:\s*(.*)", plan_content)
#         if not data['nombre_asignatura']:
#             raise ValueError("No se pudo extraer el nombre de la asignatura.")

#         unidades_bloque = safe_extract(r"##\s*Unidad\s*([\s\S]*?)##", plan_content, re.DOTALL | re.IGNORECASE)
#         contenidos_bloque = safe_extract(r"##\s*Contenidos de la Unidad\s*([\s\S]*?)##", plan_content, re.DOTALL | re.IGNORECASE)
        
#         unidades_titulos = re.findall(r'^\s*-\s*(UNIDAD\s+[IVX\d]+[:\s-].*)', unidades_bloque, re.MULTILINE | re.IGNORECASE)
#         if not unidades_titulos:
#             raise ValueError("No se encontraron títulos de UNIDAD en el formato esperado.")

#         data['unidades'] = []
#         for titulo in unidades_titulos:
#             contenido_unidad = safe_extract(re.escape(titulo.strip()) + r'([\s\S]*?)(?=\s*-\s*UNIDAD|\Z)', contenidos_bloque, re.DOTALL | re.IGNORECASE)
#             data['unidades'].append({ "nombre_unidad": titulo.strip(), "contenido_unidad": contenido_unidad or "Contenido no encontrado", "aprendizaje_esperado": "" })
        
#         print(f"    [Agente 3 - Paso 1/4] Análisis completado. Se encontraron {len(data['unidades'])} unidades.")
#         return data
        
#     except (AttributeError, IndexError, ValueError) as e:
#         print(f"    [Agente 3 - ERROR] No se pudo analizar la estructura del archivo parcial: {e}")
#         return None

# def run_agent_3(planificacion_parcial_path: Path, llm):
#     print("\n--- Iniciando Agente 3: Verificación y Generación por Razonamiento ---")
    
#     with open(planificacion_parcial_path, "r", encoding="utf-8") as f:
#         contenido_parcial = f.read()

#     context_data = parse_partial_plan(contenido_parcial)
#     if not context_data:
#         # Manejo de error si el parseo inicial falla
#         output_path = Path("./resultados/")
#         planificacion_final_path = output_path / "planificacion_final.txt"
#         with open(planificacion_final_path, "w", encoding="utf-8") as f: f.write("ERROR: El Agente 3 no pudo analizar el archivo del Agente 2.\n\n" + contenido_parcial)
#         print("    [Agente 3 - ERROR] Se guardó el contenido parcial para revisión.")
#         return

#     contenido_final = contenido_parcial
#     print(f"    [Agente 3 - Paso 2/4] Asignatura identificada: {context_data['nombre_asignatura']}.")
#     print("    [Agente 3 - Paso 3/4] Verificando y generando contenido para campos autorizados...")
    
#     unidad_ies_generados = {}

#     # --- BUCLE FINAL Y ROBUSTO ---
#     for field_name in GENERATABLE_FIELDS:
#         # Función para "normalizar" un texto para comparación flexible
#         def normalize_header(text):
#             return re.sub(r'[\s\(\)/]', '', text).lower()

#         # Buscar la línea del encabezado de forma flexible
#         header_line = None
#         for line in contenido_final.split('\n'):
#             if line.startswith('##') and normalize_header(field_name) in normalize_header(line):
#                 header_line = line
#                 break
        
#         if not header_line: continue

#         # Lógica de extracción de contenido a prueba de errores
#         content_pattern = re.compile(re.escape(header_line) + r'([\s\S]*?)(?=^##\s|^\d+\.\s|\Z)', re.MULTILINE)
#         content_match = content_pattern.search(contenido_final)
#         contenido_actual = content_match.group(1).strip() if content_match else ""
        
#         if "PENDIENTE" in contenido_actual.upper() or not contenido_actual:
#             print(f"\n       >> Campo '{field_name}' requiere generación. Iniciando...")
#             prompt_template = PROMPTS_AGENTE_3.get(field_name)
#             if not prompt_template: continue

#             if "{nombre_unidad}" in prompt_template:
#                 generated_blocks = []
#                 for i, unidad in enumerate(context_data['unidades']):
#                     # Rellenar el aprendizaje esperado si es el momento
#                     if field_name == "Resultado de aprendizaje de la unidad" and not unidad['aprendizaje_esperado']:
#                          context_data['unidades'][i]['aprendizaje_esperado'] = str(llm.complete(prompt_template.format(nombre_asignatura=context_data['nombre_asignatura'], nombre_unidad=unidad['nombre_unidad'], contenido_unidad=unidad['contenido_unidad']))).strip()
#                          time.sleep(2)

#                     prompt = prompt_template.format(
#                         nombre_asignatura=context_data['nombre_asignatura'], n_indicadores=3,
#                         nombre_unidad=unidad['nombre_unidad'], aprendizaje_esperado=unidad['aprendizaje_esperado'],
#                         contenido_unidad=unidad['contenido_unidad'],
#                         indicadores_logro=unidad_ies_generados.get(unidad['nombre_unidad'], "[Indicadores no generados previamente]")
#                     )
#                     print(f"         -> Enviando prompt para '{unidad['nombre_unidad']}'...")
#                     response = str(llm.complete(prompt)).strip()
#                     print("         <- Respuesta recibida.")
#                     time.sleep(2)
                    
#                     if field_name == "Indicadores de Evaluación (IE)":
#                         unidad_ies_generados[unidad['nombre_unidad']] = response

#                     nombre_unidad_limpio = unidad['nombre_unidad'].replace("-", "").strip()
#                     generated_blocks.append(f"### **{nombre_unidad_limpio}**\n{response}")
#                 final_generated_text = "\n\n".join(generated_blocks)
#             else:
#                 prompt = prompt_template.format(nombre_asignatura=context_data['nombre_asignatura'])
#                 print(f"         -> Enviando prompt para '{field_name}'...")
#                 final_generated_text = str(llm.complete(prompt)).strip()
#                 print("         <- Respuesta recibida.")
#                 time.sleep(2)

#             bloque_a_reemplazar = header_line + (content_match.group(1) if content_match else "")
#             nuevo_bloque_completo = f"{header_line}\n{final_generated_text}\n"
#             contenido_final = contenido_final.replace(bloque_a_reemplazar, nuevo_bloque_completo, 1)
#             print(f"       >> Campo '{field_name}' rellenado.")

#     contenido_final_formateado = add_visual_separators(contenido_final)
#     output_path = Path("./resultados/")
#     planificacion_final_path = output_path / "planificacion_final.txt"
#     with open(planificacion_final_path, "w", encoding="utf-8") as f: f.write(contenido_final_formateado)
        
#     print(f"\n    [Agente 3 - Paso 4/4] Archivo de planificación final guardado en: {planificacion_final_path}")
#     print("--- Agente 3: Proceso completado ---")