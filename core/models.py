from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    no_of_people = models.IntegerField()
    stayathome_people = models.IntegerField()
    partiallyathome_people = models.IntegerField()
    fulltimeemployees = models.IntegerField()
    no_of_rooms = models.IntegerField()
    appliances = models.ManyToManyField('Appliance', through='ApplianceUsage')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Appliance(models.Model):
    name = models.CharField(max_length=255)

class ApplianceUsage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    usage_hours = models.IntegerField()
    
# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class MyUser(AbstractUser):
#     USERNAME_FIELD = 'email'
#     email = models.EmailField(('email address'), unique=True) # changes email to unique and blank to false
#     REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

# def ready(self):
#     from django.conf import settings
#     from django.db.models.signals import post_save
#     from django.dispatch import receiver
#     from rest_framework.authtoken.models import Token
#     @receiver(post_save, sender=settings.AUTH_USER_MODEL)
#     def create_auth_token(sender, instance=None, created=False, **kwargs):
#         if created:
#             Token.objects.create(user=instance)
            
#     for user in User.objects.all():
#         Token.objects.get_or_create(user=user)
