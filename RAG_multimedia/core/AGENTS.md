# Módulo Core - API Multimedia RAG

Contiene los componentes fundamentales del sistema: configuración, autenticación JWT y sistema de almacenamiento intercambiable.

---

## Archivos

### `__init__.py`
**Propósito:** Definición del namespace del módulo core.

**Componentes principales:**
- **Exportaciones:**
  - `AbstractStorage`: Interfaz abstracta para sistemas de almacenamiento
  - `LocalStorage`: Implementación de almacenamiento local en disco
  - `StorageError`: Excepción personalizada para errores de almacenamiento

**Dependencias:** `core.storage`

---

### `config.py`
**Propósito:** Configuración centralizada del servicio RAG Multimedia.

**Componentes principales:**
- **Variables de configuración:**
  - `SECRET_KEY`: Clave secreta para firma JWT (obligatoria)
  - `ALGORITHM`: Algoritmo JWT (default: `HS256`)
  - `STORAGE_PATH`: Path base para almacenamiento de videos (default: `/app/storage/videos`)
  - `CONVERSATIONS_PATH`: Path para persistencia de conversaciones (default: `/app/conversations`)
  - `PORT`: Puerto del servidor (default: `8006`)
  - `ALLOWED_HOSTS`: Lista de hosts permitidos (default: `*`)

- **Funciones:**
  - `validate_config()`: Valida que las variables requeridas estén definidas y son válidas. Se ejecuta automáticamente al cargar el módulo.

**Dependencias:** `python-dotenv`, `os`

**Integración:** Usado por `credentials_controllers.py` y toda la API

---

### `credentials_controllers.py`
**Propósito:** Controlador de autenticación JWT para HTTP y WebSocket.

**Componentes principales:**
- **Clases:**
  - `security`: Instancia de `HTTPBearer()` para extraer credenciales automáticamente

- **Funciones:**
  - `generate_token(user_id: str) -> str`: Genera token JWT con expiración de 24 horas. Claim `sub` contiene el `user_id`.
  - `verify_jws(credentials) -> str`: Verifica token JWT para HTTP requests. Maneja tanto credenciales HTTPAuthorizationCredentials como strings (WebSocket).
  - `verify_websocket_auth(auth_token: str) -> str`: Verifica token JWT para WebSocket (recibe string directamente).
  - `get_current_user(credentials: HTTPAuthorizationCredentials) -> str`: Dependencia FastAPI para rutas protegidas.

**Flujo de validación:**
1. Extraer token de credenciales (HTTP) o string (WebSocket)
2. Decodificar con `jwt.decode()` usando `SECRET_KEY` y `ALGORITHM`
3. Retornar `payload["sub"]` (user_id)
4. Manejar errores: `ExpiredSignatureError` → 401, `InvalidTokenError` → 401

**Dependencias:** `PyJWT`, `fastapi`, `core.config`

**Integración:** Usado en todas las rutas protegidas de la API

---

### `storage.py`
**Propósito:** Sistema de almacenamiento intercambiable para videos.

**Componentes principales:**
- **Constantes:**
  - `VIDEO_MIME_TYPES`: Diccionario con 26 extensiones de video y sus MIME types correspondientes

- **Clases:**
  - `StorageError`: Excepción personalizada para errores de almacenamiento

  - `AbstractStorage`: Interfaz abstracta (ABC) que define el contrato para sistemas de almacenamiento:
    - `upload(file_id, user_id, file_content, metadata) -> str`: Subir archivo y retornar URL/path
    - `download(file_id, user_id) -> tuple[bytes, str]`: Descargar archivo y retornar (contenido, mime_type)
    - `delete(file_id, user_id) -> bool`: Eliminar archivo
    - `list(user_id) -> list[dict]`: Listar todos los archivos de un usuario
    - `get_file_info(file_id, user_id) -> Optional[dict]`: Obtener metadatos de un archivo específico

  - `LocalStorage`: Implementación de almacenamiento local en disco:
    - **Estructura:** `{STORAGE_PATH}/{user_id}/{file_id}` + `{file_id}.meta.json`
    - **Características:**
      - Almacenamiento aislado por usuario
      - Metadatos guardados en archivos JSON separados
      - Operaciones asíncronas usando `aiofiles`
      - Detección automática de MIME types por extensión y magic bytes
      - Generación automática de file_id usando UUID4 (opcional)
    
    - **Métodos principales:**
      - `_ensure_storage_directory()`: Crea directorio base si no existe
      - `_get_user_directory(user_id) -> Path`: Obtiene/crea directorio del usuario
      - `_get_file_path(user_id, file_id) -> Path`: Path completo del archivo
      - `_get_metadata_path(user_id, file_id) -> Path`: Path del archivo de metadatos
      - `_detect_mime_type(filename, file_content) -> str`: Detecta MIME type por extensión o magic bytes
      - `_validate_video(filename, mime_type)`: Valida que el archivo es un video soportado

**Dependencias:** `aiofiles`, `json`, `os`, `pathlib`

**Integración:** Usado por la API para todas las operaciones de archivos. Diseñado para ser reemplazado por implementaciones S3/GCS sin modificar el código de la API.

---

## Flujo de Operaciones

### Upload de Video
1. Frontend envía `multipart/form-data` con video y metadata
2. API valida JWT con `get_current_user()`
3. Generar `file_id` (UUID4) si no se proporciona
4. `LocalStorage.upload()` guarda video y metadata JSON
5. Retornar `VideoResponseSchema` con URL y metadatos

### Download de Video
1. Frontend solicita `/videos/{id}` con JWT
2. API valida que el usuario es dueño del archivo
3. `LocalStorage.download()` lee video y metadata
4. Retornar `FileResponse` con `content-type` correcto

### List de Videos
1. Frontend solicita `/videos` con JWT
2. `LocalStorage.list(user_id)` escanea directorio del usuario
3. Retornar lista de `VideoResponseSchema`

### Chat con Contexto de Video
1. Frontend envía WebSocket message con `input`, `conversation_id`, `file_id`
2. API valida JWT con `verify_websocket_auth()`
3. Si `file_id` proporcionado, cargar metadata del video
4. LangGraph agent procesa consulta con contexto de video
5. Stream de respuesta al frontend
