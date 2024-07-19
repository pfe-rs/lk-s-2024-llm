# model_inference.py

import output_parser
from llm_class import LanguageModel

class ModelInferencing:
    _shared_state = {}

    def __init__(self, model: LanguageModel):
        """
        Initialize the ModelInferencing class.
        Args:
            model (LanguageModel): The language model instance.
        """
        self.__dict__ = self._shared_state
        if not hasattr(self, 'initialized'):
            self.model = model
            self.initialized = True

    def get_multiple_phrases(self, text: str) -> list:
        """
        Get multiple key phrases from the input text.
        Args:
            text (str): The input text.
        Returns:
            list: The list of key phrases.
        """
        model_output = self.model.get_keyphrases(text)
        return output_parser.OutputParser.output_to_list(model_output)
    
    def get_search_phrases(self, search_text: str) -> list:
        """
        Get search key phrases from the searched text.
        Args:
            search_text (str): The input text.
        Returns:
            list: The list of search phrases.
        """
        model_output = self.model.get_searchphrases(search_text)
        return output_parser.OutputParser.output_to_list(model_output)
