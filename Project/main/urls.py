from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("<int:userID>/main", views.mainpage, name='mainpage'),
    path("search/", views.search, name="search"),
    path("login/", views.login, name="login"),
    path("auth/users", views.authUsers, name="authUsers"),
    path("auth/items", views.authItems, name="authItems"),
    path("sell/makeItem", views.createItem, name="createItem"),
    path("sell/items", views.viewProducts, name="createItem"),
    path("buy/cart", views.viewCart, name="viewCart"),
    path("buy/orders", views.viewOrders, name="viewCart")

]
