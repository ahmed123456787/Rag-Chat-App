import fitz  
import sys
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config")))

from config import CHUNK_SIZE, CHUNK_OVERLAP


class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf_document = None

    def load(self):
        """Load the PDF file."""
        try:
            self.pdf_document = fitz.open(self.file_path)
            print(f"PDF loaded successfully: {self.file_path}")
        except Exception as e:
            print(f"Error loading PDF: {e}")

    def get_num_pages(self):
        """Get the total number of pages in the PDF."""
        if self.pdf_document:
            return self.pdf_document.page_count
        print("PDF not loaded.")
        return 0

    def extract_text_from_page(self, page_num):
        """Extract text from a specific page."""
        if self.pdf_document and 0 <= page_num < self.get_num_pages():
            page = self.pdf_document.load_page(page_num)
            return page.get_text()
        print(f"Invalid page number: {page_num}")
        return None

    def extract_all_text(self):
        """Extract text from all pages."""
        if self.pdf_document:
            return "\n".join(self.extract_text_from_page(i) for i in range(self.get_num_pages()))
        print("PDF not loaded.")
        return None
        
    def split_document_into_chunks(self):
        """Split the text into chunks."""
        all_text = self.extract_all_text()
        if all_text:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                add_start_index=True,
            )
            document = Document(page_content=all_text) 
            all_splits = text_splitter.split_documents([document])  
            print(f"Split document into {len(all_splits)} sub-documents.")
            return all_splits
        print("No text extracted, cannot split.")
        return []
