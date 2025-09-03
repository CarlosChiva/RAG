from urllib import request
from langchain_ollama import ChatOllama
from langgraph.graph import  MessagesState
from config import Config
import json
from langgraph.graph.message import MessagesState,BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
import logging
logging.basicConfig(level=logging.INFO)
import websocket as ws_comfy
import uuid
import json
import urllib.request
import urllib.parse
import json
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from urllib import request
from dotenv import load_dotenv
import os
load_dotenv()
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

async def mcp_agent(state:MessagesState,config):
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
        agent = create_react_agent(model, tools)
        async for step in agent.astream({"messages":state["messages"][-1]},agent_conf, stream_mode="values"):
            logging.info(f"------------------------")
            logging.info(f"step: {step}")
            await websocket.send_json({
                    "event": "Using tools..."
                })
    except Exception as e:  
        logging.info(f"Exception: {e}")
        logging.info(f"------------------------")

    finally:
        return state


def queue_prompt(prompt, prompt_id,client_id):
    p = {"prompt": prompt, "client_id": client_id, "prompt_id": prompt_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(os.getenv("SERVER_ADDRESS")), data=data)
    urllib.request.urlopen(req).read()

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(os.getenv("SERVER_ADDRESS"), url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(os.getenv("SERVER_ADDRESS"), prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt,client_id):
    prompt_id = str(uuid.uuid4())
    queue_prompt(prompt, prompt_id,client_id)
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
            # bytesIO = BytesIO(out[8:])
            # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        images_output = []
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
        output_images[node_id] = images_output

    return output_images

import base64
import logging
import uuid
import json

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


# También mejora la función get_images para mejor manejo de errores:
def get_images(ws, prompt, client_id):
    """
    Función mejorada para obtener imágenes de ComfyUI
    """
    prompt_id = str(uuid.uuid4())
    
    try:
        queue_prompt(prompt, prompt_id, client_id)
        output_images = {}
        
        while True:
            try:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        data = message['data']
                        if data['node'] is None and data['prompt_id'] == prompt_id:
                            break  # Execution is done
                else:
                    continue  # previews are binary data
            except Exception as recv_error:
                logging.error(f"Error receiving WebSocket message: {recv_error}")
                break

        # Obtener historial y procesar imágenes
        try:
            history = get_history(prompt_id)[prompt_id]
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                images_output = []
                if 'images' in node_output:
                    for image in node_output['images']:
                        try:
                            image_data = get_image(image['filename'], image['subfolder'], image['type'])
                            if image_data:  # Verificar que los datos no estén vacíos
                                images_output.append(image_data)
                        except Exception as img_error:
                            logging.error(f"Error getting image {image['filename']}: {img_error}")
                            continue
                output_images[node_id] = images_output
                
        except Exception as history_error:
            logging.error(f"Error processing history: {history_error}")
            
        return output_images
        
    except Exception as e:
        logging.error(f"Error in get_images: {e}")
        return {}


# Función auxiliar para verificar la estructura de configuración
def validate_image_config(config):
    """
    Valida que la configuración tenga todos los campos necesarios para generar imágenes
    """
    required_keys = ["tools", "userInput"]
    configurable = config.get("configurable", {})
    
    for key in required_keys:
        if key not in configurable:
            raise KeyError(f"Missing required key: {key}")
    
    tools = configurable["tools"]
    if not tools:
        raise KeyError("tools configuration is empty")
    
    tool_config = tools.get("config", {}).get("config", {})
    if "api_json" not in tool_config:
        raise KeyError("api_json not found in tools configuration")
    
    if "positive_prompt_node" not in tool_config:
        raise KeyError("positive_prompt_node not found in tools configuration")
    
    return True