import base64
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.views import check_role_seller
from django.contrib.auth.decorators import login_required,user_passes_test

from products.models import Category, Product, Tags
from seller.models import Seller

@login_required(login_url='login')
@user_passes_test(check_role_seller)
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
    if (category_id != None and category_id != '') and (category_name != None and category_name != ''):
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

  
  # ajax part ********************************************************
  elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        try:
          seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
          messages.error(request,"You Are Not A Seller")
          return redirect("login")
        
        category_name = request.GET.get("category_name").strip()
        available = Category.objects.filter(category_name=category_name,seller=seller).exists()
        if available:
          return JsonResponse({"status":"found","message":"Already Exists!"})
        else:
          return JsonResponse({"status":"not found","message":"Not Exists!"})

  return render(request,"products/add_category.html",context)



@login_required(login_url='login')
@user_passes_test(check_role_seller)
def category_details(request):
  context={}
  try:
    seller = Seller.objects.get(user=request.user)
  except Seller.DoesNotExist:
    messages.error(request,"You are not a seller")
    return redirect("login")

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.method == 'POST':
      category_id = request.POST.get("category_id").strip()
      category_name = request.POST.get("category_name").strip()
      status = request.POST.get("category_status").strip()
      sort_by = request.POST.get("sort_by").strip()

      conditions={}
      if category_id != None and category_id != '':
        conditions['category_id'] = category_id
      if category_name != None and category_name != '':
        conditions['category_name'] = category_name
      if status != None and status != '':
        conditions['status'] = status


      my_data = Category.objects.filter(**conditions, seller=seller).order_by(sort_by) if conditions else Category.objects.filter(seller=seller).order_by(sort_by)
      if my_data.exists():
          items_per_page =10
          paginator = Paginator(my_data, items_per_page)
          page_number = request.POST.get('page', 1)
          page_obj = paginator.get_page(page_number)
          sno=1
          html_part = '<table class="table table-hover table-responsive table-striped" id="table1"><thead><tr><th>S.&nbsp;No.</th><th>Category&nbsp;ID</th><th>Category&nbsp;Name</th><th>Seller&nbsp;Name</th><th>Category&nbsp;Slug</th><th>Status</th><th align="center" colspan="5" >Action</th></tr> </thead> <tbody>'
          for sno, x in enumerate(page_obj,start=1 + (page_obj.number - 1) * items_per_page):
              # sno += 1
              html_part += f'<tr><td>{sno}</td>'
              html_part += f'<td id="category_id">{x.category_id}</td>'
              html_part += f'<td id="category_name">{x.category_name}</td>'
              html_part += f'<td id="seller_name">{x.seller.seller_name}</td>'
              html_part += f'<td id="category_slug">{x.category_slug}</td>'
              
              if x.status.lower() == 'active':
                  html_part += f'<td> <button id="statusButton" title="Active" class="btn btn-sm btn-success">Active</button></td>'
              elif x.status.lower() == 'inactive':
                  html_part += f'<td> <button id="statusButton" title="Inactive" class="btn btn-sm btn-danger">Inactive</button></td>'
              
              html_part += f'<td> <a title="Click on view to see more" class="view" ><i class="fa-solid fa-eye" style="color:blue;" ></i></a> </td>'
              html_part += f'<td> <a title="Edit" href="/categories-update/{base64.b64encode(str(x.category_id).encode()).decode()}/"><i class="fa-solid fa-pen" style="color:green;" ></i></a> </td>'
              if x.status.lower() == 'active':
                html_part += f'<td> <a title="Change Status")" ><i class="fa-solid fa-user" style="color:#56B6F7;"></i></a> </td>'
              elif x.status.lower() == 'inactive':
                html_part += f'<td> <a title="Change Status" onclick="changeStatus({base64.b64encode(str(x.category_id).encode()).decode()})" ><i class="fa-solid fa-user" style="color:red;"></i></a> </td>'
              html_part += f'<td> <a title="Delete" onclick="Delete(\'/categories-delete/{base64.b64encode(str(x.category_id).encode()).decode()}/\')" ><i class="fa-solid fa-trash" style="color:red;"></i></a> </td>'
              
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
    if request.method == 'GET':
      what = request.GET.get('what')
      category_id = request.GET.get('category_id')
      try:
        seller = Seller.objects.get(user=request.user)
      except Seller.DoesNotExist:
        messages.error(request,"You are not a Seller.")
        return redirect("login")

      if what == 'view_category':
        try:
          view_data = Category.objects.get(category_id=category_id, seller=seller)
          view_html=f'''<h4 class="card-title p-3">School Information :- </h4>
          <div class="row p-3">
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Seller ID : </div>
                      <div class="w-50"> {str(view_data.seller.id)}</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Seller Name : </div>
                      <div class="w-50"> {str(view_data.seller.seller_name)}</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category ID : </div>
                      <div class="w-50">{str(view_data.category_id)}</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category Name : </div>
                      <div class="w-50">{ str(view_data.category_name) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category Slug : </div>
                      <div class="w-50">{ str(view_data.category_slug) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category Desc : </div>
                      <div class="w-50">{ str(view_data.category_desc) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category Image : </div>
                      <div class="w-50">'''
          if view_data.category_pic:            
            view_html += f'''<img src='{view_data.category_pic.url}' alt="Category Pic" width='200' height='100' ></div>'''
          else:            
            view_html += '''Not Available'''
          view_html += '''</div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Status : </div>'''
          if view_data.status.lower() == 'active':
              view_html +=  f'''<div class="w-50"><button class="btn btn-sm btn-success text-white">{ str(view_data.status) }</button></div></div>'''
          elif view_data.status.lower() == 'pending':
              view_html +=  f'''<div class="w-50"><button class="btn btn-sm btn-warning text-white">{ str(view_data.status) }</button></div></div>'''
          elif view_data.status.lower() == 'inactive': 
              view_html +=  f'''<div class="w-50"><button class="btn btn-sm btn-danger text-white">{ str(view_data.status) }</button></div></div>'''
          
          response_data={
              "status":True,
              "view_html":view_html
          }
        except Category.DoesNotExist:        
            response_data={
                "status":False,
                "message":"Data does not exists!!!"
            }
        return JsonResponse(response_data,safe=False)
      elif what == 'changeStatus':
        try:
          category = Category.objects.get(category_id=category_id,seller=seller)
          if category.status.lower() == 'active':
            category.status = 'Inactive'
            category.save()
            response_data = {
              'status': True,
              'message': 'Category Status Changed to Inactive',
              'tags' : 'success',
              }
          elif category.status.lower() == 'inactive':
            category.status = 'Active'
            category.save()
            response_data = {
              'status': True,
              'message': 'Category Status Changed to Active',
              'tags' : 'success',
              }


        except Category.DoesNotExist:
          response_data = {
            'status': False,
            'tags' : 'error',
            'message': 'Category Not Found !',
          }
        
        return JsonResponse(response_data, safe=False)
    


  categories = seller.category.all().order_by("category_id")
  context['categories'] = categories
  return render(request,"products/search_category.html",context)



@login_required(login_url='login')
@user_passes_test(check_role_seller)
def update_category(request,iid):
  context = {}
  try:
    id = base64.b64decode(iid).decode('utf-8')
    category = Category.objects.get(category_id = id)
  except Category.DoesNotExist:
    category = None
    messages.error(request,"Category Does Not Exists!!")
  except:
    messages.error(request,"Somethings goes Wrong!!")

  context['category'] = category

  if request.method == 'POST':
    try:
      category_id = request.POST.get('category_id')
      category_name = request.POST.get('category_name')
      category_slug = request.POST.get('category_slug')
      category_status = request.POST.get('category_status')
      category_desc = request.POST.get("category_description")
      


      category.category_id = category_id
      if  category_name is not category.category_name:
        category.category_name = category_name
      category.category_slug = category_slug
      if "category_photo" in request.FILES:
        category_photo = request.FILES["category_photo"]
        category.category_pic = category_photo
      category.status = category_status
      category.category_desc = category_desc
      category.save()
      messages.success(request,"Category Updated Successfully!")
    except:
      messages.error(request,"Somethings goes Wrong!!")
    return redirect("categories_details")
                                                                               
  return render(request,"products/update_category.html",context)


@login_required(login_url='login')
@user_passes_test(check_role_seller)
def delete_category(request,iid):
  try:
    id = base64.b64decode(iid).decode('utf-8')
    seller = Seller.objects.get(user=request.user)
    category =  Category.objects.get(category_id = id,seller=seller)
    category.delete()
    messages.success(request,"Category Deleted Successfully!")
  except Seller.DoesNotExist:
    messages.error(request,"Seller Does Not Exists!!")
  except Category.DoesNotExist:
    messages.error(request,"Category Does Not Exists!!")
  except:
    messages.error(request,"Somethings goes Wrong!!")
  return redirect("categories_details")



@login_required(login_url='login')
@user_passes_test(check_role_seller)
def add_products(request):
  context={}
  try:
    seller = Seller.objects.get(user=request.user)
    categories = Category.objects.filter(seller=seller)
    tags = Tags.objects.filter(seller=seller)
    context["categories"] = categories
    context["tags"] = tags
  except Seller.DoesNotExist:
    messages.error(request,"Seller Does Not Exists!!")
    return redirect("login")
  except Category.DoesNotExist:
    messages.error(request,"Category Does Not Exists!!")
    return redirect("login")
  except Tags.DoesNotExist:
    messages.error(request,"Tags Does Not Exists!!")
    return redirect("login")
  
  # autogenerate
  prefix = 'P'
  last_product = Product.objects.filter(product_id__startswith=prefix).order_by('product_id').last()
  if last_product:
    last_id = int(last_product.product_id[1:])
    new_id = last_id + 1
    product_id = f"{prefix}{new_id:04d}"
  else:
    new_id = 1
    product_id = f"{prefix}{new_id:04d}"
  context['product_id'] = product_id

  try:
    if request.method == 'POST':
      product_name = request.POST.get('product_name')
      category_id = request.POST.get("category")
      brand = request.POST.get("brand")
      # product_slug = request.POST.get('product_slug')
      price = request.POST.get('price')
      discount = request.POST.get("discount")
      stock = request.POST.get("stock_quantity")
      sku = request.POST.get("sku")
      size = request.POST.get("size")
      color = request.POST.get("color")
      weight = request.POST.get("weight")
      material = request.POST.get("material")
      width = request.POST.get("width")
      height = request.POST.get("height")
      tags = request.POST.get("tags")
      product_desc = request.POST.get("product_desc")
      

      try:
        category = Category.objects.get(category_id=category_id)
      except Category.DoesNotExist:
        messages.error(request,"Category Does Not Exists!!")
      
      if "product_pic_front" in request.FILES:
        product_pic_front = request.FILES["product_pic_front"]
      else:
        product_pic_front = None

      if "product_pic_back" in request.FILES:
        product_pic_back = request.FILES["product_pic_back"]
      else:
        product_pic_back = None

      if "product_pic_third" in request.FILES:
        product_pic_third = request.FILES["product_pic_third"]
      else:
        product_pic_third = None

      if "product_pic_fourth" in request.FILES:
        product_pic_fourth = request.FILES["product_pic_fourth"]
      else:
        product_pic_fourth = None

      try:
        product = Product(seller=seller,category=category,product_id=product_id,product_name=product_name,brand=brand,price=price,discount=discount,stock_quantity=stock,sku=sku,color=color,size=size,weight=weight,material=material,width=width,height=height,tags=tags,product_desc=product_desc,product_pic_front=product_pic_front,product_pic_back=product_pic_back,product_pic_third=product_pic_third,product_pic_fourth=product_pic_fourth)
        product.save()
        if(Product.objects.filter(product_id=product_id,seller=seller)).exists():
          messages.success(request, "Product Added Successfully!!")
        else:
          messages.error(request, "Failed To Add Product!!")
      except:
        messages.error(request, "Failed To Add Product!!")
      return redirect("add_products")

  except:
    messages.error(request,"Somethings Went Wrong!!")

  return render(request,"products/add_products.html",context)

def products_details(request):
  return render(request,"products/products_details.html")

def add_order(request):
  return render(request,"products/add_order.html")