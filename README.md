# Agente de Planificación Curricular a partir de PDF

Este proyecto es un sistema avanzado de tres agentes diseñado para extraer, estructurar y generar contenido curricular a partir de programas de asignatura en formato PDF. El sistema automatiza la creación de una matriz de planificación curricular detallada, utilizando una cadena de razonamiento para rellenar campos que no están explícitamente en el texto.

## Arquitectura del Sistema

El sistema opera en una cadena de tres agentes secuenciales:

1.  **Agente 1 (Extractor):** Procesa el PDF de entrada, utilizando un lector híbrido para extraer tanto texto plano como la estructura de las tablas. Genera dos archivos base: `observaciones_estructuradas.txt` y `texto_bruto_completo.txt`.
2.  **Agente 2 (Estructurador):** Toma las observaciones extraídas y las utiliza para rellenar una plantilla de planificación. Deja en blanco los campos que requieren razonamiento pedagógico, marcándolos con `[PENDIENTE - AGENTE 3]`.
3.  **Agente 3 (Generador y Verificador):** Lee la planificación parcial del Agente 2. Su doble función es:
    * **Verificar:** Revisa si algún campo que debía ser extraído quedó vacío y, si es así, intenta generarlo como respaldo.
    * **Generar:** Utiliza el contexto del documento para "razonar" y crear contenido pedagógico original para todos los campos marcados como pendientes, produciendo el archivo `planificacion_final.txt`.

---

## 🚀 Tutorial de Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu propio entorno.

### **Requisitos Previos**

* **Git:** Necesitas tener Git instalado.
* **Docker:** El proyecto está completamente contenedorizado. Asegúrate de tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.

### **Paso 1: Preparación del Proyecto**

1.  **Clonar el Repositorio (si aplica):** Si estás descargando el proyecto, clónalo. Si ya tienes los archivos, continúa.

2.  **Crear Clave de API:** Dentro de la carpeta del proyecto, crea un archivo llamado `api_key.py` y añade tu clave de API de OpenAI:
    ```python
    # api_key.py
    key = "sk-..."
    ```
    > **⚠️ Advertencia:** El archivo `.gitignore` está configurado para **NUNCA** subir `api_key.py` a GitHub. Mantén tu clave siempre en privado.

3.  **Añadir un PDF:** Coloca el archivo PDF que deseas procesar dentro de la carpeta `data`.

### **Paso 2: Construir la Imagen de Docker**

Este comando debe ejecutarse **una sola vez** (o cada vez que modifiques el código).

1.  Abre una terminal (PowerShell o cmd).
2.  Navega a la carpeta de tu proyecto.
3.  Ejecuta el comando:
    ```bash
    docker build -t pdf-app .
    ```

### **Paso 3: Ejecutar la Cadena de Agentes**

Este es el comando que usarás cada vez que quieras procesar un PDF.

1.  Abre una terminal en la carpeta del proyecto.
2.  Ejecuta el comando correspondiente, reemplazando `"data/nombre_de_tu_archivo.pdf"` con la ruta a tu archivo.

    **En PowerShell:**
    ```powershell
    docker run -v ${PWD}:/app pdf-app python -u main.py "data/nombre_de_tu_archivo.pdf"
    ```

    **En Símbolo del sistema (cmd):**
    ```cmd
    docker run -v %cd%:/app pdf-app python -u main.py "data/nombre_de_tu_archivo.pdf"
    ```

### **Paso 4: Revisar los Resultados**

Una vez que el script finalice, revisa la carpeta `./resultados`. Encontrarás los tres archivos generados:
* `observaciones_estructuradas.txt`
* `texto_bruto_completo.txt`
* `planificacion_final.txt`

---

## 📂 Estructura del Proyecto

📂 pdf-app\
┣ 📂 agents\
┃   ┣ agent1.py\
┃   ┣ agent2.py\
┃   ┣ agent3.py\
┣ 📂 data\
┃   ┣ (Aquí van tus PDFs)\
┣ 📂 prompts\
┃   ┣ prompts_library.py\
┣ 📂 resultados\
┃   ┣ (Aquí se guardan los .txt generados)\
┣ .gitignore\
┣ api_key.py\
┣ Dockerfile\
┣ main.py\
┣ README.md\
┣ requirements.txt\
