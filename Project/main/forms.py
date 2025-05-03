from django import forms
from django.conf import settings
from django.contrib.sessions.models import Session
from datetime import timedelta

# Add session timeout configuration
settings.SESSION_COOKIE_AGE = timedelta(minutes=30).total_seconds()

class CreateNewAccount(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[("Buyer", "Buyer"), ("Seller", "Seller"), ("Admin", "Admin")])
    balance = forms.FloatField()

class CreateNewItem(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=200)
    category = forms.CharField(max_length=100)
    image = forms.ImageField()
    price = forms.FloatField()
    stock = forms.IntegerField()
    
class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    email = forms.EmailField()

class EditAccount(forms.Form):
    # hidden fields to keep browser from autofilling saved username and password
    username = forms.CharField(max_length=50, required=False,
                               widget=forms.TextInput(attrs={'autocomplete':'new-username'}))
    password = forms.CharField(max_length=200, required=False,
                               widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}))
    email = forms.EmailField(required=False,
                             widget=forms.EmailInput(attrs={'autocomplete':'off'}))
    add_money = forms.FloatField(required=False,
                                widget=forms.NumberInput(attrs={'autocomplete':'off'}))