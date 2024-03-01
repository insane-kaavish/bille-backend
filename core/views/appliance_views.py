from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Appliance, Usage, Room, Category, SubCategory

# View to get all the appliances
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def appliances_view(request):
    user = request.user
    # find all the rooms of the user
    rooms = Room.objects.filter(user=user)
    appliances = Appliance.objects.filter(room__in=rooms)
    appliance_data = []
    for appliance in appliances:
        usage = Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()
        appliance_data.append({
            'id': appliance.id,
            'room_id': appliance.room.id,
            'alias': appliance.alias,
            'category': appliance.category,
            'sub_category': appliance.sub_category,
            'usage': usage.units if usage is not None else 0
        })
    return Response(appliance_data, status=200)

# View to get a particular appliance
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def appliance_view(request):
    appliance_id = request.query_params.get('appliance_id')
    try:
        appliance = Appliance.objects.get(id=appliance_id)
        usage = Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()
        return Response({
            'id': appliance.id,
            'alias': appliance.alias,
            'category': appliance.category,
            'sub_category': appliance.sub_category,
            'usage': usage.units if usage is not None else 0
        }, status=200)
    except Appliance.DoesNotExist:
        return Response({'error': 'Appliance not found'}, status=404)
    
# View to update the appliance
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_appliance_view(request):
    user = request.user
    data = request.data
    try:
        appliance_id = data['appliance_id']
        appliance = Appliance.objects.get(id=appliance_id)
        appliance.alias = data['alias'] if 'alias' in data else appliance.alias
        category, _ = Category.objects.get_or_create(name=data.get('category', appliance.category.name))
        sub_category = data.get('sub_category')
        if sub_category is not None:
            sub_category, _ = SubCategory.objects.get_or_create(name=sub_category, category=category)
            appliance.sub_category = sub_category
        appliance.save()
        return Response({'message': 'Appliance updated successfully'}, status=200)
    except Appliance.DoesNotExist:
        return Response({'error': 'Appliance not found'}, status=404)
    except KeyError:
        return Response({'error': 'Appliance ID is required'}, status=400)
    
# View to delete the appliance
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_appliance_view(request):
    user = request.user
    appliance_id = request.query_params.get('appliance_id')
    try:
        appliance = Appliance.objects.get(id=appliance_id)
        appliance.delete()
        return Response({'message': 'Appliance deleted successfully'}, status=200)
    except Appliance.DoesNotExist:
        return Response({'error': 'Appliance not found'}, status=404)


# View to get all the categories
@api_view(['GET'])
@permission_classes([AllowAny],)  
def categories_view(request):
    categories = Category.objects.all()
    category_data = []
    for category in categories:
        category_data.append({
            'name': category.name,
            'sub_categories': [sub_category.name for sub_category in SubCategory.objects.filter(category=category)]
        })
    return Response(category_data, status=200)
