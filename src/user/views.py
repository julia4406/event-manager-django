from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, \
    ListAPIView
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from event.serializers import EventSerializer
from user.serializers import UserSerializer
from user.user_cschema_decorators import user_schema_view, create_user_schema, \
    profile_schema, participated_events_schema, organized_events_schema


@extend_schema(tags=["(admin only) manage user profile"])
@user_schema_view()
class UserListViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name"
    ]


@create_user_schema()
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


@profile_schema()
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@participated_events_schema()
class ParticipatedEventsView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "title",
        "location",
        "organizer__username",
    ]
    filterset_fields = ["event_format", "event_date", "organizer"]
    ordering_fields = ["event_date", "title"]
    ordering = ["event_date"]

    def get_queryset(self):
        return self.request.user.events.all()


@organized_events_schema()
class OrganizedEventsView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "title",
        "location",
        "participants__username"
    ]
    filterset_fields = ["event_format", "event_date", "participants"]
    ordering_fields = ["event_date", "title"]
    ordering = ["event_date"]

    def get_queryset(self):
        return self.request.user.organized_events.all()
