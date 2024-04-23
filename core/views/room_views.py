from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Room, Appliance, Usage, RoomTag, Category, SubCategory, Bill
from ..utils.helper import *

# View to get all the rooms
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rooms_view(request):
    user = request.user
    rooms = Room.objects.filter(user=user)
    room_data = []
    total_units = 0
    for room in rooms:
        room_units = get_latest_usage(room=room).units if get_latest_usage(room=room) else 0
        total_units += room_units
        room_data.append({
            'id': room.id,
            'tag': room.tag.tag,
            'alias': room.alias,
            'units': get_latest_usage(room=room).units if get_latest_usage(room=room) else 0,
        })
    current_units = Bill.objects.filter(user=user, is_predicted=True).latest('year', 'month').units
    # Normalize the room units according to the total units
    for room in room_data:
        room['units'] = round(current_units * room['units'] / total_units)
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
        appliances = room.appliance_set.all()
        appliances_data = [{
            'id': appliance.id,
            'alias': appliance.alias,
            'category': appliance.category.name,
            'sub_category': appliance.sub_category.name if appliance.sub_category else None,
            'daily_usage': appliance.daily_usage,
            'units': get_latest_usage(appliance=appliance).units if get_latest_usage(appliance=appliance) else 0
        } for appliance in appliances]
        return Response({
            'id': room.id,
            'tag': room.tag.tag,
            'alias': room.alias,
            'appliances': appliances_data,
            'units': get_latest_usage(room=room).units if get_latest_usage(room=room) else 0
        }, status=200)

    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    
# update the room and appliance
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_room_view(request):
    try:
        room_id = request.query_params.get('room_id')
        room = Room.objects.get(id=room_id, user=request.user)  # Ensure the room belongs to the user
        data = request.data
        room.alias = data.get('alias', room.alias)
        room.tag = RoomTag.objects.get(tag=data.get('tag', room.tag.tag))
        room.save()
        for appliance_data in data.get('appliances', []):
            appliance_id = appliance_data.get('id')
            if appliance_id:
                appliance = Appliance.objects.get(id=appliance_id, room=room)
                update_appliance_data(appliance, appliance_data)
            else:
                # Create new appliance
                category, sub_category = get_or_create_category_sub_category(appliance_data['category'], appliance_data.get('sub_category'))
                appliance = Appliance.objects.create(room=room, alias=appliance_data['alias'], category=category, sub_category=sub_category, daily_usage=appliance_data['daily_usage'])
            Usage.objects.create(appliance=appliance)  
              
        Usage.objects.create(room=room)
        return Response({'message': 'Room and appliances updated successfully'}, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    except RoomTag.DoesNotExist:
        return Response({'error': 'Invalid room tag'}, status=400)
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

# View to get all the tags
@api_view(['GET'])
@permission_classes([AllowAny],)  
def room_tags_view(request):
    tags = RoomTag.objects.all()
    tag_data = []
    for tag in tags:
        tag_data.append({
            'tag': tag.tag,
            'description': tag.description
        })
    return Response(tag_data, status=200)
