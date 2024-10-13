from django.contrib import admin
from products.models import Category,Product,Tags

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {"category_slug":("category_name",)}
  list_display = ['category_name','category_id','seller']
  exclude = ['category_id']


class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {"product_slug":("product_name",)}
  list_display = ['product_name','product_id','seller']
  exclude = ['product_id']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Tags)