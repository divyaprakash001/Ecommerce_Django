import base64
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.views import check_role_seller
from django.contrib.auth.decorators import login_required,user_passes_test
# from django.db.models import Q, FloatField
# from django.db.models.functions import Cast
from products.models import Category, Product, Tags
from seller.models import Seller
# from django.db import connection

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
    category_name = request.POST.get("category_name").strip()
    category_slug = request.POST.get("category_slug").strip()
    category_desc = request.POST.get("category_description").strip()
    if "category_photo" in request.FILES:
      category_photo = request.FILES["category_photo"]
    else:
      category_photo = None

    try:
      seller = Seller.objects.get(user = request.user)
    except Seller.DoesNotExist:
      messages.error(request, "You are not a seller")
      return redirect("login")
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
      category_id = request.POST.get('category_id').strip()
      category_name = request.POST.get('category_name').strip()
      category_slug = request.POST.get('category_slug').strip()
      category_status = request.POST.get('category_status').strip()
      category_desc = request.POST.get("category_description").strip()
      


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
      product_name = request.POST.get('product_name').strip()
      category_id = request.POST.get("category").strip()
      brand = request.POST.get("brand").strip()
      # product_slug = request.POST.get('product_slug')
      price = request.POST.get('price').strip()
      discount = request.POST.get("discount").strip()
      stock = request.POST.get("stock_quantity").strip()
      sku = request.POST.get("sku").strip()
      size = request.POST.get("size").strip()
      color = request.POST.get("color").strip()
      weight = request.POST.get("weight").strip()
      material = request.POST.get("material").strip()
      width = request.POST.get("width").strip()
      height = request.POST.get("height").strip()
      tags = request.POST.get("tags").strip()
      product_desc = request.POST.get("product_desc").strip()
      

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
        product = Product(seller=seller,category=category,product_id=product_id,product_name=product_name,brand=brand.capitalize(),price=price,discount=discount,stock_quantity=stock,sku=sku,color=color.capitalize(),size=size,weight=weight,material=material.capitalize(),width=width,height=height,tags=tags,product_desc=product_desc.capitalize(),product_pic_front=product_pic_front,product_pic_back=product_pic_back,product_pic_third=product_pic_third,product_pic_fourth=product_pic_fourth)
        product.save()
        if(Product.objects.filter(product_id=product_id,seller=seller)).exists():
          messages.success(request, "Product Added Successfully!!")
        else:
          messages.error(request, "Failed To Add Product!!")
      except Exception as e:
        print(e)
        messages.error(request, f"Failed To Add Product!!")
      return redirect("add_products")

# ajax part
    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        try:
          seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
          messages.error(request,"You Are Not A Seller")
          return redirect("login")
        
        product_name = request.GET.get("product_name").strip()
        # available = Product.objects.filter(product_name=product_name,seller=seller).exists()
        products = Product.objects.filter(seller=seller).values_list("product_name",flat=True)
        product_exists=False
        for product in products:
            if product_name.lower() == product.lower():
                product_exists = True
                
        if product_exists:
          return JsonResponse({"status":"found","message":"Already Exists!"})
        else:
          return JsonResponse({"status":"not found","message":"Not Exists!"})
  except:
    messages.error(request,"Somethings Went Wrong!!")


  return render(request,"products/add_products.html",context)

def products_details(request):
  context={}
  seller = None
  try:
    seller = Seller.objects.get(user=request.user)
  except Seller.DoesNotExist:
    seller = None
    messages.error(request,"You are not a Seller.")
    return redirect("login")

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.method == 'POST':
      product_id = request.POST.get("product_id").strip()
      product_name = request.POST.get("product_name").strip()
      brand = request.POST.get("brand").strip()
      category_id = request.POST.get("category").strip()
      stock_quantity = request.POST.get("stock_quantity").strip()
      size = request.POST.get("size").strip()
      color = request.POST.get("color").strip()
      weight = request.POST.get("weight").strip()
      material = request.POST.get("material").strip()
      min_price = request.POST.get("min_price").strip()
      max_price = request.POST.get("max_price").strip()
      sort_by = request.POST.get("sort_by").strip()

      conditions = {}
      if product_id != None and product_id != '':
        conditions['product_id'] = product_id

      if product_name != None and product_name != '':
        conditions['product_name'] = product_name

      if brand != None and brand != '':
        conditions['brand'] = brand
      
      if category_id != None and category_id != '':
        conditions['category__category_id'] = category_id
      
      if stock_quantity != None and stock_quantity != '':
        conditions['stock_quantity__lte'] = stock_quantity
      
      if size != None and size != '':
        conditions['size'] = size
        
      if color != None and color != '':
        conditions['color'] = color

      if weight != None and weight != '':
        conditions['weight__lte'] = weight

      if material != None and material != '':
        conditions['material'] = material

      if min_price != None and min_price != '':
        print(type(float(min_price)))
        conditions['price__gte'] = float(min_price)

      if max_price != None and max_price != '':
        conditions['price__lte'] = float(max_price)


      my_data = (Product.objects.filter(**conditions,seller=seller).order_by(sort_by) if conditions else Product.objects.filter(seller=seller).order_by(sort_by))
      # print(my_data.query)
      # print(connection.queries)
      if my_data.exists():
          items_per_page =10
          paginator = Paginator(my_data, items_per_page)
          page_number = request.POST.get('page', 1)
          page_obj = paginator.get_page(page_number)
          sno=1
          html_part = '<table class="table table-hover table-responsive table-striped" id="table1"><thead><tr><th>S.&nbsp;No.</th><th>Product&nbsp;ID</th><th>Product&nbsp;Name</th><th>Seller&nbsp;Name</th><th>Category</th><th>Brand</th><th>Stock&nbsp;Quantity</th><th>Status</th><th align="center" colspan="5" >Action</th></tr> </thead> <tbody>'
          for sno, x in enumerate(page_obj,start=1 + (page_obj.number - 1) * items_per_page):
              # sno += 1
              html_part += f'<tr><td>{sno}</td>'
              html_part += f'<td id="product_id">{x.product_id}</td>'
              html_part += f'<td id="product_name">{x.product_name}</td>'
              html_part += f'<td id="seller_name">{x.seller.seller_name}</td>'
              html_part += f'<td id="category_slug">{x.category}</td>'
              html_part += f'<td id="category_slug">{x.brand}</td>'
              html_part += f'<td id="category_slug">{x.stock_quantity}</td>'
              
              if x.status.lower() == 'active':
                  html_part += f'<td> <button id="statusButton" title="Active" class="btn btn-sm btn-success">Active</button></td>'
              elif x.status.lower() == 'inactive':
                  html_part += f'<td> <button id="statusButton" title="Inactive" class="btn btn-sm btn-danger">Inactive</button></td>'
              
              html_part += f'<td> <a title="Click on view to see more" class="view" ><i class="fa-solid fa-eye" style="color:blue;" ></i></a> </td>'
              html_part += f'<td> <a title="Edit" href="/product-update/{base64.b64encode(str(x.product_id).encode()).decode()}/"><i class="fa-solid fa-pen" style="color:green;" ></i></a> </td>'
              if x.status.lower() == 'active':
                html_part += f'<td> <a title="Change Status")" ><i class="fa-solid fa-user" style="color:#56B6F7;"></i></a> </td>'
              elif x.status.lower() == 'inactive':
                html_part += f'<td> <a title="Change Status"  ><i class="fa-solid fa-user" style="color:red;"></i></a> </td>'
              html_part += f'<td> <a title="Delete" onclick="Delete(\'/product-delete/{base64.b64encode(str(x.product_id).encode()).decode()}/\')" ><i class="fa-solid fa-trash" style="color:red;"></i></a> </td>'
              
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
      what = request.GET.get('what').strip()
      product_id = request.GET.get('product_id').strip()
      try:
        seller = Seller.objects.get(user=request.user)
      except Seller.DoesNotExist:
        messages.error(request,"You are not a Seller.")
        return redirect("login")

      if what == 'view_product':
        try:
          view_data = Product.objects.get(product_id=product_id, seller=seller)
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
                      <div class="w-50 fw-bold">Product ID : </div>
                      <div class="w-50">{str(view_data.product_id)}</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Product Name : </div>
                      <div class="w-50">{ str(view_data.product_name) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Brand Name : </div>
                      <div class="w-50">{ str(view_data.brand) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Category : </div>
                      <div class="w-50">{ str(view_data.category.category_name) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Original Price : </div>
                      <div class="w-50">{ str(view_data.price) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Disounted Price : </div>
                      <div class="w-50">{ str(float(view_data.price) - (float(view_data.price) * (view_data.discount / 100))) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Stock Quantity : </div>
                      <div class="w-50">{ str(view_data.stock_quantity) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">SKU : </div>
                      <div class="w-50">{ str(view_data.sku) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Size : </div>
                      <div class="w-50">{ str(view_data.size) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Color : </div>
                      <div class="w-50">{ str(view_data.color) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Weight : </div>
                      <div class="w-50">{ str(view_data.weight) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Material : </div>
                      <div class="w-50">{ str(view_data.material) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Dimension : </div>
                      <div class="w-50">{ str(view_data.width) } X {str(view_data.height)}</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Tag : </div>
                      <div class="w-50">{ str(view_data.tags) }</div>
                  </div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Front Image : </div>
                      <div class="w-50">'''
          if view_data.product_pic_front:            
            view_html += f'''<img src='{view_data.product_pic_front.url}' alt="Product Front Pic" width='200' height='100' ></div>'''
          else:            
            view_html += '''Not Available'''
          view_html += '''</div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Back Image : </div>
                      <div class="w-50">'''
          if view_data.product_pic_back:            
            view_html += f'''<img src='{view_data.product_pic_back.url}' alt="Product Front Pic" width='200' height='100' ></div>'''
          else:            
            view_html += '''Not Available'''
          view_html += '''</div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Third Image : </div>
                      <div class="w-50">'''
          if view_data.product_pic_third:            
            view_html += f'''<img src='{view_data.product_pic_third.url}' alt="Product Front Pic" width='200' height='100' ></div>'''
          else:            
            view_html += '''Not Available'''
          view_html += '''</div>
              </div>
              <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Fourth Image : </div>
                      <div class="w-50">'''
          if view_data.product_pic_fourth:            
            view_html += f'''<img src='{view_data.product_pic_fourth.url}' alt="Product Front Pic" width='200' height='100' ></div>'''
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

          view_html += f'''
          </div>
            <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Product Description : </div>
                      <div class="w-50">{ str(view_data.product_desc) }</div>
                  </div>
              </div>
            <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Created At : </div>
                      <div class="w-50">{ str(view_data.created_at.date()) }</div>
                  </div>
              </div>
            <div class="col-lg-6 col-12 mb-3">
                  <div class="row">
                      <div class="w-50 fw-bold">Updated At : </div>
                      <div class="w-50">{ str(view_data.updated_at.date()) }</div>
                  </div>
              </div>
          '''    
          
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
        print(what)
        try:
          product = Product.objects.get(product_id=product_id,seller=seller)
          if product.status.lower() == 'active':
            product.status = 'Inactive'
            product.save()
            response_data = {
              'status': True,
              'message': 'Category Status Changed to Inactive',
              'tags' : 'success',
              }
          elif product.status.lower() == 'inactive':
            product.status = 'Active'
            product.save()
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
  

  products = seller.products.all().order_by("product_id")
  unique_brand = set(product.brand for product in products)
  unique_color = set(product.color for product in products)
  unique_material = set(product.material for product in products)
  categories = seller.category.all()
  context['products'] = products
  context['categories'] = categories
  context['unique_brand'] = unique_brand
  context['unique_color'] = unique_color
  context['unique_material'] = unique_material

  return render(request,"products/products_details.html",context)




@login_required(login_url='login')
@user_passes_test(check_role_seller)
def update_product(request,iid):
  context = {}
  try:
    id = base64.b64decode(iid).decode('utf-8')
    seller = Seller.objects.get(user=request.user)
    product = Product.objects.get(product_id = id,seller=seller)
  except Product.DoesNotExist:
    product = None
    messages.error(request,"Product Does Not Exists!!")
  except Seller.DoesNotExist:
    seller = None
    messages.error(request,"You are not a Seller!!")
    return redirect("login")
  except Exception as e:
    messages.error(request,f"Somethings goes Wrong!! {e}")
  context['product'] = product

  if request.method == 'POST':
    print(request.POST)
    try:
      product_id = request.POST.get("product_id").strip()
      category_id = request.POST.get("category").strip()
      product_name = request.POST.get('product_name').strip()
      brand = request.POST.get("brand").strip()
      # product_slug = request.POST.get('product_slug')
      price = request.POST.get('price').strip()
      discount = request.POST.get("discount").strip()
      stock = request.POST.get("stock_quantity").strip()
      sku = request.POST.get("sku").strip()
      size = request.POST.get("size").strip()
      color = request.POST.get("color").strip()
      weight = request.POST.get("weight").strip()
      material = request.POST.get("material").strip()
      width = request.POST.get("width").strip()
      height = request.POST.get("height").strip()
      tags = request.POST.get("tags").strip()
      product_status = request.POST.get("status").strip()
      product_desc = request.POST.get("product_desc").strip()
      

      try:
        category = Category.objects.get(category_id=category_id)
      except Category.DoesNotExist:
        messages.error(request,"Category Does Not Exists!!")

      try:
        product.product_id = product_id
        product.category = category
        product.product_name = product_name
        product.brand = brand
        product.price = price
        product.discount=discount
        product.stock_quantity = stock
        product.sku = sku
        product.size = size
        product.color = color
        product.weight = weight
        product.material=material
        product.width = width
        product.height = height
        product.tags=tags
        product.status=product_status
        product.product_desc = product_desc

        if "product_pic_front" in request.FILES:
          product_pic_front = request.FILES["product_pic_front"]
          product.product_pic_front = product_pic_front

        if "product_pic_back" in request.FILES:
          product_pic_back = request.FILES["product_pic_back"]
          product.product_pic_back = product_pic_back

        if "product_pic_third" in request.FILES:
          product_pic_third = request.FILES["product_pic_third"]
          product.product_pic_third = product_pic_third

        if "product_pic_fourth" in request.FILES:
          product_pic_fourth = request.FILES["product_pic_fourth"]
          product.product_pic_fourth = product_pic_fourth

        product.save()
        messages.success(request,"Product Updated Successfully!")
      except:
        messages.error(request,"Failed to Update Product!!")

    except:
      messages.error(request,"Somethings goes Wrong!!")
    return redirect("products_details")
  sizes = ['S','M','L','XL','XXL','XXXL']                                                                         
  tags = Tags.objects.filter(seller=seller)
  categories = Category.objects.filter(seller=seller)
  context['tags']=tags
  context['categories']=categories
  context['sizes']=sizes
  return render(request,"products/update_product.html",context)



@login_required(login_url='login')
@user_passes_test(check_role_seller)
def delete_product(request,iid):
  try:
    id = base64.b64decode(iid).decode('utf-8')
    seller = Seller.objects.get(user=request.user)
    product =  Product.objects.get(product_id = id,seller=seller)
    product.delete()
    messages.success(request,"Product Deleted Successfully!")
  except Seller.DoesNotExist:
    messages.error(request,"Seller Does Not Exists!!")
  except Product.DoesNotExist:
    messages.error(request,"Product Does Not Exists!!")
  except:
    messages.error(request,"Somethings goes Wrong!!")
  return redirect("products_details")



def add_order(request):
  return render(request,"products/add_order.html")