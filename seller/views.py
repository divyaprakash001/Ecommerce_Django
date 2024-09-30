from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test

from accounts.views import check_role_seller
# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_seller)
def seller_profile(request):
  return render(request,"seller/seller_profile.html")