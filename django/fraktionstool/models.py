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
        ordering = ['name']

    name = models.CharField(max_length=255)
    typ = models.ForeignKey(GremiumTyp)
    member = models.ManyToManyField(User, through='GremiumUser')

    def __unicode__(self):
        return self.name

class GremiumUser(models.Model):
    class Meta:
        verbose_name = "Gremium-User-Verknüpfung"
        verbose_name_plural = "Gremium-User-Verknüpfungen"

    gremium = models.ForeignKey(Gremium)
    user = models.ForeignKey(User)

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
        ordering = ['nummer','name']

    name = models.CharField(max_length=255)
    nummer = models.CharField(max_length=255)
    typ = models.ForeignKey(VorhabenTyp)
    date = models.DateField(verbose_name = "Datum")
    beobachten = models.BooleanField()
    geschlossen = models.BooleanField()
    gremien = models.ManyToManyField(Gremium, through='GremiumVorhaben')
    abstimmung = models.TextField(blank=True, verbose_name="Vorgaben")

    def __unicode__(self):
        return self.name

class GremiumVorhaben(models.Model):
    class Meta:
        verbose_name = "Gremien-Vorhaben-Verknüpfung"
        verbose_name_plural = "Gremien-Vorhaben-Verknüpfungen"

    gremium = models.ForeignKey(Gremium)
    vorhaben = models.ForeignKey(Vorhaben)

class Nachricht(models.Model):
    class Meta:
        verbose_name = "Nachricht"
        verbose_name_plural = "Nachrichten"

    text = models.TextField()
    owner = models.ForeignKey(User)
    vorhaben = models.ForeignKey(Vorhaben)
    gremium = models.ForeignKey(Gremium)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.text

class Hilfe(models.Model):
    class Meta:
        verbose_name = "Hilfetext"
        verbose_name_plural = "Hilfetexte"

    text = models.TextField()

    def __unicode__(self):
        return self.text
