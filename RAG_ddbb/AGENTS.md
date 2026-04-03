# API RAG-DDBB - Base de Datos con LLM

API FastAPI que implementa Text-to-SQL usando RAG (Retrieval-Augmented Generation) con Ollama. Permite consultar bases de datos PostgreSQL, MySQL y SQLite mediante preguntas en lenguaje natural, con gestión multi-usuario de configuraciones de conexión y autenticación JWT.

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                   Cliente (WebSocket/HTTP)              │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  routes/routes.py - Endpoints & Autenticación JWT      │
└────────────┬──────────────────────────────┬─────────────┘
             │                              │
┌────────────▼────────────┐  ┌─────────────▼──────────────┐
│ controllers/           │  │ model/                     │
│ - controllers.py       │  │ - rag_model.py             │
│ - credentials_controllers│ │ - DataBase, RagModel       │
└────────────┬────────────┘  └─────────────┬──────────────┘
             │                              │
             └────────────┬─────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────┐
│  Bases de Datos: PostgreSQL / MySQL / SQLite          │
└────────────────────────────────────────────────────────┘
```

## Subcarpetas

- **`controllers/`**: Lógica de negocio para consultas RAG y gestión de configuraciones de conexión por usuario.  
  → [Ver documentación detallada](./controllers/AGENTS.md)

- **`model/`**: Modelos de datos, conexión a bases de datos y cadenas LangChain para Text-to-SQL.  
  → [Ver documentación detallada](./model/AGENTS.md)

- **`routes/`**: Definición de endpoints HTTP y WebSocket, validación de inputs y orquestación de controladores.  
  → [Ver documentación detallada](./routes/AGENTS.md)

## Archivos de Configuración

- **`main.py`**: Punto de entrada de la aplicación FastAPI. Configura CORS, incluye router y se ejecuta con uvicorn en puerto 8002.

- **`config.py`**: Define la clase `Config` (Pydantic BaseModel) con campos para conexión a base de datos: `connection_name`, `type_db`, `user`, `password`, `host`, `port`, `database_name`. Incluye métodos `serialize()` y `deserialize()` para persistencia JSON.

- **`enums_type.py`**: Enumeración `Enumms` con tipos de base de datos soportados: `SQLITE`, `MYSQL`, `POSTGRESQL`.

- **`requirements.txt`**: 64 dependencias incluyendo FastAPI, LangChain, Ollama, SQLAlchemy, PyJWT, psycopg2-binary, PyMySQL, pandas.

- **`Dockerfile`**: Imagen basada en Python 3.12 con dependencias compiladas (psycopg2), expone puerto 8002 y ejecuta `uvicorn main:app`.

- **`.env`**: Variables de entorno: `SECRET_KEY` (JWT), `ALGORITHM` (HS256), `SQL_MODEL` (nombre modelo Ollama), `CONFIG_FOLDER` (ruta persistencia configuraciones).

- **`README.md`**: Documentación completa de endpoints, ejemplos de uso, variables de entorno y instrucciones Docker.

## Flujos Principales

### 1. Consulta Text-to-SQL (WebSocket)
```
Cliente → POST /question (WebSocket)
  ↓
Validar JWT (credentials_controllers.verify_jws)
  ↓
Extraer: question, config (Config)
  ↓
controllers.querier() → model.RagModel.query()
  ↓
RagModel:
  - get_chain_extract_query(): pregunta → SQL
  - run_query(): ejecutar SQL en DB
  - get_chain_full_response(): generar respuesta natural
  ↓
Stream respuesta JSON a cliente:
  {"response": "..."} (chunked)
  {"table": {...}} (resultados)
  {"end": "__END__"}
```

### 2. Gestión de Configuraciones
```
GET /get-list-configurations → controllers.get_configurations(user)
  → Lee {user}.json de CONFIG_FOLDER
  → Retorna list[Config]

POST /add_configuration → controllers.add_configurations(user, conf)
  → Lee/crea {user}.json
  → Agrega o actualiza (por connection_name)
  → Sobrescribe archivo

DELETE /remove-configuration → controllers.remove_configuration(conf_rm, user)
  → Filtra configuración del JSON
  → Sobrescribe archivo

GET /try-connection → controllers.try_connection(config)
  → DataBase(config).try_connect()
  → Testea conexión sin persistir
```

## Endpoints Públicos

| Método   | Ruta                      | Propósito                          | Autenticación |
|----------|---------------------------|------------------------------------|---------------|
| WebSocket| `/question`               | Consultas Text-to-SQL en tiempo real | JWT           |
| GET      | `/get-list-configurations`| Listar configuraciones guardadas   | JWT           |
| POST     | `/add_configuration`      | Crear/actualizar configuración     | JWT           |
| GET      | `/try-connection`         | Probar conexión DB                 | JWT           |
| DELETE   | `/remove-configuration`   | Eliminar configuración             | JWT           |

## Tecnologías Clave

- **Framework:** FastAPI (asíncrono, WebSocket nativo)
- **LLM:** Ollama (modelos locales como qwen2.5)
- **RAG:** LangChain (SQLDatabase, ChatOllama, RunnablePassthrough)
- **Bases de Datos:** PostgreSQL (psycopg2), MySQL (PyMySQL), SQLite
- **Autenticación:** JWT (PyJWT, HS256)
- **Persistencia:** JSON files por usuario (CONFIG_FOLDER/{user}.json)
- **Contenedorización:** Docker (puerto 8002)
