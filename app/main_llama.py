from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from app.embedding import embeddings
from app.vector_db import create_vector_store
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(
    model="llama2",
    temperature=0.3,
    base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant named Cuervo. Your sole responsibility is to answer questions strictly and only about the company Promtior. Use exclusively the information provided in the context to generate your responses. Be detailed and informative, including all relevant facts, but also clear and concise—avoid unnecessary elaboration. Do not make assumptions or fabricate information. Simply respond to the question as if you possess direct knowledge about Promtior.
            
            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | llm

# si existe la carpeta "chroma_db" la carga y si no crea la vector store
vector_store = None
if not os.path.exists("chroma_db"):
    vector_store = create_vector_store()
else:
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="chroma_db",
    )
if vector_store is None:
    raise Exception("Vector store could not be created or loaded.")

app = FastAPI(
    title="Cuervo Chatbot Assistant",
    description="RAG Chatbot Assistant that answers questions about Promtior.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# Defino el modelo para la entrada
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Endpoint to ask a question to the chatbot.
    """
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        retrieved_docs = vector_store.similarity_search(question, k=5)
        docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt_response = chain.invoke({"question": question, "context": docs_content})
        answer = prompt_response.content
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the question: {str(e)}")


