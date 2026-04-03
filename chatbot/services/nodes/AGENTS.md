# Nodos del Grafo de LangGraph

Esta carpeta contiene los nodos que componen el grafo de ejecución del chatbot, implementando la lógica de chat básico, generación de imágenes y agentes MCP.

## Archivos

### `nodes.py`
**Propósito:** Implementación de los nodos del grafo LangGraph que procesan diferentes tipos de consultas (chat, imágenes, MCP).

**Componentes principales:**
- **Funciones (Nodos del Grafo):**
  - `orquestator(state: MessagesState, config: Config)`: Nodo inicial que carga el historial de conversación y prepara el estado para el procesamiento.
    - Carga mensajes previos desde `chats_controller.get_user_conversation`.
    - Convierte mensajes JSON a `AIMessage`/`HumanMessage`.
    - Mantiene lista de `active_users` para optimizar cargas.

  - `chatbot_node(state: MessagesState, config: Config)`: Nodo para chat básico con Ollama.
    - Usa `ChatOllama` con modelo especificado en config.
    - Streaming de respuesta por WebSocket con detección de "thinking" (tags <think>/</think>).
    - Guarda conversación completa mediante `chats_controller.add_conversation`.

  - `mcp_agent(state: MessagesState, config)`: Nodo para agentes con herramientas MCP.
    - Crea agente reactivo con `create_react_agent` de LangGraph.
    - Conecta a servidores MCP mediante `MultiServerMCPClient`.
    - Ejecuta herramientas y retorna respuesta con streaming.

  - `image_generator(state: MessagesState, config)`: Nodo para generación de imágenes con ComfyUI.
    - Extrae configuración de `api_json` y `positive_prompt_node`.
    - Conecta WebSocket a ComfyUI y ejecuta workflow.
    - Codifica imágenes en base64 y las envía al cliente.
    - Manejo robusto de errores (KeyError, excepciones de WebSocket).

  - `send_message(websocket, msg_chunk)`: Función auxiliar para streaming de respuestas.
    - Detecta tool_calls y envía eventos de uso de herramientas.
    - Maneja estados de "thinking" para respuestas con razonamiento.
    - Envía tokens en tiempo real al cliente WebSocket.

- **Funciones Auxiliares:**
  - `save_messages_state_to_file(messages_state, file_path)`: Serializa estado a JSON.
  - `load_messages_state_from_file(file_path, first_user_input)`: Deserializa estado desde JSON.

**Constantes/Configuración:**
  - `active_users`: Lista global que rastrea usuarios con conversaciones cargadas.
  - `thinking`: Flag global para detectar estado de razonamiento del modelo.

**Dependencias:** `langchain_ollama.ChatOllama`, `langgraph.graph`, `langchain_core.messages`, `websocket`, `langgraph.prebuilt.create_react_agent`, `langchain_mcp_adapters`, `controllers.chats_controller`, `.images_utils`

**Integración:** Importado por `services/graph_service.py` para construir el grafo.

### `images_utils.py`
**Propósito:** Utilidades para comunicación con ComfyUI y procesamiento de imágenes generadas.

**Componentes principales:**
- **Funciones:**
  - `queue_prompt(prompt, prompt_id, client_id)`: Envía workflow a ComfyUI vía HTTP POST.
  - `get_image(filename, subfolder, folder_type)`: Descarga imagen desde ComfyUI como bytes.
  - `get_history(prompt_id)`: Obtiene historial de ejecución de un prompt desde ComfyUI.
  - `get_images(ws, prompt, client_id)`: Orquesta la generación completa de imágenes.
    - Envía prompt y espera completitud vía WebSocket.
    - Recupera historial y descarga todas las imágenes generadas.
    - Retorna dict `{node_id: [image_bytes]}`.
  - `validate_image_config(config)`: Valida que la configuración tenga todos los campos necesarios para generación de imágenes.

**Dependencias:** `urllib.request`, `urllib.parse`, `json`, `uuid`, `dotenv`

**Integración:** Usado exclusivamente por `nodes.py` en el nodo `image_generator`.

---

## Arquitectura del Grafo

```
START → orquestator → [routing_logic] → chatbot | image_generator | mcp_agent → END
```

El enrutamiento se basa en `tools_config.type`:
- Sin tools → `chatbot`
- `type="image"` → `image_generator`
- `type="mcp"` → `mcp_agent`

## Flujo de Datos

1. **Entrada:** User input via WebSocket → `orquestator`
2. **Procesamiento:** 
   - Carga historial (si es primer mensaje)
   - Enrutamiento según configuración de tools
3. **Ejecución:** 
   - Chat básico → `chatbot_node`
   - Imágenes → `image_generator` + ComfyUI
   - Herramientas → `mcp_agent` + MCP servers
4. **Salida:** Streaming por WebSocket → Cliente
5. **Persistencia:** `chats_controller.add_conversation`

## Notas de Implementación

- Todos los nodos son `async` para streaming en tiempo real.
- El WebSocket se pasa en `config["configurable"]["websocket"]`.
- Las imágenes se codifican en base64 para transmisión WebSocket.
- El estado `thinking` se detecta por tags XML `<think>`/`</think>` en el output del modelo.
