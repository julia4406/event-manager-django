from django.urls import path, include
from rest_framework import routers

from user import views

router = routers.DefaultRouter()
router.register("manage", views.UserListViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.CreateUserView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile")
]

app_name = "user"
