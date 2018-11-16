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
from django.shortcuts import get_object_or_404
from .models import Bivacco, Reservation

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

def checkBivaccoAvailability(request, id_bivacco, person_number, day_start,
                             month_start, year_start, day_end, month_end,
                             year_end):
    bivacco = get_object_or_404(Bivacco, pk=id_bivacco)

    start_date = datetime(year=year_start, month=month_start, day=day_start)
    end_date = datetime(year=year_end, month=month_end, day=day_end)

    prenotazioni = Reservation.objects.filter(
        bivacco=bivacco, start_date__lt=end_date, end_date__gt=start_date)

    people = 0
    for p in prenotazioni:
        people += p.person_number

    if people + person_number <= bivacco.capability:
        response = response = JsonResponse({'available': 'true'})
    else:
        response = JsonResponse({'available': 'false'})
    return response
