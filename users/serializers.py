from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import ConfirmationCode
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=100)
  password = serializers.CharField(max_length=100)
  
  

class UserRegisterSerializer(UserBaseSerializer):
  pass


class ConfirmationCodeSerializer(UserBaseSerializer):
  code = serializers.CharField(max_length=6)
  
  def validate_code(self, code):
    try:
      ConfirmationCode.objects.get(code=code)
    except ConfirmationCode.DoesNotExist:
      raise ValidationError("Code not found")
    
    return code
  
  

class UserAuthorizationSerializer(UserBaseSerializer):
  pass