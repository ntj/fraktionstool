from django.db import models
from django.contrib.auth.models import User

class GremiumTyp(models.Model):
	name = models.CharField(max_length=255)

class Gremium(models.Model):
	name = models.CharField(max_length=255)
	typ = models.ForeignKey(GremiumTyp)

class VorhabenTyp(models.Model):
	name = models.CharField(max_length=255)

class Vorhaben(models.Model):
	name = models.CharField(max_length=255)
	nummer = models.CharField(max_length=255)
	typ = models.ForeignKey(VorhabenTyp)

class Nachricht(models.Model):
	text = models.TextField()
	owner = models.ForeignKey(User)
	vorhaben = models.ForeignKey(Vorhaben)
	gremium = models.ForeignKey(Gremium)

