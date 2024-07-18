# llm_class.py

import prompts
import torch

from constants import PHI_MODEL_NAME
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class LanguageModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure `__init__` runs only once
            self.model = AutoModelForCausalLM.from_pretrained(
                PHI_MODEL_NAME,
                device_map="cuda",
                torch_dtype="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            self.tokenizer = AutoTokenizer.from_pretrained(PHI_MODEL_NAME)
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
            )
            self.initialized = True

    def prompt(self, msg: str, temp: float = 0.0, new_tokens: int = 500) -> str:
        """
        Generate a response from the language model given an input message.
        Args:
            msg (str): The input message.
            temp (float): Temperature for sampling. Default is 0.0.
            new_tokens (int): Number of new tokens to generate. Default is 500.
        Returns:
            str: The generated text.
        """
        generation_args = {
            "max_new_tokens": new_tokens,
            "return_full_text": False,
            "do_sample": temp != 0,
        }
        if temp != 0:
            generation_args["temperature"] = temp

        output = self.pipe(msg, **generation_args)
        return output[0]['generated_text']

    def get_keyphrases(self, text: str) -> str:
        """
        Extract keyphrases from the given text.
        Args:
            text (str): The input text.
        Returns:
            str: The extracted keyphrases.
        """
        return self.prompt(prompts.make_multi_extraction(text), temp=0, new_tokens=500)
