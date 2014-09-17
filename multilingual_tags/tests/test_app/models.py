"""Just a dummy."""
from django.db import models
from django.contrib.contenttypes import generic


class DummyModel(models.Model):
    charfield = models.CharField(max_length=64)
    tags = generic.GenericRelation('multilingual_tags.TaggedItem')
    user = models.ForeignKey('auth.User')

    def get_user(self):
        return self.user
