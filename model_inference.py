# model_inference.py

import output_parser

from llm_class import LanguageModel

class ModelInferencing:
    def __init__(self, model: LanguageModel):
        """
        Initialize the ModelInferencing class.
        Args:
            model (LanguageModel): The language model instance.
        """
        self.model = model

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
