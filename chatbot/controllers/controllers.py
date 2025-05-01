
import os
from services.graph_service import graph
from services.ollama_services import get_models
from config import Config

async def query(question:str,credentials,conf:Config):
    #invoke grafo(input,conf_id_conversation,configuracion_modelo)
    config = {
        "configurable": {
            "thread_id": str(credentials),
        }
    }
    
    # Add any configuration from conf if needed
    if hasattr(conf, "__dict__"):
        config["configurable"].update(conf.__dict__)
    print(config)
    for i in graph.invoke({"messages":question},
                          config,
                          stream_mode="updates"):
        last=i
    print("Last",last['chatbot']["messages"])
    return last['chatbot']["messages"]
async def get_ollama_models():
    # from ollama service, get all models availables and return them
    return get_models()
