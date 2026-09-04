from rest_framework.serializers import ModelSerializer
from .models import RepairRequest
from authentication.serializers import CustomerSerializer


class RepairRequestSerializer(ModelSerializer):
    user = CustomerSerializer(read_only=True)

    class Meta:
        model = RepairRequest
        fields = '__all__'
        read_only_fields = ['created_on', 'user']
