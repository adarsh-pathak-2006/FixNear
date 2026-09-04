from django.shortcuts import get_object_or_404
from .serializers import RepairRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import CustomerProfile
from fixnear.throttling import GeneralThrottle
from fixnear.permissions import IsCustomer


class RepairRequestAPI(APIView):
    permission_classes = [IsCustomer]
    throttle_classes = [GeneralThrottle]

    def post(self, request):
        serial = RepairRequestSerializer(data=request.data)
        if serial.is_valid():
            profile = get_object_or_404(
                CustomerProfile.objects.select_related('user'), user=request.user
            )
            serial.save(user=profile)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)
