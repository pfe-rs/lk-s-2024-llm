import llm_class
import model_inference

from constants import PHI_MODEL_NAME, EMBEDDING_MODEL_NAME
from datetime import datetime
from embedding import Embedder
from model_eval import ModelEval
from scraper import Scraper
from searching import PageSearch
from webpage import Webpage

import gradio as gr

model = llm_class.LanguageModel()
inference = model_inference.ModelInferencing(model)

webpage_url="https://pfe.rs/en"

pages = Scraper.scrape_from_link(webpage_url)

for i in range(len(pages)):
    text = pages[i].get_text()
    phrases = inference.get_multiple_phrases(text)
    emb_phrases = Embedder.get_embedding(phrases)
    pages[i].set_embedding(emb_phrases)

page_collection = PageSearch(pages)

while True:
    query = input()
    pages = page_collection.search_pages(query, inference)
    for page in pages:
        print(page)