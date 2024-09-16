from django.shortcuts import redirect, render
from .forms import UserForm
from seller.forms import SellerForm
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.
def registerUser(request):
  if request.method == "POST":
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
  if request.method == "POST":
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
  if request.method == "POST":
      email = request.POST['email'].strip()
      password = request.POST['password'].strip()
      user = User.objects.get(email=email,password=password)
      if user.is_authenticated():
        messages.success("You are already logged in!")
        redirect('login')
      else:
        user = authenticate(email,password)
        print(user)
  return render(request,"accounts/login.html")