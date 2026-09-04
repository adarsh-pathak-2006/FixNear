from django.shortcuts import get_object_or_404
from .serializers import SentRequestSerializer, RepairSerializer
from .models import SentRequest, Repair
from rest_framework.views import APIView
from rest_framework.response import Response
from fixnear.pagination import GeneralPagination
from fixnear.cache_key import repairrequest_list_key
from django.core.cache import cache
from fixnear.throttling import GeneralThrottle
from fixnear.permissions import IsTechnician


class AllRequestListAPI(APIView):
    permission_classes = [IsTechnician]
    throttle_classes = [GeneralThrottle]

    def get(self, request):
        pageno = request.query_params.get('page', '1')
        key = repairrequest_list_key(page_no=pageno, userid=request.user.id)
        cached_data = cache.get(key)
        if cached_data:
            return Response(cached_data, status=200)
        paginator = GeneralPagination()
        data = paginator.paginate_queryset(
            SentRequest.objects
            .select_related('technician__user', 'request')
            .filter(technician__user=request.user),
            request,
            view=self,
        )
        serial = SentRequestSerializer(data, many=True)
        response = paginator.get_paginated_response(serial.data)
        cache.set(key, response.data, timeout=300)
        return response


class RepairRequestAcceptAPI(APIView):
    permission_classes = [IsTechnician]
    throttle_classes = [GeneralThrottle]

    def patch(self, request, pk):
        instance = get_object_or_404(
            SentRequest.objects.select_related('technician__user', 'request'),
            id=pk,
            is_accepted=False,
            technician__user=request.user,
        )
        serial = SentRequestSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            updated = serial.save()
            if updated.is_accepted:
                Repair.objects.get_or_create(accepted_request=updated)
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        instance = get_object_or_404(
            SentRequest.objects.select_related('technician__user', 'request'),
            id=pk,
            is_accepted=False,
            technician__user=request.user,
        )
        instance.delete()
        return Response(status=204)


class RepairStatusUpdateAPI(APIView):
    permission_classes = [IsTechnician]
    throttle_classes = [GeneralThrottle]

    def patch(self, request, pk):
        instance = get_object_or_404(
            Repair.objects.select_related('accepted_request__technician__user'),
            id=pk,
            accepted_request__is_accepted=True,
            accepted_request__technician__user=request.user,
        )
        serial = RepairSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)