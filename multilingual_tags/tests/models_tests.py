"""Tests for the models of the multilingual_tags app."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from .test_app.models import DummyModel
from django_libs.tests.factories import UserFactory

from . import factories
from .. import models


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


class TagManagerTestCase(TestCase):
    """Tests for the `TagManager` manager class."""
    longMessage = True

    def setUp(self):
        self.tagged_item = factories.TaggedItemFactory()
        self.dummy = self.tagged_item.object
        self.tag = self.tagged_item.tag
        self.other_tagged_item = factories.TaggedItemFactory(object=self.dummy)

        factories.TaggedItemFactory()

        self.user_item = factories.TaggedItemFactory(object=UserFactory())

    def test_manager(self):
        self.assertEqual(
            list(models.Tag.objects.get_for_obj(self.dummy)),
            list(models.Tag.objects.filter(
                tagged_items__object_id=self.dummy.id,
                tagged_items__content_type=ContentType.objects.get_for_model(
                    DummyModel))),
            msg='Expected different tags from the manager.')

        self.assertEqual(
            list(models.Tag.objects.get_for_queryset(
                DummyModel.objects.all())),
            list(models.Tag.objects.exclude(
                tagged_items__id=self.user_item.id)),
            msg='Expected different tags from the manager.')
