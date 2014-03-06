"""Test admins"""
from django.contrib import admin

from multilingual_tags.admin import MultilingualTagsAdminMixin

from . import models


class DummyAdmin(MultilingualTagsAdminMixin, admin.ModelAdmin):
    pass

admin.site.register(models.DummyModel, DummyAdmin)
