from django.contrib.auth import get_user_model
from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "event_date",
            "start_of_event",
            "location",
            "event_format",
            "organizer",
            "participants"
        ]
        read_only_fields = ["organizer"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if user.is_staff and "organizer" in validated_data:
            return super().create(validated_data)

        validated_data["organizer"] = user
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.user.is_staff:
            fields["organizer"].read_only = False
            fields["organizer"].queryset = get_user_model().objects.all()

        return fields

