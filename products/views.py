import base64
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator

from products.models import Category
from seller.models import Seller

def add_category(request):
  context={}
  prefix = 'C'
  last_category = Category.objects.filter(category_id__startswith=prefix).order_by('category_id').last()
  if last_category:
    last_id = int(last_category.category_id[1:])
    new_id = last_id + 1
    category_id = f"{prefix}{new_id:04d}"
    pass
  else:
    new_id = 1
    category_id = f"{prefix}{new_id:04d}"
  context['category_id'] = category_id

  if request.method == 'POST':
    category_name = request.POST.get("category_name")
    category_slug = request.POST.get("category_slug")
    category_desc = request.POST.get("category_description")
    if "category_photo" in request.FILES:
      category_photo = request.FILES["category_photo"]
    else:
      category_photo = None

    try:
      seller = Seller.objects.get(user = request.user)
    except Seller.DoesNotExist:
      messages.error(request, "You are not a seller")
      return redirect("add_category")
    if (category_id is not None and category_id is not '') and (category_name is not None and category_name is not ''):
      cat = Category(seller=seller,category_id=category_id,category_name=category_name,category_slug=category_slug,category_desc=category_desc,category_pic=category_photo)
      cat.save()
      try:
        if Category.objects.filter(category_id=category_id).exists():
          messages.success(request,"Category Added Successfully.")
        else:
          messages.error(request,"Failed To Add Category!")
      except Category.DoesNotExist:
        messages.error(request,"Failed To Add Category!")
    else:
      messages.error(request,"Please Fill All Required Fields!")
    return redirect("add_categories")

  
  elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        username = request.GET.get("username").strip()
        available = Category.objects.filter(category_name=category_name).exists()
        # if available:
          # return JsonResponse({"status":"found","message":"Already Exists!"})
        # else:
          # return JsonResponse({"status":"not found","message":"Not Exists!"})

  return render(request,"products/add_category.html",context)

def category_details(request):
  try:
    seller = Seller.objects.get(user=request.user)
  except Seller.DoesNotExist:
    messages.error(request,"You are not a seller")
    return redirect("login")

  context={}
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.method == 'POST':
      category_id = request.POST.get("category_id").strip()
      category_name = request.POST.get("category_name").strip()

      print(category_id)
      print(category_name)

      conditions={}
      if category_id is not None and category_id is not '':
          conditions['category_id'] = category_id
      if category_name is not  None and category_name is not '':
          conditions['category_name'] = category_name

      print(conditions)

      my_data = Category.objects.filter(**conditions, seller=seller).order_by("category_id") if conditions else Category.objects.filter(seller=seller).order_by("category_id")
      print(my_data)
      if my_data.exists():
          items_per_page =10
          paginator = Paginator(my_data, items_per_page)
          page_number = request.POST.get('page', 1)
          page_obj = paginator.get_page(page_number)
          sno=1
          html_part = '<table class="table table-hover table-responsive table-striped" id="table1"><thead><tr><th>S.&nbsp;No.</th><th>Category&nbsp;ID</th><th>Category&nbsp;Name</th><th>Seller&nbsp;Name</th><th>Category&nbsp;Slug</th><th>Image</th><th>Status</th><th align="center" colspan="5" >Action</th></tr> </thead> <tbody>'
          for sno, x in enumerate(page_obj,start=1 + (page_obj.number - 1) * items_per_page):
              # sno += 1
              html_part += f'<tr><td>{sno}</td>'
              html_part += f'<td id="branch_id">{x.category_id}</td>'
              html_part += f'<td id="school_name">{x.category_name}</td>'
              html_part += f'<td id="school_name">{x.seller.seller_name}</td>'
              html_part += f'<td id="role_id">{x.category_slug}</td>'
              html_part += f'<td> <a title="Click on view to see more" class="view" ><i class="fa-solid fa-eye" style="color:blue;" ></i></a> </td>'
              if x.status.lower() == 'active':
                  html_part += f'<td> <button title="Active" class="btn btn-sm btn-success">Active</button></td>'
              elif x.status.lower() == 'inactive':
                  html_part += f'<td> <button title="Inactive" class="btn btn-sm btn-danger">Inactive</button></td>'

              html_part += f'<td> <a title="Edit" href="/categories-update/{base64.b64encode(str(x.category_id).encode()).decode()}/"><i class="fa-solid fa-pen" style="color:green;" ></i></a> </td>'
              # html_part += f'<td> <a title="Change Status" onclick="changeStatus({base64.b64encode(str(x.role_id).encode()).decode()})" ><i class="fa-solid fa-user" style="color:#56B6F7;"></i></a> </td>'
              # html_part += f'<td> <a title="Delete" onclick="Delete(\'/privilege-delete/{base64.b64encode(str(x.role_id).encode()).decode()}/\')" ><i class="fa-solid fa-trash" style="color:red;"></i></a> </td>'
              
              html_part += f'</tr>'                        
          response_data = {   
              'status': True,
              'html_part' : html_part,
              'has_next': page_obj.has_next(),
              'has_previous': page_obj.has_previous(),
              'current_page': page_obj.number,
              'total_pages': paginator.num_pages,
            }
      else:
          response_data = {
                'status': False,
                'tags' : 'error',
                'message': 'No Record Available !',
                'html_part' : '<div class="alert text-white text-black fs-5 rounded font-bold" style="background-color:#56B6F7;"> No Record Available ! </div>'
        }
    
    return JsonResponse(response_data, safe=False)


  categories = Category.objects.all().order_by("category_id")
  context['categories'] = categories
  return render(request,"products/search_category.html",context)

def update_category(request,iid):
  context = {}
  id = base64.b64decode(iid).decode('utf-8')
  category = Category.objects.get(category_id = id)
  context['category'] = category
  if request.method == 'POST':
    category_id = request.POST.get('category_id')
    category_name = request.POST.get('category_name')
    category_slug = request.POST.get('category_slug')
    category_status = request.POST.get('category_status')
    category_desc = request.POST.get("category_description")
    if "category_photo" in request.FILES:
        category_photo = request.FILES["category_photo"]
    else:
      category_photo = None

    category.category_id = category_id
    category.category_name = category_name
    category.category_pic = category_photo
    category.status = category_status
    category.category_desc = category_desc
    category_desc.save()
    messages.success(request,"Category Updated Successfully!")
    return redirect("category_details")


                                                                                   



  # category = Category.objects.get(category_id = id)
  # context['category'] = category
  return render(request,"products/update_category.html",context)


def add_products(request):
  return render(request,"products/add_products.html")

def products_details(request):
  return render(request,"products/products_details.html")

def add_order(request):
  return render(request,"products/add_order.html")