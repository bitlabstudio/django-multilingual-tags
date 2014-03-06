# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagTranslation'
        db.create_table(u'multilingual_tags_tag_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['multilingual_tags.Tag'])),
        ))
        db.send_create_signal(u'multilingual_tags', ['TagTranslation'])

        # Adding unique constraint on 'TagTranslation', fields ['language_code', 'master']
        db.create_unique(u'multilingual_tags_tag_translation', ['language_code', 'master_id'])

        # Adding model 'Tag'
        db.create_table(u'multilingual_tags_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'multilingual_tags', ['Tag'])

        # Adding model 'TaggedItem'
        db.create_table(u'multilingual_tags_taggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tagged_items', to=orm['multilingual_tags.Tag'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'multilingual_tags', ['TaggedItem'])

        # Adding unique constraint on 'TaggedItem', fields ['content_type', 'object_id', 'tag']
        db.create_unique(u'multilingual_tags_taggeditem', ['content_type_id', 'object_id', 'tag_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TaggedItem', fields ['content_type', 'object_id', 'tag']
        db.delete_unique(u'multilingual_tags_taggeditem', ['content_type_id', 'object_id', 'tag_id'])

        # Removing unique constraint on 'TagTranslation', fields ['language_code', 'master']
        db.delete_unique(u'multilingual_tags_tag_translation', ['language_code', 'master_id'])

        # Deleting model 'TagTranslation'
        db.delete_table(u'multilingual_tags_tag_translation')

        # Deleting model 'Tag'
        db.delete_table(u'multilingual_tags_tag')

        # Deleting model 'TaggedItem'
        db.delete_table(u'multilingual_tags_taggeditem')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'multilingual_tags.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'multilingual_tags.taggeditem': {
            'Meta': {'unique_together': "(('content_type', 'object_id', 'tag'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tagged_items'", 'to': u"orm['multilingual_tags.Tag']"})
        },
        u'multilingual_tags.tagtranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'TagTranslation', 'db_table': "u'multilingual_tags_tag_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['multilingual_tags.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['multilingual_tags']
