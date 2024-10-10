from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,user_passes_test

from accounts.models import User, UserProfile
from accounts.views import check_role_seller
from seller.models import Seller
from django.contrib import messages

@login_required(login_url='login')
@user_passes_test(check_role_seller)
def seller_profile(request):
  try:
    if request.method == 'POST':
      first_name = request.POST.get('seller_first_name')
      last_name = request.POST.get('seller_last_name')
      username = request.POST.get('username')
      email = request.POST.get('seller_email')
      phone_number = request.POST.get('seller_phone_number')

      business_name = request.POST.get('business_name')
      gstno = request.POST.get('gstno')
      business_address = request.POST.get('business_address')
      website_url = request.POST.get('website_url')
      facebook_url = request.POST.get('facebook_url')
      twitter_url = request.POST.get('twitter_url')
      instagram_url = request.POST.get('instagram_url')
      youtube_url = request.POST.get('youtube_url')
      linkedin_url = request.POST.get('linkedin_url')

      bank_name = request.POST.get('bank_name')
      account_no = request.POST.get('account_no')
      ifsc_code = request.POST.get('ifsc_code')
      account_type = request.POST.get('account_type')
      accepted_payment_method = request.POST.getlist('accepted_payment_method')

      try:
        al_user = request.user
        al_user.first_name = first_name
        al_user.last_name = last_name
        al_user.username= username
        al_user.email = email
        al_user.phone_number = phone_number
        al_user.save()
      except:
        messages.error(request, 'Error in updating user details')
        return redirect("seller_profile")
      try:
        seller_profile, created = UserProfile.objects.get_or_create(user=al_user)
        if created:
          print("UserProfile created.")

        if 'profile_photo' in request.FILES:
          profile_photo = request.FILES['profile_photo']
          seller_profile.profile_photo = profile_photo
        if 'cover_photo' in request.FILES:
          cover_photo = request.FILES['cover_photo'] 
          seller_profile.cover_photo = cover_photo 
        seller_profile.save()
      except:
        messages.error(request, 'Error in updating profile')
        return redirect("seller_profile")
      
      try:
        seller = Seller.objects.get(user=request.user)
        seller.user = al_user
        seller.user_profile = seller_profile
        seller.seller_name = business_name
        seller.seller_gst_no = gstno
        seller.seller_bank_name = bank_name
        seller.seller_bank_account_no=account_no
        seller.seller_bank_acc_type = account_type
        seller.seller_bank_ifsc = ifsc_code
        seller.seller_payment_methods = accepted_payment_method
        seller.seller_website_url = website_url
        seller.seller_facebook_url = facebook_url
        seller.seller_twitter_url = twitter_url
        seller.seller_instagram_url = instagram_url
        seller.seller_youtube_url = youtube_url
        seller.seller_linkedin_url = linkedin_url

        if 'business_logo' in request.FILES:
          business_logo = request.FILES['business_logo'] 
          seller.seller_business_logo = business_logo
        if 'gst_license' in request.FILES:
          gst_license = request.FILES['gst_license'] 
          seller.seller_gst_pic = gst_license

        seller.save()
        messages.success(request,"Profile Updated Successfully!")
        return redirect("seller_profile")
      except:
        messages.error(request, 'Error in updating seller profile')



    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        username = request.GET.get("username").strip()
        available = User.objects.filter(username=username).exists()
        if available:
          return JsonResponse({"status":"found","message":"Already Exists!"})
        else:
          return JsonResponse({"status":"not found","message":"Not Exists!"})
  except:
    messages.error(request,"Something got error in updating the profile")
    return redirect("seller_profile")





  return render(request,"seller/seller_profile.html")

