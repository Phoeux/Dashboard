from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import User, Task
from api.serializers import UserSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset
