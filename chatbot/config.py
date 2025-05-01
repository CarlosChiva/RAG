from typing import Literal, Optional
from dataclasses import dataclass
from pydantic import BaseModel

class Config(BaseModel):
    model_name: str
    conversation_id: str
    image: bool
  #  path_of_image_generation_json: Optional[Literal["generation.json"]]