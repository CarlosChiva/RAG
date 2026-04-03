# Rutas de la API del Chatbot

Esta carpeta define todos los endpoints de la API REST y WebSocket del chatbot, con autenticación JWT obligatoria.

## Archivos

### `routes.py`
**Propósito:** Definición de todos los endpoints de la API con sus respectivos handlers y validaciones.

**Componentes principales:**
- **Clases:**
  - `ChatItem`: Modelo Pydantic para operaciones de chat con campo `chatName`.
  - `ChatItem` (sobrecarga): Modelo para actualización de nombre con campos `oldChatName` y `newChatName`.

- **Endpoints WebSocket:**
  - `WS /query`: Conexión WebSocket para comunicación en tiempo real con el chatbot.
    - Recibe mensajes JSON con configuración `Config`.
    - Valida JWT internamente mediante `credentials_controllers.verify_jws`.
    - Procesa la consulta mediante `controllers.query`.
    - Maneja errores de autenticación y desconexión.

- **Endpoints REST:**
  - `GET /get_ollama_models`: Lista todos los modelos disponibles en Ollama.
    - **Autenticación:** JWT requerido.
    - **Response:** `list[dict]` con nombre y tamaño de cada modelo.

  - `POST /new_chat`: Crea una nueva conversación.
    - **Body:** `ChatItem` con `chatName`.
    - **Autenticación:** JWT requerido.
    - **Response:** `{"Response": str}` con mensaje de confirmación.

  - `GET /get_chats`: Obtiene todas las conversaciones del usuario.
    - **Autenticación:** JWT requerido.
    - **Response:** `{"chats": list[dict]}` con nombres de conversaciones.

  - `POST /remove-chat`: Elimina una conversación.
    - **Body:** `ChatItem` con `chatName`.
    - **Autenticación:** JWT requerido.
    - **Response:** `{"Response": str}` con resultado de la operación.

  - `GET /get-conversation`: Recupera historial de una conversación.
    - **Query:** `chatName` (string).
    - **Autenticación:** JWT requerido.
    - **Response:** `list[dict[str, str]]` con mensajes `{user/bot: content}`.

  - `POST /update-chat-name`: Renombra una conversación.
    - **Body:** `ChatItem` con `oldChatName` y `newChatName`.
    - **Autenticación:** JWT requerido.
    - **Response:** HTTP 200 o 500 en error.

  - `POST /get-configurations`: Obtiene configuración del usuario.
    - **Autenticación:** JWT requerido.
    - **Response:** Configuración actual del usuario.

  - `POST /update_tools_conf`: Actualiza configuración de herramientas.
    - **Body:** `dict` con configuración de herramientas.
    - **Autenticación:** JWT requerido.
    - **Response:** HTTP 200 o 500 en error.

  - `GET /get_tools_conf`: Recupera configuración de herramientas.
    - **Autenticación:** JWT requerido.
    - **Response:** `dict` con configuración actual.

**Dependencias:** `fastapi`, `controllers.controllers`, `controllers.credentials_controllers`, `config.Config`, `pydantic.BaseModel`

**Integración:** Importado en `main.py` como router principal.

---

## Esquema de Autenticación

Todos los endpoints REST requieren token JWT en el header:
```
Authorization: Bearer <token>
```

El endpoint WebSocket `/query` incluye el token en el payload JSON:
```json
{
  "config": {
    "credentials": "Bearer <token>",
    "conversation": "chat_name",
    "modelName": "llama2",
    "userInput": "tu consulta"
  }
}
```

## Notas de Implementación

- El WebSocket mantiene conexión persistente para streaming de respuestas.
- Todos los endpoints REST usan `Depends(credentials_controllers.verify_jws)` para autenticación.
- Los errores de autenticación retornan HTTP 401 con detalle del error.
