from django.urls import path, include
from rest_framework import routers

from event import views

router = routers.DefaultRouter()
router.register("events", views.EventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "event"
