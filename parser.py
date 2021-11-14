import requests
from bs4 import BeautifulSoup


class EdupageNewsParser:

    def __init__(self, webhook_url, website_url):
        self.webhook_url = webhook_url
        self.website_url = website_url

    def get_formatted_page(self):
        page = requests.get(self.website_url)

        return BeautifulSoup(page.content, "html.parser")

