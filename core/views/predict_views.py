from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
import random
import os
import requests

from ..models import Bill, MonthlyAdjustment
from ..models import MONTH_CHOICES

# View to get the amount of units predicted from the Bill model
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def predict_view(request):
    user = request.user # Get the ID of the current user
    data = request.data
    try:
        month = data['month']
        month = next((m[0] for m in MONTH_CHOICES if m[1] == month), None)
        year = data['year']
        bill = Bill.objects.filter(user=user, month=month, year=year, is_predicted=True)
        if bill:
            units = bill[0].units
        else:
            url = os.environ.get('AZURE_INFERENCE_URL')
            token = os.environ.get('AZURE_BEARER_TOKEN')
            # get the units of the previous 17 months
            bills = Bill.objects.filter(user=user, is_predicted=False).order_by('-year', '-month')[:17]
            # if bills dont exist, return 0
            if not bills:
                units = 0
            else:
                units = [bill.units for bill in bills]
                # Prepare the data to send in the request body
                data =  {
                    "input_data": {
                        "columns": [
                        "Aug-22",
                        "Sep-22",
                        "Oct-22",
                        "Nov-22",
                        "Dec-22",
                        "Jan-23",
                        "Feb-23",
                        "Mar-23",
                        "Apr-23",
                        "May-23",
                        "Jun-23",
                        "Jul-23",
                        "Aug-23",
                        "Sep-23",
                        "Oct-23",
                        "Nov-23",
                        "Dec-23"
                        ],
                        "index": [0],
                        "data": []
                        }
                    }
                data['input_data']['data'].append(units)
                headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ token)}
                # Make the POST request to the Azure ML model
                response = requests.post(url, json=data, headers=headers)
                print(response.json())
                # Check if the request was successful
                if response.status_code == 200:
                    # Get the predicted units from the response
                    units = response.json()[0]
                else:
                    # Handle the error case
                    # Set a default value for units
                    units = 0
                bill = Bill.objects.create(user=user, month=month, year=year, units=units, is_predicted=True)
                bill.save()
        if units <= 100:
            per_unit_cost = 10.00
        elif units <= 200:
            per_unit_cost = 15.00
        elif units <= 300:
            per_unit_cost = 20.00
        elif units <= 400:
            per_unit_cost = 25.00
        else:
            per_unit_cost = 30.00
        per_unit_cost += MonthlyAdjustment.objects.get(month=month).adj_factor
        # find the previous 12 months and apply the adjustment factor
        prev_bills = Bill.objects.filter(user=user, is_predicted=False).order_by('-year', '-month')[:12]
        prev_adj = 0
        for prev_bill in prev_bills:
            prev_adj += prev_bill.units * MonthlyAdjustment.objects.get(month=prev_bill.month).adj_factor
        # Additional surcharge
        add_surcharge = units * 0.43
        total_cost = units * per_unit_cost + prev_adj + add_surcharge
        
        # 1.5% Electricity duty, 17% sales tax and 35rs TV fees
        total_cost *= (0.015 + 0.17) + 35
        if total_cost >= 25000:
            # Income tax for residential consumers
            total_cost *= 1.07
        response = {
            'units': units,
            'per_unit_cost': per_unit_cost,
            'prev_adj': prev_adj,
            'total_cost': units * per_unit_cost + prev_adj
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
