"""Tests for the form mixins of the ``multilingual_tags`` app."""
from django.test import TestCase

from ..models import Tag, TaggedItem
from .factories import DummyModelFactory
from .test_app.forms import DummyModelForm
from .test_app.models import Dummy


class TaggingFormMixinTestCase(TestCase):
    """Tests for the ``TaggingFormMixin`` form mixin."""
    longMessage = True

    def setUp(self):
        self.dummy = DummyModelFactory
        self.data = {
            'charfield': 'foobar',
            'tags': 'tagging, test'
        }

    def test_mixin(self):
        form = DummyModelForm(data=self.data)
        self.assertTrue(form.is_valid(), msg=(
            'The form should be valid. Errors: {0}'.format(form.errors)))

        form.save()
        self.assertEqual(Dummy.objects.count(), 1, msg=(
            'The form should have saved one dummy.'))
        self.assertEqual(TaggedItem.objects.count(), 2, msg=(
            'The form should create one TaggedItem per entered tag.'))
        self.assertEqual(Tag.objects.count(), 2, msg=(
            'The form should create one Tag per entered tag.'))
