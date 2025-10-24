# Agente de Planificación Curricular Unificada

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-brightgreen)](https://fastapi.tiangolo.com/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10%2B-orange)](https://www.llamaindex.ai/)

## Descripción

Este proyecto es una API web construida con **FastAPI** que automatiza la creación de una **Matriz de Planificación Curricular Unificada** a partir de programas de asignaturas en formato PDF. Utiliza una cadena de tres agentes basados en **LlamaIndex** y modelos de lenguaje grandes (LLMs) como **Gemini** (Google) o **GPT-4o** (OpenAI) para:

1. **Extraer** información estructurada del PDF (Identificación, Carga Académica, etc.).
2. **Generar** una planificación parcial con placeholders.
3. **Completar** la matriz con objetivos, indicadores, actividades y evaluaciones generadas por IA.

El resultado es un documento **Word (.docx)** descargable, listo para uso académico. Ideal para docentes y diseñadores instruccionales.

### Características Principales
- **Procesamiento de PDFs**: Extrae texto y tablas con **Camelot** y **PyPDF2**.
- **Cadena de Agentes IA**: Tres agentes secuenciales para extracción, planificación y enriquecimiento.
- **Soporte Multi-LLM**: Compatible con OpenAI y Gemini (configurable via `.env`).
- **API RESTful**: Endpoint para subir PDFs y descargar resultados.
- **Formato de Salida**: Documento Word con formato avanzado (títulos, listas, negritas).
- **CORS Habilitado**: Integrable con frontends (ej. React en localhost o Vercel).

## Requisitos Previos
- **Python 3.8+**: Descarga desde [python.org](https://www.python.org/downloads/).
- **Git**: Instala desde [git-scm.com](https://git-scm.com/downloads).
- **Cuenta en GitHub**: Crea una en [github.com](https://github.com).
- **Claves API**: Opcional, para OpenAI (`OPENAI_API_KEY`) o Google Gemini (`GOOGLE_API_KEY`).

## Configuración del Repositorio en GitHub

### 1. Inicializar Git Localmente
En tu directorio `C:\Users\johsa\Documentos\app-api`, abre PowerShell y ejecuta:

```bash
git init
git add .
git commit -m "Commit inicial: Estructura base del proyecto app-api"
```

### 2. Crear Repositorio en GitHub
- Ve a [github.com](https://github.com) e inicia sesión.
- Haz clic en **New** (o "Nuevo repositorio").
- Nombra el repositorio, por ejemplo: `app-api`.
- **No** marques "Add a README file" (ya tienes uno local).
- Elige **Público** o **Privado**.
- Haz clic en **Create repository**.
- Copia la URL (ej. `https://github.com/tu-usuario/app-api.git`).

### 3. Conectar y Subir
En PowerShell, conecta tu repositorio local a GitHub y sube:

```bash
git remote add origin https://github.com/tu-usuario/app-api.git
git branch -M main
git push -u origin main
```

Si te pide autenticación, usa tu usuario de GitHub y un **Personal Access Token** (genera uno en GitHub: Settings > Developer settings > Personal access tokens).

## Instalación del Proyecto

### 1. Clonar (Opcional, si trabajas en otra máquina)
Si necesitas clonar el repositorio en otra computadora:

```bash
git clone https://github.com/tu-usuario/app-api.git
cd app-api
```

### 2. Crear Entorno Virtual
Crea y activa un entorno virtual:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias
Instala las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:

```plaintext
OPENAI_API_KEY=tu_clave_openai_aqui
GOOGLE_API_KEY=tu_clave_gemini_aqui
```

- Asegúrate de que `.env` esté en `.gitignore` (ya incluido).
- Obtén claves en [platform.openai.com](https://platform.openai.com) o [Google Cloud Console](https://console.cloud.google.com).

### 5. Ejecutar la API
Inicia el servidor de desarrollo:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Accede a `http://localhost:8000/docs` para la documentación interactiva (Swagger UI).
- Prueba el endpoint en `http://localhost:8000/procesar-pdf/`.

## Uso de la API

### Flujo Principal
1. **Subir PDF**: Envía un programa de asignatura en PDF al endpoint `/procesar-pdf/`.
2. **Procesamiento**:
   - **Agente 1**: Extrae secciones clave (`agents/agent1.py`).
   - **Agente 2**: Genera plantilla parcial (`agents/agent2.py`).
   - **Agente 3**: Completa la matriz con IA (`agents/agent3.py`).
3. **Descarga**: Obtén un archivo `.docx` con la matriz curricular.

### Endpoint Principal
- **POST `/procesar-pdf/`**:
  - **Parámetros**:
    - `pdf` (UploadFile): PDF del programa de asignatura.
    - `consulta` (str, opcional): Instrucciones adicionales (ej. "Enfócate en unidad 1").
  - **Respuesta**: Archivo `.docx` descargable.
  - **Ejemplo con cURL**:

    ```bash
    curl -X POST "http://localhost:8000/procesar-pdf/" \
         -H "accept: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
         -F "pdf=@./data/Programa_ADSA_UCV_Def_2025.pdf" \
         -F "consulta=Genera para ingeniería" \
         --output planificacion.docx
    ```

  - **Errores**: HTTP 500 si falla (verifica logs en consola).

### Archivos Generados
En `./resultados/`:
- `observaciones_estructuradas.txt`: Datos extraídos.
- `texto_bruto_completo.txt`: Backup del texto crudo.
- `planificacion_parcial.txt`: Plantilla intermedia.
- `planificacion_final.txt`: Matriz final (texto).

## Estructura del Proyecto

```
app-api/
├── agents/                 # Lógica de los agentes IA
│   ├── agent1.py          # Extracción de PDF
│   ├── agent2.py          # Planificación parcial
│   ├── agent3.py          # Enriquecimiento con IA\
│   └── __init__.py
├── prompts/                # Prompts para LLMs
│   ├── prompts_library.py  # Definiciones de prompts
│   └── __init__.py
├── data/                   # PDFs subidos (temporal)
├── resultados/             # Archivos generados\
├── main.py                 # API FastAPI\
├── requirements.txt        # Dependencias
├── .env                    # Claves API (no versionado)
├── .gitignore              # Ignora cachés, .env, resultados
├── Dockerfile              # Para contenedores
├── comando.md              # Notas internas
├── README.md               # Este archivo
└── LICENSE                 # Licencia MIT
```

## Personalización
- **Cambiar LLM**: Edita `main.py` para usar OpenAI o Gemini (modifica `openai_llm` o `gemini_llm`).
- **Ajustar Prompts**: Modifica `prompts/prompts_library.py` para cambiar extracciones.
- **Formato Word**: Edita `create_word_document_from_text()` en `main.py` para personalizar el `.docx`.
- **Docker**: Construye una imagen para despliegue:

  ```bash
  docker build -t app-api .
  docker run -p 8000:8000 app-api
  ```

## Resolución de Problemas
- **Camelot falla**: Asegúrate de que las tablas en el PDF tengan bordes visibles ("lattice").
- **Errores de API**: Verifica claves en `.env` y conexión a internet.
- **Archivos no eliminados**: Windows puede bloquear archivos temporales; el código incluye pausas para evitarlo.
- **Errores en push**: Usa `git pull origin main --allow-unrelated-histories` si hay conflictos.

## Contribución
1. Forkea el repositorio.
2. Crea una rama: `git checkout -b feature/nueva-funcion`.
3. Commit: `git commit -m "Agrega X"`.
4. Push: `git push origin feature/nueva-funcion`.
5. Abre un Pull Request en GitHub.

Reporta bugs o ideas en los issues.

## Licencia
MIT License - ver [LICENSE](LICENSE).

## Soporte
- Contacto: Abre un issue en GitHub.
- Documentación adicional: Revisa `main.py` y `prompts/prompts_library.py`.

¡Gracias por usar este proyecto! 🚀