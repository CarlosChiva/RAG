# Controladores de la API RAG-DDBB

Esta carpeta contiene la lógica de negocio para las operaciones principales: consulta de bases de datos mediante LLM y gestión de configuraciones de conexión.

## Archivos

### `controllers.py`
**Propósito:** Implementa las funciones principales para interacción con bases de datos mediante RAG (Retrieval-Augmented Generation) y gestión de configuraciones de conexión por usuario.

**Componentes principales:**

- **Funciones:**
  - `querier(question: str, conf: Config, websocket)`: Ejecuta consultas naturales a la base de datos usando el modelo RAG. Recibe la pregunta, configuración de DB y websocket para streaming de respuestas.
  - `get_configurations(user: str) -> list[Config]`: Recupera todas las configuraciones de base de datos guardadas para un usuario desde archivo JSON.
  - `add_configurations(user: str, conf: Config)`: Agrega o actualiza una configuración de conexión en el archivo del usuario. Detecta duplicados por `connection_name`.
  - `try_connection(config: Config)`: Prueba la conectividad con la base de datos sin persistir la configuración.
  - `remove_configuration(conf_rm: Config, user: str)`: Elimina una configuración específica del archivo del usuario.

**Dependencias:** `model.rag_model`, `config.Config`, `json`, `os`, `fastapi.HTTPException`

**Integración:** Usado por `routes.routes` para manejar las peticiones HTTP y WebSocket.

---

### `credentials_controllers.py`
**Propósito:** Autenticación y validación de tokens JWT para proteger rutas HTTP y WebSocket.

**Componentes principales:**

- **Funciones:**
  - `get_current_user(credentials: HTTPAuthorizationCredentials) -> str`: Extrae y valida token JWT de cabecera HTTP. Devuelve el `sub` (usuario) del payload.
  - `verify_jws(credentials: Union[HTTPAuthorizationCredentials, str]) -> str`: Versión mejorada que soporta tanto peticiones HTTP como WebSocket. Maneja diferentes formatos de token (con/sin "Bearer ").

- **Constantes:**
  - `SECRET_KEY`: Clave secreta para firmar/verificar tokens (desde `.env`).
  - `ALGORITHM`: Algoritmo de firma JWT (desde `.env`, default: `HS256`).
  - `security`: Instancia de `HTTPBearer` para dependencias de autenticación.

**Dependencias:** `jwt`, `fastapi.security`, `dotenv`, `datetime`, `hashlib`

**Integración:** Usado como `Depends()` en todas las rutas protegidas de `routes.routes`.
