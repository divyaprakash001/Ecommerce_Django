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

  def __str__(self):
    return f"self.product.product_name - {self.quantity}"
  
  def total_price(self):
    return (self.product.discounted_price() * self.quantity)
  
  def subtotal(self):
    sum=0
    for item in self.products.all():
      sum += self.total_price
    return self.sum
  
  class Meta:
    db_table = "cart"
    verbose_name = "Cart"
    verbose_name_plural = "Carts"
    ordering = ['created_at']