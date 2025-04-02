from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("main/<str:username>", views.mainpage, name="mainpage"),
    path("create/", views.create, name="create"),

]
