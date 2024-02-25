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
import random

from ..models import *
from ..serializers import *
from ..scraper import scrape, read_pdf

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
        return Response({'login successfully'}, status = 201)
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
        first_name = data['first_name'] if 'first_name' in data else ''
        last_name = data['last_name'] if 'last_name' in data else ''
        user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        return Response({'error': 'User already exists'}, status=400)
    except KeyError:
        return Response({'error': 'Email, password are required'}, status=400)
    if user is not None:
        user.save()
        return Response({'user created successfully'}, status = 200)
    return Response({'user created failed'}, status = 201)


#api to contact-us, where the user gives name, email, and the message
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def message_view(request):
    data = request.data
    user_id = request.user 
    message = data['message']
    contact = Message.objects.create(user_id= user_id, message=message)
    if contact is not None:
        contact.save()
        return Response({'contact message saved successfully'}, status = 200)
    return Response({'contact message saved failed'}, status = 201)

# View to update the user details
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_view(request):
    user = request.user
    data = request.data
    user.first_name = data['first_name'] if 'first_name' in data else user.first_name
    user.last_name = data['last_name'] if 'last_name' in data else user.last_name
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
    num_people = data.get('num_people')
    rooms_data = data.get('rooms', [])

    # Update user's num_people value
    user.num_people = num_people
    user.save()

    # Process rooms data
    for room_data in rooms_data:
        # Extract room details
        tag = room_data.get('tag')
        alias = room_data.get('alias')
        appliances_data = room_data.get('appliances', [])

        # Create room
        room = Room.objects.create(user_id=user, tag=tag, alias=alias)

        total_usage = 0

        # Process appliances data
        for appliance_data in appliances_data:
            # Extract appliance details
            category = appliance_data.get('category')
            sub_category = appliance_data.get('sub_category')
            alias = appliance_data.get('alias')
            usage = appliance_data.get('usage')
            total_usage += int(usage)

            # Create appliance
            appliance = Appliance.objects.create(room_id=room, category=category, sub_category=sub_category ,alias=alias)

            # Create usage record
            Usage.objects.create(appliance_id=appliance, units=usage)
        
        Usage.objects.create(room_id=room, units=total_usage)

    return Response({'message': 'Input data saved successfully'}, status=200)


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
        bill = Bill.objects.filter(user_id=user, month=month, year=year, is_predicted=True)
        if bill:
            return Response({'units': bill[0].units}, status=200)
        else:
            # TODO: Predict units and return
            units = random.randint(100, 500)
            bill = Bill.objects.create(user_id=user, month=month, year=year, units=units, is_predicted=True)
            bill.save()
            return Response({'units': units}, status=200)
            return Response({'error': 'No bills found for the current user'}, status=404)
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
    bills = Bill.objects.filter(user_id=user)
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scrape_view(request):
    try:
        user = request.user
        print('Trying to scrape')
        if not user.ke_num:
            return Response({'error': 'KE number not found'}, status=400)
        response = scrape(user.ke_num)
        if response.status_code == 501:
            response = scrape(user.ke_num)
        units = read_pdf()
        if len(units):
            # store the units in the database
            for month, unit in units.items():
                # separate month and year from 'jan-23'
                month, year = month.split('-')
                month = month.capitalize()
                month = next((m[0] for m in MONTH_CHOICES if m[1] == month), None)
                year = int(year) + 2000
                # create a bill object only if the bill does not exist
                if not Bill.objects.filter(user_id=user, month=month, year=year, is_predicted=False).exists():
                    bill = Bill.objects.create(user_id=user, month=month, year=year, units=unit, is_predicted=False)
                    bill.save()               
            return Response({'message': 'Scraping successful'}, status=200)
        return Response({'message': 'Scraping failed'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
        