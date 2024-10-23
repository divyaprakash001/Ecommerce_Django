from django.shortcuts import render
from products.models import Product,Category

def home(request):
  context={
    'title':"Home | Asha Fashion"
  }
  products = Product.objects.filter(status='Active').order_by("created_at")[:12]
  categories = Category.objects.filter(status='Active').order_by("created_at")
  print(categories[1])
  context['products'] = products
  context['categories'] = categories
  return render(request,"index.html", context)