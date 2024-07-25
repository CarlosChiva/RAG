from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain_community.chains import RetrievalQA
from langchain import hub
from chroma_db import get_vectorstore
QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt-llama")

embedding_model=OllamaEmbeddings()
Model = "llama2"
model=Ollama(model=Model)
vector_store= get_vectorstore(collection_name="first")
retrieval= vector_store.as_retriever()
qa_chain=RetrievalQA.from_chain_type(llm=Model,
                                    retriever=retrieval,
                                    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
question = "What is the capital of France?"
response=qa_chain.invoke({"query":question})
print(response)