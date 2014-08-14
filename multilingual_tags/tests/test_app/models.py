"""Just a dummy."""
from django.db import models
from django.contrib.contenttypes import generic


class DummyModel(models.Model):
    charfield = models.CharField(max_length=64)
    tags = generic.GenericRelation('multilingual_tags.TaggedItem')
