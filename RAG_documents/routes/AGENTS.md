# Rutas de la API REST y WebSocket

Esta carpeta define todos los endpoints públicos de la API, incluyendo autenticación JWT, manejo de WebSocket para streaming de respuestas, y operaciones CRUD sobre colecciones.

## Archivos

### `routes.py`
**Propósito:** Definición de endpoints HTTP y WebSocket con autenticación JWT obligatoria en todas las rutas.

**Componentes principales:**
- **Clases:**
  - `User(BaseModel)`: Schema Pydantic para credenciales de login/signup.
    - `username: str`
    - `password: str`
  - `CollectionRequest(BaseModel)`: Schema para operaciones sobre colecciones.
    - `collection_name: str`

- **Constantes/Configuración:**
  - `router`: Instancia de `APIRouter` montada en `main.py`
  - `active_connections`: Diccionario que rastrea WebSocket activos por connection_id

- **Endpoints:**

  **WebSocket:**
  - `WS /llm-response`: 
    - **Propósito:** Streaming en tiempo real de respuestas del chatbot RAG
    - **Autenticación:** JWT en campo `auth` del payload JSON
    - **Request:** `{"auth": "Bearer <token>", "input": "<pregunta>", "collection_name": "<nombre>"}`
    - **Response:** Stream de texto fragmentado + mensaje final `__END__`
    - **Flujo:**
      1. Aceptar conexión WebSocket
      2. Registrar en `active_connections`
      3. Loop infinito recibiendo JSON
      4. Validar JWT con `credentials_controllers.verify_jws()`
      5. Ejecutar `controllers.querier()` con streaming
      6. Manejar WebSocketDisconnect y errores

  **HTTP POST:**
  - `POST /add_document`:
    - **Propósito:** Subir documento (PDF/DOCX/TXT) a una colección
    - **Autenticación:** JWT via `Depends(credentials_controllers.verify_jws)`
    - **Parameters:** 
      - `file: UploadFile` (multipart/form-data)
      - `name_collection: str` (form data)
    - **Response:** `{"data": {"message": "Added X documents to collection 'Y'"}}`
    - **Lógica:** Valida archivo → `controllers.add_new_document_collections()`

  **HTTP GET:**
  - `GET /collections`:
    - **Propósito:** Listar colecciones disponibles del usuario
    - **Autenticación:** JWT obligatorio
    - **Response:** `{"collections_name": ["colección1", "colección2", ...]}`
    - **Lógica:** `controllers.show_name_collections()`

  - `GET /get-conversation?collection_name=<nombre>`:
    - **Propósito:** Recuperar historial de conversación de una colección
    - **Autenticación:** JWT obligatorio
    - **Response:** `[{"user": "pregunta", "bot": "respuesta"}, ...]`
    - **Lógica:** `controllers.get_conversation()`

  **HTTP POST:**
  - `POST /delete-collection`:
    - **Propósito:** Eliminar colección y su historial de conversaciones
    - **Autenticación:** JWT obligatorio
    - **Request:** `{"collection_name": "<nombre>"}`
    - **Response:** `{"collection_name deleted": "<nombre>"}`
    - **Lógica:** `controllers.remove_collections()` + `controllers.remove_conversation()`

**Dependencias:** `fastapi`, `controllers.controllers`, `controllers.credentials_controllers`, `pydantic`, `json`, `tempfile`, `os`

**Integración:** Montado en `main.py` mediante `app.include_router(router)`

---

## Diagrama de Flujo de Autenticación

```
Request (HTTP/WS)
    ↓
Depends(credentials_controllers.verify_jws)
    ↓
Extraer token de Authorization header / payload JSON
    ↓
jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    ↓
Validar expiración (payload["exp"])
    ↓
Return payload["sub"] (username)
    ↓
Endpoint ejecutado con credentials=username
```

---

## Consideraciones de Seguridad

1. **Todas las rutas requieren JWT:** No hay endpoints públicos sin autenticación
2. **Aislamiento por usuario:** Cada usuario tiene su directorio de persistencia en ChromaDB (`{PERSIST_DIRECTORY}/{username}/`)
3. **Validación de tokens:** Verificación de expiración y firma en cada request
4. **WebSocket seguro:** Autenticación por mensaje, no solo por conexión

---

## Errores HTTP Comunes

- **401 Unauthorized:** Token inválido, expirado o faltante
- **400 Bad Request:** Archivo inválido o `name_collection` vacío en `/add_document`
- **500 Internal Server Error:** Error en procesamiento de PDF o excepciones no manejadas
