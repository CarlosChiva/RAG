from fastapi import *
from routes.routes import router
import uvicorn
import logging
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia este valor al origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  
)
app.include_router(router)
