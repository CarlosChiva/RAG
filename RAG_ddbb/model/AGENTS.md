# Modelos de Datos y Lógica RAG

Esta carpeta implementa la conexión a bases de datos relacionales y la cadena de procesamiento RAG para convertir preguntas naturales en consultas SQL y respuestas en lenguaje natural.

## Archivos

### `rag_model.py`
**Propósito:** Orquesta la comunicación entre la aplicación FastAPI, las bases de datos (PostgreSQL/MySQL/SQLite) y el modelo LLM (Ollama) para implementar Text-to-SQL con RAG.

**Componentes principales:**

- **Clases:**
  - `DataBase`:
    - **Responsabilidad:** Encapsula la conexión y configuración de bases de datos relacionales.
    - **Métodos clave:**
      - `__init__(conf: Config)`: Inicializa la conexión usando las credenciales proporcionadas.
      - `extract_driver(type_db: str) -> str`: Mapea tipo de DB (`sqlite`, `mysql`, `postgresql`) al driver SQLAlchemy correspondiente.
      - `get_database()`: Retorna instancia de `SQLDatabase` de LangChain.
      - `get_engine()`: Crea y retorna motor SQLAlchemy.
      - `try_connect() -> dict`: Prueba conexión sin persistir, retorna `{"success": bool, "error": str}`.
      - `connect_db()`: Establece conexión persistente mediante LangChain SQLDatabase.

  - `SQLQueryParser(StrOutputParser)`:
    - **Responsabilidad:** Parsea la salida del LLM extrayendo solo la consulta SQL de bloques markdown.
    - **Métodos clave:**
      - `parse(text: str) -> str`: Usa regex para extraer contenido entre ```sql y ```.

  - `RagModel`:
    - **Responsabilidad:** Orquesta las cadenas de LangChain para generar SQL y respuestas naturales.
    - **Métodos clave:**
      - `__init__(db, engine)`: Inicializa modelo ChatOllama y construye las cadenas de procesamiento.
      - `get_sql_query_extractor_prompt()`: Retorna prompt template para generar SQL desde pregunta natural.
      - `get_chain_extract_query()`: Cadena que transforma pregunta → SQL usando schema de la DB.
      - `get_chain_full_response()`: Cadena completa que produce respuesta natural con contexto de schema, query y resultados.
      - `run_query(query: str)`: Ejecuta consulta SQL y retorna resultados con información de columnas.
      - `query(query: str, websocket)`: Método asíncrono que streama la respuesta en tiempo real al cliente WebSocket, incluyendo tabla de resultados en JSON.

**Dependencias:** `langchain-community`, `langchain-ollama`, `langchain-core`, `sqlalchemy`, `pandas`, `pymysql`, `psycopg2`, `dotenv`, `regex`

**Integración:** Usado por `controllers.controllers` para ejecutar consultas RAG.

**Flujo de procesamiento:**
1. `DataBase` conecta a la DB y obtiene schema
2. `RagModel.get_chain_extract_query()` genera SQL desde pregunta
3. `RagModel.run_query()` ejecuta SQL
4. `RagModel.get_chain_full_response()` genera respuesta natural con contexto
5. Resultados se streaman vía WebSocket en formato JSON
