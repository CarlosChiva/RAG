# Capa de Servicios

Esta carpeta contiene servicios de bajo nivel para procesamiento de archivos Excel y gestión de agentes.

## Archivos

### `excel_loader.py`
**Propósito:** Carga, procesa y serializa archivos Excel para crear vector stores FAISS con embeddings semánticos.

**Componentes principales:**
- **Constantes:**
  - `embedding_model`: Modelo de embeddings desde `.env` (Ollama).

- **Funciones:**
  - `load_and_process_excel(file_path: str)`:
    - **Propósito:** Carga un Excel desde cero, crea chunks con metadata (hoja, celda) y genera vector store FAISS.
    - **Proceso:** `UnstructuredExcelLoader` → `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=200) → `OllamaEmbeddings` → `FAISS.from_documents()`.
    - **Retorna:** Tupla `(vectorstore, retriever, embeddings)`.
  - `load_existing_vectorstore(index_path: str = "excel_index")`:
    - **Propósito:** Carga un vector store previamente guardado para reutilización.
    - **Retorna:** Tupla `(vectorstore, retriever, embeddings)`.
  - `save_vectorstore(vectorstore, index_path: str = "excel_index")`:
    - **Propósito:** Serializa el vector store a disco para persistencia.

**Dependencias:** `pandas`, `langchain_community.document_loaders`, `langchain_text_splitters`, `langchain_ollama`, `langchain_community.vectorstores`, `dotenv`
**Integración:** Usado por `models.tools.initialize()` para inicializar el retriever y vectorstore globales.

### `excel_service.py`
**Propósito:** Gestiona sesiones de usuario de forma centralizada, creando y reutilizando instancias de `UserSession` por usuario/archivo.

**Componentes principales:**
- **Clase:**
  - `ExcelAgent` (Singleton):
    - **Atributos:**
      - `user_session: Dict[str, UserSession]`: Diccionario que mapea `user_id` → `UserSession`.
    - **Métodos clave:**
      - `query(question: str, file_path: str, credentials: str, websocket: WebSocket)`:
        - Verifica si existe `UserSession` para el `credentials` (user_id).
        - Si no existe: Crea nueva `UserSession(filename=file_path, user_id=credentials)`.
        - Si existe: Reutiliza la sesión actual.
        - Delega la consulta a `session.query_agent(websocket, question)`.

**Dependencias:** `models.user`, `fastapi.WebSocket`
**Integración:** Instanciado por `controllers.controllers.websocket_handler()` para manejar cada consulta WebSocket.

## Patrón de Diseño
- **ExcelAgent**: Singleton que actúa como orquestador de sesiones.
- **UserSession**: Singleton por instancia (cada usuario/archivo tiene su propia sesión con su `Agent` personal).
- **Caching**: Vector stores se guardan en disco (`excel_index`) para evitar reprocesamiento costoso.
