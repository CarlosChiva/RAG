# Usa la imagen correcta de Python 3.10
FROM python:3.10-slim

WORKDIR /app-front

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto en el que se ejecutará la aplicación (ajusta según sea necesario)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "front.py"]
