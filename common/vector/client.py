import os
import time
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "agent_nexus_test_collection"
VECTOR_DIMENSION = 4

def test_qdrant_connection():
    client = None
    max_retries = 10
    retry_delay = 5

    print(f"Attempting to connect to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    
    for i in range(max_retries):
        try:
            client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            client.get_collections()
            print("Qdrant connection successful!")
            
            print(f"Creating collection: {COLLECTION_NAME}...")
            client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_DIMENSION, distance=Distance.COSINE),
            )
            print("Collection created successfully.")

            print("Inserting sample points...")
            points = [
                PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"name": "InsightMate", "type": "lobe"}),
                PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"name": "StudyFlow", "type": "lobe"}),
            ]
            
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=points,
                wait=True
            )
            print("Sample points inserted.")

            print("Searching for similar vector...")
            search_result = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=[0.2, 0.7, 0.7, 0.2],
                limit=1
            )

            print(f"Search successful! Found {len(search_result)} result.")
            if search_result:
                print(f"Best match payload: {search_result[0].payload}")
            
            print(f"Deleting collection: {COLLECTION_NAME}")
            client.delete_collection(collection_name=COLLECTION_NAME)
            print("Cleanup complete. Vector DB integration verified.")
            break

        except Exception as e:
            if i < max_retries - 1:
                print(f"Qdrant not ready or connection failed (Attempt {i+1}/{max_retries}). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to Qdrant after {max_retries} attempts.")
                print(f"Error: {e}")
                raise
    
if __name__ == "__main__":
    test_qdrant_connection()
