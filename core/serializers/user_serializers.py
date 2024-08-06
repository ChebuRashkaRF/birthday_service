from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "birth_date"]
        extra_kwargs = {"birth_date": {"required": True, "allow_null": False}}
