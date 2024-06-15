from langchain_community.llms.ollama import Ollama

def initialize_ollama(model_name: str):
    return Ollama(model= model_name)

async def user_input(input: str):
    try:
        llm = initialize_ollama("phi3:latest")
        response = llm.invoke(input)

    except Exception as e:
        return {"error": str(e)}

    return {"response": response}
