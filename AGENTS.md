# RAG - Sistema Retrieval-Augmented Generation

Proyecto completo que implementa múltiples servicios RAG (Retrieval-Augmented Generation) para interactuar con diferentes fuentes de datos usando LLMs locales (Ollama) con LangGraph y LangChain.

---

## Módulos Principales

### RAG_excels
**API RAG para Excels**

Esta API implementa un sistema RAG para análisis y gestión de archivos Excel usando LLMs locales (Ollama) con LangGraph. Permite subir, consultar y editar archivos Excel mediante un agente autónomo con herramientas especializadas.

**Puerto:** 8004

**Tecnologías:** FastAPI, LangGraph, Ollama, FAISS, Pandas, OpenPyXL, Unstructured, PyJWT

**Funcionalidades:**
- Upload, list, download, delete de archivos Excel
- Consultas LLM vía WebSocket con streaming
- 6 herramientas del agente: explorar_excel, buscar_en_excel, buscar_columna, buscar_por_filtro, consulta_libre_excel, editar_excel
- Backup automático antes de ediciones
- Aislamiento multi-usuario con JWT

→ [Documentación detallada](./RAG_excels/AGENTS.md)

---

### RAG_documents
**API RAG Documents - Sistema de Chatbot con Retrieval-Augmented Generation**

API FastAPI que permite cargar documentos PDF/DOCX/TXT y responder preguntas basándose en ellos usando LangChain, ChromaDB y Ollama.

**Puerto:** 8000

**Tecnologías:** FastAPI, LangChain, ChromaDB, Ollama, pdfplumber, pytesseract, PyJWT

**Funcionalidades:**
- Carga de documentos multi-formato con OCR
- Búsqueda semántica mediante embeddings
- Respuestas en tiempo real vía WebSocket
- Historial de conversaciones persistente
- Aislamiento de datos por usuario

→ [Documentación detallada](./RAG_documents/AGENTS.md)

---

### RAG_ddbb
**API RAG-DDBB - Base de Datos con LLM**

API FastAPI que implementa Text-to-SQL usando RAG con Ollama. Permite consultar bases de datos PostgreSQL, MySQL y SQLite mediante preguntas en lenguaje natural.

**Puerto:** 8002

**Tecnologías:** FastAPI, LangChain, Ollama, SQLAlchemy, psycopg2, PyMySQL, PyJWT

**Funcionalidades:**
- Consultas Text-to-SQL en tiempo real vía WebSocket
- Gestión multi-usuario de configuraciones de conexión
- Soporte para PostgreSQL, MySQL y SQLite
- Persistencia de configuraciones en JSON por usuario

→ [Documentación detallada](./RAG_ddbb/AGENTS.md)

---

### chatbot
**API del Chatbot**

API REST y WebSocket para interacción con modelos LLM locales vía Ollama. Soporta conversaciones persistentes, generación de imágenes (ComfyUI) y agentes MCP.

**Tecnologías:** FastAPI, LangGraph, LangChain-Ollama, langchain-mcp-adapters, PyJWT

**Funcionalidades:**
- Chat general con streaming en tiempo real
- Generación de imágenes vía ComfyUI
- Ejecución de herramientas MCP mediante grafo LangGraph
- Gestión de conversaciones persistentes en JSON
- Configuración de herramientas por usuario

→ [Documentación detallada](./chatbot/AGENTS.md)

---

### ddbb
**API de Gestión de Usuarios y Servicios**

API REST con FastAPI para autenticación de usuarios y gestión de servicios. Proporciona JWT tokens y controla qué servicios puede acceder cada usuario.

**Puerto:** 8001

**Tecnologías:** FastAPI, MySQL, PyJWT, bcrypt, python-dotenv

**Funcionalidades:**
- Registro y login de usuarios
- Generación y validación de tokens JWT
- Gestión de servicios habilitados por usuario (chatbot, pdf, multimedia, excel, ddbb)
- Endpoints protegidos con autenticación JWT

→ [Documentación detallada](./ddbb/AGENTS.md)

---

### mysql
**Módulo de Base de Datos MySQL**

Configuración inicial y esquema de base de datos para el servicio MySQL del proyecto RAG.

**Tecnologías:** MySQL 5.7+

**Tablas:**
- `users`: id_user, username, password_hash, jwt_token
- `services`: id_service, user_id, chatbot, pdf, multimedia, excel, ddbb

→ [Documentación detallada](./mysql/AGENTS.md)

---

### front
**Frontend RAG - Aplicación Angular**

Frontend de la aplicación RAG construido con Angular 19.2.0. Permite a los usuarios interactuar con diferentes fuentes de datos mediante lenguaje natural.

**Puerto:** 4200

**Tecnologías:** Angular 19.2.0, TypeScript 5.7.2, RxJS, marked, prismjs

**Funcionalidades:**
- 6 pantallas: login, menu, excels, chatbot, rag_ddbb, rag_pdf
- 18 componentes reutilizables
- 5 servicios especializados
- Autenticación JWT con interceptores
- Comunicación híbrida HTTP/WebSocket
- Standalone components sin NgModules

→ [Documentación detallada](./front/AGENTS.md)

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Angular (Port 4200)                 │
│  - Login/Menu - Excels - Chatbot - RAG DDBB - RAG PDF          │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/WS + JWT
                            ↓
┌───────────────────────────▼─────────────────────────────────────┐
│  API ddbb (Port 8001) - Autenticación y Gestión de Servicios   │
│  - /log-in, /sing_up - /get-services - MySQL (users, services) │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  RAG_excels   │  │ RAG_documents │  │   RAG_ddbb    │
│  (Port 8004)  │  │  (Port 8000)  │  │  (Port 8002)  │
│  - Excel RAG  │  │  - PDF RAG    │  │  - Text-to-SQL│
│  - LangGraph  │  │  - ChromaDB   │  │  - PostgreSQL │
│  - FAISS      │  │  - Ollama     │  │  - MySQL      │
└───────────────┘  └───────────────┘  └───────────────┘
        │                   │                   │
        ↓                   ↓                   ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   chatbot     │  │    mysql      │  │    Ollama     │
│  (WebSocket)  │  │   (MySQL DB)  │  │  (LLM Local)  │
│  - LangGraph  │  │   - users     │  │  - gpt-oss    │
│  - ComfyUI    │  │   - services  │  │  - llama3.2   │
│  - MCP Agent  │  └───────────────┘  │  - bge-m3     │
└───────────────┘                      └───────────────┘
```

---

## Flujo de Autenticación

1. **Login:** Frontend → `ddbb:/log-in` → JWT token
2. **Servicios:** Frontend → `ddbb:/get-services` → Lista de servicios habilitados
3. **Acceso:** JWT incluido en header `Authorization: Bearer <token>` en todas las peticiones
4. **Validación:** Cada API valida JWT antes de procesar requests

---

## Variables de Entorno Comunes

- `SECRET_KEY`: Clave secreta para firma JWT (compartida entre servicios)
- `ALGORITHM`: Algoritmo JWT (HS256)
- `EMBEDD_MODEL`: Modelo de embeddings para RAG
- `MODEL` / `SQL_MODEL`: Modelo LLM para generación de respuestas

---

## Contenedores Docker

| Servicio | Puerto | Imagen Base |
|----------|--------|-------------|
| front | 4200 | node:18-alpine |
| ddbb | 8001 | python:3.10-slim |
| RAG_documents | 8000 | python:3.10-slim |
| RAG_ddbb | 8002 | python:3.12-slim |
| RAG_excels | 8004 | python:3.12-slim-trixie |
| chatbot | - | python:3.12 |
| mysql | 3306 | mysql:5.7+ |
