from rest_framework import serializers
from .models import UserProfile
from account.models import CustomAccount


class SendRequestSerialiser(serializers.Serializer):
    def validate(self, attrs):
        request = self.context.get("request")
        user = UserProfile.objects.get(user=request.user)
        request_profile = UserProfile.objects.filter(user__email=request.GET.get("email")).first()

        if not request_profile:
            raise serializers.ValidationError({"User": "User not exist"})

        if user.friends.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "Already a friend"})

        if user.sent_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "Friend request already sent"})
        
        if user.pending_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "The profile has already sent you a request"})

        user.sent_requests.add(request_profile)
        request_profile.pending_requests.add(user)
        user.save()
        request_profile.save()

        return attrs


class PendingRequestSerialiser(serializers.ModelSerializer):
    pending_requests = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ["pending_requests"]


class ListFriendSerialiser(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ["friends"]
