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
      accepted_payment_method = request.POST.get('accepted_payment_method')


      profile_photo = request.FILES.get('e_photo')
      cover_photo = request.FILES.get('cover_photo')
      gst_license = request.FILES.get('gst_license')

      al_user = request.user
      al_user.first_name = first_name
      al_user.last_name = last_name
      al_user.username= username
      al_user.email = email
      al_user.phone_number = phone_number
      al_user.save()

      sellerprofile = UserProfile.objects.get(user=al_user)
      if profile_photo:
        sellerprofile.profile_photo = profile_photo
      if cover_photo:
        sellerprofile.cover_photo = cover_photo

      sellerprofile.save()
        

      seller = Seller.objects.get(user=request.user)
      seller.user = al_user
      seller.user_profile = seller_profile
      seller.seller_name = business_name
      seller.seller_gst_no = gstno
      seller.seller_website_url = website_url
      seller.seller_facebook_url = facebook_url
      seller.seller_twitter_url = twitter_url
      seller.seller_instagram_url = instagram_url
      seller.seller_youtube_url = youtube_url
      seller.seller_linkedin_url = linkedin_url

      seller.save()
      messages.success(request,"Profile Updated Successfully!")
      return redirect("seller_profile")

    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
      if request.method == 'GET':
        username = request.GET.get("username").strip()
        available = User.objects.filter(username=username).exists()
        if available:
          return JsonResponse({"status":"found","message":"Already Exists!"})
        else:
          return JsonResponse({"status":"not found","message":"Not Exists!"})
  except:
    pass





  return render(request,"seller/seller_profile.html")

