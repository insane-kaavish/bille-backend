from core.models import *
from ..utils.weather import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# View to get the weather data
@api_view(['GET'])
def current_weather_view(request):
    weather_data = get_current_weather_data()
    if 'error' in weather_data:
        return Response(weather_data, status=500)
    return Response(weather_data, status=200)

# View to get all the weather related inference
@api_view(['GET'])
def weather_inference_view(request):
    weekly_data = get_weekly_weather()
    if 'error' in weekly_data:
        return Response(weekly_data, status=500)
    inferences = []
    weekly_inference = get_weekly_weather_inference(weekly_data)
    compare_inference = compare_weather()
    if 'error' in weekly_inference:
        return Response(weekly_inference, status=500)
    if 'error' in compare_inference:
        return Response(compare_inference, status=500)
    inferences.append(weekly_inference)
    inferences.append(compare_inference)
    return Response(inferences, status=200)
