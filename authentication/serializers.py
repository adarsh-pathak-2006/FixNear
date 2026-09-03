from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .models import CustomerProfile, TechnicianProfile

User=get_user_model()

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'mobile_no', 'role', 'password']
        write_only_fields=['password']

class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'role']

class CustomerSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=CustomerProfile
        fields='__all__'
        read_only_fields=['created_on']


class TechnicianProfileSerializer(ModelSerializer):
    class Meta:
        model=TechnicianProfile
        fields='__all__'
        read_only_fields=['created_on']
