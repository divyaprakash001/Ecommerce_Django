from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.myAccount, name="myAccount"),
    path("register-user", views.registerUser, name="registerUser"),
    path("register-seller", views.registerSeller, name="registerSeller"),

    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forget-password', views.forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path("myAccount", views.myAccount, name="myAccount"),
    path("customerDashboard", views.customerDashboard, name="customerDashboard"),
    path("sellerDashboard", views.sellerDashboard, name="sellerDashboard"),

    # path("dashboard", views.dashboard, name="dashboard"),
    path("access-denied",views.access_denied,name="access_denied"),

    path("seller/", include('seller.urls')),
]
