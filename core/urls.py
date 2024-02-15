from django.urls import path

from .views import *

urlpatterns = [
    path('',example_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('message/', message_view),
    path('update_password/', updatePassword_view),
    path('update_username/', updateUsername_view),
]