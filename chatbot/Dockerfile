# Usa una imagen base de Python 3.12 slim
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copiar UV desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Sincronizar dependencias con uv
RUN uv sync --locked --compile-bytecode

# Copiar todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Crear directorio para persistencia de conversaciones
RUN mkdir -p chats

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8003

# Entrypoint con uv
ENTRYPOINT ["uv", "run", "--"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
