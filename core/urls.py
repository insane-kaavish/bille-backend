from django.urls import path

from .views import *

urlpatterns = [
    path('', example_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('message/', message_view),
    path('update_password/', update_password_view),
    path('update_user/', update_user_view),
    path('input/', input_view),
    path('predict/', predict_view),
    path('months/', months_view),
    path('rooms/', rooms_view),
    path('room/', room_view),
    path('scrape/', scrape_view),
]