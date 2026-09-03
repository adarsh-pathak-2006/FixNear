from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomerProfile, TechnicianProfile, TechnicalSkill
from .serializers import RegisterSerializer, CustomerSerializer, TechnicianProfileSerializer, TechnicalSkillSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from fixnear.cache_key import customer_profile_key, technician_profile_key
from django.core.cache import cache

User=get_user_model()

class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data['username']
            email=serial.validated_data['email']
            role=serial.validated_data['role']
            mobile_no=serial.validated_data['mobile_no']
            password=serial.validated_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email) | Q(mobile_no=mobile_no)).exists():
                return Response({'message':'username, email or mobile_no already exists'}, status=400)
            User.objects.create_user(username=username, email=email, role=role, mobile_no=mobile_no, password=password)
            return Response({'message':'user registered successfully'}, status=201)
        return Response(serial.errors, status=400)

class MyCustomerProfile(APIView):
    def get(self, request):
        key=customer_profile_key(request.user.id)
        cached_data=cache.get(key=key)
        if cached_data:
            return Response(cached_data, status=200)
        data=get_object_or_404(CustomerProfile.objects.select_related('user'), user=request.user)
        serial=CustomerSerializer(data)
        cache.set(key, serial.data, timeout=300)
        return Response(serial.data, status=200)

    def patch(self, request):
        instance=get_object_or_404(CustomerProfile.objects.select_related('user'), user=request.user)
        serial=CustomerSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)


class MyTechnicianProfile(APIView):
    def get(self, request):
        key=technician_profile_key(request.user.id)
        cached_data=cache.get(key=key)
        if cached_data:
            return Response(cached_data, status=200)
        data=get_object_or_404(TechnicianProfile.objects.select_related('user'), user=request.user)
        serial=TechnicianProfileSerializer(data)
        cache.set(key, serial.data, timeout=300)
        return Response(serial.data, status=200)

    def patch(self, request):
        instance=get_object_or_404(TechnicianProfile.objects.select_related('user'), user=request.user)
        serial=TechnicianProfileSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)


class TechnicalSkillAPI(ListCreateAPIView):
    serializer_class=TechnicalSkillSerializer
    def get_queryset(self):
        return TechnicalSkill.objects.select_related('user__user').filter(user__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user__user=self.request.user)

class TechnicalSkillDetailAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=TechnicalSkillSerializer
    def get_queryset(self):
        return TechnicalSkill.objects.select_related('user__user').filter(user__user=self.request.user)   