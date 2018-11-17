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
from random import randint
from django.shortcuts import render, redirect
from datetime import datetime
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy as reverse
from .models import Bivacco, Reservation, Bar


def index(request):
    return render(request, "locateBivacchi/index.html")

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
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            print("NOOOOOOOOOOOOOOO")
    else:
        form = SignUpForm()
    return render(request, 'locateBivacchi/signup.html', {'form': form})


def checkCode(request,biv_pk):
    if request.method == 'GET':
        response = 0
        code = int(request.GET.get('code'))
        nr_res = Reservation.objects.filter(bivacco=biv_pk, start_date__lte=datetime.today(), end_date__gte=datetime.today(), code=code).count()
        if (nr_res > 0):
            response = 1
    return HttpResponse(response)


def map(request):
    biv_list = list(Bivacco.objects.all())
    return render(request, 'locateBivacchi/maps.html', {'biv_list': biv_list})

def _checkAvail(bivacco, start_date, end_date, person_number):
    prenotazioni = Reservation.objects.filter(
        bivacco=bivacco, start_date__lt=end_date, end_date__gt=start_date)

    # wrote this at 2 am, after 3 days of fever, so please dont judge it
    from datetime import timedelta, date
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    people = dict()

    for p in prenotazioni:
        for d in daterange(p.start_date, p.end_date):
            if d < start_date.date():
                continue
            if d > end_date.date():
                break

            if d not in people:
                people[d] = 0
            people[d] += p.person_number

    max_people = 0
    if len(people) > 0:
        max_people = max(people.values())

    if max_people + person_number <= bivacco.capability:
        return True
    else:
        return False

def checkBivaccoAvailability(request, id_bivacco, person_number, day_start,
                             month_start, year_start, day_end, month_end,
                             year_end):
    bivacco = get_object_or_404(Bivacco, pk=id_bivacco)

    start_date = datetime(year=year_start, month=month_start, day=day_start)
    end_date = datetime(year=year_end, month=month_end, day=day_end)

    if _checkAvail(bivacco, start_date, end_date, person_number):
        response = JsonResponse({'available': 'true'})
    else:
        response = JsonResponse({'available': 'false'})
    return response


@login_required(login_url=reverse("login"))
def reserveBivacco(request, id_bivacco, person_number, day_start,
                   month_start, year_start, day_end, month_end,
                   year_end):
    bivacco = get_object_or_404(Bivacco, pk=id_bivacco)

    start_date = datetime(year=year_start, month=month_start, day=day_start)
    end_date = datetime(year=year_end, month=month_end, day=day_end)

    if _checkAvail(bivacco=bivacco, start_date=start_date, end_date=end_date, person_number=person_number):
        reservation = Reservation()
        reservation.user = request.user
        reservation.bivacco = bivacco
        reservation.start_date = start_date
        reservation.end_date = end_date
        reservation.person_number = person_number
        reservation.code = randint(1000, 9999)

        reservation.save()

        return JsonResponse(
        {
            'available': 'true',
            'code': reservation.code
        })

    return JsonResponse({
        'available': 'false',
        'code': -1
    })

def reservations(request):
    return render(request,'locateBivacchi/manageReservation.html')
    
def viewBivacco(request, id_bivacco):
    if request.method == 'GET':
        bivacco = get_object_or_404(Bivacco, pk=id_bivacco)
        #info = get_nearest_station(bivacco.coordinate_x, bivacco.coordinate_y)
        return render(request, "locateBivacchi/bivacco.html", {'bivacco': bivacco, 'user': request.user})
