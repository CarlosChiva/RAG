from typing import Any, Dict, Literal, Optional
from dataclasses import dataclass
from pydantic import BaseModel

class Config(BaseModel):
    credentials:str
    conversation:str
    modelName:str
    userInput:str
    tools: Optional[Dict[str, Any]] = None  

    # model_name: str
    # conversation_id: str
    # image: bool
  #  path_of_image_generation_json: Optional[Literal["generation.json"]]