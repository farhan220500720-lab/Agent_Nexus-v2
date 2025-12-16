import uuid
from typing import List
from common.config import settings
from common.data_sdk.embedding_client import EMBEDDING_CLIENT
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance

VECTOR_SIZE = 384

class VectorDBClient:
    _instance = None

    def __new__(cls, host: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.host = host or settings.QDRANT_HOST
            cls._instance.client = QdrantClient(url=cls._instance.host)
        return cls._instance

    def _ensure_collection(self, collection_name: str):
        collections = self.client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
            )

    def upsert_document(self, collection_name: str, text: str, metadata: dict):
        self._ensure_collection(collection_name)

        vector = EMBEDDING_CLIENT.embed_text([text])[0]

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": text, **metadata}
        )

        self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[point]
        )
        return point.id

    def search_documents(self, collection_name: str, query_text: str, limit: int = 5):

        query_vector = EMBEDDING_CLIENT.embed_text([query_text])[0]

        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

        results = [
            {
                "text": hit.payload.get("text"),
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in search_result
        ]
        return results

VECTOR_DB_CLIENT = VectorDBClient()