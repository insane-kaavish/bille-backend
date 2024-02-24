from django.urls import path

from .views import *

urlpatterns = [
    path('', example_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('message/', message_view),
    path('update_password/', update_password_view),
    path('update_user/', update_user_view),
    path('inputdata/', inputdata_view),
    path('predicted_units/', predicted_units_view),
    path('monthwise_units/', monthwise_units_view),
    path('roomwise_units/', roomwise_units_view),
    path('scrape/', scrape_view),
]