# Rutas y Endpoints de la API

Esta carpeta define los endpoints HTTP y WebSocket de la aplicación, gestionando autenticación, validación de entradas y orquestación de controladores.

## Archivos

### `routes.py`
**Propósito:** Define todos los endpoints públicos de la API RAG-DDBB, incluyendo ruta WebSocket para consultas en tiempo real y rutas REST para gestión de configuraciones.

**Componentes principales:**

- **Clases:**
  - `User(BaseModel)`:
    - **Campos:** `username: str`, `password: str`
    - **Uso:** Esquema para autenticación (no usado directamente en este archivo, importado de auth si existe).

  - `CollectionRequest(BaseModel)`:
    - **Campos:** `collection_name: str`
    - **Uso:** Esquema para operaciones de colección (definido pero no utilizado actualmente).

- **Constantes:**
  - `router = APIRouter()`: Instancia principal del router de FastAPI.
  - `active_connections`: Diccionario que rastrea conexiones WebSocket activas por ID.

- **Endpoints:**

  1. **`websocket "/question"`** - `llm_response()`
     - **Propósito:** Endpoint principal para consultas Text-to-SQL en tiempo real.
     - **Flujo:**
       1. Acepta conexión WebSocket
       2. Registra conexión en `active_connections`
       3. Recibe mensajes JSON con `auth` (JWT), `question` y `config`
       4. Valida token JWT vía `credentials_controllers.verify_jws()`
       5. Ejecuta consulta RAG vía `controllers.querier()`
       6. Streama respuesta en tiempo real al cliente
       7. Maneja desconexiones y limpieza de recursos

  2. **`GET "/get-list-configurations"`** - `get_collections_name()`
     - **Propósito:** Retorna todas las configuraciones de DB guardadas para el usuario autenticado.
     - **Autenticación:** JWT obligatorio (`Depends(verify_jws)`)
     - **Response:** `list[Config]` serializado a JSON

  3. **`POST "/add_configuration"`** - `delete_collection()`
     - **Propósito:** Agrega o actualiza una configuración de base de datos.
     - **Body:** `Config` object
     - **Autenticación:** JWT obligatorio
     - **Response:** `{"message": str}` o `{"error": str}`

  4. **`GET "/try-connection"`** - `try_connection()`
     - **Propósito:** Prueba conectividad con DB sin persistir configuración.
     - **Query Params:** `connection_name`, `type_db`, `user`, `password`, `host`, `port`, `database_name`
     - **Autenticación:** JWT obligatorio
     - **Response:** `{"message": "Conexión exitosa"}` o HTTP 400 con error

  5. **`DELETE "/remove-configuration"`** - `remove_conf()`
     - **Propósito:** Elimina una configuración de base de datos.
     - **Body:** `Config` object (para identificar qué eliminar)
     - **Autenticación:** JWT obligatorio
     - **Response:** `{"Response": {"message"/"error": str}}`

**Dependencias:** `fastapi`, `controllers.controllers`, `controllers.credentials_controllers`, `config.Config`, `pydantic`, `json`, `logging`

**Integración:** Importado e incluido en `main.app` vía `app.include_router(router)`.

## Resumen de Endpoints

| Método   | Ruta                      | Propósito                          | Auth |
|----------|---------------------------|------------------------------------|------|
| WebSocket| `/question`               | Consultas Text-to-SQL en tiempo real | JWT  |
| GET      | `/get-list-configurations`| Listar configuraciones guardadas   | JWT  |
| POST     | `/add_configuration`      | Crear/actualizar configuración     | JWT  |
| GET      | `/try-connection`         | Probar conexión DB                 | JWT  |
| DELETE   | `/remove-configuration`   | Eliminar configuración             | JWT  |
