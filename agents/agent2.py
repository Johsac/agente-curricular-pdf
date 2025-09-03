# agents/agent2.py

from pathlib import Path
from llama_index.llms.openai import OpenAI
from prompts.prompts_library import PROMPT_AGENTE_2_TEMPLATE

def run_agent_2(structured_path: Path):
    """
    Lógica del Agente 2: Lee los .txt y genera el archivo de planificación parcial
    con marcadores de posición para el Agente 3.
    """
    print("\n--- Iniciando Agente 2: Generación de Planificación Parcial ---")
    
    with open(structured_path, "r", encoding="utf-8") as f:
        contenido_observaciones_txt = f.read()

    prompt_final = PROMPT_AGENTE_2_TEMPLATE.format(contenido_observaciones_txt=contenido_observaciones_txt)
    
    print("Generando el documento de planificación parcial con el LLM...")
    llm = OpenAI(model="gpt-4o-mini")
    response = llm.complete(prompt_final)
    planificacion_content = str(response)

    output_path = Path("./resultados/")
    planificacion_parcial_path = output_path / "planificacion_parcial.txt"
    with open(planificacion_parcial_path, "w", encoding="utf-8") as f:
        f.write(planificacion_content)
        
    print(f"Archivo de planificación parcial guardado en: {planificacion_parcial_path}")
    print("--- Agente 2: Proceso completado ---")
    
    return planificacion_parcial_path
