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

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


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
