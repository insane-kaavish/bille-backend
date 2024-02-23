from django.urls import path

from .views import *

urlpatterns = [
    path('',example_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('message/', message_view),
    path('update_password/', updatePassword_view),
    path('update_username/', updateUsername_view),
    path('inputdata/', inputdata_view),
    path('predictedUnit/', predictedUnit_view),
    path('monthwiseUnits/', monthwiseUnits_view),
    path('roomwiseUnits/', roomwiseUnits_view),
    path('scrape/', scrape_view),
]