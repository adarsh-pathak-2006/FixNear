from django.shortcuts import get_object_or_404
from .serializer import RepairRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import CustomerProfile

class RepairRequestAPI(APIView):
    def post(self, request):
        serial=RepairRequestSerializer(data=request.data)
        if serial.is_valid():
            profile_data=get_object_or_404(CustomerProfile.objects.select_related('user'), user=request.user)
            serial.save(user=profile_data)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)

