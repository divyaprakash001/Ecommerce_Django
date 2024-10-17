from django.db import models

from accounts.models import User
from products.models import Product

# Create your models here.
class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name="products", on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at= models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return self.user
  
  class Meta:
    db_table = "cart"
    verbose_name = "Cart"
    verbose_name_plural = "Carts"
    ordering = ['created_at']