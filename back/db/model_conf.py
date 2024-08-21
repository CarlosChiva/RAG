from langchain_community.llms import Ollama
def get_model():
    model=Ollama(model="llama3.1",temperature=0)
    return model

