from langchain_chroma import Chroma
from embedding import embeddings
from splitting_chunking import split_and_chunk_documents
from load_documents import load_documents
from load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

try:
    docs = load_documents("data/documento.pdf")
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
