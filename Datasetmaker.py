from webpage import Webpage
from random import randint

page_links=[
    """https://pfe.rs/en/""", # 0
    """https://pfe.rs/en/team/""",
    """https://pfe.rs/en/fields/""",
    """http://www.matf.bg.ac.rs/eng/""",
    """https://www.reddit.com/r/SQL/comments/y5emys/databases_is_so_boring/?rdt=43642""", # 4
    """https://www.mathsisfun.com/geometry/hyperbola.html""",
    """https://math.naboj.org/gb/en/""",
    """https://www.petfinder.com/cats-and-kittens/adoption/new-cat/first-30-days/""",
    """https://codeforces.com/blog/entry/61780""",
    """https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratic-functions-equations/x2f8bb11595b61c86:quadratic-formula-a1/a/quadratic-formula-explained-article""", #9
    """https://en.wikipedia.org/wiki/Miss_Meyers""",
    """https://cp-algorithms.com/dynamic_programming/intro-to-dp.html""",
    """https://mathsbeyondlimits.eu/mbl/overview/""",
    """https://rubiks-cube-solver.com/how-to-solve/""",
    """https://www.livescience.com/how-many-times-can-paper-be-folded""", # 14
    """https://www.guinnessworldrecords.com/news/2023/6/max-park-makes-history-by-solving-cube-in-fastest-time-ever-752905""",
    """https://www.quora.com/What-will-happen-if-I-drink-only-water-and-not-other-beverages-for-three-months""",
    """https://www.quora.com/Accidentally-sipped-expired-juice-will-I-be-okay""",
    """https://www.42madrid.com/en/latest-news/the-meaning-of-life-the-universe-and-everything-else-the-answer-is-42/""",
    """https://www.delve.com/insights/how-many-people-does-it-take-to-turn-on-a-lightbulb""" # 19
]

def is_file_empty_or_whitespace(file_path):
    #Determines if file is empty
    with open(file_path, 'r', encoding="utf-8") as file:
        contents = file.read()
        # Strip any leading and trailing whitespace characters
        stripped_contents = contents.strip()
        # Check if the stripped content is empty
        return len(stripped_contents) == 0


for count in range(0,len(page_links)):
    # Go over all the links and extract pages
    file = "Dataset/"+f"Sample{count}_text.txt"
    if not is_file_empty_or_whitespace(file):
        continue
    
    link=page_links[count]
    print(link)
    page = Webpage(link)
    text=page.get_text()
    print(len(text))
    with open(file, 'w', encoding="utf-8") as f:
        print(text,file=f) 