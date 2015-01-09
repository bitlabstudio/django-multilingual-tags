"""Form mixins for the ``multilingual_tags`` app."""
from django import forms
from django.forms.fields import ErrorList
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
        'max_tags': 0,
    }

    def __init__(self, *args, **kwargs):
        super(TaggingFormMixin, self).__init__(*args, **kwargs)
        self._taggeditems = []
        self._instance_ctype = None
        self.fields[self._get_tag_field_name()] = forms.CharField(
            label=self._get_tag_field_label(),
            help_text=self._get_tag_field_help_text(),
            initial=self._get_tag_field_initial(),
            required=self._get_tag_field_required(),
        )
        self.fields[self._get_tag_field_name()].widget.attrs.update({
            'data-class': 'multilingual-tags-field',
            'data-max-tags': self._get_tag_field_max_tags()})
        setattr(self, 'clean_{0}'.format(self._get_tag_field_name()),
                self._get_tag_field_clean())

    def add_error(self, fieldname, message):
        if fieldname in self._errors:
            self._errors[fieldname].append(message)
        else:
            self._errors[fieldname] = ErrorList()
            self._errors[fieldname].append(message)

    def _get_tag_field_clean(self):
        def clean_field():
            self._tags_added = []
            self._taggeditems = []
            language = get_language()
            max_tags = self._get_tag_field_max_tags()

            data = self.data.get(self._get_tag_field_name())
            if not data:
                return []
            tag_data = [t.strip() for t in data.split(',')]
            self._instance_ctype = ContentType.objects.get_for_model(
                self.instance)
            for tag_string in tag_data:
                if len(tag_string) > 64:
                    self.add_error(
                        self._get_tag_field_name(),
                        _('Tags cannot be longer than 64 characters:'
                          ' "{0}"'.format(tag_string))
                    )
                    continue
                try:
                    tag = models.Tag.objects.language(language).get(
                        slug=slugify(tag_string))
                except models.Tag.DoesNotExist:
                    tag = models.Tag.objects.create(
                        slug=slugify(tag_string),
                        name=tag_string,
                        language_code=language)
                # prevent duplicate tags
                if tag not in self._tags_added:
                    self._tags_added.append(tag)
                    if self.instance.id:
                        taggeditem, created = (
                            models.TaggedItem.objects.get_or_create(
                                tag=tag,
                                content_type=self._instance_ctype,
                                object_id=self.instance.id,
                            )
                        )
                    else:
                        taggeditem = models.TaggedItem(
                            tag=tag,
                            content_type=self._instance_ctype)
                    self._taggeditems.append(taggeditem)
                if max_tags and len(self._tags_added) > max_tags:
                    self.add_error(
                        self._get_tag_field_name(),
                        _('You cannot add more than {0} tags.'.format(
                            self._get_tag_field_max_tags()
                        ))
                    )
            return self._taggeditems
        return clean_field

    def _get_tag_field_help_text(self):
        return self.tag_field.get('help_text', '')

    def _get_tag_field_initial(self):
        tag_model_field = getattr(self.instance, self._get_tag_field_name())
        return ','.join([ti.tag.name for ti in tag_model_field.all()])

    def _get_tag_field_label(self):
        return self.tag_field.get('label', 'Tags')

    def _get_tag_field_max_tags(self):
        return int(self.tag_field.get('max_tags', 0))

    def _get_tag_field_name(self):
        return self.tag_field.get('name', 'tags')

    def _get_tag_field_required(self):
        return self.tag_field.get('required', True)

    def save(self, commit=True):
        instance = super(TaggingFormMixin, self).save(commit)
        for item in self._taggeditems:
            if hasattr(instance, 'get_user'):
                item.user = instance.get_user()
            item.object_id = instance.id
            item.save()
        models.TaggedItem.objects.filter(
            content_type=self._instance_ctype,
            object_id=instance.id).exclude(
            pk__in=[ti.pk for ti in self._taggeditems]).delete()
        return instance
