from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
  class Meta:
    model = Seller
    fields = ['seller_name','seller_gst_pic']
    widgets={
      "seller_name":forms.TextInput(attrs={"class":"form-control "}),
      "seller_gst_pic":forms.FileInput(attrs={"class":"form-control custom_file"}),
    }
