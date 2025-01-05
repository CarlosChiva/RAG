import hashlib
from fastapi import Depends, HTTPException
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
SECRET_KEY = "tu_secreto_super_seguro"
ALGORITHM = "HS256"
security = HTTPBearer()
async def generar_hash(password):
    """
    Genera un hash para un password usando el algoritmo SHA-256.

    Args:
        password (str): El password a ser hashing.

    Returns:
        str: El hash generado.
    """
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')

    # Crear un objeto SHA-256
    sha256 = hashlib.sha256()

    # Agregar los datos de la contraseña al flujo de hashing
    sha256.update(password_bytes)

    # Obtener el hash generado
    password_hash = sha256.hexdigest()

    return password_hash

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verificar si el token está expirado
        if datetime.utcnow().timestamp() > payload["exp"]:
            raise HTTPException(status_code=401, detail="Token expired")

        # Retornar el nombre de usuario extraído del token
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_jws(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def generate_token(password_hashed):
    
    # Crear payload
    payload = {
        "sub": password_hashed,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Expiración
        "iat": datetime.utcnow(),  # Fecha de emisión
    }

    # Firmar el token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token    