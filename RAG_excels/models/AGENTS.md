# Capa de Modelos

Esta carpeta define las estructuras que representan el agente LLM, sus herramientas y la gestión de sesiones de usuario.

## Archivos

### `agent.py`
**Propósito:** Configuración y construcción del agente LangGraph con LLM Ollama y herramientas para análisis de Excel.

**Componentes principales:**
- **Clase:**
  - `Agent`: Constructor que inicializa un agente LangGraph con modelo `gpt-oss` de Ollama (contexto de 70k tokens, reasoning habilitado).
    - **Métodos clave:**
      - `get_model()`: Configura `ChatOllama` con parámetros de razonamiento.
      - `build_agent()`: Crea el agente con `create_agent()`, herramientas y checkpointer `MemorySaver`.
      - `get_prompt()`: Retorna el prompt de sistema detallado con instrucciones de uso de herramientas, flujo de trabajo y reglas de seguridad.

**Dependencias:** `langgraph`, `langchain_ollama`, `langchain`, `models.tools`
**Integración:** Instanciado por `models.user.UserSession` para cada usuario/archivo.

### `tools.py`
**Propósito:** Define las 6 herramientas (LangChain tools) que el agente LLM puede invocar para interactuar con archivos Excel.

**Componentes principales:**
- **Variables globales:**
  - `retriever`: Retriever FAISS para búsqueda semántica.
  - `vectorstore`: Vector store FAISS con embeddings del Excel.
  - `current_file_path`: Ruta del archivo actual cargado.
  - `BACKUP_DIR`: Directorio para backups automáticos ("backups_excel").

- **Funciones de utilidad:**
  - `set_retriever(global_retriever)`: Establece el retriever global.
  - `set_vectorstore(global_vectorstore)`: Establece el vectorstore global.
  - `create_backup(file_path: str) -> str`: Crea backup con timestamp antes de ediciones.
  - `initialize(file_path: str, use_existing: bool)`: Inicializa vectorstore y retriever para un archivo.
  - `parse_cell_reference(cell_ref: str)`: Parsea referencias tipo "A1", "AB123" a índices (row, col).
  - `column_index_to_letter(col_idx: int) -> str`: Convierte índice de columna a letra Excel (0→A, 26→AA).

- **Herramientas (tools):**
  - `buscar_en_excel(file_path, query, filter_sheet)`: Búsqueda semántica usando FAISS retriever. Retorna contexto formateado y documentos.
  - `editar_excel(file_path, hoja, celda, nuevo_valor, confirmacion)`: Edita celda específica con validación de seguridad (requiere `confirmacion='SI'`), crea backup automático.
  - `explorar_excel(file_path, hoja, mostrar_columnas)`: Explora estructura del Excel (hojas, dimensiones, columnas, tipos de datos, preview).
  - `buscar_columna(file_path, nombre_columna, hoja)`: Busca columnas por nombre (parcial, case-insensitive) con estadísticas.
  - `buscar_por_filtro(file_path, columna, valor_busqueda, hoja, operador, max_resultados)`: Filtra filas por criterios (igual, contiene, mayor, menor, etc.).
  - `consulta_libre_excel(file_path, consulta, incluir_contexto)`: Herramienta más potente: combina búsqueda semántica + análisis estructural + estadísticas.

**Dependencias:** `langchain.tools`, `pandas`, `langchain_core.documents`, `services.excel_loader`
**Integración:** Exportado por `get_tools()` y usado en `agent.py`. Inicializado desde `services.excel_loader`.

### `user.py`
**Propósito:** Gestiona sesiones de usuario con agente personal por archivo, manejando streaming de respuestas vía WebSocket.

**Componentes principales:**
- **Clase:**
  - `UserSession` (Singleton por instancia):
    - **Atributos:**
      - `filename`: Ruta del archivo Excel.
      - `user_id`: Identificador del usuario (thread_id para LangGraph).
      - `personal_agent`: Instancia de `Agent` específica para este archivo.
      - `thinking`: Flag para estado de razonamiento.
    - **Métodos clave:**
      - `send_message(websocket, msg_chunk)`: Serializa chunks de respuesta (tool calls, reasoning, content) y envía por WebSocket.
      - `query_agent(websocket, query)`: Ejecuta la consulta en el agente con streaming, delegando a `send_message()` para cada chunk.

**Dependencias:** `models.agent`, `fastapi.WebSocket`
**Integración:** Instanciado por `services.excel_service.ExcelAgent` por cada usuario/archivo.
