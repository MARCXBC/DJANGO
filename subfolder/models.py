from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager




class User(AbstractUser):
   
    username = None
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    email = models.EmailField(unique=True,max_length=50)
    is_deleted = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,blank=True,null=True)
    is_verified = models.BooleanField(default=False)

#    is_staff = models.BooleanField(default=False)
#    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name","last_name","password"]
    objects = CustomUserManager()
# Create your models here.

    def __str__(self):
        return self.email

# class Meta:
#         ordering = ['email'] # Overrides Django's default 'username' sort layout
