from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser

from BloodBankWebApp.models import User
from BloodBankWebApp.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]