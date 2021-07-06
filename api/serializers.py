from django.core.validators import MinValueValidator
from rest_framework import serializers

from api.models import User, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate(self, data):
        if data['end_time'] < data['start_time']:
            raise serializers.ValidationError({'end_time': "finish must occur after start"})

        for check in Task.objects.filter(user=data['user']):
            if check.start_time < data['start_time'] < check.end_time:
                raise serializers.ValidationError(
                    f'User {data["user"]} is busy from {check.start_time} up to {check.end_time}')
        return data
