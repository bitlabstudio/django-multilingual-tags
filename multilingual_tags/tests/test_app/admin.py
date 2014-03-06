"""Test admins"""
from django.contrib import admin

from multilingual_tags.admin import TaggedItemInline

from . import models


class DummyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]

admin.site.register(models.DummyModel, DummyAdmin)
