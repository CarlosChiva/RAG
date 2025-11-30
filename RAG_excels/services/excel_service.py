from langchain_community.document_loaders import UnstructuredExcelLoader

def file_loader():
    loader = UnstructuredExcelLoader("./example_data/stanley-cups.xlsx", mode="elements")
    docs = loader.load()
