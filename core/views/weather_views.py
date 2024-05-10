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
def weekly_weather_inference_view(request):
    weekly_data = get_weekly_weather()
    if 'error' in weekly_data:
        return Response(weekly_data, status=500)
    weekly_inference = get_weekly_weather_inference(weekly_data)
    if 'error' in weekly_inference:
        return Response(weekly_inference, status=500)
    return Response(weekly_inference, status=200)

# View to get the current weather data vs the historical data
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def daily_weather_inference_view(request):
    user = request.user
    comparison_data = compare_weather()
    bill = Bill.objects.filter(user=user, is_predicted=False, month=datetime.now().month, year=datetime.now().year).first()
    if bill:
        comparison_data['new_bill'] = bill.units
        comparison_data['is_predicted'] = False
    else:
        comparison_data['new_bill'] = Bill.objects.filter(user=user, is_predicted=True, month=datetime.now().month, year=datetime.now().year).first().units
        comparison_data['is_predicted'] = True
    bill = Bill.objects.filter(user=user, is_predicted=False, month=datetime.now().month, year=datetime.now().year - 1).first()
    if bill:
        comparison_data['old_bill'] = bill.units
    if 'error' in comparison_data:
        return Response(comparison_data, status=500)
    return Response(comparison_data, status=200)
