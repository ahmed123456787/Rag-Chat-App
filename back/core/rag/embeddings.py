import qdrant_client
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.docstore.document import Document  # If you're using LangChain Documents


class QdrantManager:
    def __init__(self, qdrant_url="http://localhost:6333", collection_name="my_rag_collection", embedding_model='all-mpnet-base-v2'):
        self.client = qdrant_client.QdrantClient(qdrant_url)
        self.collection_name = collection_name
        self.model = SentenceTransformer(embedding_model)  # Initialize embedding model here
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        if not self.client.has_collection(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qdrant_client.models.VectorParams(size=self.model.get_sentence_embedding_dimension(), distance=qdrant_client.models.Distance.COSINE),  # Use model's dimension
            )

    def upsert_documents(self, documents):  # Accepts LangChain Documents or lists of strings/dicts
        points = []
        for i, doc in enumerate(documents):
            if isinstance(doc, Document): 
                text = doc.page_content
                metadata = doc.metadata or {}  # Use metadata from Document object
            elif isinstance(doc, str):  # Handle plain strings
              text = doc
              metadata = {}
            elif isinstance(doc, dict): # handle dictionary
              text = doc["text"]
              metadata = doc.get("metadata", {})

            else:
                raise TypeError("Documents must be LangChain Documents, strings, or dictionaries")  # Handle other types as needed

            embedding = self.model.encode(text)
            points.append(
                qdrant_client.models.PointStruct(id=i, vector=embedding.tolist(), payload=metadata)
            )

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )

    def search(self, query, limit=2):
        query_embedding = self.model.encode(query)
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=limit,
        )
        return search_result

    def close(self):
        self.client.close()


# Example usage with LangChain Documents:
documents = [
    Document(page_content="This is the first document chunk.", metadata={"source": "doc1.pdf", "page": 1}),
    Document(page_content="This is the second chunk, related to the first.", metadata={"source": "doc1.pdf", "page": 2}),
    Document(page_content="This is a completely different topic.", metadata={"source": "doc2.pdf", "page": 1}),
]

qdrant_manager = QdrantManager()  # Use default parameters or provide custom ones
qdrant_manager.upsert_documents(documents)

search_results = qdrant_manager.search("What is the first document about?")
print(search_results)

qdrant_manager.close()

