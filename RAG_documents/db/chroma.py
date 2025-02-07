from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
async def get_chain(model,vector_store):
    """ Function to get the chain. Based on the model and collection passed we get the chain."""
    """Return chain to use it :chain.invoke({"input":question})"""
    
    
    # Prompt 
    template = """Usa la información proporcionada como contexto para responder la pregunta (input) del usuario.
    Utiliza solo la informacion proporcionada en el contexto para saber si esa informacion contesta la pregunta del usuario,
    si la informacion proporcionada por el contexto es util para la respuesta,
     utilizala para contestar al usuario de lo contrario di 'no tengo informacion suficiente para responder a esta pregunta'.

    Contexto: {context}
    
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

