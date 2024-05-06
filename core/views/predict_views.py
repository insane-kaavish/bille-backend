from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
        add_surcharge = calculate_additional_surcharge(units)
        total_cost = calculate_total_cost(units, per_unit_cost, prev_adj, add_surcharge)
        response = {
            'units': units,
            'per_unit_cost': per_unit_cost,
            'prev_adj': prev_adj,
            'total_cost': total_cost
        }
        return Response(response, status=200)
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
        if month_year_key not in monthwise_bills:
            monthwise_bills[month_year_key] = []
        monthwise_bills[month_year_key].append(bill.units)
    
    sorted_monthwise_keys = sorted(
        monthwise_bills.keys(),
        key=lambda x: (int(x.split('-')[1]), next((m[0] for m in MONTH_CHOICES if m[1] == x.split('-')[0]), None))
    )
    
    for key in sorted_monthwise_keys:
        monthwise_bills[key].sort()
    
    sorted_monthwise_bills = {key: monthwise_bills[key] for key in sorted_monthwise_keys}
    
    return Response({'monthwise_units': sorted_monthwise_bills}, status=200)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_monthly_adjustment_view(request):
    data = request.data
    try:
        month = data['month']
        adj_factor = data['adj_factor']
        monthly_adj = MonthlyAdjustment.objects.get(month=month)
        monthly_adj.adj_factor = adj_factor
        monthly_adj.save()
        return Response({'message': 'Monthly adjustment updated successfully'}, status=200)
    except KeyError:
        return Response({'error': 'Month and adj_factor are required'}, status=400)
    except MonthlyAdjustment.DoesNotExist:
        return Response({'error': 'Monthly adjustment not found'}, status=404)
    
# reset monthly adjustment factors to 0
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def reset_monthly_adjustment_view(request):
    for month, _ in MONTH_CHOICES:
        monthly_adj = MonthlyAdjustment.objects.get(month=month)
        monthly_adj.adj_factor = 0
        monthly_adj.save()
    return Response({'message': 'Monthly adjustment reset successfully'}, status=200)
