from langchain_ollama import ChatOllama
from langgraph.graph import  MessagesState
from config import Config
def orquestator(state:MessagesState,config:Config):

    return {"image":str(config["metadata"]['image'])}
def chatbot_node(state:MessagesState,config:Config):
    print(config["metadata"])
    model=ChatOllama(model=config["metadata"]["model_name"], temperature=0)
    response=model.invoke(state["messages"])
    print(response.content)
    return {"messages":response.content}
def image_generator(state:MessagesState,config):
    image_prompt=state["messages"][-1]["text"]

    pass
