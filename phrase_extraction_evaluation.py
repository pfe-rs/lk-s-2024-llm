# phrase_extraction_evaluation.py

import numpy as np

from constants import EMBEDDING_MODEL_NAME
from typing import List
from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

class STSEvaluation:
    treshhold = 0.75

    @staticmethod
    def get_embedding(phrase: str) -> np.ndarray:
        """
        Get the embedding for a single phrase.
        Args:
            phrase (str): The phrase to embed.
        Returns:
            np.ndarray: The embedding vector.
        """
        return embedding_model.encode([phrase])[0]

    @staticmethod
    def get_embeddings(phrases: List[str]) -> List[np.ndarray]:
        """
        Get embeddings for a list of phrases.
        Args:
            phrases (List[str]): The phrases to embed.
        Returns:
            List[np.ndarray]: The list of embedding vectors.
        """
        return embedding_model.encode(phrases)

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two vectors.
        Args:
            a (np.ndarray): The first vector.
            b (np.ndarray): The second vector.
        Returns:
            float: The cosine similarity score.
        """
        dot_product = np.dot(a, b)
        a_magnitude = np.linalg.norm(a)
        b_magnitude = np.linalg.norm(b)
        if a_magnitude == 0 or b_magnitude == 0:
            return 0.0
        return dot_product / (a_magnitude * b_magnitude)

    @staticmethod
    def make_similarity_matrix(predictions: List[np.ndarray], labels: List[np.ndarray]) -> np.ndarray:
        """
        Create a similarity matrix between predictions and labels.
        Args:
            predictions (List[np.ndarray]): The prediction embeddings.
            labels (List[np.ndarray]): The label embeddings.
        Returns:
            np.ndarray: The similarity matrix.
        """

        return np.array([[STSEvaluation.cosine_similarity(p, l) for l in labels] for p in predictions])

    @staticmethod
    def average_cosine_score(similarity_matrix: np.ndarray) -> float:
        """
        Calculate the average cosine similarity score.
        Args:
            similarity_matrix (np.ndarray): The similarity matrix.
        Returns:
            float: The average cosine similarity score.
        """
        result = 0
        for j in range(len(similarity_matrix[0])):
            best_score = max(similarity_matrix[i][j] for i in range(len(similarity_matrix)))
            result += best_score
        return result / len(similarity_matrix[0])

    @staticmethod
    def matched_labels(similarity_matrix: np.ndarray) -> float:
        """
        Calculate the ratio of matched labels.
        Args:
            similarity_matrix (np.ndarray): The similarity matrix.
        Returns:
            float: The ratio of matched labels.
        """
        return sum(any(similarity_matrix[i][j] >= STSEvaluation.treshhold for i in range(len(similarity_matrix))) for j in range(len(similarity_matrix[0]))) / len(similarity_matrix[0])

    @staticmethod
    def redundancy(predictions: List[np.ndarray]) -> float:
        """
        Calculate the redundancy of the predictions.
        Args:
            predictions (List[np.ndarray]): The prediction embeddings.
        Returns:
            float: The redundancy score.
        """
        match_count = 0
        N = len(predictions)
        for i in range(N):
            for j in range(i + 1, N):
                if STSEvaluation.cosine_similarity(predictions[i], predictions[j]) >= STSEvaluation.treshhold:
                    match_count += 1
        return match_count / (N * (N - 1) / 2)

    @staticmethod
    def groundness(text: str, phrases: List[str]) -> float:
        """
        Calculate the groundness of the predictions.
        Args:
            text (str): The input text.
            phrases (List[str]): The predicted phrases.
        Returns:
            float: The groundness score.
        """
        count = 0
        text = text.lower()
        for phrase in phrases:
            if phrase.lower() in text:
                count += 1
        return count / len(phrases)

    @staticmethod
    def evaluate_phrases(predictions: List[str], labels: List[str], text: str) -> dict:
        """
        Evaluate the predicted phrases against the labels.
        Args:
            predictions (List[str]): The predicted phrases.
            labels (List[str]): The correct labels.
            text (str): The input text.
        Returns:
            dict: The evaluation metrics.
        """
        emb_predictions = STSEvaluation.get_embeddings(predictions)
        emb_labels = STSEvaluation.get_embeddings(labels)

        similarity_matrix = STSEvaluation.make_similarity_matrix(emb_predictions, emb_labels)

        results = {
            "cosine": STSEvaluation.average_cosine_score(similarity_matrix),
            "matchings": STSEvaluation.matched_labels(similarity_matrix),
            "redundancy": STSEvaluation.redundancy(emb_predictions),
            "groundness": STSEvaluation.groundness(text, predictions)
        }

        return results
