from rest_framework.serializers import ModelSerializer
from .models import RepairRequest
from authentication.models import CustomerProfile

class RepairRequestSerializer(ModelSerializer):
    user=CustomerProfile(read_only=True)
    class Meta:
        model=RepairRequest
        fields='__all__'
        read_only_fields=['created_on']