from django import forms

class CreateNewAccount(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=200)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=[("Buyer", "Buyer"), ("Seller", "Seller"), ("Admin", "Admin")])
    balance = forms.FloatField()

class CreateNewItem(forms.Form):
    category = forms.CharField(max_length=100)
    image = forms.ImageField()
    price = forms.FloatField()
    stock = forms.IntegerField()
    date_added=forms.DateField()
    
class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=200)
    email = forms.EmailField()
