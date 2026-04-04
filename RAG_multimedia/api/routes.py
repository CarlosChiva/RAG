"""
Rutas REST para la API Multimedia RAG.

Este módulo define los endpoints HTTP para gestión de videos y conversaciones.
Todas las rutas están protegidas con autenticación JWT.
"""

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import aiofiles
import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from core.config import CONVERSATIONS_PATH
from core.credentials_controllers import get_current_user
from core.storage import LocalStorage, StorageError
from models.schemas import (
    ConversationSchema,
    CreateConversationSchema,
    DeleteResponseSchema,
    ListConversationsResponseSchema,
    VideoResponseSchema,
)

from .deps import get_conversation_manager, get_storage
from core.conversation_manager import ConversationManager

router = APIRouter()


# =============================================================================
# Conversations Routes
# =============================================================================


@router.get("/conversations")
async def list_conversations(
    user_id: str = Depends(get_current_user),
) -> ListConversationsResponseSchema:
    """
    Listar todas las conversaciones del usuario autenticado.

    Obtiene el historial completo de conversaciones de chat multimedia
    pertenecientes al usuario identificado por el token JWT.

    Args:
        user_id: ID del usuario autenticado (extraído del token JWT)

    Returns:
        ListConversationsResponseSchema: Lista de conversaciones con metadatos:
            - conversations: Lista de objetos ConversationSchema
            - total: Número total de conversaciones

    Raises:
        HTTPException:
            - 401: Si el token JWT es inválido o expirado
            - 500: Si ocurre un error al cargar las conversaciones

    Example:
        GET /conversations
        Headers: {"Authorization": "Bearer <token>"}

        Response:
        {
            "conversations": [
                {
                    "id": "conv-123",
                    "user_id": "user-456",
                    "title": "Análisis de video de producto",
                    "messages": [...],
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T11:45:00"
                }
            ],
            "total": 1
        }
    """
    try:
        # Path del archivo de conversaciones
        conversations_file = Path(CONVERSATIONS_PATH) / f"{user_id}.json"

        # Si el archivo no existe, retornar lista vacía
        if not conversations_file.exists():
            return ListConversationsResponseSchema(
                conversations=[],
                total=0,
            )

        # Leer el archivo de conversaciones
        async with aiofiles.open(conversations_file, "r") as f:
            content = await f.read()
            conversations_data = json.loads(content)

        # Filtrar conversaciones del usuario
        conversations = [
            conv for conv in conversations_data if conv.get("user_id") == user_id
        ]

        # Convertir a schemas y retornar
        conversations_schema = [
            ConversationSchema.model_validate(conv) for conv in conversations
        ]

        return ListConversationsResponseSchema(
            conversations=conversations_schema,
            total=len(conversations_schema),
        )
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al parsear archivo de conversaciones: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno al listar conversaciones: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user),
) -> ConversationSchema:
    """
    Obtener una conversación específica por ID.

    Recupera el historial completo de una conversación individual,
    verificando que pertenezca al usuario autenticado.

    Args:
        conversation_id: ID único de la conversación a recuperar
        user_id: ID del usuario autenticado (extraído del token JWT)

    Returns:
        ConversationSchema: Objeto de conversación con todos sus mensajes:
            - id: ID de la conversación
            - user_id: ID del usuario propietario
            - title: Título opcional de la conversación
            - messages: Lista de mensajes (user/assistant)
            - created_at: Timestamp de creación (ISO 8601)
            - updated_at: Timestamp de última actualización (ISO 8600)

    Raises:
        HTTPException:
            - 401: Si el token JWT es inválido o expirado
            - 404: Si la conversación no existe
            - 403: Si el usuario no es el propietario de la conversación
            - 500: Si ocurre un error al cargar la conversación

    Example:
        GET /conversations/conv-123
        Headers: {"Authorization": "Bearer <token>"}

        Response:
        {
            "id": "conv-123",
            "user_id": "user-456",
            "title": "Análisis de video",
            "messages": [
                {
                    "role": "user",
                    "content": "¿Qué muestra este video?",
                    "timestamp": "2024-01-15T10:30:00",
                    "metadata": {"file_id": "video-789"}
                },
                {
                    "role": "assistant",
                    "content": "El video muestra...",
                    "timestamp": "2024-01-15T10:30:15"
                }
            ],
            "created_at": "2024-01-15T10:30:00",
            "updated_at": "2024-01-15T11:45:00"
        }
    """
    try:
        # Path del archivo de conversaciones
        conversations_file = Path(CONVERSATIONS_PATH) / f"{user_id}.json"

        # Si el archivo no existe, la conversación no existe
        if not conversations_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Conversación '{conversation_id}' no encontrada",
            )

        # Leer el archivo de conversaciones
        async with aiofiles.open(conversations_file, "r") as f:
            content = await f.read()
            conversations_data = json.loads(content)

        # Buscar la conversación por ID
        conversation = None
        for conv in conversations_data:
            if conv.get("id") == conversation_id:
                conversation = conv
                break

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail=f"Conversación '{conversation_id}' no encontrada",
            )

        # Verificar que la conversación pertenece al usuario
        if conversation.get("user_id") != user_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para acceder a esta conversación",
            )

        return ConversationSchema.model_validate(conversation)
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al parsear archivo de conversaciones: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno al obtener conversación: {str(e)}"
        )


@router.post("/conversations", status_code=201)
async def create_conversation(
    body: CreateConversationSchema,
    user_id: str = Depends(get_current_user),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
) -> ConversationSchema:
    """
    Crear una nueva conversación para el usuario autenticado.

    Crea una conversación vacía con un título proporcionado por el usuario,
    generando un ID único y timestamp de creación.

    Args:
        body: Schema con el nombre/título de la conversación
        user_id: ID del usuario autenticado (extraído del token JWT)
        conversation_manager: Instancia del ConversationManager para persistencia

    Returns:
        ConversationSchema: Objeto de conversación creado con todos sus campos:
            - id: ID único generado (UUID)
            - user_id: ID del usuario propietario
            - title: Título proporcionado en la solicitud
            - messages: Lista vacía de mensajes
            - created_at: Timestamp de creación (ISO 8601)
            - updated_at: Timestamp de creación (ISO 8601)

    Raises:
        HTTPException:
            - 400: Si el nombre de la conversación es inválido
            - 401: Si el token JWT es inválido o expirado
            - 500: Si ocurre un error al crear la conversación

    Example:
        POST /api/conversations
        Headers: {"Authorization": "Bearer <token>"}
        Body:
        {
            "name": "Análisis de video de producto"
        }

        Response:
        {
            "id": "conv-123e4567-e89b-12d3-a456-426614174000",
            "user_id": "user-456",
            "title": "Análisis de video de producto",
            "messages": [],
            "created_at": "2024-01-15T10:30:00+00:00",
            "updated_at": "2024-01-15T10:30:00+00:00"
        }
    """
    try:
        # Usar conversation_manager.create() que genera UUID y timestamp internamente
        # y guarda la conversación, retornando el conversation_id
        conversation_id = await conversation_manager.create(user_id, body.name)

        # Obtener la conversación guardada para retornarla completa
        conversation_data = await conversation_manager.get(user_id, conversation_id)

        if conversation_data is None:
            raise HTTPException(
                status_code=500,
                detail="Error al crear conversación: no se pudo guardar la conversación",
            )

        # Convertir a ConversationSchema y retornar
        return ConversationSchema.model_validate(conversation_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear conversación: {str(e)}",
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
) -> DeleteResponseSchema:
    """
    Eliminar una conversación específica.

    Elimina permanentemente una conversación del historial del usuario.
    Solo el propietario de la conversación puede eliminarla.

    Args:
        conversation_id: ID único de la conversación a eliminar
        user_id: ID del usuario autenticado (extraído del token JWT)
        conversation_manager: Instancia del ConversationManager para persistencia

    Returns:
        DeleteResponseSchema: Mensaje de confirmación de eliminación:
            - message: "Conversación eliminada exitosamente"

    Raises:
        HTTPException:
            - 401: Si el token JWT es inválido o expirado
            - 403: Si el usuario no es el propietario de la conversación
            - 404: Si la conversación no existe
            - 500: Si ocurre un error durante la eliminación

    Example:
        DELETE /api/conversations/conv-123e4567-e89b-12d3-a456-426614174000
        Headers: {"Authorization": "Bearer <token>"}

        Response:
        {
            "message": "Conversación eliminada exitosamente"
        }
    """
    try:
        # 1. Cargar conversaciones del usuario
        conversations = await conversation_manager.list(user_id)

        # 2. Buscar conversación
        conversation = next(
            (c for c in conversations if c.get("id") == conversation_id), None
        )

        # 3. Verificar que existe
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")

        # 4. Verificar ownership
        if conversation.get("user_id") != user_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para eliminar esta conversación",
            )

        # 5. Eliminar
        deleted = await conversation_manager.delete(user_id, conversation_id)

        if not deleted:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la conversación: no se pudo eliminar",
            )

        # 6. Retornar respuesta
        return DeleteResponseSchema(message="Conversación eliminada exitosamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al eliminar conversación: {str(e)}",
        )


# =============================================================================
# Video Routes
# =============================================================================


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    metadata: str = Form("{}"),
    file_id: str = Form(""),
    user_id: str = Depends(get_current_user),
    storage: LocalStorage = Depends(get_storage),
) -> VideoResponseSchema:
    """
    Subir un archivo de video.

    Recibe un archivo de video mediante multipart/form-data y lo almacena
    en el sistema de almacenamiento local. Valida que el archivo sea un
    video soportado y genera un ID único si no se proporciona.

    Args:
        file: Archivo de video a subir (multipart/form-data)
        metadata: JSON string con metadatos adicionales (título, descripción, etc.)
        file_id: ID personalizado para el video (opcional, se genera UUID si no se proporciona)
        user_id: ID del usuario autenticado (extraído del token JWT)
        storage: Instancia del LocalStorage para guardar el archivo

    Returns:
        VideoResponseSchema: Información del video subido:
            - file_id: ID único del video
            - url: Path relativo para acceder al video
            - metadata: Metadatos del video
            - size: Tamaño del archivo en bytes
            - mime_type: Tipo MIME del video (ej: video/mp4)
            - created_at: Timestamp de creación (ISO 8601)

    Raises:
        HTTPException:
            - 400: Si el archivo no es un video válido o el metadata JSON es inválido
            - 401: Si el token JWT es inválido o expirado
            - 413: Si el archivo es demasiado grande
            - 500: Si ocurre un error durante el upload

    Example:
        POST /upload
        Headers: {"Authorization": "Bearer <token>"}
        Form Data:
            - file: <video.mp4>
            - metadata: '{"title": "Mi video", "description": "Descripción"}'
            - file_id: "video-custom-123" (opcional)

        Response:
        {
            "file_id": "video-custom-123",
            "url": "user-456/video-custom-123",
            "metadata": {
                "title": "Mi video",
                "description": "Descripción",
                "filename": "video.mp4"
            },
            "size": 15728640,
            "mime_type": "video/mp4",
            "created_at": "2024-01-15T10:30:00"
        }
    """
    try:
        # Validar que el archivo tenga nombre
        if not file.filename:
            raise HTTPException(
                status_code=400, detail="El archivo debe tener un nombre"
            )

        # Validar que sea un archivo de video por extensión
        allowed_extensions = {".mp4", ".webm", ".mov", ".avi", ".mkv", ".flv", ".wmv"}
        file_ext = file.filename.lower().split(".")[-1]
        if (
            f".{file_ext}" not in allowed_extensions
            and file_ext not in allowed_extensions
        ):
            # Verificar por MIME type también
            if not file.content_type or not file.content_type.startswith("video/"):
                raise HTTPException(
                    status_code=400,
                    detail=f"El archivo '{file.filename}' no es un video válido. "
                    f"Extensiones soportadas: {', '.join(allowed_extensions)}",
                )

        # Parsear metadata JSON
        try:
            metadata_dict: dict[str, Any] = json.loads(metadata)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400, detail=f"Metadata JSON inválido: {str(e)}"
            )

        # Generar file_id si no se proporciona
        if not file_id:
            file_id = str(uuid4())
        else:
            # Validar que file_id sea un UUID válido si se proporciona
            try:
                UUID(file_id)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="El file_id debe ser un UUID válido"
                )

        # Leer contenido del archivo
        try:
            file_content = await file.read()
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error al leer el archivo: {str(e)}"
            )

        # Validar tamaño del archivo (máximo 500MB)
        max_size = 500 * 1024 * 1024  # 500MB
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"El archivo es demasiado grande. Tamaño máximo: 500MB",
            )

        # Agregar filename al metadata
        metadata_dict["filename"] = file.filename
        metadata_dict["mime_type"] = file.content_type or "video/mp4"

        # Subir archivo usando storage
        try:
            relative_path = await storage.upload(
                file_id=file_id,
                user_id=user_id,
                file_content=file_content,
                metadata=metadata_dict,
            )
        except StorageError as e:
            raise HTTPException(
                status_code=500, detail=f"Error al guardar el video: {str(e)}"
            )

        # Crear timestamp
        created_at = datetime.utcnow().isoformat()

        # Retornar respuesta
        return VideoResponseSchema(
            file_id=file_id,
            url=relative_path,
            metadata=metadata_dict,
            size=len(file_content),
            mime_type=file.content_type or "video/mp4",
            created_at=created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno durante el upload: {str(e)}"
        )


@router.get("/media/{file_id}")
async def get_video(
    file_id: str,
    user_id: str = Depends(get_current_user),
    storage: LocalStorage = Depends(get_storage),
) -> FileResponse:
    """
    Obtener un archivo de video.

    Descarga un archivo de video específico y lo retorna como FileResponse
    con el MIME type correcto para reproducción en el navegador.

    Args:
        file_id: ID único del video a descargar
        user_id: ID del usuario autenticado (extraído del token JWT)
        storage: Instancia del LocalStorage para leer el archivo

    Returns:
        FileResponse: Archivo de video con headers correctos:
            - content-type: MIME type del video (ej: video/mp4)
            - content-disposition: inline para reproducción en navegador
            - filename: Nombre original del archivo

    Raises:
        HTTPException:
            - 401: Si el token JWT es inválido o expirado
            - 403: Si el usuario no es el propietario del video
            - 404: Si el video no existe
            - 500: Si ocurre un error al leer el archivo

    Example:
        GET /media/video-123
        Headers: {"Authorization": "Bearer <token>"}

        Response:
        FileResponse con el video binario
        Headers:
            - Content-Type: video/mp4
            - Content-Disposition: inline; filename="video.mp4"
    """
    try:
        # Obtener información del archivo para verificar ownership
        file_info = await storage.get_file_info(file_id, user_id)

        if file_info is None:
            raise HTTPException(
                status_code=404, detail=f"Video '{file_id}' no encontrado"
            )

        # Verificar que el video pertenece al usuario
        if file_info.get("user_id") != user_id:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para acceder a este video"
            )

        # Descargar el archivo
        try:
            file_content, mime_type = await storage.download(file_id, user_id)
        except StorageError as e:
            raise HTTPException(
                status_code=500, detail=f"Error al leer el video: {str(e)}"
            )

        # Obtener filename del metadata o usar file_id
        filename = file_info.get("filename", file_id)

        # Retornar FileResponse
        from io import BytesIO

        return FileResponse(
            content=BytesIO(file_content),
            filename=filename,
            media_type=mime_type,
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno al obtener video: {str(e)}"
        )


@router.delete("/media/{file_id}")
async def delete_video(
    file_id: str,
    user_id: str = Depends(get_current_user),
    storage: LocalStorage = Depends(get_storage),
) -> dict[str, str]:
    """
    Eliminar un archivo de video.

    Elimina permanentemente un archivo de video del sistema de almacenamiento.
    Solo el propietario del video puede eliminarlo.

    Args:
        file_id: ID único del video a eliminar
        user_id: ID del usuario autenticado (extraído del token JWT)
        storage: Instancia del LocalStorage para eliminar el archivo

    Returns:
        dict[str, str]: Mensaje de confirmación:
            - message: "Video eliminado exitosamente"

    Raises:
        HTTPException:
            - 401: Si el token JWT es inválido o expirado
            - 403: Si el usuario no es el propietario del video
            - 404: Si el video no existe
            - 500: Si ocurre un error durante la eliminación

    Example:
        DELETE /media/video-123
        Headers: {"Authorization": "Bearer <token>"}

        Response:
        {
            "message": "Video eliminado exitosamente"
        }
    """
    try:
        # Verificar que el video existe y pertenece al usuario
        file_info = await storage.get_file_info(file_id, user_id)

        if file_info is None:
            raise HTTPException(
                status_code=404, detail=f"Video '{file_id}' no encontrado"
            )

        # Verificar que el video pertenece al usuario
        if file_info.get("user_id") != user_id:
            raise HTTPException(
                status_code=403, detail="No tienes permiso para eliminar este video"
            )

        # Eliminar el archivo
        try:
            deleted = await storage.delete(file_id, user_id)
        except StorageError as e:
            raise HTTPException(
                status_code=500, detail=f"Error al eliminar el video: {str(e)}"
            )

        if not deleted:
            raise HTTPException(
                status_code=404, detail=f"Video '{file_id}' no encontrado"
            )

        return {"message": "Video eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno al eliminar video: {str(e)}"
        )
