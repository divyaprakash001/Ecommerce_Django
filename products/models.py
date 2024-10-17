from decimal import Decimal
from django.db import models
from seller.models import Seller


class Tags(models.Model):
  seller = models.ForeignKey(Seller, related_name="tags", on_delete=models.CASCADE, null=True)
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
  category_name = models.CharField(max_length=50)
  category_slug = models.SlugField()
  category_pic = models.ImageField(upload_to="products/categories", null=True)
  category_desc = models.CharField(max_length=50, null=True,blank=True)
  status = models.CharField( max_length=10,default="Active")

  def __str__(self):
    return self.category_name
  
  def save(self, *args, **kwargs):
        if not self.category_id:  # Only generate if category_id is not set
            prefix = 'C'
            last_category = Category.objects.filter(category_id__startswith=prefix).order_by('category_id').last()
            if last_category:
                last_id = int(last_category.category_id[1:])
                new_id = last_id + 1
            else:
                new_id = 1
            self.category_id = f"{prefix}{new_id:04d}"

        super().save(*args, **kwargs)
  
  class Meta:
    unique_together = ('seller', 'category_name')
    db_table = "category"
    verbose_name = "Category"
    verbose_name_plural = "Categories"
    ordering = ['category_name']
  

class Product(models.Model):
  seller = models.ForeignKey(Seller, related_name="products", on_delete=models.CASCADE)
  category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
  product_id = models.CharField(max_length=50,unique=True)
  product_name = models.CharField(max_length=100,unique=True)
  product_slug = models.SlugField()
  brand  = models.CharField(max_length=50)
  price =  models.DecimalField(max_digits=10, decimal_places=2)
  discount = models.IntegerField()
  stock_quantity = models.PositiveIntegerField()
  sku = models.CharField(max_length=50)
  size = models.CharField(max_length=50,null=True,blank=True)
  color = models.CharField(max_length=50)
  weight = models.CharField(max_length=50)
  material = models.CharField(max_length=50,null=True,blank=True)
  width = models.PositiveIntegerField(null=True,blank=True)
  height = models.PositiveIntegerField(null=True,blank=True)
  tags = models.CharField(max_length=50,null=True,blank=True)
  product_desc = models.CharField(max_length=1000,null=True,blank=True)
  product_pic_front = models.ImageField(upload_to="products/product_photo/")
  product_pic_back = models.ImageField(upload_to="products/product_photo/")
  product_pic_third = models.ImageField(upload_to="products/product_photo/", null=True, blank=True)
  product_pic_fourth = models.ImageField(upload_to="products/product_photo/", null=True, blank=True)
  status = models.CharField(max_length=15,default='Active')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def discounted_price(self):
        discount_amount = (self.price * Decimal(self.discount)) / Decimal(100)
        return self.price - discount_amount

  def __str__(self):
    return self.product_name
  
  def save(self, *args, **kwargs):
    if not self.product_id:  
        prefix = 'P'
        last_product = Product.objects.filter(product_id__startswith=prefix).order_by('product_id').last()
        if last_product:
            last_id = int(last_product.product_id[1:])  
            new_id = last_id + 1
        else:
            new_id = 1
        self.product_id = f"{prefix}{new_id:04d}"

    # Generate SKU
    if self.brand and self.category and self.product_name:
        self.sku = f"{self.brand.upper()}-{self.category.category_id}-{self.product_name[:3].upper()}-{self.product_id}"

    super().save(*args, **kwargs)

  
  class Meta:
    db_table = "product"
    verbose_name = "Product"
    verbose_name_plural = "Products"
    ordering = ['product_name']