from django.urls import path, include
from rest_framework import routers

from api.views import UserViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include((router.urls, 'api'))),
]