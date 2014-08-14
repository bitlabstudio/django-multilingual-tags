"""Form mixins for the ``multilingual_tags`` app."""
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import get_language, ugettext_lazy as _

from .. import models


class TaggingFormMixin(object):
    """Mixin for ModelForms to add multilingual tags to a model."""
    tag_field = {
        'name': 'tags',
        'label': _('Tags'),
        'help_text': _('Add tags separated by comma.'),
        'required': True,
    }

    def __init__(self, *args, **kwargs):
        super(TaggingFormMixin, self).__init__(*args, **kwargs)
        self.fields[self._get_tag_field_name()] = forms.CharField(
            label=self._get_tag_field_label(),
            help_text=self._get_tag_field_help_text(),
            initial=self._get_tag_field_initial(),
            required=self._get_tag_field_required(),
        )
        self.fields[self._get_tag_field_name()].widget.attrs.update({
            'data-class': 'multilingual-tags-field'})
        setattr(self, 'clean_{0}'.format(self._get_tag_field_name()),
                self._get_tag_field_clean())

    def _get_tag_field_clean(self):
        def clean_field():
            data = self.data.get(self._get_tag_field_name())
            if not data:
                return []
            instance_ctype = ContentType.objects.get_for_model(self.instance)
            tag_data = [t.strip() for t in data.split(',')]
            taggeditems = []
            language = get_language()
            for tag_string in tag_data:
                try:
                    tag = models.Tag.objects.language(language).get(
                        slug=slugify(tag_string))
                except models.Tag.DoesNotExist:
                    tag = models.Tag.objects.create(
                        slug=slugify(tag_string),
                        name=tag_string,
                        language_code=language)
                taggeditem, created = models.TaggedItem.objects.get_or_create(
                    tag=tag,
                    content_type=instance_ctype,
                    object_id=self.instance.id)
                taggeditems.append(taggeditem)
            models.TaggedItem.objects.filter(
                content_type=instance_ctype,
                object_id=self.instance.id).exclude(
                    pk__in=[ti.pk for ti in taggeditems]).delete()
            return taggeditems
        return clean_field

    def _get_tag_field_help_text(self):
        return self.tag_field.get('help_text', '')

    def _get_tag_field_initial(self):
        tag_model_field = getattr(self.instance, self._get_tag_field_name())
        return ','.join([ti.tag.name for ti in tag_model_field.all()])

    def _get_tag_field_label(self):
        return self.tag_field.get('label', 'Tags')

    def _get_tag_field_name(self):
        return self.tag_field.get('name', 'tags')

    def _get_tag_field_required(self):
        return self.tag_field.get('required', True)
