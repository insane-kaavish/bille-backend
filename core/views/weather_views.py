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
    inferences.append(get_weekly_weather_inference(weekly_data))
    inferences.append(compare_weather())
    return Response(inferences, status=200)
