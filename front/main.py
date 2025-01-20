from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes limitarlo a los dominios necesarios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Servir archivos estáticos
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount("/images", StaticFiles(directory="static/images"), name="images")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)