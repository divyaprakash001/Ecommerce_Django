from django.shortcuts import render
from products.models import Product

def home(request):
  context={
    'title':"Home | Asha Fashion"
  }
  products = Product.objects.filter(status='Active').order_by("created_at")[:12]
  context['products'] = products
  return render(request,"index.html", context)