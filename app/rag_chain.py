from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from vector_db import get_vector_store
from splitting_chunking import split_and_chunk_documents
from load_documents import load_documents
from load_web_page import load_web_page
import os
from dotenv import load_dotenv
load_dotenv()

def get_rag_chain(chunks):
    """
    Create a Retrieval-Augmented Generation (RAG) chain
    """
    # prompt_template = PromptTemplate(
    #     template="""
    #     Your name is Cuervo, you are a helpful assistant. Answer the question based on the context provided.
    #     """
    # )

    llm = OllamaLLM(model="llama2", temperature=0.1, max_tokens=1500)
    vector_store = get_vector_store(chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever

        # chain_type="stuff",
        # chain_type_kwargs={"prompt": prompt_template}
    )
    return rag_chain

if __name__ == "__main__":
    docs = load_documents("data/documento.pdf")
    docs = load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
    chunks = split_and_chunk_documents(docs)
    rag_chain = get_rag_chain(chunks)
    query = "What services does Promtior offer?"
    result = rag_chain.invoke({"query": query})
    print(result['result'])
    print("==="*20)