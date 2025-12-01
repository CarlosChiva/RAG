import asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

# Load documents and create a VectorStoreIndex
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Define a custom function tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

# Wrap the RAG tool and the custom function as tools
async def search_documents(query: str) -> str:
    response = await query_engine.aquery(query)
    return str(response)

rag_tool = FunctionTool.from_defaults(
    fn=search_documents,
    name="search_documents",
    description="Searches documents for answers."
)
multiply_tool = FunctionTool.from_defaults(multiply)

# Create the agent with both tools
agent = FunctionAgent(
    tools=[rag_tool, multiply_tool],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="You are a helpful assistant that can search documents and multiply numbers."
)

# Example usage
async def main():
    response = await agent.run("What did the author do in college? Also, what's 7 * 8?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
