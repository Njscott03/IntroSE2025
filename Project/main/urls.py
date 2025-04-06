from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("<int:userID>/main", views.mainpage, name='mainpage'),
    path("search/", views.search, name="search")
]
