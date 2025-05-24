from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableBinding

async def get_chain(model,vector_store)-> RunnableBinding:
    """ Function to get the chain. Based on the model and collection passed we get the chain."""
    """Return chain to use it :chain.invoke({"input":question})"""
    
    
    # Prompt 
    template = """Eres un asistente que responde a las preguntas del usuario solo en base a la informacion guardada en el contexto.
    La informacion proporcionada en el contexto esta enviada desde la propia base de datos.
    Tambien puedes utilizar el historial de chat para responder a las preguntas del usuario.
    Historial de chat: {chat_history}
    Contexto: {context}
    Pregunta: {input}

    Objetivos: 
        - Analiza la informacion proporcionada del contexto para saber si responde a la pregunta del usuario.
        - Usa solo la información proporcionada del contexto para responder la pregunta (input) del usuario.
        - Utiliza solo la informacion proporcionada en el contexto para saber si esa informacion contesta la pregunta del usuario correctamente,
        - Si la informacion proporcionada por el contexto es util para la respuesta, utilizala para contestar al usuario
        - Si la informacion proporcionada por el contexto no es util para la respuesta, responde solo 'no tengo informacion suficiente para responder a esta pregunta'.
    Responde siempre con formato markdown.
     Respuesta:"""
    
    prompt = PromptTemplate(template=template, input_variables=["context", "input", "chat_history"])
    
    # build chain
    retriever = vector_store.as_retriever(search_type="mmr",search_kwargs={"k": 3})
    
    # Crear la cadena de pregunta-respuesta
    qa_chain = create_stuff_documents_chain(model, prompt)
    
    # Crear la cadena de recuperación
    return  create_retrieval_chain(retriever, qa_chain)
    

