from django.db import models

# Create your models here.
class User(models.Model):
    userID = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.SmallIntegerField()
    balance = models.FloatField(default=0)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Item(models.Model):
    itemID = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='main/static/images', default=0)
    description = models.CharField(max_length=300)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added=models.DateField()
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

    
class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_bought=models.DateField()
    status = models.CharField(max_length=50)
    totalAmount = models.FloatField(default=0.0)



    
    
    