# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
import time

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, "locateBivacchi/index.html")

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

def map(request):
    return render(request, 'locateBivacchi/maps.html')
