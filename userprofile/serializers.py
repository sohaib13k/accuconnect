from rest_framework import serializers
from .models import UserProfile
from django.utils import timezone


class FindFriendSerialser(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "first_name", "last_name"]


class SendRequestSerialiser(serializers.Serializer):
    def validate(self, attrs):
        request = self.context.get("request")
        user = UserProfile.objects.get(user=request.user)
        request_profile = UserProfile.objects.filter(user__email=request.query_params.get("email")).first()
        now = timezone.now()

        if user.sent_request_count >= 3 and (now - user.sent_request_tmstmp).total_seconds() < 60:
            raise serializers.ValidationError({"User": "Sending request too frequent. Only 3 req/mnt allowed"})

        if not request_profile:
            raise serializers.ValidationError({"User": "User not exist"})

        if user.friends.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "Already a friend"})

        if user.sent_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "Friend request already sent"})
        
        if user.pending_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "The profile has already sent you a request"})

        user.sent_requests.add(request_profile)
        
        if user.sent_request_count == 0:
            user.sent_request_count+=1
            user.sent_request_tmstmp = now
        elif user.sent_request_count >= 3:
            user.sent_request_count = 1
            user.sent_request_tmstmp = now
        else:
            user.sent_request_count+=1
        user.save()

        request_profile.pending_requests.add(user)
        request_profile.save()

        return attrs


class AcceptRequestSerialiser(serializers.Serializer):
    def validate(self, attrs):
        request = self.context.get("request")
        user = UserProfile.objects.get(user=request.user)
        request_profile = UserProfile.objects.filter(user__email=request.query_params.get("email")).first()

        if not request_profile:
            raise serializers.ValidationError({"User": "User not exist"})
        
        if user.friends.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "Already a friend"})
            
        if not user.pending_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "No pending request from this user"})

        user.friends.add(request_profile)
        user.pending_requests.remove(request_profile)
        request_profile.friends.add(user)
        request_profile.sent_requests.remove(user)
        user.save()
        request_profile.save()

        return attrs
    

class RejectRequestSerialiser(serializers.Serializer):
    def validate(self, attrs):
        request = self.context.get("request")
        user = UserProfile.objects.get(user=request.user)
        request_profile = UserProfile.objects.filter(user__email=request.query_params.get("email")).first()

        if not request_profile:
            raise serializers.ValidationError({"User": "User not exist"})
        
        if not user.pending_requests.filter(id=request_profile.id).exists():
            raise serializers.ValidationError({"User": "No such pending request to reject"})

        user.pending_requests.remove(request_profile)
        request_profile.sent_requests.remove(user)
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
