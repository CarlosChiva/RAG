FROM python:3.12

WORKDIR /app

# Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev

# Copiar UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Sincronizar dependencias con uv
RUN uv sync --frozen --compile-bytecode || (uv lock && uv sync --compile-bytecode)

# Copiar código fuente
COPY . .

# Expone el puerto
EXPOSE 8002

# Entrypoint y CMD con uv
ENTRYPOINT ["uv", "run", "--"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
