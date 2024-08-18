# Usa una imagen base de Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Crea el directorio PersistDirectory si no existe
RUN mkdir -p PersistDirectory

# Expone el puerto en el que se ejecutará la aplicación (ajusta según sea necesario)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]