from rest_framework import serializers
from .models import UserProfile


class ListFriendSerialiser(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = UserProfile
        fields = ["friends"]
