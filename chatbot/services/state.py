from dataclasses import dataclass
from typing import Any, Optional, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

class Config(TypedDict):
    model: str
    conversation_id: str
    image: bool 
    path_of_image_generation_json: Optional[Literal["generation.json"]]

class State(TypedDict):
    messages:Annotated[list,add_messages]
