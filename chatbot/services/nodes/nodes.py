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
# Example function to save MessagesState to a file
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
    
    if config["configurable"]['thread_id'] not in active_users:
        conversation = await get_user_conversation( config["configurable"]['thread_id'],config["configurable"]['conversation'])
        messages_loaded=[]
        for message in conversation:
            logging.info(f"message---{message}"   )
            if "bot" in message:
                messages_loaded.append(AIMessage(content=message["bot"]))  # ✅ Use the actual value
            elif "user" in message:
                messages_loaded.append(HumanMessage(content=message["user"]))
        active_users.append(config["configurable"]['thread_id'])
        logging.info(f"not in active users:   {state}      {messages_loaded}")
        messages_loaded.append(HumanMessage(content=state["messages"][-1].content))
        return {"messages": messages_loaded}

    else:
        conversation = state["messages"]  # Use the existing messages if the user is already active
    
        return {"messages": conversation}

async def chatbot_node(state:MessagesState,config:Config):
    logging.info(f"----------Enter chatbot node------------")
    # logging.info(f"--state---{state}")
    # logging.info(f"response---{response}")
    # logging.info(f"""config---{config["configurable"]['conversation'],
    #                        config["configurable"]['thread_id'],
    #                        state["messages"][-1],
    #                        response.content}""")
    model=ChatOllama(model=config["metadata"]["modelName"], temperature=0)
    websocket = config["configurable"].get("websocket")
    full_response = ""
    thinking=False
    async for chunk in model.astream(state["messages"]):
            if hasattr(chunk, 'content') and chunk.content:
                full_response += chunk.content
                
                # Enviar cada token por websocket si está disponible
                if websocket:
                    if chunk.content=="<think>":
                        thinking=True
                        continue
                    elif chunk.content=="</think>":
                        thinking=False
                        continue
                    if thinking:
                        await websocket.send_json({
                            "token": chunk.content,
                            "event": "thinking",
                            
                        })
                    else:

                        try:
                            await websocket.send_json({
                                "token": chunk.content,
                                "event": "response"
                            })
                        except Exception as e:
                            logging.error(f"Error sending websocket message: {e}")
       # Crear mensaje de respuesta completo
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

    pass
