from langgraph import Graph
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from config import Config
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.message import add_messages

memory = MemorySaver()

class State(TypedDict):
    messages:annotated[list,add_messages]

graph=StateGraph(State)
# node to model
def chatbot_node(state):
    user_input=state["input"]
    model=ChatOllama(model=Config.MODEL, temperature=0)
    response=model.invoke(user_input)
    return {"messages":response}

# create nodes
graph.add_edge(START, "chatbot")

graph.add_node("chatbot", chatbot_node)
graph.add_edge("chatbot", END)


# build graph
graph.compile(checkpointer=memory)