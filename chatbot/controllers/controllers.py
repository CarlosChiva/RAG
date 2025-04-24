
import os
from services.graph_service import graph
from services.ollama_services import get_models
# funcion para codigicar credenciales en una id

async def query(question:str,conf):
    #invoke grafo(input,conf_id_conversation,configuracion_modelo)
    config = {"configurable": {"thread_id": str(conf)}}
    for i in graph.invoke({"messages":question},
                          config,
                          conf,
                          stream_mode="values"):
        print(i)
    pass
async def get_ollama_models():
    # from ollama service, get all models availables and return them
    return get_models()
