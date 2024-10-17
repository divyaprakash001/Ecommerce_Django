import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from products.models import Product,Category
from django.contrib import messages

# Create your views here.
def marketplace(request):
  context={}
  products = Product.objects.filter(status='Active')
  context['products'] = products
  return render(request,"marketplace/shop.html",context)

def product_desc(request,iid):
  context={
    'title':"Product Description"
  }

  try:
    product_id =  base64.b64decode(iid).decode('utf-8')
    product  = Product.objects.get(product_id=product_id)
    context['product'] = product

    related_products = Product.objects.filter(category = product.category).order_by('updated_at')[:4]
    context['related_products'] = related_products

  except (ValueError, TypeError):
    messages.error(request,"Product Id Is Invalid!!!")
  except Product.DoesNotExist:
    messages.error(request,"Product Does Not Exists!!!")

  return render(request,"marketplace/product_desc.html",context)