# Project Structure - RAG

## Current Project Overview
RAG (Retrieval-Augmented Generation) system with multiple microservices.

## Schema of project

### A.1 Estructura General del Proyecto

```
/home/dread/VsCode/RAG/
├── AGENTS.md                    # Documentación principal del proyecto
├── docker-compose.yml           # Orquestación de contenedores (7 servicios)
├── README.md                    # Documentación pública
├── docs/                        # Documentación técnica (REQUIREMENTS.md, FRAMEWORKS.md, PROJECT_STRUCTURE.md)
├── images/                      # Assets estáticos
├── .vscode/                     # Configuración VS Code
│
├── mysql/                       # 🔹 Base de datos MySQL
│   ├── .env                     # Credenciales MySQL
│   └── init.sql                 # Esquema de tablas (users, services)
│
├── ddbb/                        # 🔹 API de Autenticación y Gestión de Servicios (Puerto 8001)
│   ├── main.py                  # FastAPI app + CORS
│   ├── Dockerfile               # python:3.10-slim
│   ├── .env                     # DB_HOST, DB_USER, DB_PASSWORD, SECRET_KEY, ALGORITHM
│   ├── requirements.txt         # fastapi, mysql-connector-python, PyJWT, bcrypt
│   ├── controllers/             # Lógica de negocio (controllers.py, credentials_controllers.py, mysql_manager.py)
│   └── routes/                  # Endpoints (routes.py)
│
├── RAG_documents/               # 🔹 API RAG PDF (Puerto 8000)
│   ├── main.py                  # FastAPI app + CORS
│   ├── Dockerfile               # python:3.10-slim + tesseract-ocr
│   ├── .env                     # PERSIST_DIRECTORY, MODEL, EMBEDD_MODEL, SECRET_KEY
│   ├── requirements.txt         # fastapi, langchain, chromadb, pdfplumber, pytesseract
│   ├── controllers/             # Gestión de documentos y conversaciones
│   ├── db/                      # ChromaDB, PDF processing, OCR
│   ├── routes/                  # Endpoints HTTP + WebSocket
│   ├── PersistDirectory/        # Volumen Docker para ChromaDB
│   └── conversations/           # Volumen Docker para JSON de chats
│
├── RAG_ddbb/                    # 🔹 API RAG Text-to-SQL (Puerto 8002)
│   ├── main.py, Dockerfile, .env, requirements.txt
│   ├── controllers/, routes/, db/
│   └── configs_folder/          # Volumen Docker para configs JSON
│
├── RAG_excels/                  # 🔹 API RAG Excel (Puerto 8004)
│   ├── main.py                  # FastAPI app + CORS
│   ├── Dockerfile               # python:3.12-slim-trixie + uv
│   ├── .env                     # SECRET_KEY, USER_FOLDERS, EMBEDDING_MODEL
│   ├── pyproject.toml           # Dependencias (FastAPI, LangGraph, Ollama, FAISS, Pandas)
│   ├── controllers/             # CRUD de archivos, JWT validation
│   ├── models/                  # Agente LLM con 6 herramientas
│   ├── routes/                  # Endpoints HTTP + WebSocket
│   ├── services/                # Excel loader, vector store
│   └── backups_excel/           # Backups automáticos
│
├── chatbot/                     # 🔹 API Chatbot General (Puerto 8003)
│   ├── main.py                  # FastAPI app + CORS (origen: *)
│   ├── dockerfile               # python:3.12
│   ├── .env                     # SECRET_KEY, PATH_CONVERSATIONS, PATH_CONFIGS, SERVER_ADDRESS
│   ├── requirements.txt         # fastapi, langgraph, langchain-ollama, langchain-mcp-adapters
│   ├── controllers/             # Orquestación, gestión de chats
│   ├── routes/                  # Endpoints HTTP + WebSocket
│   ├── services/                # LangGraph graph, Ollama integration, nodes (chat, image, MCP)
│   └── chats/                   # Volumen Docker para JSON de conversaciones
│
└── front/                       # 🔹 Frontend Angular 19.2.0 (Puerto 4200)
    ├── package.json             # Angular 19.2.0, TypeScript 5.7.2, marked, prismjs
    ├── angular.json             # Configuración CLI
    ├── Dockerfile               # node:18-alpine
    ├── tsconfig.json            # TypeScript config
    └── src/
        ├── main.ts              # Punto de entrada
        ├── index.html           # Template principal
        ├── styles.scss          # Estilos globales (gradiente oscuro)
        └── app/
            ├── app.component.ts # Componente raíz
            ├── app.config.ts    # Providers (router, HTTP, animations)
            ├── app.routes.ts    # 6 rutas (login, menu, pdf, ddbb, chatbot, excel)
            ├── screens/         # 6 pantallas (login, menu, rag_pdf, rag_ddbb, chatbot, excels)
            ├── components/      # 18 componentes reutilizables
            ├── services/        # 5 servicios (auth, collections, ddbb, excel, models)
            ├── interfaces/      # 6 interfaces TypeScript
            ├── guards/          # auth.guard.ts
            └── interceptors/    # auth.interceptor.ts
```

### A.2 Microservicios Existentes y Puertos

| Servicio | Puerto | Imagen Base | Descripción |
|----------|--------|-------------|-------------|
| **front** | 4200 | node:18-alpine | Frontend Angular |
| **ddb** | 8001 | python:3.10-slim | API de autenticación y gestión de servicios |
| **RAG_documents** | 8000 | python:3.10-slim | API RAG PDF con ChromaDB |
| **RAG_ddbb** | 8002 | python:3.12-slim | API RAG Text-to-SQL |
| **RAG_excels** | 8004 | python:3.12-slim-trixie | API RAG Excel con LangGraph |
| **chatbot** | 8003 | python:3.12 | API Chatbot con ComfyUI + MCP |
| **mysql (db)** | 3306 | mysql:8.0 | Base de datos MySQL |

### A.3 Tecnologías por Módulo

| Módulo | Backend | Frontend | Base de Datos | IA/LLM |
|--------|--------|----------|---------------|--------|
| **ddb** | FastAPI | - | MySQL | - |
| **RAG_documents** | FastAPI | - | ChromaDB | Ollama (llama3.2, bge-m3) |
| **RAG_ddbb** | FastAPI | - | PostgreSQL/MySQL/SQLite | Ollama |
| **RAG_excels** | FastAPI | - | FAISS | Ollama (gpt-oss) |
| **chatbot** | FastAPI | - | JSON files | Ollama + ComfyUI + MCP |
| **front** | - | Angular 19.2.0 | - | - |

### B. Patrones de Código Clave

#### B.1 Backend FastAPI - Autenticación JWT

**Patrón implementado en `ddb/controllers/credentials_controllers.py`:**
- SECRET_KEY y ALGORITHM compartidos entre todos los servicios
- Generación de token con `jwt.encode()` usando password_hash como subject
- Validación de token en cada request (HTTP o WebSocket)
- Para WebSocket, el token se envía en el payload JSON: `{"auth": "Bearer <token>", ...}`

#### B.2 Backend FastAPI - Estructura de Rutas

**Patrón común:**
- main.py con FastAPI + CORS middleware (allow_origins: http://localhost:4200)
- routes/routes.py con APIRouter y endpoints protegidos con `Depends(credentials_controllers.verify_jws)`

#### B.3 Backend - Almacenamiento de Archivos

**Patrón de RAG_documents:** ChromaDB por usuario → `{PERSIST_DIRECTORY}/{username}/`
**Patrón de RAG_excels:** Archivos por usuario → `{USER_FOLDERS}/{user_id}/`

**Recomendación para Multimedia:** Usar el mismo patrón que RAG_excels (carpeta por usuario) con interfaz abstracta para storage (local/cloud)

#### B.4 Frontend Angular - Patrones de Screens

**Estructura típica:**
- Standalone components (sin NgModules)
- ViewChild para comunicación con componentes hijos
- WebSocket streaming con marcador `__END__`
- Markdown rendering con `marked` + `DomSanitizer`

#### B.5 Frontend Angular - Servicios

**Patrón de servicio:**
- Injectable con `providedIn: 'root'`
- URLs HTTP y WebSocket configuradas
- Método `getHeaders()` que obtiene token de localStorage
- Observables para REST y WebSocket

#### B.6 Docker - Patrones

**Dockerfile típico (Python):**
- FROM python:3.12-slim
- WORKDIR /app
- COPY requirements.txt + pip install
- COPY . .
- mkdir directorios de persistencia
- EXPOSE puerto
- CMD uvicorn main:app

**docker-compose.yml:**
- network_mode: host
- volumes para persistencia
- env_file por servicio

### C. Puntos de Integración

#### C.1 Dónde Añadir el Nuevo Servicio Multimedia

1. **Backend - Nueva carpeta `RAG_multimedia/`**
2. **docker-compose.yml** - Añadir servicio multimedia con puerto 8006
3. **MySQL** - Script de migración para añadir columna multimedia
4. **API ddbb** - Actualizar mysql_manager.py para incluir multimedia
5. **Frontend** - Nueva screen multimedia en screens/
6. **app.routes.ts** - Añadir ruta /multimedia
7. **AGENTS.md principal** - Documentar nuevo módulo

#### C.2 Archivos Específicos a Modificar

| Archivo | Cambio Requerido | Prioridad |
|---------|-----------------|-----------|
| `docker-compose.yml` | Añadir servicio multimedia | Alta |
| `mysql/init.sql` | Añadir columna multimedia o crear migración | Alta |
| `ddb/controllers/mysql_manager.py` | Actualizar queries para incluir multimedia | Alta |
| `front/src/app/app.routes.ts` | Añadir ruta /multimedia | Alta |
| `front/src/app/screens/menu/menu.component.ts` | Añadir tarjeta de navegación | Media |
| `AGENTS.md` | Documentar nuevo módulo | Media |

### D. Recomendaciones Técnicas

- **Autenticación JWT centralizada:** Reutilizar credentials_controllers.verify_jws()
- **Aislamiento multi-usuario:** Usar patrón `{STORAGE_PATH}/{user_id}/`
- **WebSocket streaming:** Usar marcador `__END__` como los otros servicios
- **Standalone components:** Mantener patrón Angular sin NgModules
- **Volumen Docker para persistencia:** Usar volumes para videos y conversaciones
- **Puerto recomendado:** 8006 (8005 reservado para futuro)
