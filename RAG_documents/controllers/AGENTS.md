# Controladores de Lógica de Negocio

Esta carpeta contiene la lógica de negocio central de la API RAG, gestionando operaciones de documentos, consultas al chatbot y persistencia de conversaciones.

## Archivos

### `controllers.py`
**Propósito:** Orquestación de operaciones principales del sistema RAG (Retrieval-Augmented Generation).

**Componentes principales:**
- **Funciones:**
  - `show_name_collections(credentials: str) -> list[str]`: Lista todas las colecciones disponibles para un usuario autenticado.
  - `add_new_document_collections(document, name_collection, credentials) -> dict[str, str]`: Procesa y añade documentos PDF a una colección específica.
  - `remove_collections(collection_name, credentials) -> dict[str, str]`: Elimina una colección de la base de datos vectorial.
  - `querier(question: str, collection_name: str, credentials: str, websocket) -> str`: Procesa consultas del usuario mediante streaming WebSocket, consultando la base de datos vectorial y generando respuestas contextualizadas con historial de chat.
  - `add_conversation(collection_name, credentials, user_input, bot_output) -> None`: Persiste intercambio usuario-bot en archivo JSON.
  - `clear_conversation(collection_name, credentials) -> None`: Borra el historial de conversación de una colección.
  - `get_conversation(collection_name, credentials) -> list[dict[str, str]]`: Recupera el historial de conversación para contexto en respuestas.
  - `remove_conversation(collection_name, credentials) -> None`: Elimina permanentemente el historial de una colección.

**Dependencias:** `db.chroma_manager`, `db.chroma`, `db.model_conf`, `db.chroma_cli`, `json`, `os`, `logging`

**Integración:** Usado por `routes/routes.py` para manejar todas las solicitudes de la API.

---

### `credentials_controllers.py`
**Propósito:** Validación y verificación de tokens JWT para autenticación de usuarios en todas las rutas protegidas.

**Componentes principales:**
- **Constantes/Configuración:**
  - `SECRET_KEY`: Clave secreta para firma JWT (desde variable de entorno).
  - `ALGORITHM`: Algoritmo de cifrado (HS256 por defecto).
  - `security`: Instancia de `HTTPBearer` para extraer token del header Authorization.

- **Funciones:**
  - `get_current_user(credentials: HTTPAuthorizationCredentials) -> str`: Valida token JWT y extrae el subject (usuario). Maneja expiración y tokens inválidos.
  - `verify_jws(credentials: Union[HTTPAuthorizationCredentials, str]) -> str`: Versión mejorada que soporta tanto HTTP como WebSocket, manejando diferentes formatos de entrada (con/sin prefijo "Bearer").

**Dependencias:** `jwt`, `fastapi`, `fastapi.security`, `dotenv`, `datetime`, `logging`

**Integración:** Exportado como dependencia en `routes/routes.py` para proteger todas las rutas.

---

## Flujo de Datos

1. **Autenticación:** `verify_jws()` valida JWT → extrae username (`payload["sub"]`)
2. **Gestión de Colecciones:** `show_name_collections()` → `chroma_manager.get_collections()` → lista de nombres
3. **Ingesta de Documentos:** `add_new_document_collections()` → `chroma_manager.add_pdf_to_collection()` → procesamiento PDF → embeddings → ChromaDB
4. **Consultas RAG:** `querier()` → recupera historial → obtiene vectorstore → crea chain LangChain → streaming respuesta → persiste conversación
