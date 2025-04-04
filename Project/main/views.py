from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
# Create your views here.
def home(request):
    
    return render(request, "example.html")

def mainpage(request, username):
    userData = User.objects.get(username=username)
    return render(request, "example3.html", {"userData": userData})

def create(request):
    if(request.method=="POST"):
        form = CreateNewAccount(request.POST)
        if(form.is_valid()):
            form.full_clean()
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            role = request.POST.get("role") #0 = no account 1 = buyer 2 = seller 3 = admin
            balance = request.POST.get("balance")
            newUser = User(username=username, password=password, email=email, role=role, balance=balance)
            newUser.save()
            return HttpResponseRedirect("main/%s" % username)
    else:
        form = CreateNewAccount(request.POST)
        
    return render(request, "example2.html", {"form":form})


