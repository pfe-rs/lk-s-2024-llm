# Class to load the model
import prompts

import torch
import accelerate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

torch.random.manual_seed(0)

class LanguageModel:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(LanguageModel, self).__new__(self)
        return self._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure `__init__` runs only once
            self.model = AutoModelForCausalLM.from_pretrained(
                "microsoft/Phi-3-mini-4k-instruct",
                device_map="cuda",
                torch_dtype="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True  # Add this line
            )

            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

            self.pipe = pipeline( 
                "text-generation", 
                model=self.model, 
                tokenizer=self.tokenizer, 
            )
    
    def prompt(self,msg,temp=0.0,new_tokens=500):
        if temp==0.0:
            generation_args = {
                "max_new_tokens": new_tokens,
                "return_full_text": False,
                "do_sample": False,
            }
        else:
            generation_args = {
                "max_new_tokens": new_tokens,
                "return_full_text": False,
                "temperature": temp,
                "do_sample": True,
            }

        output = self.pipe(msg, **generation_args)
        return output[0]['generated_text']
    
    def get_keyphrases(self, text):
        return self.prompt(prompts.make_multi_extraction(text),temp=0,new_tokens=500)