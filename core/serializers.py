from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    birth_date = serializers.DateField()

    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
        )
