"""
Módulo core de la API Multimedia RAG.

Contiene componentes fundamentales del sistema:
- storage: Sistema de almacenamiento intercambiable para videos
"""

from .storage import AbstractStorage, LocalStorage, StorageError

__all__ = ["AbstractStorage", "LocalStorage", "StorageError"]
