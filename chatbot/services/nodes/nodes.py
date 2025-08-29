from langchain_ollama import ChatOllama
from langgraph.graph import  MessagesState

from config import Config
import json
from langgraph.graph.message import MessagesState,BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import logging
logging.basicConfig(level=logging.INFO)
from controllers.chats_controller import get_user_conversation, add_conversation

def save_messages_state_to_file(messages_state: MessagesState, file_path: str):
    messages_state_dict = messages_state.dict()
    with open(file_path, 'w') as file:
        json.dump(messages_state_dict, file)

# Example function to load MessagesState from a file
def load_messages_state_from_file(file_path: str,first_user_input:str) -> MessagesState:
    with open(file_path, 'r') as file:
        messages_state_dict = json.load(file)
    messages_state = MessagesState(**messages_state_dict)

    messages_state.messages.append(BaseMessage(content=first_user_input, role="user"))

    return messages_state


active_users=[]
async def orquestator(state:MessagesState,config:Config):
    websocket = config["configurable"].get("websocket")
    await websocket.send_json({
        "event": "Routing..."
    })
    if config["configurable"]['thread_id'] not in active_users:
        conversation = await get_user_conversation( config["configurable"]['thread_id'],
                                                   config["configurable"]['conversation']
                                                   )
        messages_loaded=[]
        for message in conversation:
            logging.info(f"message---{message}")
            if "bot" in message:
                messages_loaded.append(AIMessage(content=message["bot"]))
            elif "user" in message:
                messages_loaded.append(HumanMessage(content=message["user"]))
        
        active_users.append(config["configurable"]['thread_id'])
        
        messages_loaded.append(HumanMessage(content=state["messages"][-1].content))
        
        return {"messages": messages_loaded}

    else:
        conversation = state["messages"]
    
        return {"messages": conversation}

async def chatbot_node(state:MessagesState,config:Config):
    logging.info(f"----------Enter chatbot node------------")

    model=ChatOllama(model=config["metadata"]["modelName"], temperature=0)
    websocket = config["configurable"].get("websocket")
    full_response = ""
    thinking=False
    async for chunk in model.astream(state["messages"]):
            
            if hasattr(chunk, 'content') and chunk.content:
             
                full_response += chunk.content
                
                if websocket:
                    
                    if chunk.content=="<think>":
                        thinking=True
                        continue
                    
                    elif chunk.content=="</think>":
                        thinking=False
                        continue
                    
                    if thinking:
                        await websocket.send_json({
                            "event": "response",
                            "step":"thinking",
                            "token": chunk.content,                
                        })

                    else:

                        try:
                            await websocket.send_json({
                                "event": "response",
                                "step":"response",
                                "response":chunk.content                                
                            })
                        except Exception as e:
                            logging.error(f"Error sending websocket message: {e}")
  
    response_message = AIMessage(content=full_response)
    
    # Guardar conversación
    await add_conversation(
        chat_name=config["configurable"]['conversation'],
        credentials=config["configurable"]['thread_id'],
        user_input=state["messages"][-1].content,
        bot_output=full_response
    )
    

    return {"messages": [response_message]}
async def image_generator(state:MessagesState,config):
    image_prompt=state["messages"][-1]["text"]
    logging.info(f"image_prompt---{image_prompt}")
    pass
