import time
import qdrant_client
import openai
from qdrant_client import models
from config import QDRANT_URL, COLLECTION_NAME, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, VECTOR_DIMENSION
from langchain.docstore.document import Document

# Configure Azure OpenAI
openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.azure_endpoint = AZURE_OPENAI_ENDPOINT
openai.api_version = "2023-05-15"  # Use the latest API version

class QdrantManager:
    def __init__(self):
        print("Initializing Qdrant Manager...")
        self.client = qdrant_client.QdrantClient(QDRANT_URL)
        self.collection_name = COLLECTION_NAME
        self.embedding_model = "text-embedding-ada-002"
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            if not self.client.collection_exists(self.collection_name):
                print(f"[INFO] Collection '{self.collection_name}' does not exist. Creating...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=VECTOR_DIMENSION,
                        distance=models.Distance.COSINE
                    ),
                )
                print(f"[SUCCESS] Collection '{self.collection_name}' created successfully.")
            else:
                print(f"[INFO] Collection '{self.collection_name}' already exists.")
        except Exception as e:
            print(f"[ERROR] Error creating collection: {e}")
            raise

    def _generate_embedding(self, texts):
        """Generate embeddings using Azure OpenAI."""
        try:
            print(f"[INFO] Generating embeddings for {len(texts)} texts...")
            start_time = time.time()

            response = openai.embeddings.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                input=texts
            )

            embeddings = [item.embedding for item in response.data]  # Extract embeddings
            end_time = time.time()
            print(f"[SUCCESS] Generated embeddings in {end_time - start_time:.2f} seconds.")

            return embeddings
        except Exception as e:
            print(f"[ERROR] Error generating embeddings: {e}")
            raise

    def upsert_documents(self, documents):
        """Upsert document embeddings into Qdrant."""
        self._create_collection_if_not_exists()
        points = []
        texts = []
        metadata_list = []

        print(f"[INFO] Processing {len(documents)} documents...")

        for i, doc in enumerate(documents):
            try:
                text = doc.page_content if isinstance(doc, Document) else doc["text"]
                metadata = doc.metadata if isinstance(doc, Document) else doc.get("metadata", {})
                metadata["text"] = text  # Include text content in metadata

                texts.append(text)
                metadata_list.append((i, metadata))

            except Exception as e:
                print(f"[ERROR] Error processing document {i}: {e}")

        # Generate embeddings in batch
        embeddings = self._generate_embedding(texts)

        # Create Qdrant points
        for (i, metadata), embedding in zip(metadata_list, embeddings):
            point = models.PointStruct(
                id=i,
                vector=embedding,
                payload=metadata
            )
            points.append(point)

        # Upsert to Qdrant
        if points:
            try:
                print(f"[INFO] Upserting {len(points)} documents into '{self.collection_name}'...")
                start_time = time.time()
                
                self.client.upsert(
                    collection_name=self.collection_name,
                    wait=True,
                    points=points
                )

                end_time = time.time()
                print(f"[SUCCESS] Upserted {len(points)} documents in {end_time - start_time:.2f} seconds.")
            except Exception as e:
                print(f"[ERROR] Error upserting documents: {e}")

    def search(self, query, limit=5):
        """Search for relevant documents in Qdrant."""
        try:
            print(f"[INFO] Searching for query: {query}")
            start_time = time.time()
            
            # Generate embedding for the query
            query_embedding = self._generate_embedding([query])[0]

            # Perform search in Qdrant
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
            )

            end_time = time.time()
            print(f"[SUCCESS] Search completed in {end_time - start_time:.2f} seconds.")
            return search_result
        except Exception as e:
            print(f"[ERROR] Error searching documents: {e}")
            return []

    def delete_collection(self):
        """Delete the Qdrant collection."""
        try:
            print(f"[INFO] Deleting collection '{self.collection_name}'...")
            self.client.delete_collection(self.collection_name)
            print(f"[SUCCESS] Collection '{self.collection_name}' deleted.")
        except Exception as e:
            print(f"[ERROR] Error deleting collection: {e}")

    def close(self):
        """Close the Qdrant client."""
        print("[INFO] Closing Qdrant client.")
        self.client.close()
