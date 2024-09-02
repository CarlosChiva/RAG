from langchain_community.llms import Ollama
def get_model():
    model=Ollama(model="llama3.1:8b-instruct-q8_0",temperature=0)
    return model

