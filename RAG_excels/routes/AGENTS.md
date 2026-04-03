# Capa de Rutas

Esta carpeta define los endpoints REST y WebSocket de la API FastAPI, actuando como interfaz pública del sistema.

## Archivos

### `routes.py`
**Propósito:** Define el router FastAPI con 6 endpoints REST para gestión de archivos y 1 endpoint WebSocket para consultas LLM.

**Componentes principales:**
- **Router:**
  - `router = APIRouter()`: Router principal montado en `main.py`.

- **Endpoints REST:**
  - `POST /upload_file`: Sube un archivo Excel nuevo.
    - **Parámetros:** `file` (UploadFile), `credentials` (JWT via Depends).
    - **Retorna:** Mensaje de confirmación.
  - `GET /list_files`: Lista archivos del usuario.
    - **Parámetros:** `credentials` (JWT).
    - **Retorna:** Lista de nombres de archivos.
  - `GET /get_file`: Descarga un archivo específico.
    - **Parámetros:** `name_file` (str), `credentials` (JWT).
    - **Retorna:** FileResponse con el archivo.
  - `POST /upload_file_edited`: Sube un archivo modificado.
    - **Parámetros:** `file` (UploadFile), `credentials` (JWT).
    - **Retorna:** Mensaje de confirmación.
  - `DELETE /delete_file`: Elimina un archivo.
    - **Parámetros:** `name_file` (str), `credentials` (JWT).
    - **Retorna:** Mensaje de confirmación o error.

- **Endpoint WebSocket:**
  - `WS /llm-query`: Conexión WebSocket para consultas LLM en tiempo real.
    - **Maneja:** Recepción de JSON con `auth` (JWT), `input` (pregunta), `file_name`.
    - **Delega a:** `controllers.websocket_handler()`.

**Dependencias:** `fastapi`, `controllers.controllers`, `controllers.credentials_controllers`
**Integración:** Montado en `main.app` con `app.include_router(router)`.

## Flujo de Autenticación
Todas las rutas REST usan `Depends(credentials_controllers.verify_jws)` para validar JWT del header `Authorization: Bearer <token>` antes de ejecutar la lógica del controller.
