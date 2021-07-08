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

    def validate_end_time(self, data):
        if self.initial_data['end_time'] < self.initial_data['start_time']:
            raise serializers.ValidationError({'end_time': "finish must occur after start"})
        return data

    def validate_start_time(self, data):
        for check in Task.objects.filter(user_id=self.initial_data['user']):
            if check.start_time.strftime('%Y-%m-%dT%H:%M:%SZ') <= self.initial_data['start_time'] or \
                    self.initial_data['end_time'] <= check.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'):
                raise serializers.ValidationError(
                    f'User {check.user} is busy from {check.start_time} up to {check.end_time}')
            if check.start_time.strftime('%Y-%m-%dT%H:%M:%SZ') >= self.initial_data['start_time'] and \
                    self.initial_data['end_time'] >= check.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'):
                raise serializers.ValidationError(
                    f'User {check.user} is busy from {check.start_time} up to {check.end_time}')
        return data
