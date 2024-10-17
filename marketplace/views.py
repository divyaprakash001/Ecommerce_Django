from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product,Category

# Create your views here.
def marketplace(request):
  context={}
  products = Product.objects.filter(status='Active')
  context['products'] = products
  return render(request,"marketplace/shop.html",context)

def product_desc(request):
  context={
    'title':"Product Description"
  }
  return render(request,"marketplace/product_desc.html",context)