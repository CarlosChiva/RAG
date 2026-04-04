"""
Aplicación principal de la API Multimedia RAG.

Inicializa la aplicación FastAPI con configuración de CORS,
rutas REST y endpoints de salud.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

# =============================================================================
# Configuración de FastAPI
# =============================================================================

app = FastAPI(
    title="RAG Multimedia API",
    description="API para gestión de multimedia (videos) con almacenamiento y conversaciones",
    version="1.0.0",
)

# =============================================================================
# Configuración de CORS
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Incluir Router
# =============================================================================

app.include_router(router, prefix="/api")

# =============================================================================
# Endpoints de Salud
# =============================================================================


@app.get("/")
async def root():
    """
    Endpoint root para verificar que el servicio está corriendo.

    Proporciona información básica sobre el servicio y su estado actual.

    Returns:
        dict: Información del servicio:
            - message: Nombre del servicio
            - status: Estado actual (running)
            - version: Versión de la API

    Example:
        GET /
        Response:
        {
            "message": "RAG Multimedia API",
            "status": "running",
            "version": "1.0.0"
        }
    """
    return {"message": "RAG Multimedia API", "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """
    Endpoint de health check para Docker/Kubernetes.

    Proporciona un endpoint simple para verificar la salud del servicio
    en entornos de orquestación de contenedores.

    Returns:
        dict: Estado de salud del servicio:
            - status: Estado de salud (healthy)
            - service: Nombre del servicio

    Example:
        GET /health
        Response:
        {
            "status": "healthy",
            "service": "multimedia-api"
        }
    """
    return {"status": "healthy", "service": "multimedia-api"}


# =============================================================================
# Punto de Entrada
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    from core.config import PORT

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
