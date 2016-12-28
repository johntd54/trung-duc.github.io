---
layout: post
title: "161223 - DJANGO REST Framework"
date: 2016-12-23 10:32:59
categories: django
---

---
Main idea: the REST framework provides helpers for server to provide API service.

Model (Django's built-in models): this is the place where you store data

Serializer (REST framework): serialize the data from Model into json. Make sense since usually in API server communicates with clients not in HTML but in json

Viewsets (REST framework, like Django's built-in view): this is REST framework's pre-defined views (so more than likely, you don't have to write your own views using Django's class-based views to handle delivering the result back to client)

Routers (REST framework, like Django's urls): routers is a helper is included inside urlpatterns that disects the client's requested url to call the correct views

Settings: REST framwork's specific settings.

---
## Serializer:

Data object (such as model) (4)<----->(1) Serializer (3)<----->(2) JSON

(1) Take an object, serialize that object into Python native datatype. Example: `serializer = Serializer(object)` -> then 'serializer' is the native datatype.
(2) Native datatype can be written out into bytestrings to export to JSON with `rest_framework`.renderers.JSONRenderer`. Example: `json = JSONRenderer().render(serializer.data)`.
(3) Take a JSON, deserialize that JSON into Python native datatype. At the same time check if it's valid. This can be done with `JSONParser().parse()`. Example: `data = JSONParser().parse(json); serializer = Serializer(data=data)`.
(4) The native data can be used to create an instance of the original class with `.save()`. Example: `serialize.save()` will usually save the instance and return back the instance's reference.

This is handy in that it can serialize nested object

>Question: how does serializer (especially ModelSerializer) populate data from ManyToManyFields?

>Answer: there are 2 ways:
    
>    - use PrimaryKeyRelatedField: this field will list out the *primary keys* of related objects
>    - use Serializer for related objects, and add that Serializer as a Field: this will list out any *keys/combination of keys* of related objects

Serializer must either has a `fields` or `exclude` attribute in `.Meta` class. To include all fields, use `fields = '__all__'`

---
## Views

Since the content-type is automatically inferred from request, the API will return JSON in browser-friendly presentation if the request is made by browser.


---
Flow:

1. Create model
2. Create serializers
3. Create view
    3.1. return DRF's Response object
    3.2. use class-based views (APIView)
    3.3. class-based views allow the use of mixins
    3.4. use DFR's own generic class-based views
    3.5. combine related views into viewset
    3.6. binding viewset to urls with `Router` class
4. Add url
    4.1. (optionally) add optional format suffixes to URLs
5. Add authentication and permissions to use API


---
Environment variables can be set/unset depending on Conda environments (for Unix):
- `${ENV_PATH}/etc/conda/activate.d/env_vars.sh`
- `${ENV_PATH}/etc/conda/deactivate.d/env_vars.sh`

The `env_vars.sh` of activate should look like:

{% highlight bash %}
#!/bin/sh

export KEY1="something"
export KEY2="something else"
{% endhighlight %}


The `env_vars.sh` of deactivate should look like
{% highlight bash %}
#!/bin/sh

unset KEY1
unset KEY2
{% endhighlight %}

---


