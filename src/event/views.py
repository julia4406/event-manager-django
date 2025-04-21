from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from event.event_schema_decorator import event_schema_view
from event.models import Event
from event.serializers import EventSerializer
from event.validators import EventValidators as validator
from event.tasks import send_event_registration_email


@event_schema_view()
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = [
        "title",
        "location",
        "organizer__username",
        "participants__username"
    ]
    filterset_fields = ["event_format", "event_date", "organizer", "participants"]
    ordering_fields = ["event_date", "title"]
    ordering = ["event_date"]

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff and "organizer" in serializer.validated_data:
            serializer.save(organizer=serializer.validated_data["organizer"])
        else:
            serializer.save(organizer=user)

    def perform_update(self, serializer):
        event = self.get_object()
        validator.check_permissions_for_event(self.request, event)
        serializer.save()

    def perform_destroy(self, instance):
        validator.check_permissions_for_event(self.request, instance)
        instance.delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(
        methods=["POST"],
        detail=True,
        url_path="register"
    )
    def event_registration(self, request, pk):
        event = self.get_object()
        validator.check_event_date(event)
        validator.already_registred(self.request, event)
        event.participants.add(request.user)
        send_event_registration_email.delay(request.user.email, event.title)
        return Response({"status": "registered"}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unregister"
    )
    def event_cancel_registration(self, request, pk=None):
        event = self.get_object()
        validator.check_event_date(event)
        validator.not_registred(request, event)
        event.participants.remove(request.user)
        return Response({"status": "unregistered"}, status=status.HTTP_200_OK)
