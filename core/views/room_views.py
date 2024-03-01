from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Room, Appliance, Usage, RoomTag, Category, SubCategory
import math

# View to get all the rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rooms_view(request):
    user = request.user
    rooms = Room.objects.filter(user=user)
    room_data = []
    for room in rooms:
        appliances = Appliance.objects.filter(room=room)
        total_units = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance_id=appliance).order_by('-predict_date').first()
            total_units += usage.units if usage is not None else 0 
        room_data.append({
            'id': room.id,
            'tag': room.tag.tag,
            'alias': room.alias,
            'units': total_units,
        })
    return Response(room_data, status=200)

# View to get a particular room
# FIXME: This view is not working as expected
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def room_view(request):
    room_id = request.query_params.get('room_id') 
    try:
        room = Room.objects.get(id=room_id)
        appliances = Appliance.objects.filter(room=room)
        room_data = {
            'id': room.id,
            'tag': room.tag.tag,
            'alias': room.alias,
            'appliances': []
        }
        total_units = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()
            if usage is not None:
                total_units += usage.units
            room_data['appliances'].append({
                'id': appliance.id,
                'alias': appliance.alias,
                'category': appliance.category.name,
                'sub_category': appliance.sub_category.name if appliance.sub_category is not None else None,
                'units': usage.units if usage is not None else 0
            })
        room_data['units'] = total_units
        return Response(room_data, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    
# update the room and appliance
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_room_view(request):
    user = request.user
    data = request.data
    try:
        room_id = data['room_id']
        room = Room.objects.get(id=room_id)
        room.alias = data.get('alias', room.alias)
        room.tag = RoomTag.objects.get(tag=data.get('tag', room.tag.tag))
        room.save()

        appliances_data = data.get('appliances', [])
        for appliance_data in appliances_data:
            appliance_id = appliance_data.get('id')
            if appliance_id is None:
                # Create a new appliance
                category, _ = Category.objects.get_or_create(name=appliance_data.get('category'))
                sub_category, _ = SubCategory.objects.get_or_create(name=appliance_data.get('sub_category'), category=category)
                appliance = Appliance.objects.create(
                    alias=appliance_data.get('alias'),
                    category=category,
                    sub_category=sub_category
                )
            else:
                # Update existing appliance
                appliance = Appliance.objects.get(id=appliance_id)
                appliance.alias = appliance_data.get('alias', appliance.alias)
                category, _ = Category.objects.get_or_create(name=appliance_data.get('category', appliance.category.name))
                sub_category = appliance_data.get('sub_category')
                if sub_category is not None:
                    sub_category, _ = SubCategory.objects.get_or_create(name=sub_category, category=category)
                    appliance.sub_category = sub_category
                appliance.save()
            
            # Create a new usage record for the appliance
            units = math.ceil(appliance_data.get('usage', 0) * appliance.wattage / 1000)
            usage = Usage.objects.create(appliance=appliance, units=units)
            usage.save()
            
        appliances = Appliance.objects.filter(room=room)
        total_units = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()
            total_units += usage.units if usage is not None else 0
        
        # Create a new usage record for the room
        room_usage = Usage.objects.create(room=room, units=total_units)
        room_usage.save()

        return Response({'message': 'Room and appliance updated successfully'}, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    except Appliance.DoesNotExist:
        return Response({'error': 'Appliance not found'}, status=404)
    except KeyError:
        return Response({'error': 'Room ID is required'}, status=400)

# delete the room
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_room_view(request):
    user = request.user
    room_id = request.query_params.get('room_id')
    try:
        room = Room.objects.get(id=room_id)
        room.delete()
        return Response({'message': 'Room deleted successfully'}, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
