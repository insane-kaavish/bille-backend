from django.urls import path

from .views import *

urlpatterns = [
    path('', get_predictions),
    path('data/', get_data),
]