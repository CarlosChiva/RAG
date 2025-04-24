from langchain_ollama import ChatOllama
def orquestator(config):
    return "image" if config.image else "text"
def chatbot_node(state,config):
    user_input=state["input"]
    model=ChatOllama(model=config.model, temperature=0)
    response=model.invoke(user_input)
    return {"messages":response}
def image_generator(state,config):
    pass
