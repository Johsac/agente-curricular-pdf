# Usar imagen base de Python 3.12 slim (ligera, ~100MB)
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Camelot y OpenCV (sin extras)
RUN apt-get update && apt-get install -y \
    ghostscript \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt (crearemos este archivo a continuación)
COPY requirements.txt .

# Instalar dependencias Python (solo lo necesario)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app y otros archivos
COPY . .

# Exponer puerto para Streamlit (8501)
EXPOSE 8501

# Comando para correr la app (ajusta 'app.py' si tu archivo se llama diferente)
CMD ["streamlit", "run", "app.py"]