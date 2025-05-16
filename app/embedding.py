# from langchain_ollama import OllamaEmbeddings

# embeddings = OllamaEmbeddings(model="nomic-embed-text")

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import getpass
# import os

# if not os.environ.get("GEMINI_API_KEY"):
#   os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")