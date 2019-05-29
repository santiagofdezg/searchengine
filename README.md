# Search Engine

Project designed and implemented by **Santiago Fernández González**.

The aim of this project is implementing a search engine that works over texts. For this purpose I have used **Elasticsearch**, that is a search engine based on the Lucene library. It provides a distributed, multitenant-capable full-text search engine through RESTful APIs and JSON.

The source code is available in [GitHub](https://github.com/santiagofdezg).


## Information about implementation

The main module *search.py* contains three classes: 

- `Connection`: establish a connection with the Elasticsearch server. 
- `Index`: manage basic operations over an index, such as create and remove an index, add and delete documents from that index, etc.
- `Search`: send search requests to Elasticsearch. The requests can be filtered by several parameters: the category, the source and the publication date. 

This module also contains a script to create the index 'news'. If it is already created, it delete the old index (with all the data) and create a empty index.

The second module *crawl.py* contain the class `BBC`, which scrap the press articles from the [BBC website](https://www.bbc.com). The module contains a script to scrap the press articles and add them to the index.


## Instructions of use

The searchengine module can be run locally in a terminal. First of all it is necessary to run Elasticsearch. Then you have to create the index:
```bash
$ cd classificationWebsite/search/searchengine/searchengine/
$ python search.py
```

And now index some press articles:
```bash
$ python crawl
```

Now you can send search requests:
```python
$ python

>> from search import Connection, Search
>> es = Connection.get_connection()
>> search = Search(es, 'news')
>> articles = search.search_news(text="money investment", category="All", source="BBC", time_interval="month", max_articles=10)
```

The other option is using the **user interface** by running a Django local server. This can be done executing the following commands in the terminal:
```bash
$ cd classificationWebsite/
$ python manage.py runserver
```

Then the server is running in **localhost:8000**. You will need a **user** to use the application:

`user: test`

`password: d73he-9s1_`


## Acknowledgement
- [Borja González Seoane](https://github.com/GlezSeoane): for helping me to fix a bug related with the relative imports and adding a Conda manifest.

## License
MIT License