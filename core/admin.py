from django.contrib import admin
from .models import Bill, Room, Appliance, Usage, Message

# Register your models here.
# admin.site.register(User)
admin.site.register(Bill)
admin.site.register(Room)
admin.site.register(Appliance)
admin.site.register(Usage)
admin.site.register(Message)
# admin.site.register(InputData)