# API del Chatbot

Este directorio contiene la aplicación FastAPI que implementa un chatbot con integración Ollama, generación de imágenes (ComfyUI) y agentes MCP. Todas las rutas están protegidas por autenticación JWT.

## Resumen Ejecutivo

API REST y WebSocket para interacción con modelos LLM locales vía Ollama. Soporta conversaciones persistentes, generación de imágenes y ejecución de herramientas MCP mediante un grafo LangGraph con enrutamiento dinámico.

## Subcarpetas

- **`controllers/`**: Lógica de negocio para orquestación de servicios, gestión de conversaciones y autenticación.  
  → [Ver documentación detallada](./controllers/AGENTS.md)

- **`routes/`**: Definición de endpoints REST y WebSocket con sus handlers y validaciones.  
  → [Ver documentación detallada](./routes/AGENTS.md)

- **`services/`**: Infraestructura de ejecución con grafo LangGraph, integración Ollama y nodos de procesamiento.  
  → [Ver documentación detallada](./services/AGENTS.md)

## Archivos de Configuración

- **`main.py`**: Punto de entrada de la aplicación FastAPI.
  - Configura CORS con origen `*` (ajustable en producción).
  - Incluye el router definido en `routes/routes.py`.
  - Se ejecuta vía `uvicorn` en entorno Docker.

- **`config.py`**: Modelos Pydantic para validación de datos.
  - **`Config`**: Modelo principal con campos:
    - `credentials`: Token JWT del usuario.
    - `conversation`: Nombre de la conversación activa.
    - `modelName`: Modelo Ollama a usar (ej: "llama2").
    - `userInput`: Consulta del usuario.
    - `tools`: Configuración opcional de herramientas (image/mcp).

- **`requirements.txt`**: Dependencias legacy del proyecto.
  - **Core:** `fastapi`, `uvicorn`, `pydantic`
  - **AI/LLM:** `langgraph`, `langchain-ollama`, `langchain-mcp-adapters`
  - **Autenticación:** `PyJWT`
  - **Websocket:** `websocket-client`
  - **Ollama:** `ollama` (cliente oficial)
  - **Total:** 72 dependencias
  - ⚠️ Obsoleto: Migrado a pyproject.toml + uv.lock

- **`pyproject.toml`**: Configuración del proyecto en formato PYPA moderno.
  - name: `chatbot`
  - version: `0.1.0`
  - requires-python: `>=3.12`
  - 72 dependencias declaradas

- **`uv.lock`**: Lockfile generado por UV para reproducibilidad.
  - Tamaño: `216 KB`
  - Paquetes resueltos: `78` (72 directas + 6 transitive)
  - Hash SHA256 para builds idénticos
  - Generado: abril 2026

- **`Dockerfile`**: Imagen de contenedor para despliegue con UV strategy.
  - **Corrección migración UV:** Renombrado desde `dockerfile` (estándar Docker) ✅
  - **Gestor de paquetes:** UV (migrado de pip en abril 2026) ✅
  - Basado en imagen Python oficial
  - Estrategia: `uv sync --locked --compile-bytecode`
  - SIZE: `402 MB` (< 500MB ideal, optimizado con UV)
  - ENTRYPOINT: `["uv", "run", "--"]` con wrapper UV
  - Expone puerto de la API (configurable)

- **`README.md`**: Documentación de usuario con descripción de endpoints y ejemplos de uso.

---

## Endpoints Principales

### WebSocket
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/query` | WS | Comunicación en tiempo real con el chatbot (streaming de respuestas) |

### REST API (JWT requerido)
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/get_ollama_models` | GET | Lista modelos Ollama disponibles |
| `/new_chat` | POST | Crea nueva conversación |
| `/get_chats` | GET | Lista todas las conversaciones del usuario |
| `/remove-chat` | POST | Elimina una conversación |
| `/get-conversation` | GET | Recupera historial de una conversación |
| `/update-chat-name` | POST | Renombra una conversación |
| `/get-configurations` | POST | Obtiene configuración del usuario |
| `/update_tools_conf` | POST | Actualiza configuración de herramientas |
| `/get_tools_conf` | GET | Recupera configuración de herramientas |

---

## Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │ ─── │   Routes     │ ─── │ Controllers │
│  (WebSocket)│     │  (FastAPI)   │     │  (Lógica)   │
└─────────────┘     └──────────────┘     └─────────────┘
                                              │
                                              ↓
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Ollama/    │ ←── │   Services   │ ←── │   Nodes     │
│  ComfyUI/   │     │ (LangGraph)  │     │(Chat/Image/ │
│    MCP      │     └──────────────┘     │   MCP Agent)│
└─────────────┘                          └─────────────┘
```

## Flujo de Ejecución Típico

1. **Autenticación:** Cliente obtiene JWT desde `/log-in` o `/sing-up` (en container ddbb).
2. **Conexión:** Cliente conecta WebSocket a `/query` con token en payload.
3. **Enrutamiento:** 
   - `orquestator` carga historial de conversación.
   - `routing_logic` decide nodo según `tools.type`.
4. **Procesamiento:**
   - Chat básico → `chatbot_node` → Ollama.
   - Imágenes → `image_generator` → ComfyUI.
   - Herramientas → `mcp_agent` → MCP servers.
5. **Streaming:** Respuesta enviada en tiempo real por WebSocket.
6. **Persistencia:** Conversación guardada en JSON por usuario.

## Notas Importantes

- **Autenticación:** Todos los endpoints requieren JWT válido. Tokens son obtenidos del container `ddbb`.
- **CORS:** Configurado para permitir todos los orígenes (`*`). Debe restringirse en producción.
- **Persistencia:** Conversaciones almacenadas en JSON (no base de datos). Se pierden al reiniciar si no se montan volumes.
- **Streaming:** El WebSocket permite recibir tokens en tiempo real con detección de estados (thinking, tool usage).
- **Tools:** Soporta dos tipos:
  - `image`: Generación de imágenes vía ComfyUI (requiere `SERVER_ADDRESS` configurado).
  - `mcp`: Agentes con herramientas MCP (requiere configuración `api_json`).
