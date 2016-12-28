---
layout: post
title: "161209 - Haystack Django"
date: 2016-12-09 15:29:33
categories: django
---

# Guiding questions

1. What is the structure of Haystack?
2. What are the requirements of Haystack?
3. Use cases of Haystack?

# Ideas

* It is a portable interface, that can wraps around a search engine of choice (currently Haystack supports Solr, Elasticsearch, Whoosh, Xapian..).
* The idea is to write a single search interface, and you can freely use that interface to use any supported search engine.

# Structure

### SearchIndex

* Similar to Django Models.
* Determines what data should be placed in the search index. The search engine will only search for text that stored inside search index.
* Generally, a SearchIndex should be created for each type of Model to index.
* It will (optionally, but recommended) need a search index template in order to combine all the searchable model fields into index.
* The `SearchIndex` should be stored in a `search_indexes.py` file within the app that it applies to, so that Haystack can automatically pick it up
* To put the data from `Model` to `SearchIndex`, just run `python manage.py rebuild_index`

### SearchView

* Haystack is a reusable app just like any other application you create in your project.
* It requires you to hook a url pattern for search, which will calls Haystack URLconf. Example: `(r'^search/', include('haystack.urls')),`
* You should also create a search template for the search result page.

### Interaction:

User hits a query -> URLconf -> Invoke `SearchView` -> `earchView` is a subclass of Django's `FormView` -> `SearchForm` is called -> make a query with `SearchQuerySet` -> the search backend will handle search query from `SearchIndex` -> returns the result to `SearchView`.

# Answer questions

1. What is the structure of Haystack?
    
    * Haystack can be considered as a 3rd-party application.
    * Follows the same Model (actually in this case Index) / View / Template architecture.
    * Refer to the interaction refered above to see how it responds to user query

2. What are the requirements of Haystack?

    * It requires a backend search engine. Haystack does not actually do the searching, it is just a wrapper interface to the search engine
    * At the bare minimum, you need to create a indexed text corpus that the Haystack can direct the search engine to search into; and you need to specify a search URL

3. Use cases of Haystack?

    * Search
    * Autocomplete
    * Faceting

# Reference:
http://django-haystack.readthedocs.io/en/v2.5.1/index.html