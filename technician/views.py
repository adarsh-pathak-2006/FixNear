from django.shortcuts import get_object_or_404
from .serializer import SentRequestSerializer, RepairSerializer
from .models import SentRequest, Repair
from rest_framework.views import APIView
from rest_framework.response import Response
from fixnear.pagination import GeneralPagnination
from fixnear.cache_key import repairrequest_list_key
from django.core.cache import cache

class AllRequestListAPI(APIView):
    def get(self, request):
        pageno=request.query_params.get("page", "1")
        key=repairrequest_list_key(page_no=pageno, userid=request.user.id)
        cached_data=cache.get(key)
        if cached_data:
            return Response(cached_data, status=200)
        paginator=GeneralPagnination()
        data=paginator.paginate_queryset(SentRequest.objects.select_related('technician__user', 'request').filter(technician__user=request.user), request, view=self)
        serial=SentRequestSerializer(data, many=True)
        response=paginator.get_paginated_response(serial.data)
        cache.set(key, response.data, timeout=300)
        return response

class RepairRequestAcceptAPI(APIView):
    def patch(self, request, pk):
        instance=get_object_or_404(SentRequest.objects.select_related('technician__user', 'request'), is_accepted=False, id=pk)
        serial=SentRequestSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            Repair.objects.create(accepted_request=instance)
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        instance=get_object_or_404(SentRequest.objects.select_related('technician__user', 'request'), is_accepted=False, id=pk)
        instance.delete()
        return Response(status=204)

class RepairStatusUpdateAPI(APIView):
    def patch(self, request, pk):
        instance=get_object_or_404(Repair.objects.select_related('accepted_request'), accepted_request__is_accepted=True, id=pk)
        serial=RepairSerializer(instance, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)