from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
import random
import os
import requests

from ..models import Bill, MonthlyAdjustment
from ..models import MONTH_CHOICES
from ..utils.predict import *

# View to get the amount of units predicted from the Bill model
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def predict_view(request):
    user = request.user
    try:
        bill = Bill.objects.filter(user=user, is_predicted=True).order_by('-year', '-month').first()
        units = bill.units
        month = bill.month
        per_unit_cost = calculate_per_unit_cost(units, month)
        prev_adj = calculate_previous_adjustment(user)
        add_surcharge = units * 0.43
        cost = units * per_unit_cost + prev_adj + add_surcharge
        taxes = cost*(0.015 + 0.17)
        total_cost = cost + taxes + 35
        if total_cost >= 25000:
            total_cost *= 1.07
        slab = (units // 100) * 100
        response = {
            'units': units,
            'per_unit_cost': per_unit_cost,
            'prev_adj': int(prev_adj),
            'total_cost': int(total_cost),
            'tv_fees': 35,
            'taxes': int(taxes),
            'add_surcharge': int(add_surcharge),
            'slab': slab
        }
        return Response(response, status=200)
    except AttributeError:
        return Response({'error': 'No predicted units found'}, status=404)
    except Bill.DoesNotExist:
        return Response({'error': 'Bill not found for the current user'}, status=404)
    except KeyError:
        return Response({'error': 'Month and year are required'}, status=400)

# View to get month-wise units for bar graph
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def months_view(request):
    user = request.user
    is_predicted = request.query_params.get('is_predicted', False)
    bills = Bill.objects.filter(user=user)
    bills = bills.filter(is_predicted=is_predicted)
    
    monthwise_bills = {}
    for bill in bills:
        month_year_key = f"{bill.get_month_display()}-{bill.year}"
        monthwise_bills[month_year_key] = bill.units
    
    sorted_monthwise_keys = sorted(
        monthwise_bills.keys(),
        key=lambda x: (int(x.split('-')[1]), next((m[0] for m in MONTH_CHOICES if m[1] == x.split('-')[0]), None))
    )
    
    sorted_monthwise_bills = {key: monthwise_bills[key] for key in sorted_monthwise_keys}
    
    return Response({'monthwise_units': sorted_monthwise_bills}, status=200)

# View to send the latest forcast
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def forcast_view(request):
    user = request.user
    try:
        forcast, _ = store_predicted_units(user)
        print("Forcast: ", forcast)
        return Response({'units': forcast}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
# View to send the latest predicted and previous all non predicted units as a single list with the latest being the prediction
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bar_graph_view(request):
    user = request.user
    try:
        units = []
        for bill in Bill.objects.filter(user=user, is_predicted=False).order_by('year', 'month'):
            units.append(bill.units)
        forcast, month = store_predicted_units(user)
        units.append(int(forcast[-1]))
        # FIXME year is hardcoded to 2024
        return Response({'units': units, 'month': month, 'year': 2024}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    