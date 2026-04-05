# REQUISITOS DE MIGRACIÓN A UV

## Objetivo
Migrar 5 microservicios Python de pip/requirements.txt a UV como gestor de paquetes para mejorar velocidad y reproducibilidad.

## Microservicios a Migrar
1. RAG_documents
2. RAG_ddbb
3. RAG_excels
4. RAG_multimedia
5. chatbot

## Estrategia de Migración
- Usar `uv sync` con `uv.lock` para reproducibilidad
- Mantener requirements.txt temporalmente como fallback
- Usar última versión estable de UV (0.5.x)

## Tareas por Servicio

### A. Crear uv.lock en cada servicio
Para cada microservicio Python:
1. Leer el requirements.txt existente
2. Ejecutar: `uv lock -r requirements.txt` (genera uv.lock)
3. Verificar que uv.lock fue creado exitosamente

### B. Actualizar cada Dockerfile
Cambiar la estrategia de instalación de pip a UV optimizada:
```dockerfile
# ANTES
COPY requirements.txt .
RUN pip install -r requirements.txt

# DESPUÉS - Instalación UV optimizada
# Instalar UV
COPY --from=ghcr.io/astral-sh/uv:0.5.x /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:0.5.x /uvx /bin/uvx

# Copiar y generar lock
COPY requirements.txt .
RUN uv pip install -r requirements.txt --system || true

# Copiar lock file y sincronizar
COPY uv.lock .
RUN uv sync --frozen --no-dev
```

## Criterios de Aceptación
1. ✅ Lista de servicios con uv.lock creados
2. ✅ Lista de Dockerfiles actualizados
3. ✅ PROJECT_STATE.md generado
4. ✅ Sin errores en la migración
5. ✅ Resumen de cambios realizados

## Archivos Objetivo
- /home/dread/VsCode/RAG/RAG_documents/
- /home/dread/VsCode/RAG/RAG_ddbb/
- /home/dread/VsCode/RAG/RAG_excels/
- /home/dread/VsCode/RAG/RAG_multimedia/
- /home/dread/VsCode/RAG/chatbot/
