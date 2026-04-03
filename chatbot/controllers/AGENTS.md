# Controladores del Chatbot

Esta carpeta contiene la lógica de negocio que gestiona las operaciones del chatbot, incluyendo manejo de conversaciones, autenticación y orquestación de servicios.

## Archivos

### `controllers.py`
**Propósito:** Orquestador principal que coordina las operaciones del chatbot y se comunica con los servicios.

**Componentes principales:**
- **Funciones:**
  - `query(conf: Config, websocket)`: Procesa consultas del usuario mediante LangGraph, envía respuestas por WebSocket y gestiona el flujo de conversación.
  - `get_ollama_models()`: Retorna la lista de modelos disponibles en Ollama.
  - `new_chat(credentials, new_chat_name)`: Crea una nueva conversación para un usuario.
  - `get_chats(credentials)`: Obtiene todas las conversaciones de un usuario.
  - `remove_chat(chat_name, credentials)`: Elimina una conversación específica.
  - `get_conversation(credentials, chat_name)`: Recupera el historial de una conversación.
  - `update_chat_name(old_name, new_name, credentials)`: Renombra una conversación existente.
  - `get_conf(credentials)`: Obtiene la configuración del usuario.
  - `update_tools_conf(comfyui_conf, credentials)`: Guarda configuración de herramientas (ComfyUI/MCP).
  - `get_tools_conf(credentials)`: Recupera configuración de herramientas del usuario.

**Dependencias:** `services.graph_service`, `services.ollama_services`, `controllers.chats_controller`, `langchain_core.messages`

**Integración:** Usado por `routes/routes.py` para procesar todas las solicitudes de la API.

### `chats_controller.py`
**Propósito:** Gestión persistente de conversaciones y configuraciones de usuario en archivos JSON.

**Componentes principales:**
- **Funciones:**
  - `add_conversation(chat_name, credentials, user_input, bot_output)`: Agrega mensajes de usuario y bot al historial.
  - `clear_conversation(collection_name, credentials)`: Limpia el historial de una conversación.
  - `get_chats_list(credentials)`: Retorna lista de todas las conversaciones de un usuario.
  - `new_conversation(credentials, new_chat_name)`: Inicializa una nueva conversación vacía.
  - `remove_conversation(chat_name, credentials)`: Elimina una conversación del almacenamiento.
  - `get_user_conversation(credentials, chat_name)`: Recupera el historial completo de una conversación.
  - `update_name_chat(old_name, new_name, credentials)`: Renombra una conversación.
  - `get_configurations(credentials)`: Obtiene configuración general del usuario.
  - `get_tools_configuration(credentials)`: Recupera configuración específica de herramientas.
  - `save_tools_conf(tools_conf, credentials)`: Guarda configuración de herramientas (image_tools/mcp_tools).

**Dependencias:** `json`, `os`, `dotenv`, `langgraph.graph.MessagesState`

**Integración:** Usado por `controllers.py` para persistencia de datos.

### `credentials_controllers.py`
**Propósito:** Validación y verificación de tokens JWT para autenticación de usuarios.

**Componentes principales:**
- **Funciones:**
  - `get_current_user(credentials: HTTPAuthorizationCredentials)`: Extrae y valida token JWT, retorna el subject del usuario.
  - `verify_jws(credentials)`: Versión mejorada que maneja tokens de HTTP y WebSocket, valida expiración y firma del token.

**Constantes/Configuración:**
  - `SECRET_KEY`: Clave secreta para firma JWT (desde `.env`).
  - `ALGORITHM`: Algoritmo de encriptación (desde `.env`).
  - `security`: Instancia de `HTTPBearer` para extraer credenciales.

**Dependencias:** `jwt`, `fastapi.security`, `datetime`, `dotenv`

**Integración:** Usado como dependencia en todos los endpoints de `routes/routes.py`.

---

## Flujo de Datos

```
Routes → Controllers (orquestación) → chats_controller (persistencia)
                      ↓
              credentials_controllers (autenticación)
```

## Notas de Implementación

- Todas las funciones son `async` para compatibilidad con FastAPI.
- Las conversaciones se almacenan en JSON (ruta definida en `PATH_CONVERSATIONS` del `.env`).
- La autenticación es obligatoria en todos los endpoints excepto en WebSocket `/query` (validación interna).
