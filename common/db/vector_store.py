import os
from qdrant_client import AsyncQdrantClient, QdrantClient

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

sync_qdrant_client = QdrantClient(url=QDRANT_URL)

async_qdrant_client = AsyncQdrantClient(url=QDRANT_URL)

def get_async_qdrant_client() -> AsyncQdrantClient:
    return async_qdrant_client

def get_sync_qdrant_client() -> QdrantClient:
    return sync_qdrant_client