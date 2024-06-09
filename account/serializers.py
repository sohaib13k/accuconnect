from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import CustomAccount
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import CustomAccount


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=False)

    class Meta:
        model = CustomAccount
        fields = ["username","email","first_name","last_name","gender","password","password2",]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"Password": "Passwords not matching"})
        return attrs

    def create(self, validated_data):
        user = CustomAccount.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data.get("gender", "X"),
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField("get_token")

    def get_token(self, obj):
        user = self.context.get("user")
        response = {}
        if user:
            refresh = RefreshToken.for_user(user)
            response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        return response

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            self.context["user"] = user
        else:
            raise serializers.ValidationError("invalid payload")
        
        return attrs
