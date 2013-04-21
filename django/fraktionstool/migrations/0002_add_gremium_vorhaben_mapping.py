# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GremiumVorhaben'
        db.create_table(u'fraktionstool_gremiumvorhaben', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gremium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fraktionstool.Gremium'])),
            ('vorhaben', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fraktionstool.Vorhaben'])),
        ))
        db.send_create_signal(u'fraktionstool', ['GremiumVorhaben'])


    def backwards(self, orm):
        # Deleting model 'GremiumVorhaben'
        db.delete_table(u'fraktionstool_gremiumvorhaben')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fraktionstool.gremium': {
            'Meta': {'object_name': 'Gremium'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'typ': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.GremiumTyp']"})
        },
        u'fraktionstool.gremiumtyp': {
            'Meta': {'object_name': 'GremiumTyp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'fraktionstool.gremiumvorhaben': {
            'Meta': {'object_name': 'GremiumVorhaben'},
            'gremium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.Gremium']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vorhaben': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.Vorhaben']"})
        },
        u'fraktionstool.nachricht': {
            'Meta': {'object_name': 'Nachricht'},
            'gremium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.Gremium']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'vorhaben': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.Vorhaben']"})
        },
        u'fraktionstool.vorhaben': {
            'Meta': {'object_name': 'Vorhaben'},
            'gremien': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fraktionstool.Gremium']", 'through': u"orm['fraktionstool.GremiumVorhaben']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nummer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'typ': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fraktionstool.VorhabenTyp']"})
        },
        u'fraktionstool.vorhabentyp': {
            'Meta': {'object_name': 'VorhabenTyp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['fraktionstool']