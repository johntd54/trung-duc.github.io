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

User hits a query -> URLconf -> Invoke `SearchView` -> `SearchView` is a subclass of Django's `FormView` -> `SearchForm` is called -> make a query with `SearchQuerySet` -> the search backend will handle search query from `SearchIndex` -> returns the result to `SearchView`.

# Answer questions

1. What is the structure of Haystack?
    
    * Haystack can be considered as a 3rd-party application.
    * Follows the same Model (actually in this case Index) / View / Template architecture.
    * Refer to the interaction refered above to see how it responds to user query

2. What are the requirements of Haystack?

    * It requires a backend search engine. Haystack does not actually do the searching, it is just a wrapper interface to the search engine
    * At the bare minimum, you need to create an indexed text corpus that the Haystack can direct the search engine to search into; and you need to specify a search URL

3. Use cases of Haystack?

    * Search
    * Autocomplete
    * Faceting

# Documenting how I set up Haystack and Solr, and make them work with each other

1. Install Solr, and run Solr server

> http://django-haystack.readthedocs.io/en/v2.5.1/installing_search_engines.html
> I did not run server with `java -jar start.jar`. There isn't any `start.jar` file in `example`. The documented Solr version is 4.10.2, mine is 6.3.0, so there is a high chance that they change the way to start up Solr. Instead I ran Solr server with `bin/solr start`. Not sure whether running this way affects Haystack, but accessing http://127.0.0.1:8983/solr does return Solr server interface.
> From the link above, I ran `./manage.py build_solr_schema` but it raises error regarding lxml. `Reason: Incompatible library version: etree.cpython-35m-darwin.so requires version 12.0.0 or later, but libxml2.2.dylib provides version 10.0.0`. OK so the reason for this is when lxml is installed, it is configured with Anaconda's newer version of libxml2.2.dylib. However, when in use, lxml imports more outdated systemwide libxml2. Fix this by install libxml2 with Homebrew, and force that Homebrew's libxml2 to be a default systemwide version with `brew link libxml2 --force`

2. Run the command `./manage.py build_solr_schema` above, and copy that output to `templates/search_configuration/solr.xml`. Might need to do this again when I configure Haystack.
3. Install Haystack: `pip install django-haystack`
4. Set up Haystack in Django's setting
    
{% highlight python %}
INSTALLED_APPS += ("haystack",)
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
{% endhighlight %}

5. Subclass `haystack.indexes.SearchIndex` and `haystack.indexes.Indexable` inside `search_indexes.py`. This file is put inside application folder.
6. Create `search/indexes/myapp/note_text.txt` inside project templates directory
7. Add `url(r'^search/', include('haystack.urls'))` inside `urls.py`
8. Create search template `${TEMPLATE_DIR}/search/search.html`
9. Redo step 2. It should be noted that Solr6 does not have conf/schema.xml, so I used this method:
> `build_solr_schema` uses a template to generate `schema.xml`. Haystack provides a default template using some sensible defaults. If you would like to provide your own template, you will need to place it in `search_configuration/solr.xml`, inside a directory specified by your app’s `TEMPLATE_DIRS` setting.
10. Restart Solr with `bin/solr restart`
11. Run `./manage.py rebuild_index`. Errors thrown: `Failed to clear Solr index: Solr responded with an error (HTTP 404): [Reason: Error 404 Not Found]`. Possibly because no core is created. Run `bin/solr create_core -c default -p 8983`. Get this response: `{"responseHeader":{"status":0,"QTime":3496},"core":"default"}. Change HAYSTACK_CONNECTIONS to 

{% highlight python %}
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/default'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
{% endhighlight %}

12. Run some simple searches. Failed with `'list' object has no attribute 'split'`. Probably because of schema misconfiguration. Ok so after a while, the problem does come from schema misconfiguration. Schema generated from Haystack is for previous versions of Solr (probably version <5), so some of the fields in that schema file are deprecated. I fixed the problem by adding the following fields into Solr's, not Haystack's (it is outdated) default schema (probably `[solr dir]/server/solr/[core]/conf/managed-schema`), and then rename `managed-schema` to `schema.txt`. If you use this method, you should make a copy of `managed-schema` in case anything goes wrong. Also, [this](https://github.com/dekanayake/haystack_solr6) seems to help (I followed and failed at the very last command - curl. And then I made the fields changes mentioned above and all is well).

{% highlight xml %}
<field name="id" type="string" indexed="true" stored="true" multiValued="false" required="true"/>
<field name="django_ct" type="string" indexed="true" stored="true" multiValued="false"/>
<field name="django_id" type="string" indexed="true" stored="true" multiValued="false"/>
<field name="_version_" type="long" indexed="true" stored ="true"/>
{% endhighlight %}

OK so the above are basic steps to set Haystack and Solr up and running, though apparently the default search is stupid. A document can be matched against a query even though it contains a only single word from that query. It seems to fix this behavior I will have to modify `SearchQuerySet`. So it is because of SearchQuerySet.auto_query(string), which makes use of flawed `haystack.inputs.AutoQuery`. It returns everything. Just use filter()

## Customize search query result

Haystack uses `SearchQuerySet` object to (1) construct the query to fetch result from indexes, and (2) post-process the search result given back from indexes.

`SearchQuerySet` is currently implemented with these methods to help construct query:

- `.all()`: copy all results
- `.none()`: return an empty result
- `.exclude(*args, **kwargs)`: remove results that contain any of the words in *args, **kwargs
- `.filter(*args, **kwargs)`: filter (either using `.filter_and` or `.filter_or`)
- `.filter_and(*args, **kwargs)`: return only results that match all of the words in querystring
- `.filter_or(*args, **kwargs)`: return results that match at least 1 word in querystring
- `.order_by(*args, **kwargs)`: alter the result order
- `.highlight(**kwargs)`: add highlight to the result
- `.boost(term, boost)`: boost certain keywords in the query string
- `.facet(field, **options)`: add faceting to a query
- `.raw_search(query_string, **kwargs)`: perform raw search directly into the index

So to avoid the dreaded default result returned by Haystack, just call .filter_and(..) method, rather than .auto_query(..) method. Or if I need fancier search query, I can subclass `SearchQuerySet` and construct my own search rule.

## Make the search form looks better

- Haystack's `SearchForm` is a subclass of `django.forms.Form`. Haystack's `ModelSearchForm` is a subclass of its own `SearchForm`


## Commands

- `clear_index`: remove the search indexes
- `update_index`: refresh the entries inside indexes
- `rebuild_index`: the combination of `clear_index` then `update_index`
- `build_solr_schema`: once all of the `SearchIndex` classes are in place, this command can be used to generate XML schema Solr needs to handle the search data
- `haystack_info`: get basic information about your Haystack

For details on options and arugments, refer [here](http://django-haystack.readthedocs.io/en/v2.5.1/management_commands.html)



# Reference:
http://django-haystack.readthedocs.io/en/v2.5.1/index.html