from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

MODEL = "llama2"
data=""
text_splitter= RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
all_splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings(),persist_directory="db")
