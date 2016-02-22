"""Tests for the models of the multilingual_tags app."""
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from mixer.backend.django import mixer

from .. import models
from .test_app.models import DummyModel


class DummyModelTestCase(TestCase):
    """Tests for the ``DummyModel`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``DummyModel`` model."""
        dummymodel = mixer.blend('test_app.DummyModel')
        self.assertTrue(dummymodel.pk)


class TagTestCase(TestCase):
    """Tests for the ``Tag`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Tag`` model."""
        tag = mixer.blend('multilingual_tags.TagTranslation')
        self.assertTrue(tag.pk)


class TaggedItemTestCase(TestCase):
    """Tests for the ``TaggedItem`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``TaggedItem`` model."""
        self.dummy = mixer.blend('test_app.DummyModel')
        self.tag = mixer.blend('multilingual_tags.TagTranslation',
                               language_code='en').master
        taggeditem = mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(DummyModel),
            object_id=self.dummy.pk)
        self.assertTrue(taggeditem.pk)


class TagManagerTestCase(TestCase):
    """Tests for the `TagManager` manager class."""
    longMessage = True

    def setUp(self):
        self.dummy = mixer.blend('test_app.DummyModel')
        self.tag = mixer.blend('multilingual_tags.TagTranslation',
                               language_code='en').master
        mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(DummyModel),
            object_id=self.dummy.pk)

        self.user_item = mixer.blend(
            'multilingual_tags.TaggedItem',
            tag=self.tag,
            content_type=ContentType.objects.get_for_model(User),
            object_id=mixer.blend('auth.User').pk)

    def test_manager(self):
        self.assertEqual(
            list(models.Tag.objects.get_for_obj(self.dummy)),
            list(models.Tag.objects.filter(
                tagged_items__object_id=self.dummy.id,
                tagged_items__content_type=ContentType.objects.get_for_model(
                    DummyModel))),
            msg='Expected different tags from the manager.')
