from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    url('signup', views.userSignup, name='signup'),
    url('login', LoginView.as_view(template_name='locateBivacchi/login.html'), name='login'),
    url('', views.index, name='index'),
]
