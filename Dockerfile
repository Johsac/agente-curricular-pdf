# Dockerfile

# Usar imagen base de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (para Camelot)
RUN apt-get update && apt-get install -y ghostscript libopencv-dev && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto al contenedor
COPY . .

# Exponer el puerto 8000, que es el puerto por defecto de Uvicorn/FastAPI
EXPOSE 8000

# Comando para iniciar el servidor de la API
# Ejecuta el servidor 'uvicorn', apuntando al objeto 'app' dentro del archivo 'api/main.py'
# --host 0.0.0.0 permite que la API sea accesible desde fuera del contenedor
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Comando para correr la app (ajusta 'app.py' si tu archivo se llama diferente)
#CMD ["streamlit", "run", "app.py"]