import llm_class
import output_parser

class ModelInferencing:
    def __init__(self, model):
        self.model=model
    
    def get_multiple_phrases(self, text):
        model_output=self.model.get_keyphrases(text)
        return output_parser.Output_parser.output_to_list(model_output)

