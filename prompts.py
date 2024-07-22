# prompts.py

import json

from typing import List

multiple_keyphrases_text = """Bed Bath & Beyond Gains Bed Bath & Beyond, the largest United States home furnishings retailer, posted higher second-quarter profit, helped by sales of back-to-college merchandise. Net income climbed 2.9 percent, to $145.5 million, or 51 cents a share, matching analyst estimates. Revenue in the three months that ended Aug. 26 increased 12 percent, to $1.61 billion, the company, based in Union, N.J., said yesterday. Sales at stores open at least a year gained 4.8 percent, up from 4.5 percent a year earlier and beating analysts’ estimates. The company also said that an independent board committee had begun a voluntary review of stock option grants and that it would report further on the review in its quarterly filing with the Securities and Exchange Commission by Oct. 5. More than 130 companies have disclosed internal or federal investigations into possible irregularities in the way they paid executives with options."""

multiple_keyphrases_response = """```json
{
  "key_phrases": [
    "sales",
    "bed bath & beyond incorporated",
    "company reports",
    "retail stores and trade"
  ]
}```"""

multiple_keyphrases_prompt = """You are an AI assistant tasked with extracting key phrases from a webpage. The said key phrases should represent what person who is interested in this text might be looking for. Webpage text is delimited with square brackets. 


To successfully complete the task, do the following in order. Do not move onto the next instruction without completing the previous one. Give the keywords in json only after completing all the other instructions:

1) Read your task and the webpage text carefully.
2) Summarize the text.
3) Think about what is contained in the text and what questions it answers.
4) Focus on the questions that are being answered in most of the text.
5) Based on those questions, come up with candidates for key phrases that text gives information about. 
6) Ensure the key phrases follow the guidelines provided below.
7) Select the final key phrases.
8) Output the key phrases in JSON format.

The guidelines phrases should follow are:

1) Provide the phrases in JSON format, with each key phrase being an item in a list. The list name is "key_phrases".
2) Use at most 10 key phrases. You can use less than that.
3) Key phrases should be quite short, about 1-3 words.
4) Ensure the key phrases are distinct from each other, avoiding synonyms or phrases with the same meaning.
5) The phrases are based on information that the text provides.
6) Prioritize the phrases that are present in the majority of the text over those that are present just in one part.
7) Start the json block with ```json and end it with ```.

The text from the webpage: <&>"""

def make_multi_extraction(text_to_extract_from: str) -> list:
    """
    Create a multi-extraction prompt using the provided text.
    Args:
        text_to_extract_from (str): The text to extract key phrases from.
    Returns:
        list: The prompt to be used for extraction.
    """
    parts = multiple_keyphrases_prompt.split('&')
    if len(parts) == 1:
        new_prompt = [{"role": "user", "content": "".join([parts[0], text_to_extract_from])}]
    elif len(parts) == 2:
        new_prompt = [{"role": "user", "content": "".join([parts[0], text_to_extract_from, parts[1]])}]
    elif len(parts) == 3:
        new_prompt = [{"role": "user", "content": "".join([parts[0], multiple_keyphrases_text, parts[1], multiple_keyphrases_response, parts[2], text_to_extract_from])}]
    else:
        new_prompt = [{"role": "user", "content": "".join([parts[0], multiple_keyphrases_text, parts[1], multiple_keyphrases_response, parts[2], text_to_extract_from, parts[3]])}]

    return new_prompt

search_phrase_examples = [
    "What is capital of France?",
    "Should I buy a car or a motorcycle?",
    "Who is the smartest person ever?"
]

search_phrase_labels = [ # Make sure to verify they are actually good. They might be bad as I labled them myself with no testing
   """```json
{
  "search_phrases": [
    "Paris",
    "capital of France",
  ]
}```""",
    """```json
{
  "search_phrases": [
    "car or motorcycle",
    "what to buy",
  ]
}```""",
    """```json
{
  "search_phrases": [
    "smartest person",
    "ever",
  ]
}```""",
]

search_phrase_prompt = f"""You are an AI who is an expert in extracting key phrases from the search query. I want to search webpages by key phrases. After that, person will type in the search query. You are to extract key phrases from the search query that will be compared with key phrases from the webpages. You are to provide the key phrases in JSON format.

Key phrases will be extracted from all webpages by an AI, using the following prompt delimited by '<' for start and '>' for end. 

<{make_multi_extraction("[webpage text would go here]")}>

To complete your task, follow the following instructions in order:

1) Read your task and the search query carefully.
2) Come up with potential content of texts user is looking for.
3) Using the prompt delimited by '<' and '>', come up with key phrases for those texts.
4) Key phrases should stay relevant to the original search query.
5) The key phrases should be different, do not have 2 phrases that have the same meaning.
6) If you can use less key phrases, do so. You should never use more than 7. 
7) However, make sure they capture all the important points of the search query and potential searched texts.
8) Present the key phrases in JSON format.

The search query is delimited by '[' for start and ']' for end.

[&]""" 

def make_search_prompt(searched_text: str) -> list:
    #Makes the prompt for finding search keyphrases from given text.
    
    parts = search_phrase_prompt.split('&')
    part_count = len(parts)
    
    new_prompt=""
    
    for i in range(0, (part_count - 1) // 2):
        new_prompt += parts[2 * i]
        new_prompt += search_phrase_examples[i]
        new_prompt += parts[2 * i + 1]
        new_prompt += search_phrase_labels[i]
        
    if part_count % 2 == 0:
        new_prompt += parts[-2]
        new_prompt += searched_text
        new_prompt += parts[-1]
    else:
        new_prompt += parts[-1]
        new_prompt += searched_text
        
    return [{"role": "user", "content": new_prompt}]


key_question_prompt = """You are an AI model specialized in extracting questions from text. You will be provided with a text and you need to come up with key questions that the text answers. I am making a program that will give relevant texts based on user's questions. User's questions will be compared against your own to find similarity, and if they are similar, that means the provided text is relevant to their question. So make sure to prioritize questions that are relevant to the majority of the text. Here is what I want you to do, follow those instructions in order:

1) The text is delimited by square brackets and is at the end of the prompt. Read the text carefully.
2) Come up with the summary of every few consecutive sentences.
3) Think about what the reader learns from reading those sentences.
4) Now think about larger blocks of sentences, made up of the smaller blocks you previously observed.
5) They give more insight as a larger block, what is the main information given in those bigger blocks? What questions are being answered? They should be concise and on point.
6) Now look at the questions, which of them are frequently discussed. Which ones are just briefly mentioned, without the text being about them?
7) Make sure your assessment is correct and that you ordered questions by their frequency and their relevance to the text.
8) We do not want to have too many questions. If you made more than 10 questions, keep only the 10 most relevant ones.
9) Write the list of your questions in JSON format.

The text: [&]
"""
def questions_from_webpage(page_text: str) -> List[str]:
    parts = multiple_keyphrases_prompt.split('&')

query_question_prompt = """

"""

