from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^temperature$', views.temperature, name='temperature'),
        url(r'^bar$', views.bar, name='bar'),
]
