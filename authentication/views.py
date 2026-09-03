from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomerProfile, TechnicianProfile
from .serializers import RegisterSerializer, CustomerSerializer, TechnicianProfileSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from fixnear.cache_key import customer_profile_key, technician_profile_key, technicianlist_key
from django.core.cache import cache
from fixnear.pagination import GeneralPagnination
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from fixnear.throttling import TokenObtainThrottle, TokenRefreshThrottle, RegistrationThrottle, GeneralThrottle
from fixnear.permissions import IsCustomer, IsTechnician, IsTechnicianAndCustomer
from rest_framework.permissions import AllowAny

User=get_user_model()

class CustomTokenObtainView(TokenObtainPairView):
    throttle_classes=[TokenObtainThrottle]

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes=[TokenRefreshThrottle]

class RegisterAPI(APIView):
    permission_classes=[AllowAny]
    throttle_classes=[RegistrationThrottle]    
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
    permission_classes=[IsCustomer]
    throttle_classes=[GeneralThrottle]
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
    permission_classes=[IsTechnician]
    throttle_classes=[GeneralThrottle]
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


class TechnicalProfileListAPI(APIView):
    permission_classes=[IsTechnicianAndCustomer]
    throttle_classes=[GeneralThrottle]
    def get(self, request):
        page_no=request.query_params.get("page", "1")
        key=technicianlist_key(page_no)
        cached_data=cache.get(key)
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagnination()
        data=paginator.paginate_queryset(TechnicianProfile.objects.select_related('user').filter(is_avaliable=True), request, view=self)
        serial=TechnicianProfileSerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(key, response.data, timeout=300)
        return response