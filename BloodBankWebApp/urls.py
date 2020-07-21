from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from BloodBankWebApp.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
urlpatterns = [
    path("viewset/", include(router.urls)),
]
