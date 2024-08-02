from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# Función para cargar un documento PDF
def load_pdf(filename):
    loader = PyPDFLoader(filename)
    documents = loader.load()
    return documents

# Función para dividir el texto de los documentos
def text_split(documents, chunk_size=1500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(documents)
    return all_splits
# Función para inicializar el modelo y tokenizer de embeddings
def init_embedding_model():
    embedding_func = OllamaEmbeddings(model="llama3.1")
    return embedding_func

def docs_post_processing(docs):
    return "\n\n".join(doc.page_content for doc in docs)
