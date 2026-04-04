"""
Gestor de conversaciones para la API Multimedia RAG.

Proporciona operaciones asíncronas para crear, leer, actualizar y eliminar
conversaciones de usuarios en formato JSON.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import json
import uuid
import aiofiles


class ConversationManager:
    """
    Gestor de conversaciones para persistencia en JSON.

    Almacena las conversaciones en una estructura de directorios:
    {CONVERSATIONS_PATH}/{user_id}/{conversation_id}.json

    Cada conversación se guarda en un archivo JSON independiente con
    aislamiento por usuario.
    """

    def __init__(self, base_path: str = None):
        """
        Inicializa el ConversationManager.

        Args:
            base_path: Path base para guardar conversaciones.
                      Si None, usa CONVERSATIONS_PATH de config.
        """
        from core.config import CONVERSATIONS_PATH

        self.base_path = Path(base_path or CONVERSATIONS_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_user_path(self, user_id: str) -> Path:
        """
        Obtiene el directorio de un usuario específico.

        Args:
            user_id: Identificador del usuario.

        Returns:
            Path al directorio del usuario.
        """
        user_path = self.base_path / user_id
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path

    def _get_conversation_path(self, user_id: str, conversation_id: str) -> Path:
        """
        Obtiene el path completo de un archivo de conversación.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.

        Returns:
            Path al archivo JSON de la conversación.
        """
        return self._get_user_path(user_id) / f"{conversation_id}.json"

    def _get_timestamp(self) -> str:
        """
        Obtiene timestamp actual en formato ISO 8601.

        Returns:
            String con timestamp en formato ISO 8601 UTC.
        """
        return datetime.now(timezone.utc).isoformat()

    async def create(self, user_id: str, title: Optional[str] = None) -> str:
        """
        Crea una nueva conversación para un usuario.

        Genera un UUID para la conversación, crea la estructura inicial
        con timestamp y guarda el archivo JSON.

        Args:
            user_id: Identificador del usuario.
            title: Título opcional para la conversación.
                  Si None, usa "Untitled conversation".

        Returns:
            conversation_id: UUID generado para la nueva conversación.

        Raises:
            IOError: Si no se puede crear el archivo.
        """
        conversation_id = str(uuid.uuid4())
        timestamp = self._get_timestamp()

        conversation_data = {
            "id": conversation_id,
            "user_id": user_id,
            "title": title or "Untitled conversation",
            "messages": [],
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        file_path = self._get_conversation_path(user_id, conversation_id)

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(conversation_data, indent=2, ensure_ascii=False))

        return conversation_id

    async def get(self, user_id: str, conversation_id: str) -> Optional[dict]:
        """
        Obtiene una conversación específica por ID.

        Verifica que el archivo existe, carga el JSON y valida que
        la conversación pertenece al user_id proporcionado.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.

        Returns:
            dict: Conversación completa si existe y pertenece al usuario.
            None: Si la conversación no existe o no pertenece al usuario.
        """
        file_path = self._get_conversation_path(user_id, conversation_id)

        if not file_path.exists():
            return None

        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                conversation = json.loads(content)

            # Validar ownership
            if conversation.get("user_id") != user_id:
                return None

            return conversation

        except (json.JSONDecodeError, IOError):
            return None

    async def list(self, user_id: str) -> List[dict]:
        """
        Lista todas las conversaciones de un usuario.

        Busca todos los archivos JSON en el directorio del usuario,
        carga cada uno y filtra por user_id para asegurar ownership.

        Args:
            user_id: Identificador del usuario.

        Returns:
            List[dict]: Lista de conversaciones con metadatos (id, title,
                       created_at, updated_at).
        """
        conversations = []
        user_path = self._get_user_path(user_id)

        # Buscar todos los archivos JSON del usuario
        for file_path in user_path.glob("*.json"):
            try:
                async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                    content = await f.read()
                    conversation = json.loads(content)

                # Validar ownership
                if conversation.get("user_id") == user_id:
                    # Retornar solo metadatos para la lista
                    conversations.append(
                        {
                            "id": conversation.get("id"),
                            "title": conversation.get("title"),
                            "created_at": conversation.get("created_at"),
                            "updated_at": conversation.get("updated_at"),
                            "message_count": len(conversation.get("messages", [])),
                        }
                    )

            except (json.JSONDecodeError, IOError):
                # Saltar archivos corruptos
                continue

        # Ordenar por updated_at descendente (más recientes primero)
        conversations.sort(key=lambda x: x.get("updated_at", ""), reverse=True)

        return conversations

    async def delete(self, user_id: str, conversation_id: str) -> bool:
        """
        Elimina una conversación específica.

        Verifica que la conversación existe y pertenece al usuario
        antes de eliminar el archivo.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.

        Returns:
            bool: True si se eliminó exitosamente, False si no existía
                 o no pertenecía al usuario.
        """
        file_path = self._get_conversation_path(user_id, conversation_id)

        if not file_path.exists():
            return False

        try:
            # Verificar ownership antes de eliminar
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                conversation = json.loads(content)

            if conversation.get("user_id") != user_id:
                return False

            # Eliminar el archivo
            file_path.unlink()
            return True

        except (json.JSONDecodeError, IOError, PermissionError):
            return False

    async def add_message(
        self, user_id: str, conversation_id: str, message: dict
    ) -> bool:
        """
        Agrega un mensaje a una conversación existente.

        Carga la conversación, agrega el mensaje a la lista,
        actualiza updated_at y guarda los cambios.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.
            message: Dict con estructura del mensaje:
                    {
                        "role": "user" | "assistant",
                        "content": "message text",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "metadata": {}
                    }

        Returns:
            bool: True si se agregó exitosamente, False si la conversación
                 no existía o no pertenecía al usuario.
        """
        file_path = self._get_conversation_path(user_id, conversation_id)

        if not file_path.exists():
            return False

        try:
            # Cargar conversación
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                conversation = json.loads(content)

            # Verificar ownership
            if conversation.get("user_id") != user_id:
                return False

            # Agregar timestamp al mensaje si no tiene
            if "timestamp" not in message:
                message["timestamp"] = self._get_timestamp()

            # Agregar metadata si no existe
            if "metadata" not in message:
                message["metadata"] = {}

            # Agregar mensaje a la lista
            conversation.setdefault("messages", []).append(message)

            # Actualizar timestamp
            conversation["updated_at"] = self._get_timestamp()

            # Guardar cambios
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(conversation, indent=2, ensure_ascii=False))

            return True

        except (json.JSONDecodeError, IOError, PermissionError):
            return False

    async def update_title(
        self, user_id: str, conversation_id: str, title: str
    ) -> bool:
        """
        Actualiza el título de una conversación.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.
            title: Nuevo título para la conversación.

        Returns:
            bool: True si se actualizó exitosamente, False si no existía
                 o no pertenecía al usuario.
        """
        file_path = self._get_conversation_path(user_id, conversation_id)

        if not file_path.exists():
            return False

        try:
            # Cargar conversación
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                conversation = json.loads(content)

            # Verificar ownership
            if conversation.get("user_id") != user_id:
                return False

            # Actualizar título
            conversation["title"] = title
            conversation["updated_at"] = self._get_timestamp()

            # Guardar cambios
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(conversation, indent=2, ensure_ascii=False))

            return True

        except (json.JSONDecodeError, IOError, PermissionError):
            return False

    async def clear_messages(self, user_id: str, conversation_id: str) -> bool:
        """
        Limpia todos los mensajes de una conversación.

        Mantiene la conversación pero vacía la lista de mensajes.

        Args:
            user_id: Identificador del usuario.
            conversation_id: Identificador de la conversación.

        Returns:
            bool: True si se limpió exitosamente, False si no existía
                 o no pertenecía al usuario.
        """
        file_path = self._get_conversation_path(user_id, conversation_id)

        if not file_path.exists():
            return False

        try:
            # Cargar conversación
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                conversation = json.loads(content)

            # Verificar ownership
            if conversation.get("user_id") != user_id:
                return False

            # Vaciar mensajes
            conversation["messages"] = []
            conversation["updated_at"] = self._get_timestamp()

            # Guardar cambios
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(conversation, indent=2, ensure_ascii=False))

            return True

        except (json.JSONDecodeError, IOError, PermissionError):
            return False
