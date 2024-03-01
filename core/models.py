from django.db import models
from django.utils.timezone import now
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .managers import CustomUserManager
from .months import MONTH_CHOICES

# Create your models here.
class MonthlyAdjustment(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.IntegerField(choices=MONTH_CHOICES)
    adj_factor = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.month}'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    id = models.AutoField(primary_key=True)
    num_people = models.IntegerField(blank=True, null=True)
    ke_num = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager() 

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            # Generate a unique username
            self.username = str(uuid.uuid4())
        super().save(*args, **kwargs)

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    units = models.IntegerField()
    is_predicted = models.BooleanField()
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    wattage = models.IntegerField()

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class RoomTag(models.Model):
    tag = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tag} - {self.description}"

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey(RoomTag, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

class Appliance(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    wattage = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Automatically update wattage when sub_category is updated
    def save(self, *args, **kwargs):
        if self.sub_category:
            self.wattage = self.sub_category.wattage
        super().save(*args, **kwargs)

class Usage(models.Model):
    TYPE_CHOICES = [
        ('R', 'Room'),
        ('A', 'Appliance')
    ]

    id = models.AutoField(primary_key=True)
    appliance = models.ForeignKey(Appliance, null = True, blank = True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, null = True, blank = True, on_delete=models.CASCADE)
    units = models.IntegerField()
    predict_date = models.DateTimeField(null = True)
    month = models.IntegerField(null = True, choices=MONTH_CHOICES)
    year = models.IntegerField(null = True)
    type = models.CharField(null = True, max_length=1, choices=TYPE_CHOICES)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message
    