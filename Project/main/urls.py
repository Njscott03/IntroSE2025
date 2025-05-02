from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("<int:userID>/main", views.mainpage, name='mainpage'),
    path("search/", views.search, name="search"),
    path("search/<str:searchTerm>", views.search, name="search2"),
    path("login/", views.login, name="login"),
    path("auth/users", views.authUsers, name="authUsers"),
    path("auth/items", views.authItems, name="authItems"),
    path("sell/makeItem", views.createItem, name="createItem"),
    path("sell/items", views.viewProducts, name="sellView"),
    path("sell/orders", views.sellerViewOrders, name="sellOrders"),
    path("buy/cart", views.viewCart, name="viewCart"),
    path("buy/orders", views.viewOrders, name="viewOrders"),
    path("<int:UserID>/add_to_cart/<int:itemID>/", views.add_to_cart, name="add_to_cart"),
    path("<int:UserID>/edit", views.editAccount, name="edit"),
    path("auth/monitorItems", views.monitorItems, name="monItems"),
    path("auth/monitorUsers", views.monitorUsers, name="monUsers"),
    path("auth/orders", views.adminViewOrders, name="adminOrders")
]
