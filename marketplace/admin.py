from django.contrib import admin
from .models import Cart

# Register your models here.
class CartAdmin(admin.ModelAdmin):
  list_display=['product__product_name','user__username','quantity','updated_at']


admin.site.register(Cart,CartAdmin)