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
        soup = BeautifulSoup(self.html, "html.parser")
        text = soup.get_text()
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

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

