from django.urls import path, include
from rest_framework import routers

from user import views
from user.views import ParticipatedEventsView, OrganizedEventsView

router = routers.DefaultRouter()
router.register("manage", views.UserListViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.CreateUserView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/participated-events/",
        ParticipatedEventsView.as_view(),
        name="participated-events"),
    path(
        "profile/organized-events/",
        OrganizedEventsView.as_view(),
        name="organized-events"
    )
]

app_name = "user"
