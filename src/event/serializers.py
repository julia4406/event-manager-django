from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "event_date",
            "start_of_event",
            "location",
            "event_format",
            "organizer"
        ]
