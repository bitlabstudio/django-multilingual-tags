"""Just dummy forms to test."""
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import DummyModel
from ...forms.mixins import TaggingFormMixin


class DummyModelForm(TaggingFormMixin, forms.ModelForm):

    class Meta:
        model = DummyModel
        fields = ('charfield', )


class LimitedDummyModelForm(TaggingFormMixin, forms.ModelForm):

    tag_field = {
        'name': 'tags',
        'label': _('Tags'),
        'help_text': _('Add tags separated by comma.'),
        'required': True,
        'max_tags': 1,
    }

    class Meta:
        model = DummyModel
        fields = ('charfield', )
