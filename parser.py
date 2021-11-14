import os
import urllib.request
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
from markdownify import markdownify as md
import textwrap

from db import News


def parse_lists_of_paragraphs_to_markdown(paragraphs):
    result = ""
    for p in paragraphs:
        p = str(p).replace("//cloud", "https://cloud")
        result += md(p)
    return result.strip()


class EdupageNewsParser:

    def __init__(self, webhook_url, website_url, database):
        self.webhook_url = webhook_url
        self.website_url = website_url
        self.webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        self.database = database

    def get_formatted_page(self):
        page = requests.get(self.website_url)

        return BeautifulSoup(page.content, "html.parser")

    def send_news(self, li_tag):
        id = li_tag['id'].split("-")[-1]

        news_in_db = self.database.get_news_by_id(id)
        if news_in_db is not None:
            return

        print("Printing " + id)
        heading = li_tag.find('h4', {'class': 'skgd skgdli-news_ListItem_1-news_DFHeading_1'})
        heading_text = heading.text.strip()
        text = parse_lists_of_paragraphs_to_markdown(
            li_tag.find('div', {'class': 'erte-text-inner'}).find_all('p'))
        img_url = "https://gamtt.edupage.org" + \
                  li_tag.find('img', {'class': 'skgd skgdli-news_ListItem_1-news_DFImage_1'})['src']
        additional_imgs = [div.find('img')['src'].replace("//cloud", "https://cloud") for div in
                           li_tag.find_all('div', {'class': 'erte-photos-item-inner'})]

        wrapped_content = textwrap.wrap(text, 4096)

        for (index, wrap) in enumerate(wrapped_content):
            embed = DiscordEmbed(title=heading_text, url="https://gamtt.edupage.org/news/#news-" + id)
            embed.set_thumbnail(url=img_url)
            embed.set_description(wrap)
            embed.set_footer(text=id)
            embed.set_timestamp()

            self.webhook.add_embed(embed)

        self.webhook.execute()

        files = []

        for (index, additional_img) in enumerate(additional_imgs):
            file_name = str(index) + ".jpg"
            urllib.request.urlretrieve(additional_img, file_name)

            with open(file_name, "rb") as file:
                files.append(file_name)
                self.webhook.add_file(file=file.read(), filename=file_name)

        self.webhook.remove_embeds()
        self.webhook.execute()

        self.webhook.remove_files()

        for file in files:
            if os.path.exists(file):
                os.remove(file)

        for session in self.database.create_session():
            session.add(News(id=id,
                             sent=True,
                             title=heading_text,
                             description=text))

            session.commit()

    def get_all_news(self):
        page = self.get_formatted_page()

        for ul_tag in page.find_all('ul', {'id': 'news_News_1'}):
            for li_tag in ul_tag.find_all('li',
                                          {'class': 'skgd skgdli-news_ListItem_1-news_ListItem_1 composite skgdLi'}):
                self.send_news(li_tag)
