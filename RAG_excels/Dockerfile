FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --locked --compile-bytecode
EXPOSE 8004
CMD ["uv", "run", "--","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]