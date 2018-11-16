# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from datetime import datetime
import time
from locateBivacchi.models import Bar, Bivacco, Reservation
from django.shortcuts import get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def temperature(request, biv_pk):
    response = ''
    if(request.method == 'GET'):
        temp = int(request.GET.get('temp'))
        response = temp
        if (temp > -10 and temp < 50):
            obj = get_object_or_404(Bivacco, pk=biv_pk)
            obj.temp = temp
            obj.save()
    return HttpResponse(response)

def bar(request, bar_pk):
    response = 0
    date_now = datetime.now()
    date_server = int(time.mktime(date_now.timetuple()))
    bar = get_object_or_404(Bar, pk=bar_pk)
    date_open = date_server - int(bar.request_time)
    if (date_open < 20):
        response = 1
    return HttpResponse(response)

def userSignup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home') # TODO: cambiare questo
    else:
        form = UserCreationForm()
    return render(request, 'locateBivacchi/signup.html', {'form': form})

def checkCode(request,biv_pk):
    if request.method == 'GET':
        response = 0
        code = int(request.GET.get('code'))
        nr_res = Reservation.objects.filter(Bivacco=biv_pk, start_date__lte=datetime.today, end_date__gte=datetime.today, code=code).count()
        if (nr_res > 0):
            response = 1
    return HttpResponse(response)
        
