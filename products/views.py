from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from products.models import Category

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
    category_desc = request.POST.get("category_desc")
    category_photo = request.FILES["category_photo"]


    cat = Category(category_id=category_id,category_name=category_name,category_slug=category_slug,category_desc=category_desc,category_pic=category_photo)
    cat.save()
    try:
      if Category.objects.filter(category_id=category_id).exists():
        messages.success(request,"Category Added Successfully.")
      else:
        messages.error(request,"Failed To Add Category!")
    except Category.DoesNotExist:
      messages.error(request,"Failed To Add Category!")
    return redirect("add_categories")

  
  elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        username = request.GET.get("username").strip()
        # available = User.objects.filter(username=username).exists()
        # if available:
          # return JsonResponse({"status":"found","message":"Already Exists!"})
        # else:
          # return JsonResponse({"status":"not found","message":"Not Exists!"})

  return render(request,"products/add_category.html",context)

def category_details(request):
  context={}
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.method == 'POST':
      category_id = request.POST.get("category_id").strip()
      category_name = request.POST.get("category_name").strip()

      conditions={}
      if category_id != None or category_id != '':
          conditions['category_id'] = category_id
      if category_name != None or category_name != '':
          conditions['category_name'] = category_name

      if conditions:
        my_data = Category.objects.filter(**conditions)

        if my_data.exists():
          sno=0
          html_part = '<table class="table table-hover table-responsive table-striped" id="table1"><thead><tr><th>S.&nbsp;No.</th><th>Category&nbsp;ID</th><th>Category&nbsp;Name</th><th>Seller&nbsp;Name</th><th>Category&nbsp;Slug</th><th>Image</th><th>Status</th><th align="center" colspan="5" >Action</th></tr> </thead> <tbody>'
          for x in my_data:
              sno += 1
              html_part += '<tr><td>' + str(sno) + '</td>'
              html_part += '<td id="branch_id">' + str(x.category_id) + '</td>'
              html_part += '<td id="school_name">' + str(x.category_name) + '</td>'
              html_part += '<td id="role_id">' + str(x.category_slug) + '</td>'
              html_part += '<td>' + str(x.role_name) + '</td>'
              html_part += f'<td> <a title="Click on view to see more" class="view" ><i class="fa-solid fa-eye" style="color:blue;" ></i></a> </td>'
              if x.status.lower() == 'active':
                  html_part += f'<td> <button title="Active" class="btn btn-sm btn-success">Active</button></td>'
              elif x.status.lower() == 'inactive':
                  html_part += f'<td> <button title="Inactive" class="btn btn-sm btn-danger">Inactive</button></td>'

              # html_part += f'<td> <a title="Edit" href="/privilege-update/{base64.b64encode(str(x.role_id).encode()).decode()}/"><i class="fa-solid fa-pen" style="color:green;" ></i></a> </td>'
              # html_part += f'<td> <a title="Change Status" onclick="changeStatus({base64.b64encode(str(x.role_id).encode()).decode()})" ><i class="fa-solid fa-user" style="color:#56B6F7;"></i></a> </td>'
              # html_part += f'<td> <a title="Delete" onclick="Delete(\'/privilege-delete/{base64.b64encode(str(x.role_id).encode()).decode()}/\')" ><i class="fa-solid fa-trash" style="color:red;"></i></a> </td>'
              
              html_part += f'</tr>'                        
          response_data = {   
              'status': True,
              'html_part' : html_part
          }
        else:
          response_data = {
                'status': False,
                'tags' : 'error',
                'message': 'No Record Available !',
                'html_part' : '<div class="alert text-white text-black fs-5 rounded font-bold" style="background-color:#56B6F7;"> No Record Available ! </div>'
        }
      else:
        response_data = {
          'status': False,
          'tags' : 'info',
          'message': 'Please Select Any Condtion !',
          'html_part' : '<div class="alert text-white text-black fs-5 rounded font-bold" style="background-color:#56B6F7;"> Search To See The Records ! </div>'
        }
    return JsonResponse(response_data, safe=False)


  categories = Category.objects.all().order_by("category_id")
  context['categories'] = categories
  return render(request,"products/search_category.html",context)


def add_products(request):
  return render(request,"products/add_products.html")

def products_details(request):
  return render(request,"products/products_details.html")

def add_order(request):
  return render(request,"products/add_order.html")