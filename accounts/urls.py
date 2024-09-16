from django.urls import path
from . import views

urlpatterns = [
    path("register-user", views.registerUser, name="registerUser"),
    path("register-seller", views.registerSeller, name="registerSeller"),

    path("login", views.login, name="login"),
]
