from seller.models import Seller

def fetch_seller(request):
    seller = None  
    if request.user.is_authenticated:
        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            seller = None 
    return {'seller': seller}