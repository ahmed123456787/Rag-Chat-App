import sys
import os
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from loader import PDFLoader
from embeddings import QdrantManager
from llm_response import generate_llm_response
from django.conf import settings


def init(document_path,query:str):

    file_path = os.path.join(settings.MEDIA_ROOT, "documents", document_path)

    # Load and process the PDF
    pdf_loader = PDFLoader(file_path=file_path)
    pdf_loader.load()
    
    splits = pdf_loader.split_document_into_chunks()
    
    if splits:
        # Initialize QdrantManager
        qdrant_manager = QdrantManager()

        # Upsert the document chunks into Qdrant
        qdrant_manager.upsert_documents(splits)

        # Perform a search query
        search_results = qdrant_manager.search(query)
        
        # Extract text from the search results
        top_texts = [result.payload["text"] for result in search_results]

        generated_response = generate_llm_response(top_texts,query)
        print("generate",generated_response)


        # Close the Qdrant client
        qdrant_manager.close()
        return generated_response
    else:
        print("No document chunks to store.")
