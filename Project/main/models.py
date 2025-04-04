from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.SmallIntegerField() #0 = no account 1 = buyer 2 = seller 3 = admin
    balance = models.BigIntegerField(default=0)
    approved = models.BooleanField(default=False)
    
class Item(models.Model):
    category = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added=models.DateField()
    approved = models.BooleanField(default=False)

    
class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_bought=models.DateField()
    status = models.CharField(max_length=50)
    totalAmount = models.FloatField(default=0.0)



    
    
    