# Usa una imagen base de Python 3.10
FROM python:3.12
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev
RUN pip install psycopg2-binary
RUN pip install psycopg2    
# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
# Copia todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación (ajusta según sea necesario)
EXPOSE 8002

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]