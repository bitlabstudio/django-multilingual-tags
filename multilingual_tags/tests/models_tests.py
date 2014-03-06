"""Tests for the models of the multilingual_tags app."""
from django.test import TestCase

from . import factories


class DummyModelTestCase(TestCase):
    """Tests for the ``DummyModel`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``DummyModel`` model."""
        dummymodel = factories.DummyModelFactory()
        self.assertTrue(dummymodel.pk)


class TagTestCase(TestCase):
    """Tests for the ``Tag`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Tag`` model."""
        tag = factories.TagFactory()
        self.assertTrue(tag.pk)


class TaggedItemTestCase(TestCase):
    """Tests for the ``TaggedItem`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaggedItem`` model."""
        taggeditem = factories.TaggedItemFactory()
        self.assertTrue(taggeditem.pk)
