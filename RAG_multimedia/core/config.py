"""
Configuración del servicio RAG Multimedia.

Carga y valida las variables de entorno necesarias para el servicio.
"""

from typing import List
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde archivo .env
load_dotenv()


# Variables de autenticación JWT
SECRET_KEY: str = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be defined in environment variables")

ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

# Paths de almacenamiento
STORAGE_PATH: str = os.getenv("STORAGE_PATH", "/app/storage/videos")
CONVERSATIONS_PATH: str = os.getenv("CONVERSATIONS_PATH", "/app/conversations")

# Configuración del servidor
PORT: int = int(os.getenv("PORT", "8006"))
ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")


# Validaciones
def validate_config() -> None:
    """
    Valida las variables de configuración.

    Raises:
        ValueError: Si alguna variable requerida no está definida o es inválida.
    """
    # SECRET_KEY ya fue validado al cargar
    if not isinstance(PORT, int) or PORT < 1 or PORT > 65535:
        raise ValueError(f"PORT must be a valid port number (1-65535), got: {PORT}")

    # Validar que los paths sean absolutos
    if not os.path.isabs(STORAGE_PATH):
        raise ValueError(f"STORAGE_PATH must be an absolute path, got: {STORAGE_PATH}")

    if not os.path.isabs(CONVERSATIONS_PATH):
        raise ValueError(
            f"CONVERSATIONS_PATH must be an absolute path, got: {CONVERSATIONS_PATH}"
        )


# Ejecutar validaciones al cargar el módulo
validate_config()
