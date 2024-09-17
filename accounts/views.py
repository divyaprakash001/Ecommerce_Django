from django.shortcuts import redirect, render
from .forms import UserForm
from seller.forms import SellerForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import seller_required, customer_required
from django.core.exceptions import PermissionDenied

# restricting user to access seller dashboard
def check_role_seller(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied

# restricting seller to access customer dashboard
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied


# Create your views here.
def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!")
    return redirect("dashboard")
  elif request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username, email=email,password=password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request, "Your account has been registered successfully! Please check your email !!!", fail_silently=True)
      return redirect("registerUser")
    else:
      print(form.errors)
  else:
    form = UserForm()
  context={
      'title':'User Registration',
      'form':form
    }
  return render(request,"accounts/registerUser.html",context)


def registerSeller(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!")
    return redirect("dashboard")
  elif request.method == "POST":
    user_form = UserForm(request.POST)
    s_form = SellerForm(request.POST,request.FILES)
    if user_form.is_valid() and s_form.is_valid():
      first_name = user_form.cleaned_data['first_name']
      last_name = user_form.cleaned_data['last_name']
      username = user_form.cleaned_data['username']
      email = user_form.cleaned_data['email']
      password = user_form.cleaned_data['password']

      user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username, email=email,password=password)
      user.role = User.SELLER
      user.save()

      # seller_name = user_form.cleaned_data['seller_name']
      # seller_gst_pic = user_form.cleaned_data['seller_gst_pic']
      seller = s_form.save(commit=False)
      seller.is_approved=False
      seller.user=user
      userprofile = UserProfile.objects.get(user=user)
      seller.user_profile = userprofile
      seller.save()
      messages.success(request, "Your account has been registered successfully! Please check your email !!!", fail_silently=True)
      return redirect("registerSeller")
    else:
      print(user_form.errors)
      print(s_form.errors)
  else:
    user_form = UserForm()
    s_form = SellerForm()
  context={
      "title":"Seller Registration",
      "form":user_form,
      "s_form":s_form,
  }
  return render(request,"accounts/registerSeller.html",context)

def login(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!")
    return redirect("myAccount")
  elif request.method == "POST":
    email = request.POST['email'].strip()
    password = request.POST['password'].strip()
      
    user = auth.authenticate(email=email,password=password)

    if user is not None:
      auth.login(request,user)
      messages.success(request,"You are successfully logged in!")
      return redirect('myAccount')
    else:
      messages.error(request,"Invalid login credentials!!!")
      return redirect('login')

  return render(request,"accounts/login.html")

from .utils import detectUser
@login_required(login_url="login")
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  print(redirectUrl)
  return redirect(redirectUrl)

@login_required(login_url="login")
# @customer_required  # first way
@user_passes_test(check_role_customer)        # second way
def customerDashboard(request):
  return render(request, "accounts/customerDashboard.html")

@login_required(login_url="login")
# @seller_required
@user_passes_test(check_role_seller) 
def sellerDashboard(request):
  return render(request, "seller/sellerDashboard.html")


# @login_required(login_url="login")
def logout(request):
  if request.user.is_authenticated:
      auth.logout(request)
      messages.info(request, "You are logged out!")
  else:
      messages.info(request, "You are already logged out!")
  return redirect("login")

def access_denied(request):
    return render(request, 'accounts/access_denied.html')