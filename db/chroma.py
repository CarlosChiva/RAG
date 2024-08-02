from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain import hub
from chroma_db import get_vectorstore_mock
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

embedding_model=OllamaEmbeddings()
Model = "llama3.1"
model=Ollama(model=Model)
vector_store= get_vectorstore_mock(collection_name="first",top_k=5)
retrieval= vector_store.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    model, retriever=retrieval, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
question = "Que dia es la cita?"
response=qa_chain.invoke({"query":question})
print(response["result"])