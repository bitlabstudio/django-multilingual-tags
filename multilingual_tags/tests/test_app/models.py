"""Just a dummy."""
from django.db import models


class DummyModel(models.Model):
    charfield = models.CharField(max_length=64)
