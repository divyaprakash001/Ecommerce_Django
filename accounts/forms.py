from django import forms
from .models import User

class UserForm(forms.ModelForm):
  password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
  alternate_number = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),required=False)
  class Meta:
    model = User
    fields = ['first_name','last_name','username','email']
    widgets={
      "first_name":forms.TextInput(attrs={"class":"form-control"}),
      "last_name":forms.TextInput(attrs={"class":"form-control"}),
      "username":forms.TextInput(attrs={"class":"form-control"}),
      "email":forms.EmailInput(attrs={"class":"form-control"}),
    }

  def clean(self):
      cleaned_data = super(UserForm, self).clean()
      password = cleaned_data.get("password")
      confirm_password = cleaned_data.get("confirm_password")

      # if password and confirm_password and password != confirm_password:
      #     self.add_error('confirm_password', 'Passwords do not match')

      if password != confirm_password:
        raise forms.ValidationError(
          "Password does not match"
        )

      return cleaned_data