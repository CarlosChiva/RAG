from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv

load_dotenv()
class RagModel:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RagModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'): 
            model_name = os.getenv("MODEL")
            if model_name is None:
                raise ValueError("The environment variable 'MODEL' is not set.")
            self.model = OllamaLLM(model=model_name, temperature=0)

    def get_model(self)-> OllamaLLM:
        return self.model



