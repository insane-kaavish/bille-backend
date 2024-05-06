from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from ..models import *
from ..serializers import *
from ..utils.repopulate import *

# Create your views here.
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        }, status=201)
        
@api_view(['GET'])
@permission_classes([AllowAny],)
def example_view(request):
    return Response({'Welcome to Bill-E'}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny],)
def login_view(request):
    try:
        data = request.data
        email = data['email']
        password = data['password']
        user = authenticate(request, email=email, password=password)
    except MultiValueDictKeyError:
        return Response({'error': 'Email and password are required'}, status=400)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return Response({'login successfully'}, status = 200)
    else:
        # Return an 'invalid login' error message.
        return Response({'login failed'}, status = 401)
      
@api_view(['POST'])
@permission_classes([AllowAny],)  
def signup_view(request):
    data = request.data
    try:
        email = data['email']
        password = data['password']
        name = data['name']
        # split the name into first name and last name after the last space
        first_name = name.rsplit(' ', 1)[0] if ' ' in name else name
        last_name = name.rsplit(' ', 1)[1] if ' ' in name else ''
        ke_num = data['ke_num'] if 'ke_num' in data else ''
        user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, ke_num=ke_num)
    except IntegrityError:
        return Response({'error': 'User already exists'}, status=409)
    except KeyError:
        return Response({'error': 'Email, password are required'}, status=400)
    if user is not None:
        user.save()
        return Response({'user created successfully'}, status = 201)
    return Response({'user created failed'}, status = 500)


#api to contact-us, where the user gives name, email, and the message
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def message_view(request):
    data = request.data
    user = request.user 
    message = data['message']
    contact = Message.objects.create(user=user, message=message)
    if contact is not None:
        contact.save()
        return Response({'contact message saved successfully'}, status = 201)
    return Response({'contact message saved failed'}, status = 400)

# View to get the user details
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    user = request.user
    return Response({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'num_people': user.num_people,
        'ke_num': user.ke_num
    }, status=200)
    
# View to update the user details
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    user = request.user
    data = request.data
    name = data.get('name')
    if name:
        user.first_name = name.rsplit(' ', 1)[0] if ' ' in name else name
        user.last_name = name.rsplit(' ', 1)[1] if ' ' in name else ''
    user.email = data['email'] if 'email' in data else user.email
    user.num_people = data['num_people'] if 'num_people' in data else user.num_people
    user.ke_num = data['ke_num'] if 'ke_num' in data else user.ke_num
    user.save()
    return Response({'message': 'User details updated successfully'}, status=200)

#Complete thekedaar-hatao view for updating password, works great
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_password_view(request):
    user = request.user
    data = request.data
    old_password = data['old_password']
    new_password = data['new_password']
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=200)
    else:
        return Response({'message': 'Old password is incorrect.'}, status=400)
    
# View to store the input data such as number of people, stayathome, parttime, fulltime
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def input_view(request):
    data = request.data
    user = request.user

    # Extract data from request
    num_people = data.get('num_people', 0)
    rooms_data = data.get('rooms', [])

    # Update user's num_people value
    user.num_people = num_people
    user.save()

    # Process rooms data
    for room_data in rooms_data:
        # Extract room details
        tag = room_data.get('tag', '')
        room_tag = RoomTag.objects.get_or_create(tag=tag)[0]
        alias = room_data.get('alias', '')
        appliances_data = room_data.get('appliances', [])

        # Create room
        room = Room.objects.create(user=user, tag=room_tag, alias=alias)
        # Process appliances data
        for appliance_data in appliances_data:
            # Extract appliance details
            category_data = appliance_data.get('category')
            sub_category_data = appliance_data.get('sub_category')
            alias = appliance_data.get('alias', '')
            daily_usage = int(appliance_data.get('usage', 0))

            category, _ = Category.objects.get_or_create(name=category_data)
            sub_category, _ = SubCategory.objects.get_or_create(name=sub_category_data, category=category)
            appliance = Appliance.objects.create(room=room, category=sub_category.category, sub_category=sub_category, alias=alias, daily_usage=daily_usage)

            # Create usage record
            Usage.objects.create(appliance=appliance)
        
        Usage.objects.create(room=room)

    return Response({'message': 'Input data saved successfully'}, status=201)

  
# View to get tips for a specific appliance
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tips_view(request):
    appliance_id = request.query_params.get('appliance_id')
    appliance = Appliance.objects.get(id=appliance_id)
    category = appliance.category
    sub_category = appliance.sub_category
    tipcategories = TipCategory.objects.filter(category=category, sub_category=sub_category)
    tips = []
    for tip in tipcategories:
        tips.append({
            'title': tip.tip.title,
            'content': tip.tip.content
        })
    return Response(tips, status=200)

# Get the appliance with the highest usage in the house
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def highest_usage_view(request):
    user = request.user
    rooms = Room.objects.filter(user=user)
    highest_usage = 0
    highest_usage_appliance = None
    for room in rooms:
        appliances = Appliance.objects.filter(room=room)
        for appliance in appliances:
            usage = Usage.objects.filter(appliance=appliance).order_by('-usage').first()
            if usage is not None and usage.usage > highest_usage:
                highest_usage = usage.usage
                highest_usage_appliance = appliance
    if highest_usage_appliance is not None:
        return Response({
            'alias': highest_usage_appliance.alias,
            'category': highest_usage_appliance.category.name,
            'sub_category': highest_usage_appliance.sub_category.name,
            'usage': highest_usage
        }, status=200)
    return Response({'message': 'No appliances found'}, status=404)
