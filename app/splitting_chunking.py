from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain.text_splitter import RecursiveCharacterTextSplitter
from load_documents import load_documents
from load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

def split_documents(docs):
    """
    Split documents into smaller chunks for processing.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(docs)

    cleaned_chunks = filter_complex_metadata(chunks)

    return cleaned_chunks

if __name__ == "__main__":
    docs = load_documents("data/documento.pdf")
    docs += load_web_page([os.getenv('URL_1'),
            os.getenv('URL_2'),
            os.getenv('URL_3'),
            os.getenv('URL_4')])
    chunks = split_documents(docs)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        print(chunk.page_content)
        print("==="*20)
        print(f"Metadata: {chunk.metadata}")
        print("==="*20)
        print("\n")

