# src/semantic_search.py

from typing import List, Dict, Tuple
import numpy as np
from openai import OpenAI
from numpy.linalg import norm
from dotenv import load_dotenv
import os


class SemanticSearch:
    def __init__(self, api_key: str = None):
        """Initialize the semantic search engine.

        Args:
            api_key (str): OpenAI API key for creating embeddings
        """
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)
        # Dictionary to store page content with their indices
        self._pages: Dict[int, str] = {}
        # Dictionary to store embeddings with their indices
        self._embeddings: Dict[int, np.ndarray] = {}

    def add_pages(self, pages: List[str]) -> None:
        """Add pages to the search engine and create their embeddings.

        Args:
            pages (List[str]): List of page contents
        """
        for idx, page in enumerate(pages):
            # Store the original page content
            self._pages[idx] = page
            # Create and store the embedding
            embedding = self._create_embedding(page)
            self._embeddings[idx] = embedding

    def _create_embedding(self, text: str) -> np.ndarray:
        """Create an embedding for a piece of text.

        Args:
            text (str): Text to create embedding for

        Returns:
            np.ndarray: The embedding vector
        """
        response = self.client.embeddings.create(
            model="text-embedding-ada-002", input=text, encoding_format="float"
        )
        # Convert the embedding to a numpy array for easier computation
        return np.array(response.data[0].embedding)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.

        Args:
            a (np.ndarray): First vector
            b (np.ndarray): Second vector

        Returns:
            float: Cosine similarity score
        """
        return np.dot(a, b) / (norm(a) * norm(b))

    def search(self, query: str, k: int = 3) -> List[Tuple[int, str, float]]:
        """Search for the k most similar pages to the query.

        Args:
            query (str): The search query
            k (int): Number of results to return

        Returns:
            List[Tuple[int, str, float]]: List of (page_index, page_content, similarity_score)
        """
        # Create embedding for the query
        query_embedding = self._create_embedding(query)

        # Calculate similarities with all stored embeddings
        similarities = [
            (idx, self._cosine_similarity(query_embedding, emb))
            for idx, emb in self._embeddings.items()
        ]

        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top k results with their page content
        results = []
        for idx, score in similarities[:k]:
            results.append((idx, self._pages[idx], score))

        return results
