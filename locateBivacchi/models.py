# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bivacco(models.Model):
    coordinate_x = models.FloatField()
    coordinaye_y = models.FloatField()
    capability = models.IntegerField(default=0)
    height = models.IntegerField()

class Reservation(models.Model):
    bivacco = models.ForeignKey(Bivacco, on_delete=models.CASCADE)   
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.IntegerField(default=1234)
    person_number = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class bar(models.Model):
    request_time = models.IntegerField()
    location = models.TextField(max_length=100)
    description = models.TextField(max_length=100)