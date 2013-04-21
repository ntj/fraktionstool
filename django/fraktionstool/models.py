# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class GremiumTyp(models.Model):
	class Meta:
		verbose_name = "Gremientyp"
		verbose_name_plural = "Gremientypen"

	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Gremium(models.Model):
	class Meta:
		verbose_name = "Gremium"
		verbose_name_plural = "Gremien"

	name = models.CharField(max_length=255)
	typ = models.ForeignKey(GremiumTyp)

	def __unicode__(self):
		return self.name

class VorhabenTyp(models.Model):
	class Meta:
		verbose_name = "Vorhabentyp"
		verbose_name_plural = "Vorhabentypen"

	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Vorhaben(models.Model):
	class Meta:
		verbose_name = "Vorhaben"
		verbose_name_plural = "Vorhaben"

	name = models.CharField(max_length=255)
	nummer = models.CharField(max_length=255)
	typ = models.ForeignKey(VorhabenTyp)

	def __unicode__(self):
		return self.name

class Nachricht(models.Model):
	class Meta:
		verbose_name = "Nachricht"
		verbose_name_plural = "Nachrichten"

	text = models.TextField()
	owner = models.ForeignKey(User)
	vorhaben = models.ForeignKey(Vorhaben)
	gremium = models.ForeignKey(Gremium)

	def __unicode__(self):
		return self.text

