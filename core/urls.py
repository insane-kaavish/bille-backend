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
    path('predict/', predict_view),
    path('monthwise/', monthwise_view),
    path('roomwise/', roomwise_view),
    path('scrape/', scrape_view),
]