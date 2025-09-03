from langchain_ollama import ChatOllama
from langgraph.graph import  MessagesState
from config import Config
from langgraph.graph.message import MessagesState,BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import websocket as ws_comfy
import json
import base64
import uuid
from controllers.chats_controller import get_user_conversation, add_conversation
from .images_utils import get_images

from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)

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
thinking=False
async def send_message(websocket, msg_chunk):
    global thinking

    if hasattr(msg_chunk, "tool_calls") and msg_chunk.tool_calls:
        logging.info(f"🔧 Tool Call: {msg_chunk.tool_calls}")
        await websocket.send_json({
            "event": f"Using Tool {msg_chunk.tool_calls[0]['name']}",
        }) 
    if hasattr(msg_chunk, 'content') and msg_chunk.content:
        
        if websocket:
            
            if msg_chunk.content=="<think>":
                thinking=True
                return
                
                
            elif msg_chunk.content=="</think>":
                thinking=False
                return
            if thinking:
                await websocket.send_json({
                    "event": "response",
                    "step":"thinking",
                    "token": msg_chunk.content,                
                })

            else:

                try:
                    await websocket.send_json({
                        "event": "response",
                        "step":"response",
                        "response":msg_chunk.content                                
                    })
                except Exception as e:
                    logging.error(f"Error sending websocket message: {e}")

async def chatbot_node(state:MessagesState,config:Config):
    global  thinking
    logging.info(f"----------Enter chatbot node------------")

    model=ChatOllama(model=config["metadata"]["modelName"], temperature=0)
    websocket = config["configurable"].get("websocket")
    full_response=""
    async for msg_chunk  in model.astream(state["messages"]):
        full_response += msg_chunk.content
        await send_message(websocket,msg_chunk)

    logging.info(f"full_response: {full_response}")
    response_message = AIMessage(content=full_response)
    
    # Guardar conversación
    await add_conversation(
        chat_name=config["configurable"]['conversation'],
        credentials=config["configurable"]['thread_id'],
        user_input=state["messages"][-1].content,
        bot_output=full_response
    )
    thinking=False

    return {"messages": [response_message]}

async def mcp_agent(state:MessagesState,config):
    global  thinking
    logging.info(f"----------Enter Agent node------------")
    try:
        model=ChatOllama(model=config["metadata"]["modelName"], temperature=0)
        websocket = config["configurable"].get("websocket")
        await websocket.send_json({
            "event": "calling agent..."
        })
        
        tools_config = config["configurable"]["tools"]["config"]["config"]
        api_json = tools_config["api_json"]
        logging.info(f"mcp_conf: {api_json}")
        mcp_conf= config["configurable"]["tools"]["config"]["config"]["api_json"]
        thread_id = config["configurable"]["thread_id"]
        agent_conf={"configurable":{"thread_id":thread_id}}
        from langchain_mcp_adapters.client import MultiServerMCPClient
        try:
            client = MultiServerMCPClient(
                mcp_conf
            )
            tools = await client.get_tools()
        except Exception as e:
            logging.error(f"Error getting tools: {e}")
            logging.info(f"tools: {tools}")
        agent = create_react_agent(model=model, tools=tools)
        full_response=""
        async for msg_chunk,metadata in agent.astream({"messages":state["messages"][-1]},agent_conf, stream_mode="messages"):
            full_response += msg_chunk.content
            await send_message(websocket,msg_chunk)

    except Exception as e:  
        logging.info(f"Exception: {e}")
        logging.info(f"------------------------")  
    response_message = AIMessage(content=full_response)
    
    # Guardar conversación
    await add_conversation(
        chat_name=config["configurable"]['conversation'],
        credentials=config["configurable"]['thread_id'],
        user_input=state["messages"][-1].content,
        bot_output=full_response
    )
    
    full_response=""
    return {"messages": [response_message]}

async def image_generator(state: MessagesState, config):
    """
    Generador de imágenes con manejo mejorado de errores
    """
    websocket = config["configurable"].get("websocket")
    
    try:
        await websocket.send_json({
            "event": "Generating image..."
        })
        
        # Extraer configuración
        user_input = config["configurable"]["userInput"]
        tools_config = config["configurable"]["tools"]["config"]["config"]
        api_json = tools_config["api_json"]
        positive_prompt_node = tools_config["positive_prompt_node"]
        
        logging.info(f"image_prompt--- user_input: {user_input}")
        logging.info(f"positive_prompt_node: {positive_prompt_node}")
        
        client_id = str(uuid.uuid4())
        prompt = api_json.copy()  # Hacer una copia para no modificar el original
        
        # Configurar el prompt positivo
        prompt[str(positive_prompt_node)]["inputs"]["text"] = user_input
        
        # Conectar al WebSocket de ComfyUI
        ws = ws_comfy.create_connection("ws://{}/ws?clientId={}".format(
            os.getenv("SERVER_ADDRESS"), client_id
        ))
        
        try:
            # Generar imágenes
            images = get_images(ws, prompt, client_id)
            
            # Procesar las imágenes
            all_images_encoded = []
            image_count = 0
            
            for node_id in images:
                logging.info(f"Processing node: {node_id}")
                for image_data in images[node_id]:
                    if image_data:  # Verificar que image_data no esté vacío
                        try:
                            # Codificar imagen en base64
                            image_encoded = base64.b64encode(image_data).decode("utf-8")
                            all_images_encoded.append(image_encoded)
                            image_count += 1
                            logging.info(f"Image {image_count} encoded successfully")
                        except Exception as encode_error:
                            logging.error(f"Error encoding image: {encode_error}")
                            continue
            
            # Verificar si se generaron imágenes
            if all_images_encoded:
                await websocket.send_json({
                    "event": "Image generated",
                    "images": all_images_encoded,  # Enviar todas las imágenes
                    "count": len(all_images_encoded)
                })
                logging.info(f"Successfully sent {len(all_images_encoded)} images")
            else:
                await websocket.send_json({
                    "event": "Error",
                    "message": "No images were generated"
                })
                logging.warning("No images were generated")
                
        finally:
            # Asegurar que el WebSocket se cierre siempre
            ws.close()
            
    except KeyError as ke:
        error_msg = f"Configuration error: Missing key {ke}"
        logging.error(error_msg)
        try:
            await websocket.send_json({
                "event": "Error",
                "message": error_msg
            })
        except:
            logging.error("Failed to send KeyError to websocket")
            
    except Exception as e:
        error_msg = f"Error generating image: {str(e)}"
        logging.error(error_msg)
        try:
            await websocket.send_json({
                "event": "Error", 
                "message": error_msg
            })
        except:
            logging.error("Failed to send error to websocket")
    
    # Retornar el estado actualizado
    return state

