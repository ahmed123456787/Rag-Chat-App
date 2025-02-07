import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from loader import PDFLoader
from embeddings import QdrantManager


if __name__ == "__main__":
    # Load and process the PDF
    pdf_loader = PDFLoader("/home/ahmed/Desktop/Rag-Chat-App/back/core/rag/LSTM.pdf")
    pdf_loader.load()
    
    splits = pdf_loader.split_document_into_chunks()
    
    if splits:
        # Initialize QdrantManager
        qdrant_manager = QdrantManager()

        # Upsert the document chunks into Qdrant
        qdrant_manager.upsert_documents(splits)

        # Perform a search query
        search_results = qdrant_manager.search("What is LSTM used for?")
        
        # Extract text from the search results
        top_texts = [result.payload["text"] for result in search_results]

        # Print extracted texts
        for i, text in enumerate(top_texts, 1):
            print(f"Result {i}: {text}")
        else:
            print("No relevant results found.")

        # Close the Qdrant client
        qdrant_manager.close()
    else:
        print("No document chunks to store.")
