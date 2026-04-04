# Módulo Models - API Multimedia RAG

Contiene los esquemas Pydantic para validación de datos en la API Multimedia RAG.

---

## Archivos

### `schemas.py`
**Propósito:** Definición de esquemas Pydantic para validación de solicitudes y respuestas.

**Componentes principales:**

- **Clases:**

  - `UploadVideoSchema`: Schema para validar solicitudes de upload de videos.
    - **Campos:**
      - `file_id: Optional[str]`: ID único del video. Si no se proporciona, se genera un UUID automáticamente.
      - `metadata: Optional[dict]`: Metadatos adicionales del video (título, descripción, etiquetas, etc.). Default: `{}`
    - **Uso:** Ruta POST /upload-video

  - `VideoResponseSchema`: Schema para respuestas que incluyen información de video.
    - **Campos:**
      - `file_id: str`: ID único del video
      - `url: str`: URL o path para acceder al video
      - `metadata: dict`: Metadatos del video
      - `size: int`: Tamaño del archivo en bytes (ge=0)
      - `mime_type: str`: Tipo MIME del video (ej: video/mp4, video/webm)
      - `created_at: str`: Timestamp de creación en formato ISO 8601
    - **Uso:** Respuestas de upload y list de videos

  - `MessageSchema`: Schema para mensajes en conversaciones.
    - **Campos:**
      - `role: str`: Rol del emisor: 'user' o 'assistant'
      - `content: str`: Contenido del mensaje (min_length=1)
      - `timestamp: str`: Timestamp del mensaje en formato ISO 8601
      - `metadata: Optional[dict]`: Metadatos adicionales del mensaje (opcional)
    - **Uso:** Representa un mensaje individual dentro de una conversación

  - `ConversationSchema`: Schema para conversaciones completas.
    - **Campos:**
      - `id: str`: ID único de la conversación
      - `user_id: str`: ID del usuario propietario de la conversación
      - `title: Optional[str]`: Título opcional de la conversación
      - `messages: List[MessageSchema]`: Lista de mensajes de la conversación
      - `created_at: str`: Timestamp de creación en formato ISO 8601
      - `updated_at: str`: Timestamp de última actualización en formato ISO 8601
    - **Uso:** Persistencia y recuperación de historiales de conversaciones

  - `ListConversationsResponseSchema`: Schema para la respuesta de listar conversaciones.
    - **Campos:**
      - `conversations: List[ConversationSchema]`: Lista de conversaciones del usuario
      - `total: int`: Número total de conversaciones (ge=0)
    - **Uso:** Ruta GET /conversations

  - `ChatMessageSchema`: Schema para mensajes de chat en tiempo real.
    - **Campos:**
      - `input: str`: Mensaje del usuario (min_length=1)
      - `conversation_id: Optional[str]`: ID de conversación existente. Si no se proporciona, se crea una nueva.
      - `file_id: Optional[str]`: ID del video relacionado con el mensaje (opcional)
    - **Uso:** Ruta WebSocket /chat

**Dependencias:** `pydantic`, `typing`, `datetime`

**Integración:** Usado por todos los endpoints de la API para validación de entrada y salida.

---

## Relación entre Esquemas

```
UploadVideoSchema (input)
       ↓
[Procesamiento: upload video]
       ↓
VideoResponseSchema (output)

ChatMessageSchema (input - WebSocket)
       ↓
[Procesamiento: LangGraph agent]
       ↓
MessageSchema (output - parte de ConversationSchema)

ConversationSchema (persistencia)
       ↓
[GET /conversations]
       ↓
ListConversationsResponseSchema (output)
```
