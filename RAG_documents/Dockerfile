FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema (tesseract, poppler, compilers)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    build-essential \
    gcc && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin/:$PATH"

# Instalar UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Sincronizar dependencias con UV
RUN uv sync --locked --compile-bytecode

# Copiar código
COPY . .

# Crear directorios de persistencia
RUN mkdir -p PersistDirectory
RUN mkdir -p conversations

EXPOSE 8000

ENTRYPOINT ["uv", "run", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
