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
    return Response({'Welcome to Bill-E'}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny],)
def login_view(request):
    data = request.data
    email = data['email']
    password = data['password']
    user = authenticate(request, email=email, password=password)
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
    # username = data['username']
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
    if user is not None:
        user.save()
        return Response({'user created successfully'}, status = 200)
    return Response({'user created failed'}, status = 201)

#api to contact-us, where the user gives name, email, and the message
@api_view(['POST'])
@permission_classes([AllowAny],)
def contact_us(request):
    data = request.data
    name = data['name']
    email = data['email']
    message = data['message']
    contact = ContactUs.objects.create(name=name, email=email, message=message)
    if contact is not None:
        contact.save()
        return Response({'contact saved successfully'}, status = 200)
    return Response({'contact saved failed'}, status = 201)