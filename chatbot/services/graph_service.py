from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.redis import RedisSaver
from services.nodes.nodes import chatbot_node, orquestator,image_generator,mcp_agent
from services.state import Config
from langgraph.checkpoint.memory import MemorySaver
import logging 
logging.basicConfig(level=logging.INFO)
def routing_logic(state, config):
    """
    Función de enrutamiento que decide el siguiente nodo basado en la configuración de tools
    
    Lógica:
    - Si no hay tools -> va a chatbot_node
    - Si hay tools y type="images" -> va a image_generator
    - Si hay tools y type="mcp" -> va a mcp_agent_node
    """
    print(f"🔍 Routing - State: {state}")
    print(f"🔍 Routing - Config completo: {config}")
    
    # CORRECCIÓN: Acceder a tools desde configurable
    configurable = config.get("configurable", {})
    tools_config = configurable.get("tools")
    
    print(f"🔍 Configurable: {configurable}")
    print(f"🔍 Tools config: {tools_config}")
    
    # Si no hay tools, ir a chatbot
    if not tools_config:
        print("➡️  Enrutando a: chatbot (sin tools)")
        return "chatbot"
    
    # Si hay tools, verificar el tipo
    tool_type = tools_config.get("type")
    logging.info(f"tool_type: {tool_type}")
    print(f"🔍 Tool type: {tool_type}")
    
    if tool_type == "image":
        print("➡️  Enrutando a: image_generator")
        return "image_generator"
    elif tool_type == "mcp":
        print("➡️  Enrutando a: mcp_agent")
        return "mcp_agent"
    else:
        print(f"➡️  Enrutando a: chatbot (tipo desconocido: {tool_type})")
        return "chatbot"



builder=StateGraph(state_schema=MessagesState, config_schema=Config)
# node to model

# create nodes

builder.add_node("orquestator", orquestator)
builder.add_node("chatbot", chatbot_node)

builder.add_node("image_generator", image_generator)
builder.add_node("mcp_agent", mcp_agent)

builder.add_edge(START, "orquestator")

# Ruta única desde orquestator
builder.add_conditional_edges(
    "orquestator",
    routing_logic,
    {
        "chatbot": "chatbot",
        "image_generator": "image_generator", 
        "mcp_agent": "mcp_agent"
    }
)
builder.add_edge("chatbot", END)
builder.add_edge("image_generator", END)
builder.add_edge("mcp_agent", END)

memory=MemorySaver()
graph=builder.compile(checkpointer=memory)
