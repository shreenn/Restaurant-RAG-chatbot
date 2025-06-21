import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

load_dotenv()

CHROMA_DB_DIR = "chroma_db"

def run_chatbot():
    
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set. Please check your .env file and run 'python ingest.py' first.")

        print("Initializing OpenAI Embeddings model...")
        embeddings = OpenAIEmbeddings()

        print(f"Loading vector database from '{CHROMA_DB_DIR}'...")
        if not os.path.exists(CHROMA_DB_DIR):
            print(f"Error: ChromaDB directory '{CHROMA_DB_DIR}' not found. Please run 'python ingest.py' first to create it.")
            return

        db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

        print("Creating retriever...")
        
        retriever = db.as_retriever(search_kwargs={"k": 3})

        print("Initializing ChatOpenAI LLM (gpt-4o)...")
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

        print("Defining RAG prompt template...")
       
        template = """Use the following pieces of context to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question: {question}

        Helpful Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        print("Setting up RetrievalQA chain...")
       
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", 
            retriever=retriever,
            return_source_documents=True, 
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        print("\nChatbot initialized! Type your question or 'exit' to quit.")
        while True:
            user_input = input("Enter your question: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            print("AI: Thinking...")
            response = qa_chain.invoke({"query": user_input})

            print("AI:", response["result"])

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_chatbot()
