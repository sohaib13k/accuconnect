from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    ListFriendSerialiser, PendingRequestSerialiser, SendRequestSerialiser, 
    AcceptRequestSerialiser, RejectRequestSerialiser,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_friend(request):
    if request.GET.get("friend-request") and request.GET.get("friend-request") == "pending":
        serializer = PendingRequestSerialiser()
        return Response(serializer.data, status=200)

    if request.GET.get("friend-request"):
        if not request.GET.get("email"):
            return Response(status=400)
        
        if request.GET.get("friend-request") == "send":
            serializer = SendRequestSerialiser(data=request.data, context={"request": request})     
        elif request.GET.get("friend-request") == "accept":
            serializer = AcceptRequestSerialiser(data=request.data, context={"request": request})
        elif request.GET.get("friend-request") == "reject":
            serializer = RejectRequestSerialiser(data=request.data, context={"request": request})

        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    else:
        serializer = ListFriendSerialiser()
        return Response(serializer.data, status=200)
