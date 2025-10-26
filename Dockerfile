# --- Imagen base ---
FROM python:3.11-slim

# --- Configuración de entorno ---
ENV PYTHONDONTWRITEBYTECODE=1   
ENV PYTHONUNBUFFERED=1          

# --- Crear directorio de la app ---
WORKDIR /app

# --- Copiar requirements si los hay ---
COPY requirements.txt .

# --- Instalar dependencias ---
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- Copiar todo el proyecto ---
COPY . .

# --- Exponer puerto de Flask ---
EXPOSE 5000

# --- Comando por defecto para correr la app ---
CMD ["python", "app.py"]
