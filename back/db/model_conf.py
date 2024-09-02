from langchain_community.llms import Ollama
import os
def get_model():
    MODEL=os.getenv("MODEL")
    model=Ollama(model=MODEL,temperature=0)
    return model

