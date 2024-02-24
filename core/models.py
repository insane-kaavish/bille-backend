from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    user_id = models.AutoField(primary_key=True)
    num_people = models.IntegerField(blank=True, null=True)
    ke_num = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager() 

    def __str__(self):
        return self.email


class Bill(models.Model):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    units = models.IntegerField()
    is_predicted = models.BooleanField()

class Room(models.Model):
    TAG_CHOICES = [
        ('LR', 'Living Room'),
        ('B', 'Bedroom'),
        ('K', 'Kitchen'),
        ('L', 'Lounge'),
        ('S', 'Store'),
        ('O', 'Others')
     ]   

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=TAG_CHOICES)
    alias = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)

class Appliance(models.Model):
    CATEGORY_CHOICES = [ 
        ('Iron', 'Iron'),
        ('Air Conditioner', 'Air Conditioner'),
        ('Refrigerator', 'Refrigerator'),
        ('Freezer', 'Freezer'),
        ('Washing Machine', 'Washing Machine'),
        ('Water Dispenser', 'Water Dispenser'),
        ('Others', 'Others')
    ]

    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(null = True, max_length=50)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now, editable=False)
    
class Usage(models.Model):
    MONTH_CHOICES = [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    ]

    TYPE_CHOICES = [
        ('R', 'Room'),
        ('A', 'Appliance')
    ]

    id = models.AutoField(primary_key=True)
    appliance_id = models.ForeignKey(Appliance, null = True, blank = True, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, null = True, blank = True, on_delete=models.CASCADE)
    units = models.IntegerField()
    predict_date = models.DateTimeField(null = True)
    month = models.IntegerField(null = True, choices=MONTH_CHOICES)
    year = models.IntegerField(null = True)
    type = models.CharField(null = True, max_length=1, choices=TYPE_CHOICES)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message
    