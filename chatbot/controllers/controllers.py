
import os
from services.graph_service import graph
from services.ollama_services import get_models
from config import Config
from langchain_core.messages import HumanMessage
from controllers.chats_controller import new_conversation,get_chats_list, remove_conversation,get_user_conversation,update_name_chat
import logging
active_users=[]
def catch_event(event_metadata:dict):
    match event_metadata.get('langgraph_node'):
        case 'chatbot':
            return "chatbot"
        case 'orquestator':
            return "processing_ response"
        case 'image_generator':
            return "generating_image"
        case _ :
            return "Error"
async def query(conf:Config,websocket):
    #invoke grafo(input,conf_id_conversation,configuracion_modelo)

    config = {
        "configurable": {
            "thread_id": str(conf.credentials),
        }
    }
    
    # Add any configuration from conf if needed
    if hasattr(conf, "__dict__"):
        config["configurable"].update(conf.__dict__)
    input_messages = [HumanMessage(conf.userInput)]
    event_=""
    async for event , metadata in graph.astream({"messages": input_messages}, config, stream_mode="messages"):
        logging.info(f"metadata---{metadata}")
        event_caught= catch_event(metadata)
        if not event_caught=='chatbot':
            await websocket.send_json({"event":event.content})            
        else:
            if event_ != event_caught:
                await websocket.send_json({"event":event_})
                event_=event_caught
            else:
                continue
            

# websocket.send_json({"event":event.content})



        if metadata.get('langgraph_node')== 'chatbot':
            logging.info(f"chatbot captured---{event.content}")
            fullText+=event.content
        logging.info(f"event---{event}")
        #logging.info(f"metadata---{metadata}")
        
        last = event
    logging.info(f"last---{fullText}")
    # return last['chatbot']["messages"]
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