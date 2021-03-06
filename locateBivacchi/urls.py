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

from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('temperature/<int:biv_pk>/', views.temperature, name='temperature'),
    path('bar/<int:bar_pk>/', views.bar),
    path('opengate/<int:id_gate>/', views.open_gate),
    path('checkcode/<int:biv_pk>/', views.checkCode),
    url(r'^map$', views.map, name='map'),
    url(r'^signup', views.userSignup, name='signup'),
    url(r'^logout/$', LogoutView.as_view() ,{'next_page': '/'}),
    path('checkavailable/<int:id_bivacco>/<int:person_number>/<int:day_start>/<int:month_start>/<int:year_start>/<int:day_end>/<int:month_end>/<int:year_end>/', views.checkBivaccoAvailability, name="check_availability"),
    path('reserve/<int:id_bivacco>/', views.reserveBivacco, name="reserve"),
    path('reservation', views.reservations, name="reservation"),
    path('viewbivacco/<int:id_bivacco>/', views.viewBivacco, name="viewBivacco"),
]
