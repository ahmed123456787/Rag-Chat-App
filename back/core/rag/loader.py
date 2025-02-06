import fitz  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config.config import CHUNK_OVERLAP, CHUNK_SIZE


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
        else:
            print("PDF not loaded.")
            return 0


    def extract_text_from_page(self, page_num):
        """Extract text from a specific page."""
        if self.pdf_document and 0 <= page_num < self.get_num_pages():
            page = self.pdf_document.load_page(page_num)
            return page.get_text()
        else:
            print(f"Invalid page number: {page_num}")
            return None


    def extract_all_text(self):
        """Extract text from all pages."""
        if self.pdf_document:
            all_text = ""
            for page_num in range(self.get_num_pages()):
                all_text += self.extract_text_from_page(page_num) + "\n"
            return all_text
        else:
            print("PDF not loaded.")
            return None
        

    def split_document_into_chunks(self):
        """Split the text into chunks."""

        all_text = self.extract_all_text()  # Get all the text

        if all_text:  # Check if text was extracted successfully
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                add_start_index=True,
            )

            # Create a LangChain Document object
            document = Document(page_content=all_text) 
            all_splits = text_splitter.split_documents([document])  

            print(f"Split document into {len(all_splits)} sub-documents.")
            return all_splits # Return the splits if needed

        else:
            print("No text extracted, cannot split.")
            return [] # Or None, depending on your needs




if __name__ == "__main__":
    pdf_loader = PDFLoader("/home/ahmed/Desktop/Rag-Chat-App/back/core/rag/LSTM.pdf")
    pdf_loader.load()

    splits = pdf_loader.split_document_into_chunks()
    print(len(splits))
    # if splits:
    #   for i, split in enumerate(splits):
    #       print(f"Chunk {i+1}: {split.page_content[:50]}...") # Print a snippet of each chunk
    #       # Do something with the split documents, like store them in a vector database
    # else:
    #   print("No splits generated.")