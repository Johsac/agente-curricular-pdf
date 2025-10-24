# agents/agent1.py

import re
from pathlib import Path
import camelot
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import SentenceSplitter
from prompts.prompts_library import PROMPTS_AGENTE_1

class HybridPDFReader:
    def read_pdf(self, file_path: Path) -> list[Document]:
        all_documents = []
        page_texts = {}
        with open(file_path, 'rb') as f:
            from PyPDF2 import PdfReader
            reader = PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                page_texts[page_num + 1] = page.extract_text() or ""
        try:
            tables = camelot.read_pdf(str(file_path), pages='all', flavor='lattice')
            tables_by_page = {tbl.page: tbl.df.to_markdown(index=False) for tbl in tables}
        # --- SUGERENCIA IMPLEMENTADA: Captura de error más específica y con logging ---
        except Exception as e:
            print(f"ADVERTENCIA: Camelot no pudo procesar las tablas del PDF. Error: {e}")
            tables_by_page = {}
            
        for page_num, text in page_texts.items():
            full_content = text
            if page_num in tables_by_page:
                full_content += f"\n\n--- TABLA DETECTADA EN ESTA PÁGINA ---\n{tables_by_page[page_num]}"
            all_documents.append(Document(text=full_content, metadata={"page_number": page_num, "file_name": file_path.name}))
        return all_documents

# --- SUGERENCIA IMPLEMENTADA: Se elimina la función `find_active_categories_from_section_ii` ---
# Ya no es necesaria, el LLM nos dará esta información directamente.

def create_structured_output_file(observaciones, titulos):
    content = f"Extracción Estructurada del Documento\n"
    content += "=" * 40 + "\n\n"
    for i, (titulo, obs_text) in enumerate(zip(titulos, observaciones)):
        content += f"---------- {i+1}. {titulo} ----------\n"
        content += f"{obs_text}\n\n"
    return content

def create_raw_backup_file(documents):
    content = "Copia de Seguridad - Texto Bruto y Tablas del PDF\n"
    content += "=" * 50 + "\n\n"
    for doc in documents:
        content += f"---------- Página {doc.metadata.get('page_number', 'N/A')} ----------\n"
        content += f"{doc.text}\n\n"
    return content

def run_agent_1(pdf_path: Path, llm):
    print(f"--- Iniciando Agente 1: Extracción de PDF (Modelo: {llm.model}) ---")
    
    print(f"Leyendo el archivo: {pdf_path.name}...")
    pdf_reader = HybridPDFReader()
    documents = pdf_reader.read_pdf(pdf_path)
    
    print("Creando índice de vectores (esto puede tardar un momento)...")
    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    index = VectorStoreIndex.from_documents(documents, transformations=[node_parser])
    
    print("Ejecutando prompts de extracción...")
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=10)
    observaciones = {}
    titulos_secciones = list(PROMPTS_AGENTE_1.keys())

    # --- SUGERENCIA IMPLEMENTADA: Nueva lógica de razonamiento para Secciones II y X ---
    print("Paso 1/2: Interpretando secciones complejas (II y X)...")
    
    # Interpretar Sección II y extraer la pista de actividades
    prompt_ii = PROMPTS_AGENTE_1["II. CARGA ACADÉMICA"]
    response_ii_raw = str(query_engine.query(prompt_ii)).strip()
    
    pista_actividad = "No identificadas"
    try:
        # Extraer la lista de actividades de la respuesta del LLM
        match = re.search(r"ACTIVIDADES_ACTIVAS:\s*\[(.*?)\]", response_ii_raw)
        if match:
            pista_actividad = match.group(1)
            # Limpiar la respuesta para el archivo de texto final
            observaciones["II. CARGA ACADÉMICA"] = re.sub(r"ACTIVIDADES_ACTIVAS:\s*\[.*?\]", "", response_ii_raw).strip()
        else:
            observaciones["II. CARGA ACADÉMICA"] = response_ii_raw
    except Exception:
        observaciones["II. CARGA ACADÉMICA"] = response_ii_raw

    print(f"Pista para Sección X identificada desde el LLM: [{pista_actividad}]")

    # Interpretar Sección X usando la pista obtenida
    prompt_x_template = PROMPTS_AGENTE_1["X. CORRESPONDENCIA CRÉDITOS UNAB"]
    prompt_x_interpretado = prompt_x_template.format(pista_actividad_activa=pista_actividad)
    observaciones["X. CORRESPONDENCIA CRÉDITOS UNAB"] = str(query_engine.query(prompt_x_interpretado)).strip()

    # --- Extracción del resto de las secciones ---
    print("Paso 2/2: Extrayendo el resto de las secciones...")
    for seccion in titulos_secciones:
        if seccion not in observaciones: # Solo procesa las que no se hicieron en el paso anterior
            response = query_engine.query(PROMPTS_AGENTE_1[seccion])
            observaciones[seccion] = str(response).strip() or "No encontrado"
    
    resultados_ordenados = [observaciones[titulo] for titulo in titulos_secciones]

    output_path = Path("./resultados/")
    output_path.mkdir(exist_ok=True)
    
    structured_content = create_structured_output_file(resultados_ordenados, titulos_secciones)
    structured_file_path = output_path / "observaciones_estructuradas.txt"
    with open(structured_file_path, "w", encoding="utf-8") as f:
        f.write(structured_content)
    print(f"Archivo de observaciones guardado en: {structured_file_path}")

    raw_content = create_raw_backup_file(documents)
    raw_file_path = output_path / "texto_bruto_completo.txt"
    with open(raw_file_path, "w", encoding="utf-8") as f:
        f.write(raw_content)
    print(f"Archivo de texto bruto guardado en: {raw_file_path}")
    
    print("--- Agente 1: Proceso completado ---")
    return structured_file_path, raw_file_path

# # agents/agent1.py

# import re
# from pathlib import Path
# import camelot
# from llama_index.core import VectorStoreIndex, Document
# from llama_index.core.node_parser import SentenceSplitter
# # from llama_index.llms.base import LLM

# # Importamos los prompts desde nuestro nuevo módulo
# from prompts.prompts_library import PROMPTS_AGENTE_1


# class HybridPDFReader:
#     def read_pdf(self, file_path: Path) -> list[Document]:
#         all_documents = []
#         page_texts = {}
#         with open(file_path, 'rb') as f:
#             from PyPDF2 import PdfReader
#             reader = PdfReader(f)
#             for page_num, page in enumerate(reader.pages):
#                 page_texts[page_num + 1] = page.extract_text() or ""
#         try:
#             tables = camelot.read_pdf(str(file_path), pages='all', flavor='lattice')
#             tables_by_page = {tbl.page: tbl.df.to_markdown(index=False) for tbl in tables}
#         except Exception as e:
#             print(f"ADVERTENCIA: Camelot no pudo procesar las tablas del PDF. Error: {e}")
#             tables_by_page = {}
            
#         for page_num, text in page_texts.items():
#             full_content = text
#             if page_num in tables_by_page:
#                 full_content += f"\n\n--- TABLA DETECTADA EN ESTA PÁGINA ---\n{tables_by_page[page_num]}"
#             all_documents.append(Document(text=full_content, metadata={"page_number": page_num, "file_name": file_path.name}))
#         return all_documents

# # def find_active_categories_from_section_ii(section_ii_text: str) -> list[str]:
# #     active_categories = []
# #     lines = section_ii_text.split('\n')
# #     possible_categories = ["Teórico", "Ayudantía", "Laboratorio", "Taller", "Terreno", "Clínico"]
# #     for line in lines:
# #         if any(char.isdigit() for char in line):
# #             for category in possible_categories:
# #                 if category in line and category not in active_categories:
# #                     active_categories.append(category)
# #     return active_categories if active_categories else ["Taller"]

# def create_structured_output_file(observaciones, titulos):
#     content = f"Extracción Estructurada del Documento\n"
#     content += "=" * 40 + "\n\n"
#     for i, (titulo, obs_text) in enumerate(zip(titulos, observaciones)):
#         content += f"---------- {i+1}. {titulo} ----------\n"
#         content += f"{obs_text}\n\n"
#     return content

# def create_raw_backup_file(documents):
#     content = "Copia de Seguridad - Texto Bruto y Tablas del PDF\n"
#     content += "=" * 50 + "\n\n"
#     for doc in documents:
#         content += f"---------- Página {doc.metadata.get('page_number', 'N/A')} ----------\n"
#         content += f"{doc.text}\n\n"
#     return content

# def run_agent_1(pdf_path: Path, llm):
#     """
#     Lógica del Agente 1: Procesa un PDF y guarda los dos archivos .txt de salida.
#     """
#     print(f"--- Iniciando Agente 1: Extracción de PDF (Modelo: {llm.model}) ---")
    
#     print(f"Leyendo el archivo: {pdf_path.name}...")
#     pdf_reader = HybridPDFReader()
#     documents = pdf_reader.read_pdf(pdf_path)
    
#     print("Creando índice de vectores (esto puede tardar un momento)...")
#     node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
#     index = VectorStoreIndex.from_documents(documents, transformations=[node_parser])
    
#     print("Ejecutando prompts de extracción...")
#     # query_engine = index.as_query_engine(similarity_top_k=10)
#     query_engine = index.as_query_engine(llm=llm, similarity_top_k=10)
#     observaciones = {}
#     titulos_secciones = list(PROMPTS_AGENTE_1.keys())

#     # # --- CÓDIGO DE RAZONAMIENTO PARA LA SECCIÓN X ---
#     # print("Paso 1/3: Analizando Sección II para obtener pistas...")
#     # section_ii_response = query_engine.query(PROMPTS_AGENTE_1["II. CARGA ACADÉMICA"])
#     # observaciones["II. CARGA ACADÉMICA"] = str(section_ii_response).strip() or "No encontrado"
#     # active_categories = find_active_categories_from_section_ii(observaciones["II. CARGA ACADÉMICA"])
#     # print(f"Pista identificada: Las actividades presenciales activas son: {', '.join(active_categories)}.")

#     # print("Paso 2/3: Extrayendo datos crudos de Sección X...")
#     # section_x_raw_response = query_engine.query(PROMPTS_AGENTE_1["X. CORRESPONDENCIA CRÉDITOS UNAB"])
    
#     # try:
#     #     print("Paso 3/3: Aplicando mapeo lógico a la Sección X...")
#     #     raw_text = str(section_x_raw_response)
#     #     numeros_str = re.search(r"NUMEROS:\s*\[(.*?)\]", raw_text).group(1)
#     #     numeros = [n.strip() for n in numeros_str.split(',')]
#     #     texto_adicional = re.search(r"TEXTO:\s*(.*)", raw_text, re.DOTALL).group(1).strip()
        
#     #     creditos_unab = numeros.pop()
#     #     personal = numeros.pop()
        
#     #     final_list = {
#     #         "Presencial - Teórico": " ", "Presencial - Ayudantía": " ", "Presencial - Laboratorio": " ",
#     #         "Presencial - Taller": " ", "Presencial - Terreno": " ", "Presencial - Clínico": " ",
#     #         "Personal": personal, "Créditos UNAB": creditos_unab
#     #     }
#     #     for i, category in enumerate(active_categories):
#     #         if i < len(numeros):
#     #             final_list[f"Presencial - {category}"] = numeros[i]

#     #     obs_x_texto = "\n".join([f"- {k}: {v}" for k, v in final_list.items()])
#     #     observaciones["X. CORRESPONDENCIA CRÉDITOS UNAB"] = f"{obs_x_texto}\n-----\nTexto adicional:\n{texto_adicional}"
#     # except (AttributeError, IndexError):
#     #     observaciones["X. CORRESPONDENCIA CRÉDITOS UNAB"] = "Error al procesar la lógica de la Sección X."
#     # --- LÓGICA DE INTERPRETACIÓN PARA SECCIONES COMPLEJAS ---
    
#     print("Paso 1/2: Interpretando secciones complejas (II y X)...")
    
#     # Interpretar Sección II
#     texto_crudo_seccion_ii = query_engine.query("Extrae el texto crudo de la sección 'II. CARGA ACADÉMICA'")
#     prompt_ii_interpretado = PROMPTS_AGENTE_1["II. CARGA ACADÉMICA"].format(texto_crudo=str(texto_crudo_seccion_ii))
#     observaciones["II. CARGA ACADÉMICA"] = str(query_engine.query(prompt_ii_interpretado)).strip()
    
#     # Usar el resultado para la pista de la Sección X
#     pista_actividad = find_active_categories_from_section_ii(observaciones["II. CARGA ACADÉMICA"])
#     print(f"Pista para Sección X identificada: {pista_actividad}")

#     # Interpretar Sección X usando la pista
#     texto_crudo_seccion_x = query_engine.query("Extrae el texto crudo de la sección 'X. CORRESPONDENCIA CRÉDITOS UNAB'")
#     prompt_x_interpretado = PROMPTS_AGENTE_1["X. CORRESPONDENCIA CRÉDITOS UNAB"].format(
#         texto_crudo=str(texto_crudo_seccion_x),
#         pista_actividad_activa=', '.join(pista_actividad)
#     )
#     observaciones["X. CORRESPONDENCIA CRÉDITOS UNAB"] = str(query_engine.query(prompt_x_interpretado)).strip()


    
#     # --- Extracción del resto de las secciones ---
#     print("Paso 2/2: Extrayendo el resto de las secciones...")
#     print("Extrayendo el resto de las secciones...")
#     for seccion in titulos_secciones:
#         if seccion not in observaciones:
#             response = query_engine.query(PROMPTS_AGENTE_1[seccion])
#             observaciones[seccion] = str(response).strip() or "No encontrado"
    
#     resultados_ordenados = [observaciones[titulo] for titulo in titulos_secciones]

#     output_path = Path("./resultados/")
#     output_path.mkdir(exist_ok=True)
    
#     structured_content = create_structured_output_file(resultados_ordenados, titulos_secciones)
#     structured_file_path = output_path / "observaciones_estructuradas.txt"
#     with open(structured_file_path, "w", encoding="utf-8") as f:
#         f.write(structured_content)
#     print(f"Archivo de observaciones guardado en: {structured_file_path}")

#     raw_content = create_raw_backup_file(documents)
#     raw_file_path = output_path / "texto_bruto_completo.txt"
#     with open(raw_file_path, "w", encoding="utf-8") as f:
#         f.write(raw_content)
#     print(f"Archivo de texto bruto guardado en: {raw_file_path}")
    
#     print("--- Agente 1: Proceso completado ---")
#     return structured_file_path, raw_file_path