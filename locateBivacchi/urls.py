from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('temperature/<int:biv_pk>/', views.temperature, name='temperature'),
    path('bar/<int:bar_pk>/', views.bar),
    path('checkcode/<int:bar_pk>/', views.checkCode),
    url(r'^map$', views.map, name='map'),
    url(r'^signup', views.userSignup, name='signup'),
    url(r'^login$', LoginView.as_view(template_name='locateBivacchi/login.html'), name='login'),
]
