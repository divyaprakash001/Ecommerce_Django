from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def detectUser(user):
  if user.role == 1:
    redirectUrl = "sellerDashboard"
    return redirectUrl
  elif user.role == 2:
    redirectUrl = "customerDashboard"
    return redirectUrl
  elif user.role == None and user.is_superadmin:
    redirectUrl = '/admin'
    return redirectUrl
  



def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        if request.user.role != request.user.SELLER:
            messages.warning(request, "You do not have permission to access this page.")
            return redirect('access_denied')  # Redirect to access denied page if not a seller
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def customer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        if request.user.role != request.user.CUSTOMER:
            messages.warning(request, "You do not have permission to access this page.")
            return redirect('access_denied')  # Redirect to access denied page if not a seller
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
