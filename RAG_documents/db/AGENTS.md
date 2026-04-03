# Capa de Datos y Procesamiento

Esta carpeta implementa la infraestructura de base de datos vectorial (ChromaDB), procesamiento de documentos PDF/DOCX/TXT, y configuración de modelos LLM para el sistema RAG.

## Archivos

### `chroma_manager.py`
**Propósito:** Gestión de operaciones CRUD sobre colecciones en ChromaDB con integración de embeddings.

**Componentes principales:**
- **Funciones:**
  - `get_collections(cli) -> list[str]`: Lista nombres de todas las colecciones existentes.
  - `add_pdf_to_collection(filename, name_collection, cli) -> dict[str, str]`: 
    - Crea colección si no existe
    - Carga documento mediante `tools.load_document()`
    - Divide texto en chunks mediante `tools.text_split()`
    - Genera embeddings con `tools.init_embedding_model()`
    - Persiste en ChromaDB con IDs únicos (UUID)
  - `get_vectorstore(cli, collection_name) -> Chroma`: Devuelve instancia Chroma configurada como vectorstore para retrieval.
  - `remove_collection_db(collection_name, cli) -> dict[str, str]`: Elimina colección de ChromaDB.

**Dependencias:** `langchain_chroma`, `db.tools`, `uuid`, `logging`

**Integración:** Usado por `controllers/controllers.py` para todas las operaciones de persistencia.

---

### `chroma.py`
**Propósito:** Construcción de cadenas LangChain para generación de respuestas con contexto recuperado.

**Componentes principales:**
- **Funciones:**
  - `get_chain(model, vector_store) -> RunnableBinding`: 
    - Configura prompt con instrucciones en español para responder solo desde contexto
    - Crea retriever con estrategia MMR (Maximal Marginal Relevance), k=3 documentos
    - Combina retriever + chain de QA con `create_retrieval_chain()`
    - Soporta historial de chat mediante variable `chat_history`

**Prompt Template:** Instrucciones estrictas para:
- Usar solo información del contexto proporcionado
- Responder "no tengo información suficiente" si el contexto no es relevante
- Formato de salida en Markdown
- Considerar historial de conversaciones previas

**Dependencias:** `langchain.chains`, `langchain.prompts`, `langchain_core.runnables`

**Integración:** Invocado por `controllers.querier()` para cada consulta del usuario.

---

### `chroma_cli.py`
**Propósito:** Fábrica de clientes ChromaDB con persistencia aislada por usuario.

**Componentes principales:**
- **Funciones:**
  - `get_chroma_client(credentials=None) -> Client`: Crea cliente Chroma persistente en ruta `{PERSIST_DIRECTORY}/{credentials}/` para aislamiento de datos entre usuarios.

**Dependencias:** `chromadb`, `dotenv`, `os`

**Integración:** Punto de entrada único para acceso a ChromaDB en toda la aplicación.

---

### `model_conf.py`
**Propósito:** Configuración singleton del modelo LLM mediante Ollama.

**Componentes principales:**
- **Clases:**
  - `RagModel`: Implementación del patrón Singleton para evitar instanciaciones múltiples del modelo.
    - **Atributos:**
      - `_instance`: Referencia única a la instancia
      - `model`: Instancia de `OllamaLLM` con temperature=0 (respuestas deterministas)
    - **Métodos:**
      - `__new__()`: Controla creación única de instancia
      - `__init__()`: Inicializa modelo desde variable de entorno `MODEL`
      - `get_model() -> OllamaLLM`: Devuelve instancia configurada

**Dependencias:** `langchain_ollama`, `dotenv`, `os`

**Integración:** Usado por `controllers.querier()` para obtener modelo en cada consulta.

---

### `pdf_tools.py`
**Propósito:** Extracción avanzada de texto, tablas e imágenes desde documentos PDF con OCR.

**Componentes principales:**
- **Funciones:**
  - `text_extraction(element) -> tuple[any, list[str]]`: Extrae texto y formatos de fuente de elementos PDF.
  - `extract_table(pdf_path, page_num, table_num) -> any`: Extrae tabla específica de página PDF.
  - `table_converter(table) -> str`: Convierte tabla a formato Markdown con separadores `|`.
  - `is_element_inside_any_table(element, page, tables) -> bool`: Detecta si elemento está dentro de tabla.
  - `find_table_for_element(element, page, tables) -> (int|None)`: Identifica índice de tabla que contiene elemento.
  - `crop_image(element, pageObj) -> None`: Recorta imagen de PDF a archivo separado.
  - `convert_to_images(input_file) -> None`: Convierte PDF a imagen PNG.
  - `image_to_text(image_path) -> str`: Aplica OCR con Tesseract para extraer texto de imágenes.
  - `read_document(pdf_path) -> dict`: Procesa PDF completo extrayendo texto, tablas e imágenes por página.
  - `pdf_text_extraction(file) -> str`: Función async que recibe UploadFile, guarda temporalmente, extrae texto y limpia duplicados.

**Dependencias:** `pdfminer.six`, `pdfplumber`, `PyPDF2`, `pytesseract`, `PIL`, `pdf2image`, `tempfile`, `os`

**Integración:** Usado por `tools.load_document()` para procesamiento de PDF.

---

### `tools.py`
**Propósito:** Utilidades para carga de documentos multi-formato, chunking y configuración de embeddings.

**Componentes principales:**
- **Funciones:**
  - `load_document(file: UploadFile) -> str`: 
    - Soporta formatos: `.txt`, `.pdf`, `.docx`
    - TXT: Decodificación UTF-8 directa
    - PDF: Extracción mediante `pdf_tools.pdf_text_extraction()`
    - DOCX: Parsing con `python-docx`, join de párrafos
  - `text_split(documents, chunk_size=1000, chunk_overlap=20) -> list[Document]`: 
    - Crea `Document` LangChain con metadata de fuente
    - Aplica `RecursiveCharacterTextSplitter` con tokenizador tiktoken
    - Retorna lista de chunks para embedding
  - `init_embedding_model() -> OllamaEmbeddings`: Inicializa modelo de embeddings desde variable `EMBEDD_MODEL`.

**Dependencias:** `langchain`, `langchain_ollama`, `docx`, `db.pdf_tools`, `fastapi`, `io`, `os`

**Integración:** Usado por `chroma_manager.add_pdf_to_collection()` para procesamiento de documentos.

---

## Arquitectura de Flujo de Datos

```
UploadFile (PDF/DOCX/TXT)
    ↓
tools.load_document() → pdf_tools.pdf_text_extraction() (solo PDF)
    ↓
tools.text_split() → chunks de 1000 tokens con overlap de 20
    ↓
chroma_manager.add_pdf_to_collection()
    ↓
tools.init_embedding_model() → OllamaEmbeddings
    ↓
ChromaDB (persistencia por usuario)
    ↓
chroma_manager.get_vectorstore() → retrieval MMR k=3
    ↓
chroma.get_chain() → LangChain con prompt contextual
    ↓
model_conf.RagModel → OllamaLLM (llama3.2)
    ↓
Respuesta con contexto + historial de chat
```
