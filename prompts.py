multiple_keyphrases_text = """Bed Bath & Beyond Gains Bed Bath & Beyond, the largest United States home furnishings retailer, posted higher second-quarter profit, helped by sales of back-to-college merchandise. Net income climbed 2.9 percent, to $145.5 million, or 51 cents a share, matching analyst estimates. Revenue in the three months that ended Aug. 26 increased 12 percent, to $1.61 billion, the company, based in Union, N.J., said yesterday. Sales at stores open at least a year gained 4.8 percent, up from 4.5 percent a year earlier and beating analysts’ estimates. The company also said that an independent board committee had begun a voluntary review of stock option grants and that it would report further on the review in its quarterly filing with the Securities and Exchange Commission by Oct. 5. More than 130 companies have disclosed internal or federal investigations into possible irregularities in the way they paid executives with options."""
    
multiple_keyphrases_response = """```json
{
  "key_phrases": [
    "sales",
    "bed bath & beyond incorporated",
    "company reports",
    "retail stores and trade"
  ]
}
````"""
    
multiple_keyphrases_prompt = """You are an AI assistant tasked with extracting key phrases from webpage. The key phrases will be used to search for webpage with some specific key phrase. Webpage text is delimited by '<' for start and '>' for end. 


To successfully complete the task, do the following in order. Do not move onto the next instruction without completing the previous one. Give the keywords in json only after completing all the other instructions:

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
5) Select key phrases that are mentioned multiple times on the webpage, directly or trough context. Avoid phrases that appear only once.
6) By reading phrases the reader should have a good idea what the text is about, without reading a single word of it.
7) Start the json block with ```json and end it with ```.

The text from the webpage: <&>
"""

def make_multi_extraction(text_to_extract_from):
    parts = multiple_keyphrases_prompt.split('&') 
    if len(parts)==1:
        new_prompt=[{"role": "user", "content": "".join([parts[0], text_to_extract_from])}]
    elif len(parts)==2:
        new_prompt=[{"role": "user", "content": "".join([parts[0], text_to_extract_from, parts[1]])}]
    elif len(parts)==3:
        new_prompt=[{"role": "user", "content": "".join([parts[0], multiple_keyphrases_text, parts[1], multiple_keyphrases_response, parts[2], text_to_extract_from])}]
    else:
        new_prompt=[{"role": "user", "content": "".join([parts[0], multiple_keyphrases_text, parts[1], multiple_keyphrases_response, parts[2], text_to_extract_from, parts[3]])}]

    return new_prompt