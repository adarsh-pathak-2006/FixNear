from rest_framework.serializers import ModelSerializer
from .models import SentRequest, Repair
from authentication.serializers import TechnicianProfileSerializer
from customer.serializers import RepairRequestSerializer


class SentRequestSerializer(ModelSerializer):
    technician = TechnicianProfileSerializer(read_only=True)
    request = RepairRequestSerializer(read_only=True)

    class Meta:
        model = SentRequest
        fields = '__all__'
        read_only_fields = ['created_on', 'technician', 'request']


class RepairSerializer(ModelSerializer):
    accepted_request = SentRequestSerializer(read_only=True)

    class Meta:
        model = Repair
        fields = '__all__'
        read_only_fields = ['updated_on', 'accepted_request']
