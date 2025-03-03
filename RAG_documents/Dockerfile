# Usa una imagen base de Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias necesarias para pytesseract
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev poppler-utils

# Configura el PATH para que pueda encontrar Tesseract
ENV PATH="/usr/bin/:$PATH"

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pdfplumber[poppler]
# Copia todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Crea el directorio PersistDirectory si no existe
RUN mkdir -p PersistDirectory
RUN mkdir -p conversations


# Expone el puerto en el que se ejecutará la aplicación (ajusta según sea necesario)
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]