from django import forms

class CreateNewAccount(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=200)
    email = forms.EmailField()
    role = forms.IntegerField() #0 = no account 1 = buyer 2 = seller 3 = admin
    balance = forms.FloatField()

class CreateNewItem(forms.Form):
    category = forms.CharField(max_length=100)
    image = forms.ImageField()
    price = forms.FloatField()
    stock = forms.IntegerField()
    date_added=forms.DateField()
