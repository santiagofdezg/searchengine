# -*- coding: utf-8 -*-

"""
This module contains the classes which crawl the data from the news websites.
For this purpose it is used BeautifulSoup.

Author: Santiago Fernández González

License: MIT
"""

import requests
from bs4 import BeautifulSoup

class BBC:
    url = "https://www.bbc.com"
    main_categories = {
        # 'World': "https://www.bbc.com/news/world",
        # 'UK': "https://www.bbc.com/news/uk",
        'Business': "https://www.bbc.com/news/business",
        'Technology': "https://www.bbc.com/news/technology",
        'Science & Environment':
            "https://www.bbc.com/news/science_and_environment",
        # 'Stories': "https://www.bbc.com/news/stories",
        'Entertainment & Arts': "https://www.bbc.com/news/entertainment_and_arts",
        # 'Health': "https://www.bbc.com/news/health"
    }

    @staticmethod
    def get_articles(max_articles):
        pass

    @staticmethod
    def _article_data(url, category):
        pass


if __name__ == '__main__':
    result = requests.get("https://www.bbc.com/news/technology")

    print(result.status_code) # If 200 => OK

    # We can also check the HTTP header of the website to
    # verify that we have indeed accessed the correct page:
    print(result.headers)

    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    # Obtain all the articles

    print(soup.find_all("div", class_="gs-c-promo", limit=10))
    # Equivalent to:
    print(soup("div", class_="gs-c-promo", limit=10))

    url = "https://www.bbc.com"
    all = soup("div", class_="gs-c-promo", limit=4)
    # BUG: There is some problem and the articles are repeated
    for e in all:
        title = e.find("h3", class_="gs-c-promo-heading__title").contents[0]
        print(title)
        link = url + e.find("a", class_="gs-c-promo-heading")['href']
        print(link)
        subtitle = e.find("p", class_="gs-c-promo-summary").contents[0]
        print(subtitle)
        category = e.find("a", class_="gs-c-section-link").span.contents[0]
        print(category)
