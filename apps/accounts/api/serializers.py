from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """Detail serializer of User objetc"""
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'name', 'cellphone', 'token', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'token': {
                'read_only': True
            }
        }

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        """Create and return a new user"""
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        return user
