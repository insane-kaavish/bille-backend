from django.contrib import admin
from .models import CustomUser, Bill, Room, Appliance, Usage, Message, MonthlyAdjustment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Bill)
admin.site.register(Room)
admin.site.register(Appliance)
admin.site.register(Usage)
admin.site.register(Message)
admin.site.register(MonthlyAdjustment)
