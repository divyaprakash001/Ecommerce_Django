from django.urls import path
from . import views

urlpatterns = [
    path("register-user", views.registerUser, name="registerUser"),
    path("register-seller", views.registerSeller, name="registerSeller"),

    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    path("myAccount", views.myAccount, name="myAccount"),
    path("customerDashboard", views.customerDashboard, name="customerDashboard"),
    path("sellerDashboard", views.sellerDashboard, name="sellerDashboard"),

    # path("dashboard", views.dashboard, name="dashboard"),
    path("access-denied",views.access_denied,name="access_denied")
]
