# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class bivacco(models.Model):
    coordinate_x = models.FloatField()
    coordinaye_y = models.FloatField()
    capability = models.IntegerField(default=0)
    height = models.IntegerField()

class utente(models.Model):
    name = models.TextField(max_length=30)
    surname = models.TextField(max_length=30)
    CF = models.TextField(max_length=16 primary_key=True)
    email = models.EmailField

class reservation(models.Model):
    id_bivacco = models.ForeignKey(bivacco, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = model.DateField()
    person_number = model.IntegerField(default=0)
    id_utente = models.ForeignKey(utente, on_delete=models.CASCADE)