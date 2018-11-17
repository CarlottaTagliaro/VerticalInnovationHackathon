"""Copyright (C) 2018  Smart Bivouac
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bivacco(models.Model):
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    capability = models.IntegerField(default=0)
    height = models.IntegerField()
    temp = models.IntegerField()
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)

class Reservation(models.Model):
    bivacco = models.ForeignKey(Bivacco, on_delete=models.CASCADE)   
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.IntegerField(default=1234)
    person_number = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Bar(models.Model):
    request_time = models.IntegerField()
    location = models.TextField(max_length=100)
    description = models.TextField(max_length=100)