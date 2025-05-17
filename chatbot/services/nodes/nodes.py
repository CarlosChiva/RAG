from langchain_ollama import ChatOllama
from langgraph.graph import  MessagesState
from config import Config

def orquestator(state:MessagesState,config:Config):

    return {"image":str(config["metadata"]['image'])}
def chatbot_node(state:MessagesState,config:Config):
    model=ChatOllama(model=config["metadata"]["modelName"], temperature=0)
    response=model.invoke(state["messages"])
    return {"messages":response}
def image_generator(state:MessagesState,config):
    image_prompt=state["messages"][-1]["text"]

    pass
