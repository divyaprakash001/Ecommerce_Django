from .models import Cart
from products.models import Category, Product

def get_cart_counter(request):
  cart_count=0
  if request.user.is_authenticated:
    try:
      cart_items = Cart.objects.filter(user=request.user)
      if cart_items:
        for cart_item in cart_items:
          cart_count += cart_item.quantity
      else:
        cart_count=0
    except:
      cart_count=0
  return dict(cart_count=cart_count)


def get_cart_amounts(request):
  subtotal = 0
  tax = 0
  grand_total = 0

  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
      product = Product.objects.get(product_id=item.product.product_id)
      subtotal +=  (float(product.discounted_price()) * item.quantity)
    tax = float(subtotal) * (12/100)
    grand_total = subtotal + tax
  
  return dict(subtotal=subtotal,tax=tax,grand_total=grand_total)

def category_list(request):
  categories = Category.objects.filter(status="Active").order_by("created_at")
  return dict(categories=categories)
    