
import os
from services.graph_service import graph
from services.ollama_services import get_models
from config import Config
from langchain_core.messages import HumanMessage
from controllers.chats_controller import new_conversation,get_conversation, remove_conversation
async def query(credentials,conf:Config):
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
    input_messages = [HumanMessage(conf.userInput)]
    for i in graph.invoke({"messages":input_messages},
                          config,
                          stream_mode="updates"):
        last=i
    print("Last",last['chatbot']["messages"])
    return last['chatbot']["messages"]
async def get_ollama_models():
    # from ollama service, get all models availables and return them
    return get_models()
async def new_chat(credentials):
    return await new_conversation(credentials)
async def get_chats(credentials):
    return await get_conversation(credentials)
async def remove_chat(chat_name,credentials):
    return await remove_conversation(chat_name,credentials)



