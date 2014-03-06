"""Factories for the multilingual_tags app."""
from django.conf import settings
from django_libs.tests.factories import HvadFactoryMixin

import factory

from .. import models
from .test_app.models import DummyModel


class DummyModelFactory(factory.DjangoModelFactory):
    """Factory for the ``DummyModel`` test model."""
    FACTORY_FOR = DummyModel

    charfield = factory.Sequence(lambda n: 'charfield {0}'.format(n))


class TagFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    """Factory for the ``Tag`` model."""
    FACTORY_FOR = models.Tag

    slug = factory.Sequence(lambda n: 'slug-{0}'.format(n))
    name = factory.Sequence(lambda n: 'name {0}'.format(n))
    language_code = settings.LANGUAGE_CODE


class TaggedItemFactory(factory.DjangoModelFactory):
    """Factory for the ``TaggedItem`` model."""
    FACTORY_FOR = models.TaggedItem

    tag = factory.SubFactory(TagFactory)
    object = factory.SubFactory(DummyModelFactory)
