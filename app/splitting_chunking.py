from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import load_documents
from load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

def split_and_chunk_documents(docs):
    """
    Split documents into smaller chunks for processing.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
    )

    chunks = text_splitter.split_documents(docs)

    cleaned_chunks = filter_complex_metadata(chunks)

    return cleaned_chunks

if __name__ == "__main__":
    docs = load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
    docs += load_documents("data/documento.pdf")
    chunks = split_and_chunk_documents(docs)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        print(chunk.page_content)
        print("==="*20)
        print(f"Metadata: {chunk.metadata}")
        print("==="*20)
        print("\n")

