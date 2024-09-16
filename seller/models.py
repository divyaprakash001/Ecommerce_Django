from django.db import models
from accounts.models import User, UserProfile

# Create your models here.
class Seller(models.Model):
  user = models.OneToOneField(User,related_name="user" ,on_delete=models.CASCADE)
  user_profile = models.OneToOneField(UserProfile,related_name="user_profile" ,on_delete=models.CASCADE)
  seller_name = models.CharField(max_length=100, blank=True, null=True)
  seller_gst_no = models.CharField(max_length=50, null=True, blank=True)
  seller_gst_pic = models.ImageField(upload_to="vendor/gst_pic")
  seller_street = models.CharField(max_length=100,blank=True,null=True)
  seller_city = models.CharField(max_length=100,blank=True,null=True)
  seller_district = models.CharField(max_length=50,blank=True,null=True)
  seller_state = models.CharField(max_length=50,blank=True,null=True)
  seller_country = models.CharField(max_length=50,blank=True,null=True)
  seller_pincode = models.CharField(max_length=10,blank=True,null=True)

   # New fields
  # seller_business_type = models.CharField(max_length=50, choices=[('Retail', 'Retail'), ('Wholesale', 'Wholesale'), ('Service', 'Service')], blank=True, null=True)
  seller_website_url = models.URLField(blank=True, null=True)
  seller_bank_account = models.CharField(max_length=50, blank=True, null=True)
  seller_payment_methods = models.CharField(max_length=255, blank=True, null=True)

  # status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')], default='Active')
  # join_date = models.DateTimeField(auto_now_add=True)

  seller_facebook_url = models.URLField(blank=True, null=True)
  seller_twitter_url = models.URLField(blank=True, null=True)
  seller_instagram_url = models.URLField(blank=True, null=True)

  business_hours = models.TextField(blank=True, null=True)
  shipping_methods = models.TextField(blank=True, null=True)
  shipping_regions = models.TextField(blank=True, null=True)
  terms_and_conditions_url = models.URLField(blank=True, null=True)
  privacy_policy_url = models.URLField(blank=True, null=True)

  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.email
  
  def get_full_address(self):
    parts = [self.seller_street, self.seller_city, self.seller_district, self.seller_state, self.seller_country, self.seller_pincode]
    return ', '.join(part for part in parts if part)
  
  class Meta:
    db_table = "seller"
    verbose_name = "Seller"
    verbose_name_plural = "Sellers"
    ordering = ['created_at']

