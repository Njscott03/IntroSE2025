from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
import random
# Create your views here.
def home(request):
    isLoggedIn = 0
    return render(request, "index.html", {'isLoggedIn': isLoggedIn})

def mainpage(request, userID):
    isLoggedIn = 1
    userData = User.objects.get(userID=userID)
    return render(request, "index.html", {"userData": userData})

def create(request):
    idIsValid = False
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

            #Randomize ID until u get one that isnt in database
            while(not idIsValid):
                newUser.userID = random.randint(0, 1000000000)
                try:
                    User.objects.get(userID=newUser.userID)
                    
                except User.DoesNotExist:
                    idIsValid = True
            #Username must e unique
            if(User.objects.filter(username=username).exists()):
                messages.add_message(request, messages.SUCCESS, "Username taken")
              
            else:
                newUser.save() #If usename is unique, save the new account to database
                return HttpResponseRedirect("/%i/main" % newUser.userID)   #Redirects page to <int:userID>/main
    else:
        form = CreateNewAccount(request.POST)
        
    return render(request, "createAccount.html", {"form":form})

def search(request, UserID = 0):
    searchTerm = ''
    items = []
    if(request.method == "POST"):
        if(request.POST.get("search")):
            searchTerm = request.POST.get("search")
            items = Item.objects.filter(Q(name__contains = searchTerm) | Q(category__contains = searchTerm))
            
    return render(request, "search.html", {"items":items})
    
