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

To add tags to a model, you have to add the `MultilingualTagsAdminMixin` to
that model's admin. In your own apps, you can just do the following:

.. code-block:: python

    from django.contrib import admin

    from multilingual_tags.admin import MultilingualTagsAdminMixin

    from my_app import models

    class MyModelAdmin(MultilingualTagsAdminMixin, admin.ModelAdmin):
        pass

    admin.site.register(models.MyModel, MyModelAdmin)

This will render the inline admin form for adding tagged items.

If you want to add tags to a third party app, you might need to import its
admin instead of Django's `ModelAdmin` and then unregister and re-register the
model.

.. code-block:: python

    from django.contrib import admin

    from multilingual_tags.admin import MultilingualTagsAdminMixin

    from other_app.admin import SomeModelAdmin
    from other_app.models import SomeModel

    class SomeModelCustomAdmin(MultilingualTagsAdminMixin, SomeModelAdmin):
        pass

    admin.site.unregister(SomeModel)
    admin.site.register(SomeModel, SomeModelCustomAdmin)


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
