from django.contrib.auth import get_user_model
from rest_framework import serializers

from event.models import Event
from event.validators import validate_not_in_past


class EventSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "event_date",
            "is_all_day",
            "location",
            "event_format",
            "organizer",
            "participants"
        ]
        read_only_fields = ["organizer"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.user.is_staff:
            fields["organizer"].read_only = False
            fields["organizer"].queryset = get_user_model().objects.all()

        return fields

    def validate(self, data):
        event_date = data.get("event_date")
        if event_date:
            validate_not_in_past(event_date)
        return data
