from django import forms
from django.contrib import admin
from products.models import Category,Product,Tags

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {"category_slug":("category_name",)}
  list_display = ['category_name','category_id','seller__seller_name']
  exclude = ['category_id']
  search_fields = ['category_name','seller__seller_name']


# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         brand = cleaned_data.get('brand')
#         category = cleaned_data.get('category')
#         product_name = cleaned_data.get('product_name')

#         if brand and category and product_name:
#             cleaned_data['sku'] = f"{brand.upper()}-{category}-{product_name[:3].upper()}-{int(self.instance.pk or 0)}"
        
#         return cleaned_data


class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {"product_slug":("product_name",)}
  list_display = ['product_name','product_id','category','brand','sku','seller','updated_at']
  list_display_links=['product_name','category','brand']
  exclude = ['product_id','sku']
  search_fields = ('product_id','product_name','category__category_name','brand','size','color','weight','material','tags')

  # form = ProductAdminForm


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Tags)