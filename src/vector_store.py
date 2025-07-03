from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import hashlib
import os

def get_file_hash(file_path: str) -> str:
    """Generate a hash for the file to detect changes."""
    print(f"VectorStore: Generating hash for {file_path}")
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_vectorstore(file_path: str, embeddings: OpenAIEmbeddings) -> Chroma:

    """Load existing or create new Chroma DB for a file."""
    print(f"VectorStore: Loading vectorstore for {file_path}")
    file_hash = get_file_hash(file_path)

    persist_dir = f"./chroma_db_{file_hash}"  # Unique dir per file


    if os.path.exists(persist_dir):

        # Load existing embeddings

        print(f"VectorStore: Loading cached embeddings from {persist_dir}")

        return Chroma(

            persist_directory=persist_dir,

            embedding_function=embeddings

        )

    else:

        # Create new embeddings

        print(f"VectorStore: Creating new embeddings for {file_path}")
        loader = CSVLoader(file_path)
        docs = loader.load()
        
        # Split text if needed (e.g., large cells)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        print(f"VectorStore: Saving to Chroma {persist_dir}")

        # Save to Chroma
        vectorstore = Chroma.from_documents(

            chunks,

            embeddings,

            persist_directory=persist_dir  # Auto-saves to disk

        )

        return vectorstore
    


 