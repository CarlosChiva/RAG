"""
Dependencias de inyección para la API Multimedia RAG.

Este módulo define dependencias reutilizables que se usarán en las rutas de FastAPI
para la autenticación, gestión de almacenamiento y conversaciones.
"""

from typing import Tuple, TYPE_CHECKING
from fastapi import Depends

from core.credentials_controllers import get_current_user
from core import LocalStorage

# Import condicional para evitar error si ConversationManager no existe aún
#if TYPE_CHECKING:
from core.conversation_manager import ConversationManager


async def get_current_user(user_id: str = Depends(get_current_user)) -> str:
    """
    Obtiene el user_id del token JWT.

    Esta dependencia valida el token JWT en el header Authorization y extrae
    el user_id del payload. Se usa en todas las rutas protegidas que requieren
    autenticación de usuario.

    Args:
        user_id: ID del usuario extraído del token JWT por verify_jwt

    Returns:
        str: ID del usuario autenticado

    Raises:
        HTTPException: Si el token JWT es inválido o expirado
    """
    return user_id


async def get_storage() -> LocalStorage:
    """
    Obtiene una instancia del LocalStorage.

    Esta dependencia proporciona una instancia del gestor de almacenamiento
    local para operaciones de archivos multimedia. Cada llamada crea una nueva
    instancia para asegurar aislamiento entre peticiones.

    Returns:
        LocalStorage: Instancia del storage manager

    Note:
        LocalStorage maneja la estructura de directorios por usuario y
        operaciones de upload/download/delete de archivos multimedia.
    """
    return LocalStorage()


async def get_conversation_manager() -> ConversationManager:
    """
    Obtiene una instancia del ConversationManager.

    Esta dependencia proporciona una instancia del gestor de conversaciones
    para mantener el historial de chats de multimedia por usuario. Cada llamada
    crea una nueva instancia que se inicializa con el historial del usuario.

    Returns:
        ConversationManager: Instancia del conversation manager

    Note:
        ConversationManager maneja el historial de conversaciones en JSON
        con persistencia por usuario.
    """
    return ConversationManager()


async def get_current_user_and_storage(
    user_id: str = Depends(get_current_user),
    storage: LocalStorage = Depends(get_storage),
) -> Tuple[str, LocalStorage]:
    """
    Obtiene el user_id y una instancia del LocalStorage.

    Esta dependencia combinada es útil para rutas que requieren tanto
    autenticación de usuario como acceso al almacenamiento, como upload
    y download de archivos multimedia.

    Args:
        user_id: ID del usuario autenticado (obtenido de get_current_user)
        storage: Instancia del LocalStorage (obtenida de get_storage)

    Returns:
        Tuple[str, LocalStorage]: Tupla con (user_id, storage)

    Example:
        async def upload_file(
            file: UploadFile,
            user_id_and_storage: Tuple[str, LocalStorage] = Depends(get_current_user_and_storage)
        ):
            user_id, storage = user_id_and_storage
            # Usar user_id y storage
    """
    return (user_id, storage)


async def get_current_user_and_conversation_manager(
    user_id: str = Depends(get_current_user),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
) -> Tuple[str, ConversationManager]:
    """
    Obtiene el user_id y una instancia del ConversationManager.

    Esta dependencia combinada es útil para rutas que requieren tanto
    autenticación de usuario como acceso al historial de conversaciones,
    como las rutas de chat multimedia.

    Args:
        user_id: ID del usuario autenticado (obtenido de get_current_user)
        conversation_manager: Instancia del ConversationManager (obtenida de get_conversation_manager)

    Returns:
        Tuple[str, ConversationManager]: Tupla con (user_id, conversation_manager)

    Example:
        async def chat_multimedia(
            message: str,
            user_id_and_conv: Tuple[str, ConversationManager] = Depends(get_current_user_and_conversation_manager)
        ):
            user_id, conversation_manager = user_id_and_conv
            # Usar user_id y conversation_manager
    """
    return (user_id, conversation_manager)


async def get_all_dependencies(
    user_id: str = Depends(get_current_user),
    storage: LocalStorage = Depends(get_storage),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
) -> Tuple[str, LocalStorage, ConversationManager]:
    """
    Obtiene todas las dependencias principales: user_id, storage y conversation_manager.

    Esta dependencia combinada es útil para rutas que requieren acceso completo
    al sistema, como rutas que necesitan autenticación, almacenamiento y
    persistencia de conversaciones simultáneamente.

    Args:
        user_id: ID del usuario autenticado (obtenido de get_current_user)
        storage: Instancia del LocalStorage (obtenida de get_storage)
        conversation_manager: Instancia del ConversationManager (obtenida de get_conversation_manager)

    Returns:
        Tuple[str, LocalStorage, ConversationManager]: Tupla con (user_id, storage, conversation_manager)

    Example:
        async def process_multimedia_request(
            request: MultimediaRequest,
            all_deps: Tuple[str, LocalStorage, ConversationManager] = Depends(get_all_dependencies)
        ):
            user_id, storage, conversation_manager = all_deps
            # Usar todas las dependencias
    """
    return (user_id, storage, conversation_manager)
