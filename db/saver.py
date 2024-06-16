from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from langchain.document_loaders.pdf import PyPDFLoader

def load_pdf(filename):
    loader = PyPDFLoader(filename)
    documents = loader.load()
    return documents
MODEL = "llama2"
data="path of the pdf"
document=load_pdf(data)
text_splitter= RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
all_splits = text_splitter.split_documents(document)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings(),persist_directory="db")
