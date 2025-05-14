from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from embedding import embeddings
from dotenv import load_dotenv
load_dotenv()

llm = ChatOllama(
    model="llama2",
    temperature=0.3,
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

vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="chroma_db",
)

print("="*20 + " Chatbot Assistance " + "="*20)
try:
    while True:
        question = input("\n\nQuestion (ctrl+c to exit): ")
        if not question:
            continue
        retrieved_docs = vector_store.similarity_search(question, k=5)
        docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = chain.invoke({"question": question, "context": docs_content})
        answer = prompt.content
        print(f"\n\nAnswer: {answer}")
        print("\n\n"+"-"*20)
except KeyboardInterrupt:
    print("\nExiting the chatbot. Goodbye!")

