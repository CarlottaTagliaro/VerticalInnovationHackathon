from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^temperature$', views.temperature, name='temperature'),
    url(r'^bar$', views.bar, name='bar'),
    url(r'^signup', views.userSignup, name='signup'),
    url(r'^login$', LoginView.as_view(template_name='locateBivacchi/login.html'), name='login'),
]
