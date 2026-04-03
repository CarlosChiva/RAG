# Capa de Controladores

Esta carpeta contiene la lógica de negocio para manejar las solicitudes HTTP y WebSocket, coordinando la interacción entre rutas y servicios.

## Archivos

### `controllers.py`
**Propósito:** Manejo de operaciones CRUD de archivos Excel y gestión de conexiones WebSocket para consultas LLM.

**Componentes principales:**
- **Funciones:**
  - `get_user_folder_path(user_id: str) -> str`: Construye la ruta del directorio de archivos del usuario.
  - `remove_file(credentials: str, name_file: str)`: Elimina un archivo Excel del directorio del usuario.
  - `get_path_file(name_file: str, user_id: str) -> str`: Obtiene la ruta completa de un archivo.
  - `upload_file_controller(file: UploadFile, credentials: str)`: Sube y guarda un archivo Excel en el directorio del usuario.
  - `list_files_controller(credentials: str)`: Lista todos los archivos del directorio del usuario.
  - `get_file_controller(name_file: str, credentials: dict)`: Retorna un archivo Excel para descarga.
  - `upload_file_edited_controller(file: UploadFile, credentials: dict)`: Sube un archivo Excel modificado.
  - `websocket_handler(websocket: WebSocket)`: Maneja conexiones WebSocket para consultas LLM, valida JWT y delega a `ExcelAgent.query()`.

**Dependencias:** `fastapi`, `services.excel_service`, `controllers.credentials_controllers`, `dotenv`
**Integración:** Usado por `routes/routes.py`. Gestiona la lógica de negocio de archivos y WebSocket.

### `credentials_controllers.py`
**Propósito:** Validación y verificación de tokens JWT para autenticación de solicitudes HTTP y WebSocket.

**Componentes principales:**
- **Funciones:**
  - `get_current_user(credentials: HTTPAuthorizationCredentials) -> str`: Dependencia FastAPI que decodifica y valida JWT, retorna el `sub` (user_id).
  - `verify_jws(credentials: Union[HTTPAuthorizationCredentials, str]) -> str`: Versión flexible que maneja tanto peticiones HTTP (con prefijo "Bearer ") como WebSocket (token directo o con prefijo).

**Dependencias:** `PyJWT`, `fastapi.security`, `dotenv`
**Integración:** Usado como `Depends()` en todas las rutas de `routes/routes.py` y en `controllers.py` para WebSocket.

## Configuración
- **SECRET_KEY**: Clave secreta para firma JWT (desde `.env`)
- **ALGORITHM**: Algoritmo de firma (desde `.env`, típicamente "HS256")
- **USER_FOLDERS**: Ruta base para directorios de usuarios (desde `.env`)
