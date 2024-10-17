from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name="marketplace"),
    path('marketplace/<pk>/', views.product_desc, name="product_desc"),
]
