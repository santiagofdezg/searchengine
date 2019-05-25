# -*- coding: utf-8 -*-

"""
This module contains the class which makes the queries to Elasticsearch

Author: Santiago Fernández González

License: MIT
"""


class Connection:

    @staticmethod
    def get_connection():
        # Return a Elasticsearch instance
        pass


class Index:

    def create(self):
        # If it's already created => don't throw exception
        # Return 0 or 1
        pass

    def remove(self):
        # Return 0 or 1
        pass


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
