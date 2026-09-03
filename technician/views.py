from django.shortcuts import get_object_or_404
from .serializer import SentRequestSerializer
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
