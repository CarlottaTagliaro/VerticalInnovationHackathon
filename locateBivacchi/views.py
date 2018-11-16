# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
import time

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def temperature(request):
    response = ''
    if(request.method == 'GET'):
        temp = request.GET.get('temp')
        response = temp
    return HttpResponse(response)

def bar(request):
    response = 0
    date_now = datetime.now()
    date_server = int(time.mktime(date_now.timetuple()))
    if (request.method == 'GET'):
        return HttpResponse(date_server)

    