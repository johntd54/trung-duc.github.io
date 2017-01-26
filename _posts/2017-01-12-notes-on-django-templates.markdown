---
layout: post
title: "170112 - Notes on Django Templates"
date: 2017-01-12 18:31:48
categories: django
---

# Executing custom template tags and filters inside TextField 

## Toy problem:

I create a blog with Django, and I use a Django model's TextField to store the content of each blog post in the database. In the blog posts, I might want to include some images, but since manually writing `<img src="..." style="..." class="..." />` for each image is too clunkie and error-prone (especially for non-technical people - my mom), I would want a simpler way to insert images. One way to do that is to create a custom Django's template tag, that automatically render image url to `<img.../>`, e.g `{% raw %}{% make_image http://domain.com/img1.jpg left %}{% endraw %}` -> `<img src="http://domain.com/img1.jpg" class="left" />`

## Key reasons on why it is possible:
    
- Any string object can be considered as a template -> so the model's TextFields can also be rendered as a template
- Django provides the ability to create custom tags and filters -> so we can create the `make_image` tag of our own to perform the conversion

## Each components

### Custom template tags

1. Create a directory to store your tags. By default, this directory should be named `templatetags`, and located inside one of the registered apps in `settings.INSTALLED_APPS`. Also create an `__init__.py` inside that `templatetags`, so that Python can import anything inside `templatetags` as a module.
2. Create a Python file (in this example I would name it `extra_html.py`). The name of that Python file will be the name of the template modules (to load this module, just use `{% raw %}{% load extra_html %}{% endraw %}` inside your template file). It's important to name that file distinctly to avoid clash with other installed template tags/filters module of the same name. For example, if you have 2 apps, each with the following structure (respectively): `app1/templatetags/abc.py` and `app2/templatetags/abc.py`, then when you call `{% raw %}{% load abc %}{% endraw %}`, Django will get confused on which `abc` module you want to load. Also keep in mind to avoid naming conflicts with template modules of 3rd party app you use in your project.
3. Create `make_image` tag. As of version 1.10, the Django template system runs in 2 steps:
    a. compiling: parse the template to find any instance of `{% raw %}{% ... %}{% endraw %}` and `{% raw %}{{ ... }}{% endraw %}`, and
    b. rendering: compute and render the result of those `{% raw %}{% ... %}{% endraw %}`, `{% raw %}{{ ... }}{% endraw %}` instances.
4. Compile code:

    {% highlight python %}
    from django import template
    from django.utils.html import format_html

    register = template.Library()

    @register.tag 
    def make_image(parser, token):
        try:
            tag_name, url, location = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                    "{} tag requires 2 arguments: url and "
                    "location".format(token.contents.split()[0]))

        return MakeImage(url, location)

    {% endhighlight %}

- `register` helps Django template system to find custom template tags and filters (it is used right below with decorator `@register.tag` to register `make_image` -> so that you can use and Django can recognize `{% raw %}{% make_image ... %}{% endraw %}` in your Django templates)
- `make_image` takes 2 arguments: the first one is the parser that parses your template, and the second one is a string right after `{% raw %}{%  {% endraw %}` and before ` {% raw %}%}{% endraw %}`.
- `.split_contents()` will split the string from spaces, e.g `"make_image http://domain.com/image1 middle"` -> `["make_image", "http://domain.com/image1", "middle"]`
- `MakeImage` is a rendering class (will be shown later), that takes the url and the location to render into appropriate html tag
5. Render code:

    {% highlight python %}
    class MakeImage(template.Node):

        def __init__(self, url, location):
            """
            Initialize information needed to create image
            """
            self.url = url
            self.location = location

        def render(self, context):
            """
            Given a template node initialized with the above information, return
            a representation.
            """
            element = '<img src="{}" class="image_{}">'
            return format_html(element, self.url, self.location)
    {% endhighlight %}

- `template.Node`: all compiled/found Django template tags (`{% raw %}{% ... %}{% endraw %}`) will be rendered as an instance of `template.Node`
- `render(self, context)`: this function will be called by the Django template system to render tags.

6. Put the tag inside your TextField: suppose you want to include image in your blog post, instead of writing the full HTML img tag, you can just write `{% raw %}{% make_image http://example.com/image1 center %}{% endraw %}` in your TextField and you will get `<img src="http://example.com/image1" class="image_center" />` when your TextField is rendered. But... it does not work yet, as you have to make Django render your TextField as if it is a template (so that it can compile and render `{% raw %}{% make_image ... %}{% endraw %}`, otherwise this code will show up in your blog and no image appears)

### String/text object as a template

1. Objective: we will create another custom tag to evaluate the TextField as template. We will call this custom tag `render`. So: `\{\% render object.textfield \%\}` will render `object.textfield` as a template, hence can compile and render `make_image` tag inside it.
2. In the same Python file above, add:

    {% highlight python %}
    class RenderTextField(template.Node):
        def __init__(self, variable):
            self.variable = template.Variable(variable)

        def render(self, context):
            try:
                content = self.variable.resolve(context)
                t = template.Template(
                        "{}{}".format("{% raw %}{% load extra_html %}{% endraw %}", content))
                return t.render(context)
            except (template.VariableDoesNotExist, template.TemplateSyntaxError):
                return "Cannot load", self.variable

    @register.tag
    def render(parser, token):
        try:
            tag_name, variable = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                        "{} tag requires a single argument, which is a block of "
                        "string".format(token.contents.split()[0]))
        return RenderTextField(variable)
    {% endhighlight %}

- structurally, it looks the same as `make_image` tag: we will have `render` as a custom template tag, that Django can compile whenever it finds `\{\% render ... \%\}`, and Django will render the tag with `RenderTextField.render(context)`
- `split_contents`: after split_contents, we will get ["render", "object.textfield"]
- `template.Variable`: since we want to treat object.textfield as a variable, and not a simple text "object.textfield", we will need to wrap it inside `template.Variable`
- `content = self.variable.resolve(context)`: Django takes the context to get the value of `object.textfield`. Here, `content` will be a string that is a value of `object.textfield`
- `t = template.Template("{}{}".format("{% raw %}{% load extra_html %}{% endraw %}", content))`: the string "{% raw %}{% load extra_html %}{% endraw %}....." will be rendered as a template. We will need the "{% raw %}{% load extra_html %}{% endraw %}" appear before the string our object.textfield value, so that the `make_image` tag inside it can be recognized by the Django template system

3. Put everything inside your template, example:

    {% highlight html %}
    {% raw %}{% load extra_html %}{% endraw %}
    <html>
      <body>
        <div id="title">object.title</div>
        <div id="content">{% raw %}{% render object.textfield %}{% endraw %}</div>
      </body>
    </html>
    {% endhighlight %}

## Performance and security concern

This is a simple example of using custom tags and filters. However, keep in mind that:
    - you would want to autoescape the string object (e.g. TextField, CharField,...), especially when they come from users
    - don't be too reliant on template tags/filters. It slows down site performance. Beside, it's good to keep the logic outside of templates


## Source:

- [Custom template tags/filters documentation](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/)
- [Built-in template tags/filters documentation](https://docs.djangoproject.com/en/1.10/ref/templates/builtins/)
