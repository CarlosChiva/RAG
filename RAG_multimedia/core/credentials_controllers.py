"""
Controlador de autenticación JWT para RAG Multimedia.

Proporciona funciones para generación y verificación de tokens JWT
para autenticación de solicitudes HTTP y WebSocket.
"""

from typing import Union
from fastapi import Depends, HTTPException,Security
from fastapi.security import HTTPBearer   
from fastapi.security import HTTPAuthorizationCredentials
from jwt import decode, encode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta

from core.config import SECRET_KEY, ALGORITHM

# Instancia de seguridad HTTP Bearer
security = HTTPBearer()


async def generate_token(user_id: str) -> str:
    """
    Generar token JWT para un usuario.

    Args:
        user_id: Identificador único del usuario (se usará en el claim 'sub')

    Returns:
        Token JWT codificado con expiración de 24 horas

    Example:
        >>> token = await generate_token("user_123")
        >>> # Token válido por 24 horas
    """
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }
    return encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def verify_jws(credentials: Union[HTTPAuthorizationCredentials, str]) -> str:
    """
    Verificar token JWT para HTTP requests.

    Maneja tanto peticiones HTTP (con prefijo "Bearer ") como WebSocket
    (token directo o con prefijo).

    Args:
        credentials: Credenciales HTTP o string con token JWT

    Returns:
        user_id extraído del claim 'sub' del token

    Raises:
        HTTPException: 401 si el token es inválido o expirado

    Example:
        >>> # HTTP request
        >>> user_id = await verify_jws(credentials)
        >>> # WebSocket request
        >>> user_id = await verify_jws("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    """
    try:
        # Extraer token según el tipo de credenciales
        if isinstance(credentials, HTTPAuthorizationCredentials):
            # Caso normal: viene de dependencia HTTP (GET/POST)
            token = credentials.credentials
        elif isinstance(credentials, str) and credentials.startswith("Bearer "):
            # Caso WebSocket: token ya viene con "Bearer "
            token = credentials.split("Bearer ")[1]
        elif isinstance(credentials, str):
            # Caso WebSocket: token sin "Bearer "
            token = credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials format")

        # Decodificar y verificar el token
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Retornar el user_id del claim 'sub'
        return payload["sub"]

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def verify_websocket_auth(auth_token: str) -> str:
    """
    Verificar token JWT para WebSocket.

    El token viene en el payload JSON de la conexión WebSocket.
    Similar a verify_jws pero recibe string directamente.

    Args:
        auth_token: Token JWT como string (puede incluir o no el prefijo "Bearer ")

    Returns:
        user_id extraído del claim 'sub' del token

    Raises:
        HTTPException: 401 si el token es inválido o expirado

    Example:
        >>> # WebSocket message: {"auth": "Bearer eyJhbGci...", "input": "hello"}
        >>> user_id = await verify_websocket_auth("Bearer eyJhbGci...")
    """
    return await verify_jws(auth_token)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """
    Dependencia FastAPI para rutas protegidas.

    Esta función debe ser usada como `Depends(get_current_user)` en las rutas
    que requieren autenticación JWT.

    Args:
        credentials: Credenciales HTTP extraídas automáticamente por FastAPI

    Returns:
        user_id extraído del claim 'sub' del token

    Raises:
        HTTPException: 401 si el token es inválido o expirado

    Example:
        >>> @router.get("/protected")
        >>> async def protected_route(user_id: str = Depends(get_current_user)):
        >>>     return {"user_id": user_id}
    """
    return await verify_jws(credentials)
