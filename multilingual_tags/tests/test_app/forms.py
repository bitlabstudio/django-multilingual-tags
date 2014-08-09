"""Just dummy forms to test."""
from django import forms

from .models import DummyModel
from ...forms.mixins import TaggingFormMixin


class DummyModelForm(TaggingFormMixin, forms.ModelForm):

    class Meta:
        model = DummyModel
