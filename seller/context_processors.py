from seller.models import Seller

def fetch_seller(request):
    seller = None  # Initialize seller as None
    if request.user.is_authenticated:
        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            seller = None  # Handle the case where the seller doesn't exist
    return {'seller': seller}