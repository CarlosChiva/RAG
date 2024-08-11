import Chroma_services
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import hub
from dotenv import load_dotenv
import os
load_dotenv()
TEMPLATE=os.getenv("TEMPLATE")

# Función para crear el RAG para una colección específica
def create_rag(collection_name, model_name="llama3.1"):
    # Inicializar el modelo de lenguaje
    llm = Ollama(model=model_name)
    QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")


    vectorstore = Chroma_custom()
    vectorstore=vectorstore.get_vectorstore(collection_name)
    # Crear el retriever
    retriever = vectorstore.as_retriever()
    
    rag_prompt_template = TEMPLATE

    RAG_PROMPT = PromptTemplate(
        template=rag_prompt_template,
        input_variables=["context", "question"]
    )
    # Crear la cadena de RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_PROMPT}
        )
    
    return qa_chain

# Función para realizar una consulta en una colección específica
def rag_query(collection_name, query, model_name="llama3"):
    rag = create_rag(collection_name)
    return rag(query)
