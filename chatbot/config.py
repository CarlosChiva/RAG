from pydantic import BaseModel, Field
from typing import Any, Optional, Literal
from langchain_core.runnables import RunnableConfig
import os
class Config(BaseModel):
    model:str=Field(
        defalult="llama3.2",
        title="model",
        description="Name of model used for chatbot",
    )
    conversation_id:str=Field(
        defalult="",
        title="conversation_id",
        description="ID of conversation",
    )
    image:bool=Field(
        defalult=False,
        title="image",
        description="boolean to define if it should generate image using comfyui workflow",
    )
    path_of_image_generation_json:str=Field(
        defalult="",
        title="path_of_image_generation_json",
        description="path of json file to generate image using comfyui workflow",
    )
    
    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        
        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }
        
        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}
        
        return cls(**values)