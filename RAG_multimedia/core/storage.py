"""
Módulo de almacenamiento intercambiable para la API Multimedia RAG.

Proporciona una interfaz abstracta AbstractStorage para implementar
diferentes sistemas de almacenamiento (local, S3, GCS, etc.) de manera
consistente, permitiendo cambiar el backend de almacenamiento sin
modificar el código de la API.

Actualmente implementado: LocalStorage (almacenamiento en disco local).
"""

import json
import os
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import aiofiles


# Mapeo de extensiones de video a MIME types
VIDEO_MIME_TYPES: dict[str, str] = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
    ".flv": "video/x-flv",
    ".wmv": "video/x-ms-wmv",
    ".m4v": "video/x-m4v",
    ".mpeg": "video/mpeg",
    ".mpg": "video/mpeg",
    ".3gp": "video/3gpp",
    ".3g2": "video/3gpp2",
    ".ogv": "video/ogg",
    ".mxf": "video/mxf",
    ".vob": "video/x-ms-vob",
    ".asf": "video/ms-asf",
    ".amv": "video/x-ms-amv",
}


class StorageError(Exception):
    """Excepción personalizada para errores de almacenamiento."""

    pass


class AbstractStorage(ABC):
    """
    Interfaz abstracta para sistemas de almacenamiento de videos.

    Define el contrato que deben cumplir todas las implementaciones
    de almacenamiento, permitiendo intercambiar backends sin modificar
    el código de la API.

    Métodos:
        - upload: Subir un archivo y obtener su URL/path
        - download: Descargar un archivo y obtener su contenido
        - delete: Eliminar un archivo
        - list: Listar todos los archivos de un usuario
        - get_file_info: Obtener metadatos de un archivo específico
    """

    @abstractmethod
    async def upload(
        self,
        file_id: str,
        user_id: str,
        file_content: bytes,
        metadata: dict[str, Any],
    ) -> str:
        """
        Subir un archivo de video al sistema de almacenamiento.

        Args:
            file_id: Identificador único del archivo (UUID recomendado)
            user_id: Identificador del usuario que sube el archivo
            file_content: Contenido binario del archivo de video
            metadata: Diccionario con metadatos del archivo (título, descripción, etc.)

        Returns:
            str: URL o path donde se almacenó el archivo

        Raises:
            StorageError: Si ocurre un error durante la subida
        """
        pass

    @abstractmethod
    async def download(
        self,
        file_id: str,
        user_id: str,
    ) -> tuple[bytes, str]:
        """
        Descargar un archivo de video del sistema de almacenamiento.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario que solicita la descarga

        Returns:
            tuple[bytes, str]: (contenido_binario, mime_type) del archivo

        Raises:
            StorageError: Si el archivo no existe o no se puede acceder
        """
        pass

    @abstractmethod
    async def delete(
        self,
        file_id: str,
        user_id: str,
    ) -> bool:
        """
        Eliminar un archivo de video del sistema de almacenamiento.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario dueño del archivo

        Returns:
            bool: True si el archivo fue eliminado exitosamente, False si no existía

        Raises:
            StorageError: Si ocurre un error durante la eliminación
        """
        pass

    @abstractmethod
    async def list(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """
        Listar todos los archivos de video de un usuario.

        Args:
            user_id: Identificador del usuario

        Returns:
            list[dict]: Lista de diccionarios con información de cada archivo:
                - file_id: Identificador del archivo
                - filename: Nombre original del archivo
                - mime_type: Tipo MIME del video
                - size: Tamaño en bytes
                - created_at: Timestamp de creación
                - metadata: Diccionario con metadatos adicionales
        """
        pass

    @abstractmethod
    async def get_file_info(
        self,
        file_id: str,
        user_id: str,
    ) -> Optional[dict[str, Any]]:
        """
        Obtener información detallada de un archivo específico.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario

        Returns:
            Optional[dict]: Diccionario con información del archivo o None si no existe:
                - file_id: Identificador del archivo
                - filename: Nombre original del archivo
                - mime_type: Tipo MIME del video
                - size: Tamaño en bytes
                - path: Path completo del archivo
                - created_at: Timestamp de creación
                - metadata: Diccionario con metadatos adicionales
        """
        pass


class LocalStorage(AbstractStorage):
    """
    Implementación de almacenamiento local en disco.

    Almacena archivos de video en el sistema de archivos local con
    la siguiente estructura:
        {STORAGE_PATH}/{user_id}/{file_id}
        {STORAGE_PATH}/{user_id}/{file_id}.meta.json

    Características:
        - Almacenamiento aislado por usuario
        - Metadatos guardados en archivos JSON separados
        - Operaciones asíncronas usando aiofiles
        - Detección automática de MIME types para videos
        - Generación automática de file_id usando UUID4

    Variables de entorno:
        STORAGE_PATH: Path base para el almacenamiento (default: /app/storage/videos)
    """

    def __init__(self, storage_path: Optional[str] = None):
        """
        Inicializar el almacenamiento local.

        Args:
            storage_path: Path base para el almacenamiento. Si None, usa la variable
                de entorno STORAGE_PATH o el valor por defecto /app/storage/videos
        """
        self._storage_path = (
            storage_path or os.getenv("STORAGE_PATH") or "/app/storage/videos"
        )
        self._storage_dir = Path(self._storage_path)

        # Crear el directorio base si no existe
        self._ensure_storage_directory()

    def _ensure_storage_directory(self) -> None:
        """Crear el directorio base de almacenamiento si no existe."""
        try:
            self._storage_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise StorageError(
                f"No se tiene permiso para crear el directorio de almacenamiento: {self._storage_path}"
            ) from e
        except OSError as e:
            raise StorageError(
                f"Error al crear el directorio de almacenamiento: {e}"
            ) from e

    def _get_user_directory(self, user_id: str) -> Path:
        """
        Obtener el directorio de un usuario específico.

        Args:
            user_id: Identificador del usuario

        Returns:
            Path: Path al directorio del usuario

        Raises:
            StorageError: Si no se puede crear el directorio del usuario
        """
        user_dir = self._storage_dir / user_id
        try:
            user_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise StorageError(
                f"No se tiene permiso para crear el directorio del usuario: {user_id}"
            ) from e
        except OSError as e:
            raise StorageError(f"Error al crear el directorio del usuario: {e}") from e
        return user_dir

    def _get_file_path(self, user_id: str, file_id: str) -> Path:
        """Obtener el path completo de un archivo."""
        return self._get_user_directory(user_id) / file_id

    def _get_metadata_path(self, user_id: str, file_id: str) -> Path:
        """Obtener el path del archivo de metadatos."""
        return self._get_user_directory(user_id) / f"{file_id}.meta.json"

    def _detect_mime_type(self, filename: str, file_content: bytes) -> str:
        """
        Detectar el MIME type de un archivo de video.

        Prioriza la detección por extensión, luego por contenido.

        Args:
            filename: Nombre del archivo (puede incluir extensión)
            file_content: Contenido binario del archivo

        Returns:
            str: MIME type detectado o "application/octet-stream" si no se puede determinar
        """
        # Intentar detectar por extensión
        ext = Path(filename).suffix.lower()
        if ext in VIDEO_MIME_TYPES:
            return VIDEO_MIME_TYPES[ext]

        # Intentar detectar por magic bytes (opcional, se puede expandir)
        if file_content.startswith(b"\x00\x00\x00\x1cftismp4"):
            return "video/mp4"
        if file_content.startswith(b"RIFF" + b"\x00\x00\x00\x00WEBV"):
            return "video/webm"

        return "application/octet-stream"

    def _validate_video(self, filename: str, mime_type: str) -> None:
        """
        Validar que el archivo es un video.

        Args:
            filename: Nombre del archivo
            mime_type: Tipo MIME detectado

        Raises:
            StorageError: Si el archivo no es un video válido
        """
        ext = Path(filename).suffix.lower()
        if ext not in VIDEO_MIME_TYPES and not mime_type.startswith("video/"):
            raise StorageError(
                f"El archivo '{filename}' no es un video válido. "
                f"Extensiones soportadas: {', '.join(VIDEO_MIME_TYPES.keys())}"
            )

    async def upload(
        self,
        file_id: str,
        user_id: str,
        file_content: bytes,
        metadata: dict[str, Any],
    ) -> str:
        """
        Subir un archivo de video al almacenamiento local.

        Args:
            file_id: Identificador único del archivo (UUID recomendado)
            user_id: Identificador del usuario que sube el archivo
            file_content: Contenido binario del archivo de video
            metadata: Diccionario con metadatos del archivo

        Returns:
            str: Path relativo donde se almacenó el archivo

        Raises:
            StorageError: Si ocurre un error durante la subida
        """
        try:
            # Obtener filename del metadata o usar file_id
            filename = metadata.get("filename", f"{file_id}.mp4")

            # Detectar MIME type
            mime_type = self._detect_mime_type(filename, file_content)

            # Validar que es un video
            self._validate_video(filename, mime_type)

            # Obtener paths
            file_path = self._get_file_path(user_id, file_id)
            meta_path = self._get_metadata_path(user_id, file_id)

            # Guardar archivo de video
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_content)

            # Guardar metadatos
            meta_data = {
                "file_id": file_id,
                "user_id": user_id,
                "filename": filename,
                "mime_type": mime_type,
                "size": len(file_content),
                "metadata": metadata,
            }
            async with aiofiles.open(meta_path, "w") as f:
                await f.write(json.dumps(meta_data, indent=2, ensure_ascii=False))

            # Retornar path relativo
            return str(file_path.relative_to(self._storage_dir))

        except StorageError:
            raise
        except PermissionError as e:
            raise StorageError(f"Error de permiso al subir archivo: {e}") from e
        except OSError as e:
            raise StorageError(f"Error al subir archivo: {e}") from e
        except json.JSONEncodeError as e:
            raise StorageError(f"Error al serializar metadatos: {e}") from e

    async def download(
        self,
        file_id: str,
        user_id: str,
    ) -> tuple[bytes, str]:
        """
        Descargar un archivo de video del almacenamiento local.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario

        Returns:
            tuple[bytes, str]: (contenido_binario, mime_type) del archivo

        Raises:
            StorageError: Si el archivo no existe o no se puede acceder
        """
        file_path = self._get_file_path(user_id, file_id)
        meta_path = self._get_metadata_path(user_id, file_id)

        # Verificar que el archivo existe
        if not file_path.exists():
            raise StorageError(f"Archivo no encontrado: {file_id}")

        # Leer metadatos para obtener mime_type
        mime_type = "application/octet-stream"
        if meta_path.exists():
            try:
                async with aiofiles.open(meta_path, "r") as f:
                    meta_content = await f.read()
                    meta_data = json.loads(meta_content)
                    mime_type = meta_data.get("mime_type", mime_type)
            except (json.JSONDecodeError, OSError):
                # Si hay error leyendo metadatos, usar default
                pass

        # Leer contenido del archivo
        try:
            async with aiofiles.open(file_path, "rb") as f:
                content = await f.read()
            return content, mime_type
        except PermissionError as e:
            raise StorageError(f"Error de permiso al leer archivo: {e}") from e
        except OSError as e:
            raise StorageError(f"Error al leer archivo: {e}") from e

    async def delete(
        self,
        file_id: str,
        user_id: str,
    ) -> bool:
        """
        Eliminar un archivo de video del almacenamiento local.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario

        Returns:
            bool: True si el archivo fue eliminado, False si no existía

        Raises:
            StorageError: Si ocurre un error durante la eliminación
        """
        file_path = self._get_file_path(user_id, file_id)
        meta_path = self._get_metadata_path(user_id, file_id)

        # Verificar que el archivo existe
        if not file_path.exists():
            return False

        # Eliminar archivo de video
        try:
            file_path.unlink()
        except PermissionError as e:
            raise StorageError(f"Error de permiso al eliminar archivo: {e}") from e
        except OSError as e:
            raise StorageError(f"Error al eliminar archivo: {e}") from e

        # Eliminar archivo de metadatos si existe
        if meta_path.exists():
            try:
                meta_path.unlink()
            except (PermissionError, OSError):
                # No fallar si no se puede eliminar el metadata
                pass

        return True

    async def list(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """
        Listar todos los archivos de video de un usuario.

        Args:
            user_id: Identificador del usuario

        Returns:
            list[dict]: Lista de diccionarios con información de cada archivo
        """
        user_dir = self._storage_dir / user_id

        # Si el directorio del usuario no existe, retornar lista vacía
        if not user_dir.exists():
            return []

        files_info = []

        # Iterar sobre archivos de metadatos en el directorio del usuario
        try:
            for meta_file in user_dir.glob("*.meta.json"):
                # Extraer file_id del nombre del archivo
                file_id = meta_file.stem

                # Verificar que el archivo de video existe
                video_file = meta_file.with_name(meta_file.stem)
                if not video_file.exists():
                    # Eliminar metadata huérfana
                    try:
                        meta_file.unlink()
                    except (PermissionError, OSError):
                        pass
                    continue

                # Leer metadatos
                try:
                    async with aiofiles.open(meta_file, "r") as f:
                        meta_content = await f.read()
                        meta_data = json.loads(meta_content)

                        # Obtener tamaño real del archivo
                        try:
                            size = video_file.stat().st_size
                        except OSError:
                            size = meta_data.get("size", 0)

                        files_info.append(
                            {
                                "file_id": file_id,
                                "filename": meta_data.get("filename", file_id),
                                "mime_type": meta_data.get(
                                    "mime_type", "application/octet-stream"
                                ),
                                "size": size,
                                "created_at": video_file.stat().st_mtime,
                                "metadata": meta_data.get("metadata", {}),
                            }
                        )
                except (json.JSONDecodeError, OSError):
                    # Saltar archivos de metadata corruptos
                    continue

        except PermissionError as e:
            raise StorageError(f"Error de permiso al listar archivos: {e}") from e
        except OSError as e:
            raise StorageError(f"Error al listar archivos: {e}") from e

        return files_info

    async def get_file_info(
        self,
        file_id: str,
        user_id: str,
    ) -> Optional[dict[str, Any]]:
        """
        Obtener información detallada de un archivo específico.

        Args:
            file_id: Identificador único del archivo
            user_id: Identificador del usuario

        Returns:
            Optional[dict]: Diccionario con información del archivo o None si no existe
        """
        file_path = self._get_file_path(user_id, file_id)
        meta_path = self._get_metadata_path(user_id, file_id)

        # Verificar que el archivo existe
        if not file_path.exists():
            return None

        # Leer metadatos si existen
        if meta_path.exists():
            try:
                async with aiofiles.open(meta_path, "r") as f:
                    meta_content = await f.read()
                    meta_data = json.loads(meta_content)

                    # Obtener tamaño real del archivo
                    try:
                        stat_info = file_path.stat()
                        size = stat_info.st_size
                        created_at = stat_info.st_mtime
                    except OSError:
                        size = meta_data.get("size", 0)
                        created_at = meta_data.get("created_at", 0)

                    return {
                        "file_id": file_id,
                        "filename": meta_data.get("filename", file_id),
                        "mime_type": meta_data.get(
                            "mime_type", "application/octet-stream"
                        ),
                        "size": size,
                        "path": str(file_path),
                        "created_at": created_at,
                        "metadata": meta_data.get("metadata", {}),
                    }
            except (json.JSONDecodeError, OSError):
                # Si no se pueden leer los metadatos, retornar info básica
                try:
                    stat_info = file_path.stat()
                    return {
                        "file_id": file_id,
                        "filename": file_path.name,
                        "mime_type": "application/octet-stream",
                        "size": stat_info.st_size,
                        "path": str(file_path),
                        "created_at": stat_info.st_mtime,
                        "metadata": {},
                    }
                except OSError:
                    return None
        else:
            # No hay metadatos, retornar info básica del archivo
            try:
                stat_info = file_path.stat()
                # Intentar detectar mime_type por extensión
                mime_type = self._detect_mime_type(file_path.name, b"")
                return {
                    "file_id": file_id,
                    "filename": file_path.name,
                    "mime_type": mime_type,
                    "size": stat_info.st_size,
                    "path": str(file_path),
                    "created_at": stat_info.st_mtime,
                    "metadata": {},
                }
            except OSError:
                return None
