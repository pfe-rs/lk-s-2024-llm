import re
import requests

import numpy as np

from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urlparse, urljoin, urldefrag

class Webpage:
    # Class to store individual webpages

    @staticmethod
    def fetch_html(url: str) -> str:
        # Gives html code of url
        #print(url)
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def compare_domain(url, base_domain) -> bool:
        """
        Compares the domain of a URL with the base domain.
        """
        base_domain_len = len(base_domain.split('.'))
        
        parsed_url = urlparse(url)
        domain_parts = parsed_url.netloc.split('.')

        if len(domain_parts) < base_domain_len:
            return False

        url_domain = ".".join(domain_parts[-base_domain_len:])

        return url_domain == base_domain

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalizes the URL by removing the fragment and trailing slash.
        """
        url = urldefrag(url)[0]  # Remove the fragment
        if url.endswith('/'):
            url = url[:-1]
        return url
    
    @staticmethod
    def get_clean_content(html: str) -> str:
        # Parses the html in a way to make it easier for model to understand what is on the page


        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Define a list of tag names that often contain the main content
        content_tags = ['article', 'main', 'section', 'div']

        # Extract elements with these tags
        content = []
        for tag in content_tags:
            for element in soup.find_all(tag):
                # You may add conditions to filter elements by class, id, etc.
                if element.get('class') and 'content' in element.get('class'):
                    content.append(element)
                elif element.get('id') and 'content' in element.get('id'):
                    content.append(element)
                else:
                    # Add other conditions as necessary
                    if tag == 'div' and ('post' in element.get('class', []) or 'entry' in element.get('class', [])):
                        content.append(element)

        # Join the extracted elements' HTML
        main_content_html = ''.join(str(element) for element in content)

        # Optional: Clean with BeautifulSoup again
        clean_soup = BeautifulSoup(main_content_html, 'html.parser')

        # Remove unwanted tags or elements
        for unwanted in clean_soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
            unwanted.decompose()

        # Extract text
        clean_text = clean_soup.get_text(separator='\n')

        # Remove whitespaces
        clean_text = re.sub(r'\n+', '\n', clean_text)
        clean_text = re.sub(r' +', ' ', clean_text)
        return clean_text.strip()


    def __init__(self, link: str):
        self.link = link
        self.html = None
        self.embeddings = None

    def set_embedding(self, embedding: List[np.ndarray]) -> None:
        self.embeddings=embedding
    
    def get_text(self) -> str:
        # Returns text from webpage
        if self.html == None:
            self.html = Webpage.fetch_html(self.link)
        return Webpage.get_clean_content(self.html)

    def get_connects(self) -> List[str]:
        html = Webpage.fetch_html(self.link)
        self.html = html
        soup = BeautifulSoup(html, "html.parser")
        base_domain = urlparse(self.link).netloc

        connections = []

        links = soup.find_all('a')

        temp_link=self.link
        if temp_link[-1] != '/':
            temp_link += "/"

        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(temp_link, href)
                if Webpage.compare_domain(full_url, base_domain):
                    connections.append(full_url)
        
        if len(connections)==0:
            return []
        for i in range(len(connections)):
            connections[i] = Webpage.normalize_url(connections[i])
        connections.sort(key = lambda x: (len(x),x))

        result=[]
        result.append(connections[0])
        for i in range(1, len(connections)):
            if connections[i] != connections[i - 1]:
                result.append(connections[i])

        return result

