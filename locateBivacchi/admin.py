# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from locateBivacchi.models import Bar, Bivacco, Reservation

admin.site.register(Bar)
admin.site.register(Reservation)
admin.site.register(Bivacco)

# Register your models here.
