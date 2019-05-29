# Search Engine

Project designed and implemented by **Santiago Fernández González**.

The aim of this project is implementing a search engine that works over texts. For this purpose I have used **Elasticsearch**, that is a search engine based on the Lucene library. It provides a distributed, multitenant-capable full-text search engine through RESTful APIs and JSON.


## Information about implementation

The main module *search.py* contains three classes: 
-`Connection`: establish a connection with the Elasticsearch server. 
-`Index`: manage basic operations over an index, such as create and remove an index, add and delete documents from that index, etc.
-`Search`: send search requests to Elasticsearch. The requests can be filtered by several parameters: the category, the source and the publication date. 

This module also contains a script to create the index 'news'. If it is already created, it delete the old index (with all the data) and create a empty index.

The second module *crawl.py* contain the class `BBC`, which scrap the press articles from the [BBC website](https://www.bbc.com). The module contains a script to scrap the press articles and add them to the index.


## Acknowledgement
- [Borja González Seoane](https://github.com/GlezSeoane): for helping me to fix a bug related with the relative imports and adding a Conda manifest.