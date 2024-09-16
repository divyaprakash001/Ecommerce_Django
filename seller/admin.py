from django.contrib import admin
from .models import Seller

# Register your models here.
class SellerAdmin(admin.ModelAdmin):
  list_display = ['user','seller_name', 'is_approved','created_at']
  list_display_links = ['user','seller_name']

admin.site.register(Seller,SellerAdmin)