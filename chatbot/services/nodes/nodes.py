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

import json
from urllib import request

def queue_prompt(prompt):
    p = {"prompt": prompt}


    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)


import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    current_node = ""
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['prompt_id'] == prompt_id:
                    if data['node'] is None:
                        break #Execution is done
                    else:
                        current_node = data['node']
        else:
            if current_node == 'save_image_websocket_node':
                images_output = output_images.get(current_node, [])
                images_output.append(out[8:])
                output_images[current_node] = images_output

    return output_images






async def image_generator(state:MessagesState,config):
    websocket = config["configurable"].get("websocket")
    await websocket.send_json({
        "event": "Generating image..."
    })
    logging.info(f"image_prompt---{config["configurable"]["userInput"]}    {config["configurable"]["tools"]["image_tools"]["api_json"]}  {config["configurable"]["tools"]["image_tools"]["positive_prompt_node"]}")


    prompt = config["configurable"]["tools"]["image_tools"]["api_json"]
    #set the text prompt for our positive CLIPTextEncode
    prompt[str(config["configurable"]["tools"]["image_tools"]["positive_prompt_node"])]["inputs"]["text"] = config["configurable"]["userInput"]
    try:

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        images = get_images(ws, prompt)
        ws.close() # for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
        websocket.send_json({
            "event": "Image generated",
            "images": images
        })
    except Exception as e:
        logging.error(f"Error sending websocket message: {e}")

    pass
