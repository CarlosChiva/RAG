from dataclasses import dataclass
from typing import Any, Optional, Literal
from typing_extensions import TypedDict


class Config(TypedDict):
    model: str
    conversation_id: str
    image: bool 
    path_of_image_generation_json: Optional[Literal["generation.json"]]

class State(TypedDict):
    messages:Annotated[list,add_messages]
