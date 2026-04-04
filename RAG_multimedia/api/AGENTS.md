# Módulo API - RAG Multimedia

Contiene los endpoints REST y las dependencias de inyección para la API de gestión de videos con RAG.

---

## Archivos

### `routes.py`
**Propósito:** Definición de rutas REST para operaciones de videos y conversaciones.

**Componentes principales:**

- **Router:**
  - `router`: Instancia de `APIRouter` con todos los endpoints protegidos por JWT

- **Endpoints de Conversaciones:**
  - `GET /conversations`: Listar todas las conversaciones del usuario autenticado
    - **Dependencias:** `get_current_user`
    - **Retorna:** `ListConversationsResponseSchema` con lista de conversaciones y total
    - **Flujo:** Lee archivo JSON `{user_id}.json` desde `CONVERSATIONS_PATH`, filtra por user_id
    - **Errores:** 401 (JWT inválido), 404 (no existe), 500 (error al cargar)

  - `GET /conversations/{conversation_id}`: Obtener una conversación específica
    - **Dependencias:** `get_current_user`
    - **Retorna:** `ConversationSchema` con todos los mensajes
    - **Flujo:** Busca conversación por ID en el archivo JSON del usuario, verifica ownership
    - **Errores:** 401 (JWT inválido), 403 (no es propietario), 404 (no existe), 500 (error)

- **Endpoints de Videos:**
  - `POST /upload`: Subir un archivo de video
    - **Dependencias:** `get_current_user`, `get_storage`
    - **Parámetros:**
      - `file: UploadFile`: Archivo de video (multipart/form-data, obligatorio)
      - `metadata: str`: JSON string con metadatos (default: `{}`)
      - `file_id: str`: ID personalizado (opcional, se genera UUID si no se proporciona)
    - **Retorna:** `VideoResponseSchema` con file_id, url, metadata, size, mime_type, created_at
    - **Flujo:**
      1. Validar nombre y extensión del archivo (mp4, webm, mov, avi, mkv, flv, wmv)
      2. Parsear metadata JSON
      3. Validar/generar file_id (UUID)
      4. Validar tamaño máximo (500MB)
      5. `LocalStorage.upload()` guarda video y metadata
    - **Errores:** 400 (archivo inválido, metadata JSON inválido), 401 (JWT), 413 (archivo muy grande), 500 (error upload)

  - `GET /media/{file_id}`: Descargar un archivo de video
    - **Dependencias:** `get_current_user`, `get_storage`
    - **Retorna:** `FileResponse` con el video binario
    - **Flujo:**
      1. `get_file_info()` verifica ownership
      2. `LocalStorage.download()` lee video y mime_type
      3. Retorna FileResponse con headers `Content-Type` y `Content-Disposition: inline`
    - **Errores:** 401 (JWT), 403 (no es propietario), 404 (no existe), 500 (error lectura)

  - `DELETE /media/{file_id}`: Eliminar un archivo de video
    - **Dependencias:** `get_current_user`, `get_storage`
    - **Retorna:** `{"message": "Video eliminado exitosamente"}`
    - **Flujo:**
      1. `get_file_info()` verifica ownership
      2. `LocalStorage.delete()` elimina video y metadata JSON
    - **Errores:** 401 (JWT), 403 (no es propietario), 404 (no existe), 500 (error eliminación)

**Dependencias:** `fastapi`, `aiofiles`, `json`, `core.config`, `core.credentials_controllers`, `core.storage`, `models.schemas`, `api.deps`

**Integración:** Importado por el main.py de la aplicación FastAPI

---

### `deps.py`
**Propósito:** Dependencias de inyección reutilizables para la API.

**Componentes principales:**

- **Funciones de Dependencia:**
  - `get_current_user() -> str`: Extrae user_id del token JWT
    - **Uso:** Base para todas las rutas protegidas
    - **Flujo:** Llama a `core.credentials_controllers.get_current_user()`
    - **Retorna:** user_id del claim `sub` del JWT

  - `get_storage() -> LocalStorage`: Proporciona instancia de LocalStorage
    - **Uso:** Rutas que operan con archivos (upload, download, delete)
    - **Retorna:** Nueva instancia de `LocalStorage()` por petición

  - `get_conversation_manager() -> ConversationManager`: Proporciona instancia de ConversationManager
    - **Uso:** Rutas que manejan historial de conversaciones (en desarrollo)
    - **Retorna:** Nueva instancia de `ConversationManager()` por petición
    - **Nota:** Importación condicional con `TYPE_CHECKING` para evitar error si no existe aún

  - `get_current_user_and_storage() -> Tuple[str, LocalStorage]`: Dependencia combinada
    - **Uso:** Rutas que requieren autenticación y almacenamiento (upload, download, delete)
    - **Retorna:** Tupla `(user_id, storage)`

  - `get_current_user_and_conversation_manager() -> Tuple[str, ConversationManager]`: Dependencia combinada
    - **Uso:** Rutas de chat que requieren autenticación y historial
    - **Retorna:** Tupla `(user_id, conversation_manager)`

  - `get_all_dependencies() -> Tuple[str, LocalStorage, ConversationManager]`: Dependencia completa
    - **Uso:** Rutas que requieren acceso completo al sistema
    - **Retorna:** Tupla `(user_id, storage, conversation_manager)`

**Dependencias:** `fastapi`, `core.credentials_controllers`, `core.storage` (opcional: `core.conversation_manager`)

**Integración:** Usado por `routes.py` como `Depends(...)` en todas las rutas

---

## Arquitectura de la API

```
┌─────────────────────────────────────────────────────────────┐
│                    Routes (routes.py)                       │
│  - GET /conversations                                       │
│  - GET /conversations/{id}                                  │
│  - POST /upload                                             │
│  - GET /media/{file_id}                                     │
│  - DELETE /media/{file_id}                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │ Depends(...)
                            ↓
┌───────────────────────────▼─────────────────────────────────┐
│              Dependencies (deps.py)                         │
│  - get_current_user() → user_id                             │
│  - get_storage() → LocalStorage                             │
│  - get_conversation_manager() → ConversationManager         │
│  - get_current_user_and_storage() → (user_id, storage)      │
│  - get_all_dependencies() → (user_id, storage, conv_mgr)    │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  credentials  │  │   storage     │  │ conversation  │
│  controllers  │  │    (core)     │  │   manager     │
│  - JWT verify │  │  - LocalStorage│  │  (future)     │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## Flujo de Operaciones

### Upload de Video
1. Frontend → `POST /upload` con multipart/form-data (file, metadata, file_id opcional)
2. `get_current_user()` valida JWT → user_id
3. `get_storage()` crea LocalStorage
4. Validar archivo (extensión, tamaño <500MB)
5. `LocalStorage.upload()` guarda video + metadata JSON
6. Retornar `VideoResponseSchema`

### Listar Conversaciones
1. Frontend → `GET /conversations` con JWT
2. `get_current_user()` valida JWT → user_id
3. Leer `{CONVERSATIONS_PATH}/{user_id}.json`
4. Filtrar conversaciones por user_id
5. Retornar `ListConversationsResponseSchema`

### Download de Video
1. Frontend → `GET /media/{file_id}` con JWT
2. `get_current_user()` valida JWT → user_id
3. `get_storage().get_file_info()` verifica ownership
4. `LocalStorage.download()` lee video
5. Retornar `FileResponse` con headers correctos

### Eliminar Video
1. Frontend → `DELETE /media/{file_id}` con JWT
2. `get_current_user()` valida JWT → user_id
3. `get_storage().get_file_info()` verifica ownership
4. `LocalStorage.delete()` elimina video + metadata
5. Retornar mensaje de confirmación
