from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    ListFriendSerialiser, PendingRequestSerialiser, SendRequestSerialiser, 
    AcceptRequestSerialiser, RejectRequestSerialiser, FindFriendSerialser
)
from .models import UserProfile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def find_friend(request):
    search_string = request.query_params.get("search-string")
    if not search_string:
        return Response(status=400)

    request_profile = UserProfile.objects.filter(user__email=search_string).first()
    
    if request_profile:
        serializer = FindFriendSerialser(request_profile)
        return Response(serializer.data, status=200)
    else:
        request_profile = UserProfile.objects.annotate(
            full_name=Concat('user__first_name', V(' '), 'user__last_name')
        ).filter(Q(full_name__icontains=search_string)).distinct()

        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_profiles = paginator.paginate_queryset(request_profile, request)
        serializer = FindFriendSerialser(paginated_profiles, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_friend(request):
    if request.query_params.get("friend-request") and request.query_params.get("friend-request") == "pending":
        serializer = PendingRequestSerialiser()
        return Response(serializer.data, status=200)

    if request.query_params.get("friend-request"):
        if not request.query_params.get("email"):
            return Response(status=400)
        
        if request.query_params.get("friend-request") == "send":
            serializer = SendRequestSerialiser(data=request.data, context={"request": request})     
        elif request.query_params.get("friend-request") == "accept":
            serializer = AcceptRequestSerialiser(data=request.data, context={"request": request})
        elif request.query_params.get("friend-request") == "reject":
            serializer = RejectRequestSerialiser(data=request.data, context={"request": request})

        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    else:
        serializer = ListFriendSerialiser()
        return Response(serializer.data, status=200)
