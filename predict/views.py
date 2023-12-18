from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny],)
def get_predictions(request):
    return Response({'Welcome to Bill-E'}, status=200)