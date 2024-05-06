from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ..models import *
from ..utils.repopulate import *

# View to repopulate the database with categories, subcategories, room tags and monthly adjustments
@api_view(['POST'])
@permission_classes([IsAdminUser])
def repopulate_view(request):
    try:
        add_category_subcategory()
        add_room_tags()
        add_monthly_adjustments()
        add_tips()
        add_tips_categories()
        return Response({'message': 'Database repopulated successfully'}, status=200)
    except IntegrityError:
        return Response({'error': 'Database repopulation failed'}, status=500)
  
# reset monthly adjustment factors to 0
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def reset_monthly_adjustment_view(request):
    for month, _ in MONTH_CHOICES:
        monthly_adj = MonthlyAdjustment.objects.get(month=month)
        monthly_adj.adj_factor = 0
        monthly_adj.save()
    return Response({'message': 'Monthly adjustment reset successfully'}, status=200)

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
    