# prompts.py

import json

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

multiple_keyphrases_prompt = """You are an AI assistant tasked with extracting key phrases from a webpage. The key phrases will be used to search for webpages with some specific key phrase. Webpage text is delimited by '<' for start and '>' for end.

To successfully complete the task, do the following in order. Do not move onto the next instruction without completing the previous one. Give the keywords in JSON only after completing all the other instructions:

1) Read the text carefully.
2) Provide a short summary of the text.
3) Make sure that summary summarizes the entire text and no part is left out.
4) If some part is left out, write what is left out. After that, rewrite the summary.
5) Read the phrase guidelines carefully.
6) Utilizing the summary you wrote, find key phrases in the text.

The guidelines phrases should follow are:
1) Provide the phrases in JSON format, with each key phrase being an item in a list. The list name is "key_phrases".
2) Use at most 10 key phrases. You can use less than that.
3) Key phrases should be quite short, about 1-3 words.
4) Ensure the key phrases are distinct from each other, avoiding synonyms or phrases with the same meaning.
5) Select key phrases that are mentioned multiple times on the webpage, directly or through context. Avoid phrases that appear only once.
6) By reading phrases the reader should have a good idea of what the text is about, without reading a single word of it.
7) Start the JSON block with ```json and end it with ```.

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