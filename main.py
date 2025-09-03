# main.py

import os
import sys
from pathlib import Path
from api_key import key

# Configuración de LlamaIndex
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Importar los agentes
from agents.agent1 import run_agent_1
from agents.agent2 import run_agent_2
from agents.agent3 import run_agent_3

def main(pdf_file_path_str: str):
    """
    Función principal que orquesta la ejecución de los 3 agentes.
    """
    # Configuración inicial
    os.environ["OPENAI_API_KEY"] = key
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    
    pdf_file_path = Path(pdf_file_path_str)
    if not pdf_file_path.is_file():
        print(f"\nError: El archivo no se encuentra en la ruta: {pdf_file_path}")
        sys.exit(1)
        
    # --- Ejecutar la pipeline completa ---
    # 1. Agente 1 extrae la información cruda y estructurada.
    structured_path, _ = run_agent_1(pdf_file_path)
    
    # 2. Agente 2 crea el borrador de la planificación.
    planificacion_parcial_path = run_agent_2(structured_path)
    
    # 3. Agente 3 lee el borrador y rellena los campos restantes.
    run_agent_3(planificacion_parcial_path)
    
    print("\n¡Proceso finalizado con éxito!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nError: Debes proporcionar la ruta al archivo PDF como argumento.")
        print("Ejemplo de uso: python main.py \"ruta\\a\\mi\\documento.pdf\"")
        sys.exit(1)
    
    pdf_path_argument = sys.argv[1]
    main(pdf_path_argument)