from django.urls import path

from .views.views import *
from .views.room_views import *
from .views.appliance_views import *
from .views.predict_views import *
from .views.scrape_views import *

urlpatterns = [
    path('', example_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('update_password/', update_password_view),
    path('update_user/', update_user_view),
    path('repopulate_database/', repopulate_view),
    
    path('message/', message_view),
    path('input/', input_view),
    
    path('predict/', predict_view),
    path('months/', months_view),
    
    path('rooms/', rooms_view),
    path('room/', room_view),
    path('update_room/', update_room_view),
    path('delete_room/', delete_room_view),
    path('room_tags/', room_tags_view),

    path('appliances/', appliances_view),
    path('appliance/', appliance_view),    
    path('update_appliance/', update_appliance_view),
    path('delete_appliance/', delete_appliance_view),
    path('categories/', categories_view),
    
    path('update_adjustment/', update_monthly_adjustment_view),
    path('reset_adjustments/', reset_monthly_adjustment_view),
    path('scrape/', scrape_view),
    path('task_status/', get_task_status),
]