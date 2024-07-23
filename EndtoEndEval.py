import llm_class
import model_inference
import prompts

from constants import PHI_MODEL_NAME, EMBEDDING_MODEL_NAME
from datetime import datetime
from embedding import Embedder
from model_eval import ModelEval
from phrase_extraction_evaluation import STSEvaluation
from scraper import Scraper
from searching import PageSearch
from webpage import Webpage

import numpy as np

dataset_folder = "./Dataset/"

texts=[]
questions=[]

for test_number in range(0, 20):
    text_file = dataset_folder + f"Sample{test_number}_text.txt"
    label_file = dataset_folder + f"Sample{test_number}_label.txt"

    with open(text_file, 'r') as file:
        text = file.read()
    with open(label_file, 'r') as file:
        queries = file.read()
    
    queries = queries.split("\n")

    texts.append(text)
    questions.append(queries)


model = llm_class.LanguageModel()
inference = model_inference.ModelInferencing(model)

text_emb = []
for text in texts:
    words = inference.get_multiple_phrases(text)
    text_emb.append(Embedder.get_embedding(words))


def softmax(x):
    # Subtract the max for numerical stability
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

def run_test(text_q):
    q_emb = Embedder.get_embedding(inference.get_search_phrases(text_q))

    result = []

    for i in range(0, len(text_emb)):
        result.append(STSEvaluation.average_cosine_score(STSEvaluation.make_similarity_matrix(text_emb[i],q_emb)))
    
    return result

def run_testset():
    results = []

    for i in range(0, len(questions)):
        for q in questions[i]:
            text_res = run_test[q]
            results.append(run_test(q))

    return results