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


# def queue_prompt(prompt):
#     p = {"prompt": prompt}


#     data = json.dumps(p).encode('utf-8')
#     req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
#     request.urlopen(req)




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
async def image_generator(state:MessagesState,config):
    websocket = config["configurable"].get("websocket")
    await websocket.send_json({
        "event": "Generating image..."
    })
    logging.info(f"image_prompt---{config["configurable"]["userInput"]}    {config["configurable"]["tools"]["image_tools"]["api_json"]}  {config["configurable"]["tools"]["image_tools"]["positive_prompt_node"]}")
    client_id = str(uuid.uuid4())


    prompt = config["configurable"]["tools"]["image_tools"]["api_json"]
    #set the text prompt for our positive CLIPTextEncode
    prompt[str(config["configurable"]["tools"]["image_tools"]["positive_prompt_node"])]["inputs"]["text"] = config["configurable"]["userInput"]
    try:

        ws = ws_comfy.create_connection("ws://{}/ws?clientId={}".format(os.getenv("SERVER_ADDRESS"), client_id))
        ws.connect("ws://{}/ws?clientId={}".format(os.getenv("SERVER_ADDRESS"), client_id))
        images =  get_images(ws, prompt,client_id)
        ws.close() # for in case this example is used in an environment where it will be repeatedly called, like in a Gradio app. otherwise, you'll randomly receive connection timeouts
       
        for node_id in images:
            for image_data in images[node_id]:
               # from PIL import Image
                import io
                image = image_data#io.BytesIO(image_data)
       
        logging.info(f"images---{image}")
        image_encode = base64.b64encode(image).decode("utf-8")
        await websocket.send_json({
            "event": "Image generated",
            "images": image_encode
        })
    except Exception as e:
        logging.error(f"Error sending websocket message: {e}")

    pass
