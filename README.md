Restaurant Q&A Chatbot (RAG-based LLM)This project implements a simple Retrieval Augmented Generation (RAG) system using LangChain, OpenAI, and ChromaDB. It's designed to answer questions specifically about a restaurant, using information extracted from a provided PDF document ("Restaurant Q&A.pdf").FeaturesDocument Ingestion: Loads a PDF document, splits it into manageable chunks, and creates vector embeddings.Vector Database: Stores document chunks and their embeddings in ChromaDB for efficient similarity search.Retrieval Augmented Generation (RAG): Retrieves relevant document chunks based on a user's query and then uses these chunks as context for a Large Language Model (LLM) to generate accurate answers.Command-Line Interface (CLI): A simple interface to interact with the chatbot.Project Structure.
├── data/
│   └── Restaurant Q&A.pdf  # Your Q&A document
├── .env.example            # Template for environment variables
├── app.py                  # Main application script (chatbot CLI)
├── ingest.py               # Script to process and ingest documents into the vector DB
└── requirements.txt        # Python dependencies
└── README.md               # This file
PrerequisitesBefore you begin, ensure you have the following installed:Python 3.9+pip (Python package installer)Setup InstructionsFollow these steps to get the project up and running:1. Clone the RepositoryFirst, clone this repository to your local machine:git clone <your-repository-url>
cd <your-repository-name>
2. Create a Virtual Environment (Recommended)It's good practice to use a virtual environment to manage project dependencies:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install DependenciesInstall all the required Python packages:pip install -r requirements.txt
4. Place Your DocumentEnsure your Restaurant Q&A.pdf file is placed inside the data/ directory.5. Configure Environment VariablesCreate a .env file in the root of your project based on the .env.example template:cp .env.example .env
Now, open the newly created .env file and add your OpenAI API key:OPENAI_API_KEY="your_openai_api_key_here"
Important: Never commit your actual .env file to version control (GitHub). The .gitignore file should already be configured to ignore it.6. Ingest DataRun the ingest.py script to process your PDF document and store its content in the ChromaDB vector database. This needs to be done only once, or whenever your Restaurant Q&A.pdf file changes.python ingest.py
This will create a chroma_db directory in your project root, containing the vector database.How to Run the ChatbotAfter completing the setup and data ingestion, you can start the chatbot:python app.py
The chatbot will prompt you to enter questions. Type your query and press Enter. Type exit to quit.Example UsageEnter your question (type 'exit' to quit): What are your hours of operation?
AI: We are open from 11:00 AM to 10:00 PM on weekdays and from 9:00 AM to 11:00 PM on weekends.

Enter your question (type 'exit' to quit): Do you have wi-fi?
AI: Yes, free Wi-Fi is available for all dining guests. Please ask for the network and password at the host stand.

Enter your question (type 'exit' to quit): exit
Goodbye!
