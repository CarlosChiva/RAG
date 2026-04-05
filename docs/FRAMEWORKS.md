# Frameworks - RAG Project

## Frameworks

### Backend
- **FastAPI** (Python 3.10-3.12) - Framework principal para todas las APIs
- **LangChain** - Framework para RAG y agentes LLM
- **LangGraph** - Orquestación de agentes (RAG_excels, chatbot)
- **Ollama** - LLM local (llama3.2, gpt-oss, bge-m3)
- **PyJWT** - Autenticación JWT (HS256)
- **bcrypt** - Hash de contraseñas
- **SQLAlchemy** - ORM para bases de datos
- **ChromaDB** - Vector database para RAG_documents
- **FAISS** - Vector store para RAG_excels
- **Pandas** - Manipulación de datos Excel
- **OpenPyXL** - Lectura/escritura Excel
- **pdfplumber** - Extracción de PDF
- **pytesseract** - OCR para documentos
- **python-multipart** - Upload de archivos
- **Uvicorn** - ASGI server

### Frontend
- **Angular** 19.2.0 - Framework principal
- **TypeScript** 5.7.2 - Lenguaje
- **RxJS** - Reactive programming
- **marked** - Markdown rendering
- **prismjs** - Syntax highlighting
- **HttpClient** - HTTP requests
- **WebSocket** - Streaming en tiempo real

### Base de Datos
- **MySQL** 8.0 - Base de datos principal (users, services)
- **PostgreSQL** - Soporte en RAG_ddbb
- **SQLite** - Soporte en RAG_ddbb

### DevOps
- **Docker** - Contenerización
- **docker-compose** - Orquestación de contenedores
- **uv** - Package manager (✅ MIGRACIÓN COMPLETADA)
  - **RAG_excels:** ✅ Migrado (17 deps, 253ms build)
  - **RAG_documents:** ✅ Migrado (166 deps, 342KB lock, 1.88GB imagen)
  - **RAG_ddbb:** ✅ Migrado (66 deps, 116 paq instalados, 1.84GB imagen)
  - **RAG_multimedia:** ✅ Migrado (6 deps, 193MB imagen)
  - **chatbot:** ✅ Migrado (72 deps, 78 paq resueltos, 402MB imagen)
- **pip:** Package manager legacy (DEPRECATo - migrado a UV)

### Servicios Externos
- **ComfyUI** - Generación de imágenes (chatbot)
- **MCP (Model Context Protocol)** - Agentes externos (chatbot)

### Variables de Entorno Comunes
- `SECRET_KEY` - Clave secreta para firma JWT (compartida entre servicios)
- `ALGORITHM` - Algoritmo JWT (HS256)
- `EMBEDD_MODEL` - Modelo de embeddings para RAG
- `MODEL` / `SQL_MODEL` - Modelo LLM para generación de respuestas
- `DB_HOST`, `DB_USER`, `DB_PASSWORD` - Credenciales MySQL
