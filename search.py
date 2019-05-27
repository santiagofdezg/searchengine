# -*- coding: utf-8 -*-

"""
This module contains the class which makes search requests to Elasticsearch

Author: Santiago Fernández González

License: MIT
"""

from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl import Search as S, A, Q, Document


class Connection:
    """
    Return a connection with the Elasticsearch host
    """

    @staticmethod
    def get_connection():
        """
        Return a Elasticsearch instance
        """
        return Elasticsearch([{'host': 'localhost', 'port': 9200}])


class Index:
    """
    Manage basic operations over an index, such as create and remove an index,
    add and delete documents from that index, etc.
    """
    name = None
    __es = None
    settings = None

    @staticmethod
    def create(connection, index_name, body=None):
        """
        Create a new index and return an instance to manage it. If it is
        already created, return None
        """
        try:
            instance = Index()
            instance.name = index_name
            instance.__es = connection
            if body is None:
                connection.indices.create(index=index_name)
            else:
                connection.indices.create(index=index_name, body=body)
                instance.settings = body
            return instance

        except TransportError:
            # There is already an index with that name
            return None

    def delete(self):
        self.__es.indices.delete(self.name)

    def index_doc(self, body):
        self.__es.index(index=self.name, body=body)

    def get_doc(self, id):
        return self.__es.get(index=self.name, id=id)

    def delete_doc(self, id):
        self.__es.delete(index=self.name, id=id)


class Search:
    """
    Class to send search requests to Elasticsearch
    """
    __es = None
    __index = None

    def __init__(self, connection, index_name):
        self.__es = connection
        self.__index = index_name

    def get_all_categories(self):
        # Create the request
        s = S(using=self.__es, index=self.__index)
        s.aggs.bucket('categories', 'terms', field='category')
        response = s.execute()

        # Get a sorted list
        l = response.aggregations.categories.buckets
        categories = [cat['key'] for cat in l]
        categories.sort()

        return categories

    def get_all_sources(self):
        # Create the request
        s = S(using=self.__es, index=self.__index)
        s.aggs.bucket('sources', 'terms', field='source')
        response = s.execute()

        # Get a sorted list
        l = response.aggregations.sources.buckets
        sources = [source['key'] for source in l]
        sources.sort()

        return sources

    def search_news(self, text, category, source, time_interval,
                    max_articles):
        intervals = {
            'today': 'now/d', 'week': 'now/w', 'month': 'now/M',
            '3months': 'now-2M/M', 'year': 'now/y'
        }
        s = S(using=self.__es, index=self.__index)
        if category != "All":
            # Search in a specific category
            s = s.query("bool", must=Q("match", category=category))

        # Search in the title, subtitle and in the body of the article
        s = s.query("bool", should=Q("multi_match", query=text,
                                     fields=[
                                         'title', 'subtitle', 'article']))
        if source != "All":
            # Only articles of a specific source
            s = s.filter("term", source=source)

        # Only articles in this range of time
        s = s.filter({"range": {"date": {"gte": intervals[time_interval],
                                         "lte": "now"}}})
        # Limit the number of results
        s = s[0:int(max_articles)]
        response = s.execute()

        # + FIX THIS!! (but it looks that the response already exclude the
        # documents with score==0)
        # Return only documents with score > 0
        return response.hits

    def search_by_id(self, id):
        return Document.get(id, self.__es, self.__index)


if __name__ == '__main__':
    es = Connection.get_connection()
    s = Search(es, 'news')
    categories = s.get_all_categories()
    sources = s.get_all_sources()
    print(categories)
    print(sources)
