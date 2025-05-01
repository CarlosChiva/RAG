from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from services.nodes.nodes import chatbot_node, orquestator,image_generator
from services.state import Config

memory = MemorySaver()


builder=StateGraph(state_schema=MessagesState, config_schema=Config)
# node to model

# create nodes

builder.add_node("orquestator", orquestator)
builder.add_node("chatbot", chatbot_node)
builder.add_node("image_generator", image_generator)
builder.add_edge(START, "orquestator")
builder.add_conditional_edges("orquestator",
                                lambda state: state["image"],  # Use a lambda to return the boolean

                                    {
                                        "True": "image_generator",
                                        "False": "chatbot"
                                    }                   
                                )   

builder.add_edge("chatbot", END)
builder.add_edge("image_generator", END)


# build graph
graph=builder.compile(checkpointer=memory)
