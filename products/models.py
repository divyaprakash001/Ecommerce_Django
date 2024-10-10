from django.db import models

# Create your models here.
class Category(models.Model):
  category_id = models.CharField(max_length=10,unique=True)
  category_name = models.CharField(max_length=50)
  category_slug = models.SlugField()
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