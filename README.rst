Django Multilingual Tags
========================

A reusable Django app that allows you to add translatable tags to any other
model.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-multilingual-tags

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-multilingual-tags.git#egg=multilingual_tags


Add ``multilingual_tags`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'multilingual_tags',
    )


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate multilingual_tags


Usage
-----

Add a generic relation to the model, that you intend to tag.

.. code-block:: python

    from django.contrib.contenttypes import generic
    from django.db import models


    class UserProfile(models.Model):

        # ...
        # some other model stuff goes here
        # ...

        special_attributes = generic.GenericRelation(
            'multilingual_tags.TaggedItem',
        )


Add the ``TaggingFormMixin`` to any of your modelforms of a model, you want to
tag and configure the field with the settings dictionary. ``allowed_tags``
configures how many tags a user may add. If it's set to 0 (default), it means,
that the input is not limited.

.. code-block:: python

    from django import forms

    from multilingual_tags.forms.mixins import TaggingFormMixin


    class UserProfileForm(TaggingFormMixin, forms.ModelForm):

        tag_field = {
            # ``name`` is the name of the ``GenericRelation`` that was added to
            # the model
            'name': 'special_attributes',
            'label': _('Special Attributes'),
            'help_text': _('List any special attributes separated with comma.'),
            'required': False,
            'max_tags': 0,
        }


The form mixin will automatically add ``data-class="multilingual-tags-field"``
to the form field. This allows you to easily add ``jquery-typeahead-tagging``
to your field, which is included in this app.

Simply add the static files from ``multilingual_tags`` to your template.

.. code-block:: html

    {% load static %}

    {# Plain Bootstrap-like styles. #}
    <link href="{% static "multilingual_tags/css/typeahead.tagging.css" %}" rel="stylesheet" media="screen">

    {# You will also need jquery of course. #}
    <script src="{% static "js/libs/jquery-1.9.1.js" %}"></script>

    {# And then there's typeahead and the tagging plugin. #}
    <script src="{% static "multilingual_tags/js/typeahead.bundle.min.js" %}"></script>
    <script src="{% static "multilingual_tags/js/typeahead.tagging.js" %}"></script>


Then you can initialize your tagging field like so:

.. code-block:: javascript


    // The source of the tags for autocompletion
    var tagsource = ['Foo', 'Bar', 'Anoter Tag', 'Even more tags',
                     'Such autocomplete', 'Many tags', 'Wow'];

    // Turn the input into the tagging input
    $('[data-class="multilingual-tags-field"]').tagging(tagsource);


Et voila! That should really be all there is.


Storing the user
++++++++++++++++

For easier access later on, you can store the user, that the tagged item belongs
to on the ``TaggedItem`` itself. The form mixin will check if the instance of
the ``ModelForm`` you use it with has a ``get_user`` method for that matter.

.. code-block:: python

    class MyObject(models.Model):

        # here goes my model implementation

        def get_user(self):
            """Here I can return the user I want on the TaggedItem"""
            return self.user


Admin
+++++

To add tags to a model, you have to add the ``TaggedItemInline`` to
that model's admin. In your own apps, you can just do the following:

.. code-block:: python

    from django.contrib import admin

    from multilingual_tags.admin import TaggedItemInline

    from my_app import models

    class MyModelAdmin(admin.ModelAdmin):
        inlines = [TaggedItemInline]

    admin.site.register(models.MyModel, MyModelAdmin)

This will render the inline admin form for adding tagged items.

If you want to add tags to a third party app, you might need to import its
admin instead of Django's ``ModelAdmin`` and then unregister and re-register
the model. One way to do it would be this:

.. code-block:: python

    from django.contrib import admin

    from multilingual_tags.admin import TaggedItemInline

    from other_app.admin import SomeModelAdmin
    from other_app.models import SomeModel

    class SomeModelCustomAdmin(SomeModelAdmin):
        # be careful, if the other admin also defines admins, you need to add
        # them as well
        inlines = SomeModelAdmin.inlines + [TaggedItemInline]

    admin.site.unregister(SomeModel)
    admin.site.register(SomeModel, SomeModelCustomAdmin)


To get all the tags for an object, you can simply use the `TagManager`:

.. code-block:: python

    # Get all tags for a certain model instance
    >> Tag.objects.get_for_obj(mymodel_instance)

    [<Tag: mytag>, <Tag: myothertag>]

    # .. or get all tags for an entire queryset
    >> Tag.objects.get_for_queryset(MyModel.objects.all())

    [<Tag: mytag>, <Tag: myothertag>]



Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-multilingual-tags
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
