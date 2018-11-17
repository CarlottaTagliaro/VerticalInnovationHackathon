from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254, help_text='Username', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Name'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Surname'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'}))
    password1 = forms.CharField(label=("Password"),widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Password', 'type':'password'}))
    password2 = forms.CharField(label=("Password confirmation"), help_text=("Enter the same password as above, for verification."),widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Repeat Password', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )