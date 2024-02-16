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
    user_id = request.user
    num_people = data['num_people']
    num_stayathome = data['num_stayathome']
    num_parttime = data['num_parttime']
    num_fulltime = data['num_fulltime']
    input = InputData.objects.create(num_people=num_people, num_stayathome=num_stayathome, num_parttime=num_parttime, num_fulltime=num_fulltime)
    if input is not None:
        input.save()
        return Response({'input saved successfully'}, status = 200)
    return Response({'input saved failed'}, status = 201)
