# vector_store.py
import os
import threading

# If you installed qdrant-client: uncomment import below
# from qdrant_client import QdrantClient

_lock = threading.Lock()
_client = None

def get_vector_client():
    global _client
    if _client is None:
        with _lock:
            if _client is None:
                # Replace with real client init when installed
                # _client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
                _client = {"provider": "mock", "url": os.getenv("QDRANT_URL", "http://localhost:6333")}
    return _client
