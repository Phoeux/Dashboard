from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    end_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1), blank=True)
