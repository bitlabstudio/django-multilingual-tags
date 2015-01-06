"""Just a dummy."""
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic


class DummyModel(models.Model):
    charfield = models.CharField(max_length=64)
    tags = generic.GenericRelation('multilingual_tags.TaggedItem')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_user(self):
        return self.user
