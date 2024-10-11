from django.db import models
from seller.models import Seller


# Create your models here.
class Category(models.Model):
  seller = models.ForeignKey(Seller, related_name="seller", on_delete=models.CASCADE, null=True)
  category_id = models.CharField(max_length=10,unique=True)
  category_name = models.CharField(max_length=50,unique=True)
  category_slug = models.SlugField(unique=True)
  category_pic = models.ImageField(upload_to="products/categories", null=True)
  category_desc = models.CharField(max_length=50, null=True,blank=True)
  status = models.CharField( max_length=10,default="Active")

  def __str__(self):
    return self.category_name
  
  class Meta:
    db_table = "category"
    verbose_name = "Category"
    verbose_name_plural = "Categories"
    ordering = ['category_name']