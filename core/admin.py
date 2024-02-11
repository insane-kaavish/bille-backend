from django.contrib import admin
from .models import CustomUser, Bill, Room, Appliance, Usage

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Bill)
admin.site.register(Room)
admin.site.register(Appliance)
admin.site.register(Usage)