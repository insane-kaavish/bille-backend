from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class ContactUs(AbstractUser):
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    
    NAME = 'name'
    USERNAME_FIELD = 'email'
    MESSAGE = 'message'
    