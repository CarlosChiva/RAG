# Usa una imagen base de Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]