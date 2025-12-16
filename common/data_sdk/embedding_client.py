import random
from typing import List

# The vector size used by the Qdrant client and assumed embedding model
VECTOR_SIZE = 384

class MockEmbeddingClient:
    """
    A mock client for generating embeddings. 
    
    In a real-world scenario, this would use a library like sentence-transformers, 
    OpenAI/Gemini API, or a local service. Here, it returns random vectors of the 
    correct size (384) to ensure the system's infrastructure (Qdrant) 
    can function without error.
    """

    def __init__(self):
        pass

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embedding vectors for a list of text strings.

        Args:
            texts (List[str]): A list of text documents to embed.

        Returns:
            List[List[float]]: A list of embedding vectors.
        """
        embeddings = []
        for text in texts:
            # Generate a random vector of size 384 using pure Python random
            vector = [random.uniform(-1, 1) for _ in range(VECTOR_SIZE)]
            embeddings.append(vector)
            
        return embeddings

EMBEDDING_CLIENT = MockEmbeddingClient()
