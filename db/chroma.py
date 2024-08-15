from langchain_community.llms import Ollama
from langchain import hub
import os
from chroma_db import get_vectorstore_mock
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
# TEMPLATE=os.getenv("TEMPLATE")
# QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")
def get_chain(model,collection_name="first"):
    system_propmpt = """Use the given context to answer the question.
        If you don't know the answer, say you don't know.
        Use three sentence maximum and keep the answer concise.
        Context: {context}"""

    vector_store= get_vectorstore_mock(collection_name=collection_name)
    system_prompt = (
        system_propmpt
    )
    retrieval= vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(model, prompt)
    chain = create_retrieval_chain(retrieval, question_answer_chain)
    return chain

# --------------------------Example to use------------------------
Model = "llama3"
model=Ollama(model=Model,temperature=0)

question = "Me gustaría saber cómo puedo tramitar mi permiso de maternidad, soy profesora de secundaria, y si la puedo partir. Me gustaría cogerme cuando dé a luz, 9 ó 10 semanas y a partir de septiembre el resto. ¿Es esto posible? También me gustaría saber el total  de permisos que tengo. He leído que son 16 semanas y luego la lactancia, ¿podríais confirmarme cuanto es la lactancia y el final total?"

chain=get_chain(model)
answer=chain.invoke({"input":question})
print(answer['answer'])
