# Servicios del Chatbot

Esta carpeta contiene la infraestructura de ejecución del chatbot, incluyendo el grafo LangGraph, servicios de integración con Ollama y los nodos de procesamiento.

## Subcarpetas

- **`nodes/`**: Nodos del grafo LangGraph que implementan chat básico, generación de imágenes y agentes MCP.  
  → [Ver documentación detallada](./nodes/AGENTS.md)

## Archivos

### `graph_service.py`
**Propósito:** Construcción y compilación del grafo de estado LangGraph que orquesta el flujo de ejecución del chatbot.

**Componentes principales:**
- **Funciones:**
  - `routing_logic(state, config)`: Función de enrutamiento condicional que decide el siguiente nodo basado en la configuración de tools.
    - Sin tools → `chatbot`
    - `type="image"` → `image_generator`
    - `type="mcp"` → `mcp_agent`

- **Componentes del Grafo:**
  - `builder`: Instancia de `StateGraph` con schema `MessagesState` y config schema `Config`.
  - `graph`: Grafo compilado con checkpoint `MemorySaver` para persistencia de conversaciones.

- **Nodos registrados:**
  - `orquestator`: Punto de entrada, carga historial de conversación.
  - `chatbot`: Chat básico con Ollama.
  - `image_generator`: Generación de imágenes vía ComfyUI.
  - `mcp_agent`: Agente con herramientas MCP.

**Dependencias:** `langgraph.graph`, `langgraph.checkpoint.memory`, `services.nodes.nodes`, `services.state`

**Integración:** Exportado como `graph` y usado por `controllers/controllers.py` en la función `query()`.

### `ollama_services.py`
**Propósito:** Integración con Ollama para listar modelos disponibles localmente.

**Componentes principales:**
- **Funciones:**
  - `get_models()`: Lista todos los modelos instalados en Ollama.
    - Retorna `list[dict]` con `name` y `size` (parameter_size) de cada modelo.

**Dependencias:** `ollama` (cliente oficial)

**Integración:** Usado por `controllers/controllers.py` en `get_ollama_models()`.

### `state.py`
**Propósito:** Definición del schema de configuración para el grafo LangGraph.

**Componentes principales:**
- **Clases:**
  - `Config` (TypedDict): Schema de configuración del grafo con campos:
    - `model`: Nombre del modelo Ollama a usar.
    - `conversation_id`: Identificador único de la conversación.
    - `tools`: Dict con configuración de herramientas (image/mcp).

**Dependencias:** `typing_extensions.TypedDict`, `langgraph.graph.message`

**Integración:** Usado como `config_schema` en `graph_service.py`.

---

## Arquitectura

```
graph_service (orquestación)
    ├── nodes/nodes.py (lógica de negocio)
    ├── ollama_services.py (integración externa)
    └── state.py (schema de configuración)
```

## Flujo de Ejecución

1. `controllers.query()` invoca `graph.astream()` con messages y config.
2. El grafo ejecuta `orquestator` → `routing_logic()` → nodo específico.
3. Cada nodo procesa y retorna mensajes actualizados.
4. El checkpoint `MemorySaver` persiste el estado por `thread_id`.

## Notas de Implementación

- El grafo usa `MemorySaver` para persistencia en memoria (no sobrevive reinicios).
- La configuración se pasa en `config["configurable"]` (thread_id, websocket, conversation, tools).
- El enrutamiento es dinámico y se evalúa en tiempo de ejecución.
