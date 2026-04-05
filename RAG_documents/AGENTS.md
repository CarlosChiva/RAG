# API RAG Documents - Sistema de Chatbot con Retrieval-Augmented Generation

Esta aplicación implementa un chatbot RAG (Retrieval-Augmented Generation) que responde preguntas basándose en documentos PDF/DOCX/TXT cargados por el usuario, utilizando LangChain, ChromaDB y Ollama para generación de respuestas contextualizadas.

## Resumen Ejecutivo

API FastAPI que permite:
- Carga de documentos multi-formato con extracción avanzada de texto, tablas e imágenes (OCR)
- Búsqueda semántica mediante embeddings y base de datos vectorial ChromaDB
- Respuestas en tiempo real vía WebSocket con historial de conversaciones
- Aislamiento de datos por usuario mediante autenticación JWT

---

## Subcarpetas

- **`controllers/`**: Lógica de negocio para gestión de documentos, consultas RAG y persistencia de conversaciones.  
  → [Ver documentación detallada](./controllers/AGENTS.md)

- **`db/`**: Capa de datos con integración ChromaDB, procesamiento de PDF con OCR, chunking de texto y configuración de modelos LLM.  
  → [Ver documentación detallada](./db/AGENTS.md)

- **`routes/`**: Definición de endpoints HTTP y WebSocket con autenticación JWT obligatoria.  
  → [Ver documentación detallada](./routes/AGENTS.md)

---

## Archivos de Configuración

### `main.py`
**Propósito:** Punto de entrada de la aplicación FastAPI.

**Componentes principales:**
- **Configuración:**
  - Middleware CORS para origen `http://localhost:4200` (frontend Angular)
  - Router montado desde `routes.routes`
  - Logging en nivel DEBUG

- **Inicialización:**
  ```python
  app = FastAPI()
  app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"], ...)
  app.include_router(router)
  ```

**Dependencias:** `fastapi`, `uvicorn`, `fastapi.middleware.cors`

**Ejecución:** `uvicorn main:app --host 0.0.0.0 --port 8000`

---

### `requirements.txt`
**Propósito:** Dependencias legacy del proyecto (mantenido como fallback).

**Paquetes principales:**
- **Total:** 166 dependencias
- **Framework:** `fastapi==0.115.9`, `uvicorn==0.30.6`, `python-multipart`
- **RAG/LangChain:** `langchain==0.3.26`, `langchain-chroma==0.2.4`, `langchain-ollama==0.3.3`
- **Base de datos vectorial:** `chromadb==1.0.12`, `chroma-hnswlib==0.7.6`
- **Procesamiento de documentos:** `pdfplumber==0.10.2`, `PyPDF2==3.0.1`, `pdfminer.six`, `python-docx==1.1.2`, `pytesseract==0.3.10`
- **OCR/Imágenes:** `Pillow==10.4.0`, `pdf2image==1.16.3`
- **Autenticación:** `PyJWT==2.10.1`, `bcrypt==4.2.0`
- **Modelos:** `ollama==0.5.1`, `huggingface-hub==0.24.5`
- **Utilidades:** `python-dotenv==1.0.1`, `pydantic==2.11.5`

**Corrección migración UV:** Verificado pdfplumber (sin cambios necesarios) - poppler ya es dep del sistema  
**Instalación:** ⚠️ Obsoleto - Migrado a `pyproject.toml` + `uv.lock`

---

### `pyproject.toml`
**Propósito:** Configuración del proyecto en formato PYPA moderno (reemplaza requirements.txt).

**Configuración:**
- **name:** `rag-documents`
- **version:** `0.1.0`
- **requires-python:** `>=3.12`
- **dependencias:** 166 declaradas
- **Generado:** abril 2026

---

### `uv.lock`
**Propósito:** Lockfile generado por UV para reproducibilidad de builds.

**Detalles:**
- **Tamaño:** `342 KB`
- **Paquetes resueltos:** ~170 directos + ~613 transitive (783 multi-platforma)
- **Hash:** SHA256 para builds idénticos
- **Generado:** abril 2026

---

### `Dockerfile`
**Propósito:** Contenedorización de la aplicación para despliegue en producción con UV strategy.

**Configuración:**
- **Imagen base:** `python:3.10-slim`
- **Gestor de paquetes:** **UV** (migrado de pip en abril 2026) ✅
- **Estrategia:** `uv sync --locked --compile-bytecode`
- **Corrección migración UV:** Consolidado 2 `pip install` → 1 `uv sync` ⚠️
- **Dependencias del sistema:** `tesseract-ocr`, `libtesseract-dev`, `poppler-utils` (para OCR y procesamiento PDF)
- **Directorio de trabajo:** `/app`
- **Puerto expuesto:** `8000`
- **Entrypoint:** `["uv", "run", "--"]` (UV wrapper)
- **SIZE:** `1.88 GB` (imagen grande por dependencias ML/OCR)

**Directorios creados:**
- `/app/PersistDirectory`: Persistencia de ChromaDB por usuario
- `/app/conversations`: Almacenamiento de historiales de chat (JSON)

**Build:** `docker build -t rag-documents:uv-test .`  
**Run:** `docker run -p 8000:8000 rag-documents:uv-test`

---

### `.env`
**Propósito:** Variables de entorno confidenciales (no commitado a Git).

**Variables requeridas:**
- `PERSIST_DIRECTORY`: Ruta de persistencia ChromaDB (default: `"PersistDirectory"`)
- `MODEL`: Nombre del modelo LLM en Ollama (default: `"llama3.2"`)
- `EMBEDD_MODEL`: Modelo de embeddings (default: `"bge-m3:latest"`)
- `SECRET_KEY`: Clave secreta para firma JWT
- `ALGORITHM`: Algoritmo JWT (default: `"HS256"`)
- `PATH_CONVERSATIONS`: Ruta archivo historiales (default: `"/app/conversations/conversations.json"`)

---

### `README.md`
**Propósito:** Documentación pública de la API con descripción de endpoints, autenticación y ejemplos de uso.

**Contenido:**
- Overview del sistema
- Instrucciones de autenticación JWT
- Documentación de 5 endpoints principales
- Variables de entorno
- Comandos Docker y Docker Compose
- Requisitos del sistema
- Guía de uso paso a paso

---

## Arquitectura General

```
┌─────────────┐
│   Cliente   │ (Frontend Angular / Postman / WebSocket client)
└──────┬──────┘
       │ HTTP/WS + JWT
       ↓
┌─────────────┐
│  FastAPI    │── main.py (CORS, router mount)
│  (Port 8000)│
└──────┬──────┘
       │
       ↓
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   routes/   │────→ │ controllers/│────→ │      db/    │
│  (Endpoints)│      │  (Lógica)   │      │ (ChromaDB + │
└─────────────┘      └─────────────┘      │  Ollama +   │
                                          │  PDF tools)  │
                                          └─────────────┘
                                               │
                                               ↓
                                        ┌─────────────┐
                                        │  ChromaDB   │ (Persistencia por usuario)
                                        │  Ollama LLM │ (Generación de respuestas)
                                        └─────────────┘
```

---

## Flujo de Operación Típico

1. **Autenticación:** Usuario obtiene JWT desde endpoint `/log-in` (en otro servicio `ddb`)
2. **Carga de documentos:** `POST /add_document` con archivo PDF → procesamiento con OCR → embeddings → ChromaDB
3. **Consulta:** `WS /llm-response` con pregunta + colección → retrieval MMR (k=3) → LangChain con historial → streaming respuesta
4. **Persistencia:** Conversación guardada en `conversations.json` por usuario y colección
5. **Gestión:** Listado/eliminación de colecciones vía `GET /collections` y `POST /delete-collection`

---

## Consideraciones Técnicas

- **Aislamiento multi-usuario:** Cada usuario tiene directorio `{PERSIST_DIRECTORY}/{username}/` en ChromaDB
- **Streaming en tiempo real:** WebSocket emite fragmentos de texto mientras el LLM genera
- **Historial de conversaciones:** Contexto completo pasado al LLM para respuestas coherentes
- **Chunking inteligente:** `RecursiveCharacterTextSplitter` con tokenizador tiktoken (1000 tokens, 20% overlap)
- **Retrieval MMR:** Balance entre relevancia y diversidad de documentos recuperados
- **OCR automático:** Tablas e imágenes en PDF procesadas con Tesseract
