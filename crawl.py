# -*- coding: utf-8 -*-

"""
This module contains the classes which crawl the data from the news websites.
For this purpose it is used BeautifulSoup.

Author: Santiago Fernández González

License: MIT
"""

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from datetime import datetime

from .search import Index, Connection

class BBC:
    url = "https://www.bbc.com"
    main_categories = {
        'Business': "https://www.bbc.com/news/business",
        'Technology': "https://www.bbc.com/news/technology",
        'Science & Environment':
            "https://www.bbc.com/news/science_and_environment",
        'Entertainment & Arts': "https://www.bbc.com/news/entertainment_and_arts",
    }

    @staticmethod
    def get_articles():
        article_list = []
        # ++++
        errors = 0
        # ++++
        for c in BBC.main_categories.values():
            page = requests.get(c)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'lxml')
                container_articles = soup.find("div", id="index-page")
                all = container_articles.find_all("div", class_="gs-c-promo")
                for article in all:
                    try:
                        known_data = {}
                        link = BBC.url + article.find("a", class_="gs-c-promo-heading")['href']
                        known_data['category'] = article.find("a", class_="gs-c-section-link").span.contents[0]
                        known_data['title'] = article.find("h3", class_="gs-c-promo-heading__title").contents[0]
                        known_data['subtitle'] = article.find("p", class_="gs-c-promo-summary").contents[0]
                        known_data['source'] = "BBC"
                        data = BBC._article_data(link, known_data)
                        article_list.append(data)
                    except:
                        errors += 1

        return article_list

    @staticmethod
    def _article_data(url, known_data):
        data = known_data
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        body = soup.find("div", class_="story-body")
        data['author'] = BBC._find_author(body)
        data['date'] = BBC._find_date(body)
        data['article'] = BBC._find_text(body)
        return data

    @staticmethod
    def _find_author(article_body):
        l = article_body.find_all("span", class_="byline__name")
        if len(l):
            author = l[0].contents[0].replace('By ','')
        else:
            # Author not found => Unknown
            author = "Unknown"
        return author

    @staticmethod
    def _find_date(article_body):
        date = article_body.find("div", class_="date")['data-datetime']
        # Modify the format of the date
        mod_date = datetime.strptime(date, '%d %b %Y').strftime("%d-%m-%Y")
        return mod_date

    @staticmethod
    def _find_text(article_body):
        container = article_body.find("div",class_="story-body__inner")
        p_list = container.find_all("p")
        text = ''
        for p in p_list:
            # TODO: Fix the way to crawl the text of the article. It works
            #  wrong when there are <a> links within the text
            if p.contents[0].__class__ == NavigableString:
                text = text + "\n\n" + p.contents[0]
        return text


if __name__ == '__main__':
    """
    Script to index press articles
    """

    es = Connection.get_connection()
    i = Index(es, 'news')

    # Scrap the articles from the BBC
    articles = BBC.get_articles()

    for a in articles:
        i.index_doc(a)

    # TODO: improve the indexing of documents to avoid adding repeated
    #  documents

