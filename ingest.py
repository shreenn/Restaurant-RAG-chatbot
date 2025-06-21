import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PDF_PATH = "data/Restaurant Q&A.pdf"
CHROMA_DB_DIR = "chroma_db"

def ingest_documents():
   
    try:
        if not os.path.exists(PDF_PATH):
            print(f"Error: PDF file not found at '{PDF_PATH}'. Please ensure it's in the 'data/' directory.")
            return

        print(f"Loading document from {PDF_PATH}...")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages.")

        print("Splitting documents into chunks...")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks.")

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set. Please check your .env file.")

        print("Creating embeddings and storing in ChromaDB...")
        embeddings = OpenAIEmbeddings()

        
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_DIR
        )
        db.persist()
        print(f"Documents successfully ingested and stored in '{CHROMA_DB_DIR}'.")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during ingestion: {e}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
    ingest_documents()
