from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics

from django.shortcuts import render,redirect
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User

from .scraper import process_single_pdf, scrape, read_pdf

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'first_name': user.first_name,
            'email': user.email
        }, status=201)
        
@api_view(['GET'])
@permission_classes([AllowAny],)
def example_view(request):
    return Response({'Welcome to Thekedaar Hatao'}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny],)
def login_view(request):
    data = request.data
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password)
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
    username = data['username']
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
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
    # email = data['email']
    message = data['message']
    contact = Message.objects.create(user_id= user_id, message=message)
    if contact is not None:
        contact.save()
        return Response({'contact message saved successfully'}, status = 200)
    return Response({'contact message saved failed'}, status = 201)

#Complete thekedaar-hatao view for updating password, works great
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updatePassword_view(request):
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
    
# Separate view to update username
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUsername_view(request):
    user = request.user
    data = request.data
    new_username = data.get('new_username')  # Fetch new_username from request data

    # Check if new_username is provided
    if not new_username:
        return Response({'message': 'New username is required.'}, status=400)

    # Check if the new_username is already taken by another user
    if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
        return Response({'message': 'Username is already taken.'}, status=400)

    # Update the username
    user.username = new_username
    user.save()

    return Response({'message': 'Username updated successfully.'}, status=200)

# View to store the input data such as number of people, stayathome, parttime, fulltime
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def inputdata_view(request):
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
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def predictedUnit_view(request):
    user_id = request.user # Get the ID of the current user
    try:
        bill = Bill.objects.filter(user_id=user_id).order_by('-year', '-month').first()
        if bill is not None:
            predicted_units = {
                'units': bill.units
            }
            return Response(predicted_units, status=200)
        else:
            return Response({'error': 'No bills found for the current user'}, status=404)
    except Bill.DoesNotExist:
        return Response({'error': 'Bill not found for the current user'}, status=404)
    
# View to get month-wise units for bar graph
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def monthwiseUnits_view(request):
    user_id = request.user
    
    # Fetch bills for the current user
    bills = Bill.objects.filter(user_id=user_id)
    
    # Group bills by month and year
    monthwise_bills = {}
    for bill in bills:
        month_year_key = f"{bill.get_month_display()}-{bill.year}"
        if month_year_key not in monthwise_bills:
            monthwise_bills[month_year_key] = []
        monthwise_bills[month_year_key].append(bill.units)
    
    # Sort keys by year and month
    sorted_monthwise_keys = sorted(
    monthwise_bills.keys(),
    key=lambda x: (int(x.split('-')[1]), next((m[0] for m in Bill.MONTH_CHOICES if m[1] == x.split('-')[0]), None)))

    
    # Sort units within each group
    for key in sorted_monthwise_keys:
        monthwise_bills[key].sort()
    
    # Create the final response dictionary
    sorted_monthwise_bills = {key: monthwise_bills[key] for key in sorted_monthwise_keys}
    
    return Response({'monthwise_units': sorted_monthwise_bills}, status=200)

# View to get the units of a particular room
'''
The view is currently not giving the correct room units from the Usage model by querying on the room_id
'''
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def roomwiseUnits_view(request):
    # user_id = request.user
    room_id = request.query_params.get('room_id') 
    try:
        room = Room.objects.get(id=room_id)
        appliances = Appliance.objects.filter(room_id=room)
        units = 0
        for appliance in appliances:
            usage = Usage.objects.filter(appliance_id=appliance).order_by('-predict_date').first()
            if usage is not None:
                units += usage.units
        return Response({'units': units}, status=200)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scrape_view(request):
    # Assume web scraper called for user.ke_num
    try:
        print('Trying to scrape')
        response = scrape('0400000081726')
        while response.status_code == 500:
            response = scrape('0400000081726')
        units = read_pdf()
        if units: return Response({'message': 'Scraping successful'}, status=200)
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
        