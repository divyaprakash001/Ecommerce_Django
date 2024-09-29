from django.shortcuts import render

def add_category(request):
  return render(request,"products/add_category.html")

def category_details(request):
  return render(request,"products/search_category.html")


def add_products(request):
  return render(request,"products/add_products.html")

def products_details(request):
  return render(request,"products/products_details.html")

def add_order(request):
  return render(request,"products/add_order.html")