from rest_framework.viewsets import ModelViewSet

from event.models import Event
from event.serializers import EventSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
