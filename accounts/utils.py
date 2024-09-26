from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from ecommerce_main import settings

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
  



def send_verification_email(request,user,mail_subject,email_template):
  current_site = get_current_site(request)
  mail_subject = mail_subject
  message = render_to_string(email_template,{
  'user': user,
  'domain' : current_site,
  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
  'token':default_token_generator.make_token(user),
  })
  to_email = user.email
  mail = EmailMessage(mail_subject,message,to = [to_email])
  mail.send()


def send_notification(mail_subject, mail_template,context):
  from_email = settings.DEFAULT_FROM_EMAIL
  message = render_to_string(mail_template,context)
  to_email = context['user'].email
  mail = EmailMessage(mail_subject,message,from_email,to = [to_email])
  mail.send()


# def seller_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('login')  # Redirect to login if not authenticated
        
#         if request.user.role != request.user.SELLER:
#             messages.warning(request, "You do not have permission to access this page.")
#             return redirect('access_denied')  # Redirect to access denied page if not a seller
        
#         return view_func(request, *args, **kwargs)
    
#     return _wrapped_view


# def customer_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('login')  # Redirect to login if not authenticated
        
#         if request.user.role != request.user.CUSTOMER:
#             messages.warning(request, "You do not have permission to access this page.")
#             return redirect('access_denied')  # Redirect to access denied page if not a seller
        
#         return view_func(request, *args, **kwargs)
    
#     return _wrapped_view
