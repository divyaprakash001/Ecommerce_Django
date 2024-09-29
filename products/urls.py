from django.urls import path
from . import views

urlpatterns = [
    path('add-categories/', views.add_category, name="add_categories"),
    path('categories-details/', views.category_details, name="categories_details"),
    path('add-products/', views.add_products, name="add_products"),
    path('products-details/', views.products_details, name="products_details"),

    path('add-order/', views.add_order, name="add_order"),
]
