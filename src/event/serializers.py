import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from event.models import Event
from event.validators import EventValidators


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

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.user.is_staff:
            fields["organizer"].read_only = False
            fields["organizer"].queryset = get_user_model().objects.all()

        return fields

    def validate(self, data):
        """Validate if meeting don't planned in the past"""
        EventValidators.check_event_date_values(
            event_date=data.get("event_date"),
            start_of_event=data.get("start_of_event"),
        )
        return data

