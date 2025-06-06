from django.contrib.auth import get_user_model
from rest_framework import serializers

from event.serializers import EventSerializer


class UserSerializer(serializers.ModelSerializer):
    participated_events = EventSerializer(
        many=True,
        read_only=True,
        source="events"
    )

    organized_events = EventSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "participated_events",
            "organized_events"
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
