from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
# created the methods how user is created
class UserManager(BaseUserManager):
  # it will not contain any field, it contains only methods
  def create_user(self,first_name,last_name,username,email,password=None):
    if not email:
      raise ValueError("User must have email")
    if not username:
      raise ValueError("User must have username")
    
    user = self.model(
      email = self.normalize_email(email),
      username=username,
      first_name=first_name,
      last_name=last_name,
    )
    user.set_password(password)
    user.save(using=self.db)
    return user
  
  # method to create the superuser
  def create_superuser(self,first_name,last_name,username,email,password=None):
    user = self.create_user(
      email=self.normalize_email(email),
      username=username,
      password=password,
      first_name=first_name,
      last_name=last_name,
    )
    user.is_admin=True
    user.is_active=True
    user.is_staff=True
    user.is_superadmin=True

    user.save(using=self.db)
    return user


class User(AbstractBaseUser):
  SELLER = 1
  CUSTOMER = 2

  ROLE_CHOICE=(
    (SELLER,'Seller'),
    (CUSTOMER,'Customer'),
  )
  # this contains fields name i.e, first,last,email,etc
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50,unique=True)
  email = models.EmailField(max_length=254,unique=True)
  phone_number = models.CharField(max_length=15,blank=True)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True,null=True)

  # required fields
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  # authentication part
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS=['username','first_name','last_name']

  objects = UserManager()

  def __str__(self):
    return self.email
  
  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self,app_label):
    return True

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
  profile_photo = models.ImageField(upload_to="users/profile_photo",blank=True,null=True)
  cover_photo = models.ImageField(upload_to="users/cover_photo",blank=True, null=True)
  address = models.CharField(max_length=200,blank=True,null=True)
  country = models.CharField(max_length=50,blank=True,null=True)
  state = models.CharField(max_length=50,blank=True,null=True)
  city = models.CharField(max_length=50,blank=True,null=True)
  pincode = models.CharField(max_length=10,blank=True,null=True)
  latitude = models.CharField(max_length=20,blank=True,null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.email
  
