from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True) # changes email to unique and blank to false
    # user_id = models.AutoField(primary_key=True)
    # user_name = models.CharField(max_length=50)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
    # user_id = models.AutoField(primary_key=True)

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=50) 
#     email = models.EmailField(unique=True)
#     KE_number = models.CharField(max_length=50)
#     created_at = models.DateTimeField(default=now, editable=False)
#     updated_at = models.DateTimeField(default=now, editable=False)
#     Bills = []
#     Rooms = []

#     def __str__(self):
#         return self.user_name

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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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

    # SUB_CATEGORY_CHOICES = [ ]

    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    alias = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
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
    predict_date = models.DateTimeField()
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message
    
# class InputData(models.Model):
#     user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)

#     num_people = models.IntegerField()
#     num_stayathome = models.IntegerField()
#     num_parttime = models.IntegerField()
#     num_fulltime = models.IntegerField()

#     def __str__(self):
#         return str(self.user_id)