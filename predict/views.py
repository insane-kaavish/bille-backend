from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import pickle
# Create your views here.

model = model_filename = 'ML/model.sav'
model = pickle.load(open(model_filename, 'rb'))
data = dict()

@api_view(['POST'])
@permission_classes([AllowAny],)
def get_data(request):
    data = request.data
    print(data)
    return Response({'data': data}, status = 201)

@api_view(['POST'])
@permission_classes([AllowAny],)
def get_predictions(request):
    data = request.data
    print(data)
    return Response({'predictions': model.predict(data)}, status = 201)