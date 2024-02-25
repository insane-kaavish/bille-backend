from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Room, Appliance, Usage

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
        total_usage = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance_id=appliance).order_by('-predict_date').first()
            total_usage += usage.units if usage is not None else 0 
        room_data.append({
            'id': room.id,
            'tag': room.tag,
            'alias': room.alias,
            'usage': total_usage,
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
            'tag': room.tag,
            'alias': room.alias,
            'appliances': []
        }
        total_usage = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()
            if usage is not None:
                total_usage += usage.units
            room_data['appliances'].append({
                'id': appliance.id,
                'alias': appliance.alias,
                'category': appliance.category,
                'sub_category': appliance.sub_category,
                'usage': usage.units if usage is not None else 0
            })
        room_data['usage'] = total_usage
        return Response(room_data, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    
# update the room
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_room_view(request):
    user = request.user
    data = request.data
    try:
        room_id = data['room_id']
        room = Room.objects.get(id=room_id)
        room.alias = data['alias'] if 'alias' in data else room.alias
        room.save()
        return Response({'message': 'Room updated successfully'}, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
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
