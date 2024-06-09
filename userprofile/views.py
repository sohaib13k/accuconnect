from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ListFriendSerialiser, PendingRequestSerialiser
from .models import UserProfile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_friend(request):
    if (request.GET.get("pending-request") and request.GET.get("pending-request") == "True"):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = PendingRequestSerialiser(user_profile)
        return Response(serializer.data, status=200)

    user_profile = UserProfile.objects.get(user=request.user)
    serializer = ListFriendSerialiser(user_profile)
    return Response(serializer.data, status=200)
