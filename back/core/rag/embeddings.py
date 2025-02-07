import qdrant_client
from qdrant_client import models
from sentence_transformers import SentenceTransformer
from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_MODEL
from langchain.docstore.document import Document

class QdrantManager:
    def __init__(self):
        self.client = qdrant_client.QdrantClient(QDRANT_URL)
        self.collection_name = COLLECTION_NAME
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.model.get_sentence_embedding_dimension(), 
                        distance=models.Distance.COSINE
                    ),
                )
                print(f"Collection '{self.collection_name}' created.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            print(f"Error creating collection: {e}")

    def upsert_documents(self, documents):
        """Upsert document embeddings into Qdrant."""
        points = []
        for i, doc in enumerate(documents):
            text = doc.page_content if isinstance(doc, Document) else doc["text"]
            metadata = doc.metadata if isinstance(doc, Document) else doc.get("metadata", {})
            metadata["text"] = text  # Include text content
            embedding = self.model.encode(text)
            points.append(models.PointStruct(id=i, vector=embedding.tolist(), payload=metadata))

        self.client.upsert(collection_name=self.collection_name, wait=True, points=points)
        print(f"Upserted {len(points)} documents into '{self.collection_name}'.")

    def search(self, query, limit=5):  # Default limit is 5
        """Search for relevant documents in Qdrant."""
        query_embedding = self.model.encode(query)
        
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=limit,
        )
        
        return search_result

    def delete_collection(self):
        """Delete the Qdrant collection."""
        self.client.delete_collection(self.collection_name)
        print(f"Collection '{self.collection_name}' deleted.")

    def close(self):
        """Close the Qdrant client."""
        self.client.close()
