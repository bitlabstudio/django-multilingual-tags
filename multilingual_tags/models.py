"""Models for the `multilingual_tags` app."""
from django.contrib.contenttypes import fields, models as ctype_models
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from django.conf import settings

from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields


class TagManager(TranslatableManager):
    """Manager for the `Tag` model."""
    def get_for_model(self, obj):
        """Returns the tags for a specific model/content type."""
        qs = Tag.objects.language(get_language())
        qs = qs.filter(
            tagged_items__content_type=ctype_models.ContentType.objects.get_for_model(obj))  # NOQA
        return qs.distinct()

    def get_for_obj(self, obj):
        """Returns the tags for a specific object."""
        qs = Tag.objects.language(get_language())
        qs = qs.filter(
            tagged_items__object_id=obj.id,
            tagged_items__content_type=ctype_models.ContentType.objects.get_for_model(obj))  # NOQA
        return qs.distinct()

    def get_for_queryset(self, obj_queryset):
        """Returns all tags for a whole queryset of objects."""
        qs = Tag.objects.language(get_language())
        if obj_queryset.count() == 0:
            return qs.none()
        qs = qs.filter(
            tagged_items__object_id__in=[
                obj.id for obj in obj_queryset],
            tagged_items__content_type=ctype_models.ContentType.objects.get_for_model(obj_queryset[0]))  # NOQA
        return qs.distinct()


class Tag(TranslatableModel):
    """
    The information about the tag itself.

    :slug: A unique slug.

    translated:
    :name: A translatable name of the tag.

    """

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=64,
        unique=True,
    )

    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_('Name'),
            max_length=64,
        ),
    )

    objects = TagManager()

    def __str__(self):
        return self.safe_translation_getter('name', self.slug)


class TaggedItem(models.Model):
    """
    Intermediary model to attach a `Tag` to any other model instance.

    :tag: FK to the `Tag` that is atttached.
    :object: GFK to the other model instance, which is being tagged.

    """

    tag = models.ForeignKey(
        Tag,
        verbose_name=_('Tag'),
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

    content_type = models.ForeignKey(
        ctype_models.ContentType,
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    object = fields.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='tagged_items',
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return u'{0}: #{1}'.format(self.object, self.tag)

    class Meta:
        unique_together = ('content_type', 'object_id', 'tag')
