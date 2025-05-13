from langchain_chroma import Chroma
from embedding import embeddings
from splitting_chunking import split_and_chunk_documents
from load_documents import load_documents
from load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

def get_vector_store(chunks):
    """
    Create a vector store from the chunks of text.
    """
    vector_store = Chroma(
        collection_name="Documents",
        embedding_function=embeddings,
        persist_directory="db"
    )

    vector_store.add_documents(documents=chunks)

    return vector_store

if __name__ == "__main__":
    docs = load_documents("data/documento.pdf")
    docs += load_web_page([os.getenv('URL_1'),
            os.getenv('URL_2'),
            os.getenv('URL_3'),
            os.getenv('URL_4')])
    chunks = split_and_chunk_documents(docs)
    vector_store = get_vector_store(chunks)
    print("Vector store created and persisted.")