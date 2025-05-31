
import os
from services.graph_service import graph
from services.ollama_services import get_models
from config import Config
from langchain_core.messages import HumanMessage
from controllers.chats_controller import new_conversation,get_chats_list, remove_conversation,get_user_conversation,update_name_chat
import logging
active_users=[]
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
    input_messages = [HumanMessage(conf.userInput)]
    for i in await graph.ainvoke({"messages": input_messages}, config, stream_mode="updates"):
        logging.info(f"event---{i}")
        
        last = i
    logging.info(f"last---{last}")
    return last['chatbot']["messages"]
    # async for i in graph.ainvoke({"messages":input_messages},
    #                       config,
    #                       stream_mode="updates"):
    #     last=i
    # return last['chatbot']["messages"]
async def get_ollama_models():
    # from ollama service, get all models availables and return them
    return get_models()

async def new_chat(credentials,new_chat_name)->str:
    return await new_conversation(credentials,new_chat_name)

async def get_chats(credentials)->list[dict]:
    return await get_chats_list(credentials)

async def remove_chat(chat_name,credentials)->str:
    return await remove_conversation(chat_name,credentials)

async def get_conversation(credentials,chat_name)->list[dict[str,list[str]]]:
    return await get_user_conversation(credentials,chat_name)


async def update_chat_name(old_name,new_name,credencials):
    await update_name_chat(old_name,new_name,credencials)