# -*- coding: utf-8 -*-

"""
This module contains the class which makes the queries to Elasticsearch

Author: Santiago Fernández González

License: MIT
"""

from elasticsearch import Elasticsearch, TransportError
from elasticsearch_dsl import Search, A


class Connection:
    """
    Return a connection with the Elasticsearch host
    """

    @staticmethod
    def get_connection():
        # Return a Elasticsearch instance
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
        # If it's already created => return None
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
            return None

    def delete(self):
        self.__es.indices.delete(self.name)

    def index_doc(self, body):
        self.__es.index(index=self.name, body=body)

    def get_doc(self, id):
        return self.__es.get(index=self.name, id=id)

    def delete_doc(self, id):
        self.__es.delete(index=self.name, id=id)


class Query:
    connection = None

    def __init__(self, connection):
        pass

    def get_all_categories(self):
        pass

    def get_all_sources(self):
        pass

    def search(self):
        pass
