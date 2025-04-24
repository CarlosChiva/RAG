from langgraph.graph import StateGraph
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from nodes.nodes import chatbot_node, orquestator
from state.state import State, Config

memory = MemorySaver()


graph=StateGraph(State,Config)
# node to model

# create nodes
graph.add_node("chatbot", chatbot_node)
graph.add_node("orquestator", orquestator)
graph.add_edge(START, "orquestator")
graph.add_conditional_edges("orquestator", 
                            {"text": "chatbot"}
                            )

graph.add_edge("chatbot", END)


# build graph
graph.compile(checkpointer=memory)