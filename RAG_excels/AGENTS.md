# API RAG para Excels

Esta API implementa un sistema RAG (Retrieval-Augmented Generation) para análisis y gestión de archivos Excel usando LLMs locales (Ollama) con LangGraph. Permite subir, consultar y editar archivos Excel mediante un agente autónomo con herramientas especializadas.

## Arquitectura

La API sigue un patrón MVC modificado con las siguientes capas:

## Subcarpetas

- **`controllers/`**: Lógica de negocio para CRUD de archivos y validación de JWT.  
  → [Ver documentación detallada](./controllers/AGENTS.md)

- **`models/`**: Definición del agente LLM, herramientas para Excel y gestión de sesiones de usuario.  
  → [Ver documentación detallada](./models/AGENTS.md)

- **`routes/`**: Endpoints REST y WebSocket de la API FastAPI.  
  → [Ver documentación detallada](./routes/AGENTS.md)

- **`services/`**: Servicios de bajo nivel para carga de Excel, creación de vector stores y orquestación de sesiones.  
  → [Ver documentación detallada](./services/AGENTS.md)

- **`backups_excel/`**: Directorio para backups automáticos antes de ediciones (archivos generados).

## Archivos de Configuración

- **`main.py`**: Punto de entrada de la aplicación FastAPI. Configura CORS (origen: `http://localhost:4200`), monta el router y inicia el servidor con uvicorn.

- **`pyproject.toml`**: Definición del proyecto con dependencias (FastAPI, LangChain, LangGraph, Ollama, FAISS, Pandas, OpenPyXL, Unstructured, PyJWT).

- **`Dockerfile`**: Imagen de contenedor basada en `python:3.12-slim-trixie` con UV para gestión de dependencias. Expone puerto 8004.

- **`.env`**: Variables de entorno sensibles (SECRET_KEY, ALGORITHM, EMBEDDING_MODEL, USER_FOLDERS).

- **`.python-version`**: Especifica la versión de Python requerida (3.12+).

- **`uv.lock`**: Archivo de bloqueo de dependencias generado por UV para instalaciones reproducibles.

- **`README.md`**: Documentación general del proyecto.

## Flujo de Ejecución

1. **Autenticación**: Cliente envía JWT en header `Authorization: Bearer <token>` → `credentials_controllers.verify_jws()` valida el token → Extrae `user_id` del claim `sub`.

2. **Gestión de Archivos**:
   - **Upload**: `POST /upload_file` → `upload_file_controller()` → Guarda en `{USER_FOLDERS}/{user_id}/{filename}`.
   - **List**: `GET /list_files` → `list_files_controller()` → Lista archivos del directorio del usuario.
   - **Download**: `GET /get_file` → `get_file_controller()` → Retorna FileResponse.
   - **Delete**: `DELETE /delete_file` → `remove_file()` → Elimina archivo del disco.

3. **Consultas LLM**:
   - Cliente conecta a `WS /llm-query` → `websocket_handler()` acepta conexión.
   - Cliente envía JSON: `{auth: JWT, input: pregunta, file_name: nombre_archivo}`.
   - `verify_jws(auth)` valida JWT → Extrae `user_id`.
   - `ExcelAgent.query()` verifica/crea `UserSession` para ese `user_id` + `file_path`.
   - `UserSession.query_agent()` ejecuta el agente LangGraph con streaming.
   - El agente (`models.agent.Agent`) usa herramientas (`models.tools`) para:
     - Explorar estructura del Excel (`explorar_excel`).
     - Buscar semánticamente (`buscar_en_excel`).
     - Filtrar por criterios (`buscar_por_filtro`).
     - Consultas complejas (`consulta_libre_excel`).
     - Editar celdas con backup automático (`editar_excel`).
   - Respuestas se streaman por WebSocket en chunks: tool calls, reasoning, y contenido final.

## Herramientas del Agente

El agente tiene 6 herramientas disponibles:

| Herramienta | Propósito |
|-------------|-----------|
| `explorar_excel` | Obtener estructura completa del archivo (hojas, dimensiones, columnas, tipos) |
| `buscar_en_excel` | Búsqueda semántica usando embeddings FAISS |
| `buscar_columna` | Encontrar columnas por nombre con estadísticas |
| `buscar_por_filtro` | Filtrar filas por criterios estructurados (igual, contiene, mayor, menor) |
| `consulta_libre_excel` | Consulta libre combinando búsqueda semántica + análisis estructural + estadísticas |
| `editar_excel` | Editar celda específica con confirmación obligatoria y backup automático |

## Tecnologías Clave

- **Backend**: FastAPI + Uvicorn
- **LLM**: Ollama (modelo `gpt-oss` con razonamiento habilitado)
- **Framework de Agentes**: LangGraph con MemorySaver checkpointing
- **Vector Store**: FAISS con embeddings de Ollama
- **Procesamiento Excel**: Pandas + OpenPyXL + Unstructured
- **Autenticación**: JWT (PyJWT) con algoritmo HS256
- **Comunicación**: REST + WebSocket streaming
- **Contenerización**: Docker + UV (gestor de paquetes Python)
