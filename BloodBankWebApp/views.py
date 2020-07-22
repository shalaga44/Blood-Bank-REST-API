from django.shortcuts import render

from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAdminUser
from BloodBankWebApp.models import User
from BloodBankWebApp.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
