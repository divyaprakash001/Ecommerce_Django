from django.shortcuts import render

def add_category(request):
  if request.method == 'POST':
    category_id = request.POST.get("category_id")
    category_name = request.POST.get("category_name")
    category_slug = request.POST.get("category_slug")
    category_desc = request.POST.get("category_desc")
    category_photo = request.FILES["category_photo"]

    print(category_photo)
  
  elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        username = request.GET.get("username").strip()
        # available = User.objects.filter(username=username).exists()
        # if available:
          # return JsonResponse({"status":"found","message":"Already Exists!"})
        # else:
          # return JsonResponse({"status":"not found","message":"Not Exists!"})

  return render(request,"products/add_category.html")

def category_details(request):
  return render(request,"products/search_category.html")


def add_products(request):
  return render(request,"products/add_products.html")

def products_details(request):
  return render(request,"products/products_details.html")

def add_order(request):
  return render(request,"products/add_order.html")