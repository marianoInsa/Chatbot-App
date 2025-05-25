from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_chroma import Chroma
from app.embedding import embeddings
# from app.vector_db import create_vector_store
from langchain_core.vectorstores import InMemoryVectorStore
from app.splitting_chunking import split_and_chunk_documents
from app.load_documents import load_documents
from app.load_web_page import load_web_page
# import google.generativeai as genai
from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

os.environ.get("LANGSMITH_TRACING")
os.environ.get("LANGSMITH_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/credentials.json"

# client = genai.Client(api_key='GEMINI_API_KEY')
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# if not os.environ.get("GEMINI_API_KEY"):
#   os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# if not os.environ.get("GEMINI_API_KEY"):
#   os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise RuntimeError("GEMINI_API_KEY no está definido en las variables de entorno")

# from langchain.chat_models import init_chat_model

# llm = init_chat_model("gemini-2.0-flash-001", model_provider="google_genai")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0.3,
    google_api_key=gemini_key
)

# Definicion del prompt para responder preguntas
prompt = hub.pull("rlm/rag-prompt")

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#             You are a helpful assistant named Cuervo. Your sole responsibility is to answer questions strictly and only about the company Promtior. Use exclusively the information provided in the context to generate your responses. Be detailed and informative, including all relevant facts, but also clear and concise—avoid unnecessary elaboration. Do not make assumptions or fabricate information. Simply respond to the question as if you possess direct knowledge about Promtior.
            
#             Context: {context}
#             """,
#         ),
#         ("human", "{question}"),
#     ]
# )

# chain = prompt | llm

# si existe la carpeta "chroma_db" la carga y si no crea la vector store
# vector_store = None
# if not os.path.exists("chroma_db"):
#     vector_store = create_vector_store()
# else:
#     vector_store = Chroma(
#         embedding_function=embeddings,
#         persist_directory="chroma_db",
#     )
# if vector_store is None:
#     raise Exception("Vector store could not be created or loaded.")


# carga la vector store
vector_store = InMemoryVectorStore(embeddings)

# carga los documentos y la web
docs = []
try:
    docs = load_documents("data/documento.txt")
    docs += load_web_page(os.getenv('URL_1'), os.getenv('URL_2'), os.getenv('URL_3'), os.getenv('URL_4'))
except Exception as e:
    print(f"Error loading documents: {e}")

chunks = split_and_chunk_documents(docs)

# Indexar chunks en la vector store
_ = vector_store.add_documents(documents=chunks)

# Define el estado de la app
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# Defino los pasos de la app
# Primero, la recuperacion de contexto relevante
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

# Segundo, la generacion de respuesta
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

# Compilacion de la app
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

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
    # question = request.question
    # if not question:
    #     raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    # try:
    #     retrieved_docs = vector_store.similarity_search(question, k=5)
    #     docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])
    #     prompt_response = chain.invoke({"question": question, "context": docs_content})
    #     answer = prompt_response.content
    #     return {"answer": answer}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error processing the question: {str(e)}")

    try:
        question = request.question
        response = graph.invoke({"question": question})
        answer = response["answer"]
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
