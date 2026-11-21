from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class UserSerializer(UserDetailsSerializer):
    role = serializers.CharField(read_only=True)
    provider_id = serializers.CharField(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = ("pk", "email", "first_name", "last_name", "role", "provider_id")
        read_only_fields = ("email", "role", "provider_id")
