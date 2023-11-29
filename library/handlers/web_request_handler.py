import requests
from bs4 import BeautifulSoup

class WebRequestHandler:
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

    def extract_data(self, html, selector):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.select(selector)
            return data
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None

# 使用範例
url = 'https://example.com'
web_extractor = WebRequestHandler(url)

html_content = web_extractor.get_html()
if html_content:
    selector = 'your-css-selector'  # 替換成你想要的 CSS 選擇器
    extracted_data = web_extractor.extract_data(html_content, selector)

    if extracted_data:
        print("Extracted Data:")
        for item in extracted_data:
            print(item.text)
    else:
        print("No data extracted.")
else:
    print("Failed to fetch HTML.")