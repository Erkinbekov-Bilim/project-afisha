from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import ConfirmationCode
from .serializers import UserRegisterSerializer, UserAuthorizationSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.


@api_view(['POST'])
def registration_api_view(request):
  
  
  serializer = UserRegisterSerializer(data = request.data)
  serializer.is_valid(raise_exception=True)
  
  
  user = User.objects.create_user(**serializer.validated_data, is_active = False)
  code = ConfirmationCode.objects.create(user = user)

  print(code.code)
  
  return Response(status=status.HTTP_201_CREATED, data= {'user_id': user.id ,'code': code.code})


@api_view(['POST'])
def confirmation_api_view(request):
  
  serializer = ConfirmationCodeSerializer(data = request.data)
  serializer.is_valid(raise_exception=True)
  
  username = serializer.validated_data.get('username')
  confirmation_code = serializer.validated_data.get('code')
  
  try:
    user = User.objects.get(username = username)
    confirm = ConfirmationCode.objects.get(user = user)
    
    if confirm.code == confirmation_code:
      user.is_active = True
      user.save()
      
      return Response(status=status.HTTP_200_OK, data = {'user_id': user.id})
    
    return Response(status=status.HTTP_400_BAD_REQUEST, data = {'error': 'Code is not valid'})
    
  except (ConfirmationCode.DoesNotExist, User.DoesNotExist):
    return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def authorization_api_view(request):
  
  print(request.user)
  serializer = UserAuthorizationSerializer(data = request.data)
  serializer.is_valid(raise_exception=True)
  
  user = authenticate(**serializer.validated_data)
  
  if user: 
    
    token, created = Token.objects.get_or_create(user = user)
    
    return Response(data = {'token': token.key})

  return Response(status=status.HTTP_401_UNAUTHORIZED)