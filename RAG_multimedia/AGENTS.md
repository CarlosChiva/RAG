# API RAG Multimedia

API FastAPI para gestión de videos con RAG (Retrieval-Augmented Generation). Permite subir, consultar y analizar archivos de video usando LLMs locales (Ollama) con LangGraph.

**Puerto:** 8006

**Tecnologías:** FastAPI, LangGraph, Ollama, PyJWT, aiofiles

**Funcionalidades:**
- Upload, list, download, delete de archivos de video
- Consultas LLM vía WebSocket con streaming
- Aislamiento multi-usuario con JWT
- Almacenamiento intercambiable (LocalStorage implementado)

---

## Subcarpetas

- **`api/`**: Endpoints REST y dependencias de inyección para la API.  
  → [Ver documentación detallada](./api/AGENTS.md)

- **`conversations/`**: Carpeta para persistencia de historiales de conversaciones (actualmente vacía - en desarrollo).

- **`core/`**: Componentes fundamentales del sistema (configuración, autenticación JWT, almacenamiento).  
  → [Ver documentación detallada](./core/AGENTS.md)

- **`models/`**: Esquemas Pydantic para validación de datos.  
  → [Ver documentación detallada](./models/AGENTS.md)

- **`storage/`**: Directorio de almacenamiento físico de videos (estructura: `/videos/{user_id}/{file_id}`).

---

## Archivos de Configuración

- **`main.py`**: Punto de entrada de la aplicación FastAPI.
  - Configura CORS para `http://localhost:4200` (Frontend Angular)
  - Incluye router de rutas con prefix `/api`
  - Endpoints: `GET /` (info del servicio), `GET /health` (health check)
  - Ejecución: `uvicorn main:app --host 0.0.0.0 --port 8006`

- **`Dockerfile`**: Configuración de contenedor Docker.
  - Imagen base: `python:3.12-slim`
  - Crea directorios: `/app/storage/videos`, `/app/conversations`
  - Expone puerto `8006`
  - CMD: `uvicorn main:app --host 0.0.0.0 --port 8006`

- **`requirements.txt`**: Dependencias Python del proyecto.
  - `fastapi==0.115.9`, `uvicorn==0.30.6`, `python-multipart==0.0.12`
  - `PyJWT==2.10.1`, `python-dotenv==1.0.1`, `aiofiles`

- **`.env`**: Variables de entorno de ejemplo.
  - `SECRET_KEY`, `ALGORITHM=HS256`, `STORAGE_PATH=/app/storage/videos`
  - `CONVERSATIONS_PATH=/app/conversations`, `PORT=8006`

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│              Frontend (video player + chat)                 │
│  - Upload videos - List videos - Chat con contexto video   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/WS + JWT
                            ↓
┌───────────────────────────▼─────────────────────────────────┐
│  API Multimedia RAG (Port 8006)                             │
│  - /upload-video (multipart/form-data)                      │
│  - /videos (list)                                           │
│  - /videos/{id} (download/delete)                          │
│  - /conversations (list)                                    │
│  - /chat (WebSocket)                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  LocalStorage │  │  LangGraph    │  │    Ollama     │
│  - Upload     │  │  - Agent      │  │  - gpt-oss     │
│  - Download   │  │  - Tools      │  │  - llama3.2    │
│  - Delete     │  │  - Chat       │  │  - bge-m3      │
│  - List       │  │  - Memory     │  └───────────────┘
└───────────────┘  └───────────────┘
```

---

## Flujo de Autenticación

1. **Login:** Frontend → `ddbb:/log-in` → JWT token
2. **Acceso:** JWT incluido en header `Authorization: Bearer <token>` en todas las peticiones
3. **Validación:** `credentials_controllers.verify_jws()` valida JWT antes de procesar requests
4. **Aislamiento:** Cada usuario tiene directorio propio en `/app/storage/videos/{user_id}/`

---

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta para firma JWT (obligatoria) | - |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `STORAGE_PATH` | Path base para almacenamiento de videos | `/app/storage/videos` |
| `CONVERSATIONS_PATH` | Path para persistencia de conversaciones | `/app/conversations` |
| `PORT` | Puerto del servidor | `8006` |
| `ALLOWED_HOSTS` | Hosts permitidos (coma-separated) | `*` |

---

## Formatos de Video Soportados

- `.mp4` (video/mp4)
- `.webm` (video/webm)
- `.mov` (video/quicktime)
- `.avi` (video/x-msvideo)
- `.mkv` (video/x-matroska)
- `.flv` (video/x-flv)
- `.wmv` (video/x-ms-wmv)
- `.m4v` (video/x-m4v)
- `.mpeg/.mpg` (video/mpeg)
- `.3gp/.3g2` (video/3gpp/3gpp2)
- `.ogv` (video/ogg)
- `.mxf` (video/mxf)
- `.vob` (video/x-ms-vob)
- `.asf` (video/ms-asf)
- `.amv` (video/x-ms-amv)
