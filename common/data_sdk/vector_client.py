import os
from typing import List, Dict, Any

from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams, PointStruct, ScoredPoint

from common.ai_sdk import AIClient, EmbeddingProvider 

class VectorClient:
    
    def __init__(self, ai_client: AIClient):
        host = os.environ.get("QDRANT_HOST", "localhost")
        port = int(os.environ.get("QDRANT_PORT", 6333))
        
        self._qdrant = QdrantClient(host=host, port=port)
        
        self._embedder: EmbeddingProvider = ai_client.get_embedding_provider()
        
        print(f"VectorClient initialized. Qdrant host: {host}:{port}")

    def _ensure_collection_exists(self, collection_name: str):
        
        vector_dim = self._embedder.get_dimension()
        
        collections = self._qdrant.get_collections().collections
        if collection_name not in [c.name for c in collections]:
            print(f"Creating collection '{collection_name}' with {vector_dim} dimensions...")
            self._qdrant.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
            )
        else:
            print(f"Collection '{collection_name}' already exists.")

    def upsert_documents(self, collection_name: str, texts: List[str], metadatas: List[Dict[str, Any]]):
        
        if len(texts) != len(metadatas):
            raise ValueError("Texts and metadatas lists must have the same length.")

        self._ensure_collection_exists(collection_name)

        vectors = self._embedder.embed_documents(texts)
        
        points = []
        for i, (text, vector, metadata) in enumerate(zip(texts, vectors, metadatas)):
            payload = {"text": text, **metadata}
            
            points.append(
                PointStruct(
                    id=i, 
                    vector=vector,
                    payload=payload
                )
            )

        operation_info = self._qdrant.upsert(
            collection_name=collection_name,
            wait=True,
            points=points,
        )
        print(f"Successfully upserted {len(points)} points to '{collection_name}'. Status: {operation_info.status.value}")
        
    def search(self, collection_name: str, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        
        query_vector = self._embedder.embed_query(query_text)
        
        search_results: List[ScoredPoint] = self._qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True, 
            score_threshold=0.7 
        )
        
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "text": result.payload.get("text"),
                "score": result.score,
                "metadata": {k: v for k, v in result.payload.items() if k != "text"} 
            })
            
        return formatted_results

if __name__ == "__main__":
    from common.ai_sdk import AIClient 
    
    ai_client = AIClient(model_name="gpt-4o-mini")
    vector_client = VectorClient(ai_client)
    
    COLLECTION_NAME = "test_insight_data"
    
    documents = [
        "Kakarot needs to finalize the Qdrant connection setup by EOD Friday.",
        "The team decided to use LangGraph for all Agentic Brain logic.",
        "We are launching the StudyFlow agent next week.",
        "The current project phase is Phase 4: Agentic Brain (Week 9-12)."
    ]
    metadatas = [
        {"source": "meeting_01", "owner": "Kakarot"},
        {"source": "architecture_review", "owner": "Team"},
        {"source": "roadmap_update", "owner": "PM"},
        {"source": "roadmap_update", "owner": "PM"}
    ]
    
    print("\n--- Ingesting Documents into Vector Memory ---")
    vector_client.upsert_documents(COLLECTION_NAME, documents, metadatas)
    
    query = "What task was assigned to me regarding Qdrant?"
    
    print(f"\n--- Searching for Query: '{query}' ---")
    results = vector_client.search(COLLECTION_NAME, query, top_k=2)
    
    for i, result in enumerate(results):
        print(f"Result {i+1} (Score: {result['score']:.4f})")
        print(f"  Source: {result['metadata'].get('source')}")
        print(f"  Snippet: {result['text'][:60]}...")
        