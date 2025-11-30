from fastapi import *
from routes.routes import router
import uvicorn
import logging
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(router)
