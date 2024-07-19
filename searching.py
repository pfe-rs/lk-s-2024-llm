import model_inference
import webpage

import numpy as np

from embedding import Embedder
from phrase_extraction_evaluation import STSEvaluation
from typing import List, Union

class PageSearch:

    def __init__(self, pages: List[webpage.Webpage]):
        self.pages = pages
    
    def get_relevance(emb_key: List[np.ndarray], emb_query: List[np.ndarray]) -> float:
        ''' Finds how relevant a page is to some keywords

            emb_key - Embeddings of key phrases of the page
            emb_query - Embeddings of search phrases 
        '''
        result = np.sum([[STSEvaluation.cosine_similarity(key, query) for key in emb_key] for query in emb_query])
        return result
    
    @staticmethod
    def search_embedded_pages(self, search_phrases: List[np.ndarray]) -> List[Union[webpage.Webpage, float]]:
        page_list=[]
        for page in self.pages:
            page_data = {
                'page': page, 
                'relevance': PageSearch.get_relevance(page.embeddings, search_phrases)
            }
            page_list.append(page_data)
        
        sorted_list = sorted(sorted_list, key=lambda x: x['relevance'])

        return sorted_list
    
    @staticmethod 
    def search_pages(self, search_text: str, model: model_inference.ModelInferencing):
        search_phrases = model.get_search_phrases(search_text)
        emb_search = Embedder.get_embedding(search_phrases)
        return PageSearch.search_embedded_pages(self, emb_search)