from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name="marketplace"),
    path('<str:category_name>', views.shop_by_category, name="shop_by_category"),



    path('product/<iid>/', views.product_desc, name="product_desc"),

    # add to cart
    path('add_to_cart/<product_id>/', views.add_to_cart, name="add_to_cart"),
    path('decrease_cart/<product_id>/', views.decrease_cart, name="decrease_cart"),
    path('delete-from-cart/<cart_id>/', views.delete_from_cart, name="delete_from_cart"),


    path('shopping-cart/', views.shopping_cart,name="shopping_cart"),
]
