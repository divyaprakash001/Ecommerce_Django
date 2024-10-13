from django.db import models
from seller.models import Seller


class Tags(models.Model):
  tag_name = models.CharField(max_length=30, unique=True)
  tag_desc = models.CharField(max_length=100)

  def __str__(self):
    return self.tag_name
  
  class Meta:
    db_table = "tags"
    verbose_name = "Tags"
    verbose_name_plural = "Tags"
    ordering = ['tag_name']

# Create your models here.
class Category(models.Model):
  seller = models.ForeignKey(Seller, related_name="category", on_delete=models.CASCADE, null=True)
  category_id = models.CharField(max_length=10,unique=True)
  category_name = models.CharField(max_length=50,unique=True)
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

class Product(models.Model):
  seller = models.ForeignKey(Seller, related_name="product", on_delete=models.CASCADE)
  category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
  product_id = models.CharField(max_length=50,unique=True)
  product_name = models.CharField(max_length=100,unique=True)
  product_slug = models.SlugField()
  brand  = models.CharField(max_length=50)
  price =  models.DecimalField(max_digits=10, decimal_places=2)
  discount = models.DecimalField(max_digits=5, decimal_places=2)
  stock_quantity = models.CharField(max_length=50)
  sku = models.CharField(max_length=50, null=True,blank=True)
  size = models.CharField(max_length=50,null=True,blank=True)
  color = models.CharField(max_length=50,null=True,blank=True)
  weight = models.CharField(max_length=50,null=True,blank=True)
  material = models.CharField(max_length=50,null=True,blank=True)
  width = models.CharField(max_length=50,null=True,blank=True)
  height = models.CharField(max_length=50,null=True,blank=True)
  tags = models.CharField(max_length=50,null=True,blank=True)
  product_pic_front = models.ImageField(upload_to="products/product_photo/")
  product_pic_back = models.ImageField(upload_to="products/product_photo/")
  product_pic_third = models.ImageField(upload_to="products/product_photo/",null=True,blank=True)
  product_pic_fourth = models.ImageField(upload_to="products/product_photo/",null=True,blank=True)

  created_at  = models.TimeField(auto_now_add=True)
  updated_at = models.TimeField(auto_now=True)

  def __str__(self):
    return self.product_name
  
  class Meta:
    db_table = "product"
    verbose_name = "Product"
    verbose_name_plural = "Products"
    ordering = ['product_name']