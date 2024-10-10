import socket
from django.shortcuts import redirect, render
from .forms import UserForm
from seller.forms import SellerForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required,user_passes_test
# from .utils import seller_required, customer_required
from django.core.exceptions import PermissionDenied
from .utils import detectUser ,send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator



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

      # send verification email
      try:
        mail_subject = "Activate your account"
        email_template = "accounts/email/activation_email.html"
        send_verification_email(request,user,mail_subject,email_template)
      except socket.timeout:
        print("Connection timed out. Please try again later.")
      except socket.error as e:
        print(f"Socket error: {e}")
      except Exception as e:
        print(f"An error occurred: {e}")

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
      mail_subject = "Activate your account"
      email_template = "accounts/email/activation_email.html"
      try:
        send_verification_email(request,user,mail_subject,email_template)
      except socket.timeout:
        print("Connection timed out. Please try again later.")
      except socket.error as e:
        print(f"Socket error: {e}")
      except Exception as e:
        print(f"An error occurred: {e}")

      messages.success(request, "Your account has been registered successfully! Please check your email !!!", fail_silently=True)
      return redirect("login")
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

# activating via activation link *******************
def activate(request,uidb64,token):
  try:
    id = force_str(urlsafe_base64_decode(uidb64).decode())
    user = User.objects.get(pk=id)
    print(user)
  except (User.DoesNotExist, TypeError, ValueError, OverflowError):
    user = None
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request,"User activated successfully!")
    return redirect("login")
  else:
    messages.error(request, 'Activation link is invalid!')
    return render(request, 'accounts/activation_invalid.html')

# forgot password
def forget_password(request):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!")
    return redirect("myAccount")
  elif request.method == "POST":
    try:
      email = request.POST['email']
      user = User.objects.get(email=email)
      print(user)
    except User.DoesNotExist:
      user = None
      messages.error(request,"User doesn't exists on given email !")
      return redirect("forget_password")
    
    if user is not None and user.is_active:
      mail_subject = "Here is the code for reset password !"
      email_template = "accounts/email/reset_email.html"
      
      try:
        send_verification_email(request,user,mail_subject,email_template)
        messages.info(request,"reset link has been sent on given email")
        return redirect("login")
      except socket.timeout:
        messages.error(request,"Connection timed out. Please try again later.")
        return redirect('login')
      except socket.error as e:
        messages.error(request,"Error in sending email. Please Check your connection.")
        return redirect('login')
      except Exception as e:
        print(f"An error occurred: {e}")
        messages.error(request,"Something got error while sending email. Please try again later.")
        return redirect('login')

    else:
      messages.error(request,"User is not active ! Wait for approval !!!")
      # return redirect("login")
  # else:
  #   context={
  #     # 'token':default_token_generator.make_token(),
  #   }
    return render(request,"accounts/forget_password.html")
  return render(request,"accounts/forget_password.html")


# reset password ***********************************************
def reset_password(request,uidb64,token):
  if request.user.is_authenticated:
    messages.warning(request,"You are already logged in!")
    return redirect("myAccount")
  elif request.method == "POST":
    try:
      id = uidb64
      user = User.objects.get(pk=id)
    except User.DoesNotExist:
      user=None
    if user is not None:
      password = request.POST['password'].strip()
      confirm_password = request.POST['confirm_password'].strip()
      if  password == confirm_password:
        user.set_password(password)
        user.save()
        messages.success(request,"Password reset successfully!")
        return redirect("login")
      else:
        messages.error(request,"Password doesn't match!")
        return redirect("reset_password",uidb64,token)
    else:
      messages.error(request,"User doesn't exists!")
      return redirect("login")
  else:
    try:
      id = force_str(urlsafe_base64_decode(uidb64).decode())
      user = User.objects.get(pk=id)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
      user = None
    
    if user is not None and default_token_generator.check_token(user, token):
      context = {
        "uid":force_str(urlsafe_base64_decode(uidb64).decode()),
        "token":token
      }
      return render(request,"accounts/reset_password.html",context)
    else:
      messages.error(request, 'Reset link is invalid!')
      return redirect('forget_password')
  




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





@login_required(login_url="login")
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  print(redirectUrl)
  return redirect(redirectUrl)

# @customer_required  # first way
@login_required(login_url="login")
@user_passes_test(check_role_customer)        # second way
def customerDashboard(request):
  return render(request, "accounts/customerDashboard.html")

@login_required(login_url="login")
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