
import os
# importar grafo_service
from services.ollama_services import get_models
# funcion para codigicar credenciales en una id

async def query(question:str,conf):
    #invoke grafo(input,conf_id_conversation,configuracion_modelo)
    pass
async def get_ollama_models():
    # from ollama service, get all models availables and return them
    return get_models()
