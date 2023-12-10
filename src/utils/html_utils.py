import requests
from bs4 import BeautifulSoup

class HTMLUtils:
    def __init__(self, url):
        self._url = url

    @property
    def _url(self):
        return self._url

    @_url.setter
    def _url(self, value):
        self._url = value

    def get_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTML: {e}")
            return None

    def extract_data_list(self, html, selectors):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            data = []
            for selector in selectors:
                data.append(soup.select(selector))
            return data
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None