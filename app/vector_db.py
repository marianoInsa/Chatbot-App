from langchain_chroma import Chroma
from app.embedding import embeddings
from app.splitting_chunking import split_and_chunk_documents
from app.load_documents import load_documents
from app.load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

def create_vector_store():
    """
    Create a vector store from documents and web pages.
    """
   
    try:
        docs = load_documents("data/documento.txt")
        docs += load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
    except Exception as e:
        print(f"Error loading documents: {e}")

    chunks = split_and_chunk_documents(docs)

    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
            )
    except Exception as e:
        print(f"Error creating vector store: {e}")

    return vector_store