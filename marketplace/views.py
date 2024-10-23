import base64
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Cart
from products.models import Product,Category
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.core.paginator import Paginator

# Create your views here.
def marketplace(request):
  context={}
  products = Product.objects.filter(status='Active')

  paginator = Paginator(products, 10)  # Show 10 products per page
  page_number = request.GET.get('page')  # Get the page number from the request
  page_obj = paginator.get_page(page_number)

  context['page_obj'] = page_obj
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


# @login_required(login_url='login')
def add_to_cart(request,product_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        what = request.GET.get("what")
        if what == "by_marketplace":
          try:
            prod_id =  base64.b64decode(product_id).decode('utf-8')
            product = Product.objects.get(product_id=prod_id)
            cart_val = request.GET.get("cart_val")
            # check product is already in the cart or not
            try:
              cart = Cart.objects.get(user=request.user,product=product)
              cart.quantity += int(cart_val)
              cart.save()
              
              total_price = cart.product.discounted_price() * cart.quantity
              
              return JsonResponse({'status':"Success",'message':'Cart Updated Successfully.','cart_counter':get_cart_counter(request),"total_price":total_price})
            except Cart.DoesNotExist:
              cart = Cart(user=request.user,product=product,quantity=int(cart_val))
              cart.save()
              
              return JsonResponse({'status':"Success",'message':'Added To Cart Successfully.','cart_counter':get_cart_counter(request)})
          except Product.DoesNotExist:
            return JsonResponse({'status':"Failed",'message':'Product Doee Not Exists!!'})
          except Exception as e:
            return JsonResponse({'status':"Failed",'message':'Some Error Occurs!!',"error":f"{e}"})
        elif  what == "by_shopping_cart":
          try:
            prod_id =  base64.b64decode(product_id).decode('utf-8')
            product = Product.objects.get(product_id=prod_id)
            cart_val = request.GET.get("cart_val")
          # check product is already in the cart or not
            try:
              cart = Cart.objects.get(user=request.user,product=product)
              cart.quantity += 1
              cart.save()
              total_price = cart.product.discounted_price() * cart.quantity
              
              return JsonResponse({'status':"Success",'message':'Cart Updated Successfully.','cart_counter':get_cart_counter(request),"total_price":total_price,'get_cart_amounts':get_cart_amounts(request)})
            except Cart.DoesNotExist:
              cart = Cart(user=request.user,product=product,quantity=1)
              cart.save()
              
              return JsonResponse({'status':"Success",'message':'Added To Cart Successfully.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
          except Product.DoesNotExist:
            return JsonResponse({'status':"Failed",'message':'Product Dose Not Exists!!'})
          except Exception as e:
            return JsonResponse({'status':"Failed",'message':'Some Error Occurs!!',"error":f"{e}"})



          
    else:
      return JsonResponse({'status':"Failed",'message':'Invalid Request'})
    return JsonResponse({'status':"Success",'message':'Yeah'})
      
    
  else:  
    return JsonResponse({'status':"Login Required",'message':'Login Required'})


def decrease_cart(request,product_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        try:
          prod_id =  base64.b64decode(product_id).decode('utf-8')
          product = Product.objects.get(product_id=prod_id)
          # cart_val = request.GET.get("cart_val")
        # check product is already in the cart or not
          try:
            cart = Cart.objects.get(user=request.user,product=product)
            if cart.quantity > 1:
              cart.quantity -= 1
              cart.save()
              total_price = cart.product.discounted_price() * cart.quantity
              return JsonResponse({'status':"Success",'message':'Cart Decreased Successfully.','cart_counter':get_cart_counter(request),"total_price":total_price,'get_cart_amounts':get_cart_amounts(request)})
            elif cart.quantity == 1:
              cart.delete()
              cart.quantity == 0
              return JsonResponse({'status':"Removed",'message':'Product Removed Successfully.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
            else:
              return JsonResponse({'status':"Failed",'message':'Could Not Be Zero.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
          except Cart.DoesNotExist:
            cart = Cart(user=request.user,product=product,quantity=1)
            cart.save()
            
            return JsonResponse({'status':"Success",'message':'Added To Cart Successfully.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
        except Product.DoesNotExist:
          return JsonResponse({'status':"Failed",'message':'Product Dose Not Exists!!'})
        except Exception as e:
          return JsonResponse({'status':"Failed",'message':'Some Error Occurs!!',"error":f"{e}"})    
    else:
      return JsonResponse({'status':"Failed",'message':'Invalid Request'})
  else:
    return JsonResponse({'status':"Login Required",'message':'Login Required'})


  
login_required(login_url="login")
def shopping_cart(request):
  context={}
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
    context['cart_items'] = cart_items
  else:
    return redirect("login")
  return render(request,"marketplace/shopping_cart.html",context)


def delete_from_cart(request,cart_id=None):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        try:
          cart = Cart.objects.get(user=request.user,id=cart_id)
          if cart:
            cart.delete()
            total_price = cart.product.discounted_price() * cart.quantity
            return JsonResponse({'status':"Deleted",'message':'Product Deleted From Cart.','cart_counter':get_cart_counter(request),"total_price":total_price,'get_cart_amounts':get_cart_amounts(request)})
          else:
            return JsonResponse({'status':"Not Found",'message':'Product Not Found In Cart.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})
        except Cart.DoesNotExist:
          return JsonResponse({'status':"Not Found",'message':'Product Not Found In Cart.','cart_counter':get_cart_counter(request),'get_cart_amounts':get_cart_amounts(request)})   
    else:
      return JsonResponse({'status':"Failed",'message':'Invalid Request'})
  else:
    return JsonResponse({'status':"Login Required",'message':'Login Required'})


def shop_by_category(request,category_name):
  context={}
  try:
    category = Category.objects.filter(category_name=category_name)
  except Category.DoesNotExist:
    messages.error(request,"Category Does not exists")
    return redirect("home_page")
  products = Product.objects.filter(category__in=category,status='Active')
  paginator = Paginator(products, 10)  # Show 10 products per page
  page_number = request.GET.get('page')  # Get the page number from the request
  page_obj = paginator.get_page(page_number)
  context['page_obj'] = page_obj
  return render(request,"marketplace/shop_by_category.html",context)