from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UploadVideoSchema(BaseModel):
    """Schema para validar solicitudes de upload de videos.

    Se usa en la ruta POST /upload-video para recibir los metadatos
    adicionales del video subido por el usuario.
    """

    file_id: Optional[str] = Field(
        default=None,
        description="ID único del video. Si no se proporciona, se genera un UUID automáticamente",
    )
    metadata: Optional[dict] = Field(
        default_factory=dict,
        description="Metadatos adicionales del video (título, descripción, etiquetas, etc.)",
    )

    class Config:
        from_attributes = True


class VideoResponseSchema(BaseModel):
    """Schema para respuestas que incluyen información de video.

    Se usa en las respuestas de upload y list de videos para proporcionar
    información completa sobre el archivo almacenado.
    """

    file_id: str = Field(..., description="ID único del video")
    url: str = Field(..., description="URL o path para acceder al video")
    metadata: dict = Field(..., description="Metadatos del video")
    size: int = Field(..., ge=0, description="Tamaño del archivo en bytes")
    mime_type: str = Field(
        ..., description="Tipo MIME del video (ej: video/mp4, video/webm)"
    )
    created_at: str = Field(
        ..., description="Timestamp de creación en formato ISO 8601"
    )

    class Config:
        from_attributes = True


class MessageSchema(BaseModel):
    """Schema para mensajes en conversaciones.

    Representa un mensaje individual dentro de una conversación,
    ya sea del usuario o del asistente.
    """

    role: str = Field(..., description="Rol del emisor: 'user' o 'assistant'")
    content: str = Field(..., min_length=1, description="Contenido del mensaje")
    timestamp: str = Field(..., description="Timestamp del mensaje en formato ISO 8601")
    metadata: Optional[dict] = Field(
        default=None, description="Metadatos adicionales del mensaje (opcional)"
    )

    class Config:
        from_attributes = True


class ConversationSchema(BaseModel):
    """Schema para conversaciones completas.

    Representa una conversación completa con todos sus mensajes,
    usada para persistencia y recuperación de historiales.
    """

    id: str = Field(..., description="ID único de la conversación")
    user_id: str = Field(
        ..., description="ID del usuario propietario de la conversación"
    )
    title: Optional[str] = Field(
        default=None, description="Título opcional de la conversación"
    )
    messages: List[MessageSchema] = Field(
        default_factory=list, description="Lista de mensajes de la conversación"
    )
    created_at: str = Field(
        ..., description="Timestamp de creación en formato ISO 8601"
    )
    updated_at: str = Field(
        ..., description="Timestamp de última actualización en formato ISO 8601"
    )

    class Config:
        from_attributes = True


class ListConversationsResponseSchema(BaseModel):
    """Schema para la respuesta de listar conversaciones.

    Se usa en la ruta GET /conversations para devolver
    todas las conversaciones de un usuario con información de conteo.
    """

    conversations: List[ConversationSchema] = Field(
        default_factory=list, description="Lista de conversaciones del usuario"
    )
    total: int = Field(default=0, ge=0, description="Número total de conversaciones")

    class Config:
        from_attributes = True


class ChatMessageSchema(BaseModel):
    """Schema para mensajes de chat en tiempo real.

    Se usa en la ruta WebSocket /chat para recibir mensajes
    del usuario con contexto opcional de video.
    """

    input: str = Field(..., min_length=1, description="Mensaje del usuario")
    conversation_id: Optional[str] = Field(
        default=None,
        description="ID de conversación existente. Si no se proporciona, se crea una nueva",
    )
    file_id: Optional[str] = Field(
        default=None, description="ID del video relacionado con el mensaje (opcional)"
    )

    class Config:
        from_attributes = True


class CreateConversationSchema(BaseModel):
    """Schema para crear una nueva conversación.

    Se usa en la ruta POST /conversations para crear
    una conversación con un nombre/título proporcionado por el usuario.
    """

    name: str = Field(
        ..., min_length=1, description="Nombre/título de la nueva conversación"
    )

    class Config:
        from_attributes = True


class DeleteResponseSchema(BaseModel):
    """Schema para respuesta de eliminación.

    Se usa en las rutas DELETE para confirmar la eliminación exitosa
    de recursos como videos o conversaciones.
    """

    message: str = Field(..., description="Mensaje de confirmación de eliminación")

    class Config:
        from_attributes = True
