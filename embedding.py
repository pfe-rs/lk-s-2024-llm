# embedding.py

import numpy as np

from constants import EMBEDDING_MODEL_NAME
from sentence_transformers import SentenceTransformer
from typing import List

class Embedder:
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    @staticmethod
    def get_embedding(phrase: str) -> np.ndarray:
        """
        Get the embedding for a single phrase.
        Args:
            phrase (str): The phrase to embed.
        Returns:
            np.ndarray: The embedding vector.
        """
        return Embedder.embedding_model.encode([phrase])[0]

    @staticmethod
    def get_embedding(phrases: List[str]) -> List[np.ndarray]:
        """
        Get embeddings for a list of phrases.
        Args:
            phrases (List[str]): The phrases to embed.
        Returns:
            List[np.ndarray]: The list of embedding vectors.
        """
        return Embedder.embedding_model.encode(phrases)
