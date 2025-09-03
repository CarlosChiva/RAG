
import logging
import uuid
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
import os
load_dotenv()
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
            continue 

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
                    continue  
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