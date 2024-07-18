# Class to evaluate model output

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class STSEvaluation:
    treshhold=0.75

    @staticmethod
    def get_embedding(phrase: str) -> np.ndarray:
        return embedding_model.encode([phrase])[0]

    @staticmethod
    def get_embeddings(phrases: List[str]) -> List[np.ndarray]:
        return embedding_model.encode(phrases)
    
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        dot_product = np.dot(a, b)
        a_magnitude = np.linalg.norm(a)
        b_magnitude = np.linalg.norm(b)
        if a_magnitude == 0 or b_magnitude == 0:
            return 0.0
        return dot_product / (a_magnitude * b_magnitude)
    
    @staticmethod
    def make_similarity_matrix(predictions, labels):
        similarity_matrix=np.zeros([len(predictions),len(labels)])
        for i in range(0, len(predictions)):
            for j in range(0,len(labels)):
                similarity_matrix[i][j]=STSEvaluation.cosine_similarity(predictions[i],labels[j])
        return similarity_matrix
    @staticmethod
    def average_cosine_score(similarity_matrix) -> float:
        result = 0
        for j in range(0, len(similarity_matrix[0])):
            best_score=0
            for i in range(0,len(similarity_matrix)):
                if best_score<similarity_matrix[i][j]:
                    best_score=similarity_matrix[i][j]
            result+=best_score
        return result / len(similarity_matrix[0])
    
    @staticmethod
    def matched_labels(similarity_matrix) -> float:
        result = 0
        for j in range(0, len(similarity_matrix[0])):
            matched=0
            for i in range(0,len(similarity_matrix)):
                if similarity_matrix[i][j] >= STSEvaluation.treshhold:
                    matched=1
                    break
            result+=matched
        return result / len(similarity_matrix[0])
    
    @staticmethod 
    def redundancy(predictions):
        match_count=0
        N=len(predictions)
        for i in range(0,N):
           for j in range(i+1,N):
                if(STSEvaluation.cosine_similarity(predictions[i],predictions[j])>=STSEvaluation.treshhold):
                    match_count+=1
        return match_count/(N*(N-1)/2)

    @staticmethod
    def groundness(text,phrases):
        count=0
        text=text.lower()
        for phrase in phrases:
            if phrase.lower() in text:
                count+=1
        return count/len(phrases)

    @staticmethod 
    def evaluate_phrases(predictions: List[str], labels: List[str], text) -> dict:
        emb_predictions = STSEvaluation.get_embeddings(predictions)
        emb_labels = STSEvaluation.get_embeddings(labels)

        similarity_matrix = STSEvaluation.make_similarity_matrix(emb_predictions,emb_labels)

        results = { 
            "cosine": STSEvaluation.average_cosine_score(similarity_matrix),
            "matchings": STSEvaluation.matched_labels(similarity_matrix),
            "redundancy": STSEvaluation.redundancy(emb_predictions),
            "groundness":STSEvaluation.groundness(text, predictions)
        }

        return results