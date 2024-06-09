from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, LoginSerializer


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"}, status=205)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
