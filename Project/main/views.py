from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
import random
from .models import Item

# Create your views here.
def home(request):
    # show first 20 approved products alphabetically on homepage
    items = Item.objects.filter(approved=True).order_by('name')[:20]
    return render(request, "index.html", {'items': items})

def mainpage(request, userID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=userID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":userID, "items":items})

    items = Item.objects.filter(approved=True).order_by('name')[:20]

    return render(request, "index.html", {"userData": userData, "items": items})

def create(request):
    idIsValid = False
    if(request.method=="POST"):
        form = CreateNewAccount(request.POST)
        if(form.is_valid()):
            form.full_clean()
            username = request.POST.get("username")
            
            password = request.POST.get("password")
            email = request.POST.get("email")
            role = request.POST.get("role") #1 = buyer 2 = seller 3 = admin
            balance = request.POST.get("balance")
            if(role == "Buyer"):
                role = 1
            elif(role == "Seller"):
                role = 2
            elif(role == "Admin"):
                role = 3
            newUser = User(username=username, password=password, email=email, role=role, balance=balance)

            #Randomize ID until u get one that isnt in database
            while(not idIsValid):
                newUser.userID = random.randint(0, 1000000000)
                try:
                    User.objects.get(userID=newUser.userID)
                    
                except User.DoesNotExist:
                    idIsValid = True
            #Username must be unique
            if(User.objects.filter(username=username).exists()):
                messages.add_message(request, messages.SUCCESS, "Username taken")
              
            else:
                newUser.save() #If usename is unique, save the new account to database
                return HttpResponseRedirect("/%i/main" % newUser.userID)   #Redirects page to <int:userID>/main
    else:
        form = CreateNewAccount(request.POST)
        
    return render(request, "createAccount.html", {"form":form})

def search(request, UserID = 0, searchTerm = ''):
    userData = 0
    if(UserID != 0):
        try:
            userData = User.objects.get(userID=UserID)
            if(userData.role == 0):
                messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
                userData.delete()
        except User.DoesNotExist:
            userData = 0
            items = Item.objects.filter(approved=True).order_by('name')[:20]
            return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})

    items = Item.objects.filter(approved=True)
    items = Item.objects.filter(Q(name__contains = searchTerm) | Q(category__contains = searchTerm))

    if(request.method == "POST"):
        if(request.POST.get("searchSubmit")):
            searchTerm = request.POST.get("search")
            if(searchTerm != ''):
                items = Item.objects.filter(Q(name__contains = searchTerm) | Q(category__contains = searchTerm))
                items = items.filter(approved=True)
            if(UserID == 0):
                return HttpResponseRedirect("/search/%s" % (searchTerm))
            else:
                return HttpResponseRedirect("/%i/search/%s" % (userData.userID,searchTerm))

        else:
            for item in items.all():
                if(request.POST.get("c" + str(item.itemID)) and UserID != 0):
                    if(userData.role == 1):
                        amount = request.POST.get("amount")

                        if(Cart.objects.filter(buyer=userData, item=item).exists()):
                            cartItem = Cart.objects.get(buyer=userData, item=item)
                            cartItem.amount = amount
                            cartItem.price = round(float(amount) * float(item.price), 2)
                            cartItem.save()
                        else:
                            newCartItem = Cart(buyer = userData, item=item, amount=amount)
                            newCartItem.price = round(float(amount) * float(item.price), 2)

                            newCartItem.save()
                        messages.add_message(request, messages.SUCCESS, f"{item} added to cart")

                    else:
                        messages.add_message(request, messages.SUCCESS, f"Must be buyer")


                
                    
    return render(request, "search.html", context={"items":items, "userData":userData, "searchTerm":searchTerm})

def login(request):
    if(request.method == 'POST'):
        form = Login(request.POST)

        form.full_clean()
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username = username, email=email, password=password).exists():
            user = User.objects.get(username = username, email=email, password=password)
            if user.role == 0:
                messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
                user.delete()
            else:
                return HttpResponseRedirect("/%i/main" % user.userID)
        else:
            messages.add_message(request, messages.SUCCESS, "Info invalid")


    else:
        form = Login(request.POST)
    return render(request, "login.html", {"form":form})

def createItem(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
    
    idIsValid = False
    if(request.method=="POST"):
        form = CreateNewItem(request.POST, request.FILES)
        if(form.is_valid()):
            form.full_clean()

            name = request.POST.get("name")
            category = request.POST.get("category")
            image = request.FILES.get("image")
            description = request.POST.get("description")
            price = request.POST.get("price")
            stock = request.POST.get("stock")
            newItem = Item(seller=userData, name=name, category=category, description=description, price=round(price, 2), stock=stock, image=image)
            while(not idIsValid):
                newItem.itemID = random.randint(0, 1000000000)
                try:
                    Item.objects.get(itemID=newItem.itemID)
                except Item.DoesNotExist:
                    idIsValid = True
            newItem.save()
            return HttpResponseRedirect("/%i/main" % userData.userID)
    else:
        form = CreateNewItem(request.POST)
        
    return render(request, "makeItem.html", context={"form":form, "userData":userData})

def authUsers(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
    
    users = User.objects.filter(approved=False)
    if request.method == "POST":
        if request.POST.get("save"):
            for user in users.all():
                if request.POST.get("a" + str(user.userID)) == "approved":
                    user.approved = True
                elif request.POST.get("r" + str(user.userID)) == "rejected":
                    user.role = 0
                user.save()

                    
        
    return render(request, "adminAuth.html", context={"users":users, "userData":userData})

def authItems(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
        
    items = Item.objects.filter(approved=False)
    if request.method == "POST":
        if request.POST.get("save"):
            for item in items.all():
                if request.POST.get("a" + str(item.itemID)) == "approved":
                    item.approved = True
                    item.save()

                elif request.POST.get("r" + str(item.itemID)) == "rejected":
                    item.price = 0
        
    return render(request, "adminAuth.html", context={"items":items, "userData":userData})

def viewProducts(request, UserID=0):
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})


    if(userData.role == 0):
        messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
        userData.delete()
    items = Item.objects.filter(seller=userData)
    for item in items.all():
        if item.price == 0:
            messages.add_message(request, messages.SUCCESS, f"{item.name}(ID: {item.itemID}) has been rejected by an admin")
            item.delete()
    items = Item.objects.filter(seller=userData)
     
    if request.method == "POST":
        if request.POST.get("save"):
            for item in items.all():
                name = request.POST.get("n" + str(item.itemID))
                description = request.POST.get("d" + str(item.itemID))
                category = request.POST.get("c" + str(item.itemID))
                stock = request.POST.get("s" + str(item.itemID))
                price = request.POST.get("p" + str(item.itemID))

                if name != "":
                    item.name = name
                if description != "":
                    item.description = description
                if category != "":
                    item.category = category
                if stock != '':
                    item.stock = stock
                if price != '':
                    item.price = round(price, 2)
                item.save()
                

    
    return render(request, "viewItems.html", context={"items":items, "userData":userData})

def viewCart(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
    

    idIsValid = False
    cart = Cart.objects.filter(buyer=userData)
    
    if(request.method == "POST"):
        orderID = 0
        if(request.POST.get("makeOrder")):

            order = Order(buyer=userData)
            while(not idIsValid):
                orderID = random.randint(0, 1000000000)
                try:
                    Order.objects.get(orderID=orderID)
                except Order.DoesNotExist:
                    idIsValid = True
            sum = 0
            for item in cart:
                sum += round(item.item.price * item.amount, 2)
                
            for item in cart:
                amount = request.POST.get("v" + str(item.id))

                if (userData.balance - sum) < 0:
                    messages.add_message(request, messages.SUCCESS, "You do not have enough money.")

                else:
                    if amount == '':
                        amount = item.amount
                    seller = User.objects.get(userID = item.item.seller.userID)
                    order = Order(orderID = orderID, item=item.item, buyer = userData,
                                   price=round(item.price, 2), amount=item.amount, totalPrice=round(sum, 2))
                    item.item.stock -= int(amount)
                    seller.balance += sum
                    userData.balance -= sum
                    
                    seller.balance = round(seller.balance, 2)
                    userData.balance = round(userData.balance, 2)

                    userData.save()
                    item.item.save()
                    seller.save()
                    order.save()
                    item.delete()
                
        else:
            for item in cart:
                amount = request.POST.get("v" + str(item.id))
 
                if amount == '':
                    pass
                elif int(amount) == 0:
                    item.delete()
                else:
                    print(amount)
                    item.amount = amount
                    item.price = round(float(item.amount) * float(item.item.price), 2)
                    item.save()
                    

    return render(request, "cart.html", context={"userData":userData, "cart":cart})
    
def viewOrders(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
        
    orderIDs = []
    if(userData.role == 0):
        messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
        userData.delete()

    orderItems = Order.objects.filter(buyer=userData)
    orders = []
    for item in orderItems.all():
        if(not item.orderID in orderIDs):
            orderIDs.append(item.orderID)
            orders.append(orderItems.filter(orderID=item.orderID))
    

    return render(request, "seeOrders.html", context={"userData":userData, "orders":orders})

def add_to_cart(request, UserID=0, itemID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})

    if userData.role != 1:
        messages.add_message(request, messages.SUCCESS, "Must be buyer to add to cart")
        return HttpResponseRedirect(f"/{UserID}/main")
    if request.method == "POST":
        item = Item.objects.get(itemID=itemID)
        amount = int(request.POST.get("amount", 1))
        price_val = round(float(amount) * float(item.price), 2)
        cartItem, created = Cart.objects.get_or_create(
            buyer=userData,
            item=item,
            defaults={'amount': amount, 'price': price_val}
        )
        if not created:
            cartItem.amount = amount
            cartItem.price = round(price_val, 2)
            cartItem.save()
        messages.add_message(request, messages.SUCCESS, f"{item.name} added to cart")
    return HttpResponseRedirect(f"/{UserID}/main")

def editAccount(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})

    if(userData.role == 0):
        messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
        userData.delete()
    if request.method == "POST":
        form = EditAccount(request.POST)

        if form.is_valid():
            form.full_clean()
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            add_money = request.POST.get("add_money")

            oldUsername = userData.username
            if username != "":
                userData.username = username
            if password != "":
                userData.password = password
            if email != "":
                userData.email = email
            if add_money != "":
                userData.balance += round(float(add_money), 2)

            if(User.objects.filter(username=username).exists() and username != oldUsername):
                messages.add_message(request, messages.SUCCESS, "Username taken")
                userData.username = oldUsername
            else:
                userData.save()
                return HttpResponseRedirect("/%i/main" % userData.userID)

    else:
        form = EditAccount(request.POST)
    
    return render(request, "editAccount.html", context = {"userData":userData, "form":form})

def sellerViewOrders(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
    
    itemSet = Item.objects.filter(seller=userData)
    order = [itemSet.count()]

    for item in itemSet.all():
        if(Order.objects.filter(item=item).exists()):
            set = Order.objects.filter(item=item)
            for orderItem in set:
                order.append(orderItem)
    


    return render(request, "seeOrders.html", context={"userData":userData, "order":order})

def monitorItems(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})

    sellers = []
    sellerItems = Item.objects.filter(approved=True)

    for item in sellerItems.all():
        if(not item.seller in sellers):
            sellers.append(sellerItems.filter(seller=item.seller))
    
    if request.method == "POST":
        if request.POST.get("save"):
            for item in sellerItems.all():
                if request.POST.get("r" + str(item.itemID)) == "remove":


                    item.price = 0
                print(item.name)

    return render(request, "adminMonitor.html", context={"userData":userData, "sellers":sellers})

def monitorUsers(request, UserID=0):
    userData = 0
    try:
        userData = User.objects.get(userID=UserID)
        if(userData.role == 0):
            messages.add_message(request, messages.SUCCESS, "This account was rejected by an admin. Please create a new account")
            userData.delete()
    except User.DoesNotExist:
        userData = 0
        items = Item.objects.filter(approved=True).order_by('name')[:20]
        return render(request, "index.html", {"userData": userData, "userID":UserID, "items":items})
    
    users = User.objects.filter(approved=True)

    if request.method == "POST":
        for user in users:
            if(request.POST.get("r" + str(user.userID)) == "remove"):
                user.role = 0
    
    return render(request, "adminMonitor.html", context={"userData":userData, "users":users})

def adminViewOrders(request, UserID=0):
    pass
