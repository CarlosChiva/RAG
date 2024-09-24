from langchain_community.llms import Ollama
from langchain import hub
#import os
from db.chroma_manager import get_vectorstore, get_vectorstore_mock
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
# TEMPLATE=os.getenv("TEMPLATE")
# QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")
async def get_chain(model):
    """ Function to get the chain. Based on the model and collection passed we get the chain."""
    """Return chain to use it :chain.invoke({"input":question})"""
    
    vector_store= await get_vectorstore()
    
    # Prompt 
    template = """Usa la siguiente información para responder la pregunta del usuario.
    Si no hay información proporcionada, di "No tengo suficiente información para responder a esta pregunta".

    Información: {context}
    
    Pregunta: {input}

    Respuesta:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "input"])
    
    # build chain
    retriever = vector_store.as_retriever(search_type="mmr",search_kwargs={"k": 3})
    
    # Crear la cadena de pregunta-respuesta
    qa_chain = create_stuff_documents_chain(model, prompt)
    
    # Crear la cadena de recuperación
    chain = create_retrieval_chain(retriever, qa_chain)
    
    return chain

